#!/usr/bin/env python3
"""Write the exact R33 composition checkpoint from committed Git objects."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PUBLIC = "07d48789594324dd1ee58d1c00aa16778e79e513"
PREVIOUS_REGISTRY = "cdea2e13a447e7cdcf5f6f805d3a767d907fd679"
REGISTRY_CUTOFF = "acb48c7edaf9595b542b003ed360399870188b7f"
REGISTRY_IMPORT = "98d095ed892a8d3e3c9248048e5df7e1dda84fbe"
SOURCE_COMMIT = "458077f743a30774a4e00be1e1946f5e253b7c17"
OVERLAY_ID = "stacks-errata-a04446e-r33"
R33_BASE = "candidates/commons/stacks/errata/r33"


def run(*args: str) -> str:
    completed = subprocess.run(
        list(args),
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def blob_bytes(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{revision}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def identity(revision: str, path: str) -> dict[str, object]:
    data = blob_bytes(revision, path)
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest().upper(),
        "git_blob": git("rev-parse", f"{revision}:{path}"),
    }


def tree(revision: str) -> str:
    return git("rev-parse", f"{revision}^{{tree}}")


def sha(revision: str, path: str) -> str:
    return hashlib.sha256(blob_bytes(revision, path)).hexdigest().upper()


def commit_utc(revision: str) -> str:
    value = git("show", "-s", "--format=%cI", revision)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    previous = json.loads(
        (ROOT / "validation/composition-current.json").read_text(encoding="utf-8")
    )
    overlays = json.loads(
        (ROOT / "ai-integrated/registry/overlays.json").read_text(encoding="utf-8")
    )
    entries = overlays["registered_entries"]
    stable_ids: list[str] = []
    for entry in entries:
        raw = entry["stable_ids"]
        stable_ids.extend(raw if isinstance(raw, list) else raw.split())
    if (
        len(entries) != 34
        or entries[-1].get("id") != OVERLAY_ID
        or len(stable_ids) != 1042
        or len(set(stable_ids)) != 1042
    ):
        raise RuntimeError("R33 registry counts, cutoff, or stable-ID uniqueness mismatch")

    existing_rounds = [str(number) for number in range(18, 33)]
    target_rounds = [str(number) for number in range(18, 34)]
    command = [
        "python",
        "tools/compose_overlay_projection.py",
        "--existing-rounds",
        *existing_rounds,
        "--target-rounds",
        *target_rounds,
        "--base-revision",
        REGISTRY_IMPORT,
        "--check-revision",
        SOURCE_COMMIT,
    ]
    projection = json.loads(run(*command))
    if (
        projection.get("status") != "PASS"
        or projection.get("new_operations") != 7
        or projection.get("preapplied_operation_ids") != []
    ):
        raise RuntimeError("R33 projection verifier did not pass exactly seven new edits")
    source_row = projection["sources"].get("spaces-morphisms.tex")
    if (
        not isinstance(source_row, dict)
        or source_row.get("new_operations") != 7
        or source_row.get("composed_sha256")
        != "048BC16D80E71DBAA9C5CF11B109B69B481D920B278CBCB379C3BC9B8BBFC252"
    ):
        raise RuntimeError("R33 spaces-morphisms projection identity mismatch")
    affected = {
        "spaces-morphisms.tex": {
            **source_row,
            "composition_mode": (
                "7 manifest-bound exact replacements rebased onto the verified "
                "cumulative source"
            ),
            "committed_matches_composition": True,
            "authority_git_blob": git(
                "hash-object",
                str(
                    ROOT
                    / "ai-integrated/candidates/commons/stacks/errata/r33/authority/source/spaces-morphisms.tex"
                ),
            ),
            "written": False,
        }
    }

    overlay_path = "ai-integrated/registry/overlays.json"
    lease_path = "ai-integrated/registry/leases.json"
    previous_source = {"spaces-morphisms.tex": identity(PREVIOUS_PUBLIC, "spaces-morphisms.tex")}
    new_overlay = {
        "id": OVERLAY_ID,
        "stable_ids": 7,
        "operations": 7,
        "manifest_sha256": sha(REGISTRY_CUTOFF, f"{R33_BASE}/candidate.manifest.json"),
        "payload_sha256": sha(
            REGISTRY_CUTOFF, f"{R33_BASE}/payload/spaces-morphisms.tex"
        ),
        "payloads": [
            {
                "path": "payload/spaces-morphisms.tex",
                "sha256": sha(
                    REGISTRY_CUTOFF, f"{R33_BASE}/payload/spaces-morphisms.tex"
                ),
            }
        ],
        "review_receipt_sha256": sha(
            REGISTRY_CUTOFF, f"{R33_BASE}/replay/independent-review.json"
        ),
        "topology": "embedded_candidate_direct_admission",
        "candidate_commit": REGISTRY_CUTOFF,
        "candidate_commits": [REGISTRY_CUTOFF],
        "candidate_tree": tree(REGISTRY_CUTOFF),
        "candidate_subtree": git("rev-parse", f"{REGISTRY_CUTOFF}:{R33_BASE}"),
        "admission_commit": REGISTRY_CUTOFF,
        "admission_tree": tree(REGISTRY_CUTOFF),
        "admission_parent": PREVIOUS_REGISTRY,
        "lease_release_event": "lease-event-000071",
    }

    preservation = dict(previous.get("preservation", {}))
    for name in (
        "algebra.tex",
        "artin.tex",
        "categories.tex",
        "derived.tex",
        "fields.tex",
        "injectives.tex",
        "modules.tex",
        "more-algebra.tex",
        "simplicial.tex",
        "sites-modules.tex",
        "smoothing.tex",
        "spaces-duality.tex",
    ):
        preservation[name] = identity(SOURCE_COMMIT, name)
    preservation["r33_state"] = (
        "R33 append-only registry import and seven canonical spaces-morphisms "
        "operations composed; five locale aliases preserved without duplicate replay"
    )
    preservation["r33_duplicate_aliases_not_applied"] = [
        "P08-E588",
        "P08-E589",
        "P08-E590",
        "P08-E591",
        "P08-E592",
    ]

    stems = list(previous["required_build_stems"])
    if "spaces-morphisms" not in stems:
        anchor = stems.index("more-morphisms") + 1
        stems.insert(anchor, "spaces-morphisms")

    receipt = {
        "schema": "unofficial-ai-integrated-stacks-composition/v3",
        "status": "PASS",
        "created_utc": commit_utc(SOURCE_COMMIT),
        "authority": previous["authority"],
        "previous_cutoff": {
            "public_main_head": PREVIOUS_PUBLIC,
            "public_main_tree": tree(PREVIOUS_PUBLIC),
            "registry_commit": PREVIOUS_REGISTRY,
            "registry_tree": tree(PREVIOUS_REGISTRY),
            "last_admitted_overlay": "stacks-errata-a04446e-r32",
            "source_blobs": previous_source,
        },
        "registry": {
            "cutoff_commit": REGISTRY_CUTOFF,
            "cutoff_tree": tree(REGISTRY_CUTOFF),
            "post_admission_successor": REGISTRY_CUTOFF,
            "overlays_path": overlay_path,
            **{
                f"overlays_{key}": value
                for key, value in identity(REGISTRY_IMPORT, overlay_path).items()
            },
            "linear_import_commit": REGISTRY_IMPORT,
            "linear_import_tree": tree(REGISTRY_IMPORT),
            "registered_overlays": 34,
            "registered_stable_ids": 1042,
            "last_admitted_overlay": OVERLAY_ID,
            "leases_path": lease_path,
            **{
                f"leases_{key}": value
                for key, value in identity(REGISTRY_IMPORT, lease_path).items()
            },
        },
        "new_overlays": [new_overlay],
        "composition": {
            "mode": "manifest-bound registry-order replay rebased onto verified cumulative source",
            "base_commit": REGISTRY_IMPORT,
            "base_tree": tree(REGISTRY_IMPORT),
            "source_commit": SOURCE_COMMIT,
            "source_tree": tree(SOURCE_COMMIT),
            "total_v2_operations": 1166,
            "new_operations": 7,
            "r1_r3_replacements": previous["composition"]["r1_r3_replacements"],
            "r1_tag_additions": previous["composition"]["r1_tag_additions"],
            "affected_sources": affected,
        },
        "preservation": preservation,
        "known_admitted_metadata_defects": previous.get(
            "known_admitted_metadata_defects", []
        ),
        "projection_verifier": {
            "path": "tools/compose_overlay_projection.py",
            "command": " ".join(command),
            "status": "PASS",
        },
        "required_build_stems": stems,
    }
    destination = ROOT / "validation/composition-current.json"
    destination.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": destination.relative_to(ROOT).as_posix(),
                "bytes": destination.stat().st_size,
                "sha256": hashlib.sha256(destination.read_bytes()).hexdigest().upper(),
                "registered_overlays": 34,
                "registered_stable_ids": 1042,
                "total_v2_operations": 1166,
                "new_operations": 7,
                "required_build_stems": len(stems),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
