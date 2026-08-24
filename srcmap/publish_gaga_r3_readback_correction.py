#!/usr/bin/env python3
"""Replace only the R3 manifest and publisher in a verified Zenodo successor."""

from __future__ import annotations

import argparse
import copy
import json
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import publish_gaga_r3_zenodo as base


ROOT = base.ROOT
PREDECESSOR_ID = 22086708
CONCEPT_ID = "21781322"
EXPECTED_FILES = 94
STATE = (
    ROOT
    / "output"
    / "publication"
    / "GAGA_STACKS_R3_READBACK_CORRECTION_STATE.json"
)
RECEIPT = (
    ROOT
    / "output"
    / "publication"
    / "GAGA_STACKS_R3_READBACK_CORRECTION_RECEIPT.json"
)
NEW_VERSION = "2026-08-24 GAGA R3 anonymous readback compatibility correction"
DESCRIPTION_APPENDIX = (
    "<p>This corrective successor changes no mathematical, source, or PDF "
    "content. It replaces only the release manifest and Zenodo publisher so "
    "anonymous public-byte verification uses Zenodo's content endpoint without "
    "an incompatible Accept header and retries transient reads.</p>"
)
REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (
        "output/publication/GAGA_STACKS_R3_MANIFEST.csv",
        "83_GAGA_Stacks_R3_MANIFEST.csv",
    ),
    (
        "srcmap/publish_gaga_r3_zenodo.py",
        "84_GAGA_Stacks_R3_Zenodo_publisher.py",
    ),
)
PINNED_SHA256 = {
    "83_GAGA_Stacks_R3_MANIFEST.csv": (
        "AD594B2F29D2AA45F3FCF96030DA8633824F76678BF7A9E813FADCD941331645"
    ),
    "84_GAGA_Stacks_R3_Zenodo_publisher.py": (
        "A399A496FAE88A4AF17D1C81375932F1909B6B5F7E5238C59B240470FF29952E"
    ),
}


def replacement_identities() -> list[dict[str, Any]]:
    missing = [local for local, _ in REPLACEMENTS if not (ROOT / local).is_file()]
    if missing:
        raise RuntimeError(f"Correction files are missing: {missing}")
    base.assert_profile_name_absent_from_payload([ROOT / local for local, _ in REPLACEMENTS])
    identities = [base.local_identity(local, remote) for local, remote in REPLACEMENTS]
    for row in identities:
        expected = PINNED_SHA256[row["remote_filename"]]
        if row["sha256"] != expected:
            raise RuntimeError(
                f"Pinned correction identity drift: {row['remote_filename']}"
            )
    return identities


def replacement_inventory(
    identities: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    return {
        row["remote_filename"]: {"bytes": row["bytes"], "md5": row["md5"]}
        for row in identities
    }


def expected_inventory(
    inherited: dict[str, dict[str, Any]], identities: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    expected = copy.deepcopy(inherited)
    expected.update(replacement_inventory(identities))
    return expected


def preflight(
    identities: list[dict[str, Any]], *, require_latest: bool
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    _, predecessor = base.request_json(
        f"https://zenodo.org/api/records/{PREDECESSOR_ID}"
    )
    _, latest = base.request_json(
        f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
    )
    if str(predecessor.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Correction predecessor identity drift")
    if require_latest and str(latest.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Correction predecessor is not the latest public version")
    if (
        str(predecessor.get("conceptrecid")) != CONCEPT_ID
        or str(latest.get("conceptrecid")) != CONCEPT_ID
    ):
        raise RuntimeError("Correction concept identity drift")
    base.assert_profile_name_absent(predecessor.get("metadata", {}))
    inherited = base.public_inventory(predecessor)
    if len(inherited) != EXPECTED_FILES:
        raise RuntimeError(
            f"Expected {EXPECTED_FILES} predecessor files; found {len(inherited)}"
        )
    for row in identities:
        if row["remote_filename"] not in inherited:
            raise RuntimeError(
                f"Replacement target is absent from predecessor: {row['remote_filename']}"
            )
    return predecessor, inherited, latest


def state_inventory(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return base.inventory_from_rows(rows)


def create_intent_state(
    identities: list[dict[str, Any]], inherited: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    state = {
        "schema": "gaga-r3-readback-correction-state-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "intent",
        "stage": "intent_persisted_before_newversion",
        "predecessor_id": PREDECESSOR_ID,
        "concept_record_id": int(CONCEPT_ID),
        "replacements": identities,
        "inherited_inventory": base.inventory_rows(inherited),
    }
    base.write_json_atomic(STATE, state)
    return state


def load_state(
    identities: list[dict[str, Any]], inherited: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    if not STATE.is_file():
        return None
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("schema") != "gaga-r3-readback-correction-state-v1":
        raise RuntimeError("Correction state schema mismatch")
    if state.get("status") not in {"intent", "draft", "published", "verified"}:
        raise RuntimeError("Correction state status is invalid")
    if int(state.get("predecessor_id", -1)) != PREDECESSOR_ID:
        raise RuntimeError("Correction state predecessor mismatch")
    if int(state.get("concept_record_id", -1)) != int(CONCEPT_ID):
        raise RuntimeError("Correction state concept mismatch")
    if state.get("replacements") != identities:
        raise RuntimeError("Current correction bytes differ from frozen state")
    if state_inventory(state.get("inherited_inventory", [])) != inherited:
        raise RuntimeError("Correction predecessor inventory differs from frozen state")
    if state.get("stage") == "draft_validation_failed":
        raise RuntimeError(
            f"Persisted correction draft validation failed: {state.get('validation_error')}"
        )
    if state["status"] in {"draft", "published", "verified"}:
        draft = state.get("draft", {})
        if not isinstance(draft.get("record_id"), int):
            raise RuntimeError("Correction state lacks a draft record ID")
        for key in ("self_url", "bucket_url", "publish_url"):
            url = draft.get(key)
            if not isinstance(url, str):
                raise RuntimeError(f"Correction state lacks action URL: {key}")
            base.validate_zenodo_url(url, require_api=True)
    if state["status"] in {"published", "verified"} and not isinstance(
        state.get("published_record_id"), int
    ):
        raise RuntimeError("Published correction state lacks its record ID")
    return state


def update_state(state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    updated.update(changes)
    updated["updated_utc"] = datetime.now(timezone.utc).isoformat()
    base.write_json_atomic(STATE, updated)
    return updated


def make_target_metadata(original: dict[str, Any]) -> dict[str, Any]:
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
        raise RuntimeError(f"Unexpected correction metadata mutation set: {changed}")
    base.assert_profile_name_absent(target)
    return target


def derive_clone_metadata(
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
    unexpected = sorted(changed - {"doi", "prereserve_doi", "version"})
    if unexpected:
        raise RuntimeError(
            f"Correction draft has unexpected cloned metadata drift: {unexpected}"
        )
    target = make_target_metadata(baseline)
    if current not in (baseline, target):
        raise RuntimeError("Correction draft metadata is neither clone baseline nor target")
    return baseline


def validate_draft_inventory(
    current: dict[str, dict[str, Any]],
    inherited: dict[str, dict[str, Any]],
    identities: list[dict[str, Any]],
) -> None:
    replacements = replacement_inventory(identities)
    if set(current) != set(inherited):
        raise RuntimeError("Correction draft filename set differs from the 94-file predecessor")
    for name, inherited_row in inherited.items():
        actual = current[name]
        if name in replacements:
            if actual not in (inherited_row, replacements[name]):
                raise RuntimeError(f"Correction draft replacement identity drift: {name}")
        elif actual != inherited_row:
            raise RuntimeError(f"Correction draft changed a non-replacement file: {name}")


def find_or_create_draft(
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
        raise RuntimeError("Correction predecessor deposition is not published")
    if predecessor_deposition.get("metadata", {}).get("description") != predecessor.get(
        "metadata", {}
    ).get("description"):
        raise RuntimeError("Authenticated and anonymous correction predecessor disagree")

    draft = base.find_existing_concept_draft(token)
    origin = "adopted_existing"
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
                draft = base.find_existing_concept_draft(token)
                if draft is not None:
                    break
                time.sleep(1.0)
        if draft is None:
            raise RuntimeError("Correction new-version action exposed no draft")
        origin = "created_now"

    current_metadata = copy.deepcopy(draft.get("metadata", {}))
    original_metadata = derive_clone_metadata(
        current_metadata, predecessor_deposition.get("metadata", {})
    )
    target_metadata = make_target_metadata(original_metadata)
    links = draft.get("links", {})
    action_links = {
        "self_url": links.get("self"),
        "bucket_url": links.get("bucket"),
        "publish_url": links.get("publish"),
    }
    if not all(isinstance(value, str) and value for value in action_links.values()):
        raise RuntimeError("Correction draft lacks required action links")
    for url in action_links.values():
        base.validate_zenodo_url(url, require_api=True)
    state = update_state(
        state,
        status="draft",
        stage="draft_identity_persisted_before_validation",
        draft={"record_id": int(draft["id"]), "origin": origin, **action_links},
        original_metadata=original_metadata,
        target_metadata=target_metadata,
        metadata_changed_keys=["description", "version"],
        observed_draft_files=len(draft.get("files", [])),
    )
    try:
        if int(draft["id"]) == PREDECESSOR_ID:
            raise RuntimeError("Correction draft resolved to the published predecessor")
        if str(draft.get("conceptrecid")) != CONCEPT_ID:
            raise RuntimeError("Correction draft escaped the concept lineage")
        if draft.get("submitted") is not False or draft.get("state") == "done":
            raise RuntimeError("Correction draft is not unpublished and mutable")
        validate_draft_inventory(
            base.draft_inventory(draft), inherited, identities
        )
        if current_metadata not in (original_metadata, target_metadata):
            raise RuntimeError("Correction draft metadata is not an accepted variant")
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
        raise RuntimeError("Corrected record escaped the concept lineage")
    inventory = base.public_inventory(record)
    if inventory != expected:
        raise RuntimeError("Corrected public inventory is not the exact 94-file target")
    old_metadata = predecessor.get("metadata", {})
    metadata = record.get("metadata", {})
    if metadata.get("version") != NEW_VERSION:
        raise RuntimeError("Corrected public version metadata mismatch")
    expected_description = str(old_metadata.get("description", "")).rstrip() + DESCRIPTION_APPENDIX
    if metadata.get("description") != expected_description:
        raise RuntimeError("Corrected public description mismatch")
    verified: list[str] = []
    for key in base.PUBLIC_STABLE_METADATA_KEYS:
        if key in old_metadata or key in metadata:
            if old_metadata.get(key) != metadata.get(key):
                raise RuntimeError(f"Corrected public stable metadata drift: {key}")
            verified.append(key)
    base.assert_profile_name_absent(metadata)
    return inventory, verified


def poll_public(
    record_id: int,
    predecessor: dict[str, Any],
    expected: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    last_error = "record not yet visible"
    for attempt in range(60):
        try:
            _, record = base.request_json(f"https://zenodo.org/api/records/{record_id}")
            inventory, verified = validate_public_snapshot(record, predecessor, expected)
            return record, inventory, verified
        except RuntimeError as error:
            last_error = str(error)
        if attempt < 59:
            time.sleep(2.0)
    raise RuntimeError(f"Corrected public record did not stabilize: {last_error}")


def recover_latest(
    state: dict[str, Any],
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    *,
    wait_for_change: bool,
) -> tuple[dict[str, Any], int] | None:
    target_inventory = expected_inventory(inherited, identities)
    attempts = 45 if wait_for_change else 1
    for attempt in range(attempts):
        _, latest = base.request_json(
            f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
        )
        if str(latest.get("conceptrecid")) != CONCEPT_ID:
            raise RuntimeError("Correction latest pointer escaped the concept lineage")
        latest_id = int(latest["id"])
        if latest_id != PREDECESSOR_ID:
            poll_public(latest_id, predecessor, target_inventory)
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
    target_inventory = expected_inventory(inherited, identities)
    record, inventory, stable_keys = poll_public(
        record_id, predecessor, target_inventory
    )
    _, latest = base.request_json(
        f"https://zenodo.org/api/records/{record_id}/versions/latest"
    )
    if str(latest.get("id")) != str(record_id):
        raise RuntimeError("Corrected record is not the latest concept version")
    public_files = {row["key"]: row for row in record.get("files", [])}
    if len(public_files) != len(record.get("files", [])):
        raise RuntimeError("Corrected public record contains duplicate filenames")
    readbacks: list[dict[str, Any]] = []
    for expected in identities:
        remote = expected["remote_filename"]
        url = public_files[remote].get("links", {}).get("self")
        if not url:
            raise RuntimeError(f"Corrected public file lacks a content URL: {remote}")
        byte_count = -1
        sha256 = ""
        for attempt in range(4):
            byte_count, sha256 = base.download_sha256(url)
            if byte_count == expected["bytes"] and sha256 == expected["sha256"]:
                break
            if attempt < 3:
                time.sleep(1.0)
        if byte_count != expected["bytes"] or sha256 != expected["sha256"]:
            raise RuntimeError(f"Corrected public-byte mismatch: {remote}")
        readbacks.append(
            {
                "remote_filename": remote,
                "bytes": byte_count,
                "sha256": sha256,
                "status": "PASS",
            }
        )
    return {
        "schema": "gaga-r3-readback-correction-receipt-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "predecessor": {
            "record_id": PREDECESSOR_ID,
            "doi": predecessor.get("doi"),
            "files": EXPECTED_FILES,
        },
        "published": {
            "record_id": int(record_id),
            "doi": record.get("doi"),
            "concept_record_id": int(CONCEPT_ID),
            "concept_doi": record.get("conceptdoi"),
            "version": record.get("metadata", {}).get("version"),
            "files": len(inventory),
        },
        "unchanged_files": EXPECTED_FILES - len(REPLACEMENTS),
        "metadata": {
            "changed_keys": ["description", "version"],
            "stable_keys_verified": stable_keys,
        },
        "replacements": identities,
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
        state = create_intent_state(identities, inherited)
    if state["status"] in {"published", "verified"}:
        receipt = verify_public(
            int(state["published_record_id"]),
            identities,
            predecessor,
            inherited,
            state.get("transfer_actions"),
        )
        return finalize(receipt, state)
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
        state = find_or_create_draft(
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
                "Correction draft is unavailable and no exact successor appeared"
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

    current_inventory = base.draft_inventory(draft)
    validate_draft_inventory(current_inventory, inherited, identities)
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
        raise RuntimeError("Correction draft metadata is not a frozen accepted variant")
    if metadata != state["target_metadata"]:
        raise RuntimeError("Correction metadata write/readback mismatch")

    wanted = replacement_inventory(identities)
    by_remote = {row["remote_filename"]: row for row in identities}
    current_inventory = base.draft_inventory(draft)
    transfer_actions: list[dict[str, Any]] = []
    for local, remote in REPLACEMENTS:
        if current_inventory[remote] == wanted[remote]:
            action = "already_present"
        else:
            response = base.upload_file(links["bucket_url"], ROOT / local, remote, token)
            size = int(response.get("size", response.get("filesize", -1)))
            md5 = base.normalize_checksum(response.get("checksum", ""))
            if size != by_remote[remote]["bytes"] or md5 != by_remote[remote]["md5"]:
                raise RuntimeError(f"Correction upload identity mismatch: {remote}")
            action = "replaced"
        transfer_actions.append({"remote_filename": remote, "action": action})

    _, draft = base.request_json(links["self_url"], token=token)
    target_inventory = expected_inventory(inherited, identities)
    if base.draft_inventory(draft) != target_inventory:
        raise RuntimeError("Correction draft inventory is not the exact 94-file target")
    if draft.get("metadata", {}) != state["target_metadata"]:
        raise RuntimeError("Completed correction draft metadata drift")
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
                raise RuntimeError("Correction publish response lacks a record ID")
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

    receipt = verify_public(
        record_id,
        identities,
        predecessor,
        inherited,
        state.get("transfer_actions"),
    )
    return finalize(receipt, state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create or resume and publish the two-file compatibility correction.",
    )
    args = parser.parse_args()
    identities = replacement_identities()
    predecessor, inherited, latest = preflight(
        identities, require_latest=not STATE.is_file()
    )
    state = load_state(identities, inherited)
    summary = {
        "status": "PASS",
        "predecessor_id": PREDECESSOR_ID,
        "latest_public_id": int(latest["id"]),
        "concept_record_id": int(CONCEPT_ID),
        "files": EXPECTED_FILES,
        "unchanged_files": EXPECTED_FILES - len(REPLACEMENTS),
        "replacement_files": len(REPLACEMENTS),
        "state": state.get("status") if state else "not_started",
        "replacements": identities,
    }
    if not args.execute:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    receipt = execute(identities, predecessor, inherited, state)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
