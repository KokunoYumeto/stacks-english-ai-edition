#!/usr/bin/env python3
"""Bind the R34--R38 release state to existing, checked evidence.

This tool never builds, publishes, downloads, reads credentials, or changes Git.
It writes only an R38 receipt under validation/.  The explicit phases are:
``validated`` (two builds, visual QA, and independent composition), ``packaged``
(also a verified package), and ``published`` (also exact public-byte readback,
the Zenodo publication receipt, and a saved GitHub workflow API response).
Missing or non-passing evidence is an error, never an inferred success.

Core validation receipts must already be committed at --content-head. Package
and publication receipts may follow that commit and are bound to their exact
raw file bytes. --workflow-receipt is the JSON response for the successful
GitHub Actions run at --metadata-head; a numeric run ID alone is insufficient.
Historical candidate/receipt bytes are never rewritten.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "KokunoYumeto/unofficial-stacks-project-ai-drafts"
REPOSITORY_ID = 1332406685
BUILD_HEAD = "bb6e7ccca41fe00a06815d81e174c5261e7a1ce3"
SOURCE_HEAD = "1242d514b71e60b4fe11b4c867f7de660f9a3b77"
CONCEPT_DOI = "10.5281/zenodo.22135180"
TAG = "ai-integrated-stacks-r38-2026-08-31"
PREFIX = "validation/stacks-errata-a04446e-r38-"
SUFFIX = "-2026-08-31.json"
PATHS = {
    "composition": "validation/composition-current.json",
    "build": PREFIX + "build" + SUFFIX,
    "visual": PREFIX + "visual-qa" + SUFFIX,
    "repro": PREFIX + "reproducibility" + SUFFIX,
    "second": PREFIX + "reproducibility-second" + SUFFIX,
    "independent": PREFIX + "independent-composition" + SUFFIX,
    "package": PREFIX + "package" + SUFFIX,
    "readback": PREFIX + "public-readback" + SUFFIX,
    "zenodo": PREFIX + "zenodo-publication" + SUFFIX,
}
OVERLAYS = [f"stacks-errata-a04446e-r{number}" for number in range(34, 39)]
CLARIFICATION_COMMIT = "7418fe8de04b68eb793924b56bd3b53dc0d0838d"
CLARIFICATION_PATH = "ai-integrated/registry/admission-receipts/r38-clarification-0001.json"
CLARIFICATION_SHA256 = "DF30A7C23B80E3B788D81CDEB1696F7C85F3E512B8CBE8C12510C8E3D1737E7F"
PHASES = {"validated": 0, "packaged": 1, "published": 2}
STATUSES = {
    "validated": "VALIDATION_COMPLETE",
    "packaged": "PRESERVATION_PACKAGE_COMPLETE",
    "published": "PUBLICATION_COMPLETE",
}
DEFECT_KEYS = (
    "clipped_content", "overlapping_content", "blank_pages", "corrupted_pages",
    "missing_or_unreadable_glyphs", "broken_diagrams",
)


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    require(bool(value) and "\\" not in value and ":" not in value
            and not path.is_absolute() and ".." not in path.parts
            and path.as_posix() == value, "invalid repository-relative path")
    return value


def file_identity(path: str, raw: bytes) -> dict[str, Any]:
    return {
        "path": relative_path(path), "bytes": len(raw), "sha256": sha256(raw),
        "git_blob": hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest(),
    }


def git(*arguments: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *arguments], stderr=subprocess.PIPE,
    )


def commit(value: str) -> str:
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None, "full commit ID required")
    require(git("rev-parse", f"{value}^{{commit}}").decode().strip() == value,
            "commit identity mismatch")
    return value


def tree(value: str) -> str:
    return git("rev-parse", f"{commit(value)}^{{tree}}").decode().strip()


def ancestor(older: str, newer: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit(older), commit(newer)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, f"required ancestry failed: {older} -> {newer}")


def blob(revision: str, path: str) -> bytes:
    return git("show", f"{commit(revision)}:{relative_path(path)}")


def load(path: str, revision: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    path = relative_path(path)
    raw = (ROOT / path).read_bytes()
    value = json.loads(raw.decode("utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    if revision is not None:
        require(raw == blob(revision, path), f"uncommitted or differing evidence: {path}")
    return value, file_identity(path, raw)


def bind(row: dict[str, Any], identity: dict[str, Any], *, path_key: str = "path") -> None:
    require(isinstance(row, dict), "missing evidence binding")
    for key in ("bytes", "sha256"):
        require(row.get(key) == identity[key], f"evidence {key} mismatch: {identity['path']}")
    if path_key in row:
        require(row[path_key] == identity["path"], "evidence path mismatch")


def inventory(rows: Any, *, name_key: str = "name") -> dict[str, tuple[int, str]]:
    require(isinstance(rows, list) and rows, "nonempty artifact inventory required")
    result = {}
    for row in rows:
        require(isinstance(row, dict), "invalid artifact row")
        name = row.get(name_key)
        require(isinstance(name, str) and name and "/" not in name and "\\" not in name,
                "invalid artifact name")
        require(name not in result and type(row.get("bytes")) is int and row["bytes"] > 0,
                "duplicate artifact or invalid byte count")
        require(isinstance(row.get("sha256"), str)
                and re.fullmatch(r"[0-9A-F]{64}", row["sha256"]) is not None,
                "invalid artifact SHA-256")
        result[name] = (row["bytes"], row["sha256"])
    return result


def validate_workflow(value: dict[str, Any], metadata_head: str) -> dict[str, Any]:
    require(value.get("name") == "Unified repository validation"
            and value.get("head_sha") == metadata_head
            and value.get("status") == "completed"
            and value.get("conclusion") == "success", "workflow is not exact-head successful")
    repository = value.get("repository", {})
    require(repository.get("id") == REPOSITORY_ID
            and repository.get("full_name") == REPOSITORY
            and repository.get("private") is False, "workflow repository identity/publicity mismatch")
    run_id, attempt = value.get("id"), value.get("run_attempt")
    require(type(run_id) is int and run_id > 0 and type(attempt) is int and attempt > 0,
            "workflow run/attempt identity missing")
    url = f"https://github.com/{REPOSITORY}/actions/runs/{run_id}"
    require(value.get("html_url") == url, "workflow URL mismatch")
    return {
        "name": value["name"], "run_id": run_id, "attempt": attempt,
        "head_sha": metadata_head, "status": value["status"],
        "conclusion": value["conclusion"], "url": url,
        "role": "successful exact-head workflow for the R38 metadata head",
    }


def validate_visual(visual: dict[str, Any], build: dict[str, Any],
                    build_identity: dict[str, Any], affected_stems: set[str]) -> None:
    require(visual.get("schema") == "unofficial-ai-integrated-stacks-visual-qa/v1"
            and visual.get("status") == "PASS", "invalid/non-passing visual evidence")
    require(visual["source"] == build["source"], "visual source mismatch")
    expected_binding = {key: build_identity[key] for key in ("path", "bytes", "sha256")}
    expected_binding.update({"status": build["status"],
                             "global_fixed_point_sweep": build["build"]["global_fixed_point_sweep"]})
    require(visual["build_receipt"] == expected_binding, "visual/build binding mismatch")
    artifacts = {row["stem"]: row for row in build["artifacts"]}
    scope, checks = visual["scope"], visual["checks"]
    require(scope["affected_chapters"] == sorted(affected_stems), "visual chapter scope mismatch")
    expected_pages = sum(artifacts[stem]["pages"] for stem in affected_stems)
    require(scope["full_page_render_count"] == expected_pages
            and scope["full_page_contact_sheet_review_count"] == expected_pages,
            "visual QA does not cover every affected page")
    locus = scope["high_resolution_locus_pages"]
    require(isinstance(locus, dict) and set(locus) == affected_stems, "visual locus inventory mismatch")
    for stem, pages in locus.items():
        require(isinstance(pages, list) and pages and all(type(page) is int
                and 1 <= page <= artifacts[stem]["pages"] for page in pages)
                and pages == sorted(set(pages)), "invalid visual locus page list")
    require(scope["high_resolution_locus_page_count"] == sum(len(pages) for pages in locus.values()),
            "visual locus count mismatch")
    rendered = visual["artifacts"]
    require(isinstance(rendered, dict) and set(rendered) == affected_stems,
            "visual artifact inventory mismatch")
    for stem, row in rendered.items():
        require(all(row.get(key) == artifacts[stem][key] for key in ("pages", "bytes", "sha256"))
                and row.get("pdf") == stem + ".pdf" and row.get("encrypted") is False
                and row.get("pages_without_ink") == 0 and row.get("duplicate_render_hashes") == 0,
                "visual artifact identity/legibility mismatch")
    for key in ("all_pages_rendered", "all_pages_manually_inspected",
                "all_manifest_bound_locus_pages_inspected_at_high_resolution", "page_dimensions_consistent",
                "headers_and_page_numbers_consistent", "text_and_formulas_legible", "diagrams_intact",
                "rejected_simplicial_007_parenthesis_preserved"):
        require(checks.get(key) is True, f"visual QA gate not passed: {key}")
    require(all(checks.get(key) == 0 for key in DEFECT_KEYS), "visual defects remain")
    protocol = visual["render_protocol"]
    require("Poppler" in str(protocol.get("renderer", ""))
            and type(protocol.get("full_page_dpi")) is int and protocol["full_page_dpi"] > 0
            and type(protocol.get("high_resolution_dpi")) is int and protocol["high_resolution_dpi"] > 0
            and protocol.get("render_intermediates_published") is False, "visual rendering protocol invalid")


def core_receipt(content: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    evidence, identities = {}, {}
    for key in ("composition", "build", "visual", "repro", "second", "independent"):
        evidence[key], identities[key] = load(PATHS[key], content)
        require(evidence[key].get("status") == "PASS", f"non-passing {key} evidence")
    comp, build, visual, repro, second, independent = (
        evidence[key] for key in ("composition", "build", "visual", "repro", "second", "independent")
    )
    require(comp["composition"]["source_commit"] == SOURCE_HEAD, "wrong R38 composition source")
    require(build["source"] == {"commit": BUILD_HEAD, "tree": tree(BUILD_HEAD)},
            "wrong frozen R38 build source")
    ancestor(SOURCE_HEAD, BUILD_HEAD)
    ancestor(BUILD_HEAD, content)
    require(build["composition"]["receipt_sha256"] == identities["composition"]["sha256"]
            and build["composition"]["receipt_git_blob"] == identities["composition"]["git_blob"],
            "build/composition binding mismatch")
    new = comp["new_overlays"]
    require([row["id"] for row in new] == OVERLAYS, "R34--R38 overlay order mismatch")
    artifacts = build["artifacts"]
    inventory(artifacts, name_key="stem")
    stems = [row["stem"] for row in artifacts]
    require(len(stems) == 30 and set(stems) == set(comp["required_build_stems"]),
            "R38 must cover the exact thirty required chapters")
    require(all(type(row.get("pages")) is int and row["pages"] > 0 for row in artifacts),
            "invalid PDF page count")
    tuples = [{key: row[key] for key in ("stem", "pages", "bytes", "sha256")} for row in artifacts]
    tuple_sha = sha256(("\n".join(
        "|".join(str(row[key]) for key in ("stem", "pages", "bytes", "sha256"))
        for row in sorted(tuples, key=lambda row: row["stem"])
    ) + "\n").encode())
    pages, pdf_bytes = sum(row["pages"] for row in artifacts), sum(row["bytes"] for row in artifacts)
    require(build["build"]["artifact_tuple_set_sha256"] == tuple_sha, "build tuple hash mismatch")
    require(build["build"]["chapter_count"] == 30 and build["build"]["pdfinfo_readable"] == 30,
            "incomplete fixed-point build")
    for key, count in build["build"]["diagnostics"].items():
        require(key == "external_reference_markers" or count == 0, f"build diagnostic: {key}")
    for key in ("schema", "status", "source", "builder", "composition", "environment", "build", "artifacts", "pdfs_committed"):
        require(second.get(key) == build.get(key), f"second build differs: {key}")
    require(second["created_utc"] != build["created_utc"], "second build must be a distinct invocation")
    require(repro["source"] == build["source"], "reproducibility source mismatch")
    for key, receipt_key in (("first", "build"), ("second", "second")):
        bind(repro["runs"][key], identities[receipt_key], path_key="receipt")
        require(repro["runs"][key]["created_utc"] == evidence[receipt_key]["created_utc"],
                "reproducibility invocation binding mismatch")
    comparison = repro["comparison"]
    expected = {
        "chapter_count": 30, "matched_artifact_count": 30, "different_artifact_count": 0,
        "different_artifacts": [], "total_pages_each_run": pages,
        "total_pdf_bytes_each_run": pdf_bytes, "artifact_tuple_set_sha256_each_run": tuple_sha,
        "all_artifact_identities_exactly_equal": True, "source_identity_equal": True,
        "builder_identity_equal": True, "environment_identity_equal": True, "fixed_point_sweep_equal": True,
    }
    require(all(comparison.get(key) == value for key, value in expected.items()),
            "reproducibility comparison incomplete or not passing")
    require(repro.get("artifacts") == tuples, "reproducibility artifact inventory differs")
    affected = comp["composition"]["affected_sources"]
    affected_stems = {Path(path).stem for path in affected}
    validate_visual(visual, build, identities["build"], affected_stems)
    scope, checks = visual["scope"], visual["checks"]
    require(independent.get("review_state") == "performed"
            and independent.get("source_commit") == SOURCE_HEAD
            and independent.get("registrar_cutoff") == comp["registry"]["cutoff_commit"],
            "independent composition binding mismatch")
    for key in ("forward_replay_complete_files_exact", "reverse_replay_restores_parent_files",
                "all_bytes_outside_edit_spans_unchanged", "previous_public_source_additions_preserved"):
        require(independent.get(key) is True, f"independent composition failed: {key}")
    require(independent["accepted_unique_operations"] == comp["composition"]["new_operations"]
            and independent["applied_byte_edits"] == comp["composition"]["new_byte_edit_operations"],
            "independent operation counts differ")
    sources = []
    for path, expected_source in affected.items():
        current = file_identity(path, blob(content, path))
        require(current["sha256"] == expected_source["composed_sha256"]
                and current["bytes"] == expected_source["composed_bytes"]
                and current["git_blob"] == expected_source["composed_git_blob"], "composed source drift")
        require(blob(BUILD_HEAD, path) == blob(content, path), "build-to-content source drift")
        require(any(row["path"] == path and row["sha256"] == current["sha256"]
                    and row["bytes"] == current["bytes"] for row in independent["sources"]),
                "source absent from independent review")
        sources.append(current)
    registry, registry_id = load("ai-integrated/registry/overlays.json", content)
    _, leases_id = load("ai-integrated/registry/leases.json", content)
    entries = registry["registered_entries"]
    require([row["id"] for row in entries[-5:]] == OVERLAYS, "unexpected registry tail")
    require(len(entries) == comp["registry"]["registered_overlays"]
            and sum(len(row["stable_ids"]) for row in entries) == comp["registry"]["registered_stable_ids"],
            "registry counts differ")
    overlay_rows = []
    for row, entry in zip(new, entries[-5:]):
        candidate = f"ai-integrated/candidates/{entry['namespace']}"
        manifest, manifest_id = load(candidate + "/candidate.manifest.json", content)
        require(manifest_id["sha256"] == row["manifest_sha256"] == entry["manifest_sha256"],
                "candidate manifest drift")
        payloads = []
        for payload in row["payloads"]:
            path = candidate + "/" + relative_path(payload["path"])
            identity = file_identity(path, blob(content, path))
            require(identity["sha256"] == payload["sha256"], "payload identity mismatch")
            payloads.append(identity)
        review_path = "ai-integrated/" + entry["review_receipt"]
        review, review_id = load(review_path, content)
        require(review_id["sha256"] == row["review_receipt_sha256"]
                and review.get("candidate_id") == row["id"]
                and review.get("passed") is True
                and review.get("result", "PASS") == "PASS"
                and review.get("pass_is_unconditional", True) is True,
                "final manifest-bound independent review mismatch")
        overlay_rows.append({
            "overlay_id": row["id"], "candidate_commit": row["candidate_commit"],
            "admission_commit": row["admission_commit"], "stable_ids": len(entry["stable_ids"]),
            "operations": row["operations"], "manifest": manifest_id, "payloads": payloads,
            "independent_review": review_id,
            "affected_sources": [Path(item["path"]).name for item in payloads],
        })
    result = {
        "schema": "unofficial-ai-integrated-stacks-errata-release/v1",
        "release": {
            "repository": REPOSITORY, "default_branch": "main",
            "previous_public_main_head": comp["previous_cutoff"]["public_main_head"],
            "frozen_registry_cutoff": comp["registry"]["cutoff_commit"],
            "frozen_registry_tree": comp["registry"]["cutoff_tree"],
            "registered_overlays": len(entries),
            "registered_stable_ids": comp["registry"]["registered_stable_ids"],
            "content_head": content, "content_tree": tree(content), "tag": TAG,
            "admitted_and_composed": OVERLAYS,
        },
        "overlays": overlay_rows,
        "composition": {
            "receipt": identities["composition"], "independent_review": identities["independent"],
            "registry_import_commit": comp["registry"]["linear_import_commit"],
            "source_commit": SOURCE_HEAD, "source_tree": tree(SOURCE_HEAD),
            "cumulative_v2_operations": comp["composition"]["total_v2_operations"],
            "new_stable_ids": sum(row["stable_ids"] for row in new),
            "new_operations": comp["composition"]["new_operations"],
            "new_byte_edit_operations": comp["composition"]["new_byte_edit_operations"],
            "semantic_dispositions": comp["composition"]["semantic_dispositions"],
            "order": OVERLAYS, "mode": comp["composition"]["mode"], "composed_sources": sources,
        },
        "build": {
            "receipt_path": PATHS["build"], "receipt_bytes": identities["build"]["bytes"],
            "receipt_sha256": identities["build"]["sha256"], "receipt_git_blob": identities["build"]["git_blob"],
            "source_commit": BUILD_HEAD, "source_tree": tree(BUILD_HEAD), "chapters": 30,
            "pages": pages, "pdf_bytes": pdf_bytes,
            "global_fixed_point_sweep": build["build"]["global_fixed_point_sweep"],
            "artifact_tuple_set_sha256": tuple_sha,
        },
        "visual_qa": {
            "status": visual["status"], "receipt_path": PATHS["visual"],
            "receipt_bytes": identities["visual"]["bytes"], "receipt_sha256": identities["visual"]["sha256"],
            "receipt_git_blob": identities["visual"]["git_blob"],
            "full_page_reviews": scope["full_page_contact_sheet_review_count"],
            "high_resolution_locus_pages": scope["high_resolution_locus_page_count"],
            "defects": sum(checks[key] for key in DEFECT_KEYS),
        },
        "reproducibility": {
            "status": repro["status"], "summary_path": PATHS["repro"],
            "summary_bytes": identities["repro"]["bytes"], "summary_sha256": identities["repro"]["sha256"],
            "summary_git_blob": identities["repro"]["git_blob"], "second_receipt_path": PATHS["second"],
            "second_receipt_bytes": identities["second"]["bytes"],
            "second_receipt_sha256": identities["second"]["sha256"],
            "second_receipt_git_blob": identities["second"]["git_blob"],
            "matched_artifacts": comparison["matched_artifact_count"],
            "different_artifacts": comparison["different_artifact_count"], "artifact_tuple_set_sha256": tuple_sha,
        },
        "registry": {"overlays": registry_id, "leases": leases_id},
        "fixed_point_artifacts": {
            "pdfs_committed": build["pdfs_committed"], "artifact_count": 30,
            "pages": pages, "bytes": pdf_bytes, "artifact_tuple_set_sha256": tuple_sha,
            "public_identity_evidence": PATHS["build"],
        },
        "scope_note": (
            "Five admitted rounds R34--R38: 77 accepted operations, 76 byte edits, and one "
            "operation already satisfied by an independently verified earlier structural rewrite. "
            "MC-STK-ERR-1345 is optional equivalent notation normalization, not a substantive "
            "mathematical correction. This receipt does not claim complete EGA integration, "
            "formal proof verification, or Stacks Project review or endorsement."
        ),
    }
    return result, evidence, identities


def add_package(result: dict[str, Any], content: str, evidence: dict[str, Any],
                identities: dict[str, Any]) -> dict[str, Any]:
    package, identity = load(PATHS["package"])
    require(package.get("status") == "PASS", "package did not pass")
    package_source = package["source"]
    require(package_source["tree"] == tree(package_source["commit"]), "package source tree mismatch")
    ancestor(BUILD_HEAD, package_source["commit"])
    ancestor(package_source["commit"], content)
    source_binding = package["release_source_binding"]
    require(source_binding.get("status") == "PASS"
            and source_binding.get("build_commit") == BUILD_HEAD
            and source_binding.get("build_tree") == tree(BUILD_HEAD)
            and source_binding.get("release_commit") == package_source["commit"]
            and source_binding.get("release_tree") == package_source["tree"]
            and source_binding.get("build_relevant_intervening_changes") == 0,
            "package/build binding does not pass")
    assets = inventory(package["release_assets"])
    require(len(assets) == 6 and {"README.md", "RELEASE.json", "SHA256SUMS.txt"}.issubset(assets),
            "package must contain exactly six release assets")
    checks = package["checks"]
    for key in ("source_projection_reopen_and_listing", "pdf_listing_and_member_hashes",
                "validation_listing_and_member_hashes", "checksum_inventory"):
        require(checks.get(key) == "PASS", f"package gate failed: {key}")
    require(package["archives"]["pdfs"]["member_count"] == 30, "package omits required PDFs")
    pdf_members = package["archives"]["pdfs"]["members"]
    expected_pdfs = [{"name": row["stem"] + ".pdf", **{
        key: row[key] for key in ("pages", "bytes", "sha256")
    }} for row in evidence["build"]["artifacts"]]
    require(inventory(pdf_members) == inventory(expected_pdfs), "package PDF identities differ from build")
    expected_pages = {row["name"]: row["pages"] for row in expected_pdfs}
    require(all(row.get("pages") == expected_pages[row["name"]] for row in pdf_members),
            "package PDF page counts differ from build")
    validation_members = inventory(package["archives"]["validation"]["members"])
    for key in ("composition", "build", "visual", "repro", "second", "independent"):
        bound = identities[key]
        require(validation_members.get(Path(bound["path"]).name) == (bound["bytes"], bound["sha256"]),
                f"package omits exact {key} proof")
    result["preservation"] = {
        "status": "PACKAGE_VERIFIED_NOT_PUBLICATION_VERIFIED", "package_receipt": {**identity, "status": package["status"]},
        "packaged_source": package_source,
        "assets": [{"name": name, "bytes": size, "sha256": digest}
                   for name, (size, digest) in sorted(assets.items())],
    }
    return package


def add_publication(result: dict[str, Any], content: str, metadata: str,
                    workflow_path: str, package: dict[str, Any]) -> dict[str, dict[str, Any]]:
    readback, rb_id = load(PATHS["readback"])
    zenodo, zenodo_id = load(PATHS["zenodo"])
    workflow, workflow_id = load(workflow_path)
    require(readback.get("status") == "PASS" and zenodo.get("status") == "PASS",
            "publication evidence has not passed")
    required_checks = (
        "github_repository_public", "github_release_public", "github_release_tag_exact",
        "github_current_assets_exact", "zenodo_record_public", "zenodo_access_open",
        "zenodo_all_record_files_downloaded", "current_release_cross_host_parity",
        "all_local_zips_reopened_and_crc_checked", "all_github_zips_reopened_and_crc_checked",
        "all_zenodo_zips_reopened_and_crc_checked", "changed_path_readback_performed", "changed_path_readback_pass",
    )
    require(all(readback.get("checks", {}).get(key) is True for key in required_checks),
            "public readback is incomplete")
    gh, zn = readback["github"], readback["zenodo"]
    require(gh["repository"] == REPOSITORY and gh["repository_public"] is True
            and gh["release_public"] is True and gh["default_branch"] == "main"
            and gh["tag"] == TAG and gh["tag_commit"] == content,
            "GitHub release identity/access mismatch")
    require(zn["record_public"] is True and zn["access_right"] == "open"
            and zn["concept_doi"] == CONCEPT_DOI, "Zenodo identity/access mismatch")
    expected_assets = inventory(package["release_assets"])
    for rows in (readback["local_release_assets"], gh["current_release_assets"], zn["current_release_assets"]):
        require(inventory(rows) == expected_assets, "cross-host release asset mismatch")
    for rows in (gh["current_release_assets"], zn["current_release_assets"], zn["inherited_assets"]):
        for row in rows:
            require(row.get("status") == "PASS", "anonymous asset download failed")
            if row["name"].endswith(".zip"):
                require(row.get("zip", {}).get("status") == "PASS"
                        and row["zip"].get("crc_test") == "PASS", "ZIP reopen/CRC evidence missing")
    require(zenodo.get("all_final_files_anonymously_verified") is True
            and zenodo.get("all_final_zips_reopened") is True, "Zenodo publication readback incomplete")
    for key in ("record_id", "doi", "concept_doi", "access_right", "file_count"):
        require(zenodo["published"].get(key) == zn.get(key), f"Zenodo publication mismatch: {key}")
    zenodo_rows = zenodo["anonymous_public_readback"]
    require(inventory(zenodo_rows, name_key="remote_filename")
            == inventory(zn["current_release_assets"] + zn["inherited_assets"]),
            "Zenodo complete inventory mismatch")
    changed = readback["changed_path_readback"]
    require(changed.get("status") == "PASS" and changed["head_commit"] == content
            and changed["head_tree"] == tree(content), "public source readback head mismatch")
    ancestor(changed["base_commit"], content)
    rows, deleted, row_index = [], [], {}
    for row in changed["changed_paths"]:
        path = relative_path(row["path"])
        require(path not in row_index and row.get("status_check") == "PASS", "duplicate/non-passing public path")
        expected_revision = changed["base_commit"] if row["status"] == "deleted" else content
        require(row.get("readback_commit") == expected_revision, "public path revision mismatch")
        identity = file_identity(path, blob(expected_revision, path))
        bind(row, identity)
        require(row.get("git_blob") == identity["git_blob"], "public path blob mismatch")
        row_index[path] = row
        (deleted if row["status"] == "deleted" else rows).append(identity)
    require(rows and changed["changed_path_count"] == len(row_index)
            and changed["readback_bytes"] == sum(row["bytes"] for row in row_index.values()),
            "public readback path totals mismatch")
    decisive = set(PATHS[key] for key in ("composition", "build", "visual", "repro", "second", "independent"))
    decisive.update(row["path"] for row in result["composition"]["composed_sources"])
    require(decisive.issubset({row["path"] for row in rows}), "public readback omits decisive R38 evidence")
    ancestor(content, metadata)
    result["release"].update({"published_content_head": content, "metadata_head": metadata,
                              "metadata_tree": tree(metadata)})
    result["workflow"] = validate_workflow(workflow, metadata)
    result["workflow_evidence"] = workflow_id
    result["public_readback"] = {
        "status": readback["status"], "receipt": rb_id, "checked_utc": readback["checked_utc"],
        "method": readback["method"], "commit": content,
        "changed_path_readback_count": changed["changed_path_count"],
        "changed_path_readback_bytes": changed["readback_bytes"],
        "checked_paths": rows, "deleted_paths_read_at_base": deleted,
    }
    preservation = result["preservation"]
    preservation.update({
        "status": "PUBLIC_READBACK_VERIFIED",
        "github": {key: gh[key] for key in ("repository_public", "release_id", "tag", "tag_commit", "prerelease")},
        "zenodo": {key: zn[key] for key in ("record_id", "doi", "concept_doi", "access_right", "file_count")},
        "asset_count_each_host": len(expected_assets),
        "asset_bytes_each_host": sum(size for size, _ in expected_assets.values()),
        "anonymous_downloads": len(gh["current_release_assets"]) + len(zn["current_release_assets"]) + len(zn["inherited_assets"]),
        "github_zenodo_asset_parity": readback["checks"]["current_release_cross_host_parity"],
        "source_archive_entries": package["archives"]["source"]["entry_count"],
        "source_archive_files": package["archives"]["source"]["file_count"],
        "pdf_archive_entries": package["archives"]["pdfs"]["member_count"],
        "validation_archive_entries": package["archives"]["validation"]["member_count"],
    })
    preservation["github"]["release_url"] = f"https://github.com/{REPOSITORY}/releases/tag/{TAG}"
    preservation["zenodo"].update({"record_url": f"https://zenodo.org/records/{zn['record_id']}",
                                   "publication_receipt": zenodo_id})
    return row_index


def add_clarification(result: dict[str, Any], content: str,
                      public_rows: dict[str, dict[str, Any]] | None) -> None:
    if not (ROOT / CLARIFICATION_PATH).is_file():
        result["registrar_clarification"] = {"status": "NOT_BOUND_IN_THIS_RECEIPT"}
        return
    _, identity = load(CLARIFICATION_PATH, content)
    require(identity["bytes"] == 4623 and identity["sha256"] == CLARIFICATION_SHA256,
            "registrar clarification bytes differ from the exact handoff")
    registrar_path = CLARIFICATION_PATH.removeprefix("ai-integrated/")
    require(blob(CLARIFICATION_COMMIT, registrar_path) == blob(content, CLARIFICATION_PATH),
            "clarification registrar-to-import transport mismatch")
    public = public_rows is not None and CLARIFICATION_PATH in public_rows
    if public:
        row = public_rows[CLARIFICATION_PATH]
        require(row.get("readback_commit") == content and row.get("status_check") == "PASS",
                "clarification is not read back at the content head")
        bind(row, identity)
    result["registrar_clarification"] = {
        "status": "PUBLIC_BYTES_VERIFIED" if public else "BOUND_NOT_PUBLICLY_VERIFIED",
        "registrar_commit": CLARIFICATION_COMMIT, "receipt": identity,
        "role": "append-only clarification; does not rewrite the admitted candidate or earlier receipts",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--content-head", required=True)
    parser.add_argument("--metadata-head")
    parser.add_argument("--workflow-receipt", help="repository-relative saved GitHub Actions API JSON")
    parser.add_argument("--output", default=PREFIX + "release" + SUFFIX)
    parser.add_argument("--check-only", action="store_true", help="validate inputs without writing a receipt")
    return parser.parse_args(argv)


def atomic_write(output: Path, raw: bytes) -> None:
    require(not output.is_symlink() and output.parent.resolve().is_relative_to(ROOT.resolve()),
            "output must not be a symlink or escape the repository")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".r38-receipt-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        output_path = relative_path(args.output)
        require(output_path.startswith(PREFIX) and output_path.endswith(SUFFIX)
                and output_path not in PATHS.values(), "output must be a separate R38 receipt")
        content = commit(args.content_head)
        if args.phase == "published":
            require(args.metadata_head and args.workflow_receipt, "published phase requires metadata and workflow evidence")
        result, evidence, identities = core_receipt(content)
        package = add_package(result, content, evidence, identities) if PHASES[args.phase] >= 1 else None
        public_rows = None
        if args.phase == "published":
            public_rows = add_publication(result, content, commit(args.metadata_head),
                                          relative_path(args.workflow_receipt), package)
        add_clarification(result, content, public_rows)
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        result.update({"phase": args.phase, "status": STATUSES[args.phase],
                       "created_utc": now, "updated_utc": now})
        output = ROOT / output_path
        require(not output.is_symlink(), "output must not be a symlink")
        if output.exists():
            previous, _ = load(output_path)
            require(previous.get("schema") == result["schema"] and previous.get("phase") in PHASES,
                    "refusing to overwrite an unrelated or historical receipt")
            require(PHASES[previous["phase"]] <= PHASES[args.phase], "receipt phase cannot regress")
            if previous["phase"] == "published":
                require(previous["release"]["published_content_head"] == content,
                        "published content identity cannot be replaced")
            result["created_utc"] = previous["created_utc"]
        raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if not args.check_only:
            atomic_write(output, raw)
        print(json.dumps({"status": "PASS", "phase": args.phase, "receipt_status": result["status"],
                          "written": not args.check_only, "output": output_path,
                          "bytes": len(raw), "sha256": sha256(raw)}, sort_keys=True))
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        # File errors must not leak the local account or checkout location.
        message = str(error).replace(str(ROOT), "<repository>").replace(ROOT.as_posix(), "<repository>")
        account = Path.home().name
        if account:
            message = re.sub(re.escape(account), "[LOCAL_ACCOUNT]", message, flags=re.IGNORECASE)
        print(json.dumps({"status": "FAIL", "error": message}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
