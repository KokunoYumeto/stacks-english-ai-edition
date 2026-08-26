from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "source-validation.json"
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
STRUCTURE_PATTERNS = {
    "labels": re.compile(rb"\\label\{[^{}]+\}"),
    "references": re.compile(rb"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(rb"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
    "environments": re.compile(rb"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(rb"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.name}:{line_number}: {exc}") from exc
    return rows


def exact_payload(stem: str, rows: list[dict]) -> dict:
    authority = (ROOT / "authority" / "source" / f"{stem}.tex").read_bytes()
    payload = (ROOT / "payload" / f"{stem}.tex").read_bytes()
    operations: list[tuple[int, int, bytes, bytes, str]] = []
    for row in rows:
        if row["source"] != f"{stem}.tex":
            continue
        for operation in row["operations"]:
            old = operation["old_text"].encode("utf-8")
            new = operation["replacement_text"].encode("utf-8")
            start = operation["start_byte"]
            end = operation["end_byte_exclusive"]
            if authority[start:end] != old:
                raise AssertionError(f"{operation['operation_id']}: authority interval mismatch")
            start_line = authority[:start].count(b"\n") + 1
            end_line = authority[: max(start, end - 1)].count(b"\n") + 1
            if start_line != operation["source_start_line"] or end_line != operation["source_end_line"]:
                raise AssertionError(f"{operation['operation_id']}: line metadata mismatch")
            if authority.count(old) != operation["occurrence_count_in_frozen_authority"]:
                raise AssertionError(f"{operation['operation_id']}: occurrence-count mismatch")
            if sha_bytes(old) != operation["old_sha256"] or sha_bytes(new) != operation["replacement_sha256"]:
                raise AssertionError(f"{operation['operation_id']}: span-hash mismatch")
            operations.append((start, end, old, new, operation["operation_id"]))
    ascending = sorted(operations)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[4]} / {right[4]}")
    replay = authority
    for start, end, old, new, operation_id in sorted(operations, reverse=True):
        if replay[start:end] != old:
            raise AssertionError(f"{operation_id}: descending replay interval changed")
        replay = replay[:start] + new + replay[end:]
    if replay != payload:
        raise AssertionError(f"{stem}: payload contains changes outside the mapped operations")

    structure: dict[str, dict[str, int]] = {}
    exceptions = CONFIG["stems"][stem].get("ordered_structure_exceptions", {})
    for name, pattern in STRUCTURE_PATTERNS.items():
        before = pattern.findall(authority)
        after = pattern.findall(payload)
        expected = exceptions.get(name, [])
        differences = [(index, old, new) for index, (old, new) in enumerate(zip(before, after)) if old != new]
        declared = [
            (row["index_0based"], row["authority"].encode("utf-8"), row["payload"].encode("utf-8"))
            for row in expected
        ]
        if len(before) != len(after) or differences != declared:
            raise AssertionError(f"{stem}: ordered {name} changed outside declared exceptions")
        structure[name] = {"authority": len(before), "payload": len(after)}
    expected_display_delta = CONFIG["stems"][stem]["display_delimiter_delta"]
    if payload.count(b"$$") - authority.count(b"$$") != expected_display_delta:
        raise AssertionError(f"{stem}: display-delimiter delta mismatch")
    if payload.count(rb"\xymatrix") != authority.count(rb"\xymatrix"):
        raise AssertionError(f"{stem}: xymatrix count changed")
    return {
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
        "operation_count": len(operations),
        "ordered_structure": structure,
        "display_delimiter_delta": expected_display_delta,
        "xymatrix_count": authority.count(rb"\xymatrix"),
    }


def public_hygiene() -> dict:
    private_root = re.compile(re.escape("C:") + r"(?:\\+|/+)" + "Us" + "ers" + r"(?:\\+|/+)", re.I)
    checked = 0
    for pattern in ("*.md", "*.json", "*.jsonl", "*.csv", "*.txt", "*.py"):
        for path in ROOT.rglob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            if private_root.search(text):
                raise AssertionError(f"private local marker remains: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".json":
                json.loads(text)
            elif path.suffix.lower() == ".jsonl":
                for line in text.splitlines():
                    if line.strip():
                        json.loads(line)
            checked += 1
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    if caches:
        raise AssertionError(f"Python caches remain: {caches}")
    return {"passed": True, "text_files": checked, "python_caches": 0}


def main() -> int:
    report = {
        "schema": "mathematics-commons-stacks-errata-source-validation/v1",
        "candidate_id": CONFIG["candidate_id"],
        "authority_commit": CONFIG["authority_commit"],
        "generated_at_utc": "2026-08-25T20:33:58Z",
        "verifier_sha256": sha256(Path(__file__)),
        "scope": "source_only_no_build_or_render",
        "passed": False,
        "checks": {},
    }
    try:
        for row in CONFIG["authority_evidence"]:
            path = ROOT / row["path"]
            if not path.is_file() or path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
                raise AssertionError(f"authority evidence mismatch: {row['path']}")
        report["checks"]["authority_evidence"] = {"passed": True, "files": len(CONFIG["authority_evidence"])}

        expected_ids = CONFIG["expected_unit_ids"]
        expected_producers = CONFIG["expected_producer_ids"]
        stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        rejections = load_jsonl(ROOT / "rejections.jsonl")
        excluded_producers = {row["producer_id"] for row in rejections}
        expected_accepted_producers = [
            producer_id for producer_id in expected_producers
            if producer_id not in excluded_producers
        ]
        if (
            [row["id"] for row in stable["units"]] != expected_ids
            or [row["unit_id"] for row in source_map] != expected_ids
            or [row["producer_id"] for row in source_map] != expected_accepted_producers
            or stable["unit_count"] != len(expected_ids)
            or len(expected_producers) != len(expected_accepted_producers) + len(rejections)
        ):
            raise AssertionError("stable-unit/source-map closure mismatch")
        report["checks"]["unit_closure"] = {"passed": True, "units": len(expected_ids)}

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if lease["lease_id"] != CONFIG["lease_id"] or lease["writer_task"] != CONFIG["writer_task"]:
            raise AssertionError("candidate lease mismatch")
        decisions = load_jsonl(ROOT / "decisions.jsonl")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        classified = inventory["formula_units"] + inventory["diagram_units"] + inventory["prose_only_units"]
        if (
            sorted(classified) != expected_ids
            or len(classified) != len(set(classified))
            or len(rejections) != CONFIG["proof_closure"]["rejected"]
            or any(row.get("disposition") != "rejected" for row in rejections)
            or len(decisions) != 9
        ):
            raise AssertionError("lease/decision/inventory closure mismatch")
        report["checks"]["lease_ledgers_inventory"] = {"passed": True, "decisions": len(decisions), "rejections": len(rejections)}

        operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
        if operation_spec["operation_count"] != CONFIG["operation_count"]:
            raise AssertionError("operation-spec count mismatch")
        flattened = [operation for row in source_map for operation in row["operations"]]
        spec_pairs = [(row["stable_id"], row["operation_index"], row["start_byte"], row["end_byte_exclusive"]) for row in operation_spec["operations"]]
        map_pairs = [(row["unit_id"], index, operation["start_byte"], operation["end_byte_exclusive"]) for row in source_map for index, operation in enumerate(row["operations"], 1)]
        if len(flattened) != CONFIG["operation_count"] or spec_pairs != map_pairs:
            raise AssertionError("operation-spec/source-map mismatch")

        payloads = {stem: exact_payload(stem, source_map) for stem in CONFIG["stems"]}
        for stem, observed in payloads.items():
            expected = CONFIG["stems"][stem]
            if (
                observed["authority_sha256"] != expected["authority_sha256"]
                or observed["payload_sha256"] != expected["payload_sha256"]
                or observed["authority_bytes"] != expected["authority_bytes"]
                or observed["payload_bytes"] != expected["payload_bytes"]
            ):
                raise AssertionError(f"{stem}: configured source identity mismatch")
        if sum(row["operation_count"] for row in payloads.values()) != CONFIG["operation_count"]:
            raise AssertionError("operation-count closure mismatch")
        report["checks"]["exact_payloads"] = {"passed": True, "files": payloads}
        report["checks"]["public_hygiene"] = public_hygiene()
        report["passed"] = True
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": report["passed"], "report": REPORT.name}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
