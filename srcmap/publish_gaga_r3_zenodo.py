#!/usr/bin/env python3
"""Publish the audited GAGA R3 payload as a verified Zenodo successor version."""

from __future__ import annotations

import argparse
import copy
import csv
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


ROOT = Path(__file__).resolve().parent.parent
PREDECESSOR_ID = 22074492
CONCEPT_ID = "21781322"
EXPECTED_INHERITED_FILES = 69
MAX_ZENODO_FILES = 100
TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
RECEIPT = ROOT / "output" / "publication" / "GAGA_STACKS_R3_PUBLICATION_RECEIPT.json"
MANIFEST = ROOT / "output" / "publication" / "GAGA_STACKS_R3_MANIFEST.csv"
STATE = ROOT / "output" / "publication" / "GAGA_STACKS_R3_ZENODO_STATE.json"
R3_CHECK_SHA256 = "8A67743F56BC828558624019B3DA9CD6317F5CE4FFF8B811926023B57344922D"
NEW_VERSION = "2026-08-24 GAGA R3 Stacks bridge and localized editions"
DESCRIPTION_APPENDIX = (
    "<p>This R3 successor adds the audited GAGA-to-Stacks bridge: a 126-unit "
    "mapping with 79 explicit decisions, zero remaining review units, and zero "
    "remaining substantive statement gaps. It also adds fixed-point-built and "
    "visually inspected English, Japanese, and Simplified-Chinese PDF editions, "
    "their TeX sources, and deterministic validation tools and receipts.</p>"
)
PUBLIC_STABLE_METADATA_KEYS = (
    "title",
    "creators",
    "contributors",
    "resource_type",
    "upload_type",
    "access_right",
    "license",
    "keywords",
    "related_identifiers",
    "communities",
    "subjects",
    "language",
    "notes",
    "references",
)

PAYLOAD: tuple[tuple[str, str], ...] = (
    ("output/pdf/gaga-english.pdf", "60_GAGA_Stacks_R3_English.pdf"),
    ("output/pdf/gaga-japanese.pdf", "61_GAGA_Stacks_R3_Japanese.pdf"),
    ("output/pdf/gaga-simplified-chinese.pdf", "62_GAGA_Stacks_R3_Simplified_Chinese.pdf"),
    ("gaga.tex", "63_GAGA_Stacks_R3_English.tex"),
    ("output/source/gaga-ja.tex", "64_GAGA_Stacks_R3_Japanese.tex"),
    ("output/source/gaga-zh-cn.tex", "65_GAGA_Stacks_R3_Simplified_Chinese.tex"),
    ("output/source/chapters-ja.tex", "66_GAGA_Stacks_R3_Japanese_chapters.tex"),
    ("output/source/chapters-zh-cn.tex", "67_GAGA_Stacks_R3_Simplified_Chinese_chapters.tex"),
    ("preamble.tex", "68_GAGA_Stacks_R3_preamble.tex"),
    ("chapters.tex", "69_GAGA_Stacks_R3_chapters.tex"),
    ("my.bib", "70_GAGA_Stacks_R3_bibliography.bib"),
    ("stacks-project.cls", "71_GAGA_Stacks_R3_class.cls"),
    ("gaga_r3/units.csv", "72_GAGA_Stacks_R3_units.csv"),
    ("gaga_r3/map.csv", "73_GAGA_Stacks_R3_map.csv"),
    ("gaga_r3/dec.csv", "74_GAGA_Stacks_R3_decisions.csv"),
    ("gaga_r3/issues.csv", "75_GAGA_Stacks_R3_source_issues.csv"),
    ("gaga_r3/mcheck.json", "76_GAGA_Stacks_R3_mapping_check.json"),
    ("gaga_r3/R3_CHECK.json", "77_GAGA_Stacks_R3_terminal_receipt.json"),
    ("srcmap/build_gaga_r3.py", "78_GAGA_Stacks_R3_builder.py"),
    ("srcmap/validate_gaga_editions.py", "79_GAGA_Stacks_R3_edition_validator.py"),
    ("srcmap/build_gaga_localized_editions.py", "80_GAGA_Stacks_R3_edition_builder.py"),
    ("output/validation/gaga-localized-build-validation.json", "81_GAGA_Stacks_R3_localized_build_validation.json"),
    ("output/publication/GAGA_STACKS_R3_README.md", "82_GAGA_Stacks_R3_README.md"),
    ("output/publication/GAGA_STACKS_R3_MANIFEST.csv", "83_GAGA_Stacks_R3_MANIFEST.csv"),
    ("srcmap/publish_gaga_r3_zenodo.py", "84_GAGA_Stacks_R3_Zenodo_publisher.py"),
)


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest().upper()


def local_identity(local: str, remote: str) -> dict[str, Any]:
    path = ROOT / local
    return {
        "local_path": local,
        "remote_filename": remote,
        "bytes": path.stat().st_size,
        "md5": digest(path, "md5"),
        "sha256": digest(path, "sha256"),
    }


def require_current_identity(
    row: dict[str, Any], expected_path: str, *, recorded_path: str | None = None
) -> None:
    actual_recorded_path = row.get("path", row.get("name"))
    expected_recorded_path = recorded_path if recorded_path is not None else expected_path
    if actual_recorded_path != expected_recorded_path:
        raise RuntimeError(
            f"Receipt path mismatch: expected {expected_recorded_path}; "
            f"found {actual_recorded_path}"
        )
    path = ROOT / expected_path
    if not path.is_file():
        raise RuntimeError(f"Receipt-bound file is missing: {expected_path}")
    if int(row.get("bytes", -1)) != path.stat().st_size:
        raise RuntimeError(f"Receipt-bound byte count drift: {expected_path}")
    if row.get("sha256", "").upper() != digest(path, "sha256"):
        raise RuntimeError(f"Receipt-bound SHA-256 drift: {expected_path}")


def normalize_checksum(value: str) -> str:
    return value.split(":", 1)[-1].upper()


def public_inventory(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in record.get("files", []):
        key = row["key"]
        if key in result:
            raise RuntimeError(f"Duplicate public filename: {key}")
        result[key] = {
            "bytes": int(row["size"]),
            "md5": normalize_checksum(row["checksum"]),
        }
    return result


def draft_inventory(deposition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in deposition.get("files", []):
        key = row.get("filename") or row.get("key")
        size = row.get("filesize", row.get("size"))
        if key in result:
            raise RuntimeError(f"Duplicate draft filename: {key}")
        result[key] = {
            "bytes": int(size),
            "md5": normalize_checksum(row["checksum"]),
        }
    return result


def validate_zenodo_url(url: str, *, require_api: bool = False) -> None:
    parsed = urllib.parse.urlparse(url)
    try:
        port = parsed.port
    except ValueError as error:
        raise RuntimeError(f"Refusing malformed Zenodo URL: {url}") from error
    if (
        parsed.scheme != "https"
        or parsed.hostname != "zenodo.org"
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
        or (require_api and not parsed.path.startswith("/api/"))
    ):
        raise RuntimeError(f"Refusing non-Zenodo action URL: {url}")


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
            require_api=req.get_header("Authorization") is not None,
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
) -> tuple[int, Any]:
    validate_zenodo_url(url, require_api=token is not None)
    headers = {"Accept": "application/json"}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with ZENODO_OPENER.open(request, timeout=60) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zenodo request failed: HTTP {error.code}; body={body[:2000]}") from error
    if status not in expected:
        raise RuntimeError(f"Unexpected HTTP status {status} for {method} {url}")
    return status, json.loads(body.decode("utf-8"))


def upload_file(bucket: str, path: Path, remote: str, token: str) -> dict[str, Any]:
    url = bucket.rstrip("/") + "/" + urllib.parse.quote(remote, safe="")
    validate_zenodo_url(url, require_api=True)
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream",
    }
    request = urllib.request.Request(url, data=path.read_bytes(), headers=headers, method="PUT")
    try:
        with ZENODO_OPENER.open(request, timeout=120) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Upload failed for {remote}: HTTP {error.code}; body={body[:2000]}") from error
    if status < 200 or status >= 300:
        raise RuntimeError(f"Upload failed for {remote}: HTTP {status}")
    return json.loads(body.decode("utf-8"))


def download_sha256(url: str) -> tuple[int, str]:
    validate_zenodo_url(url)
    request = urllib.request.Request(url)
    hasher = hashlib.sha256()
    total = 0
    with ZENODO_OPENER.open(request, timeout=120) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
            total += len(chunk)
    return total, hasher.hexdigest().upper()


def load_token() -> str:
    text = TOKEN_FILE.read_text(encoding="utf-8")
    candidates = re.findall(
        r"(?<![A-Za-z0-9._-])([A-Za-z0-9][A-Za-z0-9._-]{39,})(?![A-Za-z0-9._-])",
        text,
    )
    candidates = list(dict.fromkeys(candidates))
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one token-shaped value in the credential file; found {len(candidates)}"
        )
    return candidates[0]


def validate_local_payload() -> list[dict[str, Any]]:
    if len({remote for _, remote in PAYLOAD}) != len(PAYLOAD):
        raise RuntimeError("Payload contains duplicate remote filenames")
    missing = [local for local, _ in PAYLOAD if not (ROOT / local).is_file()]
    if missing:
        raise RuntimeError(f"Payload files are missing: {missing}")
    assert_profile_name_absent_from_payload([ROOT / local for local, _ in PAYLOAD])
    if EXPECTED_INHERITED_FILES + len(PAYLOAD) > MAX_ZENODO_FILES:
        raise RuntimeError("Payload would exceed Zenodo's 100-file limit")

    r3_path = ROOT / "gaga_r3" / "R3_CHECK.json"
    if digest(r3_path, "sha256") != R3_CHECK_SHA256:
        raise RuntimeError("GAGA R3 terminal receipt identity drift")
    r3 = json.loads(r3_path.read_text(encoding="utf-8"))
    if r3.get("status") != "STRICT_PASS":
        raise RuntimeError("GAGA R3 terminal receipt is not STRICT_PASS")
    counts = r3.get("mapping", {}).get("counts", {})
    if (
        counts.get("units") != 126
        or counts.get("decisions") != 79
        or counts.get("review_units") != 0
        or counts.get("candidate_units") != 0
        or r3.get("mapping", {}).get("gaga_true_gaps_after") != 0
    ):
        raise RuntimeError("GAGA R3 terminal counts drifted")

    integration_rows = {row["name"]: row for row in r3.get("integration", {}).get("files", [])}
    for path in ("gaga.tex", "preamble.tex", "chapters.tex", "my.bib"):
        if path not in integration_rows:
            raise RuntimeError(f"GAGA R3 receipt lacks integration identity: {path}")
        require_current_identity(integration_rows[path], path)

    build_rows = {row["name"]: row for row in r3.get("build", {}).get("files", [])}
    if "output/pdf/gaga-english.pdf" not in build_rows:
        raise RuntimeError("GAGA R3 receipt lacks the English PDF identity")
    require_current_identity(build_rows["output/pdf/gaga-english.pdf"], "output/pdf/gaga-english.pdf")
    english_render = r3.get("build", {}).get("visual_review", {})
    if english_render.get("status") != "PASS_ALL_22_PAGES_PRIMARY_AGENT":
        raise RuntimeError("English visual-review receipt is not PASS")
    english_render_rows = english_render.get("pages", [])
    if len(english_render_rows) != 22:
        raise RuntimeError("English visual-review receipt does not contain 22 pages")
    for row in english_render_rows:
        require_current_identity(row, row["name"])

    mapping_rows = {row["name"]: row for row in r3.get("files_before_receipt", [])}
    for name in ("units.csv", "map.csv", "dec.csv", "issues.csv", "mcheck.json"):
        if name not in mapping_rows:
            raise RuntimeError(f"GAGA R3 receipt lacks mapping identity: {name}")
        require_current_identity(mapping_rows[name], f"gaga_r3/{name}", recorded_path=name)

    localized = json.loads(
        (ROOT / "output" / "validation" / "gaga-localized-build-validation.json").read_text(
            encoding="utf-8"
        )
    )
    if localized.get("status") != "PASS":
        raise RuntimeError("Localized build validation is not PASS")
    if localized.get("visual_inspection", {}).get("status") != "PASS":
        raise RuntimeError("Localized visual inspection is not PASS")
    if localized.get("visual_inspection", {}).get("inspected_pages") != 40:
        raise RuntimeError("Localized visual inspection is not bound to all 40 pages")

    source_results = localized.get("source_validation", {}).get("results", [])
    if localized.get("source_validation", {}).get("status") != "PASS":
        raise RuntimeError("Nested localized source validation is not PASS")
    if len(source_results) != 2 or {row.get("language") for row in source_results} != {"ja", "zh-cn"}:
        raise RuntimeError("Localized source receipt does not contain exactly both languages")
    for row in source_results:
        if row.get("status") != "PASS":
            raise RuntimeError(f"Localized source row is not PASS: {row.get('language')}")
        require_current_identity(row["source"], row["source"]["path"])
        require_current_identity(row["chapters"], row["chapters"]["path"])

    edition_rows = localized.get("editions", [])
    if len(edition_rows) != 2 or {row.get("language") for row in edition_rows} != {"ja", "zh-cn"}:
        raise RuntimeError("Localized build receipt does not contain exactly both languages")
    total_rendered_pages = 0
    for row in edition_rows:
        if row.get("status") != "PASS":
            raise RuntimeError(f"Localized build row is not PASS: {row.get('language')}")
        require_current_identity(row["source"], row["source"]["path"])
        require_current_identity(row["pdf"], row["pdf"]["path"])
        rendered = row.get("rendered_pages", [])
        if len(rendered) != int(row.get("pages", -1)):
            raise RuntimeError(f"Localized render-page count drift: {row.get('language')}")
        for rendered_row in rendered:
            require_current_identity(rendered_row, rendered_row["path"])
        total_rendered_pages += len(rendered)
    if total_rendered_pages != 40:
        raise RuntimeError("Localized build receipt does not bind exactly 40 rendered pages")

    identities = [local_identity(local, remote) for local, remote in PAYLOAD]
    expected_manifest = {
        row["remote_filename"]: row
        for row in identities
        if row["local_path"] != str(MANIFEST.relative_to(ROOT)).replace("\\", "/")
    }
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required_headers = {"local_path", "remote_filename", "bytes", "md5", "sha256"}
        if reader.fieldnames is None or not required_headers.issubset(reader.fieldnames):
            raise RuntimeError("Publication manifest lacks required identity columns")
        rows = list(reader)
    actual_manifest = {row["remote_filename"]: row for row in rows}
    if len(rows) != len(actual_manifest):
        raise RuntimeError("Publication manifest contains duplicate remote filenames")
    if set(actual_manifest) != set(expected_manifest):
        raise RuntimeError("Publication manifest filename set differs from the local payload")
    for remote, expected in expected_manifest.items():
        row = actual_manifest[remote]
        if (
            row.get("local_path") != expected["local_path"]
            or int(row.get("bytes", -1)) != expected["bytes"]
            or row.get("md5", "").upper() != expected["md5"]
            or row.get("sha256", "").upper() != expected["sha256"]
        ):
            raise RuntimeError(f"Publication manifest identity mismatch: {remote}")
    return identities


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def inventory_rows(inventory: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"remote_filename": name, **row} for name, row in sorted(inventory.items())]


def inventory_from_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    for row in rows:
        name = row.get("remote_filename")
        if not isinstance(name, str) or name in inventory:
            raise RuntimeError("Release state contains an invalid or duplicate inventory filename")
        inventory[name] = {
            "bytes": int(row.get("bytes", -1)),
            "md5": normalize_checksum(str(row.get("md5", ""))),
        }
    return inventory


def expected_new_inventory(identities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        row["remote_filename"]: {"bytes": row["bytes"], "md5": row["md5"]}
        for row in identities
    }


def expected_complete_inventory(
    inherited: dict[str, dict[str, Any]], identities: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    complete = copy.deepcopy(inherited)
    complete.update(expected_new_inventory(identities))
    return complete


def assert_profile_name_absent(metadata: dict[str, Any]) -> None:
    profile_name = Path.home().name.strip()
    if len(profile_name) >= 3 and profile_name.casefold() in json.dumps(
        metadata, ensure_ascii=False, sort_keys=True
    ).casefold():
        raise RuntimeError("Release metadata contains the local profile name, which is forbidden")


def assert_profile_name_absent_from_payload(paths: list[Path]) -> None:
    profile_name = Path.home().name.strip().casefold()
    if len(profile_name) < 3:
        return
    needles = (
        profile_name.encode("utf-8"),
        profile_name.encode("utf-16le"),
        profile_name.encode("utf-16be"),
    )
    for path in paths:
        content = path.read_bytes().lower()
        if any(needle in content for needle in needles):
            raise RuntimeError(
                f"Release payload contains the forbidden local profile name: {path.relative_to(ROOT)}"
            )


def make_target_metadata(original: dict[str, Any]) -> dict[str, Any]:
    target = copy.deepcopy(original)
    target["version"] = NEW_VERSION
    description = str(target.get("description", ""))
    if DESCRIPTION_APPENDIX not in description:
        target["description"] = description.rstrip() + DESCRIPTION_APPENDIX
    changed_keys = sorted(
        key
        for key in set(original) | set(target)
        if original.get(key) != target.get(key)
    )
    if changed_keys != ["description", "version"]:
        raise RuntimeError(f"Unexpected metadata mutation set: {changed_keys}")
    assert_profile_name_absent(target)
    return target


def assert_partial_draft_inventory(
    current: dict[str, dict[str, Any]],
    inherited: dict[str, dict[str, Any]],
    new_inventory: dict[str, dict[str, Any]],
) -> None:
    unexpected = sorted(set(current) - set(inherited) - set(new_inventory))
    if unexpected:
        raise RuntimeError(f"Successor draft contains unexpected files: {unexpected}")
    for name, expected in inherited.items():
        if current.get(name) != expected:
            raise RuntimeError(f"Inherited file drift or absence in draft: {name}")
    for name, actual in current.items():
        if name in new_inventory and actual != new_inventory[name]:
            raise RuntimeError(f"Partially uploaded file identity drift: {name}")


def validate_public_snapshot(
    record: dict[str, Any],
    predecessor: dict[str, Any],
    expected_inventory: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if str(record.get("conceptrecid")) != CONCEPT_ID:
        raise RuntimeError("Published record escaped the intended concept lineage")
    inventory = public_inventory(record)
    if inventory != expected_inventory:
        raise RuntimeError(
            f"Published inventory is not exact: expected {len(expected_inventory)} files; "
            f"found {len(inventory)}"
        )
    old_metadata = predecessor.get("metadata", {})
    metadata = record.get("metadata", {})
    if metadata.get("version") != NEW_VERSION:
        raise RuntimeError("Published version metadata is not the intended R3 version")
    expected_description = str(old_metadata.get("description", "")).rstrip() + DESCRIPTION_APPENDIX
    if metadata.get("description") != expected_description:
        raise RuntimeError("Published description is not the exact predecessor description plus R3 appendix")
    verified_keys: list[str] = []
    for key in PUBLIC_STABLE_METADATA_KEYS:
        if key in old_metadata or key in metadata:
            if old_metadata.get(key) != metadata.get(key):
                raise RuntimeError(f"Published stable metadata drift: {key}")
            verified_keys.append(key)
    assert_profile_name_absent(metadata)
    return inventory, verified_keys


def poll_public_snapshot(
    record_id: int,
    predecessor: dict[str, Any],
    expected_inventory: dict[str, dict[str, Any]],
    *,
    attempts: int = 60,
    delay_seconds: float = 2.0,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    last_error = "record not yet available"
    for attempt in range(attempts):
        try:
            _, record = request_json(f"https://zenodo.org/api/records/{record_id}")
            inventory, verified_keys = validate_public_snapshot(
                record, predecessor, expected_inventory
            )
            return record, inventory, verified_keys
        except RuntimeError as error:
            last_error = str(error)
        if attempt + 1 < attempts:
            time.sleep(delay_seconds)
    raise RuntimeError(f"Published record did not reach the exact expected state: {last_error}")


def anonymous_preflight(
    *, require_latest: bool
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    _, public = request_json(f"https://zenodo.org/api/records/{PREDECESSOR_ID}")
    _, latest = request_json(f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest")
    if str(public.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Configured predecessor record identity drift")
    if require_latest and str(latest.get("id")) != str(PREDECESSOR_ID):
        raise RuntimeError("Configured predecessor is not the latest public version")
    if str(public.get("conceptrecid")) != CONCEPT_ID or str(latest.get("conceptrecid")) != CONCEPT_ID:
        raise RuntimeError("Zenodo concept identity drift")
    assert_profile_name_absent(public.get("metadata", {}))
    inherited = public_inventory(public)
    if len(inherited) != EXPECTED_INHERITED_FILES:
        raise RuntimeError(f"Expected {EXPECTED_INHERITED_FILES} inherited files; found {len(inherited)}")
    collisions = sorted(set(inherited) & {remote for _, remote in PAYLOAD})
    if collisions:
        raise RuntimeError(f"Payload filename collisions: {collisions}")
    return public, inherited, latest


def find_existing_concept_draft(token: str) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {
            "status": "draft",
            "size": 10,
            "q": f"conceptrecid:{CONCEPT_ID}",
        }
    )
    _, rows = request_json(
        f"https://zenodo.org/api/deposit/depositions?{query}", token=token
    )
    if not isinstance(rows, list):
        raise RuntimeError("Zenodo draft search returned a non-list response")
    candidates = [
        row
        for row in rows
        if str(row.get("conceptrecid")) == CONCEPT_ID
        and row.get("submitted") is False
        and row.get("state") != "done"
    ]
    if len(candidates) > 1:
        raise RuntimeError("More than one unpublished draft exists on the concept lineage")
    if not candidates:
        return None
    draft_id = int(candidates[0]["id"])
    _, draft = request_json(
        f"https://zenodo.org/api/deposit/depositions/{draft_id}", token=token
    )
    return draft


def derive_unmutated_draft_metadata(
    current: dict[str, Any], predecessor: dict[str, Any]
) -> dict[str, Any]:
    baseline = copy.deepcopy(current)
    predecessor_description = str(predecessor.get("description", ""))
    target_description = predecessor_description.rstrip() + DESCRIPTION_APPENDIX
    if (
        baseline.get("version") == NEW_VERSION
        and baseline.get("description") == target_description
    ):
        baseline["description"] = predecessor_description
        baseline.pop("version", None)
    changed_from_predecessor = sorted(
        key
        for key in set(predecessor) | set(baseline)
        if predecessor.get(key) != baseline.get(key)
    )
    allowed_clone_changes = {"doi", "prereserve_doi", "version"}
    unexpected_changes = sorted(set(changed_from_predecessor) - allowed_clone_changes)
    if unexpected_changes:
        raise RuntimeError(
            f"Untracked successor draft has unexpected metadata changes: {unexpected_changes}"
        )
    target = make_target_metadata(baseline)
    if current not in (baseline, target):
        raise RuntimeError("Untracked successor metadata is neither the clone baseline nor R3 target")
    return baseline


def create_release_state(
    token: str,
    identities: list[dict[str, Any]],
    inherited: dict[str, dict[str, Any]],
    predecessor: dict[str, Any],
) -> dict[str, Any]:
    _, predecessor_deposition = request_json(
        f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}", token=token
    )
    if predecessor_deposition.get("submitted") is not True:
        raise RuntimeError("Configured predecessor deposition is not published")
    if predecessor_deposition.get("metadata", {}).get("description") != predecessor.get(
        "metadata", {}
    ).get("description"):
        raise RuntimeError("Authenticated and anonymous predecessor metadata disagree")

    draft = find_existing_concept_draft(token)
    draft_origin = "adopted_existing"
    if draft is None:
        _, created = request_json(
            f"https://zenodo.org/api/deposit/depositions/{PREDECESSOR_ID}/actions/newversion",
            method="POST",
            token=token,
            expected=(201,),
        )
        latest_draft_url = created.get("links", {}).get("latest_draft")
        if latest_draft_url:
            _, candidate = request_json(latest_draft_url, token=token)
            if candidate.get("submitted") is False and candidate.get("state") != "done":
                draft = candidate
        if draft is None:
            for _ in range(10):
                draft = find_existing_concept_draft(token)
                if draft is not None:
                    break
                time.sleep(1.0)
        if draft is None:
            raise RuntimeError("New-version action did not expose an unpublished successor draft")
        draft_origin = "created_now"

    if str(draft.get("conceptrecid")) != CONCEPT_ID:
        raise RuntimeError("Successor draft escaped the configured concept lineage")
    current_metadata = copy.deepcopy(draft.get("metadata", {}))
    original_metadata = derive_unmutated_draft_metadata(
        current_metadata, predecessor_deposition.get("metadata", {})
    )
    assert_profile_name_absent(original_metadata)
    target_metadata = make_target_metadata(original_metadata)
    links = draft.get("links", {})
    action_links = {
        "self_url": links.get("self"),
        "bucket_url": links.get("bucket"),
        "publish_url": links.get("publish"),
    }
    if not all(isinstance(value, str) and value for value in action_links.values()):
        raise RuntimeError("Successor draft is missing required action links")
    for url in action_links.values():
        validate_zenodo_url(url, require_api=True)
    state = {
        "schema": "gaga-stacks-r3-zenodo-state-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "draft",
        "stage": "draft_initialized",
        "predecessor_id": PREDECESSOR_ID,
        "concept_record_id": int(CONCEPT_ID),
        "draft": {
            "record_id": int(draft["id"]),
            "origin": draft_origin,
            **action_links,
        },
        "payload": identities,
        "inherited_inventory": inventory_rows(inherited),
        "original_metadata": original_metadata,
        "target_metadata": target_metadata,
        "metadata_changed_keys": ["description", "version"],
        "observed_draft_files": len(draft.get("files", [])),
    }
    write_json_atomic(STATE, state)
    try:
        if int(draft["id"]) == PREDECESSOR_ID:
            raise RuntimeError("New-version action resolved to the published predecessor")
        if draft.get("submitted") is not False or draft.get("state") == "done":
            raise RuntimeError("Successor draft is not in an unpublished mutable state")
        current_inventory = draft_inventory(draft)
        assert_partial_draft_inventory(
            current_inventory, inherited, expected_new_inventory(identities)
        )
        if current_metadata not in (original_metadata, target_metadata):
            raise RuntimeError("Successor draft metadata is not an accepted frozen variant")
    except RuntimeError as error:
        update_release_state(
            state,
            status="draft",
            stage="draft_validation_failed",
            validation_error=str(error),
        )
        raise
    state = update_release_state(
        state,
        status="draft",
        stage="draft_adopted_and_validated",
    )
    return state


def load_release_state(
    identities: list[dict[str, Any]], inherited: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    if not STATE.is_file():
        return None
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if state.get("schema") != "gaga-stacks-r3-zenodo-state-v1":
        raise RuntimeError("Release state schema mismatch")
    if state.get("status") not in {"draft", "published", "verified"}:
        raise RuntimeError("Release state has an invalid status")
    if state.get("stage") == "draft_validation_failed":
        raise RuntimeError(
            "Persisted successor-draft validation failed: "
            f"{state.get('validation_error', 'unspecified failure')}"
        )
    if int(state.get("predecessor_id", -1)) != PREDECESSOR_ID:
        raise RuntimeError("Release state predecessor mismatch")
    if int(state.get("concept_record_id", -1)) != int(CONCEPT_ID):
        raise RuntimeError("Release state concept mismatch")
    if state.get("payload") != identities:
        raise RuntimeError("Current local payload differs from the frozen release state")
    if inventory_from_rows(state.get("inherited_inventory", [])) != inherited:
        raise RuntimeError("Current predecessor inventory differs from the frozen release state")
    original_metadata = state.get("original_metadata")
    target_metadata = state.get("target_metadata")
    if not isinstance(original_metadata, dict) or not isinstance(target_metadata, dict):
        raise RuntimeError("Release state metadata is malformed")
    if make_target_metadata(original_metadata) != target_metadata:
        raise RuntimeError("Release state target metadata is not deterministic")
    draft = state.get("draft", {})
    if not isinstance(draft.get("record_id"), int):
        raise RuntimeError("Release state draft identity is malformed")
    for key in ("self_url", "bucket_url", "publish_url"):
        url = draft.get(key)
        if not isinstance(url, str):
            raise RuntimeError(f"Release state lacks the draft action URL: {key}")
        validate_zenodo_url(url, require_api=True)
    published_id = state.get("published_record_id")
    if state["status"] in {"published", "verified"} and not isinstance(published_id, int):
        raise RuntimeError("Published release state lacks a record ID")
    return state


def update_release_state(state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    updated.update(changes)
    updated["updated_utc"] = datetime.now(timezone.utc).isoformat()
    write_json_atomic(STATE, updated)
    return updated


def verify_public_record(
    record_id: int,
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    *,
    transfer_actions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    complete_inventory = expected_complete_inventory(inherited, identities)
    record, final_inventory, verified_keys = poll_public_snapshot(
        record_id, predecessor, complete_inventory
    )
    _, latest = request_json(f"https://zenodo.org/api/records/{record_id}/versions/latest")
    if str(latest.get("id")) != str(record_id):
        raise RuntimeError("Verified record is not the latest concept version")
    public_files: dict[str, dict[str, Any]] = {}
    for row in record.get("files", []):
        key = row["key"]
        if key in public_files:
            raise RuntimeError(f"Duplicate public filename during byte readback: {key}")
        public_files[key] = row
    readbacks: list[dict[str, Any]] = []
    for expected in identities:
        remote = expected["remote_filename"]
        file_row = public_files.get(remote)
        if file_row is None:
            raise RuntimeError(f"Published payload file is absent: {remote}")
        download_url = file_row.get("links", {}).get("self") or file_row.get("links", {}).get("download")
        if not download_url:
            raise RuntimeError(f"Public file lacks an anonymous download URL: {remote}")
        byte_count = -1
        sha = ""
        for attempt in range(4):
            byte_count, sha = download_sha256(download_url)
            if byte_count == expected["bytes"] and sha == expected["sha256"]:
                break
            if attempt < 3:
                time.sleep(1.0)
        if byte_count != expected["bytes"] or sha != expected["sha256"]:
            raise RuntimeError(f"Anonymous public-byte mismatch: {remote}")
        readbacks.append(
            {
                "remote_filename": remote,
                "bytes": byte_count,
                "sha256": sha,
                "status": "PASS",
            }
        )
    if transfer_actions is None:
        transfer_actions = [
            {
                "remote_filename": row["remote_filename"],
                "action": "verification_only",
            }
            for row in identities
        ]
    return {
        "schema": "gaga-stacks-r3-zenodo-publication-receipt-v2",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "predecessor": {
            "record_id": PREDECESSOR_ID,
            "doi": predecessor.get("doi"),
            "inherited_files": EXPECTED_INHERITED_FILES,
        },
        "published": {
            "record_id": int(record_id),
            "doi": record.get("doi"),
            "concept_record_id": int(CONCEPT_ID),
            "concept_doi": record.get("conceptdoi"),
            "version": record.get("metadata", {}).get("version"),
            "files": len(final_inventory),
        },
        "metadata": {
            "changed_keys": ["description", "version"],
            "stable_keys_verified": verified_keys,
            "description_appendix_exact": True,
        },
        "inherited_inventory": inventory_rows(inherited),
        "release_inventory": identities,
        "transfer_actions": transfer_actions,
        "anonymous_public_readback": readbacks,
    }


def finalize_verified_release(
    receipt: dict[str, Any], state: dict[str, Any] | None
) -> dict[str, Any]:
    write_json_atomic(RECEIPT, receipt)
    if state is not None:
        state = update_release_state(
            state,
            status="verified",
            stage="anonymous_readback_complete",
            published_record_id=int(receipt["published"]["record_id"]),
            receipt={
                "path": str(RECEIPT.relative_to(ROOT)).replace("\\", "/"),
                "bytes": RECEIPT.stat().st_size,
                "sha256": digest(RECEIPT, "sha256"),
            },
        )
    return receipt


def recover_published_successor(
    state: dict[str, Any],
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    *,
    wait_for_change: bool,
) -> tuple[dict[str, Any], int] | None:
    attempts = 45 if wait_for_change else 1
    complete_inventory = expected_complete_inventory(inherited, identities)
    for attempt in range(attempts):
        _, latest = request_json(
            f"https://zenodo.org/api/records/{PREDECESSOR_ID}/versions/latest"
        )
        if str(latest.get("conceptrecid")) != CONCEPT_ID:
            raise RuntimeError("Concept latest pointer escaped the configured lineage")
        latest_id = int(latest["id"])
        if latest_id != PREDECESSOR_ID:
            poll_public_snapshot(latest_id, predecessor, complete_inventory)
            state = update_release_state(
                state,
                status="published",
                stage="published_record_recovered",
                published_record_id=latest_id,
            )
            return state, latest_id
        if attempt + 1 < attempts:
            time.sleep(2.0)
    return None


def execute_release(
    identities: list[dict[str, Any]],
    predecessor: dict[str, Any],
    inherited: dict[str, dict[str, Any]],
    state: dict[str, Any] | None,
) -> dict[str, Any]:
    if state is not None and state["status"] in {"published", "verified"}:
        receipt = verify_public_record(
            int(state["published_record_id"]),
            identities,
            predecessor,
            inherited,
            transfer_actions=state.get("transfer_actions"),
        )
        return finalize_verified_release(receipt, state)

    if state is not None:
        recovered = recover_published_successor(
            state,
            identities,
            predecessor,
            inherited,
            wait_for_change=False,
        )
        if recovered is not None:
            state, record_id = recovered
            receipt = verify_public_record(
                record_id,
                identities,
                predecessor,
                inherited,
                transfer_actions=state.get("transfer_actions"),
            )
            return finalize_verified_release(receipt, state)

    token = load_token()
    if state is None:
        state = create_release_state(token, identities, inherited, predecessor)

    draft_links = state["draft"]
    try:
        _, draft = request_json(draft_links["self_url"], token=token)
    except RuntimeError:
        recovered = recover_published_successor(
            state,
            identities,
            predecessor,
            inherited,
            wait_for_change=True,
        )
        if recovered is None:
            raise RuntimeError(
                "Stored successor draft is unavailable and no exact published successor appeared"
            )
        state, record_id = recovered
        receipt = verify_public_record(
            record_id,
            identities,
            predecessor,
            inherited,
            transfer_actions=state.get("transfer_actions"),
        )
        return finalize_verified_release(receipt, state)

    new_inventory = expected_new_inventory(identities)
    current_inventory = draft_inventory(draft)
    assert_partial_draft_inventory(current_inventory, inherited, new_inventory)
    current_metadata = draft.get("metadata", {})
    if current_metadata == state["original_metadata"]:
        request_json(
            draft_links["self_url"],
            method="PUT",
            token=token,
            payload={"metadata": state["target_metadata"]},
            expected=(200,),
        )
        _, draft = request_json(draft_links["self_url"], token=token)
        current_metadata = draft.get("metadata", {})
    elif current_metadata != state["target_metadata"]:
        raise RuntimeError("Successor draft metadata is neither the frozen original nor target")
    if current_metadata != state["target_metadata"]:
        _, draft = request_json(draft_links["self_url"], token=token)
        if draft.get("metadata", {}) != state["target_metadata"]:
            raise RuntimeError("Draft metadata write/readback mismatch")

    local_by_remote = {row["remote_filename"]: row for row in identities}
    transfer_actions: list[dict[str, Any]] = []
    current_inventory = draft_inventory(draft)
    assert_partial_draft_inventory(current_inventory, inherited, new_inventory)
    for local, remote in PAYLOAD:
        expected = local_by_remote[remote]
        if remote in current_inventory:
            action = "already_present"
        else:
            response = upload_file(draft_links["bucket_url"], ROOT / local, remote, token)
            returned_size = int(response.get("size", response.get("filesize", -1)))
            returned_md5 = normalize_checksum(response.get("checksum", ""))
            if returned_size != expected["bytes"] or returned_md5 != expected["md5"]:
                raise RuntimeError(f"Upload identity mismatch: {remote}")
            current_inventory[remote] = {
                "bytes": returned_size,
                "md5": returned_md5,
            }
            action = "uploaded"
        transfer_actions.append({"remote_filename": remote, "action": action})

    _, draft = request_json(draft_links["self_url"], token=token)
    complete_inventory = draft_inventory(draft)
    expected_inventory = expected_complete_inventory(inherited, identities)
    if complete_inventory != expected_inventory:
        raise RuntimeError("Completed draft inventory is not the exact 94-file release inventory")
    if draft.get("metadata", {}) != state["target_metadata"]:
        raise RuntimeError("Completed draft metadata differs from the frozen target metadata")
    state = update_release_state(
        state,
        status="draft",
        stage="publish_pending",
        transfer_actions=transfer_actions,
    )

    recovered = recover_published_successor(
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
            _, published = request_json(
                draft_links["publish_url"],
                method="POST",
                token=token,
                expected=(202,),
            )
            raw_record_id = published.get("record_id") or published.get("id")
            if raw_record_id is None:
                raise RuntimeError("Publish response did not provide the new record ID")
            record_id = int(raw_record_id)
            state = update_release_state(
                state,
                status="published",
                stage="publish_response_persisted",
                published_record_id=record_id,
            )
        except RuntimeError:
            recovered = recover_published_successor(
                state,
                identities,
                predecessor,
                inherited,
                wait_for_change=True,
            )
            if recovered is None:
                raise
            state, record_id = recovered

    receipt = verify_public_record(
        record_id,
        identities,
        predecessor,
        inherited,
        transfer_actions=state.get("transfer_actions"),
    )
    return finalize_verified_release(receipt, state)


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--execute",
        action="store_true",
        help="Create or resume, upload, publish, and anonymously verify the successor version.",
    )
    action.add_argument(
        "--verify-record-id",
        type=int,
        metavar="ID",
        help="Anonymously verify an already-published successor and repair its receipt.",
    )
    args = parser.parse_args()
    identities = validate_local_payload()
    public, inherited, latest = anonymous_preflight(
        require_latest=not STATE.is_file() and args.verify_record_id is None
    )
    state = load_release_state(identities, inherited)

    if args.verify_record_id is not None:
        if state is not None and state.get("published_record_id") not in {
            None,
            args.verify_record_id,
        }:
            raise RuntimeError("Requested verification record conflicts with release state")
        receipt = verify_public_record(
            args.verify_record_id,
            identities,
            public,
            inherited,
            transfer_actions=state.get("transfer_actions") if state else None,
        )
        if state is not None:
            state = update_release_state(
                state,
                status="published",
                stage="verification_record_bound",
                published_record_id=args.verify_record_id,
            )
        receipt = finalize_verified_release(receipt, state)
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0

    preflight = {
        "status": "PASS",
        "predecessor_id": PREDECESSOR_ID,
        "latest_public_id": int(latest["id"]),
        "concept_id": int(CONCEPT_ID),
        "inherited_files": len(inherited),
        "new_files": len(PAYLOAD),
        "total_files": len(inherited) + len(PAYLOAD),
        "release_state": state.get("status") if state else "not_started",
        "payload": identities,
    }
    if not args.execute:
        print(json.dumps(preflight, ensure_ascii=False, indent=2))
        return 0

    receipt = execute_release(identities, public, inherited, state)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
