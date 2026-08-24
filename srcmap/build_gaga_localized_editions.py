#!/usr/bin/env python3
"""Build and deterministically validate the Japanese and Simplified-Chinese GAGA PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SOURCE_VALIDATOR = ROOT / "srcmap" / "validate_gaga_editions.py"
VALIDATION_DIR = ROOT / "output" / "validation"
RECEIPT = VALIDATION_DIR / "gaga-localized-build-validation.json"

EDITIONS = {
    "ja": {
        "source": ROOT / "output" / "source" / "gaga-ja.tex",
        "jobname": "gaga-ja",
        "pdf": ROOT / "output" / "pdf" / "gaga-japanese.pdf",
        "render_dir": ROOT / "tmp" / "pdfs" / "gaga_japanese_final",
        "font_markers": ("YuGothic", "Yu Gothic"),
        "script_re": re.compile(r"[\u3040-\u30ff]"),
    },
    "zh-cn": {
        "source": ROOT / "output" / "source" / "gaga-zh-cn.tex",
        "jobname": "gaga-zh-cn",
        "pdf": ROOT / "output" / "pdf" / "gaga-simplified-chinese.pdf",
        "render_dir": ROOT / "tmp" / "pdfs" / "gaga_chinese_final",
        "font_markers": ("SimSun", "宋体"),
        "script_re": re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]"),
    },
}

FATAL_LOG_PATTERNS = {
    "undefined_reference": re.compile(
        r"(?:LaTeX|Package\s+(?:hyperref|xr-hyper))\s+Warning:.*?"
        r"(?:Reference|Hyper reference|undefined references).*?undefined|"
        r"LaTeX Warning: There were undefined references",
        re.I,
    ),
    "undefined_citation": re.compile(
        r"(?:LaTeX|Package\s+natbib)\s+Warning:.*?Citation.*?undefined|"
        r"LaTeX Warning: There were undefined citations",
        re.I,
    ),
    "rerun_required": re.compile(
        r"Rerun to get cross-references right|Label\(s\) may have changed|"
        r"Package rerunfilecheck Warning:|Please \(re\)run (?:BibTeX|Biber)|"
        r"Please rerun (?:LaTeX|BibTeX|Biber)",
        re.I,
    ),
    "fatal_error": re.compile(r"Fatal error|Emergency stop", re.I),
    "overfull_box": re.compile(r"Overfull \\[hv]box", re.I),
    "underfull_box": re.compile(r"Underfull \\[hv]box", re.I),
    "missing_character": re.compile(r"Missing character:", re.I),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def identity(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def run(command: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        output = result.stdout or ""
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n{output[-4000:]}"
        )
    return (result.stdout or "") if capture else ""


def require_tools() -> None:
    missing = [
        tool
        for tool in ("xelatex", "bibtex", "pdfinfo", "pdffonts", "pdftotext", "pdftoppm")
        if shutil.which(tool) is None
    ]
    if missing:
        raise RuntimeError(f"Required tools are unavailable: {', '.join(missing)}")


def aux_snapshot(jobname: str) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for suffix in ("aux", "out", "toc"):
        path = ROOT / f"{jobname}.{suffix}"
        if not path.is_file():
            raise RuntimeError(f"Expected fixed-point file is missing: {path.name}")
        snapshot[suffix] = sha256(path)
    return snapshot


def final_log_findings(jobname: str) -> dict[str, int]:
    path = ROOT / f"{jobname}.log"
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = {name: len(pattern.findall(text)) for name, pattern in FATAL_LOG_PATTERNS.items()}
    blg = ROOT / f"{jobname}.blg"
    bibliography_log = blg.read_text(encoding="utf-8", errors="replace") if blg.is_file() else ""
    findings["bibtex_warning"] = len(re.findall(r"^Warning--", bibliography_log, re.I | re.M))
    findings["bibtex_error"] = len(
        re.findall(r"error message|I couldn't open|I found no \\bibdata", bibliography_log, re.I)
    )
    return findings


def pdf_pages(path: Path) -> int:
    output = run(["pdfinfo", str(path)], capture=True)
    match = re.search(r"^Pages:\s+(\d+)\s*$", output, re.M)
    if not match:
        raise RuntimeError(f"Could not read PDF page count: {path}")
    return int(match.group(1))


def clear_known_render_pages(render_dir: Path) -> None:
    render_dir.mkdir(parents=True, exist_ok=True)
    expected_parent = render_dir.resolve()
    for number in range(1, 1000):
        for width in (1, 2, 3):
            path = render_dir / f"page-{number:0{width}d}.png"
            if path.is_file():
                if path.resolve().parent != expected_parent:
                    raise RuntimeError(f"Render path escaped expected directory: {path}")
                path.unlink()


def render_pdf(pdf: Path, render_dir: Path, pages: int) -> list[dict[str, Any]]:
    clear_known_render_pages(render_dir)
    prefix = render_dir / "page"
    run(["pdftoppm", "-png", "-r", "144", "-f", "1", "-l", str(pages), str(pdf), str(prefix)])
    rendered = sorted(render_dir.iterdir(), key=lambda path: path.name)
    rendered = [path for path in rendered if path.is_file() and re.fullmatch(r"page-\d+\.png", path.name)]
    if len(rendered) != pages:
        raise RuntimeError(f"Rendered {len(rendered)} pages for a {pages}-page PDF: {pdf.name}")
    return [identity(path) for path in rendered]


def build_one(language: str) -> dict[str, Any]:
    config = EDITIONS[language]
    source: Path = config["source"]
    jobname: str = config["jobname"]
    canonical_pdf: Path = config["pdf"]
    render_dir: Path = config["render_dir"]
    if not source.is_file():
        raise RuntimeError(f"Localized source is missing: {source}")

    latex = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-jobname={jobname}",
        str(source.relative_to(ROOT)).replace("\\", "/"),
    ]
    run(latex)
    run(["bibtex", jobname])

    previous: dict[str, str] | None = None
    fixed_point: dict[str, str] | None = None
    passes_after_bibtex = 0
    for _ in range(6):
        run(latex)
        passes_after_bibtex += 1
        current = aux_snapshot(jobname)
        findings = final_log_findings(jobname)
        if previous == current and findings["rerun_required"] == 0:
            fixed_point = current
            break
        previous = current
    if fixed_point is None:
        raise RuntimeError(f"{language}: references did not reach a fixed point")

    findings = final_log_findings(jobname)
    active_findings = {name: count for name, count in findings.items() if count}
    if active_findings:
        raise RuntimeError(f"{language}: final LaTeX log findings: {active_findings}")

    built_pdf = ROOT / f"{jobname}.pdf"
    if not built_pdf.is_file():
        raise RuntimeError(f"Built PDF is missing: {built_pdf}")
    canonical_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(built_pdf, canonical_pdf)

    pages = pdf_pages(canonical_pdf)
    font_report = run(["pdffonts", str(canonical_pdf)], capture=True)
    if not any(marker.casefold() in font_report.casefold() for marker in config["font_markers"]):
        raise RuntimeError(f"{language}: expected CJK font is absent from PDF font inventory")

    render_dir.mkdir(parents=True, exist_ok=True)
    text_path = render_dir / "extracted.txt"
    run(["pdftotext", str(canonical_pdf), str(text_path)])
    extracted = text_path.read_text(encoding="utf-8", errors="replace")
    script_characters = len(config["script_re"].findall(extracted))
    if script_characters < 1000:
        raise RuntimeError(
            f"{language}: PDF text extraction contains too little localized script ({script_characters})"
        )

    rendered = render_pdf(canonical_pdf, render_dir, pages)
    return {
        "language": language,
        "status": "PASS",
        "source": identity(source),
        "pdf": identity(canonical_pdf),
        "pages": pages,
        "passes_after_bibtex": passes_after_bibtex,
        "fixed_point": fixed_point,
        "log_findings": findings,
        "localized_characters_in_extracted_pdf_text": script_characters,
        "font_inventory": font_report.splitlines(),
        "render_directory": str(render_dir.relative_to(ROOT)).replace("\\", "/"),
        "rendered_pages": rendered,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=("ja", "zh-cn", "all"), default="all")
    args = parser.parse_args()
    require_tools()

    selected = ("ja", "zh-cn") if args.language == "all" else (args.language,)
    validation = run(
        [sys.executable, "-B", str(SOURCE_VALIDATOR), "--language", args.language],
        capture=True,
    )
    source_validation = json.loads(validation)
    if source_validation.get("status") != "PASS":
        raise RuntimeError("Localized source validation did not pass")

    editions = [build_one(language) for language in selected]
    payload = {
        "schema": "gaga-localized-build-validation-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "source_validation": source_validation,
        "editions": editions,
        "visual_inspection": {
            "status": "PENDING",
            "requirement": "Inspect every rendered page and replace PENDING only after the final render set passes.",
        },
    }
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    receipt = (
        RECEIPT
        if args.language == "all"
        else VALIDATION_DIR / f"gaga-{args.language}-build-validation.json"
    )
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
