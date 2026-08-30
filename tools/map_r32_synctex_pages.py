#!/usr/bin/env python3
"""Map manifest-bound R31/R32 operations to final cumulative PDF pages."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "3f0fa66780213432079c6c3044a6a515508b2576"
SOURCE = "bb81deaa0f922caa8b4b4c1e85d928a03c955b24"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_blob(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{revision}:{path}"], cwd=ROOT,
        check=True, stdout=subprocess.PIPE,
    ).stdout


def load_composer():
    path = ROOT / "tools/compose_overlay_projection.py"
    spec = importlib.util.spec_from_file_location("overlay_composer", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def synctex_pages(root: Path, source: str, line: int) -> list[int]:
    source_path = (root / source).resolve()
    pdf = root / f"{Path(source).stem}.pdf"
    completed = subprocess.run(
        ["synctex", "view", "-i", f"{line}:0:{source_path}", "-o", str(pdf)],
        cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    pages = sorted({int(value) for value in re.findall(r"^Page:(\d+)$", completed.stdout, re.MULTILINE)})
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
    composer = load_composer()
    inventory: dict[str, list[dict]] = {}

    for round_number in (31, 32):
        directory = ROOT / f"ai-integrated/candidates/commons/stacks/errata/r{round_number}"
        spec = json.loads((directory / "operation-spec.json").read_text("utf-8"))
        operations = spec["operations"]
        per_source: dict[str, list[dict]] = {}
        for operation in operations:
            source = operation.get("source", "sites-modules.tex")
            per_source.setdefault(source, []).append(operation)
        for source, rows in per_source.items():
            authority = (directory / "authority/source" / source).read_bytes()
            base = git_blob(BASE, source)
            final = git_blob(SOURCE, source)
            rebased = composer.rebase_operations(authority, base, rows)
            deltas = {
                row["operation_id"]: len(row["replacement_text"].encode("utf-8"))
                - len(row["old_text"].encode("utf-8"))
                for row in rebased
            }
            mapped_rows: list[dict] = []
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
                pages = synctex_pages(synctex_root, source, final_line)
                mapped_rows.append({
                    "round": round_number,
                    "operation_id": row["operation_id"],
                    "stable_id": row["stable_id"],
                    "source": source,
                    "authority_start_byte": row["authority_start_byte"],
                    "mapped_base_start_byte": row["start_byte"],
                    "final_start_byte": final_start,
                    "authority_start_line": row["source_start_line"],
                    "final_cumulative_line": final_line,
                    "pages": pages,
                })
            inventory[source] = mapped_rows

    result = {
        "schema": "unofficial-ai-integrated-stacks-operation-page-map/v1",
        "status": "PASS",
        "composition_base": BASE,
        "composition_source": SOURCE,
        "operation_count": sum(len(rows) for rows in inventory.values()),
        "mapping_failures": 0,
        "sources": {
            source: {
                "operation_count": len(rows),
                "unique_pages": sorted({page for row in rows for page in row["pages"]}),
                "operations": rows,
            }
            for source, rows in sorted(inventory.items())
        },
    }
    if result["operation_count"] != 126:
        raise RuntimeError("R31/R32 operation count mismatch")
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", "utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS", "operations": result["operation_count"],
        "pages": {source: data["unique_pages"] for source, data in result["sources"].items()},
        "bytes": output.stat().st_size, "sha256": sha256(output.read_bytes()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
