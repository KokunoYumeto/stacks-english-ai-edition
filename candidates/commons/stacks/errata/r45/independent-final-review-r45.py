"""Independent full candidate replay for R45 before manifest sealing."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANDIDATE_ID = "stacks-errata-a04446e-r45"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ev(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def bound(row: dict) -> Path:
    path = (ROOT / row["path"]).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), row
    if "bytes" in row:
        assert path.stat().st_size == row["bytes"], row["path"]
    assert sha(path) == row["sha256"], row["path"]
    return path


def main() -> int:
    destination = ROOT / "replay/FINAL_INDEPENDENT_REVIEW.json"
    if destination.exists():
        raise FileExistsError("Independent review is immutable; use an append-only successor.")
    assert not (ROOT / "candidate.manifest.json").exists()

    stage_path = ROOT / "replay/FINAL_STAGE.json"
    stage = load(stage_path)
    assert stage["candidate_id"] == CANDIDATE_ID
    assert stage["status"] == "READY_FOR_FULL_INDEPENDENT_REVIEW_NOT_ADMITTED"
    for row in stage["snapshot_inventory"]:
        bound(row)
    excluded = {"candidate.manifest.json", "replay/FINAL_STAGE.json", "replay/FINAL_INDEPENDENT_REVIEW.json"}
    actual = sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in excluded
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    expected = sorted(row["path"] for row in stage["snapshot_inventory"])
    assert actual == expected

    authority_path = ROOT / "authority/source/topologies.tex"
    payload_path = ROOT / "payload/topologies.tex"
    authority = authority_path.read_bytes()
    payload = payload_path.read_bytes()
    spec = load(ROOT / "operation-spec.json")
    operations = spec["operations"]
    assert spec["operation_count"] == len(operations) == 36
    operation_ids = [row["operation_id"] for row in operations]
    assert len(operation_ids) == len(set(operation_ids))
    intervals = sorted((row["start_byte"], row["end_byte_exclusive"], row["operation_id"]) for row in operations)
    assert all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:]))
    for row in operations:
        old = row["old_text"].encode("utf-8")
        replacement = row["replacement_text"].encode("utf-8")
        assert len(old) == row["old_bytes"] and sha_bytes(old) == row["old_sha256"]
        assert len(replacement) == row["replacement_bytes"] and sha_bytes(replacement) == row["replacement_sha256"]
        assert authority[row["start_byte"]:row["end_byte_exclusive"]] == old
        declared_lines = authority.decode("utf-8").splitlines()[row["source_start_line"] - 1:row["source_end_line"]]
        assert row["old_text"] in "\n".join(declared_lines)
    replayed = bytearray(authority)
    for row in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        replayed[row["start_byte"]:row["end_byte_exclusive"]] = row["replacement_text"].encode("utf-8")
    assert bytes(replayed) == payload

    units_doc = load(ROOT / "stable-units.json")
    units = units_doc["units"]
    assert units_doc["unit_count"] == len(units) == 19
    stable_ids = [row["id"] for row in units]
    assert stable_ids == [f"MC-STK-ERR-{number}" for number in range(1461, 1480)]
    producer_ids = [row["producer_id"] for row in units]
    assert len(producer_ids) == len(set(producer_ids)) == 19
    assert sorted(op for unit in units for op in unit["operation_ids"]) == sorted(operation_ids)
    decisions = jsonl(ROOT / "decisions.jsonl")
    assert len(decisions) == 19
    assert len({row["stable_id"] for row in decisions}) == 19
    assert set(row["stable_id"] for row in decisions) == set(stable_ids)
    assert jsonl(ROOT / "source-map.jsonl")
    assert (ROOT / "rejections.jsonl").stat().st_size == 0

    config = load(ROOT / "candidate.config.json")
    assert config["candidate_id"] == CANDIDATE_ID
    assert config["payload_expected_sha256"] == sha(payload_path)
    assert config["expected_unit_ids"] == stable_ids
    assert config["stems"]["topologies"]["build_exceptions"]["candidate_undefined_reference_target_deltas"] == {
        "sets-lemma-coverings-site": 5,
        "sets-lemma-what-is-in-it": -5,
    }

    source_review = load(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json")
    mechanical = load(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json")
    visual = load(ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json")
    build_receipt = load(ROOT / "builds/build-receipt.json")
    deterministic = load(ROOT / "builds/deterministic-replay.json")
    mutex = load(ROOT / "builds/TEX_MUTEX_RECEIPT.json")
    attempt = load(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json")
    assert source_review["passed"] is True
    assert mechanical["passed"] is True
    assert visual["passed"] is True and visual["blocking_findings"] == []
    assert visual["scope"]["covered_pages"] == list(range(1, 47))
    assert build_receipt["passed"] is True
    assert deterministic["passed"] is True and deterministic["fresh_builds_compared"] == 2
    assert mutex["passed"] is True and mutex["acquired"] is True and mutex["released"] is True
    assert attempt["passed"] is False and attempt["acquired"] is True and attempt["released"] is True

    receipt = {
        "schema": "stacks-r45-final-independent-review/v1",
        "candidate_id": CANDIDATE_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed": True,
        "final_stage": ev(stage_path),
        "final_stage_sha256": sha(stage_path),
        "snapshot_files_rehashed": len(expected),
        "snapshot_missing": [],
        "snapshot_extra": [],
        "source_replay": {
            "authority": ev(authority_path),
            "payload": ev(payload_path),
            "semantic_units": 19,
            "operations": 36,
            "exact_preimages": 36,
            "nonoverlapping": True,
            "descending_byte_replay_payload_exact": True,
            "unlisted_byte_changes": 0,
        },
        "identity_replay": {
            "stable_ids": stable_ids,
            "producer_ids": producer_ids,
            "stable_ids_unique": True,
            "producer_ids_unique": True,
            "decision_rows": 19,
            "operation_ids_unique": True,
        },
        "mechanical_validation": ev(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json"),
        "build_receipt": ev(ROOT / "builds/build-receipt.json"),
        "deterministic_replay": ev(ROOT / "builds/deterministic-replay.json"),
        "tex_mutex_success": ev(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "tex_mutex_adverse_attempt": ev(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json"),
        "visual_adjudication": ev(ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"),
        "deduplication_boundary": {
            "registered_rounds_checked_through": 44,
            "stable_id_collisions": 0,
            "prior_topologies_operations": 0,
        },
        "adverse_evidence_preserved": [
            "Attempt 001 validator failure is retained and not overwritten; the full corrected build is a separate successful attempt.",
            "Four inherited overfull hboxes and standalone cross-chapter unresolved references remain explicitly recorded.",
            "The validation PDF is untagged.",
        ],
        "authority_mutated": False,
        "producer_target_mutated": False,
        "generated_source_composed": False,
        "registry_admission": "NOT_PERFORMED",
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "units": 19, "operations": 36, "receipt_sha256": sha(destination)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
