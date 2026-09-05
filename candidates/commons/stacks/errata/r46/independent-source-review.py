"""Independent exact-byte replay of the already materialized R46 source stage."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
SOURCE = "groupoids.tex"
AUTH_SHA = "157CC1C792F41465B8249582FEE0F6DFF266AC4224F06B05E936C66C65DB043A"
PAYLOAD_SHA = "6ED98A884E9F4AD6C3EF6720AE538F1FEFEED24E09E60111B1F9D825CF1A7C04"
INTAKE_SHA = "83000418E293CE4C9D841C7F40AC8114F716BDF506F9A573227060075EF29243"
EXPECTED_IDS = [f"MC-STK-ERR-{number}" for number in range(1480, 1523)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evidence(relative: str) -> dict:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)}


def lines(path: Path) -> list[dict]:
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines() if row]


def all_occurrences(data: bytes, needle: bytes) -> list[int]:
    result = []
    cursor = 0
    while True:
        found = data.find(needle, cursor)
        if found < 0:
            return result
        result.append(found)
        cursor = found + len(needle)


def main() -> int:
    authority = (ROOT / f"authority/source/{SOURCE}").read_bytes()
    payload = (ROOT / f"payload/{SOURCE}").read_bytes()
    assert len(authority) == 189166 and sha_bytes(authority) == AUTH_SHA
    assert len(payload) == 189152 and sha_bytes(payload) == PAYLOAD_SHA

    lease = load(ROOT / "LEASE.json")
    assert lease["lease_id"] == "stacks-lease-000050-errata-r46"
    assert lease["status"] == "active" and lease["admission_status"] == "not_admitted"
    events = load(REPO / "registry/leases.json")["events"]
    matched = [row for row in events if row["lease_id"] == lease["lease_id"]]
    assert len(matched) == 1 and matched[0]["event"] == "issued" and matched[0]["state"] == "active"

    intake = load(ROOT / "authority/intake/STACKS_GROUPOIDS_INDEPENDENT_INTAKE_20260905_R1.json")
    assert intake["summary"]["accepted"] == 43
    assert intake["summary"]["accepted_operations"] == 46
    assert intake["summary"]["rejected"] == 4
    assert intake["summary"]["duplicates_against_R1_R45"] == 0
    adjudication = load(ROOT / "authority/registrar/GROUPOIDS_R46_INDEPENDENT_ADJUDICATION_20260905.json")
    assert adjudication["passed"] is True and len(adjudication["rows"]) == 43
    original = {row["logical_path"]: row for row in adjudication["intake_originals"]}
    assert any(row["sha256"] == INTAKE_SHA and row["bytes"] == 60278 for row in original.values())

    spec = load(ROOT / "operation-spec.json")
    spec_input = load(ROOT / "operation-spec.input.json")
    stable = load(ROOT / "stable-units.json")
    stable_input = load(ROOT / "stable-units.input.json")
    source_map = lines(ROOT / "source-map.jsonl")
    source_map_input = lines(ROOT / "source-map.input.jsonl")
    decisions = lines(ROOT / "decisions.jsonl")
    decisions_input = lines(ROOT / "decisions.input.jsonl")
    rejections = lines(ROOT / "rejections.jsonl")
    rejections_input = lines(ROOT / "rejections.input.jsonl")
    assert spec == spec_input and stable == stable_input
    assert source_map == source_map_input and decisions == decisions_input and rejections == rejections_input
    assert len(rejections) == 4
    assert spec["operation_count"] == len(spec["operations"]) == 46
    assert stable["unit_count"] == len(stable["units"]) == 43
    assert [row["id"] for row in stable["units"]] == EXPECTED_IDS
    assert [row["unit_id"] for row in source_map] == EXPECTED_IDS
    assert [row["stable_id"] for row in decisions[:43]] == EXPECTED_IDS
    assert len({row["producer_id"] for row in stable["units"]}) == 43
    assert all(row["choice"] == "materialize_source_proposal_not_admission" for row in decisions[:43])
    assert all(row["choice"] == "reject_producer_proposal" for row in decisions[43:])

    operations = spec["operations"]
    assert len({row["operation_id"] for row in operations}) == 46
    assert len({row["producer_operation_id"] for row in operations}) == 46
    ordered = sorted(operations, key=lambda row: row["start_byte"])
    assert all(left["end_byte_exclusive"] <= right["start_byte"] for left, right in zip(ordered, ordered[1:]))
    first_locus = {
        row["id"]: min(op["start_byte"] for op in operations if op["stable_id"] == row["id"])
        for row in stable["units"]
    }
    assert [first_locus[key] for key in EXPECTED_IDS] == sorted(first_locus.values())

    replay = authority
    unchanged_parts = []
    cursor = 0
    for operation in ordered:
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        assert authority[start:end] == old
        assert len(old) == operation["old_bytes"] and sha_bytes(old) == operation["old_sha256"]
        assert len(replacement) == operation["replacement_bytes"]
        assert sha_bytes(replacement) == operation["replacement_sha256"]
        found = all_occurrences(authority, old)
        assert len(found) == operation["file_occurrences"]
        actual_line = authority[:start].count(b"\n") + 1
        assert actual_line == operation["line"] == operation["source_start_line"]
        assert operation["source_end_line"] in {
            actual_line + old.count(b"\n"),
            actual_line + old.count(b"\n") - int(old.endswith(b"\n")),
        }
        assert sum(authority[:value].count(b"\n") + 1 == actual_line for value in found) == 1
        unchanged_parts.append(authority[cursor:start])
        cursor = end
    unchanged_parts.append(authority[cursor:])
    for operation in reversed(ordered):
        replay = (
            replay[: operation["start_byte"]]
            + operation["replacement_text"].encode("utf-8")
            + replay[operation["end_byte_exclusive"] :]
        )
    assert replay == payload

    by_stable = {row["id"]: row for row in stable["units"]}
    by_map = {row["unit_id"]: row for row in source_map}
    for stable_id in EXPECTED_IDS:
        unit = by_stable[stable_id]
        mapped = by_map[stable_id]
        expected_ops = [row for row in operations if row["stable_id"] == stable_id]
        assert unit["operation_ids"] == [row["operation_id"] for row in expected_ops]
        assert mapped["operations"] == expected_ops
        assert mapped["authority_sha256"] == AUTH_SHA
        assert unit["producer_id"] == mapped["producer_id"]
        assert unit["class"] == mapped["class"]

    patterns = {
        "labels": rb"\\label\{[^}]*\}",
        "refs": rb"\\(?:ref|eqref)\{[^}]*\}",
        "environments": rb"\\(?:begin|end)\{[^}]*\}",
        "inputs": rb"\\input\{[^}]*\}",
        "cites": rb"\\cite(?:\[[^]]*\])?\{[^}]*\}",
    }
    structure = {}
    for key, pattern in patterns.items():
        before = re.findall(pattern, authority)
        after = re.findall(pattern, payload)
        assert len(before) == len(after)
        differences = [index for index, pair in enumerate(zip(before, after)) if pair[0] != pair[1]]
        assert not differences
        structure[key] = {
            "authority": len(before),
            "candidate": len(after),
            "count_equal": True,
            "ordered_equal": not differences,
            "declared_changed_positions": differences,
        }
    dollar_delta = payload.count(b"$") - authority.count(b"$")
    assert dollar_delta == 10

    prior_groupoids = overlaps = preimage_hits = stable_collisions = 0
    target_intervals = [(row["start_byte"], row["end_byte_exclusive"]) for row in operations]
    target_preimages = {row["old_text"] for row in operations}
    for path in (REPO / "candidates").rglob("source-map.jsonl"):
        if ROOT in path.resolve().parents:
            continue
        for row in lines(path):
            stable_collisions += int(row.get("unit_id") in EXPECTED_IDS)
            for prior in row.get("operations", []):
                if prior.get("source") != SOURCE:
                    continue
                prior_groupoids += 1
                preimage_hits += int(prior.get("old_text") in target_preimages)
                overlaps += sum(
                    not (prior["end_byte_exclusive"] <= start or end <= prior["start_byte"])
                    for start, end in target_intervals
                )
    assert prior_groupoids == overlaps == preimage_hits == stable_collisions == 0

    validation = load(ROOT / "source-validation.json")
    assert validation["passed"] is True
    assert validation["authority"]["sha256"] == AUTH_SHA
    assert validation["payload"]["sha256"] == PAYLOAD_SHA
    assert validation["unchanged_interval_sha256"] == sha_bytes(b"".join(unchanged_parts))
    assert validation["structure"] == structure

    result = {
        "schema": "stacks-r46-independent-source-validation/v1",
        "candidate_id": "stacks-errata-a04446e-r46",
        "status": "PASS_SOURCE_ONLY",
        "passed": True,
        "scope": "Independent read-only reconstruction of the R46 source stage before any build or admission.",
        "authority": evidence(f"authority/source/{SOURCE}"),
        "payload": evidence(f"payload/{SOURCE}"),
        "operation_spec": evidence("operation-spec.json"),
        "stable_units": evidence("stable-units.json"),
        "source_map": evidence("source-map.jsonl"),
        "decisions": evidence("decisions.jsonl"),
        "adjudication": evidence("authority/registrar/GROUPOIDS_R46_INDEPENDENT_ADJUDICATION_20260905.json"),
        "source_validation": evidence("source-validation.json"),
        "replay": {
            "semantic_units": 43,
            "exact_operations": 46,
            "exact_preimages": 46,
            "nonoverlap": True,
            "payload_byte_exact": True,
            "unlisted_byte_changes": 0,
            "unchanged_interval_sha256": sha_bytes(b"".join(unchanged_parts)),
            "stable_ids_first_locus_ordered": True,
            "structure": structure,
            "dollar_delimiters": {
                "authority": authority.count(b"$"),
                "candidate": payload.count(b"$"),
                "declared_operation_bound_delta": dollar_delta,
            },
        },
        "deduplication": {
            "registered_rounds_checked_through": 45,
            "prior_groupoids_operations": prior_groupoids,
            "interval_overlaps": overlaps,
            "exact_preimage_hits": preimage_hits,
            "stable_id_collisions": stable_collisions,
        },
        "build": "NOT_PERFORMED",
        "admission": "NOT_PERFORMED",
        "composition": "NOT_PERFORMED",
    }
    output = ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "units": 43, "operations": 46, "rejected": 4, "payload_sha256": PAYLOAD_SHA}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
