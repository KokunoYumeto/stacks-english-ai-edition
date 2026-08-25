#!/usr/bin/env python3
"""Deterministically materialize the EGA Stacks overlay candidate.

The source of truth is Git object data at immutable commits. Worktree TeX,
mapping ledgers, QA files, and build outputs are never trusted as evidence.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path


BASE = "a04446e57ec1fbc252a871afcec7752fb2807b14"
BASE_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
SOURCE = "dc37296a6ed6cc2947ee0c2c9c5d4c88195cb322"
SOURCE_TREE = "17cb12a27ccc058d0dbd92f08b3a9b38f1af19ca"
PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[1]
PAYLOAD_PATHS = [
    "algebra.tex",
    "more-algebra.tex",
    "more-morphisms.tex",
    "morphisms.tex",
    "properties.tex",
    "schemes.tex",
]
LOCAL_EDGE_IDS = [
    "S000022", "S000031", "S000057", "S000450", "S000720", "S000729",
    "S000739", "S000791", "S000794", "S000799", "S000825", "S000837",
    "S000852",
]
LOCAL_RESIDUAL_IDS = [
    "R000578", "R000579", "R000580", "R000581", "R000582", "R000583",
    "R000584", "R000585", "R000586", "R000587", "R000588", "R000589",
    "R000605",
]
DECISION_IDS = [
    "D000015", "D000019", "D000024", "D000029", "D000134", "D000191", "D000192",
    "D000193", "D000200", "D000201", "D000210", "D000211", "D000213",
    "D000229", "D000234", "D000235", "D000237",
]
ISSUE_IDS = ["I000014", "I000060", "I000061"]
AGENT_IDS = [
    "A000020", "A000021", "A000022", "A000023", "A000029", "A000041",
    "A000044", "A000046", "A000162", "A000163", "A000169", "A000170",
    "A000189", "A000202", "A000211", "A000217",
]
NEW_LABELS = [
    ("algebra.tex", "algebra-lemma-open-containing-vanishing-jacobson-radical", "spectrum-topology"),
    ("algebra.tex", "algebra-lemma-spec-homeomorphism-onto-image-units", "spectrum-topology"),
    ("properties.tex", "properties-lemma-characterize-quasi-coherent-quasi-affine", "quasi-affine"),
    ("schemes.tex", "schemes-lemma-reduction-functorial", "reduction"),
    ("morphisms.tex", "morphisms-lemma-reduction-morphism-properties", "reduction"),
    ("morphisms.tex", "morphisms-lemma-reductions-fibre-product", "reduction"),
    ("schemes.tex", "schemes-lemma-diagonal-identities", "diagonal"),
]


def run(*args: str) -> bytes:
    return subprocess.check_output(args, cwd=REPO)


def git_batch(refs: list[str]) -> dict[str, tuple[str, bytes]]:
    completed = subprocess.run(
        ("git", "cat-file", "--batch"), cwd=REPO,
        input=("\n".join(refs) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, check=True,
    )
    stream = io.BytesIO(completed.stdout)
    result: dict[str, tuple[str, bytes]] = {}
    for ref in refs:
        fields = stream.readline().decode("ascii").rstrip("\n").split()
        if len(fields) != 3 or fields[1] != "blob":
            raise RuntimeError(f"unexpected cat-file response for {ref}")
        blob, _, size_text = fields
        data = stream.read(int(size_text))
        if stream.read(1) != b"\n":
            raise RuntimeError(f"missing cat-file separator for {ref}")
        result[ref] = (blob, data)
    if stream.read():
        raise RuntimeError("unexpected trailing cat-file bytes")
    return result


def git_bytes(commit: str, path: str) -> bytes:
    return run("git", "show", f"{commit}:{path}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_json(path: Path, value: object) -> None:
    write(path, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def object_identity(commit: str, path: str) -> dict[str, object]:
    data = git_bytes(commit, path)
    blob = run("git", "rev-parse", f"{commit}:{path}").decode().strip()
    mode = run("git", "ls-tree", commit, "--", path).decode().split()[0]
    return {"path": path, "mode": mode, "bytes": len(data), "sha256": sha(data), "git_blob_sha1": blob}


def split_patch(raw: bytes) -> list[tuple[str, list[str], list[tuple[int, list[str]]]]]:
    text = raw.decode("utf-8")
    parts = re.split(r"(?=^diff --git )", text, flags=re.M)
    result = []
    for part in parts:
        if not part:
            continue
        lines = part.splitlines(keepends=True)
        match = re.match(r"diff --git a/(.+?) b/", lines[0])
        if not match:
            raise RuntimeError("unparseable diff header")
        path = match.group(1)
        first_hunk = next(i for i, line in enumerate(lines) if line.startswith("@@ "))
        header = [line for line in lines[:first_hunk] if not line.startswith("index ")]
        hunks: list[tuple[int, list[str]]] = []
        start = first_hunk
        for i in range(first_hunk + 1, len(lines) + 1):
            if i == len(lines) or lines[i].startswith("@@ "):
                hunk = lines[start:i]
                old_start = int(re.match(r"@@ -(\d+)", hunk[0]).group(1))
                hunks.append((old_start, hunk))
                start = i
        result.append((path, header, hunks))
    return result


def component_for(path: str, old_start: int) -> str:
    table = {
        ("algebra.tex", 3159): "spectrum-topology",
        ("algebra.tex", 3192): "dependent-refactors",
        ("algebra.tex", 3242): "dependent-refactors",
        ("algebra.tex", 3583): "spectrum-topology",
        ("more-algebra.tex", 2340): "dependent-refactors",
        ("more-morphisms.tex", 47): "unrelated-corrections",
        ("more-morphisms.tex", 68): "unrelated-corrections",
        ("morphisms.tex", 11394): "reduction",
        ("properties.tex", 2429): "quasi-affine",
        ("properties.tex", 2976): "unrelated-corrections",
        ("schemes.tex", 2289): "reduction",
        ("schemes.tex", 4018): "diagonal",
    }
    try:
        return table[(path, old_start)]
    except KeyError as exc:
        raise RuntimeError(f"unclassified hunk {path}:{old_start}") from exc


def csv_rows(path: str) -> tuple[list[str], list[dict[str, str]]]:
    raw = git_bytes(SOURCE, path).decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    return list(reader.fieldnames or []), list(reader)


def selected_rows(path: str, id_field: str, ids: list[str]) -> list[dict[str, object]]:
    _, rows = csv_rows(path)
    by_id = {row[id_field]: row for row in rows}
    missing = sorted(set(ids) - set(by_id))
    if missing:
        raise RuntimeError(f"missing {path} rows: {missing}")
    raw_lines = git_bytes(SOURCE, path).splitlines(keepends=True)
    header = raw_lines[0]
    raw_by_id = {}
    for line in raw_lines[1:]:
        first = line.decode("utf-8").split(",", 1)[0]
        raw_by_id[first] = line
    return [
        {
            "id": item_id,
            "row": by_id[item_id],
            "raw_bytes": len(raw_by_id[item_id]),
            "raw_sha256": sha(raw_by_id[item_id]),
            "header_sha256": sha(header),
        }
        for item_id in ids
    ]


def tracked_manifest(prefixes: tuple[str, ...], exclude_qa: bool = False) -> list[dict[str, object]]:
    out = run("git", "ls-tree", "-r", "-z", SOURCE, "--", *prefixes)
    selected = []
    for entry in out.split(b"\0"):
        if not entry:
            continue
        meta, path_b = entry.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        path = path_b.decode()
        is_qa = path.startswith("ega/qa/") or path.startswith("reports/qa/")
        if exclude_qa and is_qa:
            continue
        if not exclude_qa and not is_qa:
            continue
        selected.append((path, mode, blob))
    objects = git_batch([blob for _, _, blob in selected])
    rows = []
    for path, mode, blob in selected:
        actual_blob, data = objects[blob]
        if actual_blob != blob:
            raise RuntimeError(f"blob identity mismatch for {path}")
        rows.append({"path": path, "mode": mode, "git_blob_sha1": blob, "bytes": len(data), "sha256": sha(data)})
    return sorted(rows, key=lambda row: row["path"])


def manifest_identity(rows: list[dict[str, object]]) -> dict[str, object]:
    raw = (json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return {"files": len(rows), "bytes": sum(int(row["bytes"]) for row in rows), "serialized_bytes": len(raw), "serialized_sha256": sha(raw)}


def main() -> None:
    if run("git", "rev-parse", f"{BASE}^{{tree}}").decode().strip() != BASE_TREE:
        raise RuntimeError("upstream tree mismatch")
    if run("git", "rev-parse", f"{SOURCE}^{{tree}}").decode().strip() != SOURCE_TREE:
        raise RuntimeError("source tree mismatch")
    if run("git", "merge-base", BASE, SOURCE).decode().strip() != BASE:
        raise RuntimeError("source is not based on pinned upstream")

    custody = run(
        "git", "diff", "--binary", "--full-index", "--no-renames", "--no-ext-diff",
        f"{BASE}..{SOURCE}", "--", *PAYLOAD_PATHS,
    )
    write(PACKAGE / "payload/custody.patch", custody)
    parsed = split_patch(custody)
    components: dict[str, list[str]] = {name: [] for name in [
        "spectrum-topology", "quasi-affine", "reduction", "diagonal",
        "dependent-refactors", "unrelated-corrections",
    ]}
    operations = []
    for path, header, hunks in parsed:
        grouped: dict[str, list[list[str]]] = {}
        for old_start, hunk in hunks:
            component = component_for(path, old_start)
            grouped.setdefault(component, []).append(hunk)
            hunk_raw = "".join(hunk).encode("utf-8")
            operations.append({
                "operation_id": f"ega-v1:{component}:{path}:{old_start}",
                "path": path,
                "base_old_line": old_start,
                "class": component.replace("-", "_"),
                "hunk_bytes": len(hunk_raw),
                "hunk_sha256": sha(hunk_raw),
            })
        for component, component_hunks in grouped.items():
            components[component].extend(header)
            for hunk in component_hunks:
                components[component].extend(hunk)

    component_records = []
    for component in sorted(components):
        raw = "".join(components[component]).encode("utf-8")
        path = PACKAGE / f"payload/components/{component}.patch"
        write(path, raw)
        component_records.append({"id": f"ega-v1:{component}", "path": path.relative_to(PACKAGE).as_posix(), "bytes": len(raw), "sha256": sha(raw)})

    files = []
    for path in PAYLOAD_PATHS:
        files.append({"path": path, "base": object_identity(BASE, path), "result": object_identity(SOURCE, path), "rights_class": "upstream_gfdl_derivative"})
    write_json(PACKAGE / "payload/files.json", {"schema": "mc-stacks-overlay-files/v1", "files": files})
    write_json(PACKAGE / "payload/operations.json", {"schema": "mc-stacks-overlay-operations/v1", "operations": sorted(operations, key=lambda row: row["operation_id"])})

    smap_rows = selected_rows("ega/smap.csv", "edge_id", LOCAL_EDGE_IDS)
    resid_rows = selected_rows("ega/resid.csv", "residual_id", LOCAL_RESIDUAL_IDS)
    decisions = selected_rows("ega/dec.csv", "decision_id", DECISION_IDS)
    issues = selected_rows("ega/issues.csv", "issue_id", ISSUE_IDS)
    agents = selected_rows("ega/agent.csv", "run_id", AGENT_IDS)
    source_units = sorted({row["row"]["source_unit"] for row in smap_rows})
    stable = {
        "schema": "mc-stacks-overlay-stable-ids/v1",
        "scheme": "stacks-overlay:<upstream-commit>:ega:<file>#<full-label>",
        "overlay_units": [
            {
                "id": f"stacks-overlay:{BASE}:ega:{path}#{label}",
                "file": path,
                "full_label": label,
                "component": component,
                "official_tag": None,
                "upstream_acceptance": False,
            }
            for path, label, component in NEW_LABELS
        ],
        "mapping_edge_ids": LOCAL_EDGE_IDS,
        "source_unit_ids": source_units,
        "residual_ids": LOCAL_RESIDUAL_IDS,
        "decision_ids": DECISION_IDS,
    }
    write_json(PACKAGE / "payload/stable-ids.json", stable)

    controls = tracked_manifest(("ega", "reports"), exclude_qa=True)
    qa = tracked_manifest(("ega/qa", "reports/qa"), exclude_qa=False)
    write_json(PACKAGE / "evidence/control-files.json", {"schema": "mc-stacks-evidence-file-closure/v1", "source_commit": SOURCE, "summary": manifest_identity(controls), "files": controls})
    write_json(PACKAGE / "evidence/qa-closure.json", {"schema": "mc-stacks-qa-closure/v1", "source_commit": SOURCE, "summary": manifest_identity(qa), "files": qa})
    write_json(PACKAGE / "evidence/review-rows.json", {
        "schema": "mc-stacks-overlay-review-rows/v1",
        "source_commit": SOURCE,
        "mapping_edges": smap_rows,
        "mirror_residuals": resid_rows,
        "decisions": decisions,
        "issues_for_separate_corrections": issues,
        "audit_runs": agents,
    })

    rights = {
        "schema": "mc-stacks-overlay-rights/v1",
        "metadata_license": "CC0-1.0",
        "content_license": "GFDL-1.2-or-later",
        "upstream_license_identity": "GNU Free Documentation License Version 1.2, November 2002",
        "upstream_copying": {
            "path": "COPYING", "git_blob_sha1": "71ec2c40b4c76362e1d1e9ece69939e7eb8b0908",
            "bytes": 20404, "sha256": "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85",
        },
        "history_preserved": True,
        "source_delivery_method": "exact base lock plus canonical patches and source repository commits",
        "endorsement_claimed": False,
        "ai_produced": True,
        "file_rights_classes": ["commons_cc0_control", "upstream_gfdl_derivative", "mixed_review_required", "reference_only_no_payload"],
        "review_state": "review_required",
        "review_receipt": None,
        "admission_gate": "blocked_until_hash_bound_approved_rights_receipt",
    }
    write_json(PACKAGE / "rights/rights.json", rights)

    bind_paths = [
        ".gitattributes", "README.md", "build_candidate.py", "validate.py", "schema/candidate.schema.json",
        "payload/custody.patch", "payload/files.json", "payload/operations.json", "payload/stable-ids.json",
        "evidence/control-files.json", "evidence/qa-closure.json", "evidence/review-rows.json", "rights/rights.json",
    ] + [record["path"] for record in component_records]
    package_files = []
    for rel in sorted(bind_paths):
        data = (PACKAGE / rel).read_bytes()
        if rel.endswith(".patch"):
            rights_class = "upstream_gfdl_derivative"
        elif rel == "evidence/review-rows.json":
            rights_class = "mixed_review_required"
        else:
            rights_class = "commons_cc0_control"
        package_files.append({"path": rel, "bytes": len(data), "sha256": sha(data), "rights_class": rights_class})

    manifest = {
        "schema": "stacks-ega-prelease-overlay-export/v1",
        "id": "mc-stacks-overlay-ega-integration-v1",
        "kind": "stacks_source_overlay_prelease_export",
        "namespace": "commons/stacks/overlay/ega/integration/v1",
        "lifecycle_state": "prelease_export_prepared",
        "created_at_utc": "2026-08-12T22:30:00Z",
        "producer": {"id": "stacks-ega-codex-single-writer", "role": "candidate_exporter", "source_task": "019fca5a-bcf8-7813-93dd-1adff100c52d"},
        "upstream": {
            "repository": "https://github.com/stacks/stacks-project", "commit": BASE, "tree": BASE_TREE,
            "sidecar_lock_path": "upstream/stacks.lock.json", "license_blob_sha1": "71ec2c40b4c76362e1d1e9ece69939e7eb8b0908",
            "license_sha256": "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85",
        },
        "source_branch": {
            "repository": "https://github.com/KokunoYumeto/stacks-project", "ref": "refs/heads/codex/ega-scaffold",
            "content_commit": SOURCE, "content_tree": SOURCE_TREE, "custody_commit": SOURCE, "custody_tree": SOURCE_TREE,
        },
        "payload": {
            "format": "git_diff_binary_v1", "base_commit": BASE, "source_commit": SOURCE,
            "custody_patch": {"path": "payload/custody.patch", "bytes": len(custody), "sha256": sha(custody)},
            "changed_paths": PAYLOAD_PATHS, "component_patches": component_records,
            "files_manifest": "payload/files.json", "operations_manifest": "payload/operations.json",
            "classification": {"formalization_core": ["spectrum-topology", "quasi-affine", "reduction", "diagonal"], "dependent_refactors": ["dependent-refactors"], "unrelated_corrections": ["unrelated-corrections"]},
            "wholesale_merge_permitted": False,
        },
        "provenance": {
            "corpus_id": "EGA-I", "source_receipts": sorted({row["row"]["source_receipt"] for row in smap_rows}),
            "source_receipt_hashes": sorted({row["row"]["source_receipt_sha256"] for row in smap_rows}),
            "source_units_count": len(source_units), "mapping_edges_count": len(LOCAL_EDGE_IDS),
            "control_closure": "evidence/control-files.json", "qa_closure": "evidence/qa-closure.json",
            "no_french_source_prose_copied_into_package_metadata": True,
            "source_corpus_mutated": False, "translator_tree_written": False,
        },
        "stable_ids": {"path": "payload/stable-ids.json", "count": len(NEW_LABELS), "mapping_edges": len(LOCAL_EDGE_IDS)},
        "rights": {"path": "rights/rights.json", "state": "review_required", "admission_ready": False},
        "review": {
            "mathematical_state": "hard_pass_integrated_local_mirror", "source_state": "authority_receipts_bound",
            "build_state": "passed_with_historical_failure_preserved", "privacy_state": "passed",
            "reader_prose_state": "passed", "official_tag_state": "none_assigned",
            "independent_review_state": "performed_for_local_mirror_not_sidecar_admission", "receipt_path": "evidence/review-rows.json",
        },
        "replay": {
            "build_command": "python commons-candidates/mc-stacks-overlay-ega-integration-v1/build_candidate.py",
            "validate_command": "python commons-candidates/mc-stacks-overlay-ega-integration-v1/validate.py",
            "admission_command": "python commons-candidates/mc-stacks-overlay-ega-integration-v1/validate.py --admission",
            "expected_source_tree": SOURCE_TREE,
            "state": "source_repository_local_replay_only_sidecar_rebuild_required",
        },
        "dependencies": [
            {"component": "dependent-refactors", "requires": ["spectrum-topology"]},
            {"component": "reduction", "order": ["schemes-lemma-reduction-functorial", "morphisms-lemma-reduction-morphism-properties", "morphisms-lemma-reductions-fibre-product"]},
        ],
        "conflicts": [{"kind": "namespace_lease", "state": "not_yet_allocated", "sidecar": "https://github.com/KokunoYumeto/mathematics-commons-stacks"}],
        "supersedes": [],
        "package_files": package_files,
        "notes": [
            "The custody patch is evidence and must not be admitted wholesale.",
            "No official Stacks tag or upstream acceptance is claimed.",
            "No translator tree or locale branch was written.",
            "Rights review is centralized and remains fail-closed.",
            "This pre-lease export is not a central sidecar candidate and must be rebuilt under a future leased path.",
        ],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    manifest_raw = (PACKAGE / "manifest.json").read_bytes()
    proposal = {
        "schema": "stacks-ega-prelease-overlay-registry-proposal/v1",
        "status": "prelease_export_only_not_sidecar_candidate",
        "target_repository": "https://github.com/KokunoYumeto/mathematics-commons-stacks",
        "export_id": manifest["id"], "proposed_namespace": manifest["namespace"], "writer": manifest["producer"]["id"],
        "source_commit": SOURCE, "source_tree": SOURCE_TREE,
        "sidecar_candidate_manifest_path": None,
        "source_export_manifest_path": f"commons-candidates/{manifest['id']}/manifest.json",
        "source_export_manifest_bytes": len(manifest_raw), "source_export_manifest_sha256": sha(manifest_raw),
        "rights_state": "review_required", "review_state": "local_mirror_reviewed_sidecar_admission_not_performed",
        "lease_state": "awaiting_sidecar_registry_lease", "admitted_at_utc": None,
    }
    write_json(PACKAGE / "registry-proposal.json", proposal)


if __name__ == "__main__":
    main()
