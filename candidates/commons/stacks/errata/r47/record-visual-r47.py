"""Record the completed page-complete R47 visual review without rerendering."""
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
      "stacks_cjk_20260821/canon/private_evidence/errata-r47-20260905/render"
)
CANDIDATE_ID = "stacks-errata-a04446e-r47"
STEM = "more-groupoids"
EXPECTED_PAGES = list(range(1, 37))
SENSITIVE_PAGES = [3, 4, 5, 6, 7, 8, 9, 10, 12, 19, 21, 22, 26, 27, 29, 31]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def ev(path: Path) -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def verify(path: Path, row: dict) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == row["bytes"], path
    assert sha(path) == row["sha256"], path


def main() -> int:
    private_manifest_path = PRIVATE / "render-manifest.json"
    render = load(private_manifest_path)
    assert render["published"] is False
    pdf = ROOT / "builds/more-groupoids.pdf"
    pdf_rows = render["pdfs"][STEM]["renders"]
    contact_rows = render["contact_sheets"]
    high_rows = render["high_resolution"]["renders"]
    assert render["pdfs"][STEM]["pdf_sha256"] == sha(pdf)
    assert [row["page"] for row in pdf_rows] == EXPECTED_PAGES
    assert len(contact_rows) == 3
    assert [row["page"] for row in high_rows] == SENSITIVE_PAGES
    assert render["high_resolution"]["dpi"] == 180

    for row in pdf_rows:
        verify(PRIVATE / STEM / row["file"], row)
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
    assert chapter["candidate_log_summary"]["pages"] == 36
    assert chapter["authority_log_summary"]["pages"] == 36
    assert chapter["candidate_log_summary"]["overfull_hboxes"] == 1
    assert chapter["authority_log_summary"]["overfull_hboxes"] == 1
    assert chapter["candidate_log_summary"]["underfull_vboxes"] == 1
    assert chapter["authority_log_summary"]["underfull_vboxes"] == 1

    public_render = {
        "schema": "mathematics-commons-stacks-render-manifest/v1",
        "candidate_id": CANDIDATE_ID,
        "pdf": ev(pdf),
        "page_dpi": render["pdfs"][STEM]["dpi"],
        "pages": pdf_rows,
        "contact_sheets": contact_rows,
        "high_resolution": render["high_resolution"],
        "all_private_artifacts_rehashed": True,
        "private_paths_published": False,
    }
    public_manifest_path = ROOT / "replay/RENDER_MANIFEST.json"
    dump(public_manifest_path, public_render)

    visual = {
        "schema": "stacks-r47-page-complete-visual-adjudication/v1",
        "candidate_id": CANDIDATE_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "passed": True,
        "scope": {
            "pdf": ev(pdf),
            "page_count": 36,
            "covered_pages": EXPECTED_PAGES,
            "unreviewed_pages": [],
            "contact_sheet_count": 3,
            "high_resolution_pages": SENSITIVE_PAGES,
        },
        "method": (
            "Direct inspection of three ordered contact sheets covering all 36 pages, "
            "followed by direct individual inspection of all 16 correction-sensitive "
            "pages at 180 dpi."
        ),
        "blocking_findings": [],
        "checks": {
            "page_sequence": "PASS: pages 1-36 appear exactly once in order.",
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
            "The isolated candidate and authority readers each retain one inherited overfull-hbox and one inherited underfull-vbox diagnostic; inspection found no visible boundary breach.",
            "Literal unresolved cross-chapter references remain in the isolated reader; candidate and authority target multisets are identical.",
            "Red internal-link and green citation rectangles are retained hyperlink styling and do not obscure text.",
            "The validation PDF is untagged; no accessibility-tagging or human/expert certification claim is made.",
        ],
        "render_manifest": ev(public_manifest_path),
        "source_or_pdf_mutation": False,
    }
    visual_path = ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"
    dump(visual_path, visual)

    stage = {
        "schema": "stacks-r47-build-render-stage/v1",
        "candidate_id": CANDIDATE_ID,
        "status": "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS",
        "build_receipt": ev(ROOT / "builds/build-receipt.json"),
        "deterministic_replay": ev(ROOT / "builds/deterministic-replay.json"),
        "tex_mutex_success": ev(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "tex_mutex_adverse_attempt": ev(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json"),
        "source_page_map": ev(ROOT / "builds/source-page-map.json"),
        "render_manifest": ev(public_manifest_path),
        "visual_adjudication": ev(visual_path),
        "pages": 36,
        "contact_sheets": 3,
        "high_resolution_pages": SENSITIVE_PAGES,
        "adverse_history": (
            "Attempt 001 acquired and released the TeX mutex but failed closed before "
            "starting TeX because its requested work root was outside the required "
            "temporary-directory boundary. The full workflow was then repeated with "
            "fresh temporary work roots and passed."
        ),
        "generated_source_composed": False,
        "registry_admission": "NOT_PERFORMED",
    }
    stage_path = ROOT / "builds/BUILD_RENDER_STAGE.json"
    dump(stage_path, stage)
    print(json.dumps({
        "passed": True,
        "pages": 36,
        "sensitive_pages": 16,
        "visual_sha256": sha(visual_path),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
