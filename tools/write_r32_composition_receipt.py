#!/usr/bin/env python3
"""Write the exact R31/R32 composition checkpoint from committed Git objects."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_PUBLIC = "a04636f6cba6ae4adfcbcca72d60bb89eacf7cfd"
PREVIOUS_REGISTRY = "256846d6a4193f21cd6e1af675dc09e6950aa3d6"
REGISTRY_CUTOFF = "cdea2e13a447e7cdcf5f6f805d3a767d907fd679"
REGISTRY_IMPORT = "3f0fa66780213432079c6c3044a6a515508b2576"
SOURCE_COMMIT = "bb81deaa0f922caa8b4b4c1e85d928a03c955b24"
R31_ADMISSION = "1c67a23c057f6a36648d2f855013333cdcb3619c"
R32_ADMISSION = "1a27a8ce494aeabbe65103a655e240947b1d8e8f"


def run(*args: str) -> str:
    completed = subprocess.run(
        list(args), cwd=ROOT, check=True, stdout=subprocess.PIPE, text=True,
        encoding="utf-8", errors="strict",
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def blob_bytes(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "cat-file", "blob", f"{revision}:{path}"], cwd=ROOT,
        check=True, stdout=subprocess.PIPE,
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


def repair_paths() -> list[dict[str, object]]:
    prefix = "candidates/commons/stacks/errata/r31/"
    paths = [
        line for line in git(
            "diff", "--name-only", R31_ADMISSION, REGISTRY_CUTOFF, "--", prefix
        ).splitlines() if line
    ]
    rows: list[dict[str, object]] = []
    for path in paths:
        before = blob_bytes(R31_ADMISSION, path)
        after = blob_bytes(REGISTRY_CUTOFF, path)
        rows.append({
            "path": path,
            "before_git_blob": git("rev-parse", f"{R31_ADMISSION}:{path}"),
            "after_git_blob": git("rev-parse", f"{REGISTRY_CUTOFF}:{path}"),
            "before_sha256": hashlib.sha256(before).hexdigest().upper(),
            "after_sha256": hashlib.sha256(after).hexdigest().upper(),
            "before_bytes": len(before),
            "after_bytes": len(after),
        })
    return rows


def main() -> int:
    old = json.loads((ROOT / "validation/composition-current.json").read_text("utf-8"))
    overlays = json.loads((ROOT / "ai-integrated/registry/overlays.json").read_text("utf-8"))
    entries = overlays["registered_entries"]
    stable_ids: list[str] = []
    for entry in entries:
        raw = entry["stable_ids"]
        stable_ids.extend(raw if isinstance(raw, list) else raw.split())
    if len(entries) != 33 or len(stable_ids) != 1035 or len(set(stable_ids)) != 1035:
        raise RuntimeError("R32 registry counts or global stable-ID uniqueness mismatch")

    command = [
        "python", "tools/compose_overlay_projection.py",
        "--existing-rounds", *[str(n) for n in range(18, 31)],
        "--target-rounds", *[str(n) for n in range(18, 33)],
        "--base-revision", REGISTRY_IMPORT,
        "--check-revision", SOURCE_COMMIT,
    ]
    projection = json.loads(run(*command))
    if projection.get("status") != "PASS" or projection.get("new_operations") != 126:
        raise RuntimeError("R31/R32 projection verifier did not pass")

    affected = {
        name: {**row, "composition_mode": (
            f"{row['new_operations']} manifest-bound exact replacements rebased onto "
            "the verified cumulative source"
        ), "committed_matches_composition": True}
        for name, row in projection["sources"].items()
        if row.get("new_operations")
    }
    for row in affected.values():
        row["authority_git_blob"] = git(
            "hash-object", str(ROOT / "ai-integrated/candidates/commons/stacks/errata" /
            ("r31" if row["new_operations"] == 1 and row["authority_sha256"] ==
             "B7CD92AFF9DF33F05EEAB72C4B55E8AA33F3AEBD947FC53160E87CA80DFFB245"
             else "r32") / "authority/source" /
            next(name for name, value in affected.items() if value is row))
        )
        row["written"] = False

    r31_base = "candidates/commons/stacks/errata/r31"
    r32_base = "candidates/commons/stacks/errata/r32"
    new_overlays = [
        {
            "id": "stacks-errata-a04446e-r31",
            "stable_ids": 1,
            "operations": 1,
            "manifest_sha256": sha(REGISTRY_CUTOFF, f"{r31_base}/candidate.manifest.json"),
            "payload_sha256": sha(REGISTRY_CUTOFF, f"{r31_base}/payload/sites-modules.tex"),
            "review_receipt_sha256": sha(REGISTRY_CUTOFF, f"{r31_base}/replay/independent-review.json"),
            "topology": "repaired_candidate_then_admission",
            "candidate_commit": R31_ADMISSION,
            "candidate_commits": [R31_ADMISSION],
            "candidate_tree": tree(R31_ADMISSION),
            "candidate_subtree": git("rev-parse", f"{REGISTRY_CUTOFF}:{r31_base}"),
            "admission_commit": R31_ADMISSION,
            "admission_tree": tree(R31_ADMISSION),
            "admission_parent": PREVIOUS_REGISTRY,
            "transport_repair": {
                "commit": REGISTRY_CUTOFF,
                "parent": R32_ADMISSION,
                "tree": tree(REGISTRY_CUTOFF),
                "lease_id": "stacks-lease-000035-errata-r31",
                "manifest_sha256_before": sha(R31_ADMISSION, f"{r31_base}/candidate.manifest.json"),
                "manifest_sha256_after": sha(REGISTRY_CUTOFF, f"{r31_base}/candidate.manifest.json"),
                "registry_manifest_sha256_before": sha(R31_ADMISSION, f"{r31_base}/candidate.manifest.json"),
                "intervening_admission_commit": R32_ADMISSION,
                "paths": repair_paths(),
            },
            "lease_release_event": "lease-event-000067",
            "successor_lease_event": "lease-event-000068",
        },
        {
            "id": "stacks-errata-a04446e-r32",
            "stable_ids": 103,
            "operations": 125,
            "manifest_sha256": sha(R32_ADMISSION, f"{r32_base}/candidate.manifest.json"),
            "payload_sha256": sha(R32_ADMISSION, f"{r32_base}/payload/algebra.tex"),
            "payloads": [
                {"path": f"payload/{name}.tex", "sha256": sha(R32_ADMISSION, f"{r32_base}/payload/{name}.tex")}
                for name in ("fields", "categories", "algebra")
            ],
            "review_receipt_sha256": sha(R32_ADMISSION, f"{r32_base}/replay/independent-review.json"),
            "topology": "embedded_candidate_direct_admission",
            "candidate_commit": R32_ADMISSION,
            "candidate_commits": [R32_ADMISSION],
            "candidate_tree": tree(R32_ADMISSION),
            "candidate_subtree": git("rev-parse", f"{R32_ADMISSION}:{r32_base}"),
            "admission_commit": R32_ADMISSION,
            "admission_tree": tree(R32_ADMISSION),
            "admission_parent": R31_ADMISSION,
            "lease_release_event": "lease-event-000069",
        },
    ]

    overlay_path = "ai-integrated/registry/overlays.json"
    lease_path = "ai-integrated/registry/leases.json"
    previous_sources = {
        name: identity(PREVIOUS_PUBLIC, name)
        for name in ("sites-modules.tex", "fields.tex", "categories.tex", "algebra.tex")
    }
    preservation = {
        name: identity(SOURCE_COMMIT, name)
        for name in (
            "artin.tex", "derived.tex", "injectives.tex", "modules.tex",
            "more-algebra.tex", "simplicial.tex", "smoothing.tex", "spaces-duality.tex",
        )
    }
    preservation.update({
        "rejected_producers": ["SIMPLICIAL-007", "MORE-ALGEBRA-J-006", "SMOOTHING-010", "ALGEBRA-007"],
        "unadmitted_packets": [],
        "r31_r32_state": "R31 append-only transport repair and R32 historical materialization imported and composed in registry order",
    })
    stems = list(old["required_build_stems"])
    stems = [stem for index, stem in enumerate(stems) if stem != "fields" or "fields" not in stems[:index]]
    if "fields" not in stems:
        stems.insert(stems.index("artin"), "fields")
    receipt = {
        "schema": "unofficial-ai-integrated-stacks-composition/v3",
        "status": "PASS",
        "created_utc": "2026-08-30T00:00:00Z",
        "authority": old["authority"],
        "previous_cutoff": {
            "public_main_head": PREVIOUS_PUBLIC,
            "public_main_tree": tree(PREVIOUS_PUBLIC),
            "registry_commit": PREVIOUS_REGISTRY,
            "registry_tree": tree(PREVIOUS_REGISTRY),
            "last_admitted_overlay": "stacks-errata-a04446e-r30",
            "source_blobs": previous_sources,
        },
        "registry": {
            "cutoff_commit": REGISTRY_CUTOFF,
            "cutoff_tree": tree(REGISTRY_CUTOFF),
            "post_admission_successor": REGISTRY_CUTOFF,
            "overlays_path": overlay_path,
            **{f"overlays_{key}": value for key, value in identity(REGISTRY_IMPORT, overlay_path).items()},
            "linear_import_commit": REGISTRY_IMPORT,
            "linear_import_tree": tree(REGISTRY_IMPORT),
            "registered_overlays": 33,
            "registered_stable_ids": 1035,
            "last_admitted_overlay": "stacks-errata-a04446e-r32",
            "leases_path": lease_path,
            **{f"leases_{key}": value for key, value in identity(REGISTRY_IMPORT, lease_path).items()},
        },
        "new_overlays": new_overlays,
        "composition": {
            "mode": "manifest-bound registry-order replay rebased onto verified cumulative source",
            "base_commit": REGISTRY_IMPORT,
            "base_tree": tree(REGISTRY_IMPORT),
            "source_commit": SOURCE_COMMIT,
            "source_tree": tree(SOURCE_COMMIT),
            "total_v2_operations": 1159,
            "new_operations": 126,
            "r1_r3_replacements": old["composition"]["r1_r3_replacements"],
            "r1_tag_additions": old["composition"]["r1_tag_additions"],
            "affected_sources": affected,
        },
        "preservation": preservation,
        "known_admitted_metadata_defects": old["known_admitted_metadata_defects"],
        "projection_verifier": {
            "path": "tools/compose_overlay_projection.py",
            "command": " ".join(command),
            "status": "PASS",
        },
        "required_build_stems": stems,
    }
    destination = ROOT / "validation/composition-current.json"
    destination.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", "utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS", "path": destination.relative_to(ROOT).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest().upper(),
        "registered_overlays": 33, "registered_stable_ids": 1035,
        "total_v2_operations": 1159, "new_operations": 126,
        "required_build_stems": len(stems),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
