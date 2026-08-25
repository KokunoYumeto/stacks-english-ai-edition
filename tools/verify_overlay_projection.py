#!/usr/bin/env python3
"""Verify an exact cumulative projection for admitted v2 errata overlays.

Candidates are independently bound to pinned authority bytes. This checker
validates those bindings, applies only their declared byte intervals in
registry order, rejects cross-overlay overlap, and optionally proves that a
committed source blob equals the resulting projection. It never edits source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "ai-integrated/candidates/commons/stacks/errata"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_blob_id(data: bytes) -> str:
    header = f"blob {len(data)}".encode("ascii") + bytes([0])
    return hashlib.sha1(header + data).hexdigest()


def git_blob(revision: str, source: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", f"{revision}:{source}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise ValueError(completed.stderr.decode("utf-8", errors="replace").strip())
    return completed.stdout


def candidate_dir(round_number: int) -> Path:
    return CANDIDATES if round_number == 1 else CANDIDATES / f"r{round_number}"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{number}: {exc}") from exc
    return rows


def apply(authority: bytes, operations: list[dict]) -> bytes:
    output = authority
    for operation in sorted(operations, key=lambda item: item["start_byte"], reverse=True):
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if output[start:end] != old:
            raise ValueError(f"authority interval mismatch: {operation['operation_id']}")
        output = output[:start] + replacement + output[end:]
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rounds", nargs="+", type=int)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument(
        "--check-current",
        action="store_true",
        help="require each committed source blob to equal the cumulative projection",
    )
    args = parser.parse_args()

    rounds = args.rounds
    if rounds != sorted(set(rounds)):
        parser.error("rounds must be unique and supplied in ascending registry order")

    registry = json.loads(
        (ROOT / "ai-integrated/registry/overlays.json").read_text(encoding="utf-8")
    )
    registered = {entry["id"]: entry for entry in registry["registered_entries"]}
    grouped: dict[str, list[dict]] = defaultdict(list)
    authorities: dict[str, bytes] = {}
    round_reports: list[dict] = []

    for round_number in rounds:
        overlay_id = f"stacks-errata-a04446e-r{round_number}"
        if overlay_id not in registered:
            raise ValueError(f"overlay is not registered: {overlay_id}")
        directory = candidate_dir(round_number)
        manifest = directory / "candidate.manifest.json"
        manifest_hash = sha256(manifest.read_bytes())
        if manifest_hash != registered[overlay_id]["manifest_sha256"].upper():
            raise ValueError(f"registry manifest mismatch: {overlay_id}")

        rows = read_jsonl(directory / "source-map.jsonl")
        stable_ids = registered[overlay_id]["stable_ids"]
        if isinstance(stable_ids, str):
            stable_ids = stable_ids.split()
        if [row["unit_id"] for row in rows] != stable_ids:
            raise ValueError(f"registry/source-map ID mismatch: {overlay_id}")

        per_source: dict[str, list[dict]] = defaultdict(list)
        payload_paths: dict[str, str] = {}
        for row in rows:
            source = row["source"]
            if source in payload_paths and payload_paths[source] != row["payload"]:
                raise ValueError(f"multiple payload paths for {overlay_id}/{source}")
            payload_paths[source] = row["payload"]
            authority_path = directory / row["authority"]
            authority = authority_path.read_bytes()
            expected_authority = row["authority_sha256"].upper()
            if sha256(authority) != expected_authority:
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
            projection = apply(authorities[source], operations)
            payload = (directory / payload_paths[source]).read_bytes()
            if projection != payload:
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

    source_reports: dict[str, dict] = {}
    for source, operations in grouped.items():
        ordered = sorted(operations, key=lambda item: item["start_byte"])
        for left, right in zip(ordered, ordered[1:]):
            if left["end_byte_exclusive"] > right["start_byte"]:
                raise ValueError(
                    "cross-overlay authority overlap: "
                    f"{left['operation_id']} / {right['operation_id']}"
                )
        projection = apply(authorities[source], ordered)
        committed = git_blob(args.revision, source) if args.check_current else None
        if committed is not None and committed != projection:
            raise ValueError(
                f"committed source is not the exact overlay projection: {source}"
            )
        source_reports[source] = {
            "authority_bytes": len(authorities[source]),
            "authority_sha256": sha256(authorities[source]),
            "operations": len(ordered),
            "projection_bytes": len(projection),
            "projection_sha256": sha256(projection),
            "projection_git_blob": git_blob_id(projection),
            "committed_revision": args.revision if args.check_current else None,
            "committed_matches_projection": args.check_current,
        }

    report = {
        "schema": "unofficial-ai-integrated-stacks-overlay-projection/v1",
        "status": "PASS",
        "rounds": rounds,
        "operations": sum(item["operations"] for item in source_reports.values()),
        "overlays": round_reports,
        "sources": source_reports,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Overlay projection verification: FAIL\n- {exc}", file=sys.stderr)
        raise SystemExit(1)
