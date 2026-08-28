from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1202, 1216)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
    source_map = load_jsonl(ROOT / "source-map.jsonl")
    operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
    intake = json.loads((ROOT / "INTAKE_VALIDATION.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "R27_MODULES_ADJUDICATION_SPEC.json").read_text(encoding="utf-8"))
    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    authority_path = ROOT / "authority/source/modules.tex"
    payload_path = ROOT / "payload/modules.tex"
    authority = authority_path.read_bytes()
    payload = payload_path.read_bytes()

    if config["candidate_id"] != "stacks-errata-a04446e-r27":
        raise AssertionError("wrong candidate identity")
    if config["expected_unit_ids"] != EXPECTED_IDS:
        raise AssertionError("stable IDs are not contiguous 1202..1215")
    if config["accepted"] != 14 or config["operation_count"] != 14:
        raise AssertionError("sealed R27 counts are wrong")
    if config["rejected"] or config["unresolved"] or config["prior_alias_producer_ids"]:
        raise AssertionError("R27 unexpectedly contains rejects, unresolved units, or aliases")
    if lease["lease_id"] != config["lease_id"] or lease["namespace"] != config["namespace"]:
        raise AssertionError("lease/config mismatch")
    if (
        len(authority) != config["stems"]["modules"]["authority_bytes"]
        or sha_bytes(authority) != config["stems"]["modules"]["authority_sha256"]
        or len(payload) != config["stems"]["modules"]["payload_bytes"]
        or sha_bytes(payload) != config["stems"]["modules"]["payload_sha256"]
    ):
        raise AssertionError("authority or payload identity mismatch")

    for evidence in config["authority_evidence"]:
        path = ROOT / evidence["path"]
        if not path.is_file() or path.stat().st_size != evidence["bytes"] or file_sha(path) != evidence["sha256"]:
            raise AssertionError(f"authority evidence mismatch: {evidence['path']}")
    if (
        intake["status"] != "PASS"
        or intake["adjudication_spec_sha256"] != file_sha(ROOT / "R27_MODULES_ADJUDICATION_SPEC.input.json")
        or spec["semantic_unit_count"] != 14
        or spec["operation_count"] != 14
        or spec["accepted_producer_row_count"] != 14
        or spec["rejected"]
        or spec["prior_aliases"]
        or spec["unresolved"]
    ):
        raise AssertionError("intake/spec closure mismatch")

    stable_ids = [row["id"] for row in stable["units"]]
    map_ids = [row["unit_id"] for row in source_map]
    producers = [row["producer_id"] for row in source_map]
    if (
        stable["unit_count"] != 14
        or stable_ids != EXPECTED_IDS
        or map_ids != EXPECTED_IDS
        or producers != config["expected_producer_ids"]
        or producers != config["expected_all_producer_ids"]
        or len(set(producers)) != 14
    ):
        raise AssertionError("stable/source-map/producer closure mismatch")

    operations = operation_spec["operations"]
    mapped_operations = [operation for unit in source_map for operation in unit["operations"]]
    if operation_spec.get("operation_count") != 14 or len(operations) != 14:
        raise AssertionError("operation-spec count mismatch")
    if [row["operation_id"] for row in operations] != [row["operation_id"] for row in mapped_operations]:
        raise AssertionError("operation-spec/source-map order mismatch")
    intervals: list[tuple[int, int, str]] = []
    for operation, mapped in zip(operations, mapped_operations):
        keys = {
            "operation_id", "source_start_line", "source_end_line", "start_byte",
            "end_byte_exclusive", "old_text", "replacement_text", "old_sha256",
            "replacement_sha256", "occurrence_count_in_frozen_authority",
        }
        if any(operation[key] != mapped[key] for key in keys):
            raise AssertionError(f"mapped operation mismatch: {operation['operation_id']}")
        start, end = operation["start_byte"], operation["end_byte_exclusive"]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if authority[start:end] != old:
            raise AssertionError(f"authority interval mismatch: {operation['operation_id']}")
        if authority[:start].count(b"\n") + 1 != operation["source_start_line"]:
            raise AssertionError(f"start-line mismatch: {operation['operation_id']}")
        if authority[: max(start, end - 1)].count(b"\n") + 1 != operation["source_end_line"]:
            raise AssertionError(f"end-line mismatch: {operation['operation_id']}")
        if authority.count(old) != operation["occurrence_count_in_frozen_authority"]:
            raise AssertionError(f"occurrence-count mismatch: {operation['operation_id']}")
        if sha_bytes(old) != operation["old_sha256"] or sha_bytes(replacement) != operation["replacement_sha256"]:
            raise AssertionError(f"span-hash mismatch: {operation['operation_id']}")
        intervals.append((start, end, operation["operation_id"]))
    ordered = sorted(intervals)
    for left, right in zip(ordered, ordered[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlap: {left[2]} / {right[2]}")
    expected = authority
    by_id = {row["operation_id"]: row for row in operations}
    for start, end, operation_id in sorted(intervals, reverse=True):
        operation = by_id[operation_id]
        expected = expected[:start] + operation["replacement_text"].encode("utf-8") + expected[end:]
    if expected != payload:
        raise AssertionError("payload contains changes outside the 14 mapped operations")

    structural_patterns = {
        "labels": re.compile(rb"\\label\{[^{}]+\}"),
        "references": re.compile(rb"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
        "citations": re.compile(rb"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
        "environments": re.compile(rb"\\(?:begin|end)\{[^{}]+\}"),
        "sections": re.compile(rb"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
    }
    structure = {}
    for name, pattern in structural_patterns.items():
        before, after = pattern.findall(authority), pattern.findall(payload)
        if before != after:
            raise AssertionError(f"ordered {name} changed")
        structure[name] = len(before)
    if authority.count(rb"\xymatrix") != payload.count(rb"\xymatrix"):
        raise AssertionError("xymatrix count changed")
    if authority.count(b"$$") != payload.count(b"$$"):
        raise AssertionError("display delimiter count changed")

    report = {
        "schema": "mathematics-commons-stacks-errata-source-validation/v1",
        "candidate_id": config["candidate_id"],
        "passed": True,
        "verifier_sha256": file_sha(Path(__file__)),
        "authority": {"bytes": len(authority), "sha256": sha_bytes(authority)},
        "payload": {"bytes": len(payload), "sha256": sha_bytes(payload)},
        "units": 14,
        "operations": 14,
        "producer_identities": 14,
        "rejected": 0,
        "aliases": 0,
        "unresolved": 0,
        "ordered_structure": structure,
        "display_delimiters": authority.count(b"$$"),
        "xymatrix_count": authority.count(rb"\xymatrix"),
        "checks": {
            "authority_evidence": True,
            "intake_and_spec_closure": True,
            "stable_unit_and_producer_closure": True,
            "exact_bounded_preimages": True,
            "nonoverlapping_operations": True,
            "descending_payload_replay": True,
            "ordered_structure_preserved": True,
        },
    }
    write_json(ROOT / "source-validation.json", report)
    print(json.dumps({
        "passed": True,
        "units": 14,
        "operations": 14,
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
