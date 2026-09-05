"""Record the already-performed bounded R44 render and visual review.

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
      "stacks_cjk_20260821/canon/private_evidence/errata-r44-20260905/render"
)
PRIVATE_BUILD_ROOTS = [PRIVATE.parent / "build-1", PRIVATE.parent / "build-2"]


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
    pdf = ROOT / "builds/perfect.pdf"
    assert render["pdfs"]["perfect"]["pdf_sha256"] == sha(pdf)
    assert [row["page"] for row in render["pdfs"]["perfect"]["renders"]] == list(range(1, 110))

    page_rows = render["pdfs"]["perfect"]["renders"]
    contact_rows = render["contact_sheets"]
    high_rows = render["high_resolution"]["renders"]
    for row in page_rows:
        verify_private(PRIVATE / "perfect" / row["file"], row)
    for row in contact_rows:
        verify_private(PRIVATE / "contact_sheets" / row["file"], row)
    for row in high_rows:
        verify_private(PRIVATE / "highres" / row["file"], row)

    changed_pages = load(ROOT / "builds/source-page-map.json")["unique_pages"]
    high_pages = [row["page"] for row in high_rows]
    assert set(changed_pages).issubset(high_pages)
    build_receipt = load(ROOT / "builds/build-receipt.json")
    execution = load(ROOT / "builds/build-execution.json")
    deterministic = load(ROOT / "builds/deterministic-replay.json")
    assert execution["passed"] is True and execution["candidate_id"] == "stacks-errata-a04446e-r44"
    assert deterministic["passed"] is True
    assert deterministic["candidate_id"] == "stacks-errata-a04446e-r44"
    assert deterministic["fresh_builds_compared"] == 2
    assert deterministic["recorder_fls_closures_compared"] == 2
    deterministic_phases = {row["phase"]: row for row in deterministic["pdfs"]}
    assert set(deterministic_phases) == {"candidate", "authority"}
    for phase_name in ("candidate", "authority"):
        phase = execution[f"{phase_name}_phase"]["stems"]["perfect"]
        pdflatex_commands = [row for row in phase["commands"] if row["role"].startswith("pdflatex_")]
        assert len(pdflatex_commands) == 3
        assert all(
            "-recorder" in (row["argv"].split() if isinstance(row["argv"], str) else row["argv"])
            for row in pdflatex_commands
        )
        outputs = phase["outputs"]
        for output_name in ("fls", "fls_dependencies"):
            output = outputs[output_name]
            output_path = ROOT / output["path"]
            assert output_path.is_file()
            assert output_path.stat().st_size == output["bytes"]
            assert sha(output_path) == output["sha256"]
        inventory = load(ROOT / outputs["fls_dependencies"]["path"])
        assert inventory["candidate_id"] == "stacks-errata-a04446e-r44"
        assert inventory["phase"] == phase_name and inventory["stem"] == "perfect"
        assert inventory["recorder_enabled"] is True
        assert inventory["all_inputs_exist_and_hashed"] is True
        assert inventory["outputs_confined_to_worktree"] is True
        assert inventory["input_count"] == len(inventory["inputs"]) > 0
        assert inventory["output_count"] == len(inventory["outputs"]) > 0
        fls_path = ROOT / outputs["fls"]["path"]
        deterministic_row = deterministic_phases[phase_name]
        assert deterministic_row["stem"] == "perfect"
        assert deterministic_row["fls_input_closure_byte_identical"] is True
        assert deterministic_row["fls_input_closure_sha256"] == inventory["input_closure_sha256"]
        assert deterministic_row["second_fls_inventory_sha256"] == sha(ROOT / outputs["fls_dependencies"]["path"])
        private_prefix = f"perfect.{phase_name}"
        for build_index, private_root in enumerate(PRIVATE_BUILD_ROOTS):
            private_fls = private_root / f"{private_prefix}.fls"
            private_inventory = private_root / f"{private_prefix}.fls-dependencies.json"
            private_inventory_doc = load(private_inventory)
            assert private_fls.stat().st_size == private_inventory_doc["raw_fls_bytes"]
            assert sha(private_fls) == private_inventory_doc["raw_fls_sha256"]
            assert private_inventory_doc["input_closure_sha256"] == inventory["input_closure_sha256"]
            expected_inventory_sha = deterministic_row[
                "first_fls_inventory_sha256" if build_index == 0 else "second_fls_inventory_sha256"
            ]
            assert sha(private_inventory) == expected_inventory_sha
    chapter = build_receipt["chapters"][0]
    assert build_receipt["candidate_id"] == "stacks-errata-a04446e-r44"
    assert chapter["stem"] == "perfect"
    candidate_summary = chapter["candidate_log_summary"]
    authority_summary = chapter["authority_log_summary"]
    for key in ("overfull_hboxes", "underfull_hboxes", "overfull_vboxes", "underfull_vboxes"):
        assert candidate_summary[key] == authority_summary[key]
    page_count = len(page_rows)
    contact_count = len(contact_rows)
    assert page_count == candidate_summary["pages"] == authority_summary["pages"] == 109
    diagnostic_pages = [11, 12, 13, 15, 16, 25, 26, 28, 32, 33, 39, 43, 49, 50, 58, 59, 65, 96, 97, 99, 100, 101, 102, 108]
    assert set(diagnostic_pages).issubset(high_pages)

    raw = {
        "schema": "stacks-r44-bounded-visual-review/v1",
        "reviewer": "perfect_packet_audit",
        "producer_status": "producer_uncertified",
        "scope": {
            "pdf": "builds/perfect.pdf",
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
    raw_path = ROOT / "replay/VISUAL_PAGES_001_109.json"
    dump(raw_path, raw)

    aggregate = {
        "schema": "stacks-r44-visual-adjudication/v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "candidate_id": "stacks-errata-a04446e-r44",
        "passed": True,
        "scope": "Bounded AI visual layout review of the 109-page correction-validation reader; not complete-corpus reference resolution or independent mathematical certification.",
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
            "builds/perfect.pdf",
            "builds/perfect.authority.pdf",
            "builds/perfect.fls",
            "builds/perfect.authority.fls",
            "builds/perfect.fls-dependencies.json",
            "builds/perfect.authority.fls-dependencies.json",
            "builds/build-execution.json",
            "builds/build-receipt.json",
            "builds/deterministic-replay.json",
            "builds/TEX_MUTEX_RECEIPT.json",
            "builds/source-page-map.json",
            "replay-build.py",
            "derive-visual-pages.py",
            "replay/SOURCE_INDEPENDENT_VALIDATION.json",
            "replay/VISUAL_PAGES_001_109.json",
            "replay/VISUAL_ADJUDICATION.json",
        )
    ]
    stage = {
        "schema": "stacks-r44-build-render-stage-v1",
        "status": "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS",
        "identities": identities,
        "candidate": chapter["candidate_log_summary"],
        "authority": chapter["authority_log_summary"],
        "render": {
            "path": "canon/private_evidence/errata-r44-20260905/render/render-manifest.json",
            "bytes": manifest_path.stat().st_size,
            "sha256": sha(manifest_path),
            "checked": len(page_rows) + len(contact_rows) + len(high_rows),
            "failures": [],
            "pages": len(page_rows),
            "contact_sheets": len(contact_rows),
            "high_resolution_pages": high_pages,
        },
        "tex_mutex": evidence(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "recorder_fls": {
            "prospective_gate": "PASS",
            "pdflatex_invocations_with_recorder": 6,
            "fresh_phase_closures_compared": deterministic["recorder_fls_closures_compared"],
            "candidate_input_closure_sha256": deterministic_phases["candidate"]["fls_input_closure_sha256"],
            "authority_input_closure_sha256": deterministic_phases["authority"]["fls_input_closure_sha256"],
            "all_inputs_exist_and_hashed": True,
            "outputs_confined_to_worktree": True,
            "private_build_roots_rehashed": 2,
            "public_fls_transcripts_sanitized": True,
        },
        "operational_findings": [
            "Both candidate and authority PDFs and their recorder/FLS input closures reproduced byte-for-byte across two fresh isolated builds under one continuously held named mutex.",
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
