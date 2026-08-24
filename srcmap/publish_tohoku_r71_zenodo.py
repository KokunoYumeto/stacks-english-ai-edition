#!/usr/bin/env python3
"""Publish and anonymously verify the terminal Tôhoku-to-Stacks r71 dossier."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import publish_gaga_r3_zenodo as base


ROOT = base.ROOT
PREDECESSOR_ID = 21890525
CONCEPT_ID = "21792220"
EXPECTED_INHERITED_FILES = 8
MAX_ZENODO_FILES = 100
R71_RECEIPT_SHA256 = "097240D2CE69993FA61E9BA7CB81F47EC0329C23B686D69A6771DE0C9F6A6369"
NEW_VERSION = "0.68.0 — terminal Tôhoku-to-Stacks r71 formalization"
DESCRIPTION_APPENDIX = (
    "<p>This successor preserves the complete French/English edition inventory "
    "and adds the terminal Tôhoku-to-Stacks r71 formalization: 991 audited "
    "source units, 1,066 append-only decisions, 33 resolved and zero active "
    "source issues, zero review or candidate units, and zero remaining "
    "gap-class dispositions. It includes the mapping dossier, privacy-clean "
    "source-repair evidence, audited Stacks source surfaces, rebuilt PDFs and "
    "logs, deterministic tools, and anonymous public-byte verification.</p>"
)
STATE = (
    ROOT
    / "output"
    / "publication"
    / "TOHOKU_STACKS_R71_ZENODO_STATE.json"
)
RECEIPT = (
    ROOT
    / "output"
    / "publication"
    / "TOHOKU_STACKS_R71_PUBLICATION_RECEIPT.json"
)
MANIFEST = (
    ROOT
    / "output"
    / "publication"
    / "TOHOKU_STACKS_R71_MANIFEST.csv"
)

PAYLOAD: tuple[tuple[str, str], ...] = (
    ("output/publication/TOHOKU_STACKS_R71_README.md", "70_TOHOKU_STACKS_R71_README.md"),
    ("output/publication/TOHOKU_STACKS_R71_MANIFEST.csv", "71_TOHOKU_STACKS_R71_MANIFEST.csv"),
    ("tohoku_r71/r71-check.json", "72_TOHOKU_STACKS_R71_terminal_receipt.json"),
    ("tohoku_r71/STATUS.md", "73_TOHOKU_STACKS_R71_STATUS.md"),
    ("tohoku_r71/cfg.json", "74_TOHOKU_STACKS_R71_config.json"),
    ("tohoku_r71/intake.json", "75_TOHOKU_STACKS_R71_intake.json"),
    ("tohoku_r71/units.csv", "76_TOHOKU_STACKS_R71_units.csv"),
    ("tohoku_r71/map.csv", "77_TOHOKU_STACKS_R71_map.csv"),
    ("tohoku_r71/dec.csv", "78_TOHOKU_STACKS_R71_decisions.csv"),
    ("tohoku_r71/issues.csv", "79_TOHOKU_STACKS_R71_source_issues.csv"),
    ("tohoku_r71/mcheck.json", "80_TOHOKU_STACKS_R71_mapping_check.json"),
    ("tohoku_r71/check.json", "81_TOHOKU_STACKS_R71_check.json"),
    ("tohoku_r71/stx.csv", "82_TOHOKU_STACKS_R71_stacks_inventory.csv"),
    ("tohoku_r71/topics.csv", "83_TOHOKU_STACKS_R71_topics.csv"),
    ("tohoku_r71/tmap.csv", "84_TOHOKU_STACKS_R71_topic_map.csv"),
    ("tohoku_r71/tcand.csv", "85_TOHOKU_STACKS_R71_topic_candidates.csv"),
    ("tohoku_r71/ucand.csv", "86_TOHOKU_STACKS_R71_unit_candidates.csv"),
    ("srcmap/build_tohoku_r71.py", "87_TOHOKU_STACKS_R71_builder.py"),
    ("srcmap/tohoku_r71_contract.json", "88_TOHOKU_STACKS_R71_contract.json"),
    ("D1029_CHECK.json", "89_TOHOKU_STACKS_R71_D1029_audit.json"),
    (
        "output/publication/TOHOKU_R71_SOURCE_REPAIR_CHECK_PUBLIC.json",
        "90_TOHOKU_STACKS_R71_D1029_source_repair_public.json",
    ),
    ("D1030_CHECK.json", "91_TOHOKU_STACKS_R71_D1030_audit.json"),
    ("D1031_CHECK.json", "92_TOHOKU_STACKS_R71_D1031_audit.json"),
    ("D1031_FINAL_SCAN_CHECK.json", "93_TOHOKU_STACKS_R71_final_scan.json"),
    (
        "tmp/d1029_post_live_independent_review_r1.json",
        "94_TOHOKU_STACKS_R71_D1029_independent_review.json",
    ),
    (
        "tmp/d1030_post_live_independent_review_r1.json",
        "95_TOHOKU_STACKS_R71_D1030_independent_review.json",
    ),
    (
        "tmp/d1031_post_live_independent_review_r1.json",
        "96_TOHOKU_STACKS_R71_D1031_independent_review.json",
    ),
    (
        "tmp/d1031_final_four_gap_batch_design.json",
        "97_TOHOKU_STACKS_R71_final_four_design.json",
    ),
    ("cohomology.tex", "98_TOHOKU_STACKS_R71_cohomology.tex"),
    ("divisors.tex", "99_TOHOKU_STACKS_R71_divisors.tex"),
    ("homology.tex", "100_TOHOKU_STACKS_R71_homology.tex"),
    ("cohomology.pdf", "101_TOHOKU_STACKS_R71_cohomology.pdf"),
    ("divisors.pdf", "102_TOHOKU_STACKS_R71_divisors.pdf"),
    ("homology.pdf", "103_TOHOKU_STACKS_R71_homology.pdf"),
    (
        "srcmap/build_tohoku_r71_publication.py",
        "104_TOHOKU_STACKS_R71_public_projection_builder.py",
    ),
    ("srcmap/publish_tohoku_r71_zenodo.py", "105_TOHOKU_STACKS_R71_Zenodo_publisher.py"),
)


def require_identity(row: dict[str, Any], path: Path, recorded_name: str) -> None:
    if row.get("name") != recorded_name:
        raise RuntimeError(
            f"r71 receipt path mismatch: expected {recorded_name}; found {row.get('name')}"
        )
    if not path.is_file():
        raise RuntimeError(f"r71 receipt-bound file is missing: {path}")
    if int(row.get("bytes", -1)) != path.stat().st_size:
        raise RuntimeError(f"r71 receipt-bound byte drift: {path}")
    if row.get("sha256", "").upper() != base.digest(path, "sha256"):
        raise RuntimeError(f"r71 receipt-bound SHA-256 drift: {path}")


def validate_r71_receipt() -> None:
    receipt_path = ROOT / "tohoku_r71" / "r71-check.json"
    if base.digest(receipt_path, "sha256") != R71_RECEIPT_SHA256:
        raise RuntimeError("Terminal r71 receipt identity drift")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "PASS" or receipt.get("errors") != []:
        raise RuntimeError("Terminal r71 receipt is not an error-free PASS")
    deltas = receipt.get("deltas", {})
    counts = deltas.get("mapping_counts", {})
    expected_counts = {
        "units": 991,
        "decisions": 1066,
        "decided_units": 679,
        "source_issues": 33,
        "active_source_issues": 0,
        "review_units": 0,
        "candidate_units": 0,
        "unit_candidates": 0,
    }
    for key, value in expected_counts.items():
        if counts.get(key) != value:
            raise RuntimeError(f"Terminal r71 count drift: {key}")
    if deltas.get("remaining_gap_class_dispositions") != 0:
        raise RuntimeError("Terminal r71 receipt has remaining gap dispositions")
    if deltas.get("mapping_closures_appended") != 4 or deltas.get(
        "source_repairs_appended"
    ) != 1:
        raise RuntimeError("Terminal r71 append-only delta drift")

    for row in receipt.get("files", []):
        require_identity(row, ROOT / "tohoku_r71" / row["name"], row["name"])
    formalization = receipt.get("formalization", {})
    for row in formalization.get("live_sources", []):
        require_identity(row, ROOT / row["name"], row["name"])
    for row in formalization.get("build_artifacts", []):
        require_identity(row, ROOT / row["name"], row["name"])
    named_bindings = (
        formalization.get("D1029", {}).get("audit"),
        formalization.get("D1029", {}).get("post_live_review"),
        formalization.get("D1029", {}).get("source_repair"),
        formalization.get("D1030", {}).get("audit"),
        formalization.get("D1030", {}).get("post_live_review"),
        formalization.get("D1031", {}).get("audit"),
        formalization.get("D1031", {}).get("post_live_review"),
        formalization.get("batch_design"),
        formalization.get("final_scanner_audit"),
    )
    for row in named_bindings:
        if not isinstance(row, dict):
            raise RuntimeError("Terminal r71 receipt lacks a formalization binding")
        require_identity(row, ROOT / row["name"], row["name"])
    for key in ("contract", "engine", "script"):
        row = receipt.get("execution", {}).get(key)
        if not isinstance(row, dict):
            raise RuntimeError(f"Terminal r71 receipt lacks execution binding: {key}")
        require_identity(row, ROOT / row["name"], row["name"])

    projection_path = (
        ROOT / "output" / "publication" / "TOHOKU_R71_SOURCE_REPAIR_CHECK_PUBLIC.json"
    )
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    source_repair = formalization["D1029"]["source_repair"]
    projection_info = projection.get("projection", {})
    if (
        projection.get("status") != "PASS"
        or projection_info.get("source_name") != source_repair["name"]
        or projection_info.get("source_bytes") != source_repair["bytes"]
        or projection_info.get("source_sha256") != source_repair["sha256"]
        or projection_info.get("strings_transformed") != 10
        or projection_info.get("semantic_fields_removed") != 0
    ):
        raise RuntimeError("Public source-repair projection is not bound to the private audit")


def local_identities() -> list[dict[str, Any]]:
    if len({remote for _, remote in PAYLOAD}) != len(PAYLOAD):
        raise RuntimeError("Tôhoku payload contains duplicate remote filenames")
    missing = [local for local, _ in PAYLOAD if not (ROOT / local).is_file()]
    if missing:
        raise RuntimeError(f"Tôhoku payload files are missing: {missing}")
    base.assert_profile_name_absent_from_payload([ROOT / local for local, _ in PAYLOAD])
    if EXPECTED_INHERITED_FILES + len(PAYLOAD) > MAX_ZENODO_FILES:
        raise RuntimeError("Tôhoku payload would exceed Zenodo's file-count limit")
    validate_r71_receipt()
    identities = [base.local_identity(local, remote) for local, remote in PAYLOAD]

    manifest_rel = str(MANIFEST.relative_to(ROOT)).replace("\\", "/")
    expected = {
        row["remote_filename"]: row
        for row in identities
        if row["local_path"] != manifest_rel
    }
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"local_path", "remote_filename", "bytes", "md5", "sha256"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise RuntimeError("Tôhoku manifest lacks required identity columns")
        rows = list(reader)
    actual = {row["remote_filename"]: row for row in rows}
    if len(rows) != len(actual):
        raise RuntimeError("Tôhoku manifest contains duplicate remote filenames")
    if set(actual) != set(expected):
        raise RuntimeError("Tôhoku manifest filename set differs from the payload")
    for remote, wanted in expected.items():
        row = actual[remote]
        if (
            row.get("local_path") != wanted["local_path"]
            or int(row.get("bytes", -1)) != wanted["bytes"]
            or row.get("md5", "").upper() != wanted["md5"]
            or row.get("sha256", "").upper() != wanted["sha256"]
        ):
            raise RuntimeError(f"Tôhoku manifest identity mismatch: {remote}")
    return identities


def new_inventory(identities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        row["remote_filename"]: {"bytes": row["bytes"], "md5": row["md5"]}
        for row in identities
    }


def complete_inventory(
    inherited: dict[str, dict[str, Any]], identities: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    result = copy.deepcopy(inherited)
    result.update(new_inventory(identities))
    return result


def anonymous_preflight(
    *, require_latest: bool
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    _, predecessor = base.request_json(
        f"https://zenodo.org/api/records/{PREDECESSOR_ID}"
    )
    _, latest = base.request_json(
        f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
    )
    if str(predecessor.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Tôhoku predecessor identity drift")
    if require_latest and str(latest.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Configured Tôhoku predecessor is not the latest public version")
    if (
        str(predecessor.get("conceptrecid")) != CONCEPT_ID
        or str(latest.get("conceptrecid")) != CONCEPT_ID
    ):
        raise RuntimeError("Tôhoku concept identity drift")
    base.assert_profile_name_absent(predecessor.get("metadata", {}))
    inherited = base.public_inventory(predecessor)
    if len(inherited) != EXPECTED_INHERITED_FILES:
        raise RuntimeError(
            f"Expected {EXPECTED_INHERITED_FILES} inherited Tôhoku files; found {len(inherited)}"
        )
    collisions = sorted(set(inherited) & {remote for _, remote in PAYLOAD})
    if collisions:
        raise RuntimeError(f"Tôhoku payload filename collisions: {collisions}")
    return predecessor, inherited, latest


def find_concept_draft(token: str) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {"status": "draft", "size": 10, "q": f"conceptrecid:{CONCEPT_ID}"}
    )
    _, rows = base.request_json(
        f"https://zenodo.org/api/deposit/depositions?{query}", token=token
    )
    if not isinstance(rows, list):
        raise RuntimeError("Tôhoku draft search returned a non-list response")
    candidates = [
        row
        for row in rows
        if str(row.get("conceptrecid")) == CONCEPT_ID
        and row.get("submitted") is False
        and row.get("state") != "done"
    ]
    if len(candidates) > 1:
        raise RuntimeError("More than one unpublished Tôhoku successor draft exists")
    if not candidates:
        return None
    _, draft = base.request_json(
        f"https://zenodo.org/api/deposit/depositions/{int(candidates[0]['id'])}",
        token=token,
    )
    return draft


def target_metadata(original: dict[str, Any]) -> dict[str, Any]:
    target = copy.deepcopy(original)
    target["version"] = NEW_VERSION
    description = str(target.get("description", ""))
    if DESCRIPTION_APPENDIX not in description:
        target["description"] = description.rstrip() + DESCRIPTION_APPENDIX
    changed = sorted(
        key
        for key in set(original) | set(target)
        if original.get(key) != target.get(key)
    )
    if changed != ["description", "version"]:
        raise RuntimeError(f"Unexpected Tôhoku metadata mutation set: {changed}")
    base.assert_profile_name_absent(target)
    return target


def clone_metadata(
    current: dict[str, Any], predecessor: dict[str, Any]
) -> dict[str, Any]:
    baseline = copy.deepcopy(current)
    target_description = str(predecessor.get("description", "")).rstrip() + DESCRIPTION_APPENDIX
    if (
        baseline.get("version") == NEW_VERSION
        and baseline.get("description") == target_description
    ):
        baseline["description"] = predecessor.get("description", "")
        baseline.pop("version", None)
    changed = {
        key
        for key in set(predecessor) | set(baseline)
        if predecessor.get(key) != baseline.get(key)
    }
    unexpected = sorted(
        changed - {"doi", "prereserve_doi", "publication_date", "version"}
    )
    if unexpected:
        raise RuntimeError(f"Tôhoku clone metadata drift: {unexpected}")
    wanted = target_metadata(baseline)
    if current not in (baseline, wanted):
        raise RuntimeError("Tôhoku draft metadata is neither clone baseline nor target")
    return baseline


def validate_partial_inventory(
    current: dict[str, dict[str, Any]],
    inherited: dict[str, dict[str, Any]],
    identities: list[dict[str, Any]],
) -> None:
    added = new_inventory(identities)
    unexpected = sorted(set(current) - set(inherited) - set(added))
    if unexpected:
        raise RuntimeError(f"Tôhoku draft contains unexpected files: {unexpected}")
    for name, row in inherited.items():
        if current.get(name) != row:
            raise RuntimeError(f"Inherited Tôhoku file drift or absence: {name}")
    for name, row in current.items():
        if name in added and row != added[name]:
            raise RuntimeError(f"Partial Tôhoku upload identity drift: {name}")


def create_intent(
    identities: list[dict[str, Any]], inherited: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    state = {
        "schema": "tohoku-stacks-r71-zenodo-state-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "intent",
        "stage": "intent_persisted_before_newversion",
        "predecessor_id": PREDECESSOR_ID,
        "concept_record_id": int(CONCEPT_ID),
        "payload": identities,
        "inherited_inventory": base.inventory_rows(inherited),
    }
    base.write_json_atomic(STATE, state)
    return state


def update_state(state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    updated.update(changes)
    updated["updated_utc"] = datetime.now(timezone.utc).isoformat()
    base.write_json_atomic(STATE, updated)
    return updated


def load_state(
    identities: list[dict[str, Any]], inherited: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    if not STATE.is_file():
        return None
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("schema") != "tohoku-stacks-r71-zenodo-state-v1":
        raise RuntimeError("Tôhoku release state schema mismatch")
    if state.get("status") not in {"intent", "draft", "published", "verified"}:
        raise RuntimeError("Tôhoku release state status is invalid")
    if int(state.get("predecessor_id", -1)) != PREDECESSOR_ID:
        raise RuntimeError("Tôhoku release state predecessor mismatch")
    if int(state.get("concept_record_id", -1)) != int(CONCEPT_ID):
        raise RuntimeError("Tôhoku release state concept mismatch")
    if state.get("payload") != identities:
        if state.get("status") == "intent" and state.get("stage") in {
            "intent_persisted_before_newversion",
            "draft_identity_persisted_before_metadata_validation",
        }:
            state["_payload_rebind_required"] = True
        else:
            raise RuntimeError("Current Tôhoku payload differs from the frozen state")
    if base.inventory_from_rows(state.get("inherited_inventory", [])) != inherited:
        raise RuntimeError("Tôhoku inherited inventory differs from frozen state")
    if state.get("stage") == "draft_validation_failed":
        raise RuntimeError(
            f"Persisted Tôhoku draft validation failed: {state.get('validation_error')}"
        )
    if state["status"] in {"draft", "published", "verified"}:
        draft = state.get("draft", {})
        if not isinstance(draft.get("record_id"), int):
            raise RuntimeError("Tôhoku state lacks a draft record ID")
        for key in ("self_url", "bucket_url", "publish_url"):
            url = draft.get(key)
            if not isinstance(url, str):
                raise RuntimeError(f"Tôhoku state lacks action URL: {key}")
            base.validate_zenodo_url(url, require_api=True)
        original = state.get("original_metadata")
        target = state.get("target_metadata")
        if not isinstance(original, dict) or target_metadata(original) != target:
            raise RuntimeError("Tôhoku state metadata is malformed or nondeterministic")
    if state["status"] in {"published", "verified"} and not isinstance(
        state.get("published_record_id"), int
    ):
        raise RuntimeError("Published Tôhoku state lacks its record ID")
    return state


def adopt_or_create_draft(
    token: str,
    state: dict[str, Any],
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    _, predecessor_deposition = base.request_json(
        f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}", token=token
    )
    if predecessor_deposition.get("submitted") is not True:
        raise RuntimeError("Tôhoku predecessor deposition is not published")
    if predecessor_deposition.get("metadata", {}).get("description") != predecessor.get(
        "metadata", {}
    ).get("description"):
        raise RuntimeError("Authenticated and anonymous Tôhoku predecessor disagree")
    persisted_candidate = state.get("draft_candidate")
    draft: dict[str, Any] | None = None
    origin = "adopted_existing"
    if isinstance(persisted_candidate, dict):
        candidate_url = persisted_candidate.get("self_url")
        if not isinstance(candidate_url, str):
            raise RuntimeError("Persisted Tôhoku draft candidate lacks its self URL")
        base.validate_zenodo_url(candidate_url, require_api=True)
        _, draft = base.request_json(candidate_url, token=token)
        origin = str(persisted_candidate.get("origin", "adopted_existing"))
    if draft is None:
        draft = find_concept_draft(token)
    if draft is None:
        _, response = base.request_json(
            f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}/actions/newversion",
            method="POST",
            token=token,
            expected=(201,),
        )
        latest_draft_url = response.get("links", {}).get("latest_draft")
        if latest_draft_url:
            _, candidate = base.request_json(latest_draft_url, token=token)
            if candidate.get("submitted") is False and candidate.get("state") != "done":
                draft = candidate
        if draft is None:
            for _ in range(10):
                draft = find_concept_draft(token)
                if draft is not None:
                    break
                time.sleep(1.0)
        if draft is None:
            raise RuntimeError("Tôhoku new-version action exposed no mutable draft")
        origin = "created_now"
    links = draft.get("links", {})
    action_links = {
        "self_url": links.get("self"),
        "bucket_url": links.get("bucket"),
        "publish_url": links.get("publish"),
    }
    if not all(isinstance(value, str) and value for value in action_links.values()):
        raise RuntimeError("Tôhoku draft lacks required action links")
    for url in action_links.values():
        base.validate_zenodo_url(url, require_api=True)
    state = update_state(
        state,
        status="intent",
        stage="draft_identity_persisted_before_metadata_validation",
        draft_candidate={
            "record_id": int(draft["id"]),
            "origin": origin,
            **action_links,
        },
        observed_draft_files=len(draft.get("files", [])),
    )
    current_metadata = copy.deepcopy(draft.get("metadata", {}))
    original_metadata = clone_metadata(
        current_metadata, predecessor_deposition.get("metadata", {})
    )
    wanted_metadata = target_metadata(original_metadata)
    state = update_state(
        state,
        status="draft",
        stage="draft_identity_persisted_before_validation",
        draft={"record_id": int(draft["id"]), "origin": origin, **action_links},
        original_metadata=original_metadata,
        target_metadata=wanted_metadata,
        metadata_changed_keys=["description", "version"],
    )
    try:
        if int(draft["id"]) == PREDECESSOR_ID:
            raise RuntimeError("Tôhoku draft resolved to the published predecessor")
        if str(draft.get("conceptrecid")) != CONCEPT_ID:
            raise RuntimeError("Tôhoku draft escaped the concept lineage")
        if draft.get("submitted") is not False or draft.get("state") == "done":
            raise RuntimeError("Tôhoku draft is not unpublished and mutable")
        validate_partial_inventory(base.draft_inventory(draft), inherited, identities)
        if current_metadata not in (original_metadata, wanted_metadata):
            raise RuntimeError("Tôhoku draft metadata is not a frozen accepted variant")
    except RuntimeError as error:
        update_state(
            state,
            stage="draft_validation_failed",
            validation_error=str(error),
        )
        raise
    return update_state(state, stage="draft_adopted_and_validated")


def validate_public_snapshot(
    record: dict[str, Any],
    predecessor: dict[str, Any],
    expected: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if str(record.get("conceptrecid")) != CONCEPT_ID:
        raise RuntimeError("Published Tôhoku record escaped the concept lineage")
    inventory = base.public_inventory(record)
    if inventory != expected:
        raise RuntimeError("Published Tôhoku inventory is not the exact target")
    old_metadata = predecessor.get("metadata", {})
    metadata = record.get("metadata", {})
    if metadata.get("version") != NEW_VERSION:
        raise RuntimeError("Published Tôhoku version metadata mismatch")
    expected_description = str(old_metadata.get("description", "")).rstrip() + DESCRIPTION_APPENDIX
    if metadata.get("description") != expected_description:
        raise RuntimeError("Published Tôhoku description mismatch")
    stable_keys: list[str] = []
    for key in base.PUBLIC_STABLE_METADATA_KEYS:
        if key in old_metadata or key in metadata:
            if old_metadata.get(key) != metadata.get(key):
                raise RuntimeError(f"Published Tôhoku stable metadata drift: {key}")
            stable_keys.append(key)
    base.assert_profile_name_absent(metadata)
    return inventory, stable_keys


def poll_public(
    record_id: int,
    predecessor: dict[str, Any],
    expected: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    last_error = "record not yet visible"
    for attempt in range(60):
        try:
            _, record = base.request_json(f"https://zenodo.org/api/records/{record_id}")
            inventory, stable_keys = validate_public_snapshot(
                record, predecessor, expected
            )
            return record, inventory, stable_keys
        except RuntimeError as error:
            last_error = str(error)
        if attempt < 59:
            time.sleep(2.0)
    raise RuntimeError(f"Published Tôhoku record did not stabilize: {last_error}")


def recover_latest(
    state: dict[str, Any],
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    *,
    wait_for_change: bool,
) -> tuple[dict[str, Any], int] | None:
    expected = complete_inventory(inherited, identities)
    attempts = 45 if wait_for_change else 1
    for attempt in range(attempts):
        _, latest = base.request_json(
            f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
        )
        if str(latest.get("conceptrecid")) != CONCEPT_ID:
            raise RuntimeError("Tôhoku latest pointer escaped the concept lineage")
        latest_id = int(latest["id"])
        if latest_id != PREDECESSOR_ID:
            poll_public(latest_id, predecessor, expected)
            state = update_state(
                state,
                status="published",
                stage="published_record_recovered",
                published_record_id=latest_id,
            )
            return state, latest_id
        if attempt + 1 < attempts:
            time.sleep(2.0)
    return None


def verify_public(
    record_id: int,
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    transfer_actions: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    expected = complete_inventory(inherited, identities)
    record, inventory, stable_keys = poll_public(record_id, predecessor, expected)
    _, latest = base.request_json(
        f"https://zenodo.org/api/records/{record_id}/versions/latest"
    )
    if str(latest.get("id")) != str(record_id):
        raise RuntimeError("Published Tôhoku record is not the latest concept version")
    public_files = {row["key"]: row for row in record.get("files", [])}
    if len(public_files) != len(record.get("files", [])):
        raise RuntimeError("Published Tôhoku record contains duplicate filenames")
    readbacks: list[dict[str, Any]] = []
    for wanted in identities:
        remote = wanted["remote_filename"]
        url = public_files[remote].get("links", {}).get("self")
        if not url:
            raise RuntimeError(f"Published Tôhoku file lacks a content URL: {remote}")
        byte_count = -1
        sha256 = ""
        for attempt in range(4):
            byte_count, sha256 = base.download_sha256(url)
            if byte_count == wanted["bytes"] and sha256 == wanted["sha256"]:
                break
            if attempt < 3:
                time.sleep(1.0)
        if byte_count != wanted["bytes"] or sha256 != wanted["sha256"]:
            raise RuntimeError(f"Anonymous Tôhoku public-byte mismatch: {remote}")
        readbacks.append(
            {
                "remote_filename": remote,
                "bytes": byte_count,
                "sha256": sha256,
                "status": "PASS",
            }
        )
    return {
        "schema": "tohoku-stacks-r71-zenodo-publication-receipt-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "predecessor": {
            "record_id": PREDECESSOR_ID,
            "doi": predecessor.get("doi"),
            "inherited_files": len(inherited),
        },
        "published": {
            "record_id": int(record_id),
            "doi": record.get("doi"),
            "concept_record_id": int(CONCEPT_ID),
            "concept_doi": record.get("conceptdoi"),
            "version": record.get("metadata", {}).get("version"),
            "files": len(inventory),
        },
        "metadata": {
            "changed_keys": ["description", "version"],
            "stable_keys_verified": stable_keys,
        },
        "inherited_inventory": base.inventory_rows(inherited),
        "release_inventory": identities,
        "transfer_actions": transfer_actions
        or [
            {"remote_filename": row["remote_filename"], "action": "verification_only"}
            for row in identities
        ],
        "anonymous_public_readback": readbacks,
    }


def finalize(receipt: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    base.write_json_atomic(RECEIPT, receipt)
    update_state(
        state,
        status="verified",
        stage="anonymous_readback_complete",
        published_record_id=int(receipt["published"]["record_id"]),
        receipt={
            "path": str(RECEIPT.relative_to(ROOT)).replace("\\", "/"),
            "bytes": RECEIPT.stat().st_size,
            "sha256": base.digest(RECEIPT, "sha256"),
        },
    )
    return receipt


def execute(
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    state: dict[str, Any] | None,
) -> dict[str, Any]:
    if state is None:
        state = create_intent(identities, inherited)
    if state.pop("_payload_rebind_required", False):
        state = update_state(
            state,
            payload=identities,
            stage="intent_payload_rebound_before_remote_mutation",
        )
    if state["status"] in {"published", "verified"}:
        return finalize(
            verify_public(
                int(state["published_record_id"]),
                identities,
                predecessor,
                inherited,
                state.get("transfer_actions"),
            ),
            state,
        )
    if state["status"] == "draft":
        recovered = recover_latest(
            state,
            identities,
            predecessor,
            inherited,
            wait_for_change=False,
        )
        if recovered is not None:
            state, record_id = recovered
            return finalize(
                verify_public(
                    record_id,
                    identities,
                    predecessor,
                    inherited,
                    state.get("transfer_actions"),
                ),
                state,
            )
    token = base.load_token()
    if state["status"] == "intent":
        state = adopt_or_create_draft(
            token, state, identities, predecessor, inherited
        )
    links = state["draft"]
    try:
        _, draft = base.request_json(links["self_url"], token=token)
    except RuntimeError:
        recovered = recover_latest(
            state,
            identities,
            predecessor,
            inherited,
            wait_for_change=True,
        )
        if recovered is None:
            raise RuntimeError(
                "Tôhoku draft is unavailable and no exact published successor appeared"
            )
        state, record_id = recovered
        return finalize(
            verify_public(
                record_id,
                identities,
                predecessor,
                inherited,
                state.get("transfer_actions"),
            ),
            state,
        )

    validate_partial_inventory(base.draft_inventory(draft), inherited, identities)
    metadata = draft.get("metadata", {})
    if metadata == state["original_metadata"]:
        base.request_json(
            links["self_url"],
            method="PUT",
            token=token,
            payload={"metadata": state["target_metadata"]},
            expected=(200,),
        )
        _, draft = base.request_json(links["self_url"], token=token)
        metadata = draft.get("metadata", {})
    elif metadata != state["target_metadata"]:
        raise RuntimeError("Tôhoku draft metadata is not a frozen accepted variant")
    if metadata != state["target_metadata"]:
        raise RuntimeError("Tôhoku metadata write/readback mismatch")

    current = base.draft_inventory(draft)
    wanted = new_inventory(identities)
    by_remote = {row["remote_filename"]: row for row in identities}
    transfer_actions: list[dict[str, Any]] = []
    for local, remote in PAYLOAD:
        if remote in current:
            action = "already_present"
        else:
            response = base.upload_file(links["bucket_url"], ROOT / local, remote, token)
            size = int(response.get("size", response.get("filesize", -1)))
            md5 = base.normalize_checksum(response.get("checksum", ""))
            if size != by_remote[remote]["bytes"] or md5 != by_remote[remote]["md5"]:
                raise RuntimeError(f"Tôhoku upload identity mismatch: {remote}")
            current[remote] = wanted[remote]
            action = "uploaded"
        transfer_actions.append({"remote_filename": remote, "action": action})

    _, draft = base.request_json(links["self_url"], token=token)
    expected = complete_inventory(inherited, identities)
    if base.draft_inventory(draft) != expected:
        raise RuntimeError("Completed Tôhoku draft inventory is not the exact target")
    if draft.get("metadata", {}) != state["target_metadata"]:
        raise RuntimeError("Completed Tôhoku draft metadata drift")
    state = update_state(
        state,
        status="draft",
        stage="publish_pending",
        transfer_actions=transfer_actions,
    )
    recovered = recover_latest(
        state,
        identities,
        predecessor,
        inherited,
        wait_for_change=False,
    )
    if recovered is not None:
        state, record_id = recovered
    else:
        try:
            _, published = base.request_json(
                links["publish_url"],
                method="POST",
                token=token,
                expected=(202,),
            )
            raw_id = published.get("record_id") or published.get("id")
            if raw_id is None:
                raise RuntimeError("Tôhoku publish response lacks a record ID")
            record_id = int(raw_id)
            state = update_state(
                state,
                status="published",
                stage="publish_response_persisted",
                published_record_id=record_id,
            )
        except RuntimeError:
            recovered = recover_latest(
                state,
                identities,
                predecessor,
                inherited,
                wait_for_change=True,
            )
            if recovered is None:
                raise
            state, record_id = recovered
    return finalize(
        verify_public(
            record_id,
            identities,
            predecessor,
            inherited,
            state.get("transfer_actions"),
        ),
        state,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create or resume, publish, and anonymously verify the r71 successor.",
    )
    args = parser.parse_args()
    identities = local_identities()
    predecessor, inherited, latest = anonymous_preflight(
        require_latest=not STATE.is_file()
    )
    state = load_state(identities, inherited)
    summary = {
        "status": "PASS",
        "predecessor_id": PREDECESSOR_ID,
        "latest_public_id": int(latest["id"]),
        "concept_record_id": int(CONCEPT_ID),
        "inherited_files": len(inherited),
        "new_files": len(PAYLOAD),
        "total_files": len(inherited) + len(PAYLOAD),
        "state": state.get("status") if state else "not_started",
        "payload": identities,
    }
    if not args.execute:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    receipt = execute(identities, predecessor, inherited, state)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
