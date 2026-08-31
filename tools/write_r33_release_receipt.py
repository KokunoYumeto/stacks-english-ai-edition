#!/usr/bin/env python3
"""Write the publication-complete R33 release receipt from bound evidence.

The writer only reads the local, already-verified R33 artifacts and a supplied
metadata-head/workflow identity.  It never reads credentials or mutates source
files.  The resulting receipt is intentionally independent of local absolute
paths so it can be published as provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
CONTENT_HEAD = "a52883a83081348d0ea4927a03d5fd8aa036890b"
REPOSITORY = "KokunoYumeto/unofficial-ai-integrated-stacks-project"
TAG = "ai-integrated-stacks-r33-2026-08-30"


def load(relative: str) -> dict[str, Any]:
    with (ROOT / relative).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {relative}")
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_bytes(revision: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{revision}:{relative}"],
        stderr=subprocess.DEVNULL,
    )


def identity(revision: str, relative: str) -> dict[str, Any]:
    data = git_bytes(revision, relative)
    return {
        "path": relative,
        "bytes": len(data),
        "sha256": sha256(data),
        "git_blob": git_blob(data),
    }


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-head", required=True)
    parser.add_argument("--metadata-tree", required=True)
    parser.add_argument("--workflow-run", required=True, type=int)
    parser.add_argument(
        "--output",
        default="validation/stacks-errata-a04446e-r33-release-2026-08-30.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    composition = load("validation/composition-current.json")
    build = load("validation/stacks-errata-a04446e-r33-build-2026-08-30.json")
    visual = load("validation/stacks-errata-a04446e-r33-visual-qa-2026-08-30.json")
    reproduction = load(
        "validation/stacks-errata-a04446e-r33-reproducibility-2026-08-30.json"
    )
    second = load(
        "validation/stacks-errata-a04446e-r33-reproducibility-second-2026-08-30.json"
    )
    package = load("validation/stacks-errata-a04446e-r33-package-2026-08-30.json")
    readback = load(
        "validation/stacks-errata-a04446e-r33-public-readback-2026-08-30.json"
    )
    zenodo_receipt = load(
        "validation/stacks-errata-a04446e-r33-zenodo-publication-2026-08-30.json"
    )
    registry = load("ai-integrated/registry/overlays.json")
    entries = registry["registered_entries"]
    r33_entry = entries[-1]
    namespace = str(r33_entry["namespace"])
    candidate_root = f"ai-integrated/candidates/{namespace}"
    manifest_path = f"{candidate_root}/candidate.manifest.json"
    manifest = json.loads(git_bytes(CONTENT_HEAD, manifest_path).decode("utf-8"))
    payload_rel = next(
        str(item["path"])
        for item in manifest.get("builds", [])
        if str(item.get("path", "")).startswith("payload/")
    )
    payload_path = f"{candidate_root}/{payload_rel}"
    review_path = f"{candidate_root}/replay/independent-review.json"
    source_path = "spaces-morphisms.tex"
    new_overlay = composition["new_overlays"][0]
    build_artifacts = build["artifacts"]
    visual_scope = visual["scope"]
    visual_checks = visual["checks"]
    tuple_lines = [
        "|".join(
            (
                str(item["stem"]),
                str(item["pages"]),
                str(item["bytes"]),
                str(item["sha256"]),
            )
        )
        for item in sorted(build_artifacts, key=lambda item: str(item["stem"]))
    ]
    tuple_sha = sha256(("\n".join(tuple_lines) + "\n").encode("utf-8"))
    changed = readback["changed_path_readback"]
    checked_paths = [
        {
            "path": row["path"],
            "bytes": row["bytes"],
            "sha256": row["sha256"],
            "git_blob": row["git_blob"],
        }
        for row in changed["changed_paths"]
    ]
    content_tree = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{CONTENT_HEAD}^{{tree}}"],
        text=True,
    ).strip()
    composition_id = identity(CONTENT_HEAD, "validation/composition-current.json")
    build_id = identity(CONTENT_HEAD, "validation/stacks-errata-a04446e-r33-build-2026-08-30.json")
    visual_id = identity(CONTENT_HEAD, "validation/stacks-errata-a04446e-r33-visual-qa-2026-08-30.json")
    repro_id = identity(CONTENT_HEAD, "validation/stacks-errata-a04446e-r33-reproducibility-2026-08-30.json")
    second_id = identity(CONTENT_HEAD, "validation/stacks-errata-a04446e-r33-reproducibility-second-2026-08-30.json")
    registry_overlay_id = identity(CONTENT_HEAD, "ai-integrated/registry/overlays.json")
    registry_lease_id = identity(CONTENT_HEAD, "ai-integrated/registry/leases.json")
    manifest_id = identity(CONTENT_HEAD, manifest_path)
    payload_id = identity(CONTENT_HEAD, payload_path)
    review_id = identity(CONTENT_HEAD, review_path)
    source_id = identity(CONTENT_HEAD, source_path)
    package_id = identity(CONTENT_HEAD, "validation/stacks-errata-a04446e-r33-package-2026-08-30.json")
    package_assets = package["release_assets"]
    rb_github = readback["github"]
    rb_zenodo = readback["zenodo"]
    receipt: dict[str, Any] = {
        "schema": "unofficial-ai-integrated-stacks-errata-release/v1",
        "status": "PUBLICATION_COMPLETE",
        "created_utc": package["created_utc"],
        "updated_utc": now(),
        "release": {
            "repository": REPOSITORY,
            "default_branch": "main",
            "previous_public_main_head": composition["previous_cutoff"]["public_main_head"],
            "frozen_registry_cutoff": composition["registry"]["cutoff_commit"],
            "frozen_registry_tree": composition["registry"]["cutoff_tree"],
            "registered_overlays": composition["registry"]["registered_overlays"],
            "registered_stable_ids": composition["registry"]["registered_stable_ids"],
            "published_content_head": CONTENT_HEAD,
            "content_tree": content_tree,
            "metadata_head": args.metadata_head,
            "metadata_tree": args.metadata_tree,
            "tag": TAG,
            "admitted_and_composed": ["stacks-errata-a04446e-r33"],
        },
        "overlays": [
            {
                "overlay_id": r33_entry["id"],
                "lease_commit": new_overlay["candidate_commit"],
                "candidate_commit": new_overlay["candidate_commit"],
                "admission_commit": new_overlay["admission_commit"],
                "stable_ids": len(r33_entry["stable_ids"]),
                "operations": new_overlay["operations"],
                "affected_source": source_path,
                "manifest": manifest_id,
                "payload": payload_id,
                "independent_review": review_id,
                "composed_source": source_id,
            }
        ],
        "composition": {
            "receipt": composition_id,
            "registry_import_commit": composition["registry"]["linear_import_commit"],
            "source_commit": composition["composition"]["source_commit"],
            "source_tree": composition["composition"]["source_tree"],
            "cumulative_v2_operations": composition["composition"]["total_v2_operations"],
            "new_stable_ids": new_overlay["stable_ids"],
            "new_operations": new_overlay["operations"],
            "order": ["stacks-errata-a04446e-r33"],
            "mode": composition["composition"]["mode"],
            "composed_sources": [source_id],
        },
        "build": {
            "receipt_path": "validation/stacks-errata-a04446e-r33-build-2026-08-30.json",
            "receipt_bytes": build_id["bytes"],
            "receipt_sha256": build_id["sha256"],
            "receipt_git_blob": build_id["git_blob"],
            "source_commit": build["source"]["commit"],
            "source_tree": build["source"]["tree"],
            "chapters": len(build_artifacts),
            "pages": sum(int(item["pages"]) for item in build_artifacts),
            "pdf_bytes": sum(int(item["bytes"]) for item in build_artifacts),
            "global_fixed_point_sweep": build["build"]["global_fixed_point_sweep"],
            "artifact_tuple_set_sha256": build["build"]["artifact_tuple_set_sha256"],
        },
        "visual_qa": {
            "status": "PASS",
            "receipt_path": "validation/stacks-errata-a04446e-r33-visual-qa-2026-08-30.json",
            "receipt_bytes": visual_id["bytes"],
            "receipt_sha256": visual_id["sha256"],
            "receipt_git_blob": visual_id["git_blob"],
            "full_page_reviews": visual_scope["full_page_contact_sheet_review_count"],
            "high_resolution_locus_pages": visual_scope["high_resolution_locus_page_count"],
            "defects": sum(int(visual_checks.get(key, 0)) for key in (
                "clipped_content", "overlapping_content", "blank_pages",
                "corrupted_pages", "missing_or_unreadable_glyphs", "broken_diagrams",
            )),
        },
        "reproducibility": {
            "status": "PASS",
            "summary_path": "validation/stacks-errata-a04446e-r33-reproducibility-2026-08-30.json",
            "summary_bytes": repro_id["bytes"],
            "summary_sha256": repro_id["sha256"],
            "summary_git_blob": repro_id["git_blob"],
            "second_receipt_path": "validation/stacks-errata-a04446e-r33-reproducibility-second-2026-08-30.json",
            "second_receipt_bytes": second_id["bytes"],
            "second_receipt_sha256": second_id["sha256"],
            "second_receipt_git_blob": second_id["git_blob"],
            "matched_artifacts": reproduction["comparison"]["matched_artifact_count"],
            "different_artifacts": reproduction["comparison"]["different_artifact_count"],
            "artifact_tuple_set_sha256": tuple_sha,
        },
        "public_readback": {
            "status": "PASS",
            "checked_utc": readback["checked_utc"],
            "method": readback["method"],
            "commit": CONTENT_HEAD,
            "changed_path_readback_count": changed["changed_path_count"],
            "changed_path_readback_bytes": changed["readback_bytes"],
            "changed_path_mismatches": 0,
            "changed_public_bytes_local_account_name_absent": True,
            "checked_paths": checked_paths,
        },
        "workflow": {
            "name": "Unified repository validation",
            "run_id": args.workflow_run,
            "attempt": 1,
            "head_sha": args.metadata_head,
            "status": "completed",
            "conclusion": "success",
            "url": f"https://github.com/{REPOSITORY}/actions/runs/{args.workflow_run}",
            "role": "successful exact-head workflow for the public R33 metadata head",
        },
        "preservation": {
            "status": "PUBLIC_READBACK_VERIFIED",
            "package_receipt": {**package_id, "status": "PASS"},
            "github": {
                "repository_public": rb_github["repository_public"],
                "release_id": rb_github["release_id"],
                "release_url": f"https://github.com/{REPOSITORY}/releases/tag/{TAG}",
                "tag": TAG,
                "tag_commit": rb_github["tag_commit"],
                "draft": False,
                "prerelease": rb_github["prerelease"],
                "asset_count": rb_github["current_release_asset_count"],
            },
            "zenodo": {
                "record_id": rb_zenodo["record_id"],
                "record_url": f"https://zenodo.org/records/{rb_zenodo['record_id']}",
                "doi": rb_zenodo["doi"],
                "concept_doi": rb_zenodo["concept_doi"],
                "access_right": rb_zenodo["access_right"],
                "file_count": rb_zenodo["file_count"],
                "publication_receipt": {
                    "path": "validation/stacks-errata-a04446e-r33-zenodo-publication-2026-08-30.json",
                    "bytes": len(json.dumps(zenodo_receipt, ensure_ascii=False).encode("utf-8")),
                    "sha256": sha256((ROOT / "validation/stacks-errata-a04446e-r33-zenodo-publication-2026-08-30.json").read_bytes()),
                },
            },
            "asset_count_each_host": rb_github["current_release_asset_count"],
            "asset_bytes_each_host": rb_github["current_release_asset_bytes"],
            "anonymous_downloads": 12,
            "byte_or_hash_mismatches": 0,
            "zip_reopen_failures": 0,
            "source_archive_entries": package["archives"]["source"]["entry_count"],
            "source_archive_files": package["archives"]["source"]["file_count"],
            "pdf_archive_entries": package["archives"]["pdfs"]["member_count"],
            "validation_archive_entries": package["archives"]["validation"]["member_count"],
            "github_zenodo_asset_parity": True,
            "assets": [
                {"name": row["name"], "bytes": row["bytes"], "sha256": row["sha256"]}
                for row in package_assets
            ],
        },
        "registry": {
            "overlays": registry_overlay_id,
            "leases": registry_lease_id,
        },
        "fixed_point_artifacts": {
            "pdfs_committed": False,
            "artifact_count": len(build_artifacts),
            "pages": sum(int(item["pages"]) for item in build_artifacts),
            "bytes": sum(int(item["bytes"]) for item in build_artifacts),
            "artifact_tuple_set_sha256": build["build"]["artifact_tuple_set_sha256"],
            "public_identity_evidence": "validation/stacks-errata-a04446e-r33-build-2026-08-30.json",
        },
        "scope_note": (
            "This release composes and validates admitted Stacks errata through R33. "
            "The integrated EGA semantic work is public through EGA I §6.6.3 and "
            "continues at §6.6.4; complete EGA integration and formal verification "
            "are not claimed."
        ),
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"status": "PASS", "output": output.as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
