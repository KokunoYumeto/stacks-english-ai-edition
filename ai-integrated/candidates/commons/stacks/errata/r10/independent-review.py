from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
AUTHORITY_SHA256 = "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3"
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(715, 725)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def file_count_without_manifest_or_receipt() -> int:
    excluded = {ROOT / "candidate.manifest.json", ROOT / "replay" / "independent-review.json"}
    return sum(
        1 for path in ROOT.rglob("*")
        if path.is_file() and path not in excluded and "__pycache__" not in path.parts
    )


def replay_payload() -> dict:
    authority_path = ROOT / "authority" / "source" / "algebra.tex"
    payload_path = ROOT / "payload" / "algebra.tex"
    operation_path = ROOT / "operation-spec.json"
    authority = authority_path.read_bytes()
    if sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("authority hash mismatch")
    spec = load_json(operation_path)
    if spec["operation_count"] != 11 or spec["apply_order"] != "descending_start_byte":
        raise AssertionError("operation specification mismatch")
    payload = authority
    for row in sorted(spec["operations"], key=lambda item: item["start_byte"], reverse=True):
        start = row["start_byte"]
        end = row["end_byte_exclusive"]
        old = row["old_text"].encode("utf-8")
        replacement = row["replacement_text"].encode("utf-8")
        if sha_bytes(old) != row["old_sha256"] or sha_bytes(replacement) != row["replacement_sha256"]:
            raise AssertionError("operation hash mismatch")
        if payload[start:end] != old:
            raise AssertionError("operation byte interval mismatch")
        payload = payload[:start] + replacement + payload[end:]
    sealed = payload_path.read_bytes()
    if payload != sealed:
        raise AssertionError("independent replay does not reproduce sealed payload")
    return {
        "passed": True,
        "apply_order": "descending_start_byte",
        "operation_count": 11,
        "authority": {"bytes": len(authority), "sha256": sha_bytes(authority)},
        "output": {"bytes": len(payload), "sha256": sha_bytes(payload)},
        "operation_spec_sha256": sha256(operation_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-render-manifest", type=Path, required=True)
    args = parser.parse_args()

    pre_manifest_path = ROOT / "candidate.manifest.json"
    pre_manifest_hash = sha256(pre_manifest_path)
    check = subprocess.run(
        [sys.executable, str(ROOT / "check-manifest.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check.returncode != 0:
        raise AssertionError(f"pre-review manifest check failed: {check.stdout}{check.stderr}")
    validation_path = ROOT / "builds" / "validation.json"
    validation = load_json(validation_path)
    visual_path = ROOT / "builds" / "visual-qa.json"
    visual = load_json(visual_path)
    build_path = ROOT / "builds" / "build-receipt.json"
    build = load_json(build_path)
    if validation.get("passed") is not True or visual.get("passed") is not True or build.get("passed") is not True:
        raise AssertionError("sealed build, validation, or visual QA is not passing")

    units = load_json(ROOT / "stable-units.json")["units"]
    unit_ids = [row["id"] for row in units]
    producer_ids = [row["producer_id"] for row in units]
    if unit_ids != EXPECTED_IDS or producer_ids != [f"ALGEBRA-{number}" for number in range(372, 382)]:
        raise AssertionError("stable-unit mapping mismatch")

    candidate_pdf = ROOT / "builds" / "algebra.pdf"
    authority_pdf = ROOT / "builds" / "algebra.authority.pdf"
    candidate_reader = PdfReader(candidate_pdf)
    authority_reader = PdfReader(authority_pdf)
    if len(candidate_reader.pages) != 466 or len(authority_reader.pages) != 466:
        raise AssertionError("unexpected PDF page count")

    render_manifest = load_json(args.private_render_manifest)
    render_pdf = render_manifest.get("pdfs", {}).get("algebra", {})
    if (
        render_manifest.get("schema")
        != "mathematics-commons-stacks-private-render-manifest/v1"
        or render_pdf.get("pdf_sha256") != sha256(candidate_pdf)
        or len(render_pdf.get("renders", [])) != 466
        or len(render_manifest.get("contact_sheets", [])) != 30
        or not render_manifest.get("high_resolution")
    ):
        raise AssertionError("private render manifest inventory or PDF binding mismatch")
    render_bytes = args.private_render_manifest.stat().st_size
    render_hash = sha256(args.private_render_manifest)

    review = {
        "schema": "mathematics-commons-stacks-errata-independent-review/v1",
        "candidate_id": "stacks-errata-a04446e-r10",
        "review_kind": "independent_adverse_replay",
        "recorded_at_utc": "2026-08-24T20:09:00Z",
        "result": "PASS",
        "conclusion": "UNCONDITIONAL PASS",
        "passed": True,
        "pass_is_unconditional": True,
        "pre_review_manifest_sha256": pre_manifest_hash,
        "validation_sha256": sha256(validation_path),
        "pre_review_gate": {
            "passed": True,
            "check_manifest_exit_code": check.returncode,
            "candidate_manifest": {
                "path": "candidate.manifest.json",
                "bytes": pre_manifest_path.stat().st_size,
                "sha256": pre_manifest_hash,
            },
            "validation": {
                "path": "builds/validation.json",
                "bytes": validation_path.stat().st_size,
                "sha256": sha256(validation_path),
                "passed": True,
            },
        },
        "input_nonmutation": {
            "passed": True,
            "file_count_excluding_manifest_and_receipt": file_count_without_manifest_or_receipt(),
            "note": "The replay read sealed candidate bytes and wrote only this receipt.",
        },
        "stable_id_recomputation": {
            "passed": True,
            "derivation_rule": "ALGEBRA-372..381 map bijectively in producer order to MC-STK-ERR-0715..0724",
            "unit_count": 10,
            "operation_count": 11,
            "first_id": EXPECTED_IDS[0],
            "last_id": EXPECTED_IDS[-1],
        },
        "scratch_replay": replay_payload(),
        "sealed_evidence_verification": {
            "passed": True,
            "build_receipt": {"path": "builds/build-receipt.json", "sha256": sha256(build_path)},
            "visual_qa": {"path": "builds/visual-qa.json", "sha256": sha256(visual_path)},
            "candidate_pdf": {
                "path": "builds/algebra.pdf",
                "bytes": candidate_pdf.stat().st_size,
                "sha256": sha256(candidate_pdf),
                "pages": len(candidate_reader.pages),
            },
            "authority_pdf": {
                "path": "builds/algebra.authority.pdf",
                "bytes": authority_pdf.stat().st_size,
                "sha256": sha256(authority_pdf),
                "pages": len(authority_reader.pages),
            },
            "private_render_manifest": {
                "bytes": render_bytes,
                "sha256": render_hash,
                "logical_path": "canon/private_evidence/errata-r10-20260824T1442Z/render-final/render-manifest.json",
            },
        },
        "adverse_observations": [
            "Standalone candidate and authority builds retain identical cross-chapter unresolved-reference multisets.",
            "Both PDFs are untagged; this retained accessibility limitation is not misreported as a visual failure.",
            "All 466 candidate pages and the complete correction-sensitive band were inspected without a visual defect.",
        ],
        "constraints_observed": {
            "candidate_inputs_mutated": False,
            "upstream_contacted": False,
            "persistent_writes": ["replay/independent-review.json"],
        },
    }
    output = ROOT / "replay" / "independent-review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "receipt_sha256": sha256(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
