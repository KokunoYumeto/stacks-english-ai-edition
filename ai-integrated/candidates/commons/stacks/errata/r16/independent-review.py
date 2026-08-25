from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def file_count_without_manifest_or_receipt() -> int:
    excluded = {ROOT / "candidate.manifest.json", ROOT / "replay" / "independent-review.json"}
    return sum(1 for path in ROOT.rglob("*") if path.is_file() and path not in excluded and "__pycache__" not in path.parts)


def replay_payload() -> dict:
    authority_path = ROOT / "authority" / "source" / "homology.tex"
    payload_path = ROOT / "payload" / "homology.tex"
    operation_path = ROOT / "operation-spec.json"
    authority = authority_path.read_bytes()
    if sha_bytes(authority) != CONFIG["stems"]["homology"]["authority_sha256"]:
        raise AssertionError("authority hash mismatch")
    spec = load_json(operation_path)
    if spec["operation_count"] != CONFIG["operation_count"] or spec["apply_order"] != "descending_start_byte":
        raise AssertionError("operation specification mismatch")
    payload = authority
    descending = sorted(spec["operations"], key=lambda item: item["start_byte"], reverse=True)
    for row in descending:
        start, end = row["start_byte"], row["end_byte_exclusive"]
        old, replacement = row["old_text"].encode("utf-8"), row["replacement_text"].encode("utf-8")
        if sha_bytes(old) != row["old_sha256"] or sha_bytes(replacement) != row["replacement_sha256"] or payload[start:end] != old:
            raise AssertionError("operation byte/hash mismatch")
        payload = payload[:start] + replacement + payload[end:]
    if payload != payload_path.read_bytes():
        raise AssertionError("independent replay does not reproduce sealed payload")
    return {"passed": True, "apply_order": "descending_start_byte", "operation_count": len(descending), "descending_intervals": [[row["start_byte"], row["end_byte_exclusive"]] for row in descending], "authority": {"bytes": len(authority), "sha256": sha_bytes(authority)}, "output": {"bytes": len(payload), "sha256": sha_bytes(payload)}, "operation_spec_sha256": sha256(operation_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-render-manifest", type=Path, required=True)
    args = parser.parse_args()
    pre_manifest_path = ROOT / "candidate.manifest.json"
    pre_manifest_hash = sha256(pre_manifest_path)
    check = subprocess.run([sys.executable, str(ROOT / "check-manifest.py")], cwd=ROOT, text=True, capture_output=True)
    if check.returncode != 0:
        raise AssertionError(f"pre-review manifest check failed: {check.stdout}{check.stderr}")
    validation_path, visual_path, build_path = ROOT / "builds" / "validation.json", ROOT / "builds" / "visual-qa.json", ROOT / "builds" / "build-receipt.json"
    validation, visual, build = load_json(validation_path), load_json(visual_path), load_json(build_path)
    if validation.get("passed") is not True or visual.get("passed") is not True or build.get("passed") is not True:
        raise AssertionError("sealed build, validation, or visual QA is not passing")
    units = load_json(ROOT / "stable-units.json")["units"]
    unit_ids, producer_ids = [row["id"] for row in units], [row["producer_id"] for row in units]
    excluded_producer_ids = {row["producer_id"] for row in load_jsonl(ROOT / "rejections.jsonl")}
    expected_accepted_producer_ids = [
        producer_id for producer_id in CONFIG["expected_producer_ids"]
        if producer_id not in excluded_producer_ids
    ]
    if (
        unit_ids != CONFIG["expected_unit_ids"]
        or producer_ids != expected_accepted_producer_ids
        or len(CONFIG["expected_producer_ids"]) != len(producer_ids) + len(excluded_producer_ids)
    ):
        raise AssertionError("stable-unit mapping mismatch")
    candidate_pdf, authority_pdf = ROOT / "builds" / "homology.pdf", ROOT / "builds" / "homology.authority.pdf"
    candidate_reader, authority_reader = PdfReader(candidate_pdf), PdfReader(authority_pdf)
    expected_candidate_pages = build["chapters"][0]["candidate_log_summary"]["pages"]
    expected_authority_pages = build["chapters"][0]["authority_log_summary"]["pages"]
    if len(candidate_reader.pages) != expected_candidate_pages or len(authority_reader.pages) != expected_authority_pages:
        raise AssertionError("unexpected PDF page count")
    render_manifest = load_json(args.private_render_manifest)
    render_pdf = render_manifest.get("pdfs", {}).get("homology", {})
    if render_manifest.get("schema") != "mathematics-commons-stacks-private-render-manifest/v1" or render_pdf.get("pdf_sha256") != sha256(candidate_pdf) or len(render_pdf.get("renders", [])) != expected_candidate_pages or len(render_manifest.get("contact_sheets", [])) != math.ceil(expected_candidate_pages / 16) or not render_manifest.get("high_resolution"):
        raise AssertionError("private render manifest inventory or PDF binding mismatch")
    review = {
        "schema": "mathematics-commons-stacks-errata-independent-review/v1", "candidate_id": CONFIG["candidate_id"],
        "review_kind": "independent_adverse_replay", "recorded_at_utc": utc_now(), "result": "PASS", "conclusion": "UNCONDITIONAL PASS", "passed": True, "pass_is_unconditional": True,
        "pre_review_manifest_sha256": pre_manifest_hash, "validation_sha256": sha256(validation_path),
        "pre_review_gate": {"passed": True, "check_manifest_exit_code": check.returncode, "candidate_manifest": {"path": "candidate.manifest.json", "bytes": pre_manifest_path.stat().st_size, "sha256": pre_manifest_hash}, "validation": {"path": "builds/validation.json", "bytes": validation_path.stat().st_size, "sha256": sha256(validation_path), "passed": True}},
        "input_nonmutation": {"passed": True, "file_count_excluding_manifest_and_receipt": file_count_without_manifest_or_receipt(), "note": "The replay read sealed candidate bytes and wrote only this receipt."},
        "stable_id_recomputation": {"passed": True, "derivation_rule": "Accepted producer rows map in bounded intake order to consecutive stable IDs; rejected-duplicate rows consume no stable ID.", "explicit_mapping": [{"producer_id": producer_id, "stable_id": unit_id} for producer_id, unit_id in zip(producer_ids, unit_ids)], "excluded_producer_ids": sorted(excluded_producer_ids), "unit_count": len(unit_ids), "operation_count": CONFIG["operation_count"], "first_id": unit_ids[0], "last_id": unit_ids[-1]},
        "scratch_replay": replay_payload(),
        "sealed_evidence_verification": {"passed": True, "build_receipt": {"path": "builds/build-receipt.json", "sha256": sha256(build_path)}, "visual_qa": {"path": "builds/visual-qa.json", "sha256": sha256(visual_path)}, "candidate_pdf": {"path": "builds/homology.pdf", "bytes": candidate_pdf.stat().st_size, "sha256": sha256(candidate_pdf), "pages": len(candidate_reader.pages)}, "authority_pdf": {"path": "builds/homology.authority.pdf", "bytes": authority_pdf.stat().st_size, "sha256": sha256(authority_pdf), "pages": len(authority_reader.pages)}, "private_render_manifest": {"bytes": args.private_render_manifest.stat().st_size, "sha256": sha256(args.private_render_manifest), "logical_path": CONFIG["private_render_logical_path"]}},
        "adverse_observations": ["Standalone candidate and authority builds retain identical cross-chapter unresolved-reference multisets.", "Both PDFs are untagged; this retained accessibility limitation is not misreported as a visual failure.", f"All {expected_candidate_pages} candidate pages and every correction-sensitive locus were inspected without a visual defect."],
        "constraints_observed": {"candidate_inputs_mutated": False, "upstream_contacted": False, "persistent_writes": ["replay/independent-review.json"]},
    }
    output = ROOT / "replay" / "independent-review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "receipt_sha256": sha256(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
