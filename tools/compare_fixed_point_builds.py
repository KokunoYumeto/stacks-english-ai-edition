#!/usr/bin/env python3
"""Compare two fixed-point build receipts and emit a reproducibility receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


IDENTICAL_KEYS = (
    "schema",
    "status",
    "source",
    "builder",
    "composition",
    "environment",
    "build",
    "artifacts",
    "pdfs_committed",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_receipt(path: Path) -> tuple[bytes, dict[str, object]]:
    data = path.read_bytes()
    parsed = json.loads(data.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"receipt is not a JSON object: {path}")
    if (
        parsed.get("schema")
        != "unofficial-ai-integrated-stacks-fixed-point-build/v1"
        or parsed.get("status") != "PASS"
    ):
        raise ValueError(f"receipt is not a passing full fixed-point build: {path}")
    return data, parsed


def run_identity(
    logical_path: str, data: bytes, receipt: dict[str, object]
) -> dict[str, object]:
    build = receipt.get("build")
    if not isinstance(build, dict):
        raise ValueError("build receipt lacks build state")
    return {
        "receipt": logical_path,
        "created_utc": receipt.get("created_utc"),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "status": receipt.get("status"),
        "global_fixed_point_sweep": build.get("global_fixed_point_sweep"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--first-logical-path", required=True)
    parser.add_argument("--second-logical-path", required=True)
    parser.add_argument("--admitted-errata", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    first_path = args.first.resolve()
    second_path = args.second.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite output: {output}")
    first_bytes, first = load_receipt(first_path)
    second_bytes, second = load_receipt(second_path)

    mismatched_keys = [key for key in IDENTICAL_KEYS if first.get(key) != second.get(key)]
    if mismatched_keys:
        raise ValueError(
            "fixed-point receipts differ in bound state: " + ", ".join(mismatched_keys)
        )
    if first.get("created_utc") == second.get("created_utc"):
        raise ValueError("receipts do not identify distinct invocations")

    artifacts = first.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("first receipt lacks artifacts")
    artifact_identities: list[dict[str, object]] = []
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("invalid artifact row")
        identity = {
            key: artifact.get(key) for key in ("stem", "pages", "bytes", "sha256")
        }
        if (
            not isinstance(identity["stem"], str)
            or not isinstance(identity["pages"], int)
            or not isinstance(identity["bytes"], int)
            or not isinstance(identity["sha256"], str)
        ):
            raise ValueError("invalid artifact identity")
        artifact_identities.append(identity)

    tuple_lines = [
        "|".join(
            (
                str(artifact["stem"]),
                str(artifact["pages"]),
                str(artifact["bytes"]),
                str(artifact["sha256"]),
            )
        )
        for artifact in sorted(artifact_identities, key=lambda item: str(item["stem"]))
    ]
    tuple_set_sha256 = sha256_bytes(
        (("\n".join(tuple_lines)) + "\n").encode("utf-8")
    )

    source = first.get("source")
    builder = first.get("builder")
    composition = first.get("composition")
    environment = first.get("environment")
    build = first.get("build")
    if not all(
        isinstance(item, dict)
        for item in (source, builder, composition, environment, build)
    ):
        raise ValueError("first receipt lacks bound source, builder, or environment state")

    receipt = {
        "schema": "unofficial-ai-integrated-stacks-clean-build-reproducibility/v1",
        "status": "PASS",
        "created_utc": (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        ),
        "source": source,
        "builder": builder,
        "environment": environment,
        "scope": {
            "admitted_errata": args.admitted_errata,
            "registry_cutoff_commit": composition.get("registry_cutoff_commit"),
            "source_commit": source.get("commit"),
            "source_tree": source.get("tree"),
            "composition_receipt": composition.get("receipt"),
            "composition_receipt_sha256": composition.get("receipt_sha256"),
        },
        "method": {
            "execution_model": "independent_linked_worktrees",
            "first_worktree_kind": build.get("worktree_kind"),
            "second_worktree_kind": second.get("build", {}).get("worktree_kind"),
            "builder_path": builder.get("path"),
            "builder_git_blob": builder.get("git_blob"),
            "builder_sha256": builder.get("sha256"),
        },
        "runs": {
            "first": run_identity(
                args.first_logical_path, first_bytes, first
            ),
            "second": run_identity(
                args.second_logical_path, second_bytes, second
            ),
        },
        "artifacts": artifact_identities,
        "comparison": {
            "chapter_count": len(artifact_identities),
            "matched_artifact_count": len(artifact_identities),
            "different_artifact_count": 0,
            "different_artifacts": [],
            "total_pages_each_run": sum(
                int(artifact["pages"]) for artifact in artifact_identities
            ),
            "total_pdf_bytes_each_run": sum(
                int(artifact["bytes"]) for artifact in artifact_identities
            ),
            "artifact_tuple_set_sha256_each_run": tuple_set_sha256,
            "all_artifact_identities_exactly_equal": True,
            "source_identity_equal": True,
            "builder_identity_equal": True,
            "environment_identity_equal": True,
            "fixed_point_sweep_equal": True,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "matched_artifacts": len(artifact_identities),
                "artifact_tuple_set_sha256": tuple_set_sha256,
                "output": str(output),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
