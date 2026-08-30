#!/usr/bin/env python3
"""Map the seven manifest-bound R33 operations to cumulative PDF pages."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
COMPOSITION_BASE = "b2ffa008fc27bfdb8b93c431f4df0c3e197d3440"
COMPOSITION_SOURCE = "9100eefe0819f9632c6129e6d6f19a4101d223d1"
SOURCE_PATH = "spaces-morphisms.tex"
CANDIDATE = ROOT / "ai-integrated/candidates/commons/stacks/errata/r33"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    return completed.stdout.strip()


def git_blob(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{revision}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def load_composer():
    path = ROOT / "tools/compose_overlay_projection.py"
    spec = importlib.util.spec_from_file_location("overlay_composer", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load overlay composer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synctex_pages(root: Path, source: str, line: int) -> list[int]:
    source_path = (root / source).resolve()
    pdf = root / f"{Path(source).stem}.pdf"
    completed = subprocess.run(
        ["synctex", "view", "-i", f"{line}:0:{source_path}", "-o", str(pdf)],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    pages = sorted(
        {int(value) for value in re.findall(r"^Page:(\d+)$", completed.stdout, re.MULTILINE)}
    )
    if completed.returncode or not pages:
        raise RuntimeError(
            f"SyncTeX did not map {source}:{line}: {completed.stdout[-500:]}"
        )
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synctex-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    synctex_root = args.synctex_root.resolve()
    authority = (CANDIDATE / "authority/source" / SOURCE_PATH).read_bytes()
    base = git_blob(COMPOSITION_BASE, SOURCE_PATH)
    final = git_blob(COMPOSITION_SOURCE, SOURCE_PATH)
    live = (synctex_root / SOURCE_PATH).read_bytes()
    if live != final:
        raise RuntimeError("live cumulative source differs from the R33 composition commit")

    spec = json.loads((CANDIDATE / "operation-spec.json").read_text(encoding="utf-8"))
    operations = spec["operations"]
    if spec.get("operation_count") != 7 or len(operations) != 7:
        raise RuntimeError("R33 operation closure mismatch")
    composer = load_composer()
    rebased = composer.rebase_operations(authority, base, operations)
    deltas = {
        row["operation_id"]: len(row["replacement_text"].encode("utf-8"))
        - len(row["old_text"].encode("utf-8"))
        for row in rebased
    }

    pdf = synctex_root / "spaces-morphisms.pdf"
    synctex = synctex_root / "spaces-morphisms.synctex.gz"
    if not pdf.is_file() or not synctex.is_file():
        raise RuntimeError("the deterministic PDF and SyncTeX sidecar are required")
    pdf_before = sha256(pdf.read_bytes())

    mapped_rows: list[dict[str, object]] = []
    for row in sorted(rebased, key=lambda item: item["start_byte"]):
        final_start = row["start_byte"] + sum(
            deltas[other["operation_id"]]
            for other in rebased
            if other["start_byte"] < row["start_byte"]
        )
        replacement = row["replacement_text"].encode("utf-8")
        if final[final_start : final_start + len(replacement)] != replacement:
            raise RuntimeError(f"final replacement mismatch: {row['operation_id']}")
        final_line = final.count(b"\n", 0, final_start) + 1
        pages = synctex_pages(synctex_root, SOURCE_PATH, final_line)
        mapped_rows.append(
            {
                "round": 33,
                "operation_id": row["operation_id"],
                "stable_id": row["stable_id"],
                "producer_ids": row.get("producer_ids", [row.get("producer_id")]),
                "authority_start_byte": row["authority_start_byte"],
                "final_start_byte": final_start,
                "authority_start_line": row["source_start_line"],
                "final_cumulative_line": final_line,
                "pages": pages,
            }
        )

    pdf_after = sha256(pdf.read_bytes())
    result = {
        "schema": "unofficial-ai-integrated-stacks-operation-page-map/v1",
        "status": "PASS",
        "created_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "authority": {"commit": AUTHORITY_COMMIT, "tree": AUTHORITY_TREE},
        "composition_base": COMPOSITION_BASE,
        "composition_source": COMPOSITION_SOURCE,
        "validation_head": git("rev-parse", "HEAD"),
        "operation_count": len(mapped_rows),
        "mapping_failures": 0,
        "mapping_protocol": {
            "method": "SyncTeX view against the deterministic cumulative spaces-morphisms.pdf",
            "source_lines_preserved": all(
                row["authority_start_line"] == row["final_cumulative_line"]
                for row in mapped_rows
            ),
            "source_line_delta": final.count(b"\n") - authority.count(b"\n"),
            "pdf_sha256_before_synctex_mapping": pdf_before,
            "pdf_sha256_after_synctex_mapping": pdf_after,
            "pdf_byte_identity_preserved": pdf_before == pdf_after,
        },
        "sources": {
            SOURCE_PATH: {
                "authority_bytes": len(authority),
                "authority_sha256": sha256(authority),
                "composed_bytes": len(final),
                "composed_sha256": sha256(final),
                "composed_git_blob": git("rev-parse", f"{COMPOSITION_SOURCE}:{SOURCE_PATH}"),
                "operation_count": len(mapped_rows),
                "unique_pages": sorted(
                    {page for row in mapped_rows for page in row["pages"]}
                ),
                "operations": mapped_rows,
            }
        },
    }
    if (
        result["operation_count"] != 7
        or result["mapping_protocol"]["pdf_byte_identity_preserved"] is not True
    ):
        raise RuntimeError("R33 mapping invariant failed")

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "operations": len(mapped_rows),
                "pages": result["sources"][SOURCE_PATH]["unique_pages"],
                "bytes": output.stat().st_size,
                "sha256": sha256(output.read_bytes()),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
