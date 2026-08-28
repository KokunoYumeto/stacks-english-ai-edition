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
STEM = "artin"
if tuple(CONFIG["stems"]) != (STEM,):
    raise AssertionError("R25 validation requires the single configured artin stem")
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
    configured_line_exceptions = CONFIG["stems"][stem].get("source_line_exceptions", {})
    observed_line_exceptions = {}
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
            declared_lines = (operation["source_start_line"], operation["source_end_line"])
            actual_lines = (actual_start_line, actual_end_line)
            configured_line_exception = configured_line_exceptions.get(operation["operation_id"])
            if declared_lines != actual_lines:
                expected_exception = {
                    "declared_start_line": declared_lines[0],
                    "declared_end_line": declared_lines[1],
                    "actual_start_line": actual_lines[0],
                    "actual_end_line": actual_lines[1],
                    "rationale": configured_line_exception.get("rationale") if isinstance(configured_line_exception, dict) else None,
                }
                if configured_line_exception != expected_exception or not expected_exception["rationale"]:
                    raise AssertionError(
                        f"{operation['operation_id']}: source-line metadata mismatch; "
                        f"declared={declared_lines[0]}-{declared_lines[1]} "
                        f"actual={actual_lines[0]}-{actual_lines[1]}"
                    )
                observed_line_exceptions[operation["operation_id"]] = configured_line_exception
            elif configured_line_exception is not None:
                raise AssertionError(f"{operation['operation_id']}: stale source-line exception")
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
    if set(observed_line_exceptions) != set(configured_line_exceptions):
        raise AssertionError(f"{stem}: source-line exception closure mismatch")
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
            expected_addition = addition["payload"].encode("utf-8")
            if index >= len(comparable_after) or comparable_after[index] != expected_addition:
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
        "source_line_exceptions": observed_line_exceptions,
    }


def operation_identity(row: dict) -> tuple:
    keys = (
        "operation_id", "source_start_line", "source_end_line", "start_byte",
        "end_byte_exclusive", "occurrence_count_in_frozen_authority", "old_text",
        "replacement_text", "old_sha256", "replacement_sha256",
    )
    return tuple(row[key] for key in keys)


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
    parser = argparse.ArgumentParser(description="Validate the complete sealed R25 candidate evidence chain.")
    parser.parse_args()
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
        primary_producers = [row["producer_id"] for row in source_map]
        all_producers = [producer_id for row in source_map for producer_id in row["producer_ids"]]
        stable_primary = [row["producer_id"] for row in stable["units"]]
        stable_all = [producer_id for row in stable["units"] for producer_id in row["producer_ids"]]
        if (
            stable["unit_count"] != len(expected_ids)
            or ids != expected_ids
            or map_ids != expected_ids
            or primary_producers != CONFIG["expected_producer_ids"]
            or stable_primary != primary_producers
            or all_producers != CONFIG["expected_all_producer_ids"]
            or stable_all != all_producers
            or len(all_producers) != len(set(all_producers))
        ):
            raise AssertionError("stable unit, producer, or source-map closure mismatch")
        report["checks"]["unit_closure"] = {
            "passed": True,
            "expected": len(expected_ids),
            "manifested": len(ids),
            "accepted_producer_identities": len(all_producers),
        }

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if lease["lease_id"] != CONFIG["lease_id"] or lease["writer_task"] != CONFIG["writer_task"] or lease["upstream_commit"] != CONFIG["authority_commit"]:
            raise AssertionError("candidate lease mismatch")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        classified = inventory["formula_units"] + inventory["diagram_units"] + inventory["prose_only_units"]
        if inventory["unit_count"] != len(expected_ids) or sorted(classified) != expected_ids or len(classified) != len(set(classified)) or inventory["unmapped_formula_or_diagram_changes"] != 0:
            raise AssertionError("formula/diagram/prose inventory closure mismatch")
        rejections = load_jsonl(ROOT / "rejections.jsonl")
        decisions = load_jsonl(ROOT / "decisions.jsonl")
        rejected_producers = []
        authority = (ROOT / "authority" / "source" / f"{STEM}.tex").read_bytes()
        for row in rejections:
            if row.get("schema") != "mathematics-commons-stacks-errata-rejection/v1":
                raise AssertionError("rejection ledger schema mismatch")
            required_strings = ("producer_id", "locus", "class", "result", "rationale")
            if any(not isinstance(row.get(field), str) or not row[field].strip() for field in required_strings):
                raise AssertionError("rejection ledger has an empty required field")
            producer_ids = row.get("producer_ids")
            if not isinstance(producer_ids, list) or not producer_ids or producer_ids[0] != row["producer_id"] or len(producer_ids) != len(set(producer_ids)):
                raise AssertionError("rejection producer identities are invalid")
            rejected_producers.extend(producer_ids)
            operation = row.get("proposed_operation")
            if not isinstance(operation, dict) or operation.get("applied") is not False:
                raise AssertionError("rejected proposal lacks an unapplied operation record")
            start, end = operation["start_byte"], operation["end_byte_exclusive"]
            old = operation["old_text"].encode("utf-8")
            replacement = operation["replacement_text"].encode("utf-8")
            if (
                authority[start:end] != old
                or sha_bytes(old) != operation["old_sha256"]
                or sha_bytes(replacement) != operation["replacement_sha256"]
                or authority[:start].count(b"\n") + 1 != operation["source_start_line"]
                or authority[:max(start, end - 1)].count(b"\n") + 1 != operation["source_end_line"]
            ):
                raise AssertionError("rejected proposal preimage or metadata mismatch")
        if len(rejected_producers) != len(set(rejected_producers)):
            raise AssertionError("rejected producer identities are duplicated")
        absent = CONFIG["intentionally_absent_producer_ids"]
        if not isinstance(absent, list) or len(absent) != len(set(absent)):
            raise AssertionError("intentionally absent producer identities are invalid")
        if set(all_producers) & (set(rejected_producers) | set(absent)) or set(rejected_producers) & set(absent):
            raise AssertionError("accepted, rejected, and intentionally absent producer identities overlap")
        prior_aliases = [alias for row in source_map for alias in row.get("prior_aliases", [])]
        if len(prior_aliases) != len(set(prior_aliases)):
            raise AssertionError("prior alias identities are duplicated")
        closure = CONFIG["proof_closure"]
        if (
            len(rejections) != closure["rejected"]
            or len(absent) != closure["intentionally_absent"]
            or len(prior_aliases) != closure["prior_aliases"]
            or closure["packet_duplicates"] != 0
            or closure["unresolved"] != 0
            or closure["accepted"] != len(expected_ids)
            or closure["operations"] != CONFIG["operation_count"]
            or closure["producer_rows"] != len(all_producers) + len(rejected_producers)
            or not decisions
        ):
            raise AssertionError("decision/rejection closure mismatch")
        report["checks"]["lease_ledgers_inventory"] = {
            "passed": True,
            "decisions": len(decisions),
            "rejections": len(rejections),
            "intentionally_absent": len(absent),
            "prior_aliases": len(prior_aliases),
            "unresolved": closure["unresolved"],
        }

        operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
        mapped_operations = [operation for row in source_map for operation in row["operations"]]
        if (
            operation_spec.get("apply_order") != "descending_start_byte"
            or operation_spec.get("authority_sha256") != CONFIG["stems"][STEM]["authority_sha256"]
            or operation_spec.get("operation_count") != CONFIG["operation_count"]
            or [operation_identity(row) for row in operation_spec["operations"]]
            != [operation_identity(row) for row in mapped_operations]
        ):
            raise AssertionError("operation-spec/source-map closure mismatch")

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
        if (
            receipt.get("schema") != "mathematics-commons-stacks-errata-build-receipt/v1"
            or receipt.get("candidate_id") != CONFIG["candidate_id"]
            or receipt.get("authority_commit") != CONFIG["authority_commit"]
            or receipt.get("passed") is not True
            or receipt["execution"]["sha256"] != sha256(execution_path)
            or [row["stem"] for row in receipt["chapters"]] != list(CONFIG["stems"])
        ):
            raise AssertionError("build receipt failed or stale")
        for chapter in receipt["chapters"]:
            if not chapter["passed"] or not chapter["execution_binding_matches"] or not chapter["undefined_target_multisets_match_authority"]:
                raise AssertionError(f"chapter build gate failed: {chapter['stem']}")
        if receipt["runner"]["sha256"] != sha256(ROOT / "replay-build.py") or receipt["recipe"]["sha256"] != sha256(ROOT / "BUILD.md"):
            raise AssertionError("build receipt does not bind current runner/recipe")
        report["checks"]["chapter_builds"] = {"passed": True, "chapters": len(CONFIG["stems"]), "receipt_sha256": sha256(receipt_path)}

        deterministic_path = ROOT / "builds" / "deterministic-replay.json"
        deterministic = json.loads(deterministic_path.read_text(encoding="utf-8"))
        expected_replay_rows = [
            (stem, phase)
            for stem in CONFIG["stems"]
            for phase in ("candidate", "authority")
        ]
        if (
            deterministic.get("schema") != "mathematics-commons-stacks-deterministic-pdf-replay/v1"
            or deterministic.get("passed") is not True
            or deterministic.get("candidate_id") != CONFIG["candidate_id"]
            or deterministic.get("source_date_epoch") != CONFIG["source_date_epoch"]
            or deterministic.get("fresh_builds_compared") != 2
            or [(row.get("stem"), row.get("phase")) for row in deterministic.get("pdfs", [])]
            != expected_replay_rows
        ):
            raise AssertionError("deterministic PDF replay missing or failed")
        for row in deterministic["pdfs"]:
            current = ROOT / row["second_path"]
            if not row["byte_identical"] or row["second_sha256"] != sha256(current) or row["second_bytes"] != current.stat().st_size:
                raise AssertionError(f"deterministic PDF replay stale: {row['phase']}")
        report["checks"]["deterministic_pdf_replay"] = {"passed": True, "receipt_sha256": sha256(deterministic_path), "pdfs": len(deterministic["pdfs"])}

        visual_path = ROOT / "builds" / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if (
            visual.get("schema") != "mathematics-commons-stacks-errata-visual-qa/v1"
            or visual.get("candidate_id") != CONFIG["candidate_id"]
            or visual.get("authority_commit") != CONFIG["authority_commit"]
            or visual.get("passed") is not True
            or visual.get("render_protocol", {}).get("manual_review_attested") is not True
            or visual["build_receipt"]["sha256"] != sha256(receipt_path)
            or len(visual["pdfs"]) != len(CONFIG["stems"])
        ):
            raise AssertionError("visual QA missing, failed, or stale")
        visual_config = CONFIG.get("visual_qa")
        if not isinstance(visual_config, dict):
            raise AssertionError("candidate config lacks visual QA page inventories")

        page_map_binding = visual_config.get("source_page_map")
        if not isinstance(page_map_binding, dict) or set(page_map_binding) != {"path", "bytes", "sha256"}:
            raise AssertionError("candidate config lacks a complete source-page-map binding")
        page_map_path = ROOT / page_map_binding["path"]
        page_map = json.loads(page_map_path.read_text(encoding="utf-8"))
        mapped_rows = page_map.get("operations", [])
        mapped_unique_pages = page_map.get("unique_pages")
        computed_unique_pages = sorted({page for row in mapped_rows for page in row.get("pages", [])})
        configured_review_pages = visual_config.get("correction_sensitive_pages", {}).get(STEM)
        configured_high_res_pages = visual_config.get("high_resolution_pages", {}).get(STEM)
        if (
            page_map_binding["path"] != "builds/source-page-map.json"
            or page_map_path.stat().st_size != page_map_binding["bytes"]
            or sha256(page_map_path) != page_map_binding["sha256"]
            or page_map.get("schema") != "mathematics-commons-stacks-synctex-source-page-map/v1"
            or page_map.get("candidate_id") != CONFIG["candidate_id"]
            or page_map.get("stem") != STEM
            or page_map.get("unique_page_count") != len(mapped_unique_pages or [])
            or mapped_unique_pages != computed_unique_pages
            or not mapped_unique_pages
            or mapped_unique_pages != sorted(set(mapped_unique_pages))
            or len(mapped_rows) != CONFIG["operation_count"]
            or [row.get("operation_id") for row in mapped_rows]
            != [row["operation_id"] for row in operation_spec["operations"]]
            or page_map.get("operation_spec", {}).get("sha256") != sha256(ROOT / "operation-spec.json")
            or page_map.get("operation_spec", {}).get("operation_count") != CONFIG["operation_count"]
            or page_map.get("auxiliary_build", {}).get("source_sha256") != CONFIG["stems"][STEM]["payload_sha256"]
            or page_map.get("auxiliary_build", {}).get("candidate_pdf_sha256") != sha256(BUILDS / f"{STEM}.pdf")
            or page_map.get("auxiliary_build", {}).get("candidate_pdf_matches_sealed_build") is not True
            or configured_review_pages != mapped_unique_pages
            or not isinstance(configured_high_res_pages, list)
            or not set(configured_review_pages).issubset(configured_high_res_pages)
        ):
            raise AssertionError("source-page-map or configured visual-page closure mismatch")
        report["checks"]["source_page_map"] = {
            "passed": True,
            "operations": len(mapped_rows),
            "unique_pages": len(mapped_unique_pages),
            "receipt_sha256": sha256(page_map_path),
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
            stem = pdf["stem"]
            expected_high_res = visual_config.get("high_resolution_pages", {}).get(stem)
            expected_review = visual_config.get("correction_sensitive_pages", {}).get(stem)
            manual = pdf.get("manual_findings", {})
            defect_keys = (
                "clipping", "overlap", "blank_or_duplicate_pages", "broken_diagrams",
                "missing_glyphs", "unreadable_content", "warning_loci_outside_printable_area",
            )
            if (
                [row["page"] for row in pdf["high_resolution_evidence"]] != expected_high_res
                or manual.get("high_resolution_pages_inspected") != expected_review
                or manual.get("pages_inspected") != list(range(1, pdf["pages"] + 1))
                or manual.get("passed") is not True
                or any(manual.get(key) != 0 for key in defect_keys)
                or len(pdf.get("contact_sheet_evidence", [])) != math.ceil(pdf["pages"] / 16)
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
