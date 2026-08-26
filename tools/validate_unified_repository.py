#!/usr/bin/env python3
"""Fast fail-closed validation for the unified AI-integrated Stacks tree."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "a04446e57ec1fbc252a871afcec7752fb2807b14"
SOURCE_UNION = "ad58625f60e6816905ff217d21d91b07b2722fcf"
EGA_EXPORT = "91df7f1c96bd4973264c29b0e121253a05d1d361"
COMPOSITION_RECEIPT = Path("validation/composition-current.json")
DEFAULT_BUILD_RECEIPT = Path(
    "validation/unified-fixed-point-2026-08-25-r19.json"
)
R18_R19_RELEASE_RECEIPT = Path(
    "validation/errata-r18-r19-release-2026-08-25.json"
)
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9A-Fa-f]{64}$")
COMPOSITION_MODE = (
    "authority-bound registry-order projection committed as "
    "protected-branch-compatible linear history"
)
EXPECTED_FIXED_POINT_SUFFIXES = [
    ".aux",
    ".bbl",
    ".idx",
    ".ind",
    ".lof",
    ".lot",
    ".out",
    ".toc",
    ".pdf",
]

PUBLIC_MARKDOWN = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "PROVENANCE.md",
    "VALIDATION.md",
    "CONTRIBUTING.md",
    "ai-integrated/README.md",
)

REQUIRED_PATHS = (
    "chapters.tex",
    "COPYING",
    "fac/STATUS.md",
    "tohoku_r71/STATUS.md",
    "gaga_r3/STATUS.md",
    "gaga.tex",
    "fga/README.md",
    "fga/audit.json",
    "ega/README.md",
    "ega/smap.csv",
    "ai-integrated/registry/overlays.json",
    "ai-integrated/upstream/stacks.lock.json",
    "tools/verify_overlay_projection.py",
    COMPOSITION_RECEIPT.as_posix(),
    R18_R19_RELEASE_RECEIPT.as_posix(),
    "validation/unification-release-2026-08-25.json",
)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git_bytes(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git_optional(*args: str) -> str | None:
    result = git(*args)
    return result.stdout.strip() if result.returncode == 0 else None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def resolve_requested_path(value: Path) -> Path:
    return value.resolve() if value.is_absolute() else (ROOT / value).resolve()


def load_json_object(path: Path, errors: list[str], label: str) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {label} {display_path(path)}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} is not a JSON object: {display_path(path)}")
        return None
    return value


def require_commit(commit: object, label: str, errors: list[str]) -> str | None:
    if not isinstance(commit, str) or not SHA1_RE.fullmatch(commit):
        errors.append(f"invalid {label} commit: {commit!r}")
        return None
    result = git("cat-file", "-e", f"{commit}^{{commit}}")
    if result.returncode != 0:
        errors.append(f"missing {label} commit object: {commit}")
        return None
    return commit


def require_sha1_identity(value: object, label: str, errors: list[str]) -> str | None:
    """Validate a provenance identity without requiring its object in this history."""
    if not isinstance(value, str) or not SHA1_RE.fullmatch(value):
        errors.append(f"invalid {label} identity: {value!r}")
        return None
    return value


def require_ancestor(
    ancestor: str | None, descendant: str, label: str, errors: list[str]
) -> None:
    if ancestor is None:
        return
    result = git("merge-base", "--is-ancestor", ancestor, descendant)
    if result.returncode != 0:
        errors.append(f"missing {label} ancestry: {ancestor} -> {descendant}")


def commit_parents(commit: str, errors: list[str], label: str) -> tuple[str, ...]:
    result = git("rev-list", "--parents", "-n", "1", commit)
    if result.returncode != 0:
        errors.append(f"could not read {label} parent list: {commit}")
        return ()
    parts = result.stdout.strip().split()
    if not parts or parts[0] != commit:
        errors.append(f"invalid {label} parent list: {commit}")
        return ()
    return tuple(parts[1:])


def require_single_parent(
    commit: str | None,
    label: str,
    errors: list[str],
    expected: str | None = None,
) -> None:
    if commit is None:
        return
    parents = commit_parents(commit, errors, label)
    if len(parents) != 1:
        errors.append(f"{label} is not a single-parent commit: {commit}")
    elif expected is not None and parents[0] != expected:
        errors.append(
            f"{label} parent mismatch: expected {expected}, found {parents[0]}"
        )


def require_linear_suffix(
    ancestor: str | None, descendant: str, label: str, errors: list[str]
) -> None:
    if ancestor is None:
        return
    result = git("rev-list", "--parents", f"{ancestor}..{descendant}")
    if result.returncode != 0:
        errors.append(f"could not inspect {label}: {ancestor} -> {descendant}")
        return
    for line in result.stdout.splitlines():
        if len(line.split()) > 2:
            errors.append(f"{label} contains a merge commit: {line.split()[0]}")


def commit_blob(commit: str | None, relative: str, errors: list[str], label: str) -> str | None:
    if commit is None:
        return None
    result = git("rev-parse", f"{commit}:{relative}")
    value = result.stdout.strip().lower()
    if result.returncode != 0 or not SHA1_RE.fullmatch(value):
        errors.append(f"missing {label} blob {relative} at {commit}")
        return None
    return value


def require_clean_path(relative: str, errors: list[str]) -> None:
    for staged, args in (
        (False, ("diff", "--quiet", "--", relative)),
        (True, ("diff", "--cached", "--quiet", "--", relative)),
    ):
        result = git(*args)
        if result.returncode != 0:
            state = "staged" if staged else "worktree"
            errors.append(f"{state} changes prevent exact projection validation: {relative}")


def committed_bytes(commit: str, relative: str, errors: list[str], label: str) -> bytes | None:
    result = git_bytes("cat-file", "blob", f"{commit}:{relative}")
    if result.returncode != 0:
        errors.append(f"missing {label} content {relative} at {commit}")
        return None
    return result.stdout


def candidate_dir(overlay_id: str) -> Path:
    suffix = overlay_id.rsplit("-r", 1)[1]
    base = ROOT / "ai-integrated/candidates/commons/stacks/errata"
    return base if suffix == "1" else base / f"r{suffix}"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.relative_to(ROOT)}:{number}: {exc}") from exc
    return rows


def literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"missing literal assignment {name} in {path.relative_to(ROOT)}")


def validate_links(errors: list[str]) -> None:
    link_re = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for relative in PUBLIC_MARKDOWN:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        for raw_target in link_re.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"broken link in {relative}: {raw_target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-receipt",
        type=Path,
        default=DEFAULT_BUILD_RECEIPT,
        metavar="PATH",
        help=(
            "fixed-point build receipt to validate, relative to the repository root "
            f"(default: {DEFAULT_BUILD_RECEIPT.as_posix()})"
        ),
    )
    args = parser.parse_args(argv)

    errors: list[str] = []
    composition_path = ROOT / COMPOSITION_RECEIPT
    build_receipt_path = resolve_requested_path(args.build_receipt)
    build_receipt: dict = {}
    build_receipt_bytes: bytes | None = None
    try:
        build_receipt_relative = build_receipt_path.relative_to(ROOT).as_posix()
    except ValueError:
        build_receipt_relative = ""
        errors.append("fixed-point build receipt must be inside the repository")

    for relative in REQUIRED_PATHS + PUBLIC_MARKDOWN:
        if not (ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")
    if not build_receipt_path.is_file():
        errors.append(f"missing fixed-point build receipt: {display_path(build_receipt_path)}")
    elif build_receipt_relative:
        require_clean_path(build_receipt_relative, errors)
        build_receipt_bytes = committed_bytes(
            "HEAD", build_receipt_relative, errors, "fixed-point build receipt"
        )
        if build_receipt_bytes is not None:
            try:
                parsed_build_receipt = json.loads(build_receipt_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid fixed-point build receipt: {exc}")
            else:
                if isinstance(parsed_build_receipt, dict):
                    build_receipt = parsed_build_receipt
                else:
                    errors.append("fixed-point build receipt is not a JSON object")

    composition = load_json_object(composition_path, errors, "composition receipt") or {}
    if composition.get("schema") != "unofficial-ai-integrated-stacks-composition/v2":
        errors.append("composition receipt schema is invalid")
    if composition.get("status") != "PASS":
        errors.append("composition receipt is not PASS")
    composition_registry = composition.get("registry")
    composition_state = composition.get("composition")
    composition_authority = composition.get("authority")
    if not isinstance(composition_registry, dict):
        errors.append("composition receipt lacks registry state")
        composition_registry = {}
    if not isinstance(composition_state, dict):
        errors.append("composition receipt lacks composition state")
        composition_state = {}
    if not isinstance(composition_authority, dict):
        errors.append("composition receipt lacks authority state")
        composition_authority = {}
    if composition_state.get("mode") != COMPOSITION_MODE:
        errors.append("composition receipt has the wrong protected-linear mode")
    if composition_authority.get("commit") != UPSTREAM:
        errors.append("composition receipt changes the pinned upstream authority")
    upstream_tree_result = git("rev-parse", f"{UPSTREAM}^{{tree}}")
    if (
        upstream_tree_result.returncode != 0
        or composition_authority.get("tree") != upstream_tree_result.stdout.strip()
    ):
        errors.append("composition receipt has the wrong upstream authority tree")

    for commit, label in (
        (UPSTREAM, "pinned upstream"),
        (SOURCE_UNION, "FAC/Tohoku/GAGA/FGA source union"),
        (EGA_EXPORT, "EGA export"),
    ):
        result = git("merge-base", "--is-ancestor", commit, "HEAD")
        if result.returncode != 0:
            errors.append(f"missing {label} ancestor: {commit}")

    composition_source_commit = require_commit(
        composition_state.get("source_commit"), "composition source", errors
    )
    composition_source_tree = require_sha1_identity(
        composition_state.get("source_tree"), "composition source tree", errors
    )
    materialization_tip = require_sha1_identity(
        composition_state.get("materialization_tip"),
        "composition materialization tip",
        errors,
    )
    require_ancestor(
        composition_source_commit, "HEAD", "composition-source-to-HEAD", errors
    )
    if composition_source_commit is not None and composition_source_tree is not None:
        source_tree_result = git(
            "rev-parse", f"{composition_source_commit}^{{tree}}"
        )
        if (
            source_tree_result.returncode != 0
            or source_tree_result.stdout.strip() != composition_source_tree
        ):
            errors.append("composition source tree identity mismatch")

    registry_import_commit = require_commit(
        composition_registry.get("linear_import_commit"),
        "registry linear import",
        errors,
    )
    registry_import_tree = require_sha1_identity(
        composition_registry.get("linear_import_tree"),
        "registry linear import tree",
        errors,
    )
    require_ancestor(
        registry_import_commit, "HEAD", "registry-import-to-HEAD", errors
    )
    require_ancestor(
        UPSTREAM, registry_import_commit or "HEAD", "authority-to-registry-import", errors
    )
    require_single_parent(registry_import_commit, "registry linear import", errors)
    require_single_parent(
        composition_source_commit,
        "composition source",
        errors,
        registry_import_commit,
    )
    require_linear_suffix(
        composition_source_commit, "HEAD", "protected publication suffix", errors
    )
    if composition_source_commit is not None:
        require_ancestor(
            registry_import_commit,
            composition_source_commit,
            "registry-import-to-composition-source",
            errors,
        )
    if registry_import_commit is not None and registry_import_tree is not None:
        import_tree_result = git(
            "rev-parse", f"{registry_import_commit}^{{tree}}"
        )
        if (
            import_tree_result.returncode != 0
            or import_tree_result.stdout.strip() != registry_import_tree
        ):
            errors.append("registry linear-import tree identity mismatch")

    cutoff_commit = require_sha1_identity(
        composition_registry.get("cutoff_commit"), "registry cutoff commit", errors
    )

    overlays_relative = composition_registry.get("overlays_path")
    if not isinstance(overlays_relative, str) or not overlays_relative:
        errors.append("composition receipt lacks an overlay registry path")
        overlays_relative = "ai-integrated/registry/overlays.json"
    registry_path = (ROOT / overlays_relative).resolve()
    try:
        registry_path.relative_to(ROOT)
    except ValueError:
        errors.append(f"overlay registry path escapes repository: {overlays_relative}")
        registry_path = ROOT / "ai-integrated/registry/overlays.json"
        overlays_relative = "ai-integrated/registry/overlays.json"

    require_clean_path(overlays_relative, errors)
    registry_bytes = committed_bytes("HEAD", overlays_relative, errors, "registry")
    if registry_bytes is None:
        registry = {}
    else:
        expected_registry_bytes = composition_registry.get("overlays_bytes")
        expected_registry_sha = composition_registry.get("overlays_sha256")
        if type(expected_registry_bytes) is not int or len(registry_bytes) != expected_registry_bytes:
            errors.append(
                "overlay registry byte count mismatch: "
                f"expected {expected_registry_bytes}, found {len(registry_bytes)}"
            )
        if (
            not isinstance(expected_registry_sha, str)
            or not SHA256_RE.fullmatch(expected_registry_sha)
            or sha256_bytes(registry_bytes) != expected_registry_sha.upper()
        ):
            errors.append("overlay registry SHA-256 does not match composition receipt")
        try:
            registry = json.loads(registry_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid committed overlay registry: {exc}")
            registry = {}

    expected_registry_blob = require_sha1_identity(
        composition_registry.get("overlays_git_blob"),
        "overlay registry Git blob",
        errors,
    )
    if registry_bytes is not None and expected_registry_blob is not None:
        if git_blob_sha1(registry_bytes) != expected_registry_blob:
            errors.append("overlay registry Git blob does not match composition receipt")
        imported_registry_blob = commit_blob(
            registry_import_commit,
            overlays_relative,
            errors,
            "registry linear import",
        )
        if imported_registry_blob != expected_registry_blob:
            errors.append("registry linear-import blob binding mismatch")
        cutoff_registry_blob = git_optional(
            "rev-parse", f"{cutoff_commit}:registry/overlays.json"
        ) if cutoff_commit is not None else None
        if (
            cutoff_registry_blob is not None
            and cutoff_registry_blob != expected_registry_blob
        ):
            errors.append("registry cutoff blob binding mismatch")

    entries = registry.get("registered_entries", [])
    if not isinstance(entries, list):
        errors.append("overlay registry lacks registered_entries")
        entries = []
    expected_overlays = composition_registry.get("registered_overlays")
    if type(expected_overlays) is not int or len(entries) != expected_overlays:
        errors.append(
            f"expected {expected_overlays} registered overlays, found {len(entries)}"
        )
    if entries and (
        not isinstance(entries[-1], dict)
        or entries[-1].get("id") != composition_registry.get("last_admitted_overlay")
    ):
        errors.append("overlay registry does not end at the composition cutoff")

    previous = composition.get("previous_cutoff")
    if not isinstance(previous, dict):
        errors.append("composition receipt lacks previous-cutoff transition evidence")
        previous = {}
    previous_registry = require_sha1_identity(
        previous.get("registry_commit"), "previous registry cutoff", errors
    )
    previous_last = previous.get("last_admitted_overlay")
    previous_derived_blob = require_sha1_identity(
        previous.get("derived_git_blob"), "previous authority derived blob", errors
    )
    if not isinstance(previous_last, str) or not previous_last:
        errors.append("previous cutoff lacks a last-admitted overlay")
    if previous.get("derived_equal_to_authority") is not True:
        errors.append("previous cutoff does not assert authority equality")
    previous_index = next(
        (index for index, entry in enumerate(entries)
         if isinstance(entry, dict) and entry.get("id") == previous_last),
        None,
    )
    if previous_index is None:
        errors.append("previous cutoff overlay is absent from the imported registry")
        previous_index = -1
    new_overlays = composition.get("new_overlays")
    if not isinstance(new_overlays, list) or not new_overlays:
        errors.append("composition receipt lacks new-overlay transition evidence")
        new_overlays = []
    registry_suffix = entries[previous_index + 1 :] if previous_index >= 0 else []
    if len(registry_suffix) != len(new_overlays):
        errors.append("new-overlay transition length does not match registry suffix")
    for overlay, entry in zip(new_overlays, registry_suffix):
        if not isinstance(overlay, dict) or not isinstance(entry, dict):
            errors.append("new-overlay transition contains an invalid entry")
            continue
        if overlay.get("id") != entry.get("id"):
            errors.append("new-overlay transition is not registry ordered")
        stable_count = overlay.get("stable_ids")
        operation_count = overlay.get("operations")
        if type(stable_count) is not int or stable_count < 1:
            errors.append(f"invalid stable-ID count in transition: {overlay.get('id')!r}")
        elif stable_count != len(entry.get("stable_ids", [])):
            errors.append(f"transition stable-ID count mismatch: {overlay.get('id')!r}")
        if type(operation_count) is not int or operation_count < 1:
            errors.append(f"invalid operation count in transition: {overlay.get('id')!r}")
        for key in ("manifest_sha256", "payload_sha256", "review_receipt_sha256"):
            if not isinstance(overlay.get(key), str) or not SHA256_RE.fullmatch(overlay[key]):
                errors.append(f"invalid {key} in transition: {overlay.get('id')!r}")
        materialized = overlay.get("materialized_commit")
        if not isinstance(materialized, str) or not SHA1_RE.fullmatch(materialized):
            errors.append(f"invalid materialized commit in transition: {overlay.get('id')!r}")
        elif git_optional("cat-file", "-e", f"{materialized}^{{commit}}") is not None:
            require_single_parent(materialized, f"materialized {overlay.get('id')}", errors, UPSTREAM)
    if registry_suffix and registry_suffix[-1].get("id") != composition_registry.get(
        "last_admitted_overlay"
    ):
        errors.append("new-overlay transition does not end at the admitted cutoff")
    if previous_registry is not None and cutoff_commit is not None:
        if (
            git_optional("cat-file", "-e", f"{previous_registry}^{{commit}}") is not None
            and git_optional("cat-file", "-e", f"{cutoff_commit}^{{commit}}") is not None
        ):
            require_ancestor(previous_registry, cutoff_commit, "previous-to-current registry", errors)

    registered_ids: list[str] = []
    v2_operations = 0
    v1_replacements = 0
    tag_additions = 0
    overlay_operation_counts: dict[str, int] = {}
    entry_by_id: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            errors.append("overlay registry contains an invalid entry")
            continue
        overlay_id = entry["id"]
        if overlay_id in entry_by_id:
            errors.append(f"duplicate overlay registry entry: {overlay_id}")
            continue
        entry_by_id[overlay_id] = entry
        raw_ids = entry.get("stable_ids", "")
        if isinstance(raw_ids, list) and all(isinstance(item, str) for item in raw_ids):
            ids = raw_ids
        elif isinstance(raw_ids, str):
            ids = raw_ids.split()
        else:
            errors.append(f"invalid stable-ID inventory for {overlay_id}")
            ids = []
        registered_ids.extend(ids)
        directory = candidate_dir(overlay_id)
        manifest = directory / "candidate.manifest.json"
        manifest_relative = manifest.relative_to(ROOT).as_posix()
        require_clean_path(manifest_relative, errors)
        manifest_bytes = committed_bytes("HEAD", manifest_relative, errors, "manifest")
        manifest_hash = sha256_bytes(manifest_bytes) if manifest_bytes is not None else ""
        manifest_data: dict = {}
        manifest_build_hashes: dict[str, str] = {}
        if manifest_hash != str(entry.get("manifest_sha256", "")).upper():
            errors.append(f"candidate manifest hash mismatch for {overlay_id}")
        if manifest_bytes is not None:
            try:
                parsed_manifest = json.loads(manifest_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid candidate manifest for {overlay_id}: {exc}")
            else:
                if not isinstance(parsed_manifest, dict):
                    errors.append(f"candidate manifest is not an object for {overlay_id}")
                    parsed_manifest = {}
                manifest_data = parsed_manifest
                if manifest_data.get("candidate_id") != overlay_id:
                    errors.append(f"candidate manifest identity mismatch for {overlay_id}")
                if manifest_data.get("schema") != (
                    "mathematics-commons-stacks-candidate-manifest/v1"
                ):
                    errors.append(f"candidate manifest schema mismatch for {overlay_id}")
                manifest_upstream = manifest_data.get("upstream")
                if not isinstance(manifest_upstream, dict) or (
                    manifest_upstream.get("commit") != UPSTREAM
                    or manifest_upstream.get("tree")
                    != composition_authority.get("tree")
                ):
                    errors.append(f"candidate upstream binding mismatch for {overlay_id}")
                closure = manifest_data.get("source_closure")
                if not isinstance(closure, dict) or (
                    closure.get("enumerated") is not True
                    or closure.get("complete") is not True
                    or closure.get("expected_units") != len(ids)
                    or closure.get("manifested_units") != len(ids)
                ):
                    errors.append(f"candidate source closure mismatch for {overlay_id}")
                manifest_builds = manifest_data.get("builds")
                if not isinstance(manifest_builds, list):
                    errors.append(f"candidate build inventory is invalid for {overlay_id}")
                else:
                    for build_item in manifest_builds:
                        if not isinstance(build_item, dict):
                            errors.append(
                                f"candidate build inventory contains an invalid row for "
                                f"{overlay_id}"
                            )
                            continue
                        build_path = build_item.get("path")
                        build_hash = build_item.get("sha256")
                        if (
                            not isinstance(build_path, str)
                            or not isinstance(build_hash, str)
                            or not SHA256_RE.fullmatch(build_hash)
                            or build_path in manifest_build_hashes
                        ):
                            errors.append(
                                f"candidate build binding is invalid or duplicated for "
                                f"{overlay_id}: {build_path!r}"
                            )
                            continue
                        manifest_build_hashes[build_path] = build_hash.upper()

        review_relative_value = entry.get("review_receipt")
        if not isinstance(review_relative_value, str):
            errors.append(f"invalid independent replay path for {overlay_id}")
            review_relative_value = ""
        review = ROOT / "ai-integrated" / review_relative_value
        if not review.is_file():
            errors.append(f"missing independent replay receipt for {overlay_id}")
        else:
            review_relative = review.relative_to(ROOT).as_posix()
            require_clean_path(review_relative, errors)
            review_bytes = committed_bytes("HEAD", review_relative, errors, "review")
            if review_bytes is not None:
                try:
                    review_candidate_relative = review.relative_to(directory).as_posix()
                except ValueError:
                    errors.append(f"independent replay escapes candidate: {overlay_id}")
                else:
                    if manifest_build_hashes.get(review_candidate_relative) != sha256_bytes(
                        review_bytes
                    ):
                        errors.append(
                            f"manifest/review hash mismatch for {overlay_id}"
                        )
                try:
                    review_data = json.loads(review_bytes.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    errors.append(f"invalid independent replay receipt for {overlay_id}: {exc}")
                else:
                    if review_data.get("candidate_id") != overlay_id:
                        errors.append(f"independent replay identity mismatch for {overlay_id}")
                    outcome = review_data.get("outcome")
                    review_passed = review_data.get("passed") is True or (
                        isinstance(outcome, dict) and outcome.get("passed") is True
                    )
                    if not review_passed:
                        errors.append(f"independent replay is not passing for {overlay_id}")
        source_map_binding = manifest_data.get("source_map")
        if not isinstance(source_map_binding, dict) or (
            source_map_binding.get("path") != "source-map.jsonl"
            or not isinstance(source_map_binding.get("sha256"), str)
            or not SHA256_RE.fullmatch(source_map_binding["sha256"])
        ):
            errors.append(f"invalid manifest source-map binding for {overlay_id}")
            source_map_binding = {}
        source_map = directory / "source-map.jsonl"
        if not source_map.is_file():
            errors.append(f"missing source map: {source_map.relative_to(ROOT)}")
            continue
        source_map_relative = source_map.relative_to(ROOT).as_posix()
        require_clean_path(source_map_relative, errors)
        source_map_bytes = committed_bytes(
            "HEAD", source_map_relative, errors, "source map"
        )
        if source_map_bytes is not None and sha256_bytes(source_map_bytes) != str(
            source_map_binding.get("sha256", "")
        ).upper():
            errors.append(f"manifest/source-map hash mismatch for {overlay_id}")
        rows = read_jsonl(source_map)
        mapped_ids = [row.get("unit_id") for row in rows]
        if mapped_ids != ids:
            errors.append(f"registry/source-map ID mismatch for {overlay_id}")
        payload_paths = {
            row.get("payload") for row in rows if isinstance(row.get("payload"), str)
        }
        if len(payload_paths) != len(
            {row.get("payload") for row in rows}
        ):
            errors.append(f"invalid payload path in source map for {overlay_id}")
        for payload_candidate_relative in sorted(payload_paths):
            payload_path = (directory / payload_candidate_relative).resolve()
            try:
                payload_path.relative_to(directory.resolve())
                payload_relative = payload_path.relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(
                    f"payload path escapes candidate for {overlay_id}: "
                    f"{payload_candidate_relative!r}"
                )
                continue
            require_clean_path(payload_relative, errors)
            payload_bytes = committed_bytes("HEAD", payload_relative, errors, "payload")
            if payload_bytes is not None and manifest_build_hashes.get(
                payload_candidate_relative
            ) != sha256_bytes(payload_bytes):
                errors.append(
                    f"manifest/payload hash mismatch for {overlay_id}/"
                    f"{payload_candidate_relative}"
                )
        overlay_operations = 0
        for row in rows:
            operations = row.get("operations", [])
            if not operations:
                continue
            source = ROOT / row["source"]
            if not source.is_file():
                errors.append(f"missing composed source: {row['source']}")
                continue
            source_text = source.read_text(encoding="utf-8")
            for operation in operations:
                v2_operations += 1
                overlay_operations += 1
                replacement = operation["replacement_text"]
                if replacement not in source_text:
                    errors.append(
                        f"missing composed replacement {operation['operation_id']} "
                        f"in {row['source']}"
                    )
        overlay_operation_counts[overlay_id] = overlay_operations

    for round_number in (1, 2, 3):
        overlay_id = f"stacks-errata-a04446e-r{round_number}"
        directory = candidate_dir(overlay_id)
        replacements = literal_assignment(directory / "verify.py", "REPLACEMENTS")
        if not isinstance(replacements, dict):
            errors.append(f"REPLACEMENTS is not a mapping for R{round_number}")
            continue
        for source_name, rows in replacements.items():
            source_text = (ROOT / source_name).read_text(encoding="utf-8")
            for row in rows:
                replacement_text = row[1]
                v1_replacements += 1
                if replacement_text not in source_text:
                    errors.append(
                        f"missing composed R{round_number} replacement in {source_name}: "
                        f"{replacement_text!r}"
                    )

    new_tags = literal_assignment(
        candidate_dir("stacks-errata-a04446e-r1") / "verify.py", "NEW_TAGS"
    )
    tag_lines = set((ROOT / "tags/tags").read_text(encoding="utf-8").splitlines())
    for line in new_tags:
        tag_additions += 1
        if line not in tag_lines:
            errors.append(f"missing composed R1 tag record: {line}")

    scripts_dir = ROOT / "scripts"
    sys.path.insert(0, str(scripts_dir))
    try:
        from functions import get_new_tags, get_tags

        project_path = f"{ROOT.as_posix()}/"
        active_tags = get_tags(project_path)
        unassigned_tags = get_new_tags(project_path, active_tags)
        if unassigned_tags:
            errors.append(
                f"{len(unassigned_tags)} live labels lack permanent Stacks tags"
            )
        tag_codes = [row[0] for row in active_tags]
        tag_labels = [row[1] for row in active_tags]
        if len(set(tag_codes)) != len(tag_codes):
            errors.append("active Stacks tag codes are not unique")
        if len(set(tag_labels)) != len(tag_labels):
            errors.append("active Stacks tag labels are not unique")
    except (ImportError, OSError, IndexError, ValueError) as exc:
        active_tags = []
        errors.append(f"could not validate permanent Stacks tags: {exc}")

    expected_stable_ids = composition_registry.get("registered_stable_ids")
    if len(registered_ids) != expected_stable_ids:
        errors.append(
            f"expected {expected_stable_ids} registered stable IDs, "
            f"found {len(registered_ids)}"
        )
    if len(set(registered_ids)) != len(registered_ids):
        errors.append("registered stable IDs are not unique")

    expected_v2_operations = composition_state.get("total_v2_operations")
    if v2_operations != expected_v2_operations:
        errors.append(
            f"expected {expected_v2_operations} exact v2 operations, "
            f"found {v2_operations}"
        )
    expected_v1_replacements = composition_state.get("r1_r3_replacements")
    if v1_replacements != expected_v1_replacements:
        errors.append(
            f"expected {expected_v1_replacements} R1-R3 replacements, "
            f"found {v1_replacements}"
        )
    expected_tag_additions = composition_state.get("r1_tag_additions")
    if tag_additions != expected_tag_additions:
        errors.append(
            f"expected {expected_tag_additions} R1 tag additions, "
            f"found {tag_additions}"
        )

    new_overlays = composition.get("new_overlays")
    if not isinstance(new_overlays, list):
        errors.append("composition receipt lacks a new-overlay inventory")
        new_overlays = []
    new_operation_total = 0
    for overlay in new_overlays:
        if not isinstance(overlay, dict) or not isinstance(overlay.get("id"), str):
            errors.append("composition receipt contains an invalid new-overlay entry")
            continue
        overlay_id = overlay["id"]
        entry = entry_by_id.get(overlay_id)
        if entry is None:
            errors.append(f"composition overlay is not registered: {overlay_id}")
            continue
        raw_ids = entry.get("stable_ids", [])
        ids = raw_ids if isinstance(raw_ids, list) else raw_ids.split()
        if len(ids) != overlay.get("stable_ids"):
            errors.append(f"stable-ID count binding mismatch for {overlay_id}")
        operation_count = overlay_operation_counts.get(overlay_id)
        if operation_count != overlay.get("operations"):
            errors.append(f"operation-count binding mismatch for {overlay_id}")
        if isinstance(operation_count, int):
            new_operation_total += operation_count

        manifest_sha = str(entry.get("manifest_sha256", "")).upper()
        if manifest_sha != str(overlay.get("manifest_sha256", "")).upper():
            errors.append(f"composition manifest binding mismatch for {overlay_id}")

        directory = candidate_dir(overlay_id)
        overlay_rows = read_jsonl(directory / "source-map.jsonl")
        overlay_payloads = sorted(
            {
                row.get("payload")
                for row in overlay_rows
                if isinstance(row.get("payload"), str)
            }
        )
        if len(overlay_payloads) != 1:
            errors.append(
                f"composition receipt requires one bound payload for {overlay_id}, "
                f"found {len(overlay_payloads)}"
            )
        else:
            payload = (directory / overlay_payloads[0]).resolve()
            try:
                payload.relative_to(directory.resolve())
                payload_relative = payload.relative_to(ROOT).as_posix()
            except ValueError:
                errors.append(f"composition payload escapes candidate for {overlay_id}")
            else:
                require_clean_path(payload_relative, errors)
                payload_bytes = committed_bytes(
                    "HEAD", payload_relative, errors, "payload"
                )
                if payload_bytes is not None and sha256_bytes(payload_bytes) != str(
                    overlay.get("payload_sha256", "")
                ).upper():
                    errors.append(f"composition payload binding mismatch for {overlay_id}")

        review_value = entry.get("review_receipt")
        if isinstance(review_value, str):
            review_relative = (Path("ai-integrated") / review_value).as_posix()
            review_bytes = committed_bytes("HEAD", review_relative, errors, "review")
            if review_bytes is not None and sha256_bytes(review_bytes) != str(
                overlay.get("review_receipt_sha256", "")
            ).upper():
                errors.append(f"composition review binding mismatch for {overlay_id}")

        materialized = overlay.get("materialized_commit")
        if not isinstance(materialized, str) or not SHA1_RE.fullmatch(materialized):
            errors.append(f"invalid materialized-commit identity for {overlay_id}")

    if new_operation_total != composition_state.get("new_operations"):
        errors.append(
            "new-overlay operation total does not match the composition receipt: "
            f"{new_operation_total} != {composition_state.get('new_operations')}"
        )

    # Recompute the authority-bound cumulative projection. This is stronger
    # than searching for replacement snippets in the live source: it checks
    # exact byte intervals, rejects cross-round overlap, reconstructs each
    # standalone payload, and proves the committed blob is the final result.
    projection_rounds: list[int] = []
    for overlay in new_overlays:
        overlay_id = overlay.get("id") if isinstance(overlay, dict) else None
        match = re.fullmatch(r"stacks-errata-a04446e-r([1-9][0-9]*)", overlay_id or "")
        if match is None:
            errors.append(f"cannot derive projection round from overlay: {overlay_id!r}")
        else:
            projection_rounds.append(int(match.group(1)))
    if projection_rounds != sorted(set(projection_rounds)) or not projection_rounds:
        errors.append("new overlay rounds are empty, duplicated, or out of registry order")
    else:
        projection_command = [
            sys.executable,
            str(ROOT / "tools/verify_overlay_projection.py"),
            *(str(round_number) for round_number in projection_rounds),
            "--check-current",
        ]
        projection_run = subprocess.run(
            projection_command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if projection_run.returncode != 0:
            detail = projection_run.stderr.strip() or projection_run.stdout.strip()
            errors.append(f"authority-bound projection verifier failed: {detail}")
        else:
            try:
                projection_report = json.loads(projection_run.stdout)
            except json.JSONDecodeError as exc:
                errors.append(f"projection verifier returned invalid JSON: {exc}")
            else:
                if projection_report.get("status") != "PASS":
                    errors.append("projection verifier did not report PASS")
                if projection_report.get("rounds") != projection_rounds:
                    errors.append("projection verifier round inventory mismatch")
                if projection_report.get("operations") != new_operation_total:
                    errors.append("projection verifier operation count mismatch")
                projection_sources = projection_report.get("sources")
                if not isinstance(projection_sources, dict):
                    errors.append("projection verifier lacks a source inventory")
                else:
                    for relative, evidence in composition_state.get(
                        "affected_sources", {}
                    ).items():
                        observed = projection_sources.get(relative)
                        if not isinstance(observed, dict):
                            errors.append(
                                f"projection verifier omits affected source: {relative}"
                            )
                            continue
                        for key in (
                            "authority_bytes",
                            "authority_sha256",
                            "projection_bytes",
                            "projection_sha256",
                            "projection_git_blob",
                        ):
                            expected = evidence.get(key)
                            actual = observed.get(key)
                            if isinstance(expected, str):
                                expected = expected.upper()
                                actual = actual.upper() if isinstance(actual, str) else actual
                            if actual != expected:
                                errors.append(
                                    f"projection verifier binding mismatch for "
                                    f"{relative}/{key}"
                                )

    injectives = (ROOT / "injectives.tex").read_text(encoding="utf-8")
    corrected = r"$S_Y = \{\phi \in \Mor(U,X) : \phi\text{ factors through }Y\}$."
    malformed = r"$S_Y = \{\phi \in \Mor(U,X) : \phi)\text{ factors through }Y\}$."
    if corrected not in injectives or malformed in injectives:
        errors.append("independent injectives.tex parenthesis correction is absent")

    for relative in (
        "ai-integrated/registry/leases.json",
        "ai-integrated/registry/locales.json",
        "ai-integrated/registry/overlays.json",
        "ai-integrated/registry/releases.json",
        "ai-integrated/upstream/stacks.lock.json",
        COMPOSITION_RECEIPT.as_posix(),
        R18_R19_RELEASE_RECEIPT.as_posix(),
        "validation/unification-release-2026-08-25.json",
    ):
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {relative}: {exc}")

    require_clean_path(COMPOSITION_RECEIPT.as_posix(), errors)
    composition_bytes = committed_bytes(
        "HEAD", COMPOSITION_RECEIPT.as_posix(), errors, "composition receipt"
    )
    composition_sha = sha256_bytes(composition_bytes) if composition_bytes else ""

    required_build_stems = composition.get("required_build_stems")
    if (
        not isinstance(required_build_stems, list)
        or not required_build_stems
        or not all(isinstance(stem, str) and stem for stem in required_build_stems)
        or len(set(required_build_stems)) != len(required_build_stems)
    ):
        errors.append("composition receipt has an invalid required-build-stem inventory")
        required_build_stems = []

    affected_sources = composition_state.get("affected_sources")
    if not isinstance(affected_sources, dict) or "derived.tex" not in affected_sources:
        errors.append("composition receipt lacks the derived.tex projection")
        affected_sources = {}
    changed_paths_result = git(
        "diff",
        "--name-only",
        "--diff-filter=ACMRTUXB",
        f"{registry_import_commit}..{composition_source_commit}",
    ) if registry_import_commit is not None and composition_source_commit is not None else None
    changed_paths = (
        tuple(path for path in changed_paths_result.stdout.splitlines() if path)
        if changed_paths_result is not None and changed_paths_result.returncode == 0
        else ()
    )
    if tuple(sorted(changed_paths)) != tuple(sorted(affected_sources)):
        errors.append(
            "composition source changed-path inventory mismatch: "
            f"expected {sorted(affected_sources)}, found {sorted(changed_paths)}"
        )
    affected_stems: list[str] = []
    for relative, evidence in affected_sources.items():
        if not isinstance(relative, str) or not isinstance(evidence, dict):
            errors.append("composition receipt contains an invalid affected source")
            continue
        relative_path = Path(relative)
        if relative_path.is_absolute() or len(relative_path.parts) != 1:
            errors.append(f"affected source is not a root path: {relative!r}")
            continue
        affected_stems.append(relative_path.stem)
        require_clean_path(relative, errors)
        head_bytes = committed_bytes("HEAD", relative, errors, "composed projection")
        head_blob = commit_blob("HEAD", relative, errors, "HEAD projection")
        projection_sha = evidence.get("projection_sha256")
        projection_blob = evidence.get("projection_git_blob")
        projection_bytes = evidence.get("projection_bytes")
        authority_sha = evidence.get("authority_sha256")
        authority_blob_expected = evidence.get("authority_git_blob")
        authority_size = evidence.get("authority_bytes")
        if (
            not isinstance(projection_sha, str)
            or not SHA256_RE.fullmatch(projection_sha)
            or not isinstance(projection_blob, str)
            or not SHA1_RE.fullmatch(projection_blob)
            or type(projection_bytes) is not int
            or projection_bytes < 1
            or not isinstance(authority_sha, str)
            or not SHA256_RE.fullmatch(authority_sha)
            or not isinstance(authority_blob_expected, str)
            or not SHA1_RE.fullmatch(authority_blob_expected)
            or type(authority_size) is not int
            or authority_size < 1
        ):
            errors.append(f"invalid projection identity for {relative}")
        elif head_bytes is not None and (
            len(head_bytes) != projection_bytes
            or sha256_bytes(head_bytes) != projection_sha.upper()
            or git_blob_sha1(head_bytes) != projection_blob.lower()
            or head_blob != projection_blob.lower()
        ):
            errors.append(f"committed projection identity mismatch for {relative}")
        if evidence.get("committed_matches_projection") is not True:
            errors.append(f"composition receipt does not close {relative}")

        authority_bytes = committed_bytes(UPSTREAM, relative, errors, "authority")
        authority_blob = commit_blob(UPSTREAM, relative, errors, "authority")
        if authority_bytes is not None and (
            len(authority_bytes) != authority_size
            or sha256_bytes(authority_bytes)
            != authority_sha.upper()
            or authority_blob != authority_blob_expected.lower()
        ):
            errors.append(f"pinned authority identity mismatch for {relative}")

        source_blob = commit_blob(
            composition_source_commit,
            relative,
            errors,
            "composition source",
        )
        if isinstance(projection_blob, str) and source_blob != projection_blob.lower():
            errors.append(f"composition source projection mismatch for {relative}")
        if materialization_tip is not None:
            materialized_blob = git_optional(
                "rev-parse", f"{materialization_tip}:{relative}"
            )
            if (
                materialized_blob is not None
                and isinstance(projection_blob, str)
                and materialized_blob != projection_blob.lower()
            ):
                errors.append(f"materialization projection mismatch for {relative}")

    projection_verifier = composition.get("projection_verifier")
    if (
        not isinstance(projection_verifier, dict)
        or projection_verifier.get("status") != "PASS"
        or not isinstance(projection_verifier.get("path"), str)
        or not isinstance(projection_verifier.get("command"), str)
        or not projection_verifier.get("command")
    ):
        errors.append("composition receipt lacks a passing projection-verifier binding")

    if any(stem not in required_build_stems for stem in affected_stems):
        errors.append("required build stems omit an affected source")

    if build_receipt.get("schema") != "unofficial-ai-integrated-stacks-fixed-point-build/v1":
        errors.append("fixed-point build receipt schema is invalid")
    if build_receipt.get("status") != "PASS":
        errors.append("fixed-point build receipt is not PASS")

    build_source = build_receipt.get("source")
    if not isinstance(build_source, dict):
        errors.append("fixed-point build receipt lacks source identity")
        build_source = {}
    build_source_commit = require_commit(
        build_source.get("commit"), "fixed-point build source", errors
    )
    if build_source_commit is not None:
        require_ancestor(
            composition_source_commit,
            build_source_commit,
            "composition-source-to-build-source",
            errors,
        )
        require_ancestor(
            build_source_commit, "HEAD", "build-source-to-HEAD", errors
        )
        require_linear_suffix(
            composition_source_commit,
            build_source_commit,
            "composition-to-build-source suffix",
            errors,
        )
        require_linear_suffix(
            build_source_commit,
            "HEAD",
            "build-source publication suffix",
            errors,
        )
        tree_result = git("rev-parse", f"{build_source_commit}^{{tree}}")
        if tree_result.returncode != 0 or tree_result.stdout.strip() != build_source.get(
            "tree"
        ):
            errors.append("fixed-point build source tree identity mismatch")
        for relative, evidence in affected_sources.items():
            blob = commit_blob(
                build_source_commit, relative, errors, "fixed-point build source"
            )
            expected_blob = evidence.get("projection_git_blob")
            if isinstance(expected_blob, str) and blob != expected_blob.lower():
                errors.append(f"build source projection mismatch for {relative}")
        build_registry_blob = commit_blob(
            build_source_commit,
            overlays_relative,
            errors,
            "fixed-point build registry",
        )
        if build_registry_blob != expected_registry_blob:
            errors.append("fixed-point build registry blob mismatch")

    builder = build_receipt.get("builder")
    if not isinstance(builder, dict) or builder.get("path") != "tools/build_fixed_point.py":
        errors.append("fixed-point build receipt lacks the canonical builder binding")
    elif build_source_commit is not None:
        builder_blob = commit_blob(
            build_source_commit,
            "tools/build_fixed_point.py",
            errors,
            "fixed-point builder",
        )
        builder_bytes = committed_bytes(
            build_source_commit,
            "tools/build_fixed_point.py",
            errors,
            "fixed-point builder",
        )
        if builder.get("git_blob") != builder_blob:
            errors.append("fixed-point builder Git-blob binding mismatch")
        if (
            builder_bytes is None
            or builder.get("sha256") != sha256_bytes(builder_bytes)
        ):
            errors.append("fixed-point builder SHA-256 binding mismatch")

    receipt_composition = build_receipt.get("composition")
    if not isinstance(receipt_composition, dict):
        errors.append("fixed-point build receipt lacks composition binding")
        receipt_composition = {}
    expected_build_binding = {
        "schema": "unofficial-ai-integrated-stacks-composition/v2",
        "receipt": COMPOSITION_RECEIPT.as_posix(),
        "receipt_git_blob": (
            git_blob_sha1(composition_bytes) if composition_bytes is not None else None
        ),
        "receipt_sha256": composition_sha,
        "authority_commit": UPSTREAM,
        "authority_tree": composition_authority.get("tree"),
        "previous_registry_commit": previous_registry,
        "previous_last_admitted_overlay": previous_last,
        "previous_derived_git_blob": previous_derived_blob,
        "composition_mode": composition_state.get("mode"),
        "materialization_tip": materialization_tip,
        "composition_source_commit": composition_source_commit,
        "composition_source_tree": composition_source_tree,
        "registry_cutoff_commit": cutoff_commit,
        "registry_import_commit": registry_import_commit,
        "registry_import_tree": registry_import_tree,
        "registry_overlays_path": overlays_relative,
        "registry_overlays_git_blob": (
            git_blob_sha1(registry_bytes) if registry_bytes is not None else None
        ),
        "registry_overlays_sha256": str(
            composition_registry.get("overlays_sha256", "")
        ).upper(),
        "registered_overlays": len(entries),
        "registered_stable_ids": len(registered_ids),
        "last_admitted_overlay": composition_registry.get("last_admitted_overlay"),
        "new_overlay_ids": [entry.get("id") for entry in registry_suffix],
        "new_overlay_materialized_commits": [
            overlay.get("materialized_commit")
            for overlay in new_overlays
            if isinstance(overlay, dict)
        ],
        "required_build_stems": required_build_stems,
        "affected_source_stems": affected_stems,
        "affected_source_identities": affected_sources,
    }
    for key, expected in expected_build_binding.items():
        if receipt_composition.get(key) != expected:
            errors.append(
                f"fixed-point build composition binding mismatch for {key}: "
                f"{receipt_composition.get(key)!r} != {expected!r}"
            )

    artifacts = build_receipt.get("artifacts")
    if not isinstance(artifacts, list):
        errors.append("fixed-point build receipt lacks an artifact inventory")
        artifacts = []
    artifact_stems: list[str] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict) or not isinstance(artifact.get("stem"), str):
            errors.append("fixed-point build receipt contains an invalid artifact")
            continue
        artifact_stems.append(artifact["stem"])
        if not isinstance(artifact.get("pages"), int) or artifact["pages"] < 1:
            errors.append(f"nonpositive page count for build artifact {artifact['stem']}")
        if not isinstance(artifact.get("bytes"), int) or artifact["bytes"] < 1:
            errors.append(f"nonpositive byte count for build artifact {artifact['stem']}")
        artifact_sha = artifact.get("sha256")
        if not isinstance(artifact_sha, str) or not SHA256_RE.fullmatch(artifact_sha):
            errors.append(f"invalid SHA-256 for build artifact {artifact['stem']}")
        diagnostics = artifact.get("diagnostics")
        diagnostic_keys = {
            "fatal_markers",
            "missing_glyph_markers",
            "undefined_reference_markers",
            "external_reference_markers",
            "undefined_citation_markers",
            "multiply_defined_markers",
            "rerun_required_markers",
            "destination_warning_markers",
        }
        if not isinstance(diagnostics, dict) or set(diagnostics) != diagnostic_keys:
            errors.append(
                f"incomplete TeX diagnostics for build artifact {artifact['stem']}"
            )
        elif (
            any(
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
                for value in diagnostics.values()
            )
            or any(
                value != 0
                for key, value in diagnostics.items()
                if key != "external_reference_markers"
            )
        ):
            errors.append(f"nonzero TeX diagnostics for build artifact {artifact['stem']}")
    if len(set(artifact_stems)) != len(artifact_stems):
        errors.append("fixed-point build artifact stems are not unique")
    if artifact_stems != required_build_stems:
        errors.append("fixed-point build artifact order or coverage is not the required profile")
    build_state = build_receipt.get("build")
    if not isinstance(build_state, dict):
        errors.append("fixed-point build receipt lacks build state")
        build_state = {}
    if build_state.get("chapter_count") != len(artifacts):
        errors.append("fixed-point chapter count does not match artifact inventory")
    if build_state.get("pdfinfo_readable") != len(artifacts):
        errors.append("fixed-point PDF readability count does not match artifacts")
    sweep = build_state.get("global_fixed_point_sweep")
    if not isinstance(sweep, int) or sweep < 1:
        errors.append("fixed-point build receipt lacks a positive fixed-point sweep")
    receipt_stems = build_state.get("stems")
    if receipt_stems != artifact_stems:
        errors.append("fixed-point build stem list does not match artifact inventory")
    if build_state.get("stem_selection") != "composition_receipt":
        errors.append("fixed-point build did not use the receipt-bound stem profile")
    if build_state.get("strategy") != (
        "sequential-prime-bibtex-global-state-sweeps"
    ):
        errors.append("fixed-point build does not use generated-state convergence")
    if build_state.get("fixed_point_suffixes") != EXPECTED_FIXED_POINT_SUFFIXES:
        errors.append("fixed-point build has the wrong generated-state inventory")
    if build_state.get("worktree_kind") != "linked":
        errors.append("fixed-point build did not run in a linked disposable worktree")
    if build_state.get("primary_worktree_override") is not False:
        errors.append("fixed-point build used or ambiguously recorded a primary override")
    build_diagnostics = build_state.get("diagnostics")
    diagnostic_keys = {
        "fatal_markers",
        "missing_glyph_markers",
        "undefined_reference_markers",
        "external_reference_markers",
        "undefined_citation_markers",
        "multiply_defined_markers",
        "rerun_required_markers",
        "destination_warning_markers",
    }
    if not isinstance(build_diagnostics, dict) or set(build_diagnostics) != diagnostic_keys:
        errors.append("fixed-point build lacks complete aggregate diagnostics")
    elif (
        any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in build_diagnostics.values()
        )
        or any(
            value != 0
            for key, value in build_diagnostics.items()
            if key != "external_reference_markers"
        )
    ):
        errors.append("fixed-point build has nonzero aggregate diagnostics")
    elif artifacts and all(
        isinstance(artifact, dict)
        and isinstance(artifact.get("diagnostics"), dict)
        and set(artifact["diagnostics"]) == diagnostic_keys
        and all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in artifact["diagnostics"].values()
        )
        for artifact in artifacts
    ):
        summed_diagnostics = {
            key: sum(artifact["diagnostics"][key] for artifact in artifacts)
            for key in diagnostic_keys
        }
        if summed_diagnostics != build_diagnostics:
            errors.append("aggregate diagnostics do not equal artifact diagnostics")

    release_receipt = load_json_object(
        ROOT / R18_R19_RELEASE_RECEIPT,
        errors,
        "R18-R19 release receipt",
    ) or {}
    if release_receipt.get("status") != "PUBLICATION_COMPLETE":
        errors.append("R18-R19 release receipt is not publication-complete")
    release_state = release_receipt.get("release")
    if not isinstance(release_state, dict):
        errors.append("R18-R19 release receipt lacks release state")
        release_state = {}
    if release_state.get("repository") != "KokunoYumeto/unofficial-ai-integrated-stacks-project":
        errors.append("R18-R19 release receipt names the wrong repository")
    if release_state.get("default_branch") != "main":
        errors.append("R18-R19 release receipt names the wrong default branch")
    if release_state.get("frozen_registry_cutoff") != cutoff_commit:
        errors.append("R18-R19 release cutoff binding mismatch")
    if release_state.get("registered_overlays") != len(entries):
        errors.append("R18-R19 release overlay-count binding mismatch")
    if release_state.get("registered_stable_ids") != len(registered_ids):
        errors.append("R18-R19 release stable-ID binding mismatch")
    readback = release_receipt.get("public_readback")
    if not isinstance(readback, dict) or readback.get("status") != "PASS":
        errors.append("R18-R19 release receipt lacks passing public readback")
        readback = {}
    readback_commit = require_commit(
        readback.get("commit"), "R18-R19 public readback", errors
    )
    require_ancestor(readback_commit, "HEAD", "R18-R19 readback-to-current", errors)
    if readback_commit != release_state.get("published_content_head"):
        errors.append("R18-R19 readback and published-content heads differ")
    metadata_head = require_commit(
        release_state.get("metadata_head"), "R18-R19 metadata head", errors
    )
    require_ancestor(metadata_head, "HEAD", "R18-R19 metadata-to-current", errors)
    checked_paths = readback.get("checked_paths")
    if not isinstance(checked_paths, list) or not checked_paths:
        errors.append("R18-R19 release receipt lacks checked public paths")
        checked_paths = []
    for row in checked_paths:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            errors.append("R18-R19 release receipt has an invalid readback row")
            continue
        relative = row["path"]
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append(f"R18-R19 readback path escapes repository: {relative}")
            continue
        data = committed_bytes(
            readback_commit or "HEAD", relative, errors, "R18-R19 public readback"
        )
        if data is None:
            continue
        expected_sha = row.get("sha256")
        expected_blob = row.get("git_blob")
        if (
            type(row.get("bytes")) is not int
            or row.get("bytes") != len(data)
            or not isinstance(expected_sha, str)
            or not SHA256_RE.fullmatch(expected_sha)
            or sha256_bytes(data) != expected_sha.upper()
            or not isinstance(expected_blob, str)
            or not SHA1_RE.fullmatch(expected_blob)
            or git_blob_sha1(data) != expected_blob.lower()
        ):
            errors.append(f"R18-R19 public readback identity mismatch: {relative}")
    release_composition = release_receipt.get("composition")
    if not isinstance(release_composition, dict):
        errors.append("R18-R19 release receipt lacks composition state")
        release_composition = {}
    release_comp_receipt = release_composition.get("receipt")
    if isinstance(release_comp_receipt, dict):
        if release_comp_receipt.get("sha256") != composition_sha:
            errors.append("R18-R19 release composition-receipt hash mismatch")
    else:
        errors.append("R18-R19 release receipt lacks composition-receipt identity")
    release_build = release_receipt.get("build")
    if not isinstance(release_build, dict):
        errors.append("R18-R19 release receipt lacks build state")
        release_build = {}
    if release_build.get("receipt_sha256") != sha256_bytes(
        build_receipt_bytes or b""
    ):
        errors.append("R18-R19 release build-receipt hash mismatch")
    if release_build.get("source_commit") != build_source_commit or release_build.get(
        "source_tree"
    ) != build_source.get("tree"):
        errors.append("R18-R19 release build-source identity mismatch")
    if release_build.get("chapters") != len(artifacts):
        errors.append("R18-R19 release chapter-count mismatch")
    if release_build.get("pages") != sum(
        artifact.get("pages", 0) for artifact in artifacts if isinstance(artifact, dict)
    ):
        errors.append("R18-R19 release page-count mismatch")
    if release_build.get("global_fixed_point_sweep") != build_state.get(
        "global_fixed_point_sweep"
    ):
        errors.append("R18-R19 release fixed-point sweep mismatch")
    workflow = release_receipt.get("workflow")
    if (
        not isinstance(workflow, dict)
        or workflow.get("status") != "completed"
        or workflow.get("conclusion") != "success"
        or workflow.get("head_sha") != release_state.get("metadata_head")
    ):
        errors.append("R18-R19 release receipt lacks a passing exact-head workflow record")

    historical_receipt = load_json_object(
        ROOT / "validation/unification-release-2026-08-25.json",
        errors,
        "historical unification release receipt",
    ) or {}
    if historical_receipt.get("status") != "PUBLICATION_COMPLETE":
        errors.append("historical unification release receipt is not publication-complete")
    if historical_receipt.get("public_readback", {}).get("status") != "PASS":
        errors.append("historical release receipt lacks passing public readback")
    if historical_receipt.get("preservation", {}).get("status") != "PUBLIC_READBACK_VERIFIED":
        errors.append("historical preservation assets lack public readback verification")
    if not historical_receipt.get("source_repository", {}).get("archived"):
        errors.append("historical receipt does not record the source provenance archive")

    marker_paths = [ROOT / item for item in PUBLIC_MARKDOWN]
    marker_paths.extend(ROOT.glob("*.tex"))
    for path in marker_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "<<<<<<< " in text or ">>>>>>> " in text:
            errors.append(f"unresolved merge marker: {path.relative_to(ROOT)}")

    validate_links(errors)

    if errors:
        print("Unified repository validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Unified repository validation: PASS")
    print(f"- registered overlays: {len(entries)}")
    print(f"- registered stable IDs: {len(registered_ids)}")
    print(f"- exact v2 operations checked: {v2_operations}")
    print(f"- exact R1-R3 replacements checked: {v1_replacements}")
    print(f"- R1 tag additions checked: {tag_additions}")
    print(f"- active permanent Stacks tags checked: {len(active_tags)}")
    print(f"- fixed-point build receipt: {display_path(build_receipt_path)}")
    print(f"- required build stems covered: {len(required_build_stems)}")
    print(f"- public Markdown documents checked: {len(PUBLIC_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
