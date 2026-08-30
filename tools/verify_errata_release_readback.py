#!/usr/bin/env python3
"""Anonymously verify a GitHub/Zenodo errata checkpoint release.

The verifier is deliberately read-only and fail-closed.  It binds every local
release asset to the public GitHub release and to the current-file subset of a
public, open-access Zenodo record, downloads every Zenodo file (including
inherited preservation files), and reopens every ZIP with a complete listing
digest and CRC check.  An optional Git-tree comparison verifies the exact raw
bytes of every changed leaf path without trusting a local checkout.

No credential is read, accepted, transmitted, or written to the receipt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


SCHEMA = "unofficial-ai-integrated-stacks-errata-release-readback/v1"
USER_AGENT = "unofficial-ai-stacks-release-readback/1"
HEX40_RE = re.compile(r"[0-9a-fA-F]{40}")
HEX64_RE = re.compile(r"[0-9a-fA-F]{64}")
REPOSITORY_RE = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/"
    r"[A-Za-z0-9._-](?:[A-Za-z0-9._-]{0,99})"
)
TAG_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9._/+()-]{0,199})")
MAX_JSON_BYTES = 64 * 1024 * 1024
DOWNLOAD_CHUNK_BYTES = 1024 * 1024


class VerificationError(RuntimeError):
    """A public or local invariant did not hold."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def safe_filename(value: Any) -> str:
    require(isinstance(value, str) and value not in {"", ".", ".."}, "invalid filename")
    assert isinstance(value, str)
    require(
        "/" not in value
        and "\\" not in value
        and "\x00" not in value
        and re.match(r"^[A-Za-z]:", value) is None,
        "release filename is path-shaped",
    )
    return value


def safe_repository(value: str) -> str:
    require(REPOSITORY_RE.fullmatch(value) is not None, "invalid GitHub repository")
    owner, name = value.split("/", 1)
    require(not name.endswith(".git"), "repository must not use a .git suffix")
    return f"{owner}/{name}"


def safe_tag(value: str) -> str:
    require(TAG_RE.fullmatch(value) is not None, "invalid release tag")
    require(
        ".." not in value
        and "//" not in value
        and "@{" not in value
        and not value.endswith((".", "/", ".lock")),
        "invalid release tag",
    )
    return value


def exact_commit(value: str, label: str) -> str:
    require(HEX40_RE.fullmatch(value) is not None, f"{label} must be a full commit ID")
    return value.lower()


def safe_git_path(value: Any) -> str:
    require(isinstance(value, str) and value != "", "invalid Git tree path")
    assert isinstance(value, str)
    pure = PurePosixPath(value)
    require(
        "\\" not in value
        and "\x00" not in value
        and not pure.is_absolute()
        and all(part not in {"", ".", ".."} for part in pure.parts)
        and (not pure.parts or re.match(r"^[A-Za-z]:", pure.parts[0]) is None),
        "unsafe Git tree path",
    )
    return pure.as_posix()


def validate_url(url: str, family: str) -> None:
    try:
        parsed = urllib.parse.urlparse(url)
        port = parsed.port
    except ValueError as error:
        raise VerificationError("malformed public URL") from error
    require(
        parsed.scheme == "https"
        and parsed.hostname is not None
        and parsed.username is None
        and parsed.password is None
        and port in (None, 443),
        "refusing a non-HTTPS or credential-bearing URL",
    )
    host = parsed.hostname.casefold()
    if family == "github":
        allowed = host in {"github.com", "api.github.com", "raw.githubusercontent.com"}
        allowed = allowed or host.endswith(".githubusercontent.com")
    elif family == "zenodo":
        allowed = host == "zenodo.org" or host.endswith(".zenodo.org")
    else:  # pragma: no cover - an internal programmer error
        raise VerificationError("unknown URL trust family")
    require(allowed, f"refusing a redirect outside the {family} trust boundary")


class RestrictedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, family: str) -> None:
        super().__init__()
        self.family = family

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        validate_url(newurl, self.family)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENERS = {
    family: urllib.request.build_opener(RestrictedRedirectHandler(family))
    for family in ("github", "zenodo")
}


def public_request(url: str, family: str, *, accept: str = "application/json") -> Any:
    validate_url(url, family)
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        return OPENERS[family].open(request, timeout=900)
    except urllib.error.HTTPError as error:
        raise VerificationError(
            f"anonymous {family} request returned HTTP {error.code}"
        ) from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise VerificationError(f"anonymous {family} request failed") from error


def request_json(url: str, family: str) -> Mapping[str, Any]:
    with public_request(url, family) as response:
        require(response.status == 200, f"unexpected {family} HTTP status")
        raw = response.read(MAX_JSON_BYTES + 1)
    require(len(raw) <= MAX_JSON_BYTES, f"{family} JSON response is too large")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"{family} returned malformed JSON") from error
    require(isinstance(value, Mapping), f"{family} JSON response is not an object")
    return value


def digest_file(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(DOWNLOAD_CHUNK_BYTES), b""):
            hasher.update(chunk)
    return hasher.hexdigest().upper()


def git_blob_file(path: Path) -> str:
    size = path.stat().st_size
    hasher = hashlib.sha1()
    hasher.update(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(DOWNLOAD_CHUNK_BYTES), b""):
            hasher.update(chunk)
    return hasher.hexdigest().lower()


def zip_listing(path: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = archive.infolist()
            require(bool(infos), "ZIP archive is empty")
            for info in infos:
                name = info.filename
                pure = PurePosixPath(name)
                require(
                    bool(name)
                    and name not in seen
                    and "\\" not in name
                    and "\x00" not in name
                    and not pure.is_absolute()
                    and all(part not in {"", ".", ".."} for part in pure.parts)
                    and (not pure.parts or re.match(r"^[A-Za-z]:", pure.parts[0]) is None),
                    "ZIP has an unsafe or duplicate member",
                )
                require(not (info.flag_bits & 0x1), "ZIP contains an encrypted member")
                seen.add(name)
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
            require(bad is None, "ZIP CRC check failed")
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as error:
        raise VerificationError("ZIP could not be reopened") from error
    return {
        "status": "PASS",
        "entry_count": len(rows),
        "file_count": sum(not row["directory"] for row in rows),
        "directory_count": sum(row["directory"] for row in rows),
        "uncompressed_bytes": sum(row["bytes"] for row in rows),
        "compressed_member_bytes": sum(row["compressed_bytes"] for row in rows),
        "listing_sha256": canonical_json_sha256(rows),
        "crc_test": "PASS",
    }


def file_identity(path: Path, name: str | None = None) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "asset is not an ordinary file")
    before = path.stat().st_size
    result: dict[str, Any] = {
        "name": safe_filename(name if name is not None else path.name),
        "bytes": before,
        "md5": digest_file(path, "md5"),
        "sha256": digest_file(path, "sha256"),
    }
    require(path.stat().st_size == before, "asset changed while it was hashed")
    if result["name"].casefold().endswith(".zip"):
        result["zip"] = zip_listing(path)
    return result


def local_assets(asset_dir: Path) -> dict[str, dict[str, Any]]:
    require(asset_dir.is_dir() and not asset_dir.is_symlink(), "asset directory is invalid")
    children = sorted(asset_dir.iterdir(), key=lambda item: item.name)
    require(bool(children), "asset directory is empty")
    require(
        all(child.is_file() and not child.is_symlink() for child in children),
        "asset directory must contain ordinary files only",
    )
    result: dict[str, dict[str, Any]] = {}
    folded: set[str] = set()
    for child in children:
        name = safe_filename(child.name)
        require(name.casefold() not in folded, "asset filenames collide case-insensitively")
        folded.add(name.casefold())
        result[name] = file_identity(child, name)
    return result


def download_file(url: str, family: str, directory: Path, sequence: int) -> Path:
    target = directory / f"download-{sequence:06d}.bin"
    hasher = hashlib.sha256()  # stream once here; identity performs an independent pass
    total = 0
    with public_request(url, family, accept="application/octet-stream") as response:
        require(response.status == 200, f"unexpected {family} download status")
        content_length = response.headers.get("Content-Length")
        with target.open("wb") as output:
            while True:
                chunk = response.read(DOWNLOAD_CHUNK_BYTES)
                if not chunk:
                    break
                output.write(chunk)
                hasher.update(chunk)
                total += len(chunk)
            output.flush()
            os.fsync(output.fileno())
    if content_length is not None:
        try:
            declared = int(content_length)
        except ValueError as error:
            raise VerificationError("download Content-Length is malformed") from error
        require(declared == total, "download Content-Length mismatch")
    require(target.stat().st_size == total, "download size changed after streaming")
    require(digest_file(target, "sha256") == hasher.hexdigest().upper(), "download hash race")
    return target


def public_download_identity(
    *,
    url: str,
    family: str,
    name: str,
    directory: Path,
    sequence: int,
    expected_bytes: int | None = None,
    expected_sha256: str | None = None,
    expected_md5: str | None = None,
) -> dict[str, Any]:
    target = download_file(url, family, directory, sequence)
    identity = file_identity(target, name)
    if expected_bytes is not None:
        require(identity["bytes"] == expected_bytes, f"public byte count mismatch for {name}")
    if expected_sha256 is not None:
        require(
            identity["sha256"] == expected_sha256.upper(),
            f"public SHA-256 mismatch for {name}",
        )
    if expected_md5 is not None:
        require(identity["md5"] == expected_md5.upper(), f"public MD5 mismatch for {name}")
    identity["status"] = "PASS"
    return identity


def inventory_tuple_sha(rows: Sequence[Mapping[str, Any]]) -> str:
    tuples = [
        {"name": row["name"], "bytes": row["bytes"], "sha256": row["sha256"]}
        for row in sorted(rows, key=lambda item: str(item["name"]))
    ]
    return canonical_json_sha256(tuples)


def require_identity_match(
    observed: Mapping[str, Any], expected: Mapping[str, Any], label: str
) -> None:
    require(
        (observed.get("bytes"), observed.get("sha256"))
        == (expected.get("bytes"), expected.get("sha256")),
        f"{label} identity mismatch for {expected.get('name')}",
    )
    if "zip" in expected:
        require(observed.get("zip") == expected.get("zip"), f"{label} ZIP listing mismatch")


def github_url(repository: str, suffix: str) -> str:
    return f"https://api.github.com/repos/{repository}/{suffix}"


def verify_github(
    repository: str,
    tag: str,
    local: Mapping[str, Mapping[str, Any]],
    directory: Path,
    source_commit: str | None,
) -> tuple[dict[str, Any], str, int]:
    repo = request_json(github_url(repository, ""), "github")
    require(repo.get("private") is False, "GitHub repository is not public")
    require(
        str(repo.get("full_name", "")).casefold() == repository.casefold(),
        "GitHub repository identity mismatch",
    )
    visibility = repo.get("visibility")
    require(visibility in (None, "public"), "GitHub repository visibility is not public")

    encoded_tag = urllib.parse.quote(tag, safe="")
    release = request_json(github_url(repository, f"releases/tags/{encoded_tag}"), "github")
    require(release.get("draft") is False, "GitHub release is still a draft")
    require(release.get("tag_name") == tag, "GitHub release tag mismatch")
    require(isinstance(release.get("id"), int), "GitHub release ID is malformed")

    commit = request_json(github_url(repository, f"commits/{encoded_tag}"), "github")
    resolved_commit = str(commit.get("sha", "")).lower()
    require(HEX40_RE.fullmatch(resolved_commit) is not None, "release tag did not resolve")
    if source_commit is not None:
        require(resolved_commit == source_commit, "release tag does not resolve to source commit")

    raw_assets = release.get("assets")
    require(isinstance(raw_assets, list), "GitHub release asset inventory is malformed")
    inventory: dict[str, Mapping[str, Any]] = {}
    folded: set[str] = set()
    for row in raw_assets:
        require(isinstance(row, Mapping), "GitHub release has a malformed asset row")
        name = safe_filename(row.get("name"))
        require(name not in inventory and name.casefold() not in folded, "duplicate GitHub asset")
        require(row.get("state") == "uploaded", f"GitHub asset is not uploaded: {name}")
        require(isinstance(row.get("size"), int) and row["size"] >= 0, "bad GitHub asset size")
        url = row.get("browser_download_url")
        require(isinstance(url, str), "GitHub asset lacks a public download URL")
        validate_url(url, "github")
        inventory[name] = row
        folded.add(name.casefold())
    require(set(inventory) == set(local), "GitHub release asset filenames differ from local assets")

    verified: list[dict[str, Any]] = []
    sequence = 0
    for name in sorted(local):
        sequence += 1
        expected = local[name]
        row = inventory[name]
        require(row["size"] == expected["bytes"], f"GitHub API size mismatch for {name}")
        digest_field = row.get("digest")
        if digest_field is not None:
            require(
                str(digest_field).casefold() == f"sha256:{expected['sha256']}".casefold(),
                f"GitHub API digest mismatch for {name}",
            )
        observed = public_download_identity(
            url=str(row["browser_download_url"]),
            family="github",
            name=name,
            directory=directory,
            sequence=sequence,
            expected_bytes=int(expected["bytes"]),
            expected_sha256=str(expected["sha256"]),
            expected_md5=str(expected["md5"]),
        )
        require_identity_match(observed, expected, "GitHub")
        verified.append(observed)

    return (
        {
            "repository": repository,
            "repository_public": True,
            "default_branch": repo.get("default_branch"),
            "release_id": release["id"],
            "tag": tag,
            "tag_commit": resolved_commit,
            "release_public": True,
            "prerelease": bool(release.get("prerelease")),
            "current_release_assets": verified,
            "current_release_asset_count": len(verified),
            "current_release_asset_bytes": sum(row["bytes"] for row in verified),
            "current_release_tuple_set_sha256": inventory_tuple_sha(verified),
        },
        resolved_commit,
        sequence,
    )


def normalize_md5(value: Any) -> str:
    text = str(value).split(":", 1)[-1].upper()
    require(re.fullmatch(r"[0-9A-F]{32}", text) is not None, "Zenodo checksum is malformed")
    return text


def zenodo_inventory(record: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = record.get("files")
    require(isinstance(rows, list), "Zenodo file inventory is malformed")
    result: dict[str, dict[str, Any]] = {}
    folded: set[str] = set()
    for row in rows:
        require(isinstance(row, Mapping), "Zenodo has a malformed file row")
        name = safe_filename(row.get("key"))
        require(name not in result and name.casefold() not in folded, "duplicate Zenodo file")
        size = row.get("size")
        require(isinstance(size, int) and size >= 0, "Zenodo file size is malformed")
        md5 = normalize_md5(row.get("checksum"))
        links = row.get("links")
        require(isinstance(links, Mapping), "Zenodo file links are malformed")
        url = links.get("self") or links.get("download") or links.get("content")
        require(isinstance(url, str), "Zenodo file lacks a public download URL")
        validate_url(url, "zenodo")
        result[name] = {"name": name, "bytes": size, "md5": md5, "url": url}
        folded.add(name.casefold())
    require(bool(result), "Zenodo record has no public files")
    return result


def verify_zenodo(
    record_id: int,
    local: Mapping[str, Mapping[str, Any]],
    directory: Path,
    sequence: int,
) -> tuple[dict[str, Any], int]:
    record = request_json(f"https://zenodo.org/api/records/{record_id}", "zenodo")
    require(int(record.get("id", -1)) == record_id, "Zenodo record identity mismatch")
    metadata = record.get("metadata")
    require(isinstance(metadata, Mapping), "Zenodo metadata is malformed")
    require(metadata.get("access_right") == "open", "Zenodo record is not open access")
    inventory = zenodo_inventory(record)
    require(set(local).issubset(inventory), "Zenodo omits a current release asset")

    verified: list[dict[str, Any]] = []
    for name in sorted(inventory):
        sequence += 1
        row = inventory[name]
        expected = local.get(name)
        if expected is not None:
            require(row["bytes"] == expected["bytes"], f"Zenodo API size mismatch for {name}")
            require(row["md5"] == expected["md5"], f"Zenodo API MD5 mismatch for {name}")
        observed = public_download_identity(
            url=str(row["url"]),
            family="zenodo",
            name=name,
            directory=directory,
            sequence=sequence,
            expected_bytes=int(row["bytes"]),
            expected_sha256=str(expected["sha256"]) if expected is not None else None,
            expected_md5=str(row["md5"]),
        )
        if expected is not None:
            require_identity_match(observed, expected, "Zenodo")
            observed["role"] = "current_release"
        else:
            observed["role"] = "inherited"
        verified.append(observed)

    current = [row for row in verified if row["role"] == "current_release"]
    inherited = [row for row in verified if row["role"] == "inherited"]
    concept_record_id = record.get("conceptrecid")
    concept_doi = record.get("conceptdoi") or metadata.get("conceptdoi")
    return (
        {
            "record_id": record_id,
            "doi": record.get("doi"),
            "concept_record_id": int(concept_record_id) if str(concept_record_id).isdigit() else concept_record_id,
            "concept_doi": concept_doi,
            "access_right": "open",
            "record_public": True,
            "file_count": len(verified),
            "file_bytes": sum(row["bytes"] for row in verified),
            "current_release_assets": current,
            "current_release_asset_count": len(current),
            "current_release_asset_bytes": sum(row["bytes"] for row in current),
            "current_release_tuple_set_sha256": inventory_tuple_sha(current),
            "inherited_assets": inherited,
            "inherited_asset_count": len(inherited),
            "inherited_asset_bytes": sum(row["bytes"] for row in inherited),
            "complete_record_tuple_set_sha256": inventory_tuple_sha(verified),
        },
        sequence,
    )


def github_commit(repository: str, commit_id: str) -> Mapping[str, Any]:
    value = request_json(github_url(repository, f"commits/{commit_id}"), "github")
    require(str(value.get("sha", "")).lower() == commit_id, "GitHub commit identity mismatch")
    return value


def recursive_tree(repository: str, commit_id: str) -> tuple[str, dict[str, dict[str, Any]]]:
    commit = github_commit(repository, commit_id)
    commit_data = commit.get("commit")
    require(isinstance(commit_data, Mapping), "GitHub commit data is malformed")
    tree_link = commit_data.get("tree")
    require(isinstance(tree_link, Mapping), "GitHub commit tree link is malformed")
    tree_sha = str(tree_link.get("sha", "")).lower()
    require(HEX40_RE.fullmatch(tree_sha) is not None, "GitHub tree identity is malformed")
    value = request_json(github_url(repository, f"git/trees/{tree_sha}?recursive=1"), "github")
    require(value.get("truncated") is False, "GitHub recursive tree response is truncated")
    require(str(value.get("sha", "")).lower() == tree_sha, "GitHub tree response drift")
    rows = value.get("tree")
    require(isinstance(rows, list), "GitHub recursive tree is malformed")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        require(isinstance(row, Mapping), "GitHub tree has a malformed row")
        kind = row.get("type")
        if kind == "tree":
            continue
        require(kind in {"blob", "commit"}, "GitHub tree has an unsupported leaf type")
        path = safe_git_path(row.get("path"))
        require(path not in result, "GitHub recursive tree has a duplicate leaf path")
        sha = str(row.get("sha", "")).lower()
        require(HEX40_RE.fullmatch(sha) is not None, "GitHub tree leaf SHA is malformed")
        size = row.get("size")
        if kind == "blob":
            require(isinstance(size, int) and size >= 0, "GitHub blob size is malformed")
        result[path] = {
            "type": kind,
            "mode": row.get("mode"),
            "sha": sha,
            "bytes": size,
        }
    return tree_sha, result


def raw_github_url(repository: str, commit_id: str, path: str) -> str:
    quoted_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    return f"https://raw.githubusercontent.com/{repository}/{commit_id}/{quoted_path}"


def verify_changed_paths(
    repository: str,
    base: str,
    head: str,
    directory: Path,
    sequence: int,
) -> tuple[dict[str, Any], int]:
    require(base != head, "changed-base and changed-head are identical")
    base_tree_sha, base_tree = recursive_tree(repository, base)
    head_tree_sha, head_tree = recursive_tree(repository, head)
    paths = sorted(
        path
        for path in set(base_tree) | set(head_tree)
        if base_tree.get(path) != head_tree.get(path)
    )
    require(bool(paths), "Git tree comparison found no changed paths")
    rows: list[dict[str, Any]] = []
    total = 0
    for path in paths:
        before = base_tree.get(path)
        after = head_tree.get(path)
        if before is None:
            status = "added"
            readback_commit = head
            leaf = after
        elif after is None:
            status = "deleted"
            readback_commit = base
            leaf = before
        else:
            status = "modified"
            readback_commit = head
            leaf = after
        require(isinstance(leaf, Mapping), "changed path lacks a leaf identity")
        require(leaf.get("type") == "blob", "changed Git submodules cannot be raw-verified")
        sequence += 1
        observed_path = download_file(
            raw_github_url(repository, readback_commit, path),
            "github",
            directory,
            sequence,
        )
        identity = file_identity(observed_path, Path(path).name)
        blob = git_blob_file(observed_path)
        require(identity["bytes"] == leaf.get("bytes"), f"raw byte count mismatch: {path}")
        require(blob == leaf.get("sha"), f"raw Git-blob mismatch: {path}")
        total += identity["bytes"]
        row: dict[str, Any] = {
            "path": path,
            "status": status,
            "readback_commit": readback_commit,
            "bytes": identity["bytes"],
            "sha256": identity["sha256"],
            "git_blob": blob,
            "status_check": "PASS",
        }
        if before is not None:
            row["base_git_blob"] = before["sha"]
        if after is not None:
            row["head_git_blob"] = after["sha"]
        rows.append(row)
    return (
        {
            "status": "PASS",
            "base_commit": base,
            "base_tree": base_tree_sha,
            "head_commit": head,
            "head_tree": head_tree_sha,
            "changed_path_count": len(rows),
            "readback_bytes": total,
            "changed_paths": rows,
            "changed_path_tuple_set_sha256": canonical_json_sha256(rows),
        },
        sequence,
    )


def sanitized(value: Any) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    require(
        re.search(
            r"(?i)(?:(?<![A-Za-z0-9])[a-z]:[\\/]"
            r"|(?:^|[\s\"'(\[])/(?:home|users)/)",
            serialized,
        )
        is None,
        "receipt contains a local absolute path",
    )
    require(
        re.search(r"(?i)(access[_ -]?token|authorization\s*[:=]|bearer\s+)", serialized)
        is None,
        "receipt contains credential-shaped text",
    )
    require("?" not in serialized or "https://" not in serialized, "receipt contains a query URL")


def write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    sanitized(value)
    require(not path.is_symlink(), "output path must not be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Anonymously verify exact GitHub/Zenodo release bytes, ZIP listings, "
            "cross-host parity, and optionally every changed Git path."
        )
    )
    parser.add_argument("--repository", required=True, help="GitHub owner/repository")
    parser.add_argument("--tag", required=True, help="public GitHub release tag")
    parser.add_argument("--asset-dir", required=True, type=Path, help="local release assets")
    parser.add_argument(
        "--zenodo-record-id", required=True, type=int, help="public Zenodo record ID"
    )
    parser.add_argument("--output", required=True, type=Path, help="sanitized JSON receipt")
    parser.add_argument(
        "--source-commit", help="require the release tag to resolve to this full commit ID"
    )
    parser.add_argument(
        "--changed-base", help="full base commit for optional remote changed-path readback"
    )
    parser.add_argument(
        "--changed-head", help="full head commit for optional remote changed-path readback"
    )
    args = parser.parse_args(argv)
    try:
        args.repository = safe_repository(args.repository)
        args.tag = safe_tag(args.tag)
        require(args.zenodo_record_id > 0, "Zenodo record ID must be positive")
        if args.source_commit is not None:
            args.source_commit = exact_commit(args.source_commit, "source-commit")
        require(
            (args.changed_base is None) == (args.changed_head is None),
            "changed-base and changed-head must be supplied together",
        )
        if args.changed_base is not None:
            args.changed_base = exact_commit(args.changed_base, "changed-base")
            args.changed_head = exact_commit(args.changed_head, "changed-head")
            if args.source_commit is not None:
                require(
                    args.changed_head == args.source_commit,
                    "changed-head must equal source-commit",
                )
    except VerificationError as error:
        parser.error(str(error))
    return args


def run(args: argparse.Namespace) -> dict[str, Any]:
    local = local_assets(args.asset_dir)
    with tempfile.TemporaryDirectory(prefix="stacks-release-readback-") as temporary:
        directory = Path(temporary)
        github, resolved_commit, sequence = verify_github(
            args.repository,
            args.tag,
            local,
            directory,
            args.source_commit,
        )
        zenodo, sequence = verify_zenodo(
            args.zenodo_record_id, local, directory, sequence
        )
        local_rows = [local[name] for name in sorted(local)]
        local_tuple_sha = inventory_tuple_sha(local_rows)
        require(
            github["current_release_tuple_set_sha256"] == local_tuple_sha,
            "GitHub/local current release parity failed",
        )
        require(
            zenodo["current_release_tuple_set_sha256"] == local_tuple_sha,
            "Zenodo/local current release parity failed",
        )
        changed = None
        if args.changed_base is not None:
            assert args.changed_head is not None
            require(
                args.changed_head == resolved_commit,
                "changed-head does not equal the release tag commit",
            )
            changed, sequence = verify_changed_paths(
                args.repository,
                args.changed_base,
                args.changed_head,
                directory,
                sequence,
            )

    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS",
        "checked_utc": utc_now(),
        "method": (
            "unauthenticated HTTPS/API readback; exact filename, byte, MD5, SHA-256, "
            "Git-blob where applicable, ZIP reopen/CRC/complete-listing, and cross-host checks"
        ),
        "local_release_assets": local_rows,
        "local_release_asset_count": len(local_rows),
        "local_release_asset_bytes": sum(row["bytes"] for row in local_rows),
        "current_release_tuple_set_sha256": local_tuple_sha,
        "github": github,
        "zenodo": zenodo,
        "changed_path_readback": changed,
        "checks": {
            "github_repository_public": True,
            "github_release_public": True,
            "github_release_tag_exact": True,
            "github_current_assets_exact": True,
            "zenodo_record_public": True,
            "zenodo_access_open": True,
            "zenodo_all_record_files_downloaded": True,
            "current_release_cross_host_parity": True,
            "all_local_zips_reopened_and_crc_checked": all(
                "zip" not in row or row["zip"]["status"] == "PASS" for row in local_rows
            ),
            "all_github_zips_reopened_and_crc_checked": all(
                "zip" not in row or row["zip"]["status"] == "PASS"
                for row in github["current_release_assets"]
            ),
            "all_zenodo_zips_reopened_and_crc_checked": all(
                "zip" not in row or row["zip"]["status"] == "PASS"
                for row in zenodo["current_release_assets"] + zenodo["inherited_assets"]
            ),
            "changed_path_readback_performed": changed is not None,
            "changed_path_readback_pass": changed is None or changed["status"] == "PASS",
        },
    }
    sanitized(receipt)
    return receipt


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        receipt = run(args)
        write_json_atomic(args.output, receipt)
    except VerificationError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": args.output.name,
                "current_release_assets": receipt["local_release_asset_count"],
                "zenodo_record_files": receipt["zenodo"]["file_count"],
                "changed_paths": (
                    receipt["changed_path_readback"]["changed_path_count"]
                    if receipt["changed_path_readback"] is not None
                    else 0
                ),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
