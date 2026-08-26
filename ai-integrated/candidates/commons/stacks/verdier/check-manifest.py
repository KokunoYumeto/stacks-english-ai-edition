from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPECTED_UNIT_COUNT = 12
SHA256_RE = re.compile(r"[0-9A-F]{64}")


class ManifestError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def repo_root() -> Path:
    for directory in (ROOT, *ROOT.parents):
        if (
            (directory / "schemas" / "candidate-manifest.schema.json").is_file()
            and (directory / "registry" / "leases.json").is_file()
            and (directory / "upstream" / "stacks.lock.json").is_file()
        ):
            return directory.resolve()
    raise ManifestError("cannot resolve repository root")


REPO = repo_root()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot parse {path.name}: {exc}") from exc
    require(isinstance(value, dict), f"{path.name} must contain one JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (FileNotFoundError, OSError, UnicodeError) as exc:
        raise ManifestError(f"cannot read {path.name}: {exc}") from exc
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ManifestError(f"invalid JSONL at {path.name}:{number}: {exc}") from exc
        require(isinstance(row, dict), f"non-object JSONL row at {path.name}:{number}")
        rows.append(row)
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate_datetime(value: Any, locus: str) -> None:
    require(isinstance(value, str) and bool(value), f"{locus} must be a date-time string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ManifestError(f"{locus} is not ISO-8601: {value}") from exc
    require(parsed.tzinfo is not None, f"{locus} must include a timezone")


def validate_evidence(row: Any, locus: str) -> dict[str, str]:
    require(isinstance(row, dict), f"{locus} must be an object")
    allowed = {"path", "sha256", "source_url", "accessed_at_utc"}
    required = {"path", "sha256"}
    require(set(row) == required or (required <= set(row) <= allowed), f"{locus} has missing or additional fields: {sorted(set(row))}")
    logical = row.get("path")
    digest = row.get("sha256")
    require(isinstance(logical, str) and bool(logical), f"{locus}.path is empty")
    require("\\" not in logical, f"{locus}.path must use forward slashes")
    require(not Path(logical).is_absolute(), f"{locus}.path is absolute")
    require(isinstance(digest, str) and SHA256_RE.fullmatch(digest) is not None, f"{locus}.sha256 is not uppercase SHA-256")
    if "source_url" in row:
        require(isinstance(row["source_url"], str), f"{locus}.source_url must be a string")
    if "accessed_at_utc" in row:
        validate_datetime(row["accessed_at_utc"], f"{locus}.accessed_at_utc")
    resolved = (ROOT / logical).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ManifestError(f"{locus}.path escapes the candidate: {logical}") from exc
    require(resolved != (ROOT / "candidate.manifest.json").resolve(), "candidate.manifest.json may not hash itself")
    require(resolved.is_file(), f"manifest reference does not exist: {logical}")
    actual = sha256(resolved)
    require(actual == digest, f"manifest hash mismatch for {logical}: expected {digest}, found {actual}")
    return {"path": logical, "sha256": digest}


def validate_shape(manifest: dict[str, Any]) -> list[dict[str, str]]:
    required = {
        "schema",
        "candidate_id",
        "lease_id",
        "namespace",
        "writer_task",
        "upstream",
        "source_authorities",
        "source_closure",
        "stable_unit_manifest",
        "source_map",
        "decision_ledger",
        "rejection_ledger",
        "formula_diagram_inventory",
        "builds",
        "rights_state",
        "review_state",
        "independent_replay",
        "unresolved_defects",
        "stop_conditions",
        "generated_at_utc",
    }
    allowed = required | {"$schema"}
    require(set(manifest) == required or set(manifest) == allowed, f"manifest has missing/additional fields: {sorted(set(manifest))}")
    require(manifest["schema"] == "mathematics-commons-stacks-candidate-manifest/v1", "wrong manifest schema")
    expected_schema_path = Path(os.path.relpath(REPO / "schemas" / "candidate-manifest.schema.json", ROOT)).as_posix()
    if "$schema" in manifest:
        require(manifest["$schema"] == expected_schema_path, f"manifest $schema must reference the local schema as {expected_schema_path}")
    patterns = {
        "candidate_id": r"[a-z0-9][a-z0-9._-]*",
        "lease_id": r"stacks-lease-[0-9]{6}-[a-z0-9-]+",
        "namespace": r"commons/stacks/[a-z0-9][a-z0-9/-]*",
        "writer_task": r"[0-9a-f-]{36}",
    }
    for key, pattern in patterns.items():
        require(isinstance(manifest[key], str) and re.fullmatch(pattern, manifest[key]) is not None, f"invalid manifest {key}")

    upstream = manifest["upstream"]
    require(isinstance(upstream, dict) and set(upstream) == {"lock", "commit", "tree"}, "invalid upstream object")
    require(upstream["lock"] == "upstream/stacks.lock.json", "manifest uses the wrong upstream lock")
    for key in ("commit", "tree"):
        require(isinstance(upstream[key], str) and re.fullmatch(r"[0-9a-f]{40}", upstream[key]) is not None, f"invalid upstream {key}")

    closure = manifest["source_closure"]
    closure_keys = {"enumerated", "expected_units", "manifested_units", "complete"}
    require(isinstance(closure, dict) and set(closure) == closure_keys, "invalid source_closure object")
    require(closure["enumerated"] is True and closure["complete"] is True, "source closure is not declared complete")
    require(
        closure["expected_units"] == closure["manifested_units"] == EXPECTED_UNIT_COUNT,
        "source closure counts must both equal 12",
    )
    require(isinstance(manifest["rights_state"], str) and bool(manifest["rights_state"].strip()), "rights_state is empty")
    require(manifest["review_state"] in {"not_performed", "partial", "performed"}, "invalid review_state")
    require(manifest["independent_replay"] in {"not_performed", "passed", "failed"}, "invalid independent_replay")
    require(
        isinstance(manifest["unresolved_defects"], list)
        and all(isinstance(item, str) for item in manifest["unresolved_defects"]),
        "unresolved_defects must be a string array",
    )
    require(
        isinstance(manifest["stop_conditions"], list)
        and bool(manifest["stop_conditions"])
        and all(isinstance(item, str) for item in manifest["stop_conditions"]),
        "stop_conditions must be a nonempty string array",
    )
    validate_datetime(manifest["generated_at_utc"], "generated_at_utc")

    references: list[dict[str, str]] = []
    for key in ("source_authorities", "builds"):
        rows = manifest[key]
        require(isinstance(rows, list) and bool(rows), f"{key} must be a nonempty array")
        references.extend(validate_evidence(row, f"{key}[{index}]") for index, row in enumerate(rows))
    require(
        all(row["path"].startswith("authority/") for row in manifest["source_authorities"]),
        "source_authorities contains a path outside authority/",
    )
    require(
        all(not row["path"].startswith("authority/") for row in manifest["builds"]),
        "builds misclassifies an authority file",
    )
    for key in (
        "stable_unit_manifest",
        "source_map",
        "decision_ledger",
        "rejection_ledger",
        "formula_diagram_inventory",
    ):
        references.append(validate_evidence(manifest[key], key))
    exact_singled = {
        "stable_unit_manifest": "stable-units.json",
        "source_map": "source-map.jsonl",
        "decision_ledger": "decisions.jsonl",
        "rejection_ledger": "rejections.jsonl",
        "formula_diagram_inventory": "formula-diagram-inventory.json",
    }
    for key, expected_path in exact_singled.items():
        require(manifest[key]["path"] == expected_path, f"{key} must reference {expected_path}")
    paths = [row["path"] for row in references]
    require(len(paths) == len(set(paths)), "manifest repeats a referenced path")
    return references


def validate_identity_and_counts(manifest: dict[str, Any]) -> None:
    pointer = load_json(ROOT / "LEASE.json")
    config = load_json(ROOT / "candidate.config.json")
    registry = load_json(REPO / pointer.get("lease_registry", "registry/leases.json"))
    matches = [
        row
        for row in registry.get("events", [])
        if isinstance(row, dict) and row.get("lease_id") == pointer.get("lease_id")
    ]
    require(matches and matches[-1].get("state") == "active", "candidate lease is not active")
    active = matches[-1]
    expected_path = ROOT.relative_to(REPO).as_posix()
    require(active.get("candidate_path") == expected_path, "active lease points to another candidate path")
    for field in ("lease_id", "namespace", "writer_task"):
        require(manifest[field] == pointer.get(field) == active.get(field) == config.get(field), f"identity mismatch for {field}")
    require(manifest["candidate_id"] == config.get("candidate_id"), "manifest candidate_id differs from config")
    lock = load_json(REPO / "upstream" / "stacks.lock.json")
    require(manifest["upstream"]["commit"] == active.get("upstream_commit") == lock.get("commit"), "manifest upstream commit does not match lease/lock")
    require(manifest["upstream"]["tree"] == active.get("upstream_tree") == lock.get("tree"), "manifest upstream tree does not match lease/lock")

    stable_path = ROOT / manifest["stable_unit_manifest"]["path"]
    stable = load_json(stable_path)
    units = stable.get("units")
    require(isinstance(units, list) and stable.get("unit_count") == len(units) == EXPECTED_UNIT_COUNT, "manifested stable-unit count is not 12")
    unit_ids = [row.get("id", row.get("unit_id")) for row in units if isinstance(row, dict)]
    require(len(unit_ids) == EXPECTED_UNIT_COUNT and len(unit_ids) == len(set(unit_ids)), "manifested stable-unit IDs are missing or duplicated")
    source_rows = load_jsonl(ROOT / manifest["source_map"]["path"])
    mapped = [row.get("unit_id", row.get("candidate_unit_id")) for row in source_rows]
    require(mapped == unit_ids, "manifested source map does not cover the stable units exactly")
    inventory = load_json(ROOT / manifest["formula_diagram_inventory"]["path"])
    require(inventory.get("unit_count") == EXPECTED_UNIT_COUNT, "manifested formula inventory count is not 12")

    replay_path = ROOT / "replay" / "independent-review.json"
    if replay_path.exists():
        replay = load_json(replay_path)
        require(isinstance(replay.get("passed"), bool), "independent replay receipt lacks Boolean passed")
        expected_replay = "passed" if replay["passed"] else "failed"
        require(manifest["independent_replay"] == expected_replay, "manifest independent_replay differs from receipt")
        require(manifest["review_state"] == "performed", "manifest does not record performed independent review")
    else:
        require(manifest["independent_replay"] == "not_performed", "manifest overstates absent independent replay")


def public_candidate_files() -> list[Path]:
    files: list[Path] = []
    stack = [ROOT]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            if entry.is_dir(follow_symlinks=False):
                if entry.name in {".work", ".git", "__pycache__"}:
                    continue
                stack.append(Path(entry.path))
            elif entry.is_file(follow_symlinks=False):
                path = Path(entry.path)
                if path.name != "candidate.manifest.json":
                    files.append(path)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def validate_file_closure(references: list[dict[str, str]]) -> None:
    referenced = sorted(row["path"] for row in references)
    actual = sorted(
        path.relative_to(ROOT).as_posix()
        for path in public_candidate_files()
    )
    missing = sorted(set(actual) - set(referenced))
    extra = sorted(set(referenced) - set(actual))
    require(not missing and not extra, f"manifest file closure mismatch; unreferenced={missing}; nonexistent={extra}")
    require("candidate.manifest.json" not in referenced, "manifest self-hash recursion detected")
    require(any(path.endswith("builds/build-receipt.json") for path in referenced), "manifest does not reference a build receipt")
    require(any(path.endswith("builds/validation.json") for path in referenced), "manifest does not reference validation evidence")
    require(any(path.endswith("builds/visual-qa.json") for path in referenced), "manifest does not reference visual-QA evidence")


def main() -> int:
    try:
        manifest_path = ROOT / "candidate.manifest.json"
        manifest = load_json(manifest_path)
        references = validate_shape(manifest)
        validate_identity_and_counts(manifest)
        validate_file_closure(references)
        print(
            json.dumps(
                {
                    "passed": True,
                    "references": len(references),
                    "manifest_sha256": sha256(manifest_path),
                    "stable_units": EXPECTED_UNIT_COUNT,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ManifestError, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        print(f"MANIFEST CHECK FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
