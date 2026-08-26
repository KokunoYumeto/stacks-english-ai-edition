#!/usr/bin/env python3
"""Compose one admitted insertion-only overlay into a canonical source.

The admitted candidate remains immutable.  Its frozen composition contract is
first replayed against the recorded base commit.  The insertion is then rebased
to ``--base-revision`` through the contract's unique unchanged byte context.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(detail or f"git {' '.join(args)} failed")
    return completed.stdout


def git_text(*args: str, input_bytes: bytes | None = None) -> str:
    return git(*args, input_bytes=input_bytes).decode("ascii").strip()


def committed_bytes(revision: str, path: str) -> bytes:
    return git("show", f"{revision}:{path}")


def git_blob_id(data: bytes) -> str:
    return git_text("hash-object", "--stdin", input_bytes=data)


def filtered_git_blob_id(data: bytes, path: str) -> str:
    return git_text("hash-object", f"--path={path}", "--stdin", input_bytes=data)


def read_single_jsonl(data: bytes, label: str) -> dict:
    rows = [
        json.loads(line)
        for line in data.decode("utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError(f"expected exactly one JSON object in {label}")
    return rows[0]


def read_jsonl(data: bytes, label: str) -> list[dict]:
    rows = [
        json.loads(line)
        for line in data.decode("utf-8").splitlines()
        if line.strip()
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"non-object JSONL row in {label}")
    return rows


def require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"invalid SHA-256 identity for {label}")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"invalid SHA-256 identity for {label}") from exc
    return value.upper()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overlay-id", required=True)
    parser.add_argument(
        "--base-revision",
        default="HEAD",
        help="committed canonical preimage to which the insertion is rebased",
    )
    parser.add_argument(
        "--check-revision",
        help="require the composed bytes to equal this committed revision",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="atomically replace the affected root source after all checks pass",
    )
    args = parser.parse_args()
    if args.write and args.check_revision:
        parser.error("--write and --check-revision are mutually exclusive")

    registry_relative = "ai-integrated/registry/overlays.json"
    registry = json.loads(committed_bytes("HEAD", registry_relative).decode("utf-8"))
    matches = [
        entry
        for entry in registry.get("registered_entries", [])
        if isinstance(entry, dict) and entry.get("id") == args.overlay_id
    ]
    if len(matches) != 1:
        raise ValueError(f"overlay is not uniquely registered: {args.overlay_id}")
    entry = matches[0]
    namespace = entry.get("namespace")
    if not isinstance(namespace, str) or not namespace:
        raise ValueError("registered overlay lacks a namespace")
    namespace_path = Path(namespace)
    if namespace_path.is_absolute() or ".." in namespace_path.parts:
        raise ValueError("registered namespace escapes the candidate root")
    directory_relative = (Path("ai-integrated/candidates") / namespace_path).as_posix()
    directory = ROOT / directory_relative

    manifest_relative = f"{directory_relative}/candidate.manifest.json"
    manifest_bytes = committed_bytes("HEAD", manifest_relative)
    manifest_sha = sha256(manifest_bytes)
    if manifest_sha != require_sha256(entry.get("manifest_sha256"), "registry manifest"):
        raise ValueError("registry/candidate manifest hash mismatch")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if manifest.get("candidate_id") != args.overlay_id:
        raise ValueError("manifest candidate identity mismatch")
    if manifest.get("schema") != "mathematics-commons-stacks-candidate-manifest/v1":
        raise ValueError("unexpected candidate manifest schema")
    build_hashes: dict[str, str] = {}
    for item in manifest.get("builds", []):
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ValueError("manifest contains an invalid build binding")
        item_path = item["path"]
        if item_path in build_hashes:
            raise ValueError(f"manifest repeats a build binding: {item_path}")
        build_hashes[item_path] = require_sha256(item.get("sha256"), item_path)

    source_map_relative = f"{directory_relative}/source-map.jsonl"
    source_map_bytes = committed_bytes("HEAD", source_map_relative)
    source_map_binding = manifest.get("source_map", {})
    if source_map_binding.get("path") != "source-map.jsonl" or sha256(
        source_map_bytes
    ) != require_sha256(source_map_binding.get("sha256"), "source map"):
        raise ValueError("manifest/source-map binding mismatch")
    source_rows = read_jsonl(source_map_bytes, source_map_relative)
    stable_ids = entry.get("stable_ids")
    if isinstance(stable_ids, str):
        stable_ids = stable_ids.split()
    if [row.get("unit_id") for row in source_rows] != stable_ids:
        raise ValueError("registry/source-map stable-ID mismatch")

    review_relative = entry.get("review_receipt")
    if not isinstance(review_relative, str):
        raise ValueError("registry lacks an independent-review path")
    review_path = (ROOT / "ai-integrated" / review_relative).resolve()
    try:
        review_candidate_relative = review_path.relative_to(directory.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError("independent-review path escapes the candidate") from exc
    review_repository_relative = review_path.relative_to(ROOT).as_posix()
    review_bytes = committed_bytes("HEAD", review_repository_relative)
    if build_hashes.get(review_candidate_relative) != sha256(review_bytes):
        raise ValueError("manifest/independent-review binding mismatch")
    review = json.loads(review_bytes.decode("utf-8"))
    outcome = review.get("outcome")
    if review.get("candidate_id") != args.overlay_id or not (
        review.get("passed") is True
        or isinstance(outcome, dict) and outcome.get("passed") is True
    ):
        raise ValueError("independent replay is not passing")

    composition_relative = f"{directory_relative}/composition.jsonl"
    composition_bytes = committed_bytes("HEAD", composition_relative)
    if build_hashes.get("composition.jsonl") != sha256(composition_bytes):
        raise ValueError("manifest/composition binding mismatch")
    operation = read_single_jsonl(composition_bytes, composition_relative)
    if (
        operation.get("schema")
        != "mathematics-commons-stacks-composition-operation/v1"
        or operation.get("operation") != "insert_bytes"
        or operation.get("mode") != "insertion_only"
    ):
        raise ValueError("candidate is not an insertion-only composition contract")

    payload_record = operation.get("payload")
    if not isinstance(payload_record, dict):
        raise ValueError("composition contract lacks a payload")
    payload_relative = payload_record.get("path")
    if not isinstance(payload_relative, str):
        raise ValueError("composition payload path is invalid")
    payload_path = (directory / payload_relative).resolve()
    try:
        payload_path.relative_to(directory.resolve())
    except ValueError as exc:
        raise ValueError("composition payload escapes the candidate") from exc
    payload_repository_relative = payload_path.relative_to(ROOT).as_posix()
    payload = committed_bytes("HEAD", payload_repository_relative)
    payload_sha = sha256(payload)
    if (
        len(payload) != payload_record.get("bytes")
        or payload_sha != require_sha256(payload_record.get("sha256"), "payload")
        or build_hashes.get(payload_relative) != payload_sha
    ):
        raise ValueError("payload identity mismatch")

    target = operation.get("target")
    insertion = operation.get("insertion")
    constraints = operation.get("constraints")
    if not all(isinstance(item, dict) for item in (target, insertion, constraints)):
        raise ValueError("composition contract is incomplete")
    assert isinstance(target, dict)
    assert isinstance(insertion, dict)
    assert isinstance(constraints, dict)
    if (
        constraints.get("existing_target_bytes_changed") != 0
        or constraints.get("delete_bytes") != 0
        or constraints.get("replace_bytes") != 0
        or constraints.get("insert_payload_once") is not True
    ):
        raise ValueError("composition contract is not strictly insertion-only")

    source = target.get("path")
    frozen_commit = target.get("commit")
    if not isinstance(source, str) or Path(source).is_absolute() or ".." in Path(source).parts:
        raise ValueError("composition target path is invalid")
    if not isinstance(frozen_commit, str):
        raise ValueError("composition target commit is invalid")
    frozen_tree = git_text("rev-parse", f"{frozen_commit}^{{tree}}")
    if frozen_tree != target.get("tree"):
        raise ValueError("frozen target tree mismatch")
    frozen = committed_bytes(frozen_commit, source)
    frozen_blob = git_text("rev-parse", f"{frozen_commit}:{source}")
    if (
        frozen_blob != target.get("blob")
        or len(frozen) != target.get("bytes")
        or sha256(frozen) != require_sha256(target.get("preimage_sha256"), "frozen target")
    ):
        raise ValueError("frozen target preimage mismatch")

    context_start = insertion.get("context_start_byte")
    context_end = insertion.get("context_end_byte_exclusive")
    offset = insertion.get("byte_offset")
    before_count = insertion.get("before_context_bytes")
    after_count = insertion.get("after_context_bytes")
    if not all(type(value) is int for value in (context_start, context_end, offset, before_count, after_count)):
        raise ValueError("composition context offsets are invalid")
    assert isinstance(context_start, int)
    assert isinstance(context_end, int)
    assert isinstance(offset, int)
    assert isinstance(before_count, int)
    assert isinstance(after_count, int)
    context = frozen[context_start:context_end]
    before_context = frozen[context_start:offset]
    after_context = frozen[offset:context_end]
    if (
        len(context) != insertion.get("context_bytes")
        or len(before_context) != before_count
        or len(after_context) != after_count
        or before_count + after_count != len(context)
        or sha256(context) != require_sha256(insertion.get("context_sha256"), "context")
        or sha256(before_context)
        != require_sha256(insertion.get("before_context_sha256"), "before context")
        or sha256(after_context)
        != require_sha256(insertion.get("after_context_sha256"), "after context")
    ):
        raise ValueError("frozen composition context mismatch")
    if (
        insertion.get("required_anchor_occurrences") != 1
        or frozen.count(context) != 1
    ):
        raise ValueError("frozen context is not unique")

    frozen_projection = frozen[:offset] + payload + frozen[offset:]
    if (
        len(frozen_projection) != target.get("postimage_bytes")
        or sha256(frozen_projection)
        != require_sha256(target.get("postimage_sha256"), "frozen postimage")
    ):
        raise ValueError("frozen composition postimage mismatch")

    base = committed_bytes(args.base_revision, source)
    base_blob = git_text("rev-parse", f"{args.base_revision}:{source}")
    if base.count(context) != 1:
        raise ValueError("canonical base does not contain exactly one frozen context")
    if base.count(payload) != 0:
        raise ValueError("payload is already present in the canonical base")
    label = payload_record.get("proposed_label")
    if not isinstance(label, str) or not label:
        raise ValueError("payload lacks a proposed label")
    label_bytes = label.encode("utf-8")
    if base.count(label_bytes) != 0:
        raise ValueError("proposed label is already present in the canonical base")
    rebased_context_start = base.index(context)
    rebased_offset = rebased_context_start + before_count
    if base[rebased_context_start:rebased_offset] != before_context or base[
        rebased_offset : rebased_context_start + len(context)
    ] != after_context:
        raise ValueError("rebased context split mismatch")
    projection = base[:rebased_offset] + payload + base[rebased_offset:]
    if projection.count(payload) != 1 or projection.count(label_bytes) != 1:
        raise ValueError("composed payload or label is not unique")
    if projection[:rebased_offset] != base[:rebased_offset] or projection[
        rebased_offset + len(payload) :
    ] != base[rebased_offset:]:
        raise ValueError("composition changed bytes outside the insertion")

    source_path = ROOT / source
    worktree_before: bytes | None = None
    if args.write:
        worktree_before = source_path.read_bytes()
        if filtered_git_blob_id(worktree_before, source) != base_blob:
            raise ValueError(
                f"worktree source differs from base revision {args.base_revision}: {source}"
            )
        source_mode = stat.S_IMODE(source_path.stat().st_mode)
        if filtered_git_blob_id(projection, source) != git_blob_id(projection):
            raise ValueError(
                f"repository clean filters would transform composed bytes: {source}"
            )
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=source_path.parent,
                prefix=f".{source_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(projection)
                handle.flush()
                os.fsync(handle.fileno())
                temporary = Path(handle.name)
            os.replace(temporary, source_path)
            os.chmod(source_path, source_mode)
            temporary = None
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        if source_path.read_bytes() != projection:
            raise ValueError("post-write byte mismatch")
    elif args.check_revision:
        checked = committed_bytes(args.check_revision, source)
        if checked != projection:
            raise ValueError("checked revision is not the composed projection")

    report = {
        "schema": "unofficial-ai-integrated-stacks-registered-insertion-composition/v1",
        "status": "PASS",
        "overlay_id": args.overlay_id,
        "operation_id": operation.get("operation_id"),
        "manifest_sha256": manifest_sha,
        "independent_replay_sha256": sha256(review_bytes),
        "composition_sha256": sha256(composition_bytes),
        "base_revision": args.base_revision,
        "check_revision": args.check_revision,
        "write_requested": args.write,
        "source": source,
        "frozen_contract": {
            "commit": frozen_commit,
            "tree": frozen_tree,
            "path": source,
            "blob": frozen_blob,
            "bytes": len(frozen),
            "sha256": sha256(frozen),
            "postimage_bytes": len(frozen_projection),
            "postimage_sha256": sha256(frozen_projection),
        },
        "canonical_composition": {
            "before_blob": base_blob,
            "before_bytes": len(base),
            "before_sha256": sha256(base),
            "context_occurrences": base.count(context),
            "context_bytes": len(context),
            "context_sha256": sha256(context),
            "rebased_byte_offset": rebased_offset,
            "payload_bytes": len(payload),
            "payload_sha256": payload_sha,
            "composed_blob": git_blob_id(projection),
            "composed_bytes": len(projection),
            "composed_sha256": sha256(projection),
            "payload_occurrences_after": projection.count(payload),
            "label_occurrences_after": projection.count(label_bytes),
            "prefix_unchanged": True,
            "suffix_unchanged": True,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"Registered insertion composition: FAIL\n- {exc}", file=os.sys.stderr)
        raise SystemExit(1)
