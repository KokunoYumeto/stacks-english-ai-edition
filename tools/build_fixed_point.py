#!/usr/bin/env python3
"""Build selected Stacks chapters sequentially to a global PDF fixed point."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STEMS = (
    "sets",
    "categories",
    "topology",
    "sheaves",
    "sites",
    "algebra",
    "brauer",
    "homology",
    "more-algebra",
    "smoothing",
    "schemes",
    "properties",
    "morphisms",
    "more-morphisms",
    "crystalline",
    "spaces-cohomology",
    "stacks-limits",
    "injectives",
    "gaga",
    "moduli",
)

GENERATED_SUFFIXES = (
    ".aux",
    ".bbl",
    ".blg",
    ".log",
    ".out",
    ".pdf",
    ".toc",
    ".synctex.gz",
)


def run(command: list[str], source: Path, env: dict[str, str]) -> str:
    completed = subprocess.run(
        command,
        cwd=source,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        tail = "\n".join(completed.stdout.splitlines()[-80:])
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n{tail}"
        )
    return completed.stdout


def git(source: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip())
    return completed.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def version_line(executable: str, env: dict[str, str], source: Path) -> str:
    output = run([executable, "--version"], source, env)
    return output.splitlines()[0].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-date-epoch", default="1785270512")
    parser.add_argument("--max-sweeps", type=int, default=6)
    parser.add_argument("stems", nargs="*", default=list(DEFAULT_STEMS))
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output
    if not output.is_absolute():
        output = source / output
    output = output.resolve()
    stems = tuple(args.stems)
    if not stems:
        parser.error("at least one chapter stem is required")
    if args.max_sweeps < 2:
        parser.error("--max-sweeps must be at least 2")

    for executable in ("pdflatex", "bibtex", "pdfinfo"):
        if shutil.which(executable) is None:
            raise RuntimeError(f"required executable is unavailable: {executable}")
    for stem in stems:
        if not (source / f"{stem}.tex").is_file():
            raise RuntimeError(f"missing chapter source: {stem}.tex")

    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = args.source_date_epoch
    env["FORCE_SOURCE_DATE"] = "1"
    env["TZ"] = "UTC"

    for stem in stems:
        for suffix in GENERATED_SUFFIXES:
            artifact = source / f"{stem}{suffix}"
            if artifact.is_file():
                artifact.unlink()

    latex = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
    ]
    for stem in stems:
        print(f"prime {stem}", flush=True)
        run([*latex, f"{stem}.tex"], source, env)
    for stem in stems:
        print(f"bibtex {stem}", flush=True)
        run(["bibtex", stem], source, env)

    previous: tuple[str, ...] | None = None
    fixed_sweep: int | None = None
    for sweep in range(1, args.max_sweeps + 1):
        print(f"global sweep {sweep}", flush=True)
        for stem in stems:
            run([*latex, f"{stem}.tex"], source, env)
        current = tuple(sha256(source / f"{stem}.pdf") for stem in stems)
        if current == previous:
            fixed_sweep = sweep
            break
        previous = current
    if fixed_sweep is None:
        raise RuntimeError(
            f"PDF vector did not reach a fixed point in {args.max_sweeps} sweeps"
        )

    artifacts: list[dict[str, object]] = []
    pages_pattern = re.compile(r"^Pages:\s+(\d+)\s*$", re.MULTILINE)
    for stem in stems:
        pdf = source / f"{stem}.pdf"
        info = run(["pdfinfo", str(pdf)], source, env)
        match = pages_pattern.search(info)
        if not match or int(match.group(1)) < 1:
            raise RuntimeError(f"pdfinfo did not report a positive page count: {pdf}")
        artifacts.append(
            {
                "stem": stem,
                "pages": int(match.group(1)),
                "bytes": pdf.stat().st_size,
                "sha256": sha256(pdf),
            }
        )

    receipt = {
        "schema": "unofficial-ai-integrated-stacks-fixed-point-build/v1",
        "status": "PASS",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "source": {
            "commit": git(source, "rev-parse", "HEAD"),
            "tree": git(source, "rev-parse", "HEAD^{tree}"),
        },
        "environment": {
            "operating_system": platform.platform(),
            "python": platform.python_version(),
            "pdftex": version_line("pdflatex", env, source),
            "bibtex": version_line("bibtex", env, source),
            "pdfinfo": version_line("pdfinfo", env, source),
            "source_date_epoch": args.source_date_epoch,
        },
        "build": {
            "strategy": "sequential-prime-bibtex-global-sweeps",
            "chapter_count": len(stems),
            "global_fixed_point_sweep": fixed_sweep,
            "pdfinfo_readable": len(artifacts),
        },
        "artifacts": artifacts,
        "pdfs_committed": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(stems)} PDFs reached a fixed point on sweep {fixed_sweep}")
    print(f"receipt: {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
