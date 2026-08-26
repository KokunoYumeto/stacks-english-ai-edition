#!/usr/bin/env python3
"""Compose admitted v2 errata overlays into the checked-out source tree.

The existing source must be the exact cumulative projection of
``--existing-rounds``.  The target rounds must extend that sequence in registry
order.  Candidate payloads are used only as independent replay checks: output
is reconstructed from the pinned authority bytes and the manifest-bound
operations, never copied from a payload wholesale.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from verify_overlay_projection import (
    ROOT,
    apply as apply_operations,
    candidate_dir,
    git_blob,
    git_blob_id,
    read_jsonl,
    sha256,
)


def filtered_git_blob_id(data: bytes, source: str) -> str:
    """Return the blob Git would stage for *source* from these worktree bytes."""
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "hash-object",
            f"--path={source}",
            "--stdin",
        ],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise ValueError(completed.stderr.decode("utf-8", errors="replace").strip())
    return completed.stdout.decode("ascii").strip()


def byte_offsets(lines: list[bytes]) -> list[int]:
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    return offsets


def rebase_operations(
    authority: bytes, current: bytes, operations: list[dict]
) -> list[dict]:
    """Map authority-bound operations through unchanged line blocks in current."""
    authority_lines = authority.splitlines(keepends=True)
    current_lines = current.splitlines(keepends=True)
    authority_offsets = byte_offsets(authority_lines)
    current_offsets = byte_offsets(current_lines)
    matcher = difflib.SequenceMatcher(
        None, authority_lines, current_lines, autojunk=False
    )
    regions: list[tuple[int, int, int, int]] = []
    for block in matcher.get_matching_blocks():
        if not block.size:
            continue
        authority_start = authority_offsets[block.a]
        authority_end = authority_offsets[block.a + block.size]
        current_start = current_offsets[block.b]
        current_end = current_offsets[block.b + block.size]
        if authority[authority_start:authority_end] != current[current_start:current_end]:
            raise ValueError("line matcher returned a non-identical byte region")
        regions.append((authority_start, authority_end, current_start, current_end))

    rebased: list[dict] = []
    for operation in operations:
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        matches = [
            region
            for region in regions
            if region[0] <= start and end <= region[1]
        ]
        if len(matches) != 1:
            raise ValueError(
                "operation does not map through exactly one unchanged region: "
                f"{operation['operation_id']}"
            )
        authority_start, _, current_start, _ = matches[0]
        mapped = dict(operation)
        mapped["authority_start_byte"] = start
        mapped["authority_end_byte_exclusive"] = end
        mapped["start_byte"] = current_start + (start - authority_start)
        mapped["end_byte_exclusive"] = current_start + (end - authority_start)
        old = operation["old_text"].encode("utf-8")
        if current[mapped["start_byte"] : mapped["end_byte_exclusive"]] != old:
            raise ValueError(f"rebased preimage mismatch: {operation['operation_id']}")
        rebased.append(mapped)

    ordered = sorted(rebased, key=lambda item: item["start_byte"])
    for left, right in zip(ordered, ordered[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise ValueError(
                "rebased operation overlap: "
                f"{left['operation_id']} / {right['operation_id']}"
            )
    return rebased


def collect_projection(rounds: list[int]) -> tuple[dict[str, bytes], dict[str, list[dict]], list[dict]]:
    registry = json.loads(
        (ROOT / "ai-integrated/registry/overlays.json").read_text(encoding="utf-8")
    )
    entries = registry["registered_entries"]
    registered = {entry["id"]: entry for entry in entries}
    registry_ids = [entry["id"] for entry in entries]

    authorities: dict[str, bytes] = {}
    grouped: dict[str, list[dict]] = defaultdict(list)
    round_reports: list[dict] = []
    prior_position = -1

    for round_number in rounds:
        overlay_id = f"stacks-errata-a04446e-r{round_number}"
        entry = registered.get(overlay_id)
        if entry is None:
            raise ValueError(f"overlay is not registered: {overlay_id}")
        position = registry_ids.index(overlay_id)
        if position <= prior_position:
            raise ValueError(f"overlay is out of registry order: {overlay_id}")
        prior_position = position

        directory = candidate_dir(round_number)
        manifest = directory / "candidate.manifest.json"
        manifest_hash = sha256(manifest.read_bytes())
        if manifest_hash != entry["manifest_sha256"].upper():
            raise ValueError(f"registry manifest mismatch: {overlay_id}")

        rows = read_jsonl(directory / "source-map.jsonl")
        stable_ids = entry["stable_ids"]
        if isinstance(stable_ids, str):
            stable_ids = stable_ids.split()
        if [row["unit_id"] for row in rows] != stable_ids:
            raise ValueError(f"registry/source-map ID mismatch: {overlay_id}")

        per_source: dict[str, list[dict]] = defaultdict(list)
        payload_paths: dict[str, str] = {}
        for row in rows:
            source = row["source"]
            payload = row["payload"]
            if source in payload_paths and payload_paths[source] != payload:
                raise ValueError(f"multiple payload paths for {overlay_id}/{source}")
            payload_paths[source] = payload

            authority = (directory / row["authority"]).read_bytes()
            if sha256(authority) != row["authority_sha256"].upper():
                raise ValueError(f"authority hash mismatch: {overlay_id}/{source}")
            if source in authorities and authorities[source] != authority:
                raise ValueError(f"overlays use different authority bytes: {source}")
            authorities[source] = authority

            for operation in row.get("operations", []):
                enriched = dict(operation)
                enriched["round"] = round_number
                grouped[source].append(enriched)
                per_source[source].append(enriched)

        payload_reports: dict[str, dict] = {}
        for source, operations in per_source.items():
            replay = apply_operations(authorities[source], operations)
            payload = (directory / payload_paths[source]).read_bytes()
            if replay != payload:
                raise ValueError(f"standalone payload mismatch: {overlay_id}/{source}")
            payload_reports[source] = {
                "operations": len(operations),
                "bytes": len(payload),
                "sha256": sha256(payload),
                "git_blob": git_blob_id(payload),
            }

        round_reports.append(
            {
                "round": round_number,
                "overlay_id": overlay_id,
                "manifest_sha256": manifest_hash,
                "stable_ids": len(stable_ids),
                "sources": payload_reports,
            }
        )

    return authorities, grouped, round_reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--existing-rounds", nargs="+", required=True, type=int)
    parser.add_argument("--target-rounds", nargs="+", required=True, type=int)
    parser.add_argument(
        "--base-revision",
        default="HEAD",
        help="committed cumulative source to which only the new operations apply",
    )
    parser.add_argument(
        "--check-revision",
        help="require the composed bytes to equal this committed revision",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="atomically replace affected root sources after all checks pass",
    )
    args = parser.parse_args()
    if args.write and args.check_revision:
        parser.error("--write and --check-revision are mutually exclusive")

    existing = args.existing_rounds
    target = args.target_rounds
    if existing != sorted(set(existing)):
        parser.error("existing rounds must be unique and ascending")
    if target != sorted(set(target)):
        parser.error("target rounds must be unique and ascending")
    if target[: len(existing)] != existing or len(target) <= len(existing):
        parser.error("target rounds must strictly extend the existing sequence")

    authorities, grouped, round_reports = collect_projection(target)
    existing_set = set(existing)
    prepared: dict[str, dict] = {}

    for source, operations in grouped.items():
        ordered = sorted(operations, key=lambda item: item["start_byte"])
        for left, right in zip(ordered, ordered[1:]):
            if left["end_byte_exclusive"] > right["start_byte"]:
                raise ValueError(
                    "cross-overlay authority overlap: "
                    f"{left['operation_id']} / {right['operation_id']}"
                )

        previous_operations = [
            operation for operation in ordered if operation["round"] in existing_set
        ]
        new_operations = [
            operation for operation in ordered if operation["round"] not in existing_set
        ]
        previous = apply_operations(authorities[source], previous_operations)
        authority_projection = apply_operations(authorities[source], ordered)
        source_path = ROOT / source
        current = git_blob(args.base_revision, source)
        current_blob = git_blob_id(current)
        current_worktree = source_path.read_bytes() if args.write else None
        worktree_blob = (
            filtered_git_blob_id(current_worktree, source)
            if current_worktree is not None
            else None
        )
        if args.write and worktree_blob != current_blob:
            raise ValueError(
                f"worktree source differs from base revision {args.base_revision}: {source}"
            )
        previous_blob = git_blob_id(previous)
        authority_projection_blob = git_blob_id(authority_projection)
        rebased = rebase_operations(authorities[source], current, new_operations)
        projection = apply_operations(current, rebased)
        projection_blob = git_blob_id(projection)
        if current_blob == previous_blob and projection != authority_projection:
            raise ValueError(f"direct projection and rebased composition differ: {source}")
        prepared[source] = {
            "path": source_path,
            "current": current,
            "current_worktree": current_worktree,
            "current_blob": current_blob,
            "worktree_blob": worktree_blob,
            "previous": previous,
            "previous_blob": previous_blob,
            "authority_projection": authority_projection,
            "authority_projection_blob": authority_projection_blob,
            "projection": projection,
            "projection_blob": projection_blob,
            "operations": ordered,
            "new_operations": new_operations,
            "rebased_operations": rebased,
        }

    temporary_paths: dict[str, Path] = {}
    try:
        if args.write:
            for source, item in prepared.items():
                if item["current_blob"] == item["projection_blob"]:
                    continue
                source_path: Path = item["path"]
                with tempfile.NamedTemporaryFile(
                    dir=source_path.parent,
                    prefix=f".{source_path.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as handle:
                    handle.write(item["projection"])
                    handle.flush()
                    os.fsync(handle.fileno())
                    temporary_paths[source] = Path(handle.name)
            for source, temporary in temporary_paths.items():
                os.replace(temporary, prepared[source]["path"])
        source_reports = {}
        for source, item in prepared.items():
            if args.write:
                current_after = item["path"].read_bytes()
                current_after_blob = filtered_git_blob_id(current_after, source)
                expected_after_blob = item["projection_blob"]
                if current_after_blob != expected_after_blob:
                    raise ValueError(f"post-write byte mismatch: {source}")
            elif args.check_revision:
                checked = git_blob(args.check_revision, source)
                current_after_blob = git_blob_id(checked)
                if current_after_blob != item["projection_blob"]:
                    raise ValueError(
                        f"checked revision is not the composed projection: {source}"
                    )
            else:
                current_after_blob = item["current_blob"]
            source_reports[source] = {
                "authority_bytes": len(authorities[source]),
                "authority_sha256": sha256(authorities[source]),
                "existing_operations": sum(
                    operation["round"] in existing_set
                    for operation in item["operations"]
                ),
                "target_operations": len(item["operations"]),
                "new_operations": len(item["new_operations"]),
                "before_worktree_bytes": (
                    len(item["current_worktree"])
                    if item["current_worktree"] is not None
                    else None
                ),
                "before_worktree_sha256": (
                    sha256(item["current_worktree"])
                    if item["current_worktree"] is not None
                    else None
                ),
                "before_bytes": len(item["current"]),
                "before_sha256": sha256(item["current"]),
                "before_git_blob": item["current_blob"],
                "before_state": (
                    "exact_existing_overlay_projection"
                    if item["current_blob"] == item["previous_blob"]
                    else "verified_committed_cumulative_source"
                ),
                "authority_projection_bytes": len(item["authority_projection"]),
                "authority_projection_sha256": sha256(item["authority_projection"]),
                "authority_projection_git_blob": item["authority_projection_blob"],
                "composed_bytes": len(item["projection"]),
                "composed_sha256": sha256(item["projection"]),
                "composed_git_blob": item["projection_blob"],
                "written": args.write
                and item["current_blob"] != item["projection_blob"],
                "matches_target_after": current_after_blob == item["projection_blob"],
            }
    finally:
        for temporary in temporary_paths.values():
            if temporary.exists():
                temporary.unlink()

    report = {
        "schema": "unofficial-ai-integrated-stacks-overlay-composition/v1",
        "status": "PASS",
        "existing_rounds": existing,
        "target_rounds": target,
        "base_revision": args.base_revision,
        "check_revision": args.check_revision,
        "write_requested": args.write,
        "operations": sum(len(item["operations"]) for item in prepared.values()),
        "new_operations": sum(
            operation["round"] not in existing_set
            for item in prepared.values()
            for operation in item["operations"]
        ),
        "overlays": round_reports,
        "sources": source_reports,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Overlay composition: FAIL\n- {exc}", file=os.sys.stderr)
        raise SystemExit(1)
