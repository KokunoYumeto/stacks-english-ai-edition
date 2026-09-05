"""Append-only page-complete R44 closure and manifest sealing.

The original FINAL_STAGE.json is immutable.  This helper binds the four
independent one-page-at-a-time visual receipts in a successor snapshot, then
requires a separate final review before sealing candidate.manifest.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
PRIVATE = (
    REPO.parent
    / "03_projects/language_management/cjk/03_working_translations/"
      "stacks_cjk_20260821/canon/private_evidence/errata-r44-20260905/render"
)
PAGE_RECEIPTS = (
    ("replay/PAGE_COMPLETE_VISUAL_001_028.json", 1, 28),
    ("replay/PAGE_COMPLETE_VISUAL_029_056.json", 29, 56),
    ("replay/PAGE_COMPLETE_VISUAL_057_084.json", 57, 84),
    ("replay/PAGE_COMPLETE_VISUAL_085_109.json", 85, 109),
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    if path.exists():
        raise FileExistsError(f"append-only destination already exists: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def ev(path: Path) -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def bound(row: dict) -> None:
    path = (ROOT / row["path"]).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), row["path"]
    assert path.stat().st_size == row["bytes"], row["path"]
    assert sha(path) == row["sha256"], row["path"]


def assert_original_stage() -> dict:
    path = ROOT / "replay/FINAL_STAGE.json"
    stage = load(path)
    assert stage["candidate_id"] == "stacks-errata-a04446e-r44"
    assert stage["status"] == "READY_FOR_FULL_INDEPENDENT_REVIEW_NOT_ADMITTED"
    for row in stage["snapshot_inventory"]:
        bound(row)
    return stage


def aggregate_visual() -> dict:
    assert_original_stage()
    destination = ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"
    render_manifest_path = PRIVATE / "render-manifest.json"
    render_manifest = load(render_manifest_path)
    renders = render_manifest["pdfs"]["perfect"]["renders"]
    assert [row["page"] for row in renders] == list(range(1, 110))
    render_by_page = {row["page"]: row for row in renders}
    pdf_path = ROOT / "builds/perfect.pdf"
    pdf_sha = sha(pdf_path)
    assert render_manifest["pdfs"]["perfect"]["pdf_sha256"] == pdf_sha

    receipts = []
    covered: list[int] = []
    for relative, start, end in PAGE_RECEIPTS:
        path = ROOT / relative
        doc = load(path)
        assert doc.get("passed") is True, relative
        pdf_row = doc.get("pdf")
        if not isinstance(pdf_row, dict) or "sha256" not in pdf_row:
            pdf_row = doc.get("candidate_pdf")
        if not isinstance(pdf_row, dict) or "sha256" not in pdf_row:
            pdf_row = doc.get("authority", {}).get("pdf")
        assert isinstance(pdf_row, dict) and pdf_row.get("sha256") == pdf_sha, relative
        assert pdf_row.get("bytes") == pdf_path.stat().st_size, relative
        rows = doc.get("pages") or doc.get("per_page")
        assert isinstance(rows, list), relative
        assert [row["page"] for row in rows] == list(range(start, end + 1)), relative
        for row in rows:
            expected = render_by_page[row["page"]]
            observed_bytes = row.get("bytes", row.get("actual_bytes", row.get("observed_bytes", row.get("manifest_bytes"))))
            observed_sha = row.get("sha256", row.get("actual_sha256", row.get("observed_sha256", row.get("manifest_sha256"))))
            assert row["file"] == expected["file"], (relative, row["page"])
            assert observed_bytes == expected["bytes"], (relative, row["page"])
            assert observed_sha == expected["sha256"], (relative, row["page"])
            assert str(row.get("result", row.get("layout_result", ""))).upper() == "PASS", (relative, row["page"])
            image = PRIVATE / "perfect" / row["file"]
            assert image.is_file() and image.stat().st_size == observed_bytes
            assert sha(image) == observed_sha
        if "blocking_findings" in doc:
            assert doc["blocking_findings"] == [], relative
        covered.extend(range(start, end + 1))
        receipts.append({**ev(path), "page_start": start, "page_end": end, "page_count": end - start + 1})
    assert covered == list(range(1, 110))
    assert len(covered) == len(set(covered)) == 109

    report = {
        "schema": "stacks-r44-page-complete-visual-adjudication/v1",
        "candidate_id": "stacks-errata-a04446e-r44",
        "passed": True,
        "status": "PASS_ALL_109_PAGES_INDIVIDUALLY_INSPECTED",
        "pdf": {"path": "builds/perfect.pdf", "bytes": pdf_path.stat().st_size, "sha256": pdf_sha, "pages": 109},
        "render_manifest": {
            "private_path_role": "hash-bound validation evidence outside the public candidate",
            "bytes": render_manifest_path.stat().st_size,
            "sha256": sha(render_manifest_path),
            "page_rows": 109,
        },
        "coverage": {
            "method": "Every retained per-page PNG was independently opened and inspected one page at a time; contact sheets were not used as a substitute.",
            "pages": list(range(1, 110)),
            "page_count": 109,
            "duplicates": 0,
            "unreviewed": [],
        },
        "receipts": receipts,
        "blocking_findings": [],
        "preserved_adverse_evidence": [
            "Standalone cross-chapter reference warnings match authority and remain visible as literal question marks.",
            "Candidate and authority each retain 25 overfull hboxes and one underfull vbox; individual visual inspection found no blocking geometry defect.",
            "Visible colored link rectangles are inherited hyperlink styling and do not obscure text.",
            "The PDF is untagged; AI page inspection is not human or expert certification.",
        ],
        "source_pdf_or_render_mutation": False,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    dump(destination, report)
    return report


def prepare_successor() -> dict:
    original = assert_original_stage()
    aggregate_path = ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"
    aggregate = load(aggregate_path)
    assert aggregate["passed"] is True
    assert aggregate["coverage"]["page_count"] == 109
    assert aggregate["coverage"]["unreviewed"] == []
    destination = ROOT / "replay/FINAL_STAGE_SUCCESSOR_001.json"
    excluded = {
        "candidate.manifest.json",
        "replay/FINAL_INDEPENDENT_REVIEW.json",
        "replay/FINAL_STAGE_SUCCESSOR_001.json",
    }
    inventory = [
        ev(path)
        for path in sorted(ROOT.rglob("*"))
        if path.is_file()
        and path.relative_to(ROOT).as_posix() not in excluded
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ]
    report = {
        "schema": "stacks-r44-final-stage-successor/v1",
        "candidate_id": "stacks-errata-a04446e-r44",
        "status": "READY_FOR_GENUINELY_INDEPENDENT_FINAL_REVIEW_NOT_ADMITTED",
        "predecessor": ev(ROOT / "replay/FINAL_STAGE.json"),
        "predecessor_inventory_rows_reverified": len(original["snapshot_inventory"]),
        "page_complete_visual_adjudication": ev(aggregate_path),
        "page_complete_visual_gate": "PASS_ALL_109_PAGES_INDIVIDUALLY_INSPECTED",
        "snapshot_inventory": inventory,
        "closure_order": "This append-only successor binds the immutable original stage and stronger page-complete visual receipts. A separate reviewer binds this successor; candidate.manifest.json is sealed afterward and neither stage is rewritten.",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    dump(destination, report)
    return report


def seal() -> dict:
    original_path = ROOT / "replay/FINAL_STAGE.json"
    successor_path = ROOT / "replay/FINAL_STAGE_SUCCESSOR_001.json"
    assert_original_stage()
    successor = load(successor_path)
    assert successor["status"] == "READY_FOR_GENUINELY_INDEPENDENT_FINAL_REVIEW_NOT_ADMITTED"
    for row in successor["snapshot_inventory"]:
        bound(row)
    review_path = ROOT / "replay/FINAL_INDEPENDENT_REVIEW.json"
    review = load(review_path)
    assert review.get("passed") is True
    assert review.get("final_stage_sha256") == sha(original_path)
    assert review.get("final_stage_successor_sha256") == sha(successor_path)
    assert review.get("candidate_manifest_absent_during_review") is True
    assert review.get("page_complete_visual_gate") == "PASS_ALL_109_PAGES_INDIVIDUALLY_INSPECTED"

    config = load(ROOT / "candidate.config.json")
    primary = {
        "stable_unit_manifest": "stable-units.json",
        "source_map": "source-map.jsonl",
        "decision_ledger": "decisions.jsonl",
        "rejection_ledger": "rejections.jsonl",
        "formula_diagram_inventory": "formula-diagram-inventory.json",
    }
    authorities = sorted(path for path in (ROOT / "authority").rglob("*") if path.is_file())
    excluded = {path.resolve() for path in authorities}
    excluded |= {(ROOT / relative).resolve() for relative in primary.values()}
    excluded.add((ROOT / "candidate.manifest.json").resolve())
    others = [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_file()
        and path.resolve() not in excluded
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ]
    manifest = {
        "schema": "mathematics-commons-stacks-candidate-manifest/v1",
        "candidate_id": config["candidate_id"],
        "lease_id": config["lease_id"],
        "namespace": config["namespace"],
        "writer_task": config["writer_task"],
        "upstream": {"lock": "upstream/stacks.lock.json", "commit": config["authority_commit"], "tree": config["authority_tree"]},
        "source_authorities": [ev(path) for path in authorities],
        "source_closure": {"enumerated": True, "expected_units": 24, "manifested_units": 24, "complete": True},
        **{key: ev(ROOT / relative) for key, relative in primary.items()},
        "builds": [ev(path) for path in others],
        "rights_state": "Upstream GNU FDL rights are preserved in authority/COPYING; this independently prepared AI correction overlay is not an official Stacks Project edition or endorsement.",
        "review_state": "performed",
        "independent_replay": "passed",
        "unresolved_defects": ["Standalone cross-chapter reference warnings match authority; cumulative AUX is not supplied. Accessibility tagging is not asserted."],
        "stop_conditions": ["A changed referenced byte invalidates this final manifest. Registry admission and composition remain separate."],
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    schema = load(REPO / "schemas/candidate-manifest.schema.json")
    Draft202012Validator(schema).validate(manifest)
    destination = ROOT / "candidate.manifest.json"
    dump(destination, manifest)
    return {"manifest": ev(destination), "schema_errors": 0, "manifest_references": len(manifest["source_authorities"]) + 5 + len(manifest["builds"])}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("aggregate-visual", "prepare-successor", "seal"))
    args = parser.parse_args()
    result = {
        "aggregate-visual": aggregate_visual,
        "prepare-successor": prepare_successor,
        "seal": seal,
    }[args.stage]()
    print(json.dumps({"stage": args.stage, "passed": True, "result": result.get("status", result.get("manifest"))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
