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
    assert receipt["schema"] == "stacks-r41-tex-mutex-execution/v1"
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


def validate() -> dict:
    execution_path = BUILDS / "build-execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    replay = json.loads((BUILDS / "deterministic-replay.json").read_text(encoding="utf-8"))
    if not execution["passed"] or execution["authority_commit"] != CONFIG["authority_commit"]:
        raise AssertionError("build execution authority or pass state mismatch")
    assert replay["passed"] is True and replay["candidate_id"] == CONFIG["candidate_id"]
    receipt = {
        "schema": "mathematics-commons-stacks-errata-build-receipt/v1",
        "candidate_id": CONFIG["candidate_id"],
        "authority_commit": CONFIG["authority_commit"],
        "generated_at_utc": execution["completed_at_utc"],
        "command": "pdflatex; bibtex; pdflatex twice, sequentially per source and phase; two fresh full executions",
        "build_scope": f"{len(CONFIG['stems'])} directly modified chapter source in a fresh isolated copy of the pinned upstream tree",
        "recipe": artifact(ROOT / "BUILD.md"),
        "runner": artifact(ROOT / "replay-build.py"),
        "execution": artifact(execution_path),
        "deterministic_replay": artifact(BUILDS / "deterministic-replay.json"),
        "expected_limitation": "Standalone chapter builds may retain unresolved cross-chapter references because the cumulative AUX set is intentionally absent.",
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
        candidate_exec = execution["candidate_phase"]["stems"][stem]
        authority_exec = execution["authority_phase"]["stems"][stem]
        binding = (
            candidate_exec["source"]["sha256"] == candidate_source["sha256"]
            and candidate_exec["outputs"]["pdf"]["sha256"] == sha256(candidate_pdf)
            and candidate_exec["outputs"]["log"]["sha256"] == sha256(candidate_log)
            and authority_exec["source"]["sha256"] == authority_source["sha256"]
            and authority_exec["outputs"]["pdf"]["sha256"] == sha256(authority_pdf)
            and authority_exec["outputs"]["log"]["sha256"] == sha256(authority_log)
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
