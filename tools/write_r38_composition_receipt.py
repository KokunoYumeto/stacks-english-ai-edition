#!/usr/bin/env python3
"""Bind the R34--R38 cumulative composition to its actual committed lineage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from write_r33_composition_receipt import (
    ROOT, blob_bytes, commit_utc, git, identity, run, sha, tree,
)

PREVIOUS_PUBLIC = "d4a2a2d40bee38ae8505fcfd98fcd1a757038f3d"
PREVIOUS_REGISTRY = "acb48c7edaf9595b542b003ed360399870188b7f"
IMPORTS = [
    (34, "cf44258b59a2a0189897367b90d131eb36af3d34", "e731c22f18bac7e841cbebef68df13489c2023b9"),
    (35, "fd63306e7896a1cbafebb49e10735dbe82405d0d", "546452e8a175203979640ce0e76a6f2c769a93cb"),
    (36, "4a49f441ee535dc7de7fbaa9e702d19e48a5336a", "dc1903c46d9e2b990cd6e73eac7509ad365d2f10"),
    (37, "f6395eb5d171cc517a7231811fabf6855296505e", "30e566fd0b25627b89e23c0182a4543bfa90b541"),
    (38, "69f14d67c3a456c3d1447e1a201bdfc3f3d87f0c", "e4978987d5bf67f09a1b7649bda6fd90fe0fb2d8"),
]
EXPECTED_SOURCES = {
    "cohomology.tex": "591F19389EF437DDFE05B00214064DDA31AA225D44B019A779F9F98F6EC0B4DE",
    "sites-cohomology.tex": "DDDCD6951A94B839540D4EBB35F03A34AEDB6D30516B63A55385BA6D8F5CB98B",
    "more-algebra.tex": "0490028F82EFFCF08C0D790D0C8145EEB8D55DB66BFB8CF7BA29CCD27FC3FABE",
}


def exact_commit(value: str) -> str:
    commit = git("rev-parse", f"{value}^{{commit}}")
    if len(commit) != 40:
        raise ValueError("invalid exact commit")
    return commit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    source_commit = exact_commit(args.source_commit)
    parents = git("rev-list", "--parents", "-n", "1", source_commit).split()[1:]
    if len(parents) != 1:
        raise ValueError("source composition must have exactly one parent")
    base = parents[0]
    cutoff, imported = IMPORTS[-1][1:]
    previous = json.loads(blob_bytes(PREVIOUS_PUBLIC, "validation/composition-current.json"))
    overlays = json.loads(blob_bytes(imported, "ai-integrated/registry/overlays.json"))
    leases = json.loads(blob_bytes(cutoff, "registry/leases.json"))
    entries = overlays["registered_entries"]
    all_ids = [stable_id for entry in entries for stable_id in
               (entry["stable_ids"] if isinstance(entry["stable_ids"], list)
                else entry["stable_ids"].split())]
    if len(entries) != 39 or len(all_ids) != 1106 or len(set(all_ids)) != 1106:
        raise ValueError("R38 registry count or uniqueness mismatch")
    if [entry["id"] for entry in entries[-5:]] != [
        f"stacks-errata-a04446e-r{number}" for number, _, _ in IMPORTS
    ]:
        raise ValueError("R34--R38 registry order mismatch")

    command = [sys.executable, "tools/compose_overlay_projection.py",
               "--existing-rounds", *map(str, range(18, 34)),
               "--target-rounds", *map(str, range(18, 39)),
               "--base-revision", base, "--check-revision", source_commit]
    projection = json.loads(run(*command))
    if (projection.get("status") != "PASS" or projection.get("new_operations") != 77
            or projection.get("preapplied_operation_ids") != []
            or projection.get("semantic_dispositions", {}).get("consumed_operation_ids")
            != ["MC-STK-ERR-1296-OP1"]):
        raise ValueError("R38 projection or exact semantic-disposition consumption mismatch")
    affected = {}
    for name, row in projection["sources"].items():
        if not row["new_operations"]:
            continue
        if (row["composed_sha256"] != EXPECTED_SOURCES.get(name)
                or not row["matches_target_after"]):
            raise ValueError(f"R38 cumulative source mismatch: {name}")
        if identity(PREVIOUS_PUBLIC, name)["git_blob"] != row["before_git_blob"]:
            raise ValueError(f"source changed before composition: {name}")
        affected[name] = {
            **row,
            "composition_mode": "Exact manifest-bound operations on cumulative source; separately hash-bound ancestor-rewrite disposition where recorded",
            "committed_matches_composition": True,
            "authority_git_blob": git("rev-parse", f"{previous['authority']['commit']}:{name}"),
            "written": False,
        }
    if set(affected) != set(EXPECTED_SOURCES):
        raise ValueError("affected source inventory mismatch")
    changed = git("diff", "--name-only", "--no-renames", base, source_commit).splitlines()
    if sorted(changed) != sorted(EXPECTED_SOURCES):
        raise ValueError("source commit contains changes outside exact affected sources")

    new_overlays = []
    round_reports = {row["round"]: row for row in projection["overlays"]}
    for number, admission, imported_commit in IMPORTS:
        path = f"candidates/commons/stacks/errata/r{number}"
        report = round_reports[number]
        payloads = [{"path": f"payload/{name}", "sha256": row["sha256"]}
                    for name, row in sorted(report["sources"].items())]
        release_events = [event for event in leases["events"]
                          if event.get("namespace") == f"commons/stacks/errata/r{number}"
                          and event.get("event") == "released"]
        if len(release_events) != 1:
            raise ValueError(f"ambiguous release event: R{number}")
        new_overlays.append({
            "id": report["overlay_id"], "stable_ids": report["stable_ids"],
            "operations": sum(row["operations"] for row in report["sources"].values()),
            "manifest_sha256": sha(admission, f"{path}/candidate.manifest.json"),
            "payload_sha256": payloads[0]["sha256"], "payloads": payloads,
            "review_receipt_sha256": sha(admission, f"{path}/replay/independent-review.json"),
            "topology": "embedded_candidate_direct_admission",
            "candidate_commit": admission, "candidate_commits": [admission],
            "candidate_tree": tree(admission),
            "candidate_subtree": git("rev-parse", f"{admission}:{path}"),
            "admission_commit": admission, "admission_tree": tree(admission),
            "admission_parent": git("rev-parse", f"{admission}^"),
            "lease_release_event": release_events[0]["event_id"],
        })
    preparations = []
    for revision in git("rev-list", "--reverse", f"{imported}..{base}").splitlines():
        preparations.append({
            "commit": revision, "parent": git("rev-parse", f"{revision}^"),
            "tree": tree(revision),
            "paths": git("diff", "--name-only", "--no-renames", f"{revision}^", revision).splitlines(),
        })
    preservation = dict(previous.get("preservation", {}))
    for name in ("algebra.tex", "artin.tex", "categories.tex", "derived.tex",
                 "fields.tex", "injectives.tex", "modules.tex", "more-algebra.tex",
                 "simplicial.tex", "sites-modules.tex", "smoothing.tex",
                 "spaces-duality.tex", "spaces-morphisms.tex"):
        preservation[name] = identity(source_commit, name)
        if name not in affected and identity(PREVIOUS_PUBLIC, name) != preservation[name]:
            raise ValueError(f"unaffected source changed: {name}")
    preservation["r34_r38_state"] = "Five ordered immutable admissions; 77 accepted operations, 76 applied byte edits, one proved earlier structural rewrite. Prior integrated additions and rejected-producer exclusions preserved."
    stems = list(previous["required_build_stems"])
    position = stems.index("injectives") + 1
    for name in ("cohomology", "sites-cohomology"):
        if name not in stems:
            stems.insert(position, name)
            position += 1
    overlay_path = "ai-integrated/registry/overlays.json"
    lease_path = "ai-integrated/registry/leases.json"
    receipt = {
        "schema": "unofficial-ai-integrated-stacks-composition/v3", "status": "PASS",
        "created_utc": commit_utc(source_commit), "authority": previous["authority"],
        "previous_cutoff": {
            "public_main_head": PREVIOUS_PUBLIC, "public_main_tree": tree(PREVIOUS_PUBLIC),
            "registry_commit": PREVIOUS_REGISTRY, "registry_tree": tree(PREVIOUS_REGISTRY),
            "last_admitted_overlay": "stacks-errata-a04446e-r33",
            "source_blobs": {name: identity(PREVIOUS_PUBLIC, name) for name in affected},
        },
        "registry": {
            "cutoff_commit": cutoff, "cutoff_tree": tree(cutoff),
            "post_admission_successor": cutoff, "overlays_path": overlay_path,
            **{f"overlays_{key}": value for key, value in identity(imported, overlay_path).items()},
            "linear_import_commit": imported, "linear_import_tree": tree(imported),
            "linear_import_chain": [{"registry_commit": admission,
                                     "import_commit": target, "import_tree": tree(target)}
                                    for _, admission, target in IMPORTS],
            "registered_overlays": 39, "registered_stable_ids": 1106,
            "last_admitted_overlay": "stacks-errata-a04446e-r38", "leases_path": lease_path,
            **{f"leases_{key}": value for key, value in identity(imported, lease_path).items()},
        },
        "new_overlays": new_overlays,
        "composition": {
            "mode": "manifest-bound registry-order replay rebased onto verified cumulative source",
            "base_commit": base, "base_tree": tree(base),
            "preparation_commits": preparations,
            "source_commit": source_commit, "source_tree": tree(source_commit),
            "total_v2_operations": previous["composition"]["total_v2_operations"] + 77,
            "new_operations": 77, "new_byte_edit_operations": 76,
            "semantic_dispositions": projection["semantic_dispositions"],
            "r1_r3_replacements": previous["composition"]["r1_r3_replacements"],
            "r1_tag_additions": previous["composition"]["r1_tag_additions"],
            "affected_sources": affected,
        },
        "preservation": preservation,
        "known_admitted_metadata_defects": previous.get("known_admitted_metadata_defects", []) + [{
            "overlay": "stacks-errata-a04446e-r38", "stable_id": "MC-STK-ERR-1345",
            "disposition": "Optional equivalent summation-notation normalization, not repair of invalid mathematical notation; original and replacement are both valid. Immutable admission retained; do not describe this unit as a substantive mathematical defect.",
        }, {
            "overlay": "stacks-errata-a04446e-r38",
            "path": "candidates/commons/stacks/errata/r38/REGENERATION_RECEIPT.json",
            "field": "independent_review",
            "stale_reference": {"bytes": 5706, "sha256": "1C82ED4A65BA9D1FDAF9076E46C060C2BACD98269FF3B6143DBE9A1318A9CCE9"},
            "final_manifest_bound_review": {"bytes": 4172, "sha256": "1DB05892DD5F76C055432B4CB28E52273F41C3C9023A46C4E635AA6630C11AFD"},
            "disposition": "Direct final manifest closure passes; the earlier regeneration receipt has a stale transitive review pointer. Preserve immutable bytes and use the final manifest-bound review above. A registrar clarification was requested. Historical private raster references are not claimed independently transported; fresh cumulative build and visual QA remain required.",
        }],
        "projection_verifier": {"path": "tools/compose_overlay_projection.py",
                                "command": " ".join(["python", *command[1:]]), "status": "PASS"},
        "required_build_stems": stems,
    }
    destination = ROOT / "validation/composition-current.json"
    destination.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "path": destination.relative_to(ROOT).as_posix(),
                      "registered_overlays": 39, "stable_ids": 1106,
                      "new_operations": 77, "new_byte_edits": 76,
                      "required_build_stems": len(stems)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
