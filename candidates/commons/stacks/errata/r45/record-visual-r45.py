"""Rehash and record the already-performed bounded R45 visual review.

This script launches no TeX process and never mutates source or PDFs.  It
copies only a sanitized, relative-path render inventory into the candidate and
writes additive review receipts for the inspection already performed.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
PRIVATE = (
    REPO.parent
    / "03_projects/language_management/cjk/03_working_translations/"
      "stacks_cjk_20260821/canon/private_evidence/errata-r45-20260905/render"
)
EXPECTED_PAGES = list(range(1, 47))
SENSITIVE_PAGES = [8, 9, 10, 13, 14, 15, 16, 18, 19, 20, 22, 24, 25, 27, 28, 33, 35, 37, 39, 40, 41, 42, 43]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def ev(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def verify(path: Path, row: dict) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == row["bytes"], path
    assert sha(path) == row["sha256"], path


def main() -> int:
    private_manifest_path = PRIVATE / "render-manifest.json"
    render = load(private_manifest_path)
    assert render["published"] is False
    pdf = ROOT / "builds/topologies.pdf"
    pdf_rows = render["pdfs"]["topologies"]["renders"]
    contact_rows = render["contact_sheets"]
    high_rows = render["high_resolution"]["renders"]
    assert render["pdfs"]["topologies"]["pdf_sha256"] == sha(pdf)
    assert [row["page"] for row in pdf_rows] == EXPECTED_PAGES
    assert len(contact_rows) == 3
    assert [row["page"] for row in high_rows] == SENSITIVE_PAGES
    assert render["high_resolution"]["dpi"] == 180

    for row in pdf_rows:
        verify(PRIVATE / "topologies" / row["file"], row)
    for row in contact_rows:
        verify(PRIVATE / "contact_sheets" / row["file"], row)
    for row in high_rows:
        verify(PRIVATE / "highres" / row["file"], row)

    page_map = load(ROOT / "builds/source-page-map.json")
    assert page_map["unique_pages"] == SENSITIVE_PAGES
    assert page_map["unique_page_count"] == len(SENSITIVE_PAGES)
    build_receipt = load(ROOT / "builds/build-receipt.json")
    chapter = build_receipt["chapters"][0]
    assert build_receipt["passed"] is True
    assert chapter["candidate_log_summary"]["pages"] == 46
    assert chapter["authority_log_summary"]["pages"] == 46
    assert chapter["candidate_log_summary"]["overfull_hboxes"] == 4
    assert chapter["authority_log_summary"]["overfull_hboxes"] == 4

    public_render = {
        "schema": "mathematics-commons-stacks-render-manifest/v1",
        "candidate_id": "stacks-errata-a04446e-r45",
        "pdf": ev(pdf),
        "page_dpi": render["pdfs"]["topologies"]["dpi"],
        "pages": pdf_rows,
        "contact_sheets": contact_rows,
        "high_resolution": render["high_resolution"],
        "all_private_artifacts_rehashed": True,
        "private_paths_published": False,
    }
    public_manifest_path = ROOT / "replay/RENDER_MANIFEST.json"
    dump(public_manifest_path, public_render)

    visual = {
        "schema": "stacks-r45-page-complete-visual-adjudication/v1",
        "candidate_id": "stacks-errata-a04446e-r45",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed": True,
        "scope": {
            "pdf": ev(pdf),
            "page_count": 46,
            "covered_pages": EXPECTED_PAGES,
            "unreviewed_pages": [],
            "contact_sheet_count": 3,
            "high_resolution_pages": SENSITIVE_PAGES,
        },
        "method": (
            "Direct inspection of three ordered contact sheets covering all 46 pages, followed by direct "
            "individual inspection of all 23 correction-sensitive pages at 180 dpi."
        ),
        "blocking_findings": [],
        "checks": {
            "page_sequence": "PASS: pages 1-46 appear exactly once in order.",
            "clipping_and_margins": "PASS: no visible clipped body text, formula, diagram, footnote, header, or footer.",
            "overlap": "PASS: no visible overlapping text, formulas, diagrams, or link rectangles.",
            "glyphs": "PASS: no visible missing-glyph boxes or malformed mathematical glyphs.",
            "correction_sensitive_content": "PASS: every mapped correction page is readable and geometrically intact.",
        },
        "reviewed_contact_sheets": [
            {**row, "path": f"contact_sheets/{row['file']}", "layout_result": "PASS"}
            for row in contact_rows
        ],
        "reviewed_high_resolution_pages": [
            {**row, "path": f"highres/{row['file']}", "layout_result": "PASS"}
            for row in high_rows
        ],
        "adverse_evidence": [
            "The isolated candidate and authority readers each retain four inherited overfull-hbox diagnostics; inspection found no visible boundary breach.",
            "Literal unresolved cross-chapter references remain in the isolated reader. The deterministic receipt separately verifies the configured signed reference-key deltas and no unaccounted target change.",
            "Red internal-link and green citation rectangles are visible retained hyperlink styling and do not obscure text.",
            "The validation PDF is untagged; no accessibility-tagging or human/expert certification claim is made.",
        ],
        "render_manifest": ev(public_manifest_path),
        "source_or_pdf_mutation": False,
    }
    visual_path = ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"
    dump(visual_path, visual)

    stage = {
        "schema": "stacks-r45-build-render-stage/v1",
        "candidate_id": "stacks-errata-a04446e-r45",
        "status": "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS",
        "build_receipt": ev(ROOT / "builds/build-receipt.json"),
        "deterministic_replay": ev(ROOT / "builds/deterministic-replay.json"),
        "tex_mutex_success": ev(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "tex_mutex_adverse_attempt": ev(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json"),
        "source_page_map": ev(ROOT / "builds/source-page-map.json"),
        "render_manifest": ev(public_manifest_path),
        "visual_adjudication": ev(visual_path),
        "pages": 46,
        "contact_sheets": 3,
        "high_resolution_pages": SENSITIVE_PAGES,
        "adverse_history": (
            "Attempt 001 completed both TeX build pairs but its post-build validator failed because the generic "
            "reference-parity rule did not account for five intentional reference-key replacements. The validator "
            "was corrected to require the exact signed -5/+5 target delta, and the entire deterministic build was "
            "repeated under the mutex successfully."
        ),
        "generated_source_composed": False,
        "registry_admission": "NOT_PERFORMED",
    }
    stage_path = ROOT / "builds/BUILD_RENDER_STAGE.json"
    dump(stage_path, stage)
    print(json.dumps({"passed": True, "pages": 46, "sensitive_pages": 23, "visual_sha256": sha(visual_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
