from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
REPORT = BUILDS / "validation.json"
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
STEM = "injectives"
if tuple(CONFIG["stems"]) != (STEM,):
    raise AssertionError("R30 validation requires the single configured injectives stem")
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


def exact_payload(rows: list[dict]) -> dict:
    authority_path = ROOT / "authority" / "source" / f"{STEM}.tex"
    payload_path = ROOT / "payload" / f"{STEM}.tex"
    authority = authority_path.read_bytes()
    payload = payload_path.read_bytes()
    operations = []
    for row in rows:
        if row["source"] != f"{STEM}.tex":
            raise AssertionError("source map contains another source file")
        for operation in row["operations"]:
            old = operation["old_text"].encode("utf-8")
            new = operation["replacement_text"].encode("utf-8")
            start, end = operation["start_byte"], operation["end_byte_exclusive"]
            if authority[start:end] != old:
                raise AssertionError(f"{operation['operation_id']}: authority interval mismatch")
            actual_start_line = authority[:start].count(b"\n") + 1
            actual_end_line = authority[:max(start, end - 1)].count(b"\n") + 1
            if (operation["source_start_line"], operation["source_end_line"]) != (actual_start_line, actual_end_line):
                raise AssertionError(f"{operation['operation_id']}: source-line metadata mismatch")
            if authority.count(old) != operation["occurrence_count_in_frozen_authority"]:
                raise AssertionError(f"{operation['operation_id']}: occurrence count mismatch")
            if sha_bytes(old) != operation["old_sha256"] or sha_bytes(new) != operation["replacement_sha256"]:
                raise AssertionError(f"{operation['operation_id']}: span hash mismatch")
            if len(old) != operation["old_bytes"] or len(new) != operation["replacement_bytes"]:
                raise AssertionError(f"{operation['operation_id']}: span byte-count mismatch")
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
        raise AssertionError(f"{STEM}: payload extends beyond mapped operations")

    structure = {}
    for name, pattern in STRUCTURE_PATTERNS.items():
        before, after = pattern.findall(authority), pattern.findall(payload)
        configured = CONFIG["stems"][STEM].get("ordered_structure_exceptions", {}).get(name, {})
        candidate_only = [value.encode("utf-8") for value in configured.get("candidate_only", [])]
        normalized_after = list(after)
        for token in candidate_only:
            if normalized_after.count(token) != 1 or token in before:
                raise AssertionError(f"{STEM}: invalid configured candidate-only {name} token")
            normalized_after.remove(token)
        if before != normalized_after:
            raise AssertionError(f"{STEM}: ordered {name} changed")
        structure[name] = {
            "authority": len(before),
            "payload": len(after),
            "candidate_only": [value.decode("utf-8") for value in candidate_only],
        }
    expected_display_delta = CONFIG["stems"][STEM]["display_delimiter_delta"]
    if payload.count(b"$$") - authority.count(b"$$") != expected_display_delta:
        raise AssertionError("display-delimiter delta is not configured")
    if authority.count(rb"\xymatrix") != payload.count(rb"\xymatrix"):
        raise AssertionError("xymatrix count changed")
    return {
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
        "operation_count": len(operations),
        "structure": structure,
        "authority_display_delimiters": authority.count(b"$$"),
        "payload_display_delimiters": payload.count(b"$$"),
        "display_delimiter_delta": expected_display_delta,
        "xymatrix_count": authority.count(rb"\xymatrix"),
    }


def public_hygiene() -> dict:
    private_root = re.compile(re.escape("C:") + r"(?:\\+|/+)" + "Us" + "ers" + r"(?:\\+|/+)", re.IGNORECASE)

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
    parser = argparse.ArgumentParser(description="Validate the complete sealed R30 candidate evidence chain.")
    parser.parse_args()
    completed = json.loads((BUILDS / "build-execution.json").read_text(encoding="utf-8"))["completed_at_utc"]
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
        stable_numbers = []
        if not expected_ids or len(expected_ids) != len(set(expected_ids)):
            raise AssertionError("config stable-ID list is empty or duplicated")
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
        stable_aliases = [row["producer_id"] for row in stable["units"]]
        map_aliases = [row["producer_id"] for row in source_map]
        operation_ids = [operation_id for row in stable["units"] for operation_id in row["operation_ids"]]
        map_operation_ids = [operation["operation_id"] for row in source_map for operation in row["operations"]]
        if (
            stable["unit_count"] != len(expected_ids)
            or ids != expected_ids
            or map_ids != expected_ids
            or stable_aliases != CONFIG["expected_producer_aliases"]
            or map_aliases != stable_aliases
            or len(stable_aliases) != len(set(stable_aliases))
            or operation_ids != map_operation_ids
            or len(operation_ids) != CONFIG["operation_count"]
            or len(operation_ids) != len(set(operation_ids))
        ):
            raise AssertionError("stable-unit, alias, operation-ID, or source-map closure mismatch")
        report["checks"]["unit_closure"] = {
            "passed": True,
            "expected": len(expected_ids),
            "manifested": len(ids),
            "producer_aliases": len(stable_aliases),
            "operation_ids": len(operation_ids),
            "operation_ids_unique": len(set(operation_ids)),
        }

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if (
            lease["lease_id"] != CONFIG["lease_id"]
            or lease["writer_task"] != CONFIG["writer_task"]
            or lease["upstream_commit"] != CONFIG["authority_commit"]
            or lease["state"] != "prospective_unissued_not_in_registry"
        ):
            raise AssertionError("candidate lease pointer mismatch")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        classified = inventory["formula_units"] + inventory["diagram_units"] + inventory["prose_only_units"]
        if (
            inventory["unit_count"] != len(expected_ids)
            or sorted(classified) != expected_ids
            or len(classified) != len(set(classified))
            or inventory["unmapped_formula_or_diagram_changes"] != 0
        ):
            raise AssertionError("formula/diagram/prose inventory closure mismatch")
        rejections = load_jsonl(ROOT / "rejections.jsonl")
        decisions = load_jsonl(ROOT / "decisions.jsonl")
        closure = CONFIG["proof_closure"]
        if (
            len(rejections) != CONFIG["rejected"]
            or closure != CONFIG["proof_closure"]
            or not decisions
            or len({row["id"] for row in decisions}) != len(decisions)
            or any(row.get("status") != "rejected" for row in rejections)
        ):
            raise AssertionError("decision/rejection closure mismatch")
        report["checks"]["lease_ledgers_inventory"] = {
            "passed": True,
            "decisions": len(decisions),
            "rejections": len(rejections),
            "unresolved": closure["unresolved"],
            "prospective_lease_pointer": True,
        }

        operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
        mapped_operations = [operation for row in source_map for operation in row["operations"]]
        if (
            operation_spec.get("apply_order") != "descending_start_byte"
            or operation_spec.get("authority_sha256") != CONFIG["stems"][STEM]["authority_sha256"]
            or operation_spec.get("operation_count") != CONFIG["operation_count"]
            or operation_spec.get("operations") != mapped_operations
        ):
            raise AssertionError("operation-spec/source-map closure mismatch")

        payload = exact_payload(source_map)
        expected = CONFIG["stems"][STEM]
        if (
            payload["authority_sha256"] != expected["authority_sha256"]
            or payload["payload_sha256"] != expected["payload_sha256"]
            or payload["payload_bytes"] != expected["payload_bytes"]
            or payload["operation_count"] != CONFIG["operation_count"]
        ):
            raise AssertionError("payload hash or operation closure mismatch")
        report["checks"]["exact_payloads"] = {"passed": True, "files": {STEM: payload}}

        receipt_path = BUILDS / "build-receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        execution_path = BUILDS / "build-execution.json"
        if (
            receipt.get("schema") != "mathematics-commons-stacks-errata-build-receipt/v1"
            or receipt.get("candidate_id") != CONFIG["candidate_id"]
            or receipt.get("authority_commit") != CONFIG["authority_commit"]
            or receipt.get("passed") is not True
            or receipt["execution"]["sha256"] != sha256(execution_path)
            or [row["stem"] for row in receipt["chapters"]] != [STEM]
        ):
            raise AssertionError("build receipt failed or stale")
        for chapter in receipt["chapters"]:
            if (
                not chapter["passed"]
                or not chapter["execution_binding_matches"]
                or chapter["undefined_reference_target_multisets_identical_to_authority"] is not False
                or not chapter["undefined_reference_target_multiset_matches_authority_plus_configured_exceptions"]
                or not chapter["undefined_citation_target_multisets_match_authority"]
            ):
                raise AssertionError(f"chapter build gate failed: {chapter['stem']}")
        if receipt["runner"]["sha256"] != sha256(ROOT / "replay-build.py") or receipt["recipe"]["sha256"] != sha256(ROOT / "BUILD.md"):
            raise AssertionError("build receipt does not bind current runner/recipe")
        report["checks"]["chapter_builds"] = {"passed": True, "chapters": 1, "receipt_sha256": sha256(receipt_path)}

        deterministic_path = BUILDS / "deterministic-replay.json"
        deterministic = json.loads(deterministic_path.read_text(encoding="utf-8"))
        if (
            deterministic.get("schema") != "mathematics-commons-stacks-deterministic-pdf-replay/v1"
            or deterministic.get("passed") is not True
            or deterministic.get("candidate_id") != CONFIG["candidate_id"]
            or deterministic.get("source_date_epoch") != CONFIG["source_date_epoch"]
            or deterministic.get("fresh_builds_compared") != 2
            or [(row.get("stem"), row.get("phase")) for row in deterministic.get("pdfs", [])]
            != [(STEM, "candidate"), (STEM, "authority")]
        ):
            raise AssertionError("deterministic PDF replay missing or failed")
        for row in deterministic["pdfs"]:
            current = ROOT / row["second_path"]
            if not row["byte_identical"] or row["second_sha256"] != sha256(current) or row["second_bytes"] != current.stat().st_size:
                raise AssertionError(f"deterministic PDF replay stale: {row['phase']}")
        report["checks"]["deterministic_pdf_replay"] = {"passed": True, "receipt_sha256": sha256(deterministic_path), "pdfs": 2}

        visual_path = BUILDS / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if (
            visual.get("schema") != "mathematics-commons-stacks-errata-visual-qa/v1"
            or visual.get("candidate_id") != CONFIG["candidate_id"]
            or visual.get("authority_commit") != CONFIG["authority_commit"]
            or visual.get("passed") is not True
            or visual.get("render_protocol", {}).get("manual_review_attested") is not True
            or visual["build_receipt"]["sha256"] != sha256(receipt_path)
            or len(visual["pdfs"]) != 1
        ):
            raise AssertionError("visual QA missing, failed, or stale")

        page_path = ROOT / CONFIG["visual_qa"]["source_page_map_path"]
        page_map = json.loads(page_path.read_text(encoding="utf-8"))
        mapped_rows = page_map.get("operations", [])
        mapped_unique_pages = page_map.get("unique_pages")
        computed_unique_pages = sorted({page for row in mapped_rows for page in row.get("pages", [])})
        configured_review = computed_unique_pages
        configured_high = computed_unique_pages
        if (
            page_map.get("schema") != "mathematics-commons-stacks-synctex-source-page-map/v1"
            or page_map.get("candidate_id") != CONFIG["candidate_id"]
            or page_map.get("stem") != STEM
            or page_map.get("unique_page_count") != len(mapped_unique_pages or [])
            or mapped_unique_pages != computed_unique_pages
            or not mapped_unique_pages
            or len(mapped_rows) != CONFIG["operation_count"]
            or [row.get("operation_id") for row in mapped_rows] != [row["operation_id"] for row in mapped_operations]
            or page_map.get("operation_spec", {}).get("sha256") != sha256(ROOT / "operation-spec.json")
            or page_map.get("auxiliary_build", {}).get("source_sha256") != expected["payload_sha256"]
            or page_map.get("auxiliary_build", {}).get("candidate_pdf_sha256") != sha256(BUILDS / f"{STEM}.pdf")
            or page_map.get("auxiliary_build", {}).get("candidate_pdf_matches_sealed_build") is not True
        ):
            raise AssertionError("source-page-map or configured visual-page closure mismatch")
        report["checks"]["source_page_map"] = {
            "passed": True,
            "operations": len(mapped_rows),
            "unique_pages": len(mapped_unique_pages),
            "receipt_sha256": sha256(page_path),
        }

        covered = []
        for pdf in visual["pdfs"]:
            path = ROOT / pdf["path"]
            if (
                sha256(path) != pdf["sha256"]
                or path.stat().st_size != pdf["bytes"]
                or pdf["unembedded_fonts"]
                or pdf["fonts_without_tounicode"]
                or pdf["malformed_link_rectangles"]
                or pdf["out_of_bounds_link_rectangles"]
            ):
                raise AssertionError(f"visual PDF gate failed: {pdf['path']}")
            manual = pdf.get("manual_findings", {})
            defect_keys = (
                "clipping", "overlap", "blank_or_duplicate_pages", "broken_diagrams",
                "missing_glyphs", "unreadable_content", "warning_loci_outside_printable_area",
            )
            if (
                [row["page"] for row in pdf["high_resolution_evidence"]] != configured_high
                or manual.get("high_resolution_pages_inspected") != configured_review
                or manual.get("pages_inspected") != list(range(1, pdf["pages"] + 1))
                or manual.get("passed") is not True
                or any(manual.get(key) != 0 for key in defect_keys)
                or len(pdf.get("contact_sheet_evidence", []))
                != math.ceil(pdf["pages"] / CONFIG["visual_qa"]["contact_sheet_page_capacity"])
            ):
                raise AssertionError("visual QA page inventory is stale")
            covered.extend(pdf["covered_units"])
        if sorted(covered) != expected_ids:
            raise AssertionError("visual QA does not cover every stable unit")
        report["checks"]["visual_pdf_qa"] = {"passed": True, "pdfs": 1, "direct_units": len(expected_ids), "receipt_sha256": sha256(visual_path)}
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
