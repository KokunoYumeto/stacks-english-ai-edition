from __future__ import annotations

import bisect
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[4]
STAMP = "2026-08-29T20:45:00Z"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def line_starts(data: bytes) -> list[int]:
    return [0] + [index + 1 for index, byte in enumerate(data) if byte == 10]


def line_at(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def main() -> int:
    config = read_json(ROOT / "candidate.config.json")
    stable_doc = read_json(ROOT / "stable-units.json")
    operation_doc = read_json(ROOT / "operation-spec.json")
    source_map = read_jsonl(ROOT / "source-map.jsonl")
    decisions = read_jsonl(ROOT / "decisions.jsonl")
    rejections = read_jsonl(ROOT / "rejections.jsonl")
    validation = read_json(ROOT / "source-validation.json")
    inventory = read_json(ROOT / "formula-diagram-inventory.json")

    expected = [
        *(f"MC-STK-ERR-{number:04d}" for number in range(338, 346)),
        "MC-STK-ERR-0396",
        *(f"MC-STK-ERR-{number:04d}" for number in range(399, 493)),
    ]
    assert config["candidate_id"] == "stacks-errata-a04446e-r32"
    assert config["expected_unit_ids"] == expected
    assert config["accepted"] == len(expected) == 103
    assert config["rejected"] == config["unresolved"] == 0
    assert config["operation_count"] == 125
    assert config["materialization_only"] is True
    assert config["composition_performed"] is False

    units = stable_doc["units"]
    assert stable_doc["unit_count"] == len(units) == 103
    assert [unit["id"] for unit in units] == expected
    assert len({unit["id"] for unit in units}) == 103
    assert len({unit["producer_id"] for unit in units}) == 103
    assert [unit["producer_id"] for unit in units] == config["expected_producer_ids"]
    assert all(unit["status"] == "accepted_prior_round_materialized_r32" for unit in units)

    operations = operation_doc["operations"]
    assert operation_doc["operation_count"] == len(operations) == 125
    assert operation_doc["apply_order"] == "descending_start_byte_per_source"
    operation_ids = [row["operation_id"] for row in operations]
    assert len(operation_ids) == len(set(operation_ids))
    operation_by_id = {row["operation_id"]: row for row in operations}
    unit_by_id = {unit["id"]: unit for unit in units}
    assert set(operation_by_id) == {
        operation_id for unit in units for operation_id in unit["operation_ids"]
    }
    for stable_id, unit in unit_by_id.items():
        unit_operations = [operation_by_id[operation_id] for operation_id in unit["operation_ids"]]
        assert [row["operation_index_within_unit"] for row in unit_operations] == list(
            range(1, len(unit_operations) + 1)
        )
        assert all(row["stable_id"] == stable_id for row in unit_operations)
        assert all(row["producer_id"] == unit["producer_id"] for row in unit_operations)
        assert all(row["source"] == unit["source"] for row in unit_operations)

    assert len(source_map) == 103
    assert [row["unit_id"] for row in source_map] == expected
    for row in source_map:
        unit = unit_by_id[row["unit_id"]]
        assert row["producer_id"] == unit["producer_id"]
        assert [item["operation_id"] for item in row["operations"]] == unit["operation_ids"]
        assert row["proof"] == "prior_acceptance_replayed_against_frozen_authority"

    with (ROOT / "authority" / "producer" / "accepted-unmaterialized.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        accepted_rows = list(csv.DictReader(handle))
    assert len(accepted_rows) == 103
    assert [row["id"] for row in accepted_rows] == config["expected_producer_ids"]
    assert all("accepted" in row["status"] for row in accepted_rows)
    assert all(row["authority_sha256"] == config["stems"][row["source_file"]]["authority_sha256"] for row in accepted_rows)

    assert len(decisions) == 4
    assert len({row["id"] for row in decisions}) == 4
    assert rejections == []
    assert validation["passed"] is True
    assert validation["accepted_units"] == 103
    assert validation["operation_count"] == 125
    assert validation["composition_performed"] is False
    assert inventory["classified_units"] == expected
    assert inventory["unmapped_formula_or_diagram_changes"] == 0

    replay: dict[str, dict] = {}
    by_source: dict[str, list[dict]] = defaultdict(list)
    for row in operations:
        by_source[row["source"]].append(row)
    assert Counter(row["source"] for row in operations) == Counter(
        {"fields.tex": 9, "categories.tex": 1, "algebra.tex": 115}
    )
    for source in ("fields.tex", "categories.tex", "algebra.tex"):
        authority = (ROOT / "authority" / "source" / source).read_bytes()
        payload = (ROOT / "payload" / source).read_bytes()
        stem = config["stems"][source]
        assert len(authority) == stem["authority_bytes"]
        assert sha(authority) == stem["authority_sha256"]
        assert len(payload) == stem["payload_bytes"]
        assert sha(payload) == stem["payload_sha256"]
        rows = sorted(by_source[source], key=lambda row: row["start_byte"])
        assert len(rows) == stem["operations"]
        starts = line_starts(authority)
        for left, right in zip(rows, rows[1:]):
            assert left["end_byte_exclusive"] <= right["start_byte"]
        for row in rows:
            old = row["old_text"].encode("utf-8")
            new = row["replacement_text"].encode("utf-8")
            assert authority[row["start_byte"]:row["end_byte_exclusive"]] == old
            assert row["old_bytes"] == len(old)
            assert row["old_sha256"] == sha(old)
            assert row["replacement_bytes"] == len(new)
            assert row["replacement_sha256"] == sha(new)
            assert row["occurrence_count_in_frozen_authority"] == authority.count(old)
            assert line_at(starts, row["start_byte"]) == row["source_start_line"]
            assert line_at(starts, max(row["start_byte"], row["end_byte_exclusive"] - 1)) == row["source_end_line"]
        scratch = authority
        for row in reversed(rows):
            old = row["old_text"].encode("utf-8")
            new = row["replacement_text"].encode("utf-8")
            assert scratch[row["start_byte"]:row["end_byte_exclusive"]] == old
            scratch = scratch[:row["start_byte"]] + new + scratch[row["end_byte_exclusive"]:]
        assert scratch == payload
        replay[source] = {
            "passed": True,
            "operation_count": len(rows),
            "authority_bytes": len(authority),
            "authority_sha256": sha(authority),
            "payload_bytes": len(payload),
            "payload_sha256": sha(payload),
        }

    registry_path = REPOSITORY / "registry" / "overlays.json"
    registry_bytes = registry_path.read_bytes()
    registry = json.loads(registry_bytes)
    entries = registry["registered_entries"]
    all_prior_stable = [stable for entry in entries for stable in entry.get("stable_ids", [])]
    assert not (set(expected) & set(all_prior_stable))
    assert all(entry["id"] != config["candidate_id"] for entry in entries)
    assert entries[-1]["id"] == "stacks-errata-a04446e-r31"

    review = {
        "schema": "mathematics-commons-stacks-errata-independent-review/v1",
        "candidate_id": config["candidate_id"],
        "review_kind": "independent_exact_preimage_and_payload_replay",
        "recorded_at_utc": STAMP,
        "result": "PASS",
        "conclusion": "UNCONDITIONAL PASS",
        "passed": True,
        "pass_is_unconditional": True,
        "stable_id_recomputation": {
            "passed": True,
            "unit_count": 103,
            "first_id": expected[0],
            "last_id": expected[-1],
            "nonconsecutive_historical_ids_preserved": True,
            "stable_ids": expected,
        },
        "prior_acceptance_evidence": {
            "passed": True,
            "accepted_row_count": 103,
            "producer_ids_unique": 103,
            "status_rule": "every bounded producer row retains an accepted or provisionally accepted status",
            "path": "authority/producer/accepted-unmaterialized.csv",
            "sha256": sha((ROOT / "authority" / "producer" / "accepted-unmaterialized.csv").read_bytes()),
        },
        "scratch_replay": {
            "passed": True,
            "apply_order": "descending_start_byte_per_source",
            "operation_count": 125,
            "stems": replay,
        },
        "closure_checks": {
            "passed": True,
            "stable_units": 103,
            "source_map_rows": 103,
            "decision_rows": 4,
            "rejection_rows": 0,
            "operation_ids": 125,
            "operation_ids_unique": 125,
            "authority_sources": 3,
            "payload_sources": 3,
        },
        "registry_pre_admission": {
            "passed": True,
            "path": "registry/overlays.json",
            "bytes": len(registry_bytes),
            "sha256": sha(registry_bytes),
            "last_overlay": entries[-1]["id"],
            "r32_absent": True,
            "stable_id_collisions": 0,
        },
        "constraints_observed": {
            "upstream_authority_mutated": False,
            "generated_source_composed": False,
            "generated_source_pushed": False,
            "registry_mutated_by_review": False,
            "persistent_writes": ["replay/independent-review.json"],
        },
        "adverse_observations": [
            "These 103 stable IDs were allocated in earlier adjudication but had no registered payload; R32 supplies the missing exact materialization without renumbering or reopening them.",
            "R32 is a source-overlay replay gate only. Cumulative English source composition and chapter/PDF build validation remain the separate composer's responsibility.",
            "The overlay contains no correction for rejected ALGEBRA-007 and no newly adjudicated semantic unit.",
        ],
    }
    output = ROOT / "replay" / "independent-review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({
        "passed": True,
        "candidate_id": config["candidate_id"],
        "stable_units": 103,
        "operations": 125,
        "review_sha256": sha(output.read_bytes()),
        "stems": replay,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
