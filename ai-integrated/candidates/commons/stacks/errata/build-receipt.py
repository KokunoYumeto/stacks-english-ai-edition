from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
STEMS = ("smoothing", "crystalline", "spaces-cohomology")
EXPECTED_PAYLOAD_HASHES = {
    "smoothing": "9CF7DCF31E447C585E81515C9A8059B37A566998DCAFA77A16AB7CB1D27A0A46",
    "crystalline": "EDA38E502E0C6B3743C0FCD769203EAA6186440002A9AD2C97DC6F642B03DEC7",
    "spaces-cohomology": "81438F655CEAB1A2E07CFEEC645A9A7C2447DB983D6BCEFAED6575859B75D196",
}
EXPECTED_AUTHORITY_HASHES = {
    "smoothing": "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068",
    "crystalline": "466C0634A5E8E3899B157A42A4B4BB5F4357199F96708CAF5854F5A92BE58054",
    "spaces-cohomology": "63F19991B7B2BCE90B5FB30FCDBB8A3B06CBBFFEC42FA7C413776C29AE4B69C5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def artifact(path: Path) -> dict:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    flat = re.sub(r"\s+", " ", text)
    references = collections.Counter(
        re.findall(
            r"LaTeX Warning: (?:Hyper reference|Reference) `([^']+)' .*? undefined on input line \d+\.",
            flat,
        )
    )
    citations = collections.Counter(
        re.findall(
            r"LaTeX Warning: Citation `([^']+)' .*? undefined on input line \d+\.",
            flat,
        )
    )
    output = re.search(r"Output written on .*?\((\d+) pages?, (\d+) bytes\)\.", flat)
    if not output:
        raise AssertionError(f"No successful PDF output record in {path}")
    fatal = re.findall(r"(?m)^!|Emergency stop|Fatal error", text)
    return {
        "pages": int(output.group(1)),
        "reported_pdf_bytes": int(output.group(2)),
        "undefined_reference_targets": dict(sorted(references.items())),
        "undefined_citation_targets": dict(sorted(citations.items())),
        "overfull_boxes": len(re.findall(r"Overfull \\[hv]box", text)),
        "underfull_boxes": len(re.findall(r"Underfull \\[hv]box", text)),
        "fatal_markers": len(fatal),
    }


def main() -> int:
    execution_path = BUILDS / "build-execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    if not execution["passed"]:
        raise AssertionError("build execution receipt is not passed")
    if execution["authority_commit"] != "a04446e57ec1fbc252a871afcec7752fb2807b14":
        raise AssertionError("build execution authority commit mismatch")
    receipt = {
        "schema": "mathematics-commons-stacks-errata-build-receipt/v1",
        "candidate_id": "stacks-errata-a04446e-r1",
        "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
        "generated_at_utc": execution["completed_at_utc"],
        "command": "pdflatex -interaction=nonstopmode -halt-on-error -file-line-error STEM.tex; bibtex STEM; pdflatex twice",
        "build_scope": "three directly modified chapter sources; sequential isolated chapter builds",
        "build_workdir": "fresh isolated copy of the exact upstream tree outside the repository; local path redacted",
        "recipe": artifact(ROOT / "BUILD.md"),
        "runner": artifact(ROOT / "replay-build.py"),
        "execution": artifact(execution_path),
        "tag_payload": artifact(ROOT / "payload" / "tags" / "tags"),
        "tag_allocator_receipt": artifact(BUILDS / "tag-allocator.json"),
        "expected_limitation": "Standalone chapter builds retain unresolved cross-chapter references because the complete corpus AUX set is intentionally absent.",
        "passed": True,
        "chapters": [],
    }
    for stem in STEMS:
        source_path = ROOT / "payload" / f"{stem}.tex"
        source_artifact = artifact(source_path)
        if source_artifact["sha256"] != EXPECTED_PAYLOAD_HASHES[stem]:
            raise AssertionError(f"payload hash changed before build receipt: {stem}")
        candidate_log_path = BUILDS / f"{stem}.log"
        authority_log_path = BUILDS / f"{stem}.authority.log"
        pdf_path = BUILDS / f"{stem}.pdf"
        authority_pdf_path = BUILDS / f"{stem}.authority.pdf"
        candidate = parse_log(candidate_log_path)
        authority = parse_log(authority_log_path)
        candidate_execution = execution["candidate_phase"]["stems"][stem]
        authority_execution = execution["authority_phase"]["stems"][stem]
        execution_binding_matches = (
            candidate_execution["source"]["sha256"] == source_artifact["sha256"]
            and candidate_execution["outputs"]["pdf"]["sha256"] == sha256(pdf_path)
            and candidate_execution["outputs"]["log"]["sha256"] == sha256(candidate_log_path)
            and authority_execution["source"]["sha256"] == EXPECTED_AUTHORITY_HASHES[stem]
            and authority_execution["outputs"]["pdf"]["sha256"] == sha256(authority_pdf_path)
            and authority_execution["outputs"]["log"]["sha256"] == sha256(authority_log_path)
        )
        warnings_match = (
            candidate["undefined_reference_targets"] == authority["undefined_reference_targets"]
            and candidate["undefined_citation_targets"] == authority["undefined_citation_targets"]
        )
        chapter_passed = (
            candidate["fatal_markers"] == 0
            and authority["fatal_markers"] == 0
            and warnings_match
            and execution_binding_matches
            and candidate["reported_pdf_bytes"] == pdf_path.stat().st_size
            and authority["reported_pdf_bytes"] == authority_pdf_path.stat().st_size
        )
        receipt["passed"] = receipt["passed"] and chapter_passed
        receipt["chapters"].append(
            {
                "stem": stem,
                "passed": chapter_passed,
                "candidate_source": source_artifact,
                "candidate_pdf": artifact(pdf_path),
                "candidate_log": artifact(candidate_log_path),
                "authority_log": artifact(authority_log_path),
                "authority_pdf": artifact(authority_pdf_path),
                "candidate_stdout": artifact(BUILDS / f"{stem}.pass3.txt"),
                "candidate_bibtex": artifact(BUILDS / f"{stem}.bibtex.txt"),
                "authority_stdout": artifact(BUILDS / f"{stem}.authority.pass3.txt"),
                "authority_bibtex": artifact(BUILDS / f"{stem}.authority.bibtex.txt"),
                "candidate_log_summary": candidate,
                "authority_log_summary": authority,
                "execution_binding_matches": execution_binding_matches,
                "undefined_target_multisets_match_authority": warnings_match,
            }
        )
    path = BUILDS / "build-receipt.json"
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": receipt["passed"], "receipt": str(path)}, ensure_ascii=False))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
