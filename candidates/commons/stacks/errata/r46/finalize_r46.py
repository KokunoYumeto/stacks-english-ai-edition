"""Fail-closed mechanical closure, snapshot, and manifest sealing for R46."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
PRIVATE_BASE = (
    REPO.parent
    / "03_projects/language_management/cjk/03_working_translations/"
      "stacks_cjk_20260821/canon/private_evidence/errata-r46-20260905"
)
PRIVATE_RENDER = PRIVATE_BASE / "render"
PRIVATE_BUILD_ROOTS = [PRIVATE_BASE / "build-3", PRIVATE_BASE / "build-4"]
CANDIDATE_ID = "stacks-errata-a04446e-r46"
STEM = "groupoids"
PAGE_COUNT = 55
UNIT_COUNT = 43
OPERATION_COUNT = 46
REJECTION_COUNT = 4


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


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


def bound(row: dict) -> Path:
    path = (ROOT / row["path"]).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), row
    if "bytes" in row:
        assert path.stat().st_size == row["bytes"], row["path"]
    assert sha(path) == row["sha256"], row["path"]
    return path


def replay_source() -> dict:
    authority_path = ROOT / "authority/source/groupoids.tex"
    payload_path = ROOT / "payload/groupoids.tex"
    authority = authority_path.read_bytes()
    payload = payload_path.read_bytes()
    spec = load(ROOT / "operation-spec.json")
    operations = spec["operations"]
    assert spec["operation_count"] == len(operations) == OPERATION_COUNT
    operation_ids = [row["operation_id"] for row in operations]
    assert len(operation_ids) == len(set(operation_ids))
    intervals = sorted(
        (row["start_byte"], row["end_byte_exclusive"], row["operation_id"])
        for row in operations
    )
    assert all(left[1] <= right[0] for left, right in zip(intervals, intervals[1:]))
    source_lines = authority.decode("utf-8").splitlines()
    for row in operations:
        old = row["old_text"].encode("utf-8")
        replacement = row["replacement_text"].encode("utf-8")
        assert len(old) == row["old_bytes"] and sha_bytes(old) == row["old_sha256"]
        assert len(replacement) == row["replacement_bytes"]
        assert sha_bytes(replacement) == row["replacement_sha256"]
        assert authority[row["start_byte"]:row["end_byte_exclusive"]] == old
        # The exact byte interval is controlling.  Some producer line locators
        # deliberately exclude adjacent context or a terminal newline.
        assert 1 <= row["source_start_line"] <= row["source_end_line"] <= len(source_lines)
    replayed = bytearray(authority)
    for row in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        replayed[row["start_byte"]:row["end_byte_exclusive"]] = row["replacement_text"].encode("utf-8")
    assert bytes(replayed) == payload
    return {
        "authority": authority_path,
        "payload": payload_path,
        "operation_ids": operation_ids,
    }


def validate_source_stage() -> dict:
    replay = replay_source()
    review = load(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json")
    assert review["passed"] is True and review["candidate_id"] == CANDIDATE_ID
    for key in (
        "adjudication", "authority", "decisions", "operation_spec", "payload",
        "source_map", "source_validation", "stable_units",
    ):
        bound(review[key])
    assert review["replay"]["semantic_units"] == UNIT_COUNT
    assert review["replay"]["exact_operations"] == OPERATION_COUNT
    assert review["replay"]["exact_preimages"] == OPERATION_COUNT
    assert review["replay"]["payload_byte_exact"] is True
    assert review["replay"]["unlisted_byte_changes"] == 0

    units_doc = load(ROOT / "stable-units.json")
    units = units_doc["units"]
    stable_ids = [row["id"] for row in units]
    assert units_doc["unit_count"] == len(units) == UNIT_COUNT
    assert stable_ids == [f"MC-STK-ERR-{number}" for number in range(1480, 1523)]
    assert len({row["producer_id"] for row in units}) == UNIT_COUNT
    assert sorted(op for unit in units for op in unit["operation_ids"]) == sorted(replay["operation_ids"])
    decisions = jsonl(ROOT / "decisions.jsonl")
    rejections = jsonl(ROOT / "rejections.jsonl")
    assert len(decisions) == UNIT_COUNT + REJECTION_COUNT
    accepted_decisions = [row for row in decisions if row["stable_id"] is not None]
    rejected_decisions = [row for row in decisions if row["stable_id"] is None]
    assert len(accepted_decisions) == UNIT_COUNT
    assert len(rejected_decisions) == REJECTION_COUNT
    assert {row["stable_id"] for row in accepted_decisions} == set(stable_ids)
    assert len(rejections) == REJECTION_COUNT
    assert len({row["producer_id"] for row in rejections}) == REJECTION_COUNT

    config = load(ROOT / "candidate.config.json")
    assert config["candidate_id"] == CANDIDATE_ID
    assert config["accepted"] == UNIT_COUNT
    assert config["operation_count"] == OPERATION_COUNT
    assert config["rejected"] == REJECTION_COUNT
    assert config["payload_expected_sha256"] == sha(replay["payload"])
    assert config["expected_unit_ids"] == stable_ids
    assert config["stems"][STEM]["build_exceptions"]["candidate_undefined_reference_target_deltas"] == {}
    assert load(ROOT / "candidate.config.input.json") == config

    regeneration = load(ROOT / "REGENERATION_RECEIPT.json")
    assert regeneration["schema"] == "stacks-r46-source-regeneration/v1"
    assert regeneration["status"] == "SOURCE_REPLAY_PASS_BUILD_PENDING"
    for key in ("pipeline", "source_validation", "operation_spec", "stable_units", "source_map", "payload"):
        bound(regeneration[key])
    return {"review": review, "config": config, "stable_ids": stable_ids, **replay}


def validate_build() -> dict:
    receipt = load(ROOT / "builds/build-receipt.json")
    execution = load(ROOT / "builds/build-execution.json")
    deterministic = load(ROOT / "builds/deterministic-replay.json")
    mutex = load(ROOT / "builds/TEX_MUTEX_RECEIPT.json")
    attempt = load(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json")
    assert receipt["passed"] is True and receipt["candidate_id"] == CANDIDATE_ID
    assert execution["passed"] is True and execution["candidate_id"] == CANDIDATE_ID
    assert deterministic["passed"] is True and deterministic["candidate_id"] == CANDIDATE_ID
    assert deterministic["fresh_builds_compared"] == 2
    assert deterministic["recorder_fls_closures_compared"] == 2
    assert mutex["passed"] is True and mutex["acquired"] is True and mutex["released"] is True
    assert mutex["mutex_name"] == "Global\\InterlanguageTeXSlotV1"
    assert attempt["passed"] is False and attempt["acquired"] is True and attempt["released"] is True
    assert attempt["guarded_commands"][-1]["role"] == "immediate_log_and_build_preflight"
    assert attempt["guarded_commands"][-1]["exit_code"] == 1
    for row in (
        receipt["deterministic_replay"], receipt["tex_mutex"], receipt["execution"],
        receipt["recipe"], receipt["runner"],
    ):
        bound(row)

    chapter = receipt["chapters"][0]
    assert chapter["stem"] == STEM and chapter["passed"] is True
    assert chapter["candidate_page_delta_matches"] is True
    assert chapter["undefined_target_multisets_match_authority"] is True
    for name in (
        "candidate_source", "authority_source", "candidate_pdf", "authority_pdf",
        "candidate_log", "authority_log", "candidate_stdout", "authority_stdout",
        "candidate_bibtex", "authority_bibtex", "candidate_fls", "authority_fls",
    ):
        bound(chapter[name])
    for name in ("candidate_fls_dependencies", "authority_fls_dependencies"):
        bound(chapter[name]["artifact"])

    phases = {row["phase"]: row for row in deterministic["pdfs"]}
    assert set(phases) == {"candidate", "authority"}
    fls_results = {}
    for phase_name in ("candidate", "authority"):
        phase = execution[f"{phase_name}_phase"]["stems"][STEM]
        commands = [row for row in phase["commands"] if row["role"].startswith("pdflatex_")]
        assert len(commands) == 3
        for command in commands:
            argv = command["argv"].split() if isinstance(command["argv"], str) else command["argv"]
            assert "-recorder" in argv
        summary = chapter[f"{phase_name}_fls_dependencies"]
        inventory_path = bound(summary["artifact"])
        inventory = load(inventory_path)
        assert inventory["candidate_id"] == CANDIDATE_ID
        assert inventory["phase"] == phase_name and inventory["stem"] == STEM
        assert inventory["recorder_enabled"] is True
        assert inventory["all_inputs_exist_and_hashed"] is True
        assert inventory["outputs_confined_to_worktree"] is True
        assert inventory["input_count"] == summary["input_count"] == len(inventory["inputs"]) > 0
        assert inventory["output_count"] == summary["output_count"] == len(inventory["outputs"]) > 0
        replay_row = phases[phase_name]
        assert replay_row["byte_identical"] is True
        assert replay_row["fls_input_closure_byte_identical"] is True
        assert replay_row["fls_input_closure_sha256"] == inventory["input_closure_sha256"]
        assert replay_row["second_fls_inventory_sha256"] == sha(inventory_path)
        private_prefix = f"{STEM}.{phase_name}"
        for build_index, private_root in enumerate(PRIVATE_BUILD_ROOTS):
            private_fls = private_root / f"{private_prefix}.fls"
            private_inventory = private_root / f"{private_prefix}.fls-dependencies.json"
            doc = load(private_inventory)
            assert private_fls.stat().st_size == doc["raw_fls_bytes"]
            assert sha(private_fls) == doc["raw_fls_sha256"]
            assert doc["input_closure_sha256"] == inventory["input_closure_sha256"]
            expected = replay_row[
                "first_fls_inventory_sha256" if build_index == 0 else "second_fls_inventory_sha256"
            ]
            assert sha(private_inventory) == expected
        fls_results[phase_name] = {
            "artifact": ev(inventory_path),
            "input_count": inventory["input_count"],
            "output_count": inventory["output_count"],
            "input_closure_sha256": inventory["input_closure_sha256"],
            "private_fresh_builds_rehashed": 2,
        }

    pdf = ROOT / chapter["candidate_pdf"]["path"]
    reader = PdfReader(pdf)
    assert len(reader.pages) == PAGE_COUNT
    assert chapter["candidate_log_summary"]["pages"] == PAGE_COUNT
    assert chapter["authority_log_summary"]["pages"] == PAGE_COUNT
    assert chapter["candidate_log_summary"]["overfull_hboxes"] == 2
    assert chapter["authority_log_summary"]["overfull_hboxes"] == 2
    links = 0
    bad_rectangles = []
    for number, page in enumerate(reader.pages, 1):
        box = [float(value) for value in page.mediabox]
        for annotation in page.get("/Annots", []):
            obj = annotation.get_object()
            if obj.get("/Subtype") != "/Link":
                continue
            links += 1
            rect = obj.get("/Rect")
            if not rect or len(rect) != 4:
                bad_rectangles.append(number)
                continue
            x0, y0, x1, y1 = map(float, rect)
            if (
                x0 > x1 or y0 > y1 or x0 < box[0] - 0.01 or y0 < box[1] - 0.01
                or x1 > box[2] + 0.01 or y1 > box[3] + 0.01
            ):
                bad_rectangles.append(number)
    assert not bad_rectangles, bad_rectangles
    return {
        "receipt": receipt,
        "chapter": chapter,
        "pdf": pdf,
        "links": links,
        "tagged": "/StructTreeRoot" in reader.trailer["/Root"],
        "fls": fls_results,
    }


def validate_render() -> dict:
    public_path = ROOT / "replay/RENDER_MANIFEST.json"
    visual_path = ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"
    stage_path = ROOT / "builds/BUILD_RENDER_STAGE.json"
    public = load(public_path)
    visual = load(visual_path)
    stage = load(stage_path)
    assert public["candidate_id"] == visual["candidate_id"] == stage["candidate_id"] == CANDIDATE_ID
    assert visual["passed"] is True and visual["blocking_findings"] == []
    assert visual["scope"]["covered_pages"] == list(range(1, PAGE_COUNT + 1))
    assert visual["scope"]["unreviewed_pages"] == []
    assert stage["status"] == "BUILD_DETERMINISTIC_RENDER_VISUAL_PASS"
    bound(visual["render_manifest"])
    for row in stage.values():
        if isinstance(row, dict) and {"path", "sha256"}.issubset(row):
            bound(row)
    assert public["pdf"]["sha256"] == sha(ROOT / "builds/groupoids.pdf")
    assert [row["page"] for row in public["pages"]] == list(range(1, PAGE_COUNT + 1))
    assert [row["page"] for row in public["high_resolution"]["renders"]] == visual["scope"]["high_resolution_pages"]
    assert len(public["contact_sheets"]) == 4
    private = load(PRIVATE_RENDER / "render-manifest.json")
    assert private["pdfs"][STEM]["pdf_sha256"] == public["pdf"]["sha256"]
    private_rows = [(PRIVATE_RENDER / STEM / row["file"], row) for row in private["pdfs"][STEM]["renders"]]
    private_rows += [(PRIVATE_RENDER / "contact_sheets" / row["file"], row) for row in private["contact_sheets"]]
    private_rows += [(PRIVATE_RENDER / "highres" / row["file"], row) for row in private["high_resolution"]["renders"]]
    for path, row in private_rows:
        assert path.is_file() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"]
    return {"public": public, "visual": visual, "private_artifacts_rehashed": len(private_rows)}


def mechanical() -> dict:
    source = validate_source_stage()
    build = validate_build()
    render = validate_render()
    page_map = load(ROOT / "builds/source-page-map.json")
    assert page_map["candidate_id"] == CANDIDATE_ID and page_map["stem"] == STEM
    assert page_map["operation_spec"]["operation_count"] == OPERATION_COUNT
    assert len(page_map["operations"]) == OPERATION_COUNT
    assert page_map["operation_spec"]["sha256"] == sha(ROOT / "operation-spec.json")
    assert page_map["auxiliary_build"]["candidate_pdf_sha256"] == sha(build["pdf"])
    report = {
        "schema": "stacks-r46-final-mechanical-validation/v1",
        "candidate_id": CANDIDATE_ID,
        "passed": True,
        "source_independent_validation": ev(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"),
        "source_regeneration": ev(ROOT / "REGENERATION_RECEIPT.json"),
        "build_receipt": ev(ROOT / "builds/build-receipt.json"),
        "build_execution": ev(ROOT / "builds/build-execution.json"),
        "deterministic_replay": ev(ROOT / "builds/deterministic-replay.json"),
        "tex_mutex_success": ev(ROOT / "builds/TEX_MUTEX_RECEIPT.json"),
        "tex_mutex_adverse_attempt": ev(ROOT / "builds/TEX_MUTEX_RECEIPT_ATTEMPT_001.json"),
        "recorder_fls": build["fls"],
        "candidate_pdf": ev(build["pdf"]),
        "pdf_pages": PAGE_COUNT,
        "pdf_links": build["links"],
        "bad_link_rectangles": [],
        "tagged_pdf": build["tagged"],
        "source_page_map": ev(ROOT / "builds/source-page-map.json"),
        "source_operations_mapped": OPERATION_COUNT,
        "render_manifest": ev(ROOT / "replay/RENDER_MANIFEST.json"),
        "render_artifacts_rehashed": render["private_artifacts_rehashed"],
        "visual_receipt": ev(ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"),
        "visual_conclusion_recomputed": False,
        "stable_ids": source["stable_ids"],
        "adverse_evidence": [
            "Attempt 001 failed only because the build recipe file had not yet been materialized; the attempt receipt is retained and a complete two-build rerun passed.",
            "The candidate and authority each retain two inherited overfull hboxes; page-complete visual review found no blocking defect.",
            "The isolated chapter retains cross-chapter unresolved references with an identical target multiset in candidate and authority.",
            "The PDF is untagged.",
        ],
        "generated_source_composed": False,
        "registry_admission": "NOT_PERFORMED",
    }
    destination = ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json"
    dump(destination, report)
    return report


def prepare() -> dict:
    mechanical_report = load(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json")
    assert mechanical_report["passed"] is True
    validate_source_stage()
    validate_render()
    destination = ROOT / "replay/FINAL_STAGE.json"
    if destination.exists():
        raise FileExistsError("FINAL_STAGE.json is immutable; use an append-only successor.")
    excluded = {
        "candidate.manifest.json",
        "replay/FINAL_STAGE.json",
        "replay/FINAL_INDEPENDENT_REVIEW.json",
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
        "schema": "stacks-r46-final-stage-snapshot/v1",
        "candidate_id": CANDIDATE_ID,
        "status": "READY_FOR_FULL_INDEPENDENT_REVIEW_NOT_ADMITTED",
        "snapshot_inventory": inventory,
        "mechanical_validation": ev(ROOT / "builds/FINAL_MECHANICAL_VALIDATION.json"),
        "visual_adjudication": ev(ROOT / "replay/PAGE_COMPLETE_VISUAL_ADJUDICATION.json"),
        "source_validation": ev(ROOT / "replay/SOURCE_INDEPENDENT_VALIDATION.json"),
        "independent_final_replay": "NOT_PERFORMED",
        "generated_source_composed": False,
        "registry_admission": "NOT_PERFORMED",
        "closure_order": "Independent review binds this snapshot; candidate.manifest.json is sealed last.",
    }
    dump(destination, report)
    return report


def seal() -> dict:
    snapshot_path = ROOT / "replay/FINAL_STAGE.json"
    snapshot = load(snapshot_path)
    for row in snapshot["snapshot_inventory"]:
        bound(row)
    review_path = ROOT / "replay/FINAL_INDEPENDENT_REVIEW.json"
    review = load(review_path)
    assert review["passed"] is True and review["candidate_id"] == CANDIDATE_ID
    assert review["final_stage_sha256"] == sha(snapshot_path)

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
        "candidate_id": CANDIDATE_ID,
        "lease_id": config["lease_id"],
        "namespace": config["namespace"],
        "writer_task": config["writer_task"],
        "upstream": {
            "lock": "upstream/stacks.lock.json",
            "commit": config["authority_commit"],
            "tree": config["authority_tree"],
        },
        "source_authorities": [ev(path) for path in authorities],
        "source_closure": {
            "enumerated": True,
            "expected_units": UNIT_COUNT,
            "manifested_units": UNIT_COUNT,
            "complete": True,
        },
        **{key: ev(ROOT / relative) for key, relative in primary.items()},
        "builds": [ev(path) for path in others],
        "rights_state": "Upstream GNU FDL rights are preserved in authority/COPYING; this independently prepared AI correction overlay is not an official Stacks Project edition or endorsement.",
        "review_state": "performed",
        "independent_replay": "passed",
        "unresolved_defects": [
            "Standalone cross-chapter reference warnings remain; candidate and authority target multisets match and cumulative AUX is not supplied.",
            "Two inherited overfull hboxes remain in both candidate and authority, with no blocking visual defect.",
            "Accessibility tagging is not asserted.",
        ],
        "stop_conditions": [
            "A changed referenced byte invalidates this manifest. Registry admission and generated-source composition remain separate."
        ],
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    schema = load(REPO / "schemas/candidate-manifest.schema.json")
    Draft202012Validator(schema).validate(manifest)
    destination = ROOT / "candidate.manifest.json"
    if destination.exists():
        raise FileExistsError("candidate.manifest.json is immutable; use a successor round.")
    dump(destination, manifest)
    return {"manifest": ev(destination), "manifested_files": len(authorities) + len(primary) + len(others)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["mechanical", "prepare", "seal"])
    args = parser.parse_args()
    result = {"mechanical": mechanical, "prepare": prepare, "seal": seal}[args.stage]()
    print(json.dumps({
        "stage": args.stage,
        "passed": True,
        "result": result.get("status", result.get("manifest", result.get("candidate_id"))),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
