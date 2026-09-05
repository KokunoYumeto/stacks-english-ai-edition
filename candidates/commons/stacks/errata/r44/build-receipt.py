from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def artifact(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}


def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    flat = re.sub(r"\s+", " ", text)
    references: collections.Counter[str] = collections.Counter()
    citations: collections.Counter[str] = collections.Counter()
    for fragment in text.split("LaTeX Warning:")[1:]:
        block = fragment.split("\n\n", 1)[0]
        compact = re.sub(r"\s+", "", block)
        reference = re.search(r"(?:Hyperreference|Reference)`([^']+)'onpage\d+undefinedoninputline\d+\.", compact)
        citation = re.search(r"Citation`([^']+)'onpage\d+undefinedoninputline\d+\.", compact)
        if reference:
            references[reference.group(1)] += 1
        if citation:
            citations[citation.group(1)] += 1
    output = re.search(r"Output written on .*?\((\d+) pages?, (\d+) bytes\)\.", flat)
    if not output:
        raise AssertionError(f"successful PDF record absent in {path}")
    return {
        "pages": int(output.group(1)),
        "reported_pdf_bytes": int(output.group(2)),
        "undefined_reference_targets": dict(sorted(references.items())),
        "undefined_citation_targets": dict(sorted(citations.items())),
        "overfull_hboxes": len(re.findall(r"Overfull \\hbox", text)),
        "underfull_hboxes": len(re.findall(r"Underfull \\hbox", text)),
        "overfull_vboxes": len(re.findall(r"Overfull \\vbox", text)),
        "underfull_vboxes": len(re.findall(r"Underfull \\vbox", text)),
        "fatal_markers": len(
            re.findall(
                r"(?m)^! (?:Emergency stop\.|Undefined control sequence\.|LaTeX Error:|Package [^\r\n]+ Error:)|"
                r"^!  ==> Fatal error occurred|^Emergency stop\.|Fatal error occurred",
                text,
            )
        ),
        "missing_glyph_markers": len(re.findall(r"Missing character:", text)),
    }


def validate_mutex() -> dict:
    path = BUILDS / "TEX_MUTEX_RECEIPT.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["schema"] == "stacks-r44-tex-mutex-execution/v1"
    assert receipt["candidate_id"] == CONFIG["candidate_id"]
    assert receipt["mutex_name"] == r"Global\InterlanguageTeXSlotV1"
    assert receipt["wait_timeout_seconds"] == 600
    assert receipt["acquired"] is True and receipt["released"] is True and receipt["passed"] is True
    assert isinstance(receipt["abandoned_mutex_recovered"], bool)
    assert [row["role"] for row in receipt["guarded_commands"]] == [
        "fresh_candidate_authority_build_1",
        "fresh_candidate_authority_build_2",
        "deterministic_pdf_comparison",
        "immediate_log_and_build_preflight",
    ]
    assert all(row["exit_code"] == 0 for row in receipt["guarded_commands"])
    return artifact(path)


def validate_fls(path: Path, stem: str, phase: str, expected_source_sha256: str) -> dict:
    inventory = json.loads(path.read_text(encoding="utf-8"))
    assert inventory["schema"] == "mathematics-commons-stacks-fls-dependency-inventory/v1"
    assert inventory["candidate_id"] == CONFIG["candidate_id"]
    assert inventory["stem"] == stem and inventory["phase"] == phase
    assert inventory["recorder_enabled"] is True
    assert inventory["all_inputs_exist_and_hashed"] is True
    assert inventory["outputs_confined_to_worktree"] is True
    assert inventory["input_count"] == len(inventory["inputs"]) > 0
    assert inventory["output_count"] == len(inventory["outputs"]) > 0
    primary = [row for row in inventory["inputs"] if row["logical_path"] == f"worktree/{stem}.tex"]
    assert len(primary) == 1 and primary[0]["sha256"] == expected_source_sha256
    assert all(row["exists"] and row["bytes"] >= 0 and len(row["sha256"]) == 64 for row in inventory["inputs"])
    return {
        "artifact": artifact(path),
        "input_count": inventory["input_count"],
        "output_count": inventory["output_count"],
        "input_closure_sha256": inventory["input_closure_sha256"],
        "primary_source_sha256": primary[0]["sha256"],
        "all_inputs_exist_and_hashed": True,
        "outputs_confined_to_worktree": True,
    }


def validate() -> dict:
    execution_path = BUILDS / "build-execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    replay = json.loads((BUILDS / "deterministic-replay.json").read_text(encoding="utf-8"))
    if (
        not execution["passed"]
        or execution["candidate_id"] != CONFIG["candidate_id"]
        or execution["authority_commit"] != CONFIG["authority_commit"]
        or execution["authority_tree"] != CONFIG["authority_tree"]
    ):
        raise AssertionError("build execution authority or pass state mismatch")
    assert replay["passed"] is True and replay["candidate_id"] == CONFIG["candidate_id"]
    receipt = {
        "schema": "mathematics-commons-stacks-errata-build-receipt/v1",
        "candidate_id": CONFIG["candidate_id"],
        "authority_commit": CONFIG["authority_commit"],
        "generated_at_utc": execution["completed_at_utc"],
        "command": "pdflatex -recorder; bibtex; pdflatex -recorder twice, sequentially per source and phase; two fresh full executions",
        "build_scope": f"{len(CONFIG['stems'])} directly modified chapter source in a fresh isolated copy of the pinned upstream tree",
        "recipe": artifact(ROOT / "BUILD.md"),
        "runner": artifact(ROOT / "replay-build.py"),
        "execution": artifact(execution_path),
        "deterministic_replay": artifact(BUILDS / "deterministic-replay.json"),
        "expected_limitation": "Standalone chapter builds may retain unresolved cross-chapter references because the cumulative AUX set is intentionally absent; recorder/FLS closure is fully claimed for both fresh executions.",
        "passed": True,
        "chapters": [],
    }
    for stem, expected in CONFIG["stems"].items():
        candidate_source = artifact(ROOT / "payload" / f"{stem}.tex")
        authority_source = artifact(ROOT / "authority/source" / f"{stem}.tex")
        assert candidate_source["sha256"] == expected["payload_sha256"]
        assert authority_source["sha256"] == expected["authority_sha256"]
        candidate_log = BUILDS / f"{stem}.log"
        authority_log = BUILDS / f"{stem}.authority.log"
        candidate_pdf = BUILDS / f"{stem}.pdf"
        authority_pdf = BUILDS / f"{stem}.authority.pdf"
        candidate_summary = parse_log(candidate_log)
        authority_summary = parse_log(authority_log)
        candidate_fls = validate_fls(BUILDS / f"{stem}.fls-dependencies.json", stem, "candidate", candidate_source["sha256"])
        authority_fls = validate_fls(BUILDS / f"{stem}.authority.fls-dependencies.json", stem, "authority", authority_source["sha256"])
        candidate_exec = execution["candidate_phase"]["stems"][stem]
        authority_exec = execution["authority_phase"]["stems"][stem]
        binding = (
            candidate_exec["source"]["sha256"] == candidate_source["sha256"]
            and candidate_exec["outputs"]["pdf"]["sha256"] == sha256(candidate_pdf)
            and candidate_exec["outputs"]["log"]["sha256"] == sha256(candidate_log)
            and candidate_exec["outputs"]["fls"]["sha256"] == sha256(BUILDS / f"{stem}.fls")
            and candidate_exec["outputs"]["fls_dependencies"]["sha256"] == candidate_fls["artifact"]["sha256"]
            and authority_exec["source"]["sha256"] == authority_source["sha256"]
            and authority_exec["outputs"]["pdf"]["sha256"] == sha256(authority_pdf)
            and authority_exec["outputs"]["log"]["sha256"] == sha256(authority_log)
            and authority_exec["outputs"]["fls"]["sha256"] == sha256(BUILDS / f"{stem}.authority.fls")
            and authority_exec["outputs"]["fls_dependencies"]["sha256"] == authority_fls["artifact"]["sha256"]
        )
        build_exceptions = expected.get("build_exceptions", {})
        candidate_only_refs = build_exceptions.get("candidate_only_undefined_reference_targets", {})
        expected_candidate_refs = collections.Counter(authority_summary["undefined_reference_targets"])
        expected_candidate_refs.update(candidate_only_refs)
        warnings_match = (
            collections.Counter(candidate_summary["undefined_reference_targets"]) == expected_candidate_refs
            and candidate_summary["undefined_citation_targets"] == authority_summary["undefined_citation_targets"]
        )
        page_delta_matches = candidate_summary["pages"] - authority_summary["pages"] == build_exceptions.get("candidate_page_delta", 0)
        passed = (
            candidate_summary["fatal_markers"] == 0
            and authority_summary["fatal_markers"] == 0
            and candidate_summary["missing_glyph_markers"] == 0
            and authority_summary["missing_glyph_markers"] == 0
            and warnings_match
            and page_delta_matches
            and binding
            and candidate_summary["reported_pdf_bytes"] == candidate_pdf.stat().st_size
            and authority_summary["reported_pdf_bytes"] == authority_pdf.stat().st_size
        )
        receipt["passed"] = receipt["passed"] and passed
        receipt["chapters"].append(
            {
                "stem": stem,
                "passed": passed,
                "candidate_source": candidate_source,
                "authority_source": authority_source,
                "candidate_pdf": artifact(candidate_pdf),
                "candidate_log": artifact(candidate_log),
                "authority_pdf": artifact(authority_pdf),
                "authority_log": artifact(authority_log),
                "candidate_fls": artifact(BUILDS / f"{stem}.fls"),
                "candidate_fls_dependencies": candidate_fls,
                "authority_fls": artifact(BUILDS / f"{stem}.authority.fls"),
                "authority_fls_dependencies": authority_fls,
                "candidate_stdout": artifact(BUILDS / f"{stem}.pass3.txt"),
                "candidate_bibtex": artifact(BUILDS / f"{stem}.bibtex.txt"),
                "authority_stdout": artifact(BUILDS / f"{stem}.authority.pass3.txt"),
                "authority_bibtex": artifact(BUILDS / f"{stem}.authority.bibtex.txt"),
                "candidate_log_summary": candidate_summary,
                "authority_log_summary": authority_summary,
                "execution_binding_matches": binding,
                "undefined_target_multisets_match_authority": warnings_match,
                "configured_build_exceptions": build_exceptions,
                "candidate_page_delta_matches": page_delta_matches,
            }
        )
    assert receipt["passed"] is True
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    receipt = validate()
    if args.preflight:
        print(json.dumps({"passed": True, "preflight": True, "chapters": len(receipt["chapters"])}))
        return 0
    receipt["tex_mutex"] = validate_mutex()
    path = BUILDS / "build-receipt.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "receipt": str(path), "sha256": sha256(path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
