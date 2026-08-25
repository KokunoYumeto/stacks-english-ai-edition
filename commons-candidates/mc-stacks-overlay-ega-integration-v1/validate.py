#!/usr/bin/env python3
"""Validate the source-local pre-lease export; admission mode is a negative preflight."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[1]
SOURCE = "dc37296a6ed6cc2947ee0c2c9c5d4c88195cb322"
TERMINAL_FILES = {
    "manifest.json",
    "registry-proposal.json",
    "validation.json",
    "admission-validation.json",
}
EXPECTED_REVIEW_IDS = {
    "mapping_edges": ["S000022", "S000031", "S000057", "S000450", "S000720", "S000729", "S000739", "S000791", "S000794", "S000799", "S000825", "S000837", "S000852"],
    "mirror_residuals": ["R000578", "R000579", "R000580", "R000581", "R000582", "R000583", "R000584", "R000585", "R000586", "R000587", "R000588", "R000589", "R000605"],
    "decisions": ["D000015", "D000019", "D000024", "D000029", "D000134", "D000191", "D000192", "D000193", "D000200", "D000201", "D000210", "D000211", "D000213", "D000229", "D000234", "D000235", "D000237"],
    "issues_for_separate_corrections": ["I000014", "I000060", "I000061"],
    "audit_runs": ["A000020", "A000021", "A000022", "A000023", "A000029", "A000041", "A000044", "A000046", "A000162", "A000163", "A000169", "A000170", "A000189", "A000202", "A000211", "A000217"],
}
REVIEW_SOURCES = {
    "mapping_edges": ("ega/smap.csv", "edge_id"),
    "mirror_residuals": ("ega/resid.csv", "residual_id"),
    "decisions": ("ega/dec.csv", "decision_id"),
    "issues_for_separate_corrections": ("ega/issues.csv", "issue_id"),
    "audit_runs": ("ega/agent.csv", "run_id"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_json(path: Path) -> object:
    def reject(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key {key} in {path}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject)


def git(*args: str, env: dict[str, str] | None = None) -> bytes:
    return subprocess.check_output(("git", *args), cwd=REPO, env=env)


def git_batch(refs: list[str]) -> dict[str, tuple[str, bytes]]:
    """Read many immutable Git objects through one cat-file process."""
    completed = subprocess.run(
        ("git", "cat-file", "--batch"), cwd=REPO,
        input=("\n".join(refs) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE, check=True,
    )
    stream = io.BytesIO(completed.stdout)
    result: dict[str, tuple[str, bytes]] = {}
    for ref in refs:
        header = stream.readline().decode("ascii").rstrip("\n")
        fields = header.split()
        if len(fields) != 3 or fields[1] != "blob":
            raise ValueError(f"unexpected cat-file header for {ref}: {header}")
        blob, _, size_text = fields
        data = stream.read(int(size_text))
        if stream.read(1) != b"\n":
            raise ValueError(f"missing cat-file record separator for {ref}")
        result[ref] = (blob, data)
    if stream.read():
        raise ValueError("unexpected trailing cat-file bytes")
    return result


def exact_keys(value: object, expected: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        errors.append(f"CLOSED_SHAPE:{label}")


def manifest_identity(rows: list[dict[str, object]]) -> dict[str, object]:
    raw = (json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return {
        "files": len(rows),
        "bytes": sum(int(row["bytes"]) for row in rows),
        "serialized_bytes": len(raw),
        "serialized_sha256": sha(raw),
    }


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
            raise ValueError("unparseable diff header")
        first_hunk = next(i for i, line in enumerate(lines) if line.startswith("@@ "))
        hunks: list[tuple[int, list[str]]] = []
        start = first_hunk
        for i in range(first_hunk + 1, len(lines) + 1):
            if i == len(lines) or lines[i].startswith("@@ "):
                hunk = lines[start:i]
                old_start = int(re.match(r"@@ -(\d+)", hunk[0]).group(1))
                hunks.append((old_start, hunk))
                start = i
        result.append((match.group(1), lines[:first_hunk], hunks))
    return result


def source_paths() -> tuple[set[str], set[str]]:
    raw = git("ls-tree", "-r", "-z", SOURCE, "--", "ega", "reports")
    controls: set[str] = set()
    qa: set[str] = set()
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        path = entry.split(b"\t", 1)[1].decode("utf-8")
        (qa if path.startswith(("ega/qa/", "reports/qa/")) else controls).add(path)
    return controls, qa


def validate_review_rows(review: dict[str, object], errors: list[str]) -> None:
    for group, expected_ids in EXPECTED_REVIEW_IDS.items():
        path, id_field = REVIEW_SOURCES[group]
        raw = git("show", f"{SOURCE}:{path}")
        lines = raw.splitlines(keepends=True)
        header = lines[0]
        parsed = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
        parsed_by_id = {row[id_field]: row for row in parsed}
        raw_by_id = {line.decode("utf-8").split(",", 1)[0]: line for line in lines[1:]}
        records = review[group]
        if not isinstance(records, list) or [record.get("id") for record in records] != expected_ids:
            errors.append(f"REVIEW_ID_SET:{group}")
            continue
        for record in records:
            exact_keys(record, {"header_sha256", "id", "raw_bytes", "raw_sha256", "row"}, f"review.{group}.record", errors)
            item_id = record["id"]
            expected_raw = raw_by_id.get(item_id)
            if expected_raw is None or record["row"] != parsed_by_id.get(item_id):
                errors.append(f"REVIEW_ROW:{group}:{item_id}")
                continue
            if record["raw_bytes"] != len(expected_raw) or record["raw_sha256"] != sha(expected_raw) or record["header_sha256"] != sha(header):
                errors.append(f"REVIEW_RECEIPT:{group}:{item_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--admission", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    blockers: list[str] = []
    checks = {name: False for name in ["anchors", "namespace", "package_files", "patch", "components", "local_edges", "governance", "qa_closure", "schemas", "rights", "privacy"]}
    try:
        manifest = load_json(PACKAGE / "manifest.json")
        schema = load_json(PACKAGE / "schema/candidate.schema.json")
        rights = load_json(PACKAGE / "rights/rights.json")
        proposal = load_json(PACKAGE / "registry-proposal.json")
        exact_keys(proposal, {"admitted_at_utc", "export_id", "lease_state", "proposed_namespace", "review_state", "rights_state", "schema", "sidecar_candidate_manifest_path", "source_commit", "source_export_manifest_bytes", "source_export_manifest_path", "source_export_manifest_sha256", "source_tree", "status", "target_repository", "writer"}, "registry_proposal", errors)
        schema_errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda item: list(item.path))
        if schema_errors:
            errors.extend(f"JSON_SCHEMA:{'/'.join(map(str, item.path))}:{item.validator}" for item in schema_errors)
        required = set(schema["required"])
        allowed = set(schema["properties"])
        if set(manifest) != allowed or not required.issubset(manifest):
            errors.append("MANIFEST_CLOSED_SCHEMA_MISMATCH")
        elif manifest["schema"] != "stacks-ega-prelease-overlay-export/v1":
            errors.append("MANIFEST_SCHEMA_VERSION")
        else:
            checks["schemas"] = True

        exact_keys(manifest["producer"], {"id", "role", "source_task"}, "producer", errors)
        exact_keys(manifest["upstream"], {"commit", "license_blob_sha1", "license_sha256", "repository", "sidecar_lock_path", "tree"}, "upstream", errors)
        exact_keys(manifest["source_branch"], {"content_commit", "content_tree", "custody_commit", "custody_tree", "ref", "repository"}, "source_branch", errors)
        exact_keys(manifest["payload"], {"base_commit", "changed_paths", "classification", "component_patches", "custody_patch", "files_manifest", "format", "operations_manifest", "source_commit", "wholesale_merge_permitted"}, "payload", errors)
        exact_keys(manifest["payload"]["classification"], {"dependent_refactors", "formalization_core", "unrelated_corrections"}, "payload.classification", errors)
        exact_keys(manifest["payload"]["custody_patch"], {"bytes", "path", "sha256"}, "payload.custody_patch", errors)
        for item in manifest["payload"]["component_patches"]:
            exact_keys(item, {"bytes", "id", "path", "sha256"}, "payload.component_patch", errors)
        exact_keys(manifest["provenance"], {"control_closure", "corpus_id", "mapping_edges_count", "no_french_source_prose_copied_into_package_metadata", "qa_closure", "source_corpus_mutated", "source_receipt_hashes", "source_receipts", "source_units_count", "translator_tree_written"}, "provenance", errors)
        exact_keys(manifest["stable_ids"], {"count", "mapping_edges", "path"}, "stable_ids", errors)
        exact_keys(manifest["rights"], {"admission_ready", "path", "state"}, "rights", errors)
        exact_keys(manifest["review"], {"build_state", "independent_review_state", "mathematical_state", "official_tag_state", "privacy_state", "reader_prose_state", "receipt_path", "source_state"}, "review", errors)
        exact_keys(manifest["replay"], {"admission_command", "build_command", "expected_source_tree", "state", "validate_command"}, "replay", errors)
        for item in manifest["conflicts"]:
            exact_keys(item, {"kind", "sidecar", "state"}, "conflict", errors)
        for item in manifest["dependencies"]:
            if "component" not in item or set(item) not in ({"component", "requires"}, {"component", "order"}):
                errors.append("CLOSED_SHAPE:dependency")
        for item in manifest["package_files"]:
            exact_keys(item, {"bytes", "path", "rights_class", "sha256"}, "package_file", errors)

        upstream = manifest["upstream"]
        source = manifest["source_branch"]
        if git("rev-parse", f"{upstream['commit']}^{{tree}}").decode().strip() != upstream["tree"]:
            errors.append("UPSTREAM_TREE")
        if git("rev-parse", f"{source['content_commit']}^{{tree}}").decode().strip() != source["content_tree"]:
            errors.append("SOURCE_TREE")
        if git("merge-base", upstream["commit"], source["content_commit"]).decode().strip() != upstream["commit"]:
            errors.append("MERGE_BASE")
        if not any(code in errors for code in ["UPSTREAM_TREE", "SOURCE_TREE", "MERGE_BASE"]):
            checks["anchors"] = True

        namespace = manifest["namespace"]
        if not re.fullmatch(r"commons/stacks/[a-z0-9][a-z0-9._/-]*", namespace) or ".." in namespace or "\\" in namespace:
            errors.append("NAMESPACE")
        elif manifest["conflicts"][0]["state"] != "not_yet_allocated":
            errors.append("LEASE_STATE")
        else:
            checks["namespace"] = True
            blockers.append("SIDECAR_NAMESPACE_LEASE_NOT_ALLOCATED")
            blockers.append("CENTRAL_CANDIDATE_MANIFEST_NOT_MATERIALIZED")
            blockers.append("PORTABLE_SIDECAR_REBUILD_NOT_PERFORMED")
            blockers.append("INDEPENDENT_SIDECAR_REPLAY_NOT_PERFORMED")

        package_paths = [row["path"] for row in manifest["package_files"]]
        if package_paths != sorted(package_paths) or len(package_paths) != len(set(path.casefold() for path in package_paths)):
            errors.append("PACKAGE_PATH_ORDER_OR_COLLISION")
        for record in manifest["package_files"]:
            rel = record["path"]
            path = PACKAGE / rel
            if Path(rel).is_absolute() or ".." in Path(rel).parts or "\\" in rel or not path.is_file():
                errors.append("PACKAGE_PATH_INVALID")
                continue
            raw = path.read_bytes()
            if len(raw) != record["bytes"] or sha(raw) != record["sha256"]:
                errors.append("PACKAGE_FILE_IDENTITY")
            if b"\r" in raw and path.suffix in {".json", ".md", ".py", ".patch"}:
                errors.append("PACKAGE_CR")
            if path.suffix in {".json", ".md", ".py", ".patch"} and raw and not raw.endswith(b"\n"):
                errors.append("PACKAGE_FINAL_LF")
        actual_paths = {
            path.relative_to(PACKAGE).as_posix()
            for path in PACKAGE.rglob("*")
            if path.is_file()
        }
        allowed_paths = set(package_paths) | TERMINAL_FILES
        if actual_paths - allowed_paths:
            errors.append("PACKAGE_UNLISTED_FILES:" + ",".join(sorted(actual_paths - allowed_paths)))
        if set(package_paths) - actual_paths or not {"manifest.json", "registry-proposal.json"}.issubset(actual_paths):
            errors.append("PACKAGE_MISSING_FILES")
        if not any(code.startswith("PACKAGE_") for code in errors):
            checks["package_files"] = True

        payload = manifest["payload"]
        canonical = git(
            "diff", "--binary", "--full-index", "--no-renames", "--no-ext-diff",
            f"{upstream['commit']}..{source['content_commit']}", "--", *payload["changed_paths"],
        )
        custody = (PACKAGE / payload["custody_patch"]["path"]).read_bytes()
        if custody != canonical or len(custody) != payload["custody_patch"]["bytes"] or sha(custody) != payload["custody_patch"]["sha256"]:
            errors.append("CUSTODY_PATCH")
        else:
            checks["patch"] = True

        component_by_path = {row["path"]: row for row in payload["component_patches"]}
        if set(component_by_path) != {
            "payload/components/dependent-refactors.patch",
            "payload/components/diagonal.patch",
            "payload/components/quasi-affine.patch",
            "payload/components/reduction.patch",
            "payload/components/spectrum-topology.patch",
            "payload/components/unrelated-corrections.patch",
        }:
            errors.append("COMPONENT_SET")
        for rel, record in component_by_path.items():
            raw = (PACKAGE / rel).read_bytes()
            if len(raw) != record["bytes"] or sha(raw) != record["sha256"]:
                errors.append("COMPONENT_METADATA")

        operations = load_json(PACKAGE / payload["operations_manifest"])
        exact_keys(operations, {"operations", "schema"}, "operations", errors)
        expected_operations = []
        component_names = {Path(rel).stem: rel for rel in component_by_path}
        for component, rel in sorted(component_names.items()):
            for path, _, hunks in split_patch((PACKAGE / rel).read_bytes()):
                for old_start, hunk in hunks:
                    raw = "".join(hunk).encode("utf-8")
                    expected_operations.append({
                        "operation_id": f"ega-v1:{component}:{path}:{old_start}",
                        "path": path,
                        "base_old_line": old_start,
                        "class": component.replace("-", "_"),
                        "hunk_bytes": len(raw),
                        "hunk_sha256": sha(raw),
                    })
        expected_operations.sort(key=lambda row: row["operation_id"])
        if operations["schema"] != "mc-stacks-overlay-operations/v1" or operations["operations"] != expected_operations:
            errors.append("OPERATIONS_REPLAY")

        stable = load_json(PACKAGE / "payload/stable-ids.json")
        files = load_json(PACKAGE / "payload/files.json")
        if len(stable["overlay_units"]) != 7 or len(stable["mapping_edge_ids"]) != 13:
            errors.append("STABLE_ID_COUNTS")
        for unit in stable["overlay_units"]:
            base_text = git("show", f"{upstream['commit']}:{unit['file']}").decode("utf-8")
            post_text = git("show", f"{source['content_commit']}:{unit['file']}").decode("utf-8")
            marker = "\\label{" + unit["full_label"].split("-", 1)[1] + "}"
            if marker in base_text or post_text.count(marker) != 1 or unit["official_tag"] is not None or unit["upstream_acceptance"] is not False:
                errors.append("LOCAL_LABEL_CONTRACT")
        for record in files["files"]:
            for role, commit in [("base", upstream["commit"]), ("result", source["content_commit"])]:
                raw = git("show", f"{commit}:{record['path']}")
                if len(raw) != record[role]["bytes"] or sha(raw) != record[role]["sha256"]:
                    errors.append("PAYLOAD_FILE_IDENTITY")
        if not any(code in errors for code in ["STABLE_ID_COUNTS", "LOCAL_LABEL_CONTRACT", "PAYLOAD_FILE_IDENTITY"]):
            checks["local_edges"] = True

        with tempfile.TemporaryDirectory() as temp_name:
            index_path = Path(temp_name) / "candidate.index"
            env = dict(os.environ)
            env["GIT_INDEX_FILE"] = str(index_path)
            subprocess.check_call(("git", "read-tree", upstream["commit"]), cwd=REPO, env=env)
            for component in payload["component_patches"]:
                subprocess.check_call(("git", "apply", "--cached", str(PACKAGE / component["path"])), cwd=REPO, env=env)
            index_rows = subprocess.check_output(
                ("git", "ls-files", "-s", "--", *payload["changed_paths"]),
                cwd=REPO, env=env,
            ).decode("utf-8").splitlines()
            index_blobs = {line.split("\t", 1)[1]: line.split()[1] for line in index_rows}
            expected_blobs = {row["path"]: row["result"]["git_blob_sha1"] for row in files["files"]}
            if index_blobs != expected_blobs:
                errors.append("COMPONENT_POSTIMAGE")
        if "COMPONENT_POSTIMAGE" not in errors:
            checks["components"] = True

        review = load_json(PACKAGE / "evidence/review-rows.json")
        exact_keys(review, {"audit_runs", "decisions", "issues_for_separate_corrections", "mapping_edges", "mirror_residuals", "schema", "source_commit"}, "review", errors)
        if review["source_commit"] != SOURCE:
            errors.append("REVIEW_SOURCE_COMMIT")
        validate_review_rows(review, errors)
        edges = review["mapping_edges"]
        if [row["id"] for row in edges] != stable["mapping_edge_ids"]:
            errors.append("EDGE_SET")
        for item in edges:
            row = item["row"]
            if row["review_state"] != "integrated_local" or row["stacks_commit"] != "LOCAL_WORKTREE" or row["official_tag"] not in ("", None):
                errors.append("EDGE_STATE")
        residuals = review["mirror_residuals"]
        if len(residuals) != 13 or any(item["row"]["status"] != "integrated_local_mirror" for item in residuals):
            errors.append("RESIDUAL_STATE")
        if not any(code in errors for code in ["EDGE_SET", "EDGE_STATE", "RESIDUAL_STATE"]):
            checks["governance"] = True

        closures = [load_json(PACKAGE / rel) for rel in ("evidence/control-files.json", "evidence/qa-closure.json")]
        expected_control_paths, expected_qa_paths = source_paths()
        refs = [record["git_blob_sha1"] for closure in closures for record in closure["files"]]
        objects = git_batch(refs)
        for closure, expected_paths in zip(closures, (expected_control_paths, expected_qa_paths)):
            exact_keys(closure, {"files", "schema", "source_commit", "summary"}, "closure", errors)
            if closure["source_commit"] != SOURCE or {row["path"] for row in closure["files"]} != expected_paths:
                errors.append("EVIDENCE_PATH_SET")
            if closure["summary"] != manifest_identity(closure["files"]):
                errors.append("EVIDENCE_SUMMARY")
            for record in closure["files"]:
                exact_keys(record, {"bytes", "git_blob_sha1", "mode", "path", "sha256"}, "closure.file", errors)
                ref = record["git_blob_sha1"]
                blob, raw = objects[ref]
                path_blob = git("rev-parse", f"{SOURCE}:{record['path']}").decode().strip()
                mode = git("ls-tree", SOURCE, "--", record["path"]).decode().split()[0]
                if len(raw) != record["bytes"] or sha(raw) != record["sha256"] or blob != record["git_blob_sha1"] or path_blob != blob or mode != record["mode"]:
                    errors.append("EVIDENCE_FILE_IDENTITY")
        if len(closures[1]["files"]) != 184:
            errors.append("QA_FILE_COUNT")
        if not any(code in errors for code in ["EVIDENCE_FILE_IDENTITY", "QA_FILE_COUNT"]):
            checks["qa_closure"] = True

        if rights["review_state"] != "review_required" or rights["review_receipt"] is not None or rights["endorsement_claimed"] is not False:
            errors.append("RIGHTS_FAIL_CLOSED_STATE")
        else:
            checks["rights"] = True
            blockers.append("APPROVED_RIGHTS_RECEIPT_ABSENT")

        private_patterns = [
            re.compile(b"[A-Za-z]:" + bytes([92, 92]) + b"Users" + bytes([92, 92])),
            re.compile(b"file" + b"://", re.I),
            re.compile(b"BEGIN " + b"(?:RSA |OPENSSH )?PRIVATE KEY"),
        ]
        privacy_paths = [PACKAGE / rel for rel in sorted(actual_paths)]
        for path in privacy_paths:
            raw = path.read_bytes()
            if any(pattern.search(raw) for pattern in private_patterns):
                errors.append("PRIVACY_LEAK")
        if "PRIVACY_LEAK" not in errors:
            checks["privacy"] = True

        manifest_raw = (PACKAGE / "manifest.json").read_bytes()
        if proposal["source_export_manifest_bytes"] != len(manifest_raw) or proposal["source_export_manifest_sha256"] != sha(manifest_raw) or proposal["status"] != "prelease_export_only_not_sidecar_candidate" or proposal["sidecar_candidate_manifest_path"] is not None:
            errors.append("REGISTRY_PROPOSAL")
    except Exception as exc:  # deterministic error surface for malformed packages
        errors.append(f"EXCEPTION:{type(exc).__name__}:{exc}")

    admission_ready = not errors and not blockers
    package_integrity = not errors and all(checks.values())
    receipt = {
        "schema": "stacks-ega-prelease-export-validation/v1",
        "candidate_id": "mc-stacks-overlay-ega-integration-v1",
        "validated_subject": "manifest.json",
        "validated_subject_bytes": len((PACKAGE / "manifest.json").read_bytes()),
        "validated_subject_sha256": sha((PACKAGE / "manifest.json").read_bytes()),
        "validator_sha256": sha(Path(__file__).read_bytes()),
        "validated_at_utc": "2026-08-12T22:30:00Z",
        "mode": "admission_negative_preflight" if args.admission else "prelease_export_integrity",
        "checks": checks,
        "errors": sorted(set(errors)),
        "admission_blockers": sorted(set(blockers)),
        "package_integrity": "PASS" if package_integrity else "FAIL",
        "admission_ready": admission_ready,
        "overall": "PASS" if package_integrity and (not args.admission or admission_ready) else "FAIL",
    }
    output_name = "admission-validation.json" if args.admission else "validation.json"
    (PACKAGE / output_name).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
