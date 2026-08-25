from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    manifest_path = ROOT / "candidate.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads((REPO / "schemas" / "candidate-manifest.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        raise AssertionError("; ".join(error.message for error in errors))
    references = []
    for key in ("source_authorities", "builds"):
        references.extend(manifest[key])
    for key in ("stable_unit_manifest", "source_map", "decision_ledger", "rejection_ledger", "formula_diagram_inventory"):
        references.append(manifest[key])
    paths = [row["path"] for row in references]
    if len(paths) != len(set(paths)):
        raise AssertionError("manifest repeats a referenced path")
    actual = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() and path.name != "candidate.manifest.json" and "__pycache__" not in path.parts)
    if sorted(paths) != actual:
        missing = sorted(set(actual) - set(paths))
        extra = sorted(set(paths) - set(actual))
        raise AssertionError(f"manifest file closure mismatch; missing={missing}; extra={extra}")
    for row in references:
        path = ROOT / row["path"]
        if sha256(path) != row["sha256"]:
            raise AssertionError(f"manifest hash mismatch: {row['path']}")
    print(json.dumps({"passed": True, "references": len(references), "manifest_sha256": sha256(manifest_path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
