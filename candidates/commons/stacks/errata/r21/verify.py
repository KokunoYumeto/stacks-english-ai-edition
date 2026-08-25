from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "builds" / "validation.json"
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
STRUCTURE_PATTERNS = {
    "labels": re.compile(rb"\\label\{[^{}]+\}"),
    "references": re.compile(rb"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(rb"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
    "environments": re.compile(rb"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(rb"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(f"{path}:{line_number}: {exc}") from exc
    return rows


def exact_payload(stem: str, rows: list[dict]) -> dict:
    authority_path = ROOT / "authority" / "source" / f"{stem}.tex"
    payload_path = ROOT / "payload" / f"{stem}.tex"
    authority = authority_path.read_bytes()
    payload = payload_path.read_bytes()
    operations = []
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
            actual_start_line = authority[:start].count(b"\n") + 1
            actual_end_line = authority[:max(start, end - 1)].count(b"\n") + 1
            if (
                operation["source_start_line"] != actual_start_line
                or operation["source_end_line"] != actual_end_line
            ):
                raise AssertionError(
                    f"{operation['operation_id']}: source-line metadata mismatch; "
                    f"declared={operation['source_start_line']}-{operation['source_end_line']} "
                    f"actual={actual_start_line}-{actual_end_line}"
                )
            if authority.count(old) != operation["occurrence_count_in_frozen_authority"]:
                raise AssertionError(f"{operation['operation_id']}: occurrence count mismatch")
            if sha_bytes(old) != operation["old_sha256"] or sha_bytes(new) != operation["replacement_sha256"]:
                raise AssertionError(f"{operation['operation_id']}: span hash mismatch")
            operations.append((start, end, old, new, operation["operation_id"]))
    ascending = sorted(operations)
    for first, second in zip(ascending, ascending[1:]):
        if first[1] > second[0]:
            raise AssertionError(f"overlapping operations: {first[4]}, {second[4]}")
    expected = authority
    for start, end, old, new, operation_id in sorted(operations, reverse=True):
        if expected[start:end] != old:
            raise AssertionError(f"{operation_id}: replay interval changed")
        expected = expected[:start] + new + expected[end:]
    if expected != payload:
        raise AssertionError(f"{stem}: payload extends beyond mapped operations")
    structure = {}
    configured_exceptions = CONFIG["stems"][stem].get("ordered_structure_exceptions", {})
    observed_exceptions = {}
    for name, pattern in STRUCTURE_PATTERNS.items():
        before = pattern.findall(authority)
        after = pattern.findall(payload)
        exceptions = configured_exceptions.get(name, [])
        additions = configured_exceptions.get(f"{name}_added", [])
        comparable_after = list(after)
        for addition in sorted(additions, key=lambda row: row["index_0based"], reverse=True):
            index = addition["index_0based"]
            expected = addition["payload"].encode("utf-8")
            if index >= len(comparable_after) or comparable_after[index] != expected:
                raise AssertionError(f"{stem}: ordered {name} addition mismatch at {index}")
            comparable_after.pop(index)
        if len(before) != len(comparable_after):
            raise AssertionError(f"{stem}: ordered {name} count changed")
        differences = [(index, old, new) for index, (old, new) in enumerate(zip(before, comparable_after)) if old != new]
        expected_differences = [
            (
                row["index_0based"],
                row["authority"].encode("utf-8"),
                row["payload"].encode("utf-8"),
            )
            for row in exceptions
        ]
        if differences != expected_differences:
            raise AssertionError(f"{stem}: ordered {name} changes differ from mapped exceptions")
        structure[name] = {"authority": len(before), "payload": len(after)}
        if exceptions:
            observed_exceptions[name] = exceptions
        if additions:
            observed_exceptions[f"{name}_added"] = additions
    expected_display_delta = CONFIG["stems"][stem]["display_delimiter_delta"]
    if payload.count(b"$$") - authority.count(b"$$") != expected_display_delta:
        raise AssertionError(f"{stem}: display-delimiter delta is not the mapped exception")
    if authority.count(rb"\xymatrix") != payload.count(rb"\xymatrix"):
        raise AssertionError(f"{stem}: xymatrix count changed")
    return {
        "authority_bytes": len(authority), "authority_sha256": sha_bytes(authority),
        "payload_bytes": len(payload), "payload_sha256": sha_bytes(payload),
        "operation_count": len(operations), "structure": structure,
        "authority_display_delimiters": authority.count(b"$$"),
        "payload_display_delimiters": payload.count(b"$$"),
        "display_delimiter_delta": expected_display_delta,
        "xymatrix_count": authority.count(rb"\xymatrix"),
        "ordered_structure_exceptions": observed_exceptions,
    }


def public_hygiene() -> dict:
    private_root = re.compile(
        re.escape("C:") + r"(?:\\+|/+)" + "Us" + "ers" + r"(?:\\+|/+)",
        re.IGNORECASE,
    )

    def assert_clean(value: object, path: Path) -> None:
        if isinstance(value, str):
            if private_root.search(value):
                raise AssertionError(f"private local marker remains in decoded JSON: {path.relative_to(ROOT)}")
        elif isinstance(value, list):
            for item in value:
                assert_clean(item, path)
        elif isinstance(value, dict):
            for item in value.values():
                assert_clean(item, path)

    checked = 0
    for pattern in ("*.md", "*.json", "*.jsonl", "*.csv", "*.log", "*.txt", "*.py"):
        for path in ROOT.rglob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            if private_root.search(text):
                raise AssertionError(f"private local marker remains: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".json":
                assert_clean(json.loads(text), path)
            elif path.suffix.lower() == ".jsonl":
                for line in text.splitlines():
                    if line.strip():
                        assert_clean(json.loads(line), path)
            checked += 1
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    if caches:
        raise AssertionError(f"Python caches remain: {caches}")
    return {"passed": True, "text_files": checked, "python_caches": 0}


def main() -> int:
    completed = json.loads((ROOT / "builds" / "build-execution.json").read_text(encoding="utf-8"))["completed_at_utc"]
    report = {
        "schema": "mathematics-commons-stacks-errata-validation/v1",
        "candidate_id": CONFIG["candidate_id"],
        "authority_commit": CONFIG["authority_commit"],
        "generated_at_utc": completed,
        "verifier_sha256": sha256(Path(__file__)),
        "passed": False,
        "checks": {},
    }
    try:
        for row in CONFIG["authority_evidence"]:
            path = ROOT / row["path"]
            if sha256(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
                raise AssertionError(f"authority evidence mismatch: {row['path']}")
        report["checks"]["authority_evidence"] = {"passed": True, "files": len(CONFIG["authority_evidence"])}

        expected_ids = CONFIG["expected_unit_ids"]
        if not expected_ids or len(expected_ids) != len(set(expected_ids)):
            raise AssertionError("config stable-ID list is empty or duplicated")
        stable_numbers = []
        for stable_id in expected_ids:
            match = re.fullmatch(r"MC-STK-ERR-(\d{4})", stable_id)
            if not match:
                raise AssertionError(f"invalid stable ID: {stable_id}")
            stable_numbers.append(int(match.group(1)))
        if stable_numbers != list(range(stable_numbers[0], stable_numbers[-1] + 1)):
            raise AssertionError("config stable-ID range is not consecutive")
        stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        ids = [row["id"] for row in stable["units"]]
        map_ids = [row["unit_id"] for row in source_map]
        if stable["unit_count"] != len(expected_ids) or ids != expected_ids or map_ids != expected_ids:
            raise AssertionError("stable unit or source-map closure mismatch")
        if len({row["producer_id"] for row in source_map}) != len(expected_ids):
            raise AssertionError("producer correction identities are not unique")
        report["checks"]["unit_closure"] = {"passed": True, "expected": len(expected_ids), "manifested": len(ids)}

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if lease["lease_id"] != CONFIG["lease_id"] or lease["writer_task"] != CONFIG["writer_task"] or lease["upstream_commit"] != CONFIG["authority_commit"]:
            raise AssertionError("candidate lease mismatch")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        classified = inventory["formula_units"] + inventory["diagram_units"] + inventory["prose_only_units"]
        if inventory["unit_count"] != len(expected_ids) or sorted(classified) != expected_ids or len(classified) != len(set(classified)) or inventory["unmapped_formula_or_diagram_changes"] != 0:
            raise AssertionError("formula/diagram/prose inventory closure mismatch")
        rejections = load_jsonl(ROOT / "rejections.jsonl")
        decisions = load_jsonl(ROOT / "decisions.jsonl")
        allowed_dispositions = {"rejected", "duplicate_alias", "rejected_duplicate", "candidate_unproved"}
        rejection_ids = []
        rejection_producers = []
        for row in rejections:
            required = ("schema", "id", "timestamp_utc", "producer_id", "disposition", "reason")
            if row.get("schema") != "mathematics-commons-stacks-candidate-rejection/v1":
                raise AssertionError("rejection ledger schema mismatch")
            if any(not isinstance(row.get(field), str) or not row[field].strip() for field in required[1:]):
                raise AssertionError("rejection ledger has an empty required field")
            if row["disposition"] not in allowed_dispositions:
                raise AssertionError(f"unsupported rejection disposition: {row['disposition']}")
            rejection_ids.append(row["id"])
            rejection_producers.append(row["producer_id"])
        if len(rejection_ids) != len(set(rejection_ids)) or len(rejection_producers) != len(set(rejection_producers)):
            raise AssertionError("rejection IDs or producer IDs are duplicated")
        accepted_producers = [row["producer_id"] for row in source_map]
        if set(accepted_producers) & set(rejection_producers):
            raise AssertionError("accepted and rejected producer identities overlap")
        rejected = [row for row in rejections if row.get("disposition") == "rejected"]
        duplicates = [row for row in rejections if row.get("disposition") in {"duplicate_alias", "rejected_duplicate"}]
        unresolved = [row for row in rejections if row.get("disposition") == "candidate_unproved"]
        closure = CONFIG["proof_closure"]
        if (
            len(rejected) != closure["rejected"]
            or len(duplicates) != closure["prior_overlay_aliases"] + closure["packet_duplicates"]
            or len(unresolved) != closure["unresolved"]
            or closure["accepted"] != len(expected_ids)
            or closure["operations"] != CONFIG["operation_count"]
            or closure["producer_rows"] != (
                closure["accepted"]
                + closure["rejected"]
                + closure["prior_overlay_aliases"]
                + closure["packet_duplicates"]
                + closure["unresolved"]
            )
            or not decisions
        ):
            raise AssertionError("decision/rejection closure mismatch")
        report["checks"]["lease_ledgers_inventory"] = {
            "passed": True,
            "decisions": len(decisions),
            "rejections": len(rejected),
            "duplicate_aliases": len(duplicates),
            "unresolved": len(unresolved),
        }

        payloads = {}
        for stem, expected in CONFIG["stems"].items():
            payloads[stem] = exact_payload(stem, source_map)
            if payloads[stem]["authority_sha256"] != expected["authority_sha256"] or payloads[stem]["payload_sha256"] != expected["payload_sha256"]:
                raise AssertionError(f"payload hash mismatch after reconstruction: {stem}")
        if sum(item["operation_count"] for item in payloads.values()) != CONFIG["operation_count"]:
            raise AssertionError("operation-count closure mismatch")
        report["checks"]["exact_payloads"] = {"passed": True, "files": payloads}

        receipt_path = ROOT / "builds" / "build-receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        execution_path = ROOT / "builds" / "build-execution.json"
        if not receipt["passed"] or receipt["execution"]["sha256"] != sha256(execution_path) or [row["stem"] for row in receipt["chapters"]] != list(CONFIG["stems"]):
            raise AssertionError("build receipt failed or stale")
        for chapter in receipt["chapters"]:
            if not chapter["passed"] or not chapter["execution_binding_matches"] or not chapter["undefined_target_multisets_match_authority"]:
                raise AssertionError(f"chapter build gate failed: {chapter['stem']}")
        if receipt["runner"]["sha256"] != sha256(ROOT / "replay-build.py") or receipt["recipe"]["sha256"] != sha256(ROOT / "BUILD.md"):
            raise AssertionError("build receipt does not bind current runner/recipe")
        report["checks"]["chapter_builds"] = {"passed": True, "chapters": len(CONFIG["stems"]), "receipt_sha256": sha256(receipt_path)}

        deterministic_path = ROOT / "builds" / "deterministic-replay.json"
        deterministic = json.loads(deterministic_path.read_text(encoding="utf-8"))
        if not deterministic.get("passed") or deterministic.get("candidate_id") != CONFIG["candidate_id"]:
            raise AssertionError("deterministic PDF replay missing or failed")
        for row in deterministic["pdfs"]:
            current = ROOT / row["second_path"]
            if not row["byte_identical"] or row["second_sha256"] != sha256(current) or row["second_bytes"] != current.stat().st_size:
                raise AssertionError(f"deterministic PDF replay stale: {row['phase']}")
        report["checks"]["deterministic_pdf_replay"] = {"passed": True, "receipt_sha256": sha256(deterministic_path), "pdfs": len(deterministic["pdfs"])}

        visual_path = ROOT / "builds" / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if not visual["passed"] or visual["build_receipt"]["sha256"] != sha256(receipt_path) or len(visual["pdfs"]) != len(CONFIG["stems"]):
            raise AssertionError("visual QA missing, failed, or stale")
        visual_config = CONFIG.get("visual_qa")
        if not isinstance(visual_config, dict):
            raise AssertionError("candidate config lacks visual QA page inventories")
        covered = []
        for pdf in visual["pdfs"]:
            path = ROOT / pdf["path"]
            if sha256(path) != pdf["sha256"] or path.stat().st_size != pdf["bytes"] or pdf["unembedded_fonts"] or pdf["malformed_link_rectangles"] or pdf["out_of_bounds_link_rectangles"]:
                raise AssertionError(f"visual PDF gate failed: {pdf['path']}")
            stem = pdf["stem"]
            expected_high_res = visual_config.get("high_resolution_pages", {}).get(stem)
            expected_review = visual_config.get("correction_sensitive_pages", {}).get(stem)
            if (
                [row["page"] for row in pdf["high_resolution_evidence"]] != expected_high_res
                or pdf["manual_findings"]["high_resolution_pages_inspected"] != expected_review
            ):
                raise AssertionError(f"visual QA page inventory is stale: {stem}")
            covered.extend(pdf["covered_units"])
        if sorted(covered) != expected_ids:
            raise AssertionError("visual QA does not cover every stable unit")
        report["checks"]["visual_pdf_qa"] = {"passed": True, "pdfs": len(CONFIG["stems"]), "direct_units": len(expected_ids), "receipt_sha256": sha256(visual_path)}
        report["checks"]["public_hygiene"] = public_hygiene()
        report["passed"] = True
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "report": str(REPORT)}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())

