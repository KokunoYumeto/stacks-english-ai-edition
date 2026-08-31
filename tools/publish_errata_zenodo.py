#!/usr/bin/env python3
"""Publish a six-file errata checkpoint into an existing Zenodo lineage.

The transaction is deliberately fail-closed and resumable.  Without
``--execute`` it validates the frozen local package and anonymously proves that
the named predecessor is the latest public version.  Only ``--execute`` reads
the credential.  The successor preserves every noncolliding predecessor file,
replaces README.md, RELEASE.json, and SHA256SUMS.txt, uploads the three new
versioned archives, publishes open access, and anonymously re-reads every final
byte.  State and receipts never contain credentials or local paths.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterator, Mapping, Sequence


TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
PROJECT_URL = "https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts"
# The repository was renamed in place; frozen packages retain the former URL.
PROJECT_URL_ALIASES = frozenset(
    {
        PROJECT_URL,
        "https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project",
    }
)
PACKAGE_SCHEMA = "unofficial-ai-integrated-stacks-preservation-package/v2"
STATE_SCHEMA = "unofficial-ai-integrated-stacks-errata-zenodo-state/v1"
RECEIPT_SCHEMA = "unofficial-ai-integrated-stacks-errata-zenodo-receipt/v1"
PREFLIGHT_SCHEMA = "unofficial-ai-integrated-stacks-errata-zenodo-preflight/v1"
REPLACED_DOCUMENTS = frozenset({"README.md", "RELEASE.json", "SHA256SUMS.txt"})
STABLE_METADATA_KEYS = (
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
MUTATED_METADATA_KEYS = frozenset({"access_right", "description", "title", "version"})
VOLATILE_DRAFT_METADATA_KEYS = frozenset({"doi", "prereserve_doi"})
SAFE_VERSION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+() -]{0,127}")
HEX40_RE = re.compile(r"[0-9a-fA-F]{40}")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest().upper()


def canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest().upper()


def normalize_checksum(value: str) -> str:
    return value.split(":", 1)[-1].upper()


def canonical_license_id(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip().casefold()
    if isinstance(value, Mapping):
        identifier = value.get("id")
        if isinstance(identifier, str) and identifier.strip():
            return identifier.strip().casefold()
    raise RuntimeError("Zenodo license metadata lacks a canonical identifier")


def safe_remote_name(value: Any) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."}:
        raise RuntimeError("A release file has an invalid filename")
    if (
        "/" in value
        or "\\" in value
        or "\x00" in value
        or re.match(r"^[A-Za-z]:", value)
    ):
        raise RuntimeError("A release filename is path-shaped")
    return value


def assert_sanitized(value: Any) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    profile_name = Path.home().name.strip()
    if len(profile_name) >= 3 and profile_name.casefold() in serialized.casefold():
        raise RuntimeError("Sanitized publication data contains the local profile name")
    if re.search(
        r"(?i)(?:(?<![A-Za-z0-9])[a-z]:[\\/]"
        r"|(?:^|[\s\"'(\[])/(?:home|users)/)",
        serialized,
    ):
        raise RuntimeError("Sanitized publication data contains a local absolute path")
    if re.search(r"(?i)(access[_ -]?token|authorization\s*[:=]|bearer\s+)", serialized):
        raise RuntimeError("Sanitized publication data contains credential-shaped text")


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    assert_sanitized(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def zip_listing(path: Path) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = archive.infolist()
            if not infos:
                raise RuntimeError(f"ZIP is empty: {path.name}")
            names: set[str] = set()
            rows: list[dict[str, Any]] = []
            for info in infos:
                name = info.filename
                pure = PurePosixPath(name)
                if (
                    not name
                    or name in names
                    or "\\" in name
                    or pure.is_absolute()
                    or any(part in {"", ".", ".."} for part in pure.parts)
                    or (pure.parts and re.match(r"^[A-Za-z]:", pure.parts[0]))
                ):
                    raise RuntimeError(f"ZIP has an unsafe or duplicate member: {path.name}")
                if info.flag_bits & 0x1:
                    raise RuntimeError(f"ZIP contains an encrypted member: {path.name}")
                names.add(name)
                rows.append(
                    {
                        "name": name,
                        "bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                        "crc32": f"{info.CRC:08X}",
                        "directory": info.is_dir(),
                    }
                )
            bad = archive.testzip()
            if bad is not None:
                raise RuntimeError(f"ZIP integrity test failed at {bad!r}: {path.name}")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        raise RuntimeError(f"ZIP could not be reopened: {path.name}") from error
    return {
        "status": "PASS",
        "entry_count": len(rows),
        "file_count": sum(not row["directory"] for row in rows),
        "member_tuple_set_sha256": canonical_json_sha256(rows),
    }


def local_identity(path: Path) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "remote_filename": safe_remote_name(path.name),
        "bytes": path.stat().st_size,
        "md5": digest(path, "md5"),
        "sha256": digest(path, "sha256"),
    }
    if path.suffix.casefold() == ".zip":
        identity["zip"] = zip_listing(path)
    return identity


def parse_sha256sums(asset_dir: Path, identities: Mapping[str, dict[str, Any]]) -> None:
    rows: dict[str, str] = {}
    try:
        lines = (asset_dir / "SHA256SUMS.txt").read_text(encoding="ascii").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise RuntimeError("SHA256SUMS.txt is not readable strict ASCII") from error
    for line in lines:
        match = re.fullmatch(r"([0-9A-Fa-f]{64})  ([^/\\]+)", line)
        if match is None:
            raise RuntimeError("SHA256SUMS.txt contains a malformed row")
        sha256, name = match.groups()
        safe_remote_name(name)
        if name in rows:
            raise RuntimeError("SHA256SUMS.txt contains a duplicate filename")
        rows[name] = sha256.upper()
    expected = set(identities) - {"SHA256SUMS.txt"}
    if set(rows) != expected:
        raise RuntimeError("SHA256SUMS.txt does not bind exactly the other five files")
    for name, sha256 in rows.items():
        if identities[name]["sha256"] != sha256:
            raise RuntimeError(f"SHA256SUMS.txt identity mismatch for {name}")


def parse_release_manifest(
    asset_dir: Path,
    identities: Mapping[str, dict[str, Any]],
    concept_record_id: int,
) -> dict[str, Any]:
    try:
        value = json.loads((asset_dir / "RELEASE.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("RELEASE.json is not valid UTF-8 JSON") from error
    if not isinstance(value, dict) or value.get("schema") != PACKAGE_SCHEMA:
        raise RuntimeError("RELEASE.json is not the generic errata package schema")
    title = value.get("title")
    release_id = value.get("release")
    if not isinstance(title, str) or not title.strip() or not isinstance(release_id, str):
        raise RuntimeError("RELEASE.json lacks its title or release identity")
    if value.get("validation", {}).get("status") != "PASS":
        raise RuntimeError("RELEASE.json does not bind a passing validation state")
    source = value.get("source", {})
    if (
        source.get("repository") not in PROJECT_URL_ALIASES
        or not isinstance(source.get("commit"), str)
        or HEX40_RE.fullmatch(source["commit"]) is None
        or not isinstance(source.get("tree"), str)
        or HEX40_RE.fullmatch(source["tree"]) is None
    ):
        raise RuntimeError("RELEASE.json source binding is malformed")
    preservation = value.get("preservation", {})
    concept_doi = f"10.5281/zenodo.{concept_record_id}"
    if preservation.get("zenodo_concept_doi") != concept_doi:
        raise RuntimeError("RELEASE.json targets a different Zenodo concept DOI")
    if not isinstance(preservation.get("license"), str):
        raise RuntimeError("RELEASE.json lacks its license identity")
    manifest_rows = value.get("assets")
    if not isinstance(manifest_rows, list):
        raise RuntimeError("RELEASE.json assets are malformed")
    manifest: dict[str, tuple[int, str]] = {}
    for row in manifest_rows:
        if not isinstance(row, dict):
            raise RuntimeError("RELEASE.json contains a malformed asset row")
        name = safe_remote_name(row.get("name"))
        if name in manifest:
            raise RuntimeError("RELEASE.json contains a duplicate asset row")
        manifest[name] = (int(row.get("bytes", -1)), str(row.get("sha256", "")).upper())
    expected_manifest_names = {"README.md"} | {
        name for name in identities if name.casefold().endswith(".zip")
    }
    if set(manifest) != expected_manifest_names:
        raise RuntimeError("RELEASE.json does not bind README plus the three ZIPs")
    for name, declared in manifest.items():
        actual = identities[name]
        if declared != (actual["bytes"], actual["sha256"]):
            raise RuntimeError(f"RELEASE.json identity mismatch for {name}")
    archives = value.get("archives")
    if not isinstance(archives, dict) or set(archives) != {"source", "pdfs", "validation"}:
        raise RuntimeError("RELEASE.json archive inventory is malformed")
    archive_names = {row.get("name") for row in archives.values() if isinstance(row, dict)}
    if archive_names != {name for name in identities if name.casefold().endswith(".zip")}:
        raise RuntimeError("RELEASE.json archive names differ from the three ZIPs")
    assert_sanitized(value)
    return value


def validate_local_assets(
    asset_dir: Path, concept_record_id: int
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if asset_dir.is_symlink() or not asset_dir.is_dir():
        raise RuntimeError("The asset directory does not exist or is a symlink")
    children = list(asset_dir.iterdir())
    if any(child.is_symlink() or not child.is_file() for child in children):
        raise RuntimeError("The asset directory must contain ordinary files only")
    names = {safe_remote_name(child.name) for child in children}
    zip_names = {name for name in names if name.casefold().endswith(".zip")}
    if len(children) != 6 or names != REPLACED_DOCUMENTS | zip_names or len(zip_names) != 3:
        raise RuntimeError("The release must be exactly three documents and three ZIPs")
    identities = {child.name: local_identity(child) for child in children}
    parse_sha256sums(asset_dir, identities)
    release = parse_release_manifest(asset_dir, identities, concept_record_id)
    return [identities[name] for name in sorted(identities)], release


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
            newurl, authenticated=req.get_header("Authorization") is not None
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
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with ZENODO_OPENER.open(request, timeout=timeout) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        raw_error = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Zenodo request failed with HTTP {error.code}: {raw_error[:1600]}"
        ) from error
    if status not in expected:
        raise RuntimeError(f"Unexpected Zenodo HTTP status {status}")
    if not raw:
        return status, None
    try:
        return status, json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError("Zenodo returned malformed JSON") from error


def request_no_content(url: str, *, method: str, token: str) -> None:
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
        raw_error = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Zenodo draft mutation failed with HTTP {error.code}: {raw_error[:1600]}"
        ) from error
    if status != 204:
        raise RuntimeError(f"Unexpected Zenodo deletion status {status}")


@contextmanager
def downloaded_file(
    url: str, *, token: str | None = None
) -> Iterator[tuple[Path, int, str, str]]:
    validate_zenodo_url(url, authenticated=token is not None)
    headers: dict[str, str] = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    descriptor, temporary_name = tempfile.mkstemp(prefix="stacks-zenodo-readback-")
    os.close(descriptor)
    temporary = Path(temporary_name)
    total = 0
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    try:
        try:
            with ZENODO_OPENER.open(request, timeout=900) as response, temporary.open(
                "wb"
            ) as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output.write(chunk)
                    total += len(chunk)
                    sha256.update(chunk)
                    md5.update(chunk)
        except urllib.error.HTTPError as error:
            raise RuntimeError(
                f"Zenodo file readback failed with HTTP {error.code}"
            ) from error
        yield temporary, total, sha256.hexdigest().upper(), md5.hexdigest().upper()
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def upload_file(bucket_url: str, path: Path, name: str, token: str) -> dict[str, Any]:
    url = bucket_url.rstrip("/") + "/" + urllib.parse.quote(name, safe="")
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
        with ZENODO_OPENER.open(request, timeout=1200) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        raw_error = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Upload failed for {name} with HTTP {error.code}: {raw_error[:1600]}"
        ) from error
    if status < 200 or status >= 300:
        raise RuntimeError(f"Upload failed for {name} with HTTP {status}")
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Upload returned malformed JSON for {name}") from error


def load_token() -> str:
    text = TOKEN_FILE.read_text(encoding="utf-8")
    candidates = list(
        dict.fromkeys(
            re.findall(
                r"(?<![A-Za-z0-9._-])([A-Za-z0-9][A-Za-z0-9._-]{39,})"
                r"(?![A-Za-z0-9._-])",
                text,
            )
        )
    )
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly one token-shaped credential; found {len(candidates)}"
        )
    return candidates[0]


def public_row_identity(row: Mapping[str, Any]) -> tuple[str, int, str, str]:
    name = safe_remote_name(row.get("key"))
    size = int(row.get("size", -1))
    md5 = normalize_checksum(str(row.get("checksum", "")))
    links = row.get("links", {})
    url = links.get("self") or links.get("download") if isinstance(links, Mapping) else None
    if size < 0 or re.fullmatch(r"[0-9A-F]{32}", md5) is None:
        raise RuntimeError(f"Public file identity is malformed: {name}")
    if not isinstance(url, str) or not url:
        raise RuntimeError(f"Public file lacks a download URL: {name}")
    validate_zenodo_url(url)
    return name, size, md5, url


def public_inventory(record: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = record.get("files")
    if not isinstance(rows, list):
        raise RuntimeError("Public record has a malformed file inventory")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise RuntimeError("Public record has a malformed file row")
        name, size, md5, url = public_row_identity(row)
        if name in result:
            raise RuntimeError("Public record has a duplicate filename")
        result[name] = {"bytes": size, "md5": md5, "download_url": url}
    return result


def draft_row_identity(row: Mapping[str, Any]) -> tuple[str, int, str]:
    name = safe_remote_name(row.get("filename") or row.get("key"))
    size = int(row.get("filesize", row.get("size", -1)))
    md5 = normalize_checksum(str(row.get("checksum", "")))
    if size < 0 or re.fullmatch(r"[0-9A-F]{32}", md5) is None:
        raise RuntimeError(f"Draft file identity is malformed: {name}")
    return name, size, md5


def draft_download_url(row: Mapping[str, Any]) -> str:
    links = row.get("links", {})
    url = links.get("download") or links.get("self") if isinstance(links, Mapping) else None
    if not isinstance(url, str) or not url:
        raise RuntimeError("Draft file lacks an authenticated readback URL")
    validate_zenodo_url(url, authenticated=True)
    return url


def validate_lineage_record(
    record: Mapping[str, Any], concept_record_id: int, expected_id: int | None = None
) -> None:
    if expected_id is not None and int(record.get("id", -1)) != expected_id:
        raise RuntimeError("Zenodo record identity drift")
    if str(record.get("conceptrecid")) != str(concept_record_id):
        raise RuntimeError("Zenodo record escaped the intended concept lineage")
    concept_doi = record.get("conceptdoi") or (
        record.get("metadata", {}).get("conceptdoi")
        if isinstance(record.get("metadata"), Mapping)
        else None
    )
    expected_doi = f"10.5281/zenodo.{concept_record_id}"
    if concept_doi not in (None, expected_doi):
        raise RuntimeError("Zenodo concept DOI drift")


def anonymous_preflight(
    predecessor_id: int,
    concept_record_id: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _, predecessor = request_json(f"https://zenodo.org/api/records/{predecessor_id}")
    _, latest = request_json(
        f"https://zenodo.org/api/records/{predecessor_id}/versions/latest"
    )
    if not isinstance(predecessor, dict) or not isinstance(latest, dict):
        raise RuntimeError("Zenodo record response is malformed")
    validate_lineage_record(predecessor, concept_record_id, predecessor_id)
    validate_lineage_record(latest, concept_record_id)
    metadata = predecessor.get("metadata", {})
    if not isinstance(metadata, dict):
        raise RuntimeError("Predecessor metadata is malformed")
    if not isinstance(metadata.get("creators"), list) or not metadata["creators"]:
        raise RuntimeError("Predecessor creators are absent")
    canonical_license_id(metadata.get("license"))
    if metadata.get("access_right") != "open":
        raise RuntimeError("Predecessor is not open access")
    assert_sanitized(metadata)
    public_inventory(predecessor)
    return predecessor, latest


def target_description(release: Mapping[str, Any]) -> str:
    title = html.escape(str(release["title"]))
    scope = html.escape(str(release.get("scope_note", "Validated errata checkpoint.")))
    return (
        f"<p>This source-reproducible successor records {title}.</p>"
        f"<p>{scope}</p>"
        "<p>This is independent, unofficial work. No Stacks Project affiliation, "
        "review, approval, or endorsement is claimed.</p>"
    )


def target_public_metadata(
    predecessor: Mapping[str, Any], release: Mapping[str, Any], version: str
) -> dict[str, Any]:
    metadata = predecessor.get("metadata", {})
    return {
        "title": release["title"],
        "version": version,
        "access_right": "open",
        "description": target_description(release),
        "creators": copy.deepcopy(metadata.get("creators")),
        "license": copy.deepcopy(metadata.get("license")),
    }


def make_target_draft_metadata(
    current: dict[str, Any],
    authenticated_predecessor: Mapping[str, Any],
    release: Mapping[str, Any],
    version: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    predecessor_metadata = authenticated_predecessor.get("metadata", {})
    if not isinstance(predecessor_metadata, dict):
        raise RuntimeError("Authenticated predecessor metadata is malformed")
    if current.get("creators") != predecessor_metadata.get("creators"):
        raise RuntimeError("Successor draft creators differ from the predecessor")
    if canonical_license_id(current.get("license")) != canonical_license_id(
        predecessor_metadata.get("license")
    ):
        raise RuntimeError("Successor draft license differs from the predecessor")
    desired = {
        "title": release["title"],
        "version": version,
        "access_right": "open",
        "description": target_description(release),
    }
    states: list[str] = []
    for key, target in desired.items():
        current_value = current.get(key)
        predecessor_value = predecessor_metadata.get(key)
        if target == predecessor_value:
            if current_value != target:
                raise RuntimeError(f"Successor draft has an unexpected {key}")
        elif current_value == target:
            states.append("target")
        elif current_value == predecessor_value or (key == "version" and current_value in (None, "")):
            states.append("baseline")
        else:
            raise RuntimeError(f"Successor draft has an unexpected {key}")
    if states and len(set(states)) != 1:
        raise RuntimeError("Successor draft metadata is partially mutated")
    excluded = MUTATED_METADATA_KEYS | VOLATILE_DRAFT_METADATA_KEYS
    for key in set(current) | set(predecessor_metadata):
        if key not in excluded and current.get(key) != predecessor_metadata.get(key):
            raise RuntimeError(f"Successor draft has unexpected metadata drift: {key}")
    baseline = copy.deepcopy(current)
    if states and states[0] == "target":
        for key in MUTATED_METADATA_KEYS:
            if key in predecessor_metadata:
                baseline[key] = copy.deepcopy(predecessor_metadata[key])
            else:
                baseline.pop(key, None)
    target = copy.deepcopy(baseline)
    target.update(desired)
    assert_sanitized(target)
    if current not in (baseline, target):
        raise RuntimeError("Draft metadata is neither baseline nor exact target")
    return baseline, target


def collect_inherited_assets(
    predecessor: Mapping[str, Any], local_assets: Sequence[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    local = {row["remote_filename"]: row for row in local_assets}
    predecessor_inventory = public_inventory(predecessor)
    inherited: list[dict[str, Any]] = []
    collisions: list[dict[str, Any]] = []
    for name in sorted(predecessor_inventory):
        weak = predecessor_inventory[name]
        if name in REPLACED_DOCUMENTS:
            collisions.append({"remote_filename": name, "disposition": "replace_document"})
            continue
        with downloaded_file(weak["download_url"]) as (path, size, sha256, md5):
            if size != weak["bytes"] or md5 != weak["md5"]:
                raise RuntimeError(f"Predecessor anonymous identity mismatch for {name}")
            strong: dict[str, Any] = {
                "remote_filename": name,
                "bytes": size,
                "md5": md5,
                "sha256": sha256,
            }
            if name.casefold().endswith(".zip"):
                strong["zip"] = zip_listing(path)
        if name in local:
            if strong != local[name]:
                raise RuntimeError(
                    f"A non-document local filename collides with different predecessor bytes: {name}"
                )
            collisions.append(
                {"remote_filename": name, "disposition": "retain_identical_local_collision"}
            )
        else:
            inherited.append(strong)
    return inherited, collisions


def expected_final_inventory(
    local_assets: Sequence[dict[str, Any]], inherited_assets: Sequence[dict[str, Any]]
) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for origin, rows in (("inherited", inherited_assets), ("local", local_assets)):
        for row in rows:
            name = row["remote_filename"]
            if name in result:
                raise RuntimeError(f"Final inventory has a duplicate filename: {name}")
            result[name] = {**copy.deepcopy(row), "origin": origin}
    return [result[name] for name in sorted(result)]


def public_weak_map(rows: Sequence[dict[str, Any]]) -> dict[str, tuple[int, str]]:
    return {row["remote_filename"]: (row["bytes"], row["md5"]) for row in rows}


def find_existing_concept_draft(token: str, concept_record_id: int) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {"status": "draft", "size": 100, "q": f"conceptrecid:{concept_record_id}"}
    )
    _, rows = request_json(
        f"https://zenodo.org/api/deposit/depositions?{query}", token=token
    )
    if not isinstance(rows, list):
        raise RuntimeError("Zenodo draft search returned malformed data")
    candidates = [
        row
        for row in rows
        if str(row.get("conceptrecid")) == str(concept_record_id)
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
    if not isinstance(draft, dict):
        raise RuntimeError("Zenodo returned a malformed draft")
    return draft


def validated_draft_links(
    draft: Mapping[str, Any], predecessor_id: int, concept_record_id: int
) -> dict[str, Any]:
    if str(draft.get("conceptrecid")) != str(concept_record_id):
        raise RuntimeError("Successor draft escaped the concept lineage")
    if draft.get("submitted") is not False or draft.get("state") == "done":
        raise RuntimeError("Successor draft is not mutable")
    draft_id = int(draft.get("id", -1))
    if draft_id <= 0 or draft_id == predecessor_id:
        raise RuntimeError("Successor draft identity is invalid")
    links = draft.get("links", {})
    if not isinstance(links, Mapping):
        raise RuntimeError("Successor draft links are malformed")
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
    expected_path = f"/api/deposit/depositions/{draft_id}"
    if urllib.parse.urlparse(result["self_url"]).path.rstrip("/") != expected_path:
        raise RuntimeError("Successor draft self link does not bind its identity")
    return result


def new_or_adopt_draft(
    token: str,
    predecessor_id: int,
    concept_record_id: int,
    public_predecessor: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], str]:
    _, authenticated = request_json(
        f"https://zenodo.org/api/deposit/depositions/{predecessor_id}", token=token
    )
    if not isinstance(authenticated, dict) or authenticated.get("submitted") is not True:
        raise RuntimeError("Authenticated predecessor deposition is not published")
    public_metadata = public_predecessor.get("metadata", {})
    authenticated_metadata = authenticated.get("metadata", {})
    if authenticated_metadata.get("creators") != public_metadata.get("creators"):
        raise RuntimeError("Authenticated and anonymous predecessor creators disagree")
    if canonical_license_id(authenticated_metadata.get("license")) != canonical_license_id(
        public_metadata.get("license")
    ):
        raise RuntimeError("Authenticated and anonymous predecessor license disagree")
    draft = find_existing_concept_draft(token, concept_record_id)
    origin = "adopted_existing"
    if draft is None:
        try:
            _, created = request_json(
                f"https://zenodo.org/api/deposit/depositions/{predecessor_id}/actions/newversion",
                method="POST",
                token=token,
                expected=(201,),
            )
        except RuntimeError:
            created = {}
            draft = find_existing_concept_draft(token, concept_record_id)
            if draft is None:
                raise
        if draft is None:
            latest_draft_url = (
                created.get("links", {}).get("latest_draft")
                if isinstance(created, Mapping)
                else None
            )
            if isinstance(latest_draft_url, str):
                _, candidate = request_json(latest_draft_url, token=token)
                if isinstance(candidate, dict):
                    draft = candidate
        if draft is None:
            for _ in range(12):
                draft = find_existing_concept_draft(token, concept_record_id)
                if draft is not None:
                    break
                time.sleep(1.0)
        if draft is None:
            raise RuntimeError("New-version action did not expose a successor draft")
        origin = "created_now"
    validated_draft_links(draft, predecessor_id, concept_record_id)
    return draft, authenticated, origin


def delete_exact_draft_file(row: Mapping[str, Any], draft_id: int, token: str) -> None:
    file_id = row.get("id")
    links = row.get("links", {})
    url = links.get("self") if isinstance(links, Mapping) else None
    if not isinstance(file_id, str) or not file_id or not isinstance(url, str):
        raise RuntimeError("Draft file lacks an exact deletion identity")
    validate_zenodo_url(url, authenticated=True)
    expected = f"/api/deposit/depositions/{draft_id}/files/{file_id}"
    if urllib.parse.urlparse(url).path.rstrip("/") != expected:
        raise RuntimeError("Refusing deletion outside the exact successor draft")
    request_no_content(url, method="DELETE", token=token)


def verify_remote_file(
    url: str, expected: Mapping[str, Any], *, token: str | None
) -> dict[str, Any]:
    with downloaded_file(url, token=token) as (path, size, sha256, md5):
        if (
            size != int(expected["bytes"])
            or md5 != expected["md5"]
            or sha256 != expected["sha256"]
        ):
            raise RuntimeError(f"Strong readback mismatch: {expected['remote_filename']}")
        observed_zip = zip_listing(path) if str(expected["remote_filename"]).casefold().endswith(".zip") else None
    if observed_zip is not None and observed_zip != expected.get("zip"):
        raise RuntimeError(f"ZIP listing drift: {expected['remote_filename']}")
    result = {
        "remote_filename": expected["remote_filename"],
        "bytes": size,
        "md5": md5,
        "sha256": sha256,
        "status": "PASS",
    }
    if observed_zip is not None:
        result["zip"] = observed_zip
    return result


def reconcile_draft_files(
    draft: Mapping[str, Any],
    draft_id: int,
    expected_rows: Sequence[dict[str, Any]],
    local_rows: Sequence[dict[str, Any]],
    token: str,
) -> list[dict[str, Any]]:
    expected = {row["remote_filename"]: row for row in expected_rows}
    local = {row["remote_filename"]: row for row in local_rows}
    rows = draft.get("files")
    if not isinstance(rows, list):
        raise RuntimeError("Draft file inventory is malformed")
    seen: set[str] = set()
    retained: set[str] = set()
    actions: list[dict[str, Any]] = []
    for raw_row in rows:
        if not isinstance(raw_row, Mapping):
            raise RuntimeError("Draft contains a malformed file row")
        name, size, md5 = draft_row_identity(raw_row)
        if name in seen:
            raise RuntimeError("Draft contains duplicate filenames")
        seen.add(name)
        target = expected.get(name)
        if target is None:
            raise RuntimeError(f"Draft has an unowned file; refusing deletion: {name}")
        weak_exact = (size, md5) == (target["bytes"], target["md5"])
        if weak_exact:
            verify_remote_file(draft_download_url(raw_row), target, token=token)
            retained.add(name)
            actions.append({"remote_filename": name, "action": "kept_exact"})
            continue
        if name not in REPLACED_DOCUMENTS:
            raise RuntimeError(f"Non-document draft file drifted; refusing deletion: {name}")
        delete_exact_draft_file(raw_row, draft_id, token)
        actions.append(
            {
                "remote_filename": name,
                "action": "replaced_document",
                "removed_bytes": size,
                "removed_md5": md5,
            }
        )
    missing = set(expected) - retained
    if any(name not in local for name in missing):
        raise RuntimeError("An inherited draft file is missing and cannot be reconstructed")
    return actions


def draft_inventory(draft: Mapping[str, Any]) -> dict[str, tuple[int, str]]:
    rows = draft.get("files")
    if not isinstance(rows, list):
        raise RuntimeError("Draft file inventory is malformed")
    result: dict[str, tuple[int, str]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise RuntimeError("Draft contains a malformed file row")
        name, size, md5 = draft_row_identity(row)
        if name in result:
            raise RuntimeError("Draft contains a duplicate filename")
        result[name] = (size, md5)
    return result


def verify_full_draft(
    draft: Mapping[str, Any], expected_rows: Sequence[dict[str, Any]], token: str
) -> list[dict[str, Any]]:
    expected = {row["remote_filename"]: row for row in expected_rows}
    if draft_inventory(draft) != public_weak_map(expected_rows):
        raise RuntimeError("Draft inventory differs from the exact final inventory")
    by_name: dict[str, Mapping[str, Any]] = {}
    for row in draft.get("files", []):
        name, _, _ = draft_row_identity(row)
        by_name[name] = row
    return [
        verify_remote_file(draft_download_url(by_name[name]), expected[name], token=token)
        for name in sorted(expected)
    ]


def target_metadata_from_state(state: Mapping[str, Any]) -> dict[str, Any]:
    target = state.get("target_metadata")
    if not isinstance(target, dict):
        raise RuntimeError("Release state lacks target metadata")
    return target


def validate_public_metadata(
    record: Mapping[str, Any], predecessor: Mapping[str, Any], target: Mapping[str, Any]
) -> list[str]:
    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        raise RuntimeError("Published metadata is malformed")
    for key in MUTATED_METADATA_KEYS:
        if metadata.get(key) != target.get(key):
            raise RuntimeError(f"Published target metadata drift: {key}")
    predecessor_metadata = predecessor.get("metadata", {})
    verified: list[str] = []
    for key in STABLE_METADATA_KEYS:
        if key in predecessor_metadata or key in metadata:
            if metadata.get(key) != predecessor_metadata.get(key):
                raise RuntimeError(f"Published stable metadata drift: {key}")
            verified.append(key)
    if metadata.get("access_right") != "open":
        raise RuntimeError("Published successor is not open access")
    assert_sanitized(metadata)
    return verified


def validate_public_snapshot(
    record: Mapping[str, Any],
    predecessor: Mapping[str, Any],
    concept_record_id: int,
    expected_rows: Sequence[dict[str, Any]],
    target_metadata: Mapping[str, Any],
) -> list[str]:
    validate_lineage_record(record, concept_record_id)
    weak = {
        name: (row["bytes"], row["md5"])
        for name, row in public_inventory(record).items()
    }
    if weak != public_weak_map(expected_rows):
        raise RuntimeError("Published inventory differs from the exact final inventory")
    return validate_public_metadata(record, predecessor, target_metadata)


def poll_public_record(
    record_id: int,
    predecessor_id: int,
    concept_record_id: int,
    predecessor: Mapping[str, Any],
    expected_rows: Sequence[dict[str, Any]],
    target_metadata: Mapping[str, Any],
    *,
    attempts: int = 60,
) -> tuple[dict[str, Any], list[str]]:
    last_error = "record not yet visible"
    for attempt in range(attempts):
        try:
            _, record = request_json(f"https://zenodo.org/api/records/{record_id}")
            if not isinstance(record, dict):
                raise RuntimeError("Published record is malformed")
            stable = validate_public_snapshot(
                record,
                predecessor,
                concept_record_id,
                expected_rows,
                target_metadata,
            )
            _, latest = request_json(
                f"https://zenodo.org/api/records/{predecessor_id}/versions/latest"
            )
            validate_lineage_record(latest, concept_record_id)
            if int(latest.get("id", -1)) != record_id:
                raise RuntimeError("Published successor is not concept-latest")
            return record, stable
        except RuntimeError as error:
            last_error = str(error)
        if attempt + 1 < attempts:
            time.sleep(2.0)
    raise RuntimeError(f"Published successor did not stabilize: {last_error}")


def verify_public_downloads(
    record: Mapping[str, Any], expected_rows: Sequence[dict[str, Any]]
) -> list[dict[str, Any]]:
    expected = {row["remote_filename"]: row for row in expected_rows}
    inventory = public_inventory(record)
    if set(inventory) != set(expected):
        raise RuntimeError("Anonymous readback inventory differs from the final inventory")
    return [
        verify_remote_file(inventory[name]["download_url"], expected[name], token=None)
        for name in sorted(expected)
    ]


def make_initial_state(
    args: argparse.Namespace,
    local_assets: Sequence[dict[str, Any]],
    inherited_assets: Sequence[dict[str, Any]],
    collisions: Sequence[dict[str, Any]],
    predecessor: Mapping[str, Any],
    release: Mapping[str, Any],
) -> dict[str, Any]:
    state = {
        "schema": STATE_SCHEMA,
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "status": "planned",
        "stage": "predecessor_and_local_assets_bound",
        "transaction": {
            "predecessor_record_id": args.predecessor_id,
            "concept_record_id": args.concept_record_id,
            "concept_doi": f"10.5281/zenodo.{args.concept_record_id}",
            "version": args.version,
            "release": release["release"],
            "title": release["title"],
        },
        "predecessor": {
            "doi": predecessor.get("doi"),
            "inventory": [
                {
                    "remote_filename": name,
                    "bytes": identity["bytes"],
                    "md5": identity["md5"],
                }
                for name, identity in sorted(public_inventory(predecessor).items())
            ],
        },
        "local_assets": list(copy.deepcopy(local_assets)),
        "inherited_assets": list(copy.deepcopy(inherited_assets)),
        "collisions": list(copy.deepcopy(collisions)),
        "expected_final_inventory": expected_final_inventory(local_assets, inherited_assets),
        "preserved_public_metadata": {
            "creators": copy.deepcopy(predecessor.get("metadata", {}).get("creators")),
            "license": copy.deepcopy(predecessor.get("metadata", {}).get("license")),
        },
    }
    assert_sanitized(state)
    return state


def update_state(path: Path, state: dict[str, Any], **changes: Any) -> dict[str, Any]:
    updated = copy.deepcopy(state)
    updated.update(changes)
    updated["updated_utc"] = utc_now()
    write_json_atomic(path, updated)
    return updated


def load_state(
    path: Path,
    args: argparse.Namespace,
    local_assets: Sequence[dict[str, Any]],
    predecessor: Mapping[str, Any],
    release: Mapping[str, Any],
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("Persisted release state is malformed") from error
    if state.get("schema") != STATE_SCHEMA:
        raise RuntimeError("Persisted release-state schema mismatch")
    transaction = state.get("transaction", {})
    expected_transaction = {
        "predecessor_record_id": args.predecessor_id,
        "concept_record_id": args.concept_record_id,
        "concept_doi": f"10.5281/zenodo.{args.concept_record_id}",
        "version": args.version,
        "release": release["release"],
        "title": release["title"],
    }
    if transaction != expected_transaction:
        raise RuntimeError("Persisted release state belongs to another transaction")
    if state.get("local_assets") != list(local_assets):
        raise RuntimeError("Local release assets differ from the frozen state")
    expected_preserved = {
        "creators": predecessor.get("metadata", {}).get("creators"),
        "license": predecessor.get("metadata", {}).get("license"),
    }
    if state.get("preserved_public_metadata") != expected_preserved:
        raise RuntimeError("Persisted creators or license differ from the predecessor")
    predecessor_inventory = [
        {
            "remote_filename": name,
            "bytes": identity["bytes"],
            "md5": identity["md5"],
        }
        for name, identity in sorted(public_inventory(predecessor).items())
    ]
    if state.get("predecessor", {}).get("inventory") != predecessor_inventory:
        raise RuntimeError("Predecessor public inventory differs from the frozen state")
    inherited = state.get("inherited_assets")
    expected_final = state.get("expected_final_inventory")
    if not isinstance(inherited, list) or not isinstance(expected_final, list):
        raise RuntimeError("Persisted inherited/final inventories are malformed")
    local_names = {row["remote_filename"] for row in local_assets}
    predecessor_weak = {
        name: (identity["bytes"], identity["md5"])
        for name, identity in public_inventory(predecessor).items()
    }
    expected_inherited_names = set(predecessor_weak) - local_names
    inherited_by_name: dict[str, dict[str, Any]] = {}
    for row in inherited:
        if not isinstance(row, dict):
            raise RuntimeError("Persisted inherited asset is malformed")
        name = safe_remote_name(row.get("remote_filename"))
        if name in inherited_by_name:
            raise RuntimeError("Persisted inherited inventory has duplicate names")
        inherited_by_name[name] = row
    if set(inherited_by_name) != expected_inherited_names:
        raise RuntimeError("Persisted inherited filenames differ from the predecessor")
    for name, row in inherited_by_name.items():
        if (row.get("bytes"), row.get("md5")) != predecessor_weak[name]:
            raise RuntimeError(f"Persisted inherited identity drift: {name}")
        if re.fullmatch(r"[0-9A-F]{64}", str(row.get("sha256", ""))) is None:
            raise RuntimeError(f"Persisted inherited SHA-256 is malformed: {name}")
        if name.casefold().endswith(".zip") and not isinstance(row.get("zip"), dict):
            raise RuntimeError(f"Persisted inherited ZIP receipt is absent: {name}")
    if expected_final != expected_final_inventory(local_assets, inherited):
        raise RuntimeError("Persisted final inventory is not deterministic")
    if state.get("status") not in {"planned", "draft", "published", "verified"}:
        raise RuntimeError("Persisted release status is invalid")
    if state["status"] in {"draft", "published", "verified"}:
        baseline = state.get("baseline_metadata")
        target = state.get("target_metadata")
        if not isinstance(baseline, dict) or not isinstance(target, dict):
            raise RuntimeError("Persisted metadata states are malformed")
        derived_target = copy.deepcopy(baseline)
        derived_target.update(
            {
                "title": release["title"],
                "version": args.version,
                "access_right": "open",
                "description": target_description(release),
            }
        )
        if target != derived_target:
            raise RuntimeError("Persisted target metadata is not deterministic")
        draft = state.get("draft")
        if not isinstance(draft, dict):
            raise RuntimeError("Persisted draft identity is malformed")
        for key in ("record_id", "self_url", "bucket_url", "publish_url"):
            if key not in draft:
                raise RuntimeError(f"Persisted draft lacks {key}")
        validated_draft_links(
            {
                "id": draft["record_id"],
                "conceptrecid": args.concept_record_id,
                "submitted": False,
                "state": "unsubmitted",
                "links": {
                    "self": draft["self_url"],
                    "bucket": draft["bucket_url"],
                    "publish": draft["publish_url"],
                },
            },
            args.predecessor_id,
            args.concept_record_id,
        )
    if state["status"] in {"published", "verified"} and int(
        state.get("published_record_id", -1)
    ) <= 0:
        raise RuntimeError("Published release state lacks its public record ID")
    assert_sanitized(state)
    return state


def recover_public_successor(
    args: argparse.Namespace,
    predecessor: Mapping[str, Any],
    state: Mapping[str, Any],
    *,
    attempts: int,
) -> tuple[dict[str, Any], list[str]] | None:
    expected = state["expected_final_inventory"]
    target = target_metadata_from_state(state)
    for attempt in range(attempts):
        _, latest = request_json(
            f"https://zenodo.org/api/records/{args.predecessor_id}/versions/latest"
        )
        validate_lineage_record(latest, args.concept_record_id)
        latest_id = int(latest.get("id", -1))
        if latest_id != args.predecessor_id:
            stable = validate_public_snapshot(
                latest, predecessor, args.concept_record_id, expected, target
            )
            return latest, stable
        if attempt + 1 < attempts:
            time.sleep(2.0)
    return None


def make_receipt(
    args: argparse.Namespace,
    state: Mapping[str, Any],
    predecessor: Mapping[str, Any],
    record: Mapping[str, Any],
    stable_keys: Sequence[str],
) -> dict[str, Any]:
    readback = verify_public_downloads(record, state["expected_final_inventory"])
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "created_utc": utc_now(),
        "status": "PASS",
        "predecessor": {
            "record_id": args.predecessor_id,
            "doi": predecessor.get("doi"),
            "concept_record_id": args.concept_record_id,
            "concept_doi": f"10.5281/zenodo.{args.concept_record_id}",
        },
        "published": {
            "record_id": int(record["id"]),
            "doi": record.get("doi"),
            "concept_record_id": args.concept_record_id,
            "concept_doi": f"10.5281/zenodo.{args.concept_record_id}",
            "title": state["transaction"]["title"],
            "version": args.version,
            "access_right": "open",
            "file_count": len(state["expected_final_inventory"]),
        },
        "metadata": {
            "creators_retained_exact": True,
            "license_retained_exact": True,
            "stable_keys_verified": list(stable_keys),
        },
        "local_release_assets": state["local_assets"],
        "inherited_assets": state["inherited_assets"],
        "collision_dispositions": state["collisions"],
        "final_inventory": state["expected_final_inventory"],
        "draft_actions": state.get("draft_actions", []),
        "anonymous_public_readback": readback,
        "all_final_files_anonymously_verified": True,
        "all_final_zips_reopened": all(
            "zip" in row for row in readback if row["remote_filename"].casefold().endswith(".zip")
        ),
    }
    assert_sanitized(receipt)
    return receipt


def finalize_receipt(
    args: argparse.Namespace,
    state: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    write_json_atomic(args.receipt, receipt)
    update_state(
        args.state,
        state,
        status="verified",
        stage="anonymous_public_readback_complete",
        published_record_id=int(receipt["published"]["record_id"]),
        receipt_identity={
            "bytes": args.receipt.stat().st_size,
            "sha256": digest(args.receipt, "sha256"),
        },
    )
    return receipt


def execute_release(
    args: argparse.Namespace,
    local_assets: Sequence[dict[str, Any]],
    release: Mapping[str, Any],
    predecessor: Mapping[str, Any],
    latest: Mapping[str, Any],
    loaded_state: dict[str, Any] | None,
) -> dict[str, Any]:
    state = loaded_state
    if state is None:
        if int(latest.get("id", -1)) != args.predecessor_id:
            raise RuntimeError("The configured predecessor is not concept-latest")
        inherited, collisions = collect_inherited_assets(predecessor, local_assets)
        state = make_initial_state(
            args, local_assets, inherited, collisions, predecessor, release
        )
        write_json_atomic(args.state, state)
    else:
        status = state["status"]
        latest_id = int(latest.get("id", -1))
        if status == "planned" and latest_id != args.predecessor_id:
            raise RuntimeError("Concept latest advanced before a successor draft was bound")
        if status == "draft" and latest_id != args.predecessor_id:
            recovered = recover_public_successor(
                args, predecessor, state, attempts=1
            )
            if recovered is None:
                raise RuntimeError("Concept latest advanced without the exact successor")
            record, stable = recovered
            state = update_state(
                args.state,
                state,
                status="published",
                stage="published_successor_recovered",
                published_record_id=int(record["id"]),
            )
            return finalize_receipt(
                args, state, make_receipt(args, state, predecessor, record, stable)
            )
        if status in {"published", "verified"}:
            record_id = int(state.get("published_record_id", -1))
            record, stable = poll_public_record(
                record_id,
                args.predecessor_id,
                args.concept_record_id,
                predecessor,
                state["expected_final_inventory"],
                target_metadata_from_state(state),
            )
            return finalize_receipt(
                args, state, make_receipt(args, state, predecessor, record, stable)
            )

    token = load_token()
    if state["status"] == "planned":
        draft, authenticated, origin = new_or_adopt_draft(
            token,
            args.predecessor_id,
            args.concept_record_id,
            predecessor,
        )
        baseline, target = make_target_draft_metadata(
            copy.deepcopy(draft.get("metadata", {})),
            authenticated,
            release,
            args.version,
        )
        state = update_state(
            args.state,
            state,
            status="draft",
            stage="draft_adopted_and_metadata_frozen",
            baseline_metadata=baseline,
            target_metadata=target,
            draft={
                "origin": origin,
                **validated_draft_links(draft, args.predecessor_id, args.concept_record_id),
            },
        )

    draft_links = state.get("draft")
    if not isinstance(draft_links, dict):
        raise RuntimeError("Persisted state lacks its successor draft")
    try:
        _, draft = request_json(draft_links["self_url"], token=token)
    except RuntimeError:
        recovered = recover_public_successor(args, predecessor, state, attempts=45)
        if recovered is None:
            raise
        record, stable = recovered
        state = update_state(
            args.state,
            state,
            status="published",
            stage="published_successor_recovered",
            published_record_id=int(record["id"]),
        )
        return finalize_receipt(
            args, state, make_receipt(args, state, predecessor, record, stable)
        )
    if not isinstance(draft, dict):
        raise RuntimeError("Zenodo returned a malformed persisted draft")
    live_links = validated_draft_links(draft, args.predecessor_id, args.concept_record_id)
    for key in ("record_id", "self_url", "bucket_url", "publish_url"):
        if live_links[key] != draft_links[key]:
            raise RuntimeError("Persisted draft identity or action links drifted")
    current_metadata = draft.get("metadata", {})
    if current_metadata not in (state["baseline_metadata"], state["target_metadata"]):
        raise RuntimeError("Draft metadata differs from both frozen accepted states")

    actions = reconcile_draft_files(
        draft,
        int(draft_links["record_id"]),
        state["expected_final_inventory"],
        local_assets,
        token,
    )
    _, draft = request_json(draft_links["self_url"], token=token)
    current = draft_inventory(draft)
    expected = public_weak_map(state["expected_final_inventory"])
    local_map = {row["remote_filename"]: row for row in local_assets}
    for name in sorted(set(expected) - set(current)):
        if name not in local_map:
            raise RuntimeError("A preserved inherited asset disappeared from the draft")
        response = upload_file(
            draft_links["bucket_url"], args.asset_dir / name, name, token
        )
        response_size = int(response.get("size", response.get("filesize", -1)))
        response_md5 = normalize_checksum(str(response.get("checksum", "")))
        if (response_size, response_md5) != expected[name]:
            raise RuntimeError(f"Upload identity mismatch for {name}")
        actions.append({"remote_filename": name, "action": "uploaded_local_asset"})
    _, draft = request_json(draft_links["self_url"], token=token)
    strong_draft_readback = verify_full_draft(
        draft, state["expected_final_inventory"], token
    )
    state = update_state(
        args.state,
        state,
        status="draft",
        stage="inventory_exact_and_strongly_verified",
        draft_actions=actions,
        authenticated_draft_readback=strong_draft_readback,
    )

    if draft.get("metadata", {}) == state["baseline_metadata"]:
        request_json(
            draft_links["self_url"],
            method="PUT",
            token=token,
            payload={"metadata": state["target_metadata"]},
            expected=(200,),
        )
        _, draft = request_json(draft_links["self_url"], token=token)
    if draft.get("metadata", {}) != state["target_metadata"]:
        raise RuntimeError("Draft metadata write/readback mismatch")
    verify_full_draft(draft, state["expected_final_inventory"], token)
    state = update_state(
        args.state,
        state,
        status="draft",
        stage="publish_pending",
    )

    recovered = recover_public_successor(args, predecessor, state, attempts=1)
    if recovered is None:
        try:
            _, published = request_json(
                draft_links["publish_url"],
                method="POST",
                token=token,
                expected=(202,),
            )
            if not isinstance(published, dict):
                raise RuntimeError("Publish response is malformed")
            record_id = int(published.get("record_id") or published.get("id") or -1)
            if record_id <= 0:
                raise RuntimeError("Publish response omitted the record ID")
            state = update_state(
                args.state,
                state,
                status="published",
                stage="publish_response_persisted",
                published_record_id=record_id,
            )
            record, stable = poll_public_record(
                record_id,
                args.predecessor_id,
                args.concept_record_id,
                predecessor,
                state["expected_final_inventory"],
                state["target_metadata"],
            )
        except RuntimeError:
            recovered = recover_public_successor(args, predecessor, state, attempts=45)
            if recovered is None:
                raise
            record, stable = recovered
    else:
        record, stable = recovered
    state = update_state(
        args.state,
        state,
        status="published",
        stage="published_record_verified",
        published_record_id=int(record["id"]),
    )
    return finalize_receipt(
        args, state, make_receipt(args, state, predecessor, record, stable)
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-dir", type=Path, required=True)
    parser.add_argument("--predecessor-id", type=int, required=True)
    parser.add_argument("--concept-record-id", type=int, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create/adopt, reconcile, publish, and anonymously verify the successor.",
    )
    return parser.parse_args(argv)


def validate_arguments(args: argparse.Namespace) -> None:
    if args.predecessor_id <= 0 or args.concept_record_id <= 0:
        raise RuntimeError("Zenodo record IDs must be positive integers")
    if args.predecessor_id == args.concept_record_id:
        raise RuntimeError("Predecessor and concept record IDs must differ")
    if SAFE_VERSION_RE.fullmatch(args.version) is None or args.version.strip() != args.version:
        raise RuntimeError("Version is empty or contains unsafe characters")
    asset_root = args.asset_dir.resolve(strict=False)
    state = args.state.resolve(strict=False)
    receipt = args.receipt.resolve(strict=False)
    if state == receipt:
        raise RuntimeError("State and receipt paths must differ")
    for destination in (state, receipt):
        try:
            destination.relative_to(asset_root)
        except ValueError:
            pass
        else:
            raise RuntimeError("State and receipt must be outside the frozen asset directory")
    if (args.state.exists() and not args.state.is_file()) or (
        args.receipt.exists() and not args.receipt.is_file()
    ):
        raise RuntimeError("State and receipt destinations must be ordinary files")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    validate_arguments(args)
    local_assets, release = validate_local_assets(
        args.asset_dir, args.concept_record_id
    )
    predecessor, latest = anonymous_preflight(
        args.predecessor_id, args.concept_record_id
    )
    if canonical_license_id(release["preservation"]["license"]) != canonical_license_id(
        predecessor["metadata"]["license"]
    ):
        raise RuntimeError("Local package and predecessor licenses differ")
    state = load_state(args.state, args, local_assets, predecessor, release)
    latest_id = int(latest.get("id", -1))
    if state is None and latest_id != args.predecessor_id:
        raise RuntimeError("The configured predecessor is not concept-latest")
    if state is not None and state["status"] in {"planned", "draft"}:
        if latest_id != args.predecessor_id:
            validate_lineage_record(latest, args.concept_record_id)
    if args.execute:
        receipt = execute_release(
            args, local_assets, release, predecessor, latest, state
        )
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0
    preflight = {
        "schema": PREFLIGHT_SCHEMA,
        "status": "PASS",
        "predecessor_id": args.predecessor_id,
        "predecessor_is_concept_latest": latest_id == args.predecessor_id,
        "latest_public_id": latest_id,
        "concept_record_id": args.concept_record_id,
        "concept_doi": f"10.5281/zenodo.{args.concept_record_id}",
        "title": release["title"],
        "version": args.version,
        "access_right": "open",
        "local_file_count": len(local_assets),
        "local_assets": local_assets,
        "local_zip_reopen": "PASS",
        "release_state": state.get("status") if state else "not_started",
        "credential_read": False,
        "mutation_performed": False,
    }
    assert_sanitized(preflight)
    print(json.dumps(preflight, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
