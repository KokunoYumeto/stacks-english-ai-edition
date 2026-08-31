#!/usr/bin/env python3
"""Publish and anonymously verify the EGA I 6.6.3 checkpoint.

The publisher is deliberately transaction-oriented and resumable.  A dry run
performs local identity checks and an anonymous Zenodo lineage preflight.  The
``--execute`` path is the only path that reads the credential file or mutates a
Zenodo draft.  Credentials are sent exclusively in an Authorization header.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PREDECESSOR_ID = 22175419
CONCEPT_RECORD_ID = "22135180"
CONCEPT_DOI = "10.5281/zenodo.22135180"
TITLE = "Unofficial AI-Integrated Stacks Project — EGA I §6.6.3 semantic checkpoint"
VERSION = "EGA-I-6.6.3-semantic-2026-08-30"
RELEASE_ID = "ega-i-6.6.3-semantic-2026-08-30"
SOURCE_COMMIT = "f1b8d56b5f3c9999010455a38a289bce76735070"
SOURCE_TREE = "8d2e7b4f3c84d825f39b673387e0266e09573b96"
CONTENT_COMMIT = "85024a5e3456cadc79c6cde67bf1fcbbc09c48cb"
DESCRIPTION = (
    "<p>This source-reproducible successor records the unofficial AI-integrated "
    "Stacks mapping and evidence work for EGA I §6.6.3.</p>"
    "<p>The generated R32 Stacks PDFs and their build-critical source bytes are "
    "unchanged from R32; this version adds semantic mapping, provenance, and "
    "validation evidence only. The incomplete EGA integration program continues "
    "in source order at EGA I §6.6.4.</p>"
    "<p>This is independent, unofficial work. No Stacks Project affiliation, "
    "review, approval, or endorsement is claimed.</p>"
)
TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"

EXPECTED_ASSETS: dict[str, tuple[int, str]] = {
    "README.md": (
        3119,
        "6F185D051351901E025736F4A0D33947A171427F5D98F04D125C95EE76F433C7",
    ),
    "RELEASE.json": (
        23317,
        "FF86CA03D6818C3EE442B951BA7291FFE73475D0BA3195810E92F378B0731BF6",
    ),
    "SHA256SUMS.txt": (
        580,
        "678519D1582DAF1361A56E0FF3349F59E7140101DD223B7B2D42DAEE2A716188",
    ),
    "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-pdfs.zip": (
        21000346,
        "04B67B36F39AB596E14C9741352F503E2C787F1E41AEEDB3097D5B858BDA2F26",
    ),
    "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-source-f1b8d56b.zip": (
        161340724,
        "48723E1936B7DA9AD25CC83306BCF33AEDD4DB453F255A453ED6EFBB9D9D22F9",
    ),
    "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-validation.zip": (
        47363,
        "1A4BBA4E9BDE4A2FD57F5125788C0900885FFE7F529D064B204112BD8EB248E7",
    ),
}

MUTATED_METADATA_KEYS = {"access_right", "description", "title", "version"}
# Zenodo assigns a fresh publication date to every new-version draft.  Treat
# that server-owned value as volatile while continuing to reject drift in all
# inherited project metadata.
VOLATILE_DRAFT_METADATA_KEYS = {"doi", "prereserve_doi", "publication_date"}
PUBLIC_STABLE_METADATA_KEYS = (
    "communities",
    "contributors",
    "creators",
    "keywords",
    "language",
    "license",
    "notes",
    "references",
    "related_identifiers",
    "resource_type",
    "subjects",
    "upload_type",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest().upper()


def normalize_checksum(value: str) -> str:
    return value.split(":", 1)[-1].upper()


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def assert_no_local_profile_name(value: Any) -> None:
    profile_name = Path.home().name.strip()
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(profile_name) >= 3 and profile_name.casefold() in serialized.casefold():
        raise RuntimeError("Sanitized publication data contains the local profile name")
    if re.search(
        r"(?i)(?:(?<![A-Za-z0-9])[a-z]:[\\/]"
        r"|(?:^|[\s\"'(\[])/(?:home|users)/)",
        serialized,
    ):
        raise RuntimeError("Sanitized publication data contains a local absolute path")


def canonical_license_id(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip().casefold()
    if isinstance(value, dict):
        identifier = value.get("id")
        if isinstance(identifier, str) and identifier.strip():
            return identifier.strip().casefold()
    raise RuntimeError("Zenodo license metadata lacks a canonical identifier")


def validate_zenodo_url(url: str, *, authenticated: bool = False) -> None:
    parsed = urllib.parse.urlparse(url)
    try:
        port = parsed.port
    except ValueError as error:
        raise RuntimeError("Refusing a malformed Zenodo URL") from error
    query_keys = {key.casefold() for key, _ in urllib.parse.parse_qsl(parsed.query)}
    if query_keys & {"access_token", "token"}:
        raise RuntimeError("Credentials in URLs are forbidden")
    if (
        parsed.scheme != "https"
        or parsed.hostname != "zenodo.org"
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
        or (authenticated and not parsed.path.startswith("/api/"))
    ):
        raise RuntimeError("Refusing a non-Zenodo action URL")


class ZenodoOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        validate_zenodo_url(
            newurl,
            authenticated=req.get_header("Authorization") is not None,
        )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


ZENODO_OPENER = urllib.request.build_opener(ZenodoOnlyRedirectHandler())


def request_json(
    url: str,
    *,
    method: str = "GET",
    token: str | None = None,
    payload: dict[str, Any] | None = None,
    expected: tuple[int, ...] = (200,),
    timeout: int = 90,
) -> tuple[int, Any]:
    validate_zenodo_url(url, authenticated=token is not None)
    headers = {"Accept": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with ZENODO_OPENER.open(request, timeout=timeout) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Zenodo request failed with HTTP {error.code}: {body[:1600]}"
        ) from error
    if status not in expected:
        raise RuntimeError(f"Unexpected Zenodo HTTP status {status}")
    if not body:
        return status, None
    try:
        return status, json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError("Zenodo returned malformed JSON") from error


def request_no_content(
    url: str,
    *,
    method: str,
    token: str,
    expected: tuple[int, ...],
) -> int:
    validate_zenodo_url(url, authenticated=True)
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "Authorization": f"Bearer {token}"},
        method=method,
    )
    try:
        with ZENODO_OPENER.open(request, timeout=90) as response:
            response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Zenodo draft mutation failed with HTTP {error.code}: {body[:1600]}"
        ) from error
    if status not in expected:
        raise RuntimeError(f"Unexpected Zenodo draft-mutation status {status}")
    return status


def download_sha256(url: str, *, token: str | None = None) -> tuple[int, str]:
    validate_zenodo_url(url, authenticated=token is not None)
    headers: dict[str, str] = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    total = 0
    hasher = hashlib.sha256()
    try:
        with ZENODO_OPENER.open(request, timeout=600) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                hasher.update(chunk)
    except urllib.error.HTTPError as error:
        raise RuntimeError(
            f"Zenodo file readback failed with HTTP {error.code}"
        ) from error
    return total, hasher.hexdigest().upper()


def upload_file(bucket_url: str, path: Path, remote_name: str, token: str) -> dict[str, Any]:
    url = bucket_url.rstrip("/") + "/" + urllib.parse.quote(remote_name, safe="")
    validate_zenodo_url(url, authenticated=True)
    request = urllib.request.Request(
        url,
        data=path.read_bytes(),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
        },
        method="PUT",
    )
    try:
        with ZENODO_OPENER.open(request, timeout=900) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Upload failed for {remote_name} with HTTP {error.code}: {body[:1600]}"
        ) from error
    if status < 200 or status >= 300:
        raise RuntimeError(f"Upload failed for {remote_name} with HTTP {status}")
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Upload returned malformed JSON for {remote_name}") from error


def load_token() -> str:
    text = TOKEN_FILE.read_text(encoding="utf-8")
    candidates = re.findall(
        r"(?<![A-Za-z0-9._-])([A-Za-z0-9][A-Za-z0-9._-]{39,})(?![A-Za-z0-9._-])",
        text,
    )
    candidates = list(dict.fromkeys(candidates))
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one token-shaped credential; found {len(candidates)}"
        )
    return candidates[0]


def validate_sha256sums(asset_dir: Path) -> None:
    rows: dict[str, str] = {}
    sums_path = asset_dir / "SHA256SUMS.txt"
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9A-Fa-f]{64})  ([^/\\]+)", line)
        if match is None:
            raise RuntimeError("SHA256SUMS.txt contains a malformed row")
        sha, name = match.groups()
        if name in rows:
            raise RuntimeError("SHA256SUMS.txt contains a duplicate filename")
        rows[name] = sha.upper()
    expected_names = set(EXPECTED_ASSETS) - {"SHA256SUMS.txt"}
    if set(rows) != expected_names:
        raise RuntimeError("SHA256SUMS.txt does not bind exactly the other five assets")
    for name, sha in rows.items():
        if sha != EXPECTED_ASSETS[name][1]:
            raise RuntimeError(f"SHA256SUMS.txt identity mismatch for {name}")


def validate_release_manifest(asset_dir: Path) -> None:
    try:
        release = json.loads((asset_dir / "RELEASE.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError("RELEASE.json is malformed") from error
    if (
        release.get("schema")
        != "unofficial-ai-integrated-stacks-ega-semantic-preservation-package/v1"
        or release.get("release") != RELEASE_ID
        or release.get("title") != TITLE
        or release.get("source", {}).get("commit") != SOURCE_COMMIT
        or release.get("source", {}).get("tree") != SOURCE_TREE
        or release.get("integration", {})
        .get("ega_semantic_checkpoint", {})
        .get("content_commit")
        != CONTENT_COMMIT
        or release.get("integration", {})
        .get("ega_semantic_checkpoint", {})
        .get("release_commit")
        != SOURCE_COMMIT
        or release.get("validation", {}).get("status") != "PASS"
        or release.get("preservation", {}).get("zenodo_concept_doi") != CONCEPT_DOI
        or release.get("preservation", {}).get("license") != "gfdl-1.2-only"
        or release.get("scope_note")
        != "EGA I §6.6.3 semantic integration is closed; the incomplete EGA integration program continues at EGA I §6.6.4. Complete EGA integration and formal verification are not claimed."
    ):
        raise RuntimeError("RELEASE.json semantic identity or PASS state drifted")
    rows = release.get("assets")
    if not isinstance(rows, list):
        raise RuntimeError("RELEASE.json assets are malformed")
    manifest_assets: dict[str, tuple[int, str]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            raise RuntimeError("RELEASE.json contains a malformed asset row")
        name = row["name"]
        if name in manifest_assets:
            raise RuntimeError("RELEASE.json contains a duplicate asset row")
        manifest_assets[name] = (int(row.get("bytes", -1)), str(row.get("sha256", "")).upper())
    expected_manifest_names = {
        "README.md",
        "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-pdfs.zip",
        "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-source-f1b8d56b.zip",
        "unofficial-ai-integrated-stacks-project-ega-i-6.6.3-semantic-validation.zip",
    }
    if set(manifest_assets) != expected_manifest_names:
        raise RuntimeError("RELEASE.json does not bind its exact four payload artifacts")
    for name, identity in manifest_assets.items():
        if identity != EXPECTED_ASSETS[name]:
            raise RuntimeError(f"RELEASE.json identity mismatch for {name}")


def validate_local_assets(asset_dir: Path) -> list[dict[str, Any]]:
    if asset_dir.is_symlink() or not asset_dir.is_dir():
        raise RuntimeError("The supplied asset directory does not exist")
    children = list(asset_dir.iterdir())
    if any(not child.is_file() or child.is_symlink() for child in children):
        raise RuntimeError("The asset directory must contain six ordinary files only")
    if {child.name for child in children} != set(EXPECTED_ASSETS):
        raise RuntimeError("The asset directory inventory is not the frozen six-file release")
    identities: list[dict[str, Any]] = []
    for name in sorted(EXPECTED_ASSETS):
        path = asset_dir / name
        expected_bytes, expected_sha256 = EXPECTED_ASSETS[name]
        actual_bytes = path.stat().st_size
        actual_sha256 = digest(path, "sha256")
        if actual_bytes != expected_bytes or actual_sha256 != expected_sha256:
            raise RuntimeError(f"Frozen local identity mismatch for {name}")
        identities.append(
            {
                "remote_filename": name,
                "bytes": actual_bytes,
                "md5": digest(path, "md5"),
                "sha256": actual_sha256,
            }
        )
    validate_sha256sums(asset_dir)
    validate_release_manifest(asset_dir)
    return identities


def inventory_from_identities(identities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        row["remote_filename"]: {"bytes": row["bytes"], "md5": row["md5"]}
        for row in identities
    }


def public_inventory(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    rows = record.get("files", [])
    if not isinstance(rows, list):
        raise RuntimeError("Public record has a malformed file inventory")
    for row in rows:
        name = row.get("key")
        if not isinstance(name, str) or name in result:
            raise RuntimeError("Public record contains an invalid or duplicate filename")
        result[name] = {
            "bytes": int(row.get("size", -1)),
            "md5": normalize_checksum(str(row.get("checksum", ""))),
        }
    return result


def draft_inventory(deposition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    rows = deposition.get("files", [])
    if not isinstance(rows, list):
        raise RuntimeError("Draft has a malformed file inventory")
    for row in rows:
        name = row.get("filename") or row.get("key")
        if not isinstance(name, str) or name in result:
            raise RuntimeError("Draft contains an invalid or duplicate filename")
        result[name] = {
            "bytes": int(row.get("filesize", row.get("size", -1))),
            "md5": normalize_checksum(str(row.get("checksum", ""))),
        }
    return result


def validate_lineage_record(record: dict[str, Any], expected_id: int | None = None) -> None:
    if expected_id is not None and int(record.get("id", -1)) != expected_id:
        raise RuntimeError("Zenodo record identity drift")
    if str(record.get("conceptrecid")) != CONCEPT_RECORD_ID:
        raise RuntimeError("Zenodo record escaped the intended concept lineage")
    concept_doi = record.get("conceptdoi") or record.get("metadata", {}).get("conceptdoi")
    if concept_doi not in (None, CONCEPT_DOI):
        raise RuntimeError("Zenodo concept DOI drift")


def anonymous_preflight(*, require_predecessor_latest: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    _, predecessor = request_json(f"https://zenodo.org/api/records/{PREDECESSOR_ID}")
    _, latest = request_json(f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest")
    validate_lineage_record(predecessor, PREDECESSOR_ID)
    validate_lineage_record(latest)
    if require_predecessor_latest and int(latest.get("id", -1)) != PREDECESSOR_ID:
        raise RuntimeError("The configured predecessor is no longer the latest public version")
    metadata = predecessor.get("metadata", {})
    if not isinstance(metadata.get("creators"), list) or not metadata["creators"]:
        raise RuntimeError("Predecessor creators are absent")
    if not metadata.get("license"):
        raise RuntimeError("Predecessor license is absent")
    if metadata.get("access_right") != "open":
        raise RuntimeError("Predecessor is not openly accessible")
    assert_no_local_profile_name(metadata)
    return predecessor, latest


def target_public_metadata(predecessor: dict[str, Any]) -> dict[str, Any]:
    metadata = predecessor.get("metadata", {})
    return {
        "title": TITLE,
        "version": VERSION,
        "access_right": "open",
        "description": DESCRIPTION,
        "creators": copy.deepcopy(metadata.get("creators")),
        "license": copy.deepcopy(metadata.get("license")),
    }


def metadata_matches_target_public(metadata: dict[str, Any], predecessor: dict[str, Any]) -> bool:
    expected = target_public_metadata(predecessor)
    return all(metadata.get(key) == value for key, value in expected.items())


def make_target_draft_metadata(
    current: dict[str, Any], predecessor: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    predecessor_metadata = predecessor.get("metadata", {})
    if current.get("creators") != predecessor_metadata.get("creators"):
        raise RuntimeError("Successor draft creators differ from the predecessor")
    if current.get("license") != predecessor_metadata.get("license"):
        raise RuntimeError("Successor draft license differs from the predecessor")

    desired_values = {
        "title": TITLE,
        "version": VERSION,
        "access_right": "open",
        "description": DESCRIPTION,
    }
    states: list[str] = []
    for key, desired in desired_values.items():
        value = current.get(key)
        predecessor_value = predecessor_metadata.get(key)
        if desired == predecessor_value:
            if value != desired:
                raise RuntimeError(f"Successor draft has an unexpected {key} value")
            continue
        if value == desired:
            states.append("target")
        elif value == predecessor_value:
            states.append("baseline")
        elif key == "version" and value in (None, ""):
            states.append("baseline")
        else:
            raise RuntimeError(f"Successor draft has an unexpected {key} value")
    if not states or len(set(states)) != 1:
        raise RuntimeError("Successor draft metadata is only partially mutated")

    excluded = MUTATED_METADATA_KEYS | VOLATILE_DRAFT_METADATA_KEYS
    for key in set(current) | set(predecessor_metadata):
        if key not in excluded and current.get(key) != predecessor_metadata.get(key):
            raise RuntimeError(f"Successor draft has unexpected metadata drift: {key}")

    baseline = copy.deepcopy(current)
    if states[0] == "target":
        for key in MUTATED_METADATA_KEYS:
            if key in predecessor_metadata:
                baseline[key] = copy.deepcopy(predecessor_metadata[key])
            else:
                baseline.pop(key, None)
    target = copy.deepcopy(baseline)
    target.update(desired_values)
    if target.get("creators") != predecessor_metadata.get("creators"):
        raise RuntimeError("Target metadata would alter creators")
    if target.get("license") != predecessor_metadata.get("license"):
        raise RuntimeError("Target metadata would alter the license")
    assert_no_local_profile_name(target)
    if current not in (baseline, target):
        raise RuntimeError("Draft metadata is neither the baseline nor exact target")
    return baseline, target


def find_existing_concept_draft(token: str) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {"status": "draft", "size": 100, "q": f"conceptrecid:{CONCEPT_RECORD_ID}"}
    )
    _, rows = request_json(
        f"https://zenodo.org/api/deposit/depositions?{query}", token=token
    )
    if not isinstance(rows, list):
        raise RuntimeError("Zenodo draft search returned malformed data")
    candidates = [
        row
        for row in rows
        if str(row.get("conceptrecid")) == CONCEPT_RECORD_ID
        and row.get("submitted") is False
        and row.get("state") != "done"
    ]
    if len(candidates) > 1:
        raise RuntimeError("More than one unpublished draft exists in the concept lineage")
    if not candidates:
        return None
    draft_id = int(candidates[0].get("id", -1))
    _, draft = request_json(
        f"https://zenodo.org/api/deposit/depositions/{draft_id}", token=token
    )
    return draft


def validated_draft_links(draft: dict[str, Any]) -> dict[str, Any]:
    if str(draft.get("conceptrecid")) != CONCEPT_RECORD_ID:
        raise RuntimeError("Successor draft escaped the concept lineage")
    if draft.get("submitted") is not False or draft.get("state") == "done":
        raise RuntimeError("Successor draft is not mutable")
    draft_id = int(draft.get("id", -1))
    if draft_id <= 0 or draft_id == PREDECESSOR_ID:
        raise RuntimeError("Successor draft identity is invalid")
    links = draft.get("links", {})
    result = {
        "record_id": draft_id,
        "self_url": links.get("self"),
        "bucket_url": links.get("bucket"),
        "publish_url": links.get("publish"),
    }
    for key in ("self_url", "bucket_url", "publish_url"):
        if not isinstance(result[key], str) or not result[key]:
            raise RuntimeError(f"Successor draft lacks {key}")
        validate_zenodo_url(result[key], authenticated=True)
    expected_self = f"/api/deposit/depositions/{draft_id}"
    if urllib.parse.urlparse(result["self_url"]).path.rstrip("/") != expected_self:
        raise RuntimeError("Successor draft self link does not bind its exact identity")
    return result


def new_or_adopt_draft(
    token: str, predecessor: dict[str, Any]
) -> tuple[dict[str, Any], str, dict[str, Any], dict[str, Any]]:
    _, authenticated_predecessor = request_json(
        f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}", token=token
    )
    if authenticated_predecessor.get("submitted") is not True:
        raise RuntimeError("Authenticated predecessor deposition is not published")
    if authenticated_predecessor.get("metadata", {}).get("creators") != (
        predecessor.get("metadata", {}).get("creators")
    ):
        raise RuntimeError(
            "Authenticated and anonymous predecessor creators disagree"
        )
    if canonical_license_id(
        authenticated_predecessor.get("metadata", {}).get("license")
    ) != canonical_license_id(predecessor.get("metadata", {}).get("license")):
        raise RuntimeError("Authenticated and anonymous predecessor license disagrees")

    draft = find_existing_concept_draft(token)
    origin = "adopted_existing"
    if draft is None:
        _, created = request_json(
            f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}/actions/newversion",
            method="POST",
            token=token,
            expected=(201,),
        )
        latest_draft_url = created.get("links", {}).get("latest_draft")
        if isinstance(latest_draft_url, str):
            _, candidate = request_json(latest_draft_url, token=token)
            if candidate.get("submitted") is False and candidate.get("state") != "done":
                draft = candidate
        if draft is None:
            for _ in range(12):
                draft = find_existing_concept_draft(token)
                if draft is not None:
                    break
                time.sleep(1.0)
        if draft is None:
            raise RuntimeError("New-version action did not expose a successor draft")
        origin = "created_now"

    validated_draft_links(draft)
    baseline, target = make_target_draft_metadata(
        copy.deepcopy(draft.get("metadata", {})),
        authenticated_predecessor,
    )
    return draft, origin, baseline, target


def make_initial_state(
    draft: dict[str, Any],
    origin: str,
    baseline_metadata: dict[str, Any],
    target_metadata: dict[str, Any],
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
) -> dict[str, Any]:
    links = validated_draft_links(draft)
    state = {
        "schema": "ega-i-6.6.3-semantic-zenodo-state/v1",
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "status": "draft",
        "stage": "draft_adopted_and_frozen",
        "predecessor": {
            "record_id": PREDECESSOR_ID,
            "concept_record_id": int(CONCEPT_RECORD_ID),
            "concept_doi": CONCEPT_DOI,
        },
        "payload": identities,
        "preserved_public_metadata": {
            "creators": copy.deepcopy(predecessor.get("metadata", {}).get("creators")),
            "license": copy.deepcopy(predecessor.get("metadata", {}).get("license")),
        },
        "baseline_metadata": baseline_metadata,
        "target_metadata": target_metadata,
        "draft": {"origin": origin, **links},
    }
    assert_no_local_profile_name(state)
    return state


def update_state(state_path: Path, state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    updated.update(changes)
    updated["updated_utc"] = utc_now()
    assert_no_local_profile_name(updated)
    write_json_atomic(state_path, updated)
    return updated


def load_state(
    state_path: Path, identities: list[dict[str, Any]], predecessor: dict[str, Any]
) -> dict[str, Any] | None:
    if not state_path.is_file():
        return None
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError("Persisted release state is malformed") from error
    if state.get("schema") != "ega-i-6.6.3-semantic-zenodo-state/v1":
        raise RuntimeError("Persisted release-state schema mismatch")
    if state.get("status") not in {"draft", "published", "verified"}:
        raise RuntimeError("Persisted release state has an invalid status")
    if state.get("payload") != identities:
        raise RuntimeError("Local payload differs from the frozen release state")
    predecessor_state = state.get("predecessor", {})
    if (
        int(predecessor_state.get("record_id", -1)) != PREDECESSOR_ID
        or str(predecessor_state.get("concept_record_id")) != CONCEPT_RECORD_ID
        or predecessor_state.get("concept_doi") != CONCEPT_DOI
    ):
        raise RuntimeError("Persisted release state has the wrong lineage")
    expected_preserved = {
        "creators": predecessor.get("metadata", {}).get("creators"),
        "license": predecessor.get("metadata", {}).get("license"),
    }
    if state.get("preserved_public_metadata") != expected_preserved:
        raise RuntimeError("Persisted creators or license differ from the predecessor")
    baseline = state.get("baseline_metadata")
    target = state.get("target_metadata")
    if not isinstance(baseline, dict) or not isinstance(target, dict):
        raise RuntimeError("Persisted metadata is malformed")
    derived_target = copy.deepcopy(baseline)
    derived_target.update(
        {
            "title": TITLE,
            "version": VERSION,
            "access_right": "open",
            "description": DESCRIPTION,
        }
    )
    if derived_target != target:
        raise RuntimeError("Persisted target metadata is not deterministic")
    if target.get("creators") != expected_preserved["creators"]:
        raise RuntimeError("Persisted target metadata would alter creators")
    if canonical_license_id(target.get("license")) != canonical_license_id(
        expected_preserved["license"]
    ):
        raise RuntimeError("Persisted target metadata would alter the license")
    draft = state.get("draft")
    if not isinstance(draft, dict):
        raise RuntimeError("Persisted draft identity is malformed")
    for key in ("self_url", "bucket_url", "publish_url"):
        if not isinstance(draft.get(key), str):
            raise RuntimeError(f"Persisted draft lacks {key}")
        validate_zenodo_url(draft[key], authenticated=True)
    if not isinstance(draft.get("record_id"), int):
        raise RuntimeError("Persisted draft record ID is malformed")
    if state["status"] in {"published", "verified"} and not isinstance(
        state.get("published_record_id"), int
    ):
        raise RuntimeError("Published state lacks a record ID")
    assert_no_local_profile_name(state)
    return state


def draft_row_identity(row: dict[str, Any]) -> tuple[str, int, str]:
    name = row.get("filename") or row.get("key")
    if not isinstance(name, str) or not name:
        raise RuntimeError("Draft contains a file without a valid filename")
    if name in {".", ".."} or "/" in name or "\\" in name or re.match(r"^[A-Za-z]:", name):
        raise RuntimeError("Draft contains a path-shaped filename; refusing mutation")
    size = int(row.get("filesize", row.get("size", -1)))
    md5 = normalize_checksum(str(row.get("checksum", "")))
    if size < 0 or not re.fullmatch(r"[0-9A-F]{32}", md5):
        raise RuntimeError(f"Draft file identity is malformed: {name}")
    return name, size, md5


def draft_download_url(row: dict[str, Any]) -> str:
    links = row.get("links", {})
    url = links.get("download") or links.get("self")
    if not isinstance(url, str) or not url:
        raise RuntimeError("Draft file lacks an authenticated readback URL")
    validate_zenodo_url(url, authenticated=True)
    return url


def delete_exact_draft_file(row: dict[str, Any], draft_id: int, token: str) -> None:
    file_id = row.get("id")
    url = row.get("links", {}).get("self")
    if not isinstance(file_id, str) or not file_id:
        raise RuntimeError("Draft file lacks a deletion identity")
    if not isinstance(url, str) or not url:
        raise RuntimeError("Draft file lacks a deletion URL")
    validate_zenodo_url(url, authenticated=True)
    parsed = urllib.parse.urlparse(url)
    expected_path = f"/api/deposit/depositions/{draft_id}/files/{file_id}"
    if parsed.path.rstrip("/") != expected_path:
        raise RuntimeError("Refusing a draft-file deletion outside the exact successor draft")
    request_no_content(url, method="DELETE", token=token, expected=(204,))


def clean_draft_files(
    draft: dict[str, Any],
    draft_id: int,
    identities: list[dict[str, Any]],
    token: str,
) -> list[dict[str, Any]]:
    expected = {row["remote_filename"]: row for row in identities}
    kept: set[str] = set()
    actions: list[dict[str, Any]] = []
    rows = draft.get("files", [])
    if not isinstance(rows, list):
        raise RuntimeError("Draft file list is malformed")
    for row in rows:
        name, size, md5 = draft_row_identity(row)
        target = expected.get(name)
        reason = "removed_not_in_release"
        keep = False
        if target is not None and name not in kept:
            if size == target["bytes"] and md5 == target["md5"]:
                read_bytes, read_sha256 = download_sha256(
                    draft_download_url(row), token=token
                )
                if read_bytes != target["bytes"] or read_sha256 != target["sha256"]:
                    raise RuntimeError(
                        f"Existing draft file has an MD5 match but SHA-256 mismatch: {name}"
                    )
                keep = True
                kept.add(name)
            else:
                reason = "replaced_incorrect_identity"
        elif target is not None:
            reason = "removed_duplicate"
        if keep:
            actions.append({"remote_filename": name, "action": "kept_exact"})
            continue
        delete_exact_draft_file(row, draft_id, token)
        actions.append(
            {
                "remote_filename": name,
                "action": reason,
                "removed_bytes": size,
                "removed_md5": md5,
            }
        )
    return actions


def assert_exact_draft_inventory(
    draft: dict[str, Any], identities: list[dict[str, Any]]
) -> None:
    if draft_inventory(draft) != inventory_from_identities(identities):
        raise RuntimeError("Draft inventory is not exactly the six frozen local assets")


def verify_draft_sha256s(
    draft: dict[str, Any], identities: list[dict[str, Any]], token: str
) -> None:
    expected = {row["remote_filename"]: row for row in identities}
    seen: set[str] = set()
    for row in draft.get("files", []):
        name, _, _ = draft_row_identity(row)
        if name not in expected or name in seen:
            raise RuntimeError("Draft strong-hash readback found an unexpected file")
        seen.add(name)
        read_bytes, read_sha256 = download_sha256(draft_download_url(row), token=token)
        if read_bytes != expected[name]["bytes"] or read_sha256 != expected[name]["sha256"]:
            raise RuntimeError(f"Authenticated draft SHA-256 mismatch: {name}")
    if seen != set(expected):
        raise RuntimeError("Authenticated draft readback did not cover all six files")


def validate_public_metadata(
    record: dict[str, Any], predecessor: dict[str, Any]
) -> list[str]:
    metadata = record.get("metadata", {})
    if not metadata_matches_target_public(metadata, predecessor):
        raise RuntimeError("Published metadata differs from the exact target")
    predecessor_metadata = predecessor.get("metadata", {})
    verified: list[str] = []
    for key in PUBLIC_STABLE_METADATA_KEYS:
        if key in predecessor_metadata or key in metadata:
            if metadata.get(key) != predecessor_metadata.get(key):
                raise RuntimeError(f"Published stable metadata drift: {key}")
            verified.append(key)
    if metadata.get("access_right") != "open":
        raise RuntimeError("Published successor is not open access")
    assert_no_local_profile_name(metadata)
    return verified


def validate_public_snapshot(
    record: dict[str, Any],
    predecessor: dict[str, Any],
    identities: list[dict[str, Any]],
) -> list[str]:
    validate_lineage_record(record)
    if public_inventory(record) != inventory_from_identities(identities):
        raise RuntimeError("Published inventory is not exactly the six frozen assets")
    return validate_public_metadata(record, predecessor)


def poll_public_record(
    record_id: int,
    predecessor: dict[str, Any],
    identities: list[dict[str, Any]],
    *,
    attempts: int = 60,
) -> tuple[dict[str, Any], list[str]]:
    last_error = "record not yet visible"
    for attempt in range(attempts):
        try:
            _, record = request_json(f"https://zenodo.org/api/records/{record_id}")
            stable_keys = validate_public_snapshot(record, predecessor, identities)
            _, latest = request_json(
                f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
            )
            validate_lineage_record(latest)
            if int(latest.get("id", -1)) != record_id:
                raise RuntimeError("Published successor is not the latest concept version")
            return record, stable_keys
        except RuntimeError as error:
            last_error = str(error)
        if attempt + 1 < attempts:
            time.sleep(2.0)
    raise RuntimeError(f"Public successor did not reach the exact target state: {last_error}")


def verify_public_downloads(
    record: dict[str, Any], identities: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    expected = {row["remote_filename"]: row for row in identities}
    rows = record.get("files", [])
    by_name: dict[str, dict[str, Any]] = {}
    for row in rows:
        name = row.get("key")
        if not isinstance(name, str) or name in by_name:
            raise RuntimeError("Public download inventory contains a duplicate filename")
        by_name[name] = row
    if set(by_name) != set(expected):
        raise RuntimeError("Public download inventory is not the six-file target")
    readbacks: list[dict[str, Any]] = []
    for name in sorted(expected):
        row = by_name[name]
        url = row.get("links", {}).get("self") or row.get("links", {}).get("download")
        if not isinstance(url, str) or not url:
            raise RuntimeError(f"Public file lacks an anonymous download URL: {name}")
        read_bytes, read_sha256 = download_sha256(url)
        if read_bytes != expected[name]["bytes"] or read_sha256 != expected[name]["sha256"]:
            raise RuntimeError(f"Anonymous public download mismatch: {name}")
        readbacks.append(
            {
                "remote_filename": name,
                "bytes": read_bytes,
                "sha256": read_sha256,
                "status": "PASS",
            }
        )
    return readbacks


def make_receipt(
    record: dict[str, Any],
    predecessor: dict[str, Any],
    identities: list[dict[str, Any]],
    stable_keys: list[str],
    actions: list[dict[str, Any]],
) -> dict[str, Any]:
    receipt = {
        "schema": "ega-i-6.6.3-semantic-zenodo-publication-receipt/v1",
        "created_utc": utc_now(),
        "status": "PASS",
        "predecessor": {
            "record_id": PREDECESSOR_ID,
            "doi": predecessor.get("doi"),
            "concept_record_id": int(CONCEPT_RECORD_ID),
            "concept_doi": CONCEPT_DOI,
        },
        "published": {
            "record_id": int(record["id"]),
            "doi": record.get("doi"),
            "concept_record_id": int(CONCEPT_RECORD_ID),
            "concept_doi": CONCEPT_DOI,
            "title": TITLE,
            "version": VERSION,
            "access_right": "open",
            "file_count": len(identities),
        },
        "metadata": {
            "creators_retained_exact": True,
            "license_retained_exact": True,
            "stable_keys_verified": stable_keys,
            "r32_pdfs_unchanged_noted": True,
            "continuation_at_ega_i_6_6_4_noted": True,
        },
        "release_inventory": identities,
        "draft_actions": actions,
        "anonymous_public_readback": verify_public_downloads(record, identities),
    }
    assert_no_local_profile_name(receipt)
    return receipt


def finalize_receipt(
    receipt_path: Path,
    state_path: Path,
    state: dict[str, Any] | None,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    write_json_atomic(receipt_path, receipt)
    if state is not None:
        update_state(
            state_path,
            state,
            status="verified",
            stage="anonymous_readback_complete",
            published_record_id=int(receipt["published"]["record_id"]),
            receipt_identity={
                "bytes": receipt_path.stat().st_size,
                "sha256": digest(receipt_path, "sha256"),
            },
        )
    return receipt


def recover_published_successor(
    predecessor: dict[str, Any],
    identities: list[dict[str, Any]],
    *,
    attempts: int,
) -> tuple[dict[str, Any], list[str]] | None:
    for attempt in range(attempts):
        _, latest = request_json(
            f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
        )
        validate_lineage_record(latest)
        latest_id = int(latest.get("id", -1))
        if latest_id != PREDECESSOR_ID:
            stable_keys = validate_public_snapshot(latest, predecessor, identities)
            return latest, stable_keys
        if attempt + 1 < attempts:
            time.sleep(2.0)
    return None


def execute_release(
    asset_dir: Path,
    state_path: Path,
    receipt_path: Path,
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    latest: dict[str, Any],
) -> dict[str, Any]:
    state = load_state(state_path, identities, predecessor)
    if state is None and int(latest.get("id", -1)) != PREDECESSOR_ID:
        raise RuntimeError("No release state exists and the predecessor is no longer latest")

    if state is not None and state["status"] in {"published", "verified"}:
        record, stable_keys = poll_public_record(
            int(state["published_record_id"]), predecessor, identities
        )
        receipt = make_receipt(
            record,
            predecessor,
            identities,
            stable_keys,
            state.get("draft_actions", []),
        )
        return finalize_receipt(receipt_path, state_path, state, receipt)

    if state is not None and int(latest.get("id", -1)) != PREDECESSOR_ID:
        recovered = recover_published_successor(predecessor, identities, attempts=1)
        if recovered is None:
            raise RuntimeError("Concept latest advanced without an exact published successor")
        record, stable_keys = recovered
        state = update_state(
            state_path,
            state,
            status="published",
            stage="published_successor_recovered",
            published_record_id=int(record["id"]),
        )
        receipt = make_receipt(
            record,
            predecessor,
            identities,
            stable_keys,
            state.get("draft_actions", []),
        )
        return finalize_receipt(receipt_path, state_path, state, receipt)

    token = load_token()
    if state is None:
        draft, origin, baseline, target = new_or_adopt_draft(token, predecessor)
        state = make_initial_state(
            draft, origin, baseline, target, identities, predecessor
        )
        write_json_atomic(state_path, state)

    draft_links = state["draft"]
    try:
        _, draft = request_json(draft_links["self_url"], token=token)
    except RuntimeError:
        recovered = recover_published_successor(predecessor, identities, attempts=45)
        if recovered is None:
            raise RuntimeError(
                "Persisted draft is unavailable and no exact published successor appeared"
            )
        record, stable_keys = recovered
        state = update_state(
            state_path,
            state,
            status="published",
            stage="published_successor_recovered",
            published_record_id=int(record["id"]),
        )
        receipt = make_receipt(
            record,
            predecessor,
            identities,
            stable_keys,
            state.get("draft_actions", []),
        )
        return finalize_receipt(receipt_path, state_path, state, receipt)

    live_links = validated_draft_links(draft)
    if any(live_links[key] != draft_links[key] for key in live_links):
        raise RuntimeError("Persisted draft identity or action links drifted")
    current_metadata = draft.get("metadata", {})
    if current_metadata not in (state["baseline_metadata"], state["target_metadata"]):
        raise RuntimeError("Draft metadata differs from both frozen accepted states")

    actions = list(state.get("draft_actions", []))
    if state.get("stage") not in {
        "inventory_exact",
        "metadata_exact",
        "publish_pending",
    }:
        actions.extend(
            clean_draft_files(draft, int(draft_links["record_id"]), identities, token)
        )
        _, draft = request_json(draft_links["self_url"], token=token)
        partial = draft_inventory(draft)
        expected = inventory_from_identities(identities)
        if any(name not in expected or identity != expected[name] for name, identity in partial.items()):
            raise RuntimeError("Post-clean draft contains an unexpected file identity")
        by_name = {row["remote_filename"]: row for row in identities}
        for name in sorted(set(expected) - set(partial)):
            local_path = asset_dir / name
            response = upload_file(draft_links["bucket_url"], local_path, name, token)
            response_bytes = int(response.get("size", response.get("filesize", -1)))
            response_md5 = normalize_checksum(str(response.get("checksum", "")))
            if response_bytes != by_name[name]["bytes"] or response_md5 != by_name[name]["md5"]:
                raise RuntimeError(f"Upload identity mismatch: {name}")
            actions.append({"remote_filename": name, "action": "uploaded"})
        _, draft = request_json(draft_links["self_url"], token=token)
        assert_exact_draft_inventory(draft, identities)
        verify_draft_sha256s(draft, identities, token)
        state = update_state(
            state_path,
            state,
            status="draft",
            stage="inventory_exact",
            draft_actions=actions,
        )

    _, draft = request_json(draft_links["self_url"], token=token)
    assert_exact_draft_inventory(draft, identities)
    current_metadata = draft.get("metadata", {})
    if current_metadata == state["baseline_metadata"]:
        request_json(
            draft_links["self_url"],
            method="PUT",
            token=token,
            payload={"metadata": state["target_metadata"]},
            expected=(200,),
        )
        _, draft = request_json(draft_links["self_url"], token=token)
    elif current_metadata != state["target_metadata"]:
        raise RuntimeError("Draft metadata is not a frozen accepted state")
    if draft.get("metadata", {}) != state["target_metadata"]:
        raise RuntimeError("Draft metadata write/readback mismatch")
    assert_exact_draft_inventory(draft, identities)
    verify_draft_sha256s(draft, identities, token)
    state = update_state(
        state_path,
        state,
        status="draft",
        stage="publish_pending",
        draft_actions=actions,
    )

    recovered = recover_published_successor(predecessor, identities, attempts=1)
    if recovered is not None:
        record, stable_keys = recovered
    else:
        try:
            _, published = request_json(
                draft_links["publish_url"],
                method="POST",
                token=token,
                expected=(202,),
            )
            raw_record_id = published.get("record_id") or published.get("id")
            if raw_record_id is None:
                raise RuntimeError("Publish response omitted the record ID")
            record_id = int(raw_record_id)
            state = update_state(
                state_path,
                state,
                status="published",
                stage="publish_response_persisted",
                published_record_id=record_id,
            )
            record, stable_keys = poll_public_record(record_id, predecessor, identities)
        except RuntimeError:
            recovered = recover_published_successor(predecessor, identities, attempts=45)
            if recovered is None:
                raise
            record, stable_keys = recovered

    state = update_state(
        state_path,
        state,
        status="published",
        stage="published_record_verified",
        published_record_id=int(record["id"]),
    )
    receipt = make_receipt(
        record,
        predecessor,
        identities,
        stable_keys,
        state.get("draft_actions", actions),
    )
    return finalize_receipt(receipt_path, state_path, state, receipt)


def verify_existing_record(
    record_id: int,
    receipt_path: Path,
    state_path: Path,
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
) -> dict[str, Any]:
    state = load_state(state_path, identities, predecessor)
    if state is not None and state.get("published_record_id") not in (None, record_id):
        raise RuntimeError("Requested record conflicts with the persisted release state")
    record, stable_keys = poll_public_record(record_id, predecessor, identities)
    receipt = make_receipt(
        record,
        predecessor,
        identities,
        stable_keys,
        state.get("draft_actions", []) if state else [],
    )
    if state is not None:
        state = update_state(
            state_path,
            state,
            status="published",
            stage="verification_record_bound",
            published_record_id=record_id,
        )
    return finalize_receipt(receipt_path, state_path, state, receipt)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish the EGA I §6.6.3 semantic checkpoint to Zenodo."
    )
    parser.add_argument("--asset-dir", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--execute",
        action="store_true",
        help="Create/adopt the successor draft, replace its inventory, publish, and verify.",
    )
    action.add_argument(
        "--verify-record-id",
        type=int,
        metavar="ID",
        help="Anonymously verify an already-published exact successor.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.state.resolve() == args.receipt.resolve():
        raise RuntimeError("State and receipt paths must differ")
    asset_root = args.asset_dir.resolve()
    if args.state.resolve().is_relative_to(asset_root) or args.receipt.resolve().is_relative_to(
        asset_root
    ):
        raise RuntimeError("State and receipt paths must be outside the frozen asset directory")
    if (args.state.exists() and not args.state.is_file()) or (
        args.receipt.exists() and not args.receipt.is_file()
    ):
        raise RuntimeError("State and receipt destinations must be ordinary files")
    identities = validate_local_assets(args.asset_dir)
    predecessor, latest = anonymous_preflight(
        require_predecessor_latest=(
            not args.state.is_file() and args.verify_record_id is None
        )
    )

    if args.verify_record_id is not None:
        receipt = verify_existing_record(
            args.verify_record_id,
            args.receipt,
            args.state,
            identities,
            predecessor,
        )
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0

    if args.execute:
        receipt = execute_release(
            args.asset_dir,
            args.state,
            args.receipt,
            identities,
            predecessor,
            latest,
        )
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0

    state = load_state(args.state, identities, predecessor)
    preflight = {
        "schema": "ega-i-6.6.3-semantic-zenodo-preflight/v1",
        "status": "PASS",
        "predecessor_id": PREDECESSOR_ID,
        "latest_public_id": int(latest["id"]),
        "concept_record_id": int(CONCEPT_RECORD_ID),
        "concept_doi": CONCEPT_DOI,
        "title": TITLE,
        "version": VERSION,
        "access_right": "open",
        "file_count": len(identities),
        "payload": identities,
        "release_state": state.get("status") if state else "not_started",
        "credential_read": False,
        "mutation_performed": False,
    }
    assert_no_local_profile_name(preflight)
    print(json.dumps(preflight, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
