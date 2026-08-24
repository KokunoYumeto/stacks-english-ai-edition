from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def validate_manifest_shape(manifest: dict[str, object]) -> None:
    required = {
        "schema", "candidate_id", "lease_id", "namespace", "writer_task",
        "upstream", "source_authorities", "source_closure",
        "stable_unit_manifest", "source_map", "decision_ledger",
        "rejection_ledger", "formula_diagram_inventory", "builds",
        "rights_state", "review_state", "independent_replay",
        "unresolved_defects", "stop_conditions", "generated_at_utc",
    }
    allowed = required | {"$schema"}
    if set(manifest) - allowed:
        raise AssertionError(f"unexpected manifest keys: {sorted(set(manifest) - allowed)}")
    if required - set(manifest):
        raise AssertionError(f"missing manifest keys: {sorted(required - set(manifest))}")
    if manifest["schema"] != "mathematics-commons-stacks-candidate-manifest/v1":
        raise AssertionError("wrong manifest schema")
    patterns = {
        "candidate_id": r"^[a-z0-9][a-z0-9._-]*$",
        "lease_id": r"^stacks-lease-[0-9]{6}-[a-z0-9-]+$",
        "namespace": r"^commons/stacks/[a-z0-9][a-z0-9/-]*$",
        "writer_task": r"^[0-9a-f-]{36}$",
    }
    for key, pattern in patterns.items():
        if not isinstance(manifest[key], str) or not re.fullmatch(pattern, manifest[key]):
            raise AssertionError(f"invalid {key}")
    upstream = manifest["upstream"]
    if not isinstance(upstream, dict) or set(upstream) != {"lock", "commit", "tree"}:
        raise AssertionError("invalid upstream object")
    if upstream["lock"] != "upstream/stacks.lock.json":
        raise AssertionError("invalid upstream lock")
    for key in ("commit", "tree"):
        if not isinstance(upstream[key], str) or not re.fullmatch(r"[0-9a-f]{40}", upstream[key]):
            raise AssertionError(f"invalid upstream {key}")
    closure = manifest["source_closure"]
    if not isinstance(closure, dict) or set(closure) != {"enumerated", "expected_units", "manifested_units", "complete"}:
        raise AssertionError("invalid source_closure object")
    if closure["enumerated"] is not True or closure["complete"] is not True:
        raise AssertionError("source closure is not complete")
    for key in ("expected_units", "manifested_units"):
        if not isinstance(closure[key], int) or closure[key] < 1:
            raise AssertionError(f"invalid source_closure {key}")
    if manifest["review_state"] not in {"not_performed", "partial", "performed"}:
        raise AssertionError("invalid review_state")
    if manifest["independent_replay"] not in {"not_performed", "passed", "failed"}:
        raise AssertionError("invalid independent_replay")
    if not isinstance(manifest["rights_state"], str) or not manifest["rights_state"]:
        raise AssertionError("empty rights_state")
    if not isinstance(manifest["unresolved_defects"], list) or not all(isinstance(x, str) for x in manifest["unresolved_defects"]):
        raise AssertionError("invalid unresolved_defects")
    if not isinstance(manifest["stop_conditions"], list) or not manifest["stop_conditions"] or not all(isinstance(x, str) for x in manifest["stop_conditions"]):
        raise AssertionError("invalid stop_conditions")
    if not isinstance(manifest["generated_at_utc"], str):
        raise AssertionError("invalid generated_at_utc")
    datetime.fromisoformat(manifest["generated_at_utc"].replace("Z", "+00:00"))

    def validate_evidence(row: object) -> None:
        if not isinstance(row, dict) or not {"path", "sha256"}.issubset(row):
            raise AssertionError("invalid hashed evidence")
        if set(row) - {"path", "sha256", "source_url", "accessed_at_utc"}:
            raise AssertionError("unexpected hashed-evidence keys")
        if not isinstance(row["path"], str) or not row["path"]:
            raise AssertionError("empty evidence path")
        if not isinstance(row["sha256"], str) or not re.fullmatch(r"[0-9A-F]{64}", row["sha256"]):
            raise AssertionError(f"invalid evidence hash: {row['path']}")

    for key in ("source_authorities", "builds"):
        rows = manifest[key]
        if not isinstance(rows, list) or not rows:
            raise AssertionError(f"empty {key}")
        for row in rows:
            validate_evidence(row)
    for key in ("stable_unit_manifest", "source_map", "decision_ledger", "rejection_ledger", "formula_diagram_inventory"):
        validate_evidence(manifest[key])


def main() -> int:
    manifest_path = ROOT / "candidate.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest_shape(manifest)
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
