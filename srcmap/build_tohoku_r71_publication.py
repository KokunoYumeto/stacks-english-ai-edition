#!/usr/bin/env python3
"""Build the privacy-clean public projection of the r71 source-repair audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "D1029_SOURCE_REPAIR_CHECK.json"
OUTPUT = (
    ROOT
    / "output"
    / "publication"
    / "TOHOKU_R71_SOURCE_REPAIR_CHECK_PUBLIC.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def replace_home(value: Any, counters: dict[str, int]) -> Any:
    if isinstance(value, dict):
        return {key: replace_home(item, counters) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_home(item, counters) for item in value]
    if not isinstance(value, str):
        return value
    result = value
    variants = {
        str(Path.home()),
        str(Path.home()).replace("\\", "/"),
    }
    for variant in sorted(variants, key=len, reverse=True):
        result, count = re.subn(
            re.escape(variant),
            "[LOCAL_HOME]",
            result,
            flags=re.IGNORECASE,
        )
        counters["replacements"] += count
    return result


def main() -> int:
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes.decode("utf-8"))
    counters = {"replacements": 0}
    projected = replace_home(source, counters)
    profile_name = Path.home().name.casefold()
    serialized_projection = json.dumps(projected, ensure_ascii=False, sort_keys=True)
    if profile_name in serialized_projection.casefold():
        raise RuntimeError("The public projection still contains the local profile name")
    if counters["replacements"] != 10:
        raise RuntimeError(
            f"Expected exactly 10 home-path replacements; found {counters['replacements']}"
        )
    document = {
        "schema": "tohoku-r71-source-repair-public-projection-v1",
        "status": "PASS",
        "projection": {
            "source_name": SOURCE.name,
            "source_bytes": len(source_bytes),
            "source_sha256": hashlib.sha256(source_bytes).hexdigest().upper(),
            "transformation": "replace the local home-directory prefix with [LOCAL_HOME]",
            "strings_transformed": counters["replacements"],
            "semantic_fields_removed": 0,
        },
        "audit": projected,
    }
    output = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if profile_name in output.casefold():
        raise RuntimeError("The serialized public projection contains the local profile name")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_name(OUTPUT.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(output)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, OUTPUT)
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
                "bytes": OUTPUT.stat().st_size,
                "sha256": sha256(OUTPUT),
                "strings_transformed": counters["replacements"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
