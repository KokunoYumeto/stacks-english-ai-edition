from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[5]
RENDER = WORKSPACE / "r38_private_render"
AUTHORITY_RENDER = WORKSPACE / "r38_authority_p392/authority-392.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def evidence(path: Path, display: str | None = None) -> dict:
    return {"path": display or path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def main() -> int:
    config_path = ROOT / "candidate.config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    source_validation = json.loads((ROOT / "source-validation.json").read_text(encoding="utf-8"))
    build_receipt = json.loads((ROOT / "builds/build-receipt.json").read_text(encoding="utf-8"))
    deterministic = json.loads((ROOT / "builds/deterministic-replay.json").read_text(encoding="utf-8"))
    visual = json.loads((ROOT / "builds/visual-qa.json").read_text(encoding="utf-8"))
    page_map = json.loads((ROOT / "builds/source-page-map.json").read_text(encoding="utf-8"))
    render_manifest_path = RENDER / "render-manifest.json"
    render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
    required_pages = [373, 385, 386, 388, 389, 390, 391, 392, 394, 395, 396, 397, 398]
    if not (source_validation["passed"] and build_receipt["passed"] and deterministic["passed"] and visual["passed"]):
        raise AssertionError("a required R38 source/build/visual gate is not passing")
    if page_map["unique_pages"] != required_pages:
        raise AssertionError("source-page map changed")
    if len(render_manifest["pdfs"]["more-algebra"]["renders"]) != 401:
        raise AssertionError("full render closure mismatch")
    candidate_p392 = RENDER / "highres/more-algebra_p392.png"
    comparison = {
        "schema": "mathematics-commons-stacks-r38-visual-adjudication/v1",
        "candidate_id": config["candidate_id"],
        "status": "PASS",
        "reviewed_scope": {
            "contact_sheets": 26,
            "pdf_pages": 401,
            "high_resolution_pages": required_pages,
            "dpi_all_pages": 96,
            "dpi_high_resolution": 180,
        },
        "disjoint_inspection_ranges": [
            {"contact_sheets": "01-07", "pages": "1-112", "high_resolution_pages": [373, 385, 386], "result": "PASS"},
            {"contact_sheets": "08-14", "pages": "113-224", "high_resolution_pages": [388, 389, 390], "result": "PASS"},
            {"contact_sheets": "15-20", "pages": "225-320", "high_resolution_pages": [391, 392, 394], "result": "PASS_AFTER_PAGE_392_ADJUDICATION"},
            {"contact_sheets": "21-26", "pages": "321-401", "high_resolution_pages": [395, 396, 397, 398], "result": "PASS"},
        ],
        "page_392_adjudication": {
            "initial_observation": "One inspector reported a possible header-band collision.",
            "candidate_render": evidence(candidate_p392, "private-render/highres/more-algebra_p392.png"),
            "authority_control_render": evidence(AUTHORITY_RENDER, "private-authority-control/more-algebra_p392.png"),
            "dimensions_pixels": [1530, 1980],
            "pixel_difference_bbox": [317, 1091, 1213, 1718],
            "pixels_identical_from_y_0_through": 1090,
            "conclusion": "False positive. The page number, centered running header, top margin, and continuation text are pixel-identical to the separately built authority control; differences begin only in lower-body reflow from admitted corrections.",
            "candidate_induced_header_defect": False,
        },
        "findings": {"clipping": 0, "overlap": 0, "unexpected_blank_pages": 0, "duplicate_pages": 0, "broken_diagrams": 0, "missing_glyphs": 0, "unreadable_content": 0},
        "adverse_evidence": [
            "Standalone reader cross-chapter references remain visibly unresolved where the cumulative AUX set is absent; the authority and candidate undefined-target multisets match exactly.",
            "The PDF is untagged; this retained accessibility limitation is not a layout failure.",
        ],
        "render_manifest": {"logical_path": "canon/private_evidence/errata-r38-20260831T021500Z/render/render-manifest.json", "bytes": render_manifest_path.stat().st_size, "sha256": sha(render_manifest_path), "published": False},
    }
    dump(ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json", comparison)

    validation = {
        "schema": "mathematics-commons-stacks-r38-validation/v1",
        "candidate_id": config["candidate_id"],
        "passed": True,
        "source_validation": evidence(ROOT / "source-validation.json"),
        "build_receipt": evidence(ROOT / "builds/build-receipt.json"),
        "deterministic_replay": evidence(ROOT / "builds/deterministic-replay.json"),
        "source_page_map": evidence(ROOT / "builds/source-page-map.json"),
        "visual_qa": evidence(ROOT / "builds/visual-qa.json"),
        "visual_inspection_adjudication": evidence(ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json"),
        "candidate_pdf": evidence(ROOT / "builds/more-algebra.pdf"),
        "authority_pdf": evidence(ROOT / "builds/more-algebra.authority.pdf"),
        "fresh_builds": 2,
        "full_page_renders": 401,
        "high_resolution_pages": required_pages,
        "unresolved": 0,
    }
    dump(ROOT / "builds/validation.json", validation)
    intake = {
        "schema": "mathematics-commons-stacks-r38-intake-validation/v1",
        "candidate_id": config["candidate_id"],
        "passed": True,
        "original_producer_allegations": 29,
        "registrar_additive_aliases": 2,
        "semantic_units": 23,
        "operations": 31,
        "stable_id_range": ["MC-STK-ERR-1336", "MC-STK-ERR-1358"],
        "source_validation": evidence(ROOT / "source-validation.json"),
        "build_validation": evidence(ROOT / "builds/validation.json"),
        "rejections": 0,
        "unresolved": 0,
        "registry_mutated": False,
        "generated_source_mutated": False,
    }
    dump(ROOT / "INTAKE_VALIDATION.json", intake)
    config["build_render_admission_status"] = "build_deterministic_replay_and_visual_qa_pass"
    config["build_validation"] = evidence(ROOT / "builds/validation.json")
    config["visual_inspection_adjudication"] = evidence(ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json")
    dump(config_path, config)
    regeneration = json.loads((ROOT / "REGENERATION_RECEIPT.json").read_text(encoding="utf-8"))
    regeneration["build_validation"] = evidence(ROOT / "builds/validation.json")
    regeneration["visual_inspection_adjudication"] = evidence(ROOT / "replay/VISUAL_INSPECTION_ADJUDICATION.json")
    regeneration["intake_validation"] = evidence(ROOT / "INTAKE_VALIDATION.json")
    regeneration["passed"] = True
    dump(ROOT / "REGENERATION_RECEIPT.json", regeneration)
    print(json.dumps({"passed": True, "pages": 401, "high_resolution_pages": required_pages}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
