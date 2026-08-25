from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUILDS = ROOT / "builds"
STEMS = ("sets", "topology", "categories")
EXPECTED_PAYLOAD_HASHES = {
    "sets": "A4D8072BDFFEEF9B8EF1D058499761DA1E1F31EABC11BB04B8EA37D04B866D41",
    "topology": "67115451F19CE981FD591F77E6CA16A4DE64A20C71105D2E5215E41FD8F8EB8D",
    "categories": "124F381C9DD01898B8DBB3969B7771190B64E8B2B9CE73E24E7DD1FB0727E2C1",
}
EXPECTED_AUTHORITY_HASHES = {
    "sets": "9BCC55E7F11CF36B0665AE549D5BA76BE6A0EDD00F7FCA36A567E367099603F9",
    "topology": "C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872",
    "categories": "62F7611AF4C3FEEBD041DB4728B42C7112004CFBB9FA5ECB643C6F5D90DB3F25",
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
    refs = collections.Counter(
        re.findall(
            r"LaTeX Warning: (?:Hyper reference|Reference) `([^']+)' .*? undefined on input line \d+\.",
            flat,
        )
    )
    cites = collections.Counter(
        re.findall(
            r"LaTeX Warning: Citation `([^']+)' .*? undefined on input line \d+\.",
            flat,
        )
    )
    output = re.search(r"Output written on .*?\((\d+) pages?, (\d+) bytes\)\.", flat)
    if not output:
        raise AssertionError(f"No successful PDF output record in {path}")
    return {
        "pages": int(output.group(1)),
        "reported_pdf_bytes": int(output.group(2)),
        "undefined_reference_targets": dict(sorted(refs.items())),
        "undefined_citation_targets": dict(sorted(cites.items())),
        "overfull_boxes": len(re.findall(r"Overfull \\[hv]box", text)),
        "underfull_boxes": len(re.findall(r"Underfull \\[hv]box", text)),
        "fatal_markers": len(re.findall(r"(?m)^!|Emergency stop|Fatal error", text)),
    }


def main() -> int:
    execution_path = BUILDS / "build-execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    if (
        not execution["passed"]
        or execution["authority_commit"]
        != "a04446e57ec1fbc252a871afcec7752fb2807b14"
    ):
        raise AssertionError("build execution authority or pass state mismatch")
    receipt = {
        "schema": "mathematics-commons-stacks-errata-build-receipt/v1",
        "candidate_id": "stacks-errata-a04446e-r3",
        "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
        "generated_at_utc": execution["completed_at_utc"],
        "command": "pdflatex; bibtex; pdflatex twice, sequentially per stem",
        "build_scope": "three directly modified chapter sources in a fresh isolated authority copy",
        "recipe": artifact(ROOT / "BUILD.md"),
        "runner": artifact(ROOT / "replay-build.py"),
        "execution": artifact(execution_path),
        "expected_limitation": (
            "Standalone builds retain unresolved cross-chapter references because "
            "the cumulative AUX set is intentionally absent."
        ),
        "passed": True,
        "chapters": [],
    }
    for stem in STEMS:
        source = ROOT / "payload" / f"{stem}.tex"
        source_artifact = artifact(source)
        authority_source = ROOT / "authority" / "source" / f"{stem}.tex"
        authority_source_artifact = artifact(authority_source)
        if source_artifact["sha256"] != EXPECTED_PAYLOAD_HASHES[stem]:
            raise AssertionError(f"payload hash mismatch: {stem}")
        if authority_source_artifact["sha256"] != EXPECTED_AUTHORITY_HASHES[stem]:
            raise AssertionError(f"authority source hash mismatch: {stem}")
        candidate_log_path = BUILDS / f"{stem}.log"
        authority_log_path = BUILDS / f"{stem}.authority.log"
        pdf_path = BUILDS / f"{stem}.pdf"
        authority_pdf_path = BUILDS / f"{stem}.authority.pdf"
        candidate = parse_log(candidate_log_path)
        authority = parse_log(authority_log_path)
        candidate_execution = execution["candidate_phase"]["stems"][stem]
        authority_execution = execution["authority_phase"]["stems"][stem]
        binding = (
            candidate_execution["source"]["sha256"] == source_artifact["sha256"]
            and candidate_execution["outputs"]["pdf"]["sha256"] == sha256(pdf_path)
            and candidate_execution["outputs"]["log"]["sha256"]
            == sha256(candidate_log_path)
            and authority_execution["source"]["sha256"]
            == EXPECTED_AUTHORITY_HASHES[stem]
            and authority_execution["outputs"]["pdf"]["sha256"]
            == sha256(authority_pdf_path)
            and authority_execution["outputs"]["log"]["sha256"]
            == sha256(authority_log_path)
        )
        warnings_match = (
            candidate["undefined_reference_targets"]
            == authority["undefined_reference_targets"]
            and candidate["undefined_citation_targets"]
            == authority["undefined_citation_targets"]
        )
        passed = (
            candidate["fatal_markers"] == 0
            and authority["fatal_markers"] == 0
            and warnings_match
            and binding
            and candidate["reported_pdf_bytes"] == pdf_path.stat().st_size
            and authority["reported_pdf_bytes"] == authority_pdf_path.stat().st_size
        )
        receipt["passed"] = receipt["passed"] and passed
        receipt["chapters"].append(
            {
                "stem": stem,
                "passed": passed,
                "candidate_source": source_artifact,
                "authority_source": authority_source_artifact,
                "candidate_pdf": artifact(pdf_path),
                "candidate_log": artifact(candidate_log_path),
                "authority_pdf": artifact(authority_pdf_path),
                "authority_log": artifact(authority_log_path),
                "candidate_stdout": artifact(BUILDS / f"{stem}.pass3.txt"),
                "candidate_bibtex": artifact(BUILDS / f"{stem}.bibtex.txt"),
                "authority_stdout": artifact(
                    BUILDS / f"{stem}.authority.pass3.txt"
                ),
                "authority_bibtex": artifact(
                    BUILDS / f"{stem}.authority.bibtex.txt"
                ),
                "candidate_log_summary": candidate,
                "authority_log_summary": authority,
                "execution_binding_matches": binding,
                "undefined_target_multisets_match_authority": warnings_match,
            }
        )
    path = BUILDS / "build-receipt.json"
    path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"passed": receipt["passed"], "receipt": str(path)}))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
