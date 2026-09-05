"""Record the already-performed bounded R42 render and visual review.

This script never launches TeX or changes source.  It rehashes the private
render closure and writes only additive candidate receipts.
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
      "stacks_cjk_20260821/canon/private_evidence/errata-r42-20260905/render"
)


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


def evidence(path: Path, relative_to: Path = ROOT) -> dict:
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def verify_private(path: Path, row: dict) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == row["bytes"], path
    assert sha(path) == row["sha256"], path


def main() -> int:
    manifest_path = PRIVATE / "render-manifest.json"
    render = load(manifest_path)
    pdf = ROOT / "builds/descent.pdf"
    assert render["pdfs"]["descent"]["pdf_sha256"] == sha(pdf)
    assert [row["page"] for row in render["pdfs"]["descent"]["renders"]] == list(range(1, 94))

    page_rows = render["pdfs"]["descent"]["renders"]
    contact_rows = render["contact_sheets"]
    high_rows = render["high_resolution"]["renders"]
    for row in page_rows:
        verify_private(PRIVATE / "descent" / row["file"], row)
    for row in contact_rows:
        verify_private(PRIVATE / "contact_sheets" / row["file"], row)
    for row in high_rows:
        verify_private(PRIVATE / "highres" / row["file"], row)

    changed_pages = load(ROOT / "builds/source-page-map.json")["unique_pages"]
    high_pages = [row["page"] for row in high_rows]
    assert set(changed_pages).issubset(high_pages)
    build_receipt = load(ROOT / "builds/build-receipt.json")
    chapter = build_receipt["chapters"][0]
    candidate_summary = chapter["candidate_log_summary"]
    authority_summary = chapter["authority_log_summary"]
    for key in ("overfull_hboxes", "underfull_hboxes", "overfull_vboxes", "underfull_vboxes"):
        assert candidate_summary[key] == authority_summary[key]
    page_count = len(page_rows)
    contact_count = len(contact_rows)
    assert page_count == candidate_summary["pages"] == authority_summary["pages"] == 93
    diagnostic_pages = [8, 12, 13, 14, 31, 34, 35, 36, 37, 42, 62, 92]
    assert set(diagnostic_pages).issubset(high_pages)

    raw = {
        "schema": "stacks-r42-bounded-visual-review/v1",
        "reviewer": "descent_packet_audit",
        "producer_status": "producer_uncertified",
        "scope": {
            "pdf": "builds/descent.pdf",
            "pdf_bytes": pdf.stat().st_size,
            "pdf_sha256": sha(pdf),
            "assigned_pages": [1, page_count],
            "total_pdf_pages": page_count,
            "reviewed_pages_count": page_count,
            "unreviewed_pages_in_assignment": [],
        },
        "method": (
            f"Direct inspection of all {contact_count} 4x4 contact sheets covering pages 1-{page_count}, "
            f"then direct individual inspection of {len(high_rows)} existing 180-dpi renders: "
            f"all {len(changed_pages)} correction-sensitive pages and all {len(diagnostic_pages)} pages carrying "
            "candidate/authority box diagnostics. No source, PDF, or render mutation."
        ),
        "render_manifest": {
            "file": "render-manifest.json",
            "bytes": manifest_path.stat().st_size,
            "sha256": sha(manifest_path),
        },
        "result": "PASS_LAYOUT_WITH_RECORDED_CAVEATS",
        "blocking_layout_defects": [],
        "checks": {
            "page_clipping": "No visible clipped body text, display, diagram, footnote, or bibliography content.",
            "overlap": "No observed overlapping body text, formulas, diagram labels, or footnotes.",
            "glyphs": "No visible missing-glyph boxes or broken mathematical glyphs.",
            "margins": "All inspected material remains inside the physical page; running headers and text areas are consistent.",
            "correction_sensitive_pages": (
                "All edited prose and formulas on pages "
                + ",".join(str(page) for page in changed_pages)
                + " are readable and geometrically intact."
            ),
            "sequence": f"{contact_count} contact sheets cover every page exactly once in page order 1-{page_count}.",
        },
        "adverse_evidence": [
            {
                "kind": "unresolved_cross_references",
                "observation": "Literal ?? references remain visible in this standalone chapter build; the deterministic build receipt proves the candidate and authority target multisets are equal.",
            },
            {
                "kind": "inherited_box_diagnostics",
                "observation": (
                    f"Candidate and authority each report {candidate_summary['overfull_hboxes']} overfull hboxes and "
                    f"{candidate_summary['underfull_vboxes']} underfull vbox. Every corresponding page was inspected "
                    "at 180 dpi and no blocking visual defect was found."
                ),
            },
            {
                "kind": "visible_link_borders",
                "observation": "Red internal-link and green citation rectangles are visible and do not obscure text; they are retained hyperlink styling.",
            },
            {
                "kind": "coverage_limit",
                "observation": "Contact sheets establish complete page and layout coverage, but do not constitute character-level reading of every unmodified page. All correction and diagnostic pages received individual high-resolution inspection.",
            },
        ],
        "viewed_contact_artifacts": [
            {**row, "path": f"contact_sheets/{row['file']}", "matches_manifest": True}
            for row in contact_rows
        ],
        "viewed_high_resolution_artifacts": [
            {**row, "path": f"highres/{row['file']}", "matches_manifest": True, "layout_result": "PASS"}
            for row in high_rows
        ],
        "correction_sensitive_pages": changed_pages,
        "diagnostic_pages": diagnostic_pages,
        "absolute_private_paths_in_receipt": False,
    }
    raw_path = ROOT / "replay/VISUAL_PAGES_001_093.json"
    dump(raw_path, raw)

    aggregate = {
        "schema": "stacks-r42-visual-adjudication/v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "candidate_id": "stacks-errata-a04446e-r42",
        "passed": True,
        "scope": "Bounded AI visual layout review of the 93-page correction-validation reader; not complete-corpus reference resolution or independent mathematical certification.",
        "pdf_sha256": sha(pdf),
        "covered_pages": list(range(1, page_count + 1)),
        "blocking_findings": [],
        "reviews": [
            {
                **evidence(raw_path),
                "page_start": 1,
                "page_end": page_count,
                "method": (
                    f"{contact_count} contact sheets cover all {page_count} pages; {len(high_rows)} individual 180-dpi "
                    "correction-sensitive and diagnostic pages were also inspected."
                ),
            }
        ],
        "caveats": [
            "Literal ?? cross-chapter references remain; build/reference parity with authority is a separate deterministic check.",
            f"{candidate_summary['overfull_hboxes']} overfull hboxes and {candidate_summary['underfull_vboxes']} underfull vbox remain in both candidate and authority; no warning-free claim is made.",
            "Contact-sheet coverage is not character-level inspection of every unmodified page.",
            "The PDF is untagged; AI inspection is not human or expert certification.",
        ],
        "disposition": "Pass the bounded visual-layout gate with adverse evidence preserved; independent final-stage validation and registry admission remain separate.",
        "source_or_pdf_mutation": False,
    }
    aggregate_path = ROOT / "replay/VISUAL_ADJUDICATION.json"
    dump(aggregate_path, aggregate)

    identities = [
        evidence(ROOT / name)
        for name in (
            "builds/descent.pdf",
            "builds/descent.authority.pdf",
            "builds/build-execution.json",
            "builds/build-receipt.json",
            "builds/deterministic-replay.json",
            "builds/TEX_MUTEX_RECEIPT.json",
            "builds/source-page-map.json",
            "replay-build.py",
            "derive-visual-pages.py",
            "replay/SOURCE_INDEPENDENT_VALIDATION.json",
            "replay/VISUAL_PAGES_001_093.json",
            "replay/VISUAL_ADJUDICATION.json",
        )
    ]
    stage = {
        "schema": "stacks-r42-build-render-stage-v1",
        "status": "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS",
        "identities": identities,
        "candidate": chapter["candidate_log_summary"],
        "authority": chapter["authority_log_summary"],
        "render": {
            "path": "canon/private_evidence/errata-r42-20260905/render/render-manifest.json",
            "bytes": manifest_path.stat().st_size,
            "sha256": sha(manifest_path),
            "checked": len(page_rows) + len(contact_rows) + len(high_rows),
            "failures": [],
            "pages": len(page_rows),
            "contact_sheets": len(contact_rows),
            "high_resolution_pages": high_pages,
        },
        "tex_mutex": evidence(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "operational_findings": [
            "Both candidate and authority PDFs reproduced byte-for-byte across two fresh isolated builds under one continuously held named mutex.",
            "All private render artifacts were rehashed against render-manifest.json.",
            f"The complete {page_count}-page contact-sheet review and all {len(high_rows)} enlarged sensitive/diagnostic page reviews found no blocking visual defect.",
        ],
        "visual_inspection": "PERFORMED_PASS_WITH_RECORDED_CAVEATS",
        "independent_full_candidate_replay": "NOT_PERFORMED",
        "admission": "NOT_PERFORMED",
        "preservation": "Source-stage config, inputs, receipts, and the committed lease boundary remain untouched.",
        "next_action": "Run final mechanical closure, freeze the final-stage snapshot, obtain independent review, and seal the candidate manifest before registry admission.",
    }
    dump(ROOT / "builds/BUILD_RENDER_STAGE.json", stage)
    print(json.dumps({
        "passed": True,
        "pages": page_count,
        "contacts": len(contact_rows),
        "high_resolution": len(high_rows),
        "visual_receipt_sha256": sha(raw_path),
        "aggregate_sha256": sha(aggregate_path),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
