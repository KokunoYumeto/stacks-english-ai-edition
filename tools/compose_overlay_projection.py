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
import bisect
import difflib
import json
import os
import subprocess
import tempfile
from collections import Counter, defaultdict
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


SEMANTIC_DISPOSITIONS_PATH = (
    ROOT / "validation/overlay-composition-semantic-dispositions-v1.json"
)
OFFICIAL_BASELINE = "a04446e57ec1fbc252a871afcec7752fb2807b14"


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


def git_is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "merge-base",
            "--is-ancestor",
            ancestor,
            descendant,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode not in (0, 1):
        raise ValueError(
            completed.stderr.decode("utf-8", errors="replace").strip()
        )
    return completed.returncode == 0


def git_path_exists(revision: str, path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{revision}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return completed.returncode == 0


def git_commit_parents(commit: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-list", "--parents", "-n", "1", commit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        raise ValueError(completed.stderr.strip())
    fields = completed.stdout.strip().split()
    if not fields or fields[0] != commit:
        raise ValueError(f"cannot resolve exact commit parents: {commit}")
    return fields[1:]


def load_semantic_dispositions(
    base_revision: str,
) -> tuple[dict[str, dict], str | None]:
    """Load dispositions only from the committed composition base."""

    relative = SEMANTIC_DISPOSITIONS_PATH.relative_to(ROOT).as_posix()
    if not git_path_exists(base_revision, relative):
        return {}, None
    raw = git_blob(base_revision, relative)
    document = json.loads(raw.decode("utf-8"))
    if (
        document.get("schema")
        != "unofficial-ai-integrated-stacks-semantic-composition-dispositions/v1"
        or document.get("status") != "PASS"
        or not isinstance(document.get("dispositions"), list)
    ):
        raise ValueError("invalid semantic composition disposition registry")
    by_id: dict[str, dict] = {}
    for disposition in document["dispositions"]:
        if not isinstance(disposition, dict):
            raise ValueError("semantic composition disposition is not an object")
        operation = disposition.get("operation")
        if not isinstance(operation, dict):
            raise ValueError("semantic composition disposition lacks operation identity")
        operation_id = operation.get("operation_id")
        if not isinstance(operation_id, str) or not operation_id:
            raise ValueError("semantic composition disposition lacks operation_id")
        if operation_id in by_id:
            raise ValueError(
                f"duplicate semantic composition disposition: {operation_id}"
            )
        by_id[operation_id] = disposition
    return by_id, sha256(raw)


def verify_semantic_disposition_consumption(
    applicable_ids: set[str], consumed_ids: list[str]
) -> None:
    """Require one and only one proved use of every applicable disposition."""
    counts = Counter(consumed_ids)
    unused = sorted(applicable_ids - counts.keys())
    unexpected = sorted(counts.keys() - applicable_ids)
    repeated = sorted(key for key, count in counts.items() if count != 1)
    if unused or unexpected or repeated:
        raise ValueError(
            "semantic composition dispositions were not consumed exactly once: "
            f"unused={unused}, unexpected={unexpected}, repeated={repeated}"
        )


def validate_semantic_disposition(
    operation: dict,
    disposition: dict,
    authority: bytes,
    current: bytes,
    base_revision: str,
) -> dict:
    """Prove a structural predecessor already satisfies one admitted repair.

    This is deliberately stricter than a prose waiver.  The disposition must
    bind the admitted operation, the exact cumulative source blob, the earlier
    introducing commit and source blob, a unique positive evidence block at
    both revisions, and the absence of the exact defective authority text.
    """

    operation_id = operation["operation_id"]
    source = operation["source"]
    expected_operation = {
        "overlay_id": f"stacks-errata-a04446e-r{operation['round']}",
        "stable_id": operation["stable_id"],
        "operation_id": operation_id,
        "source": source,
        "old": {
            "bytes": operation["old_bytes"],
            "sha256": operation["old_sha256"],
        },
        "replacement": {
            "bytes": operation["replacement_bytes"],
            "sha256": operation["replacement_sha256"],
        },
    }
    if (
        disposition.get("operation") != expected_operation
        or disposition.get("disposition")
        != "structurally_superseded_by_ancestor_rewrite"
    ):
        raise ValueError(f"semantic disposition identity mismatch: {operation_id}")

    official_authority = git_blob(OFFICIAL_BASELINE, source)
    if official_authority != authority:
        raise ValueError(f"semantic disposition authority bytes differ: {operation_id}")
    expected_authority_source = {
        "commit": OFFICIAL_BASELINE,
        "git_blob": git_blob_id(authority),
        "bytes": len(authority),
        "sha256": sha256(authority),
    }
    if disposition.get("authority_source") != expected_authority_source:
        raise ValueError(
            f"semantic disposition authority binding mismatch: {operation_id}"
        )

    old = operation["old_text"].encode("utf-8")
    replacement = operation["replacement_text"].encode("utf-8")
    evidence_record = disposition.get("evidence")
    if (
        not isinstance(evidence_record, dict)
        or evidence_record.get("encoding") != "utf-8"
        or not isinstance(evidence_record.get("text"), str)
    ):
        raise ValueError(f"semantic disposition lacks exact evidence: {operation_id}")
    evidence = evidence_record["text"].encode("utf-8")
    if not evidence:
        raise ValueError(f"semantic disposition evidence is empty: {operation_id}")

    transition = disposition.get("rewrite_transition")
    if not isinstance(transition, dict):
        raise ValueError(f"semantic disposition lacks rewrite transition: {operation_id}")
    rewrite_commit = transition.get("commit")
    parent_commit = transition.get("parent_commit")
    if not isinstance(rewrite_commit, str) or not isinstance(parent_commit, str):
        raise ValueError(f"semantic disposition rewrite IDs are invalid: {operation_id}")
    if git_commit_parents(rewrite_commit) != [parent_commit]:
        raise ValueError(
            f"semantic disposition rewrite parent mismatch: {operation_id}"
        )
    if not git_is_ancestor(rewrite_commit, base_revision):
        raise ValueError(
            f"semantic disposition rewrite is not an ancestor: {operation_id}"
        )
    parent_source = git_blob(parent_commit, source)
    result_source = git_blob(rewrite_commit, source)
    expected_transition = {
        "commit": rewrite_commit,
        "parent_commit": parent_commit,
        "parent_source": {
            "git_blob": git_blob_id(parent_source),
            "bytes": len(parent_source),
            "sha256": sha256(parent_source),
        },
        "result_source": {
            "git_blob": git_blob_id(result_source),
            "bytes": len(result_source),
            "sha256": sha256(result_source),
        },
        "parent_counts": {
            "old": parent_source.count(old),
            "replacement": parent_source.count(replacement),
            "evidence": parent_source.count(evidence),
        },
        "result_counts": {
            "old": result_source.count(old),
            "replacement": result_source.count(replacement),
            "evidence": result_source.count(evidence),
        },
    }
    if transition != expected_transition:
        raise ValueError(
            f"semantic disposition rewrite transition mismatch: {operation_id}"
        )
    if (
        expected_transition["parent_counts"]
        != {"old": 1, "replacement": 0, "evidence": 0}
        or expected_transition["result_counts"]
        != {"old": 0, "replacement": 0, "evidence": 1}
    ):
        raise ValueError(
            f"semantic disposition rewrite does not prove the transition: {operation_id}"
        )

    expected_base = {
        "git_blob": git_blob_id(current),
        "bytes": len(current),
        "sha256": sha256(current),
        "old_count": current.count(old),
        "replacement_count": current.count(replacement),
        "evidence_count": current.count(evidence),
    }
    if disposition.get("composition_base_source") != expected_base:
        raise ValueError(
            f"semantic disposition cumulative source mismatch: {operation_id}"
        )
    if expected_base["old_count"] != 0 or expected_base["evidence_count"] != 1:
        raise ValueError(
            f"semantic disposition is not satisfied in the base: {operation_id}"
        )

    base_offset = current.find(evidence)
    rewrite_offset = result_source.find(evidence)
    expected_evidence = {
        "encoding": "utf-8",
        "text": evidence_record["text"],
        "bytes": len(evidence),
        "sha256": sha256(evidence),
        "occurrence_count": 1,
        "rewrite": {
            "byte_offset": rewrite_offset,
            "line": result_source[:rewrite_offset].count(b"\n") + 1,
        },
        "base": {
            "byte_offset": base_offset,
            "line": current[:base_offset].count(b"\n") + 1,
        },
    }
    if evidence_record != expected_evidence:
        raise ValueError(
            f"semantic disposition evidence binding mismatch: {operation_id}"
        )

    assertions = disposition.get("semantic_assertions")
    if not isinstance(assertions, list) or not assertions:
        raise ValueError(f"semantic disposition lacks assertions: {operation_id}")
    evidence_text = evidence_record["text"]
    for assertion in assertions:
        if (
            not isinstance(assertion, dict)
            or not isinstance(assertion.get("text"), str)
            or not isinstance(assertion.get("occurrence_count"), int)
            or assertion.get("scope") != "positive_evidence"
        ):
            raise ValueError(
                f"invalid semantic disposition assertion: {operation_id}"
            )
        if evidence_text.count(assertion["text"]) != assertion["occurrence_count"]:
            raise ValueError(
                f"semantic disposition assertion mismatch: {operation_id}"
            )

    return dict(disposition)


def rebase_operations(
    authority: bytes,
    current: bytes,
    operations: list[dict],
    preapplied_operations: list[dict] | None = None,
    semantic_dispositions: dict[str, dict] | None = None,
    semantic_disposition_operations: list[dict] | None = None,
    base_revision: str | None = None,
) -> list[dict]:
    """Map authority-bound operations through unchanged line blocks in current.

    A cumulative source can already contain one of the newly admitted edits when
    a repair landed directly on the public branch before its overlay admission.
    Such an operation is accepted only when a single same-sized ``replace``
    opcode is *exactly* the manifest-bound old-to-new byte substitution.  Any
    other changed block, line-count drift, ambiguous occurrence, or unrelated
    byte is still rejected.  Accepted pre-applied operations are omitted from
    the rebased edit list because their replacement is already present.
    """
    authority_lines = authority.splitlines(keepends=True)
    current_lines = current.splitlines(keepends=True)
    authority_offsets = byte_offsets(authority_lines)
    current_offsets = byte_offsets(current_lines)
    matcher = difflib.SequenceMatcher(
        None, authority_lines, current_lines, autojunk=False
    )
    opcodes = matcher.get_opcodes()
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

    def exact_preapplied(operation: dict) -> bool:
        """Prove one operation is already present as its exact byte edit."""

        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if not old or not replacement:
            return False

        # Locate the authority lines containing the manifest interval.  The
        # declared source range is part of the candidate's bound evidence and
        # prevents a coincidental replacement elsewhere from being accepted.
        authority_line_start = bisect.bisect_right(authority_offsets, start) - 1
        authority_line_end = bisect.bisect_left(authority_offsets, end)
        if authority_line_start < 0 or authority_line_end <= authority_line_start:
            return False
        if operation.get("source_start_line") != authority_line_start + 1:
            return False
        if operation.get("source_end_line") != authority_line_end:
            return False

        changed_blocks = [
            (tag, a_start, a_end, c_start, c_end)
            for tag, a_start, a_end, c_start, c_end in opcodes
            if tag != "equal"
            and a_start <= authority_line_start
            and authority_line_end <= a_end
        ]
        if len(changed_blocks) != 1:
            return False
        tag, a_start, a_end, c_start, c_end = changed_blocks[0]
        # A pre-applied edit cannot hide an insertion/deletion or a line
        # reordering.  Requiring one-for-one replacement lines keeps the proof
        # local and deterministic.
        if tag != "replace" or (a_end - a_start) != (c_end - c_start):
            return False

        authority_block_start = authority_offsets[a_start]
        authority_block_end = authority_offsets[a_end]
        current_block_start = current_offsets[c_start]
        current_block_end = current_offsets[c_end]
        authority_block = authority[authority_block_start:authority_block_end]
        current_block = current[current_block_start:current_block_end]
        relative_start = start - authority_block_start
        relative_end = end - authority_block_start
        if relative_start < 0 or relative_end > len(authority_block):
            return False
        if authority_block[relative_start:relative_end] != old:
            return False
        if authority_block.count(old) != 1:
            return False
        expected = (
            authority_block[:relative_start]
            + replacement
            + authority_block[relative_end:]
        )
        return current_block == expected

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
            if exact_preapplied(operation):
                if preapplied_operations is not None:
                    preapplied_operations.append(dict(operation))
                continue
            disposition = (semantic_dispositions or {}).get(
                operation["operation_id"]
            )
            if disposition is not None and base_revision is not None:
                validate_semantic_disposition(
                    operation, disposition, authority, current, base_revision
                )
                if semantic_disposition_operations is not None:
                    semantic_disposition_operations.append(dict(operation))
                continue
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
            if exact_preapplied(operation):
                if preapplied_operations is not None:
                    preapplied_operations.append(dict(operation))
                continue
            disposition = (semantic_dispositions or {}).get(
                operation["operation_id"]
            )
            if disposition is not None and base_revision is not None:
                validate_semantic_disposition(
                    operation, disposition, authority, current, base_revision
                )
                if semantic_disposition_operations is not None:
                    semantic_disposition_operations.append(dict(operation))
                continue
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
                enriched["candidate_directory"] = directory.relative_to(ROOT).as_posix()
                if row.get("composition_base") is not None:
                    enriched["composition_base"] = row["composition_base"]
                if row.get("composition_projection") is not None:
                    enriched["composition_projection"] = row["composition_projection"]
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


def resolve_supersessions(operations: list[dict]) -> tuple[list[dict], set[str]]:
    """Return the active last-wins operation set and superseded IDs.

    Superseding operations are append-only registry events.  They do not mutate
    their predecessor records; instead, their ``supersedes_operation_id`` field
    removes the earlier operation from the effective authority projection.
    """
    by_id: dict[str, dict] = {}
    superseded: set[str] = set()
    for operation in sorted(
        operations,
        key=lambda item: (item["round"], item["start_byte"], item["operation_id"]),
    ):
        operation_id = operation["operation_id"]
        if operation_id in by_id:
            raise ValueError(f"duplicate operation ID: {operation_id}")
        predecessor_id = operation.get("supersedes_operation_id")
        if predecessor_id is not None:
            predecessor = by_id.get(predecessor_id)
            if predecessor is None:
                raise ValueError(
                    f"superseding operation has no earlier predecessor: "
                    f"{operation_id} -> {predecessor_id}"
                )
            if predecessor["round"] >= operation["round"]:
                raise ValueError(
                    f"superseding operation is not later than its predecessor: "
                    f"{operation_id} -> {predecessor_id}"
                )
            if (
                predecessor["end_byte_exclusive"] <= operation["start_byte"]
                or operation["end_byte_exclusive"] <= predecessor["start_byte"]
            ):
                raise ValueError(
                    f"superseding operation does not overlap its predecessor: "
                    f"{operation_id} -> {predecessor_id}"
                )
            superseded.add(predecessor_id)
        by_id[operation_id] = operation
    return [operation for operation in by_id.values() if operation["operation_id"] not in superseded], superseded


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
    semantic_dispositions, semantic_dispositions_sha256 = (
        load_semantic_dispositions(args.base_revision)
    )
    existing_set = set(existing)
    prepared: dict[str, dict] = {}
    consumed_semantic_disposition_ids: list[str] = []

    for source, operations in grouped.items():
        ordered = sorted(
            operations,
            key=lambda item: (item["round"], item["start_byte"], item["operation_id"]),
        )
        active, superseded_ids = resolve_supersessions(ordered)
        active_by_offset = sorted(active, key=lambda item: item["start_byte"])
        for left, right in zip(active_by_offset, active_by_offset[1:]):
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
        previous_active, _ = resolve_supersessions(previous_operations)
        previous = apply_operations(
            authorities[source],
            sorted(previous_active, key=lambda item: item["start_byte"]),
        )
        authority_projection = apply_operations(authorities[source], active_by_offset)
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
        new_supersessions = [
            operation
            for operation in new_operations
            if operation.get("supersedes_operation_id") is not None
        ]
        preapplied_operations: list[dict] = []
        semantic_disposition_operations: list[dict] = []
        if current_blob == previous_blob:
            # The checked cumulative source is the exact effective projection of
            # the prior rounds.  Recompute it from the immutable authority using
            # the active last-wins target operation set.  This is the canonical
            # path for an append-only superseding correction such as R28.
            rebased = []
            projection = authority_projection
        else:
            if new_supersessions:
                # A cumulative generated source can contain admitted edits from
                # rounds outside this projection sequence. A superseding round
                # therefore carries an exact cumulative composition base and
                # projection. Verify those immutable artifacts and prove that
                # the projection changes only the predecessor's postimage into
                # the new postimage; never copy an isolated payload wholesale.
                if len(new_operations) != 1 or len(new_supersessions) != 1:
                    raise ValueError(
                        "superseding cumulative composition must contain exactly "
                        f"one new operation for {source}"
                    )
                operation = new_supersessions[0]
                composition_base_path = operation.get("composition_base")
                composition_projection_path = operation.get(
                    "composition_projection"
                )
                if not composition_base_path or not composition_projection_path:
                    raise ValueError(
                        f"superseding operation lacks bound composition artifacts: {source}"
                    )
                candidate_root = ROOT / operation["candidate_directory"]
                composition_base = (
                    candidate_root / composition_base_path
                ).read_bytes()
                direct_projection = (
                    candidate_root / composition_projection_path
                ).read_bytes()
                if composition_base != current:
                    raise ValueError(
                        f"bound cumulative composition base mismatch: {source}"
                    )
                predecessor_id = operation["supersedes_operation_id"]
                predecessor = next(
                    (
                        candidate
                        for candidate in ordered
                        if candidate["operation_id"] == predecessor_id
                    ),
                    None,
                )
                if predecessor is None:
                    raise ValueError(
                        f"superseded predecessor not found: {predecessor_id}"
                    )
                prior_postimage = predecessor["replacement_text"].encode("utf-8")
                new_postimage = operation["replacement_text"].encode("utf-8")
                if composition_base.count(prior_postimage) != 1:
                    raise ValueError(
                        "bound cumulative base does not contain exactly one "
                        f"predecessor postimage: {predecessor_id}"
                    )
                mapped_start = composition_base.index(prior_postimage)
                mapped_end = mapped_start + len(prior_postimage)
                expected_projection = (
                    composition_base[:mapped_start]
                    + new_postimage
                    + composition_base[mapped_end:]
                )
                if direct_projection != expected_projection:
                    raise ValueError(
                        f"bound superseding projection is not the exact last-wins edit: {source}"
                    )
                mapped = dict(operation)
                mapped["authority_start_byte"] = operation["start_byte"]
                mapped["authority_end_byte_exclusive"] = operation[
                    "end_byte_exclusive"
                ]
                mapped["start_byte"] = mapped_start
                mapped["end_byte_exclusive"] = mapped_end
                mapped["old_text"] = predecessor["replacement_text"]
                rebased = [mapped]
                projection = direct_projection
            else:
                new_active_ids = {
                    operation["operation_id"]
                    for operation in active
                    if operation["round"] not in existing_set
                }
                rebased = rebase_operations(
                    authorities[source],
                    current,
                    [
                        operation
                        for operation in new_operations
                        if operation["operation_id"] in new_active_ids
                    ],
                    preapplied_operations,
                    semantic_dispositions,
                    semantic_disposition_operations,
                    args.base_revision,
                )
                projection = apply_operations(current, rebased)
        consumed_semantic_disposition_ids.extend(
            operation["operation_id"]
            for operation in semantic_disposition_operations
        )
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
            "preapplied_operations": preapplied_operations,
            "semantic_disposition_operations": semantic_disposition_operations,
            "superseded_operation_ids": sorted(superseded_ids),
        }

    applicable_semantic_disposition_ids = {
        operation["operation_id"]
        for item in prepared.values()
        for operation in item["new_operations"]
        if operation["operation_id"] in semantic_dispositions
    }
    verify_semantic_disposition_consumption(
        applicable_semantic_disposition_ids, consumed_semantic_disposition_ids
    )

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
                "superseded_operations": len(item["superseded_operation_ids"]),
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
                "preapplied_operation_ids": [
                    operation["operation_id"]
                    for operation in item["preapplied_operations"]
                ],
                "semantic_disposition_operation_ids": [
                    operation["operation_id"]
                    for operation in item["semantic_disposition_operations"]
                ],
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
        "preapplied_operation_ids": sorted(
            operation["operation_id"]
            for item in prepared.values()
            for operation in item["preapplied_operations"]
        ),
        "semantic_dispositions": {
            "path": (
                str(SEMANTIC_DISPOSITIONS_PATH.relative_to(ROOT)).replace(
                    "\\", "/"
                )
                if semantic_dispositions_sha256 is not None
                else None
            ),
            "sha256": semantic_dispositions_sha256,
            "consumed_operation_ids": sorted(
                consumed_semantic_disposition_ids
            ),
        },
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
