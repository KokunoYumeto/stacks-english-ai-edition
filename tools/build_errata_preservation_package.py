#!/usr/bin/env python3
"""Build a deterministic, path-sanitized errata preservation package.

The release directory follows the six-asset R25 layout: README.md,
RELEASE.json, SHA256SUMS.txt, and deterministic source, PDF, and validation
ZIP archives.  The source ZIP is a commit-bound projection of ``git archive``:
the live local account token is replaced in textual members, every replacement
is bound by an embedded manifest, and every other source member remains
byte-identical.  The other ZIPs use fixed metadata, ordering, and compression
settings.  Every archive is reopened and its member identities are checked
before any output is staged.

Only basenames, repository-relative archive member names, public identifiers,
byte counts, and cryptographic hashes enter generated public metadata.  Local
input and output paths are deliberately never serialized.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence
import zipfile


PROJECT_SLUG = "unofficial-ai-integrated-stacks-project"
PROJECT_TITLE = "Unofficial AI-Integrated Stacks Project"
PROJECT_URL = (
    "https://github.com/KokunoYumeto/"
    "unofficial-ai-integrated-stacks-project"
)
ZENODO_CONCEPT_DOI = "10.5281/zenodo.22135180"
LICENSE_ID = "gfdl-1.2-only"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ZIP_COMPRESSION_LEVEL = 9
HASH_CHUNK_SIZE = 1024 * 1024
EXPECTED_PDF_COUNT = 25
SOURCE_REDACTION_MANIFEST = "SOURCE_PRIVACY_REDACTION_MANIFEST.json"
ACCOUNT_REDACTION_REPLACEMENT = b"[LOCAL_ACCOUNT_REDACTED]"

# A preservation package may be cut from a commit later than the commit used
# for the fixed-point build, because validation and release receipts follow the
# build. Such descendants are safe only when the intervening changes cannot
# alter a TeX build. Keep this list deliberately narrow and fail closed for
# every other path.
NON_BUILD_RELEVANT_POST_BUILD_PATHS = frozenset(
    {
        "README.md",
        "STATUS.md",
        "VALIDATION.md",
        "ROADMAP.md",
        "PROVENANCE.md",
        "ai-integrated/README.md",
        "validation/README.md",
        "tools/build_errata_preservation_package.py",
    }
)
NON_BUILD_RELEVANT_POST_BUILD_PREFIXES = ("validation/",)

SAFE_LABEL_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
HEX_SHA_RE = re.compile(r"[0-9A-Fa-f]{7,64}\Z")
FULL_SHA_RE = re.compile(r"[0-9A-Fa-f]{40}|[0-9A-Fa-f]{64}\Z")
WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    rb"(?i)(?<![A-Za-z0-9])(?:[A-Z]:[\\/]|\\\\[A-Za-z0-9._-]+[\\/])"
)
PRIVATE_POSIX_PATH_RE = re.compile(
    rb"(?i)(?<![A-Za-z0-9])/(?:Users|home|root|tmp|private|mnt|Volumes)"
    rb"(?:/|\Z)"
)
TEXT_SUFFIXES = frozenset(
    {
        "",
        ".aux",
        ".bib",
        ".blg",
        ".cfg",
        ".cls",
        ".csv",
        ".json",
        ".jsonl",
        ".log",
        ".md",
        ".out",
        ".py",
        ".rst",
        ".tex",
        ".toml",
        ".tsv",
        ".txt",
        ".yaml",
        ".yml",
    }
)


class PackageError(RuntimeError):
    """A deterministic validation or safe-output boundary failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(HASH_CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError as exc:
        raise PackageError(f"cannot read input file {path.name!r}") from exc
    return digest.hexdigest().upper()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_identity(path: Path, *, name: str | None = None) -> dict[str, Any]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise PackageError(f"cannot inspect file {path.name!r}") from exc
    return {
        "name": name if name is not None else path.name,
        "bytes": size,
        "sha256": sha256_file(path),
    }


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    ).encode("utf-8")


def canonical_member_digest(members: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        f"{item['sha256']}|{item['bytes']}|{item['name']}"
        for item in sorted(members, key=lambda value: str(value["name"]))
    ]
    return sha256_bytes((("\n".join(lines)) + "\n").encode("utf-8"))


def local_account_token() -> bytes | None:
    """Return the home-directory leaf for leak detection, never serialization."""

    try:
        token = Path.home().name.strip()
    except (OSError, RuntimeError):
        return None
    if len(token) < 3 or token.casefold() in {
        "admin",
        "administrator",
        "home",
        "root",
        "runner",
        "user",
        "users",
    }:
        return None
    return token.encode("utf-8", errors="ignore").lower() or None


def redact_account_token(data: bytes, account_token: bytes) -> tuple[bytes, int]:
    """Replace every case-insensitive account-token occurrence deterministically."""

    if not account_token:
        raise PackageError("local account token is unavailable")
    lowered = data.lower()
    cursor = 0
    pieces: list[bytes] = []
    replacements = 0
    while True:
        index = lowered.find(account_token, cursor)
        if index < 0:
            pieces.append(data[cursor:])
            break
        pieces.append(data[cursor:index])
        pieces.append(ACCOUNT_REDACTION_REPLACEMENT)
        cursor = index + len(account_token)
        replacements += 1
    return b"".join(pieces), replacements


def account_token_variants(account_token: bytes | None) -> tuple[bytes, ...]:
    if not account_token:
        return ()
    variants = [account_token]
    try:
        decoded = account_token.decode("utf-8")
    except UnicodeDecodeError:
        return tuple(variants)
    for encoding in ("utf-16-le", "utf-16-be"):
        candidate = decoded.encode(encoding)
        if candidate not in variants:
            variants.append(candidate)
    return tuple(variants)


def account_token_occurs(data: bytes, account_token: bytes | None) -> bool:
    lowered = data.lower()
    return any(variant in lowered for variant in account_token_variants(account_token))


def git_tree_modes(repository: Path, commit: str) -> dict[str, str]:
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                os.fspath(repository),
                "ls-tree",
                "-r",
                "-z",
                commit,
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise PackageError("git is unavailable") from exc
    if completed.returncode:
        raise PackageError("could not enumerate the bound Git tree")
    modes: dict[str, str] = {}
    for record in (item for item in completed.stdout.split(b"\x00") if item):
        try:
            metadata, encoded_path = record.split(b"\t", 1)
            mode, object_type, _object_id = metadata.decode("ascii").split(" ", 2)
            resolved_path = encoded_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise PackageError("Git tree entry metadata is malformed") from exc
        if object_type != "blob" or mode not in {"100644", "100755", "120000"}:
            raise PackageError("Git tree contains an unsupported source entry")
        if resolved_path in modes:
            raise PackageError("Git tree contains a duplicate source path")
        modes[resolved_path] = mode
    if not modes:
        raise PackageError("bound Git tree is empty")
    return modes


def validate_redactable_source_text(
    info: zipfile.ZipInfo,
    data: bytes,
    *,
    git_mode: str,
) -> None:
    mode = (info.external_attr >> 16) & 0xFFFF
    if git_mode not in {"100644", "100755"} or (
        mode and not stat.S_ISREG(mode)
    ):
        raise PackageError(
            f"non-regular source member {info.filename!r} contains the local "
            "account token"
        )
    if b"\x00" in data:
        raise PackageError(
            f"binary source member {info.filename!r} contains the local account token"
        )
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise PackageError(
            f"non-UTF-8 source member {info.filename!r} contains the local "
            "account token"
        ) from exc


def strip_zip64_extra(extra: bytes) -> bytes:
    """Remove only ZIP64 size metadata after a member payload length changes."""

    cursor = 0
    pieces: list[bytes] = []
    while cursor < len(extra):
        if cursor + 4 > len(extra):
            raise PackageError("source ZIP contains malformed extra-field metadata")
        field_id = int.from_bytes(extra[cursor : cursor + 2], "little")
        field_size = int.from_bytes(extra[cursor + 2 : cursor + 4], "little")
        end = cursor + 4 + field_size
        if end > len(extra):
            raise PackageError("source ZIP contains malformed extra-field metadata")
        if field_id != 0x0001:
            pieces.append(extra[cursor:end])
        cursor = end
    return b"".join(pieces)


def assert_no_local_path_bytes(
    data: bytes,
    *,
    public_name: str,
    account_token: bytes | None,
) -> None:
    if WINDOWS_ABSOLUTE_PATH_RE.search(data) or PRIVATE_POSIX_PATH_RE.search(data):
        raise PackageError(
            f"public text {public_name!r} contains a local absolute path"
        )
    if account_token_occurs(data, account_token):
        raise PackageError(
            f"public text {public_name!r} contains a local account name"
        )


def assert_no_local_account_bytes(
    data: bytes,
    *,
    public_name: str,
    account_token: bytes | None,
) -> None:
    """Reject the live account name while allowing already-redacted provenance."""

    if account_token_occurs(data, account_token):
        raise PackageError(
            f"public text {public_name!r} contains a local account name"
        )


def is_public_text_member(name: str) -> bool:
    normalized = name[:-1] if name.endswith("/") else name
    return PurePosixPath(normalized).suffix.lower() in TEXT_SUFFIXES


def safe_member_name(name: str, *, directory_allowed: bool) -> None:
    if not name or "\\" in name or "\x00" in name:
        raise PackageError("archive contains an invalid member name")
    if any(ord(character) < 32 for character in name):
        raise PackageError("archive contains a control character in a member name")
    is_directory = name.endswith("/")
    normalized = name[:-1] if is_directory else name
    if is_directory and not directory_allowed:
        raise PackageError("archive contains an unexpected directory member")
    if not normalized:
        raise PackageError("archive contains an empty member name")
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise PackageError("archive contains an unsafe member name")
    if ":" in path.parts[0]:
        raise PackageError("archive contains a drive-qualified member name")


def git_output(repository: Path, *arguments: str) -> str:
    command = ["git", "-C", os.fspath(repository), *arguments]
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        raise PackageError("git is unavailable") from exc
    if completed.returncode:
        raise PackageError(f"git {arguments[0]} failed")
    return completed.stdout.strip()


def resolve_commit(repository: Path, requested: str) -> tuple[str, str, str]:
    if not HEX_SHA_RE.fullmatch(requested):
        raise PackageError("source commit must be a hexadecimal Git object ID")
    commit = git_output(repository, "rev-parse", "--verify", f"{requested}^{{commit}}")
    if not FULL_SHA_RE.fullmatch(commit):
        raise PackageError("git returned an invalid source commit identity")
    if not commit.lower().startswith(requested.lower()):
        raise PackageError("resolved source commit does not match the requested ID")
    tree = git_output(repository, "rev-parse", "--verify", f"{commit}^{{tree}}")
    if not FULL_SHA_RE.fullmatch(tree):
        raise PackageError("git returned an invalid source tree identity")
    epoch_text = git_output(repository, "show", "-s", "--format=%ct", commit)
    try:
        epoch = int(epoch_text)
    except ValueError as exc:
        raise PackageError("git returned an invalid source commit time") from exc
    created_utc = (
        dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    return commit.lower(), tree.lower(), created_utc


def validate_release_source_binding(
    repository: Path,
    *,
    release_commit: str,
    release_tree: str,
    build_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind a later release commit to the exact source used by the PDF build."""

    source = build_receipt.get("source")
    if not isinstance(source, Mapping):
        raise PackageError("build receipt lacks a source identity")
    requested_build_commit = source.get("commit")
    requested_build_tree = source.get("tree")
    if not isinstance(requested_build_commit, str) or not FULL_SHA_RE.fullmatch(
        requested_build_commit
    ):
        raise PackageError("build receipt has an invalid source commit")
    if not isinstance(requested_build_tree, str) or not FULL_SHA_RE.fullmatch(
        requested_build_tree
    ):
        raise PackageError("build receipt has an invalid source tree")

    build_commit, build_tree, _ = resolve_commit(
        repository, requested_build_commit
    )
    if build_tree.lower() != requested_build_tree.lower():
        raise PackageError("build receipt source tree does not match Git")

    merge_base = git_output(
        repository, "merge-base", build_commit, release_commit
    )
    if merge_base.lower() != build_commit.lower():
        raise PackageError(
            "release commit is not a descendant of the build source commit"
        )

    changed_output = git_output(
        repository,
        "diff",
        "--name-only",
        "--diff-filter=ACDMRTUXB",
        f"{build_commit}..{release_commit}",
        "--",
    )
    changed_paths = [
        line.replace("\\", "/")
        for line in changed_output.splitlines()
        if line.strip()
    ]
    disallowed = [
        path
        for path in changed_paths
        if path not in NON_BUILD_RELEVANT_POST_BUILD_PATHS
        and not path.startswith(NON_BUILD_RELEVANT_POST_BUILD_PREFIXES)
    ]
    if disallowed:
        preview = ", ".join(disallowed[:5])
        raise PackageError(
            "release commit changes build-relevant paths after the fixed-point "
            f"build: {preview}"
        )

    return {
        "status": "PASS",
        "build_commit": build_commit,
        "build_tree": build_tree,
        "release_commit": release_commit,
        "release_tree": release_tree,
        "release_descends_from_build": True,
        "intervening_changed_path_count": len(changed_paths),
        "intervening_changed_paths": changed_paths,
        "build_relevant_intervening_changes": 0,
    }


def normalize_created_utc(value: str) -> str:
    candidate = value.strip()
    try:
        parsed = dt.datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PackageError("--created-utc must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise PackageError("--created-utc must include a UTC offset")
    return (
        parsed.astimezone(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def build_git_archive(
    repository: Path,
    commit: str,
    prefix: str,
    output: Path,
) -> None:
    if output.exists():
        raise PackageError("source archive output already exists")
    command = [
        "git",
        "-C",
        os.fspath(repository),
        "archive",
        "--format=zip",
        f"--prefix={prefix}",
        f"--output={output}",
        commit,
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        raise PackageError("git is unavailable") from exc
    if completed.returncode or not output.is_file():
        raise PackageError("git archive failed")


def projected_zip_info(
    *,
    name: str,
    source: zipfile.ZipInfo | None = None,
    directory: bool = False,
    payload_changed: bool = False,
    git_mode: str | None = None,
) -> zipfile.ZipInfo:
    date_time = source.date_time if source is not None else ZIP_TIMESTAMP
    info = zipfile.ZipInfo(name, date_time=date_time)
    info.create_system = 3
    if source is not None:
        info.create_version = source.create_version
        info.extract_version = source.extract_version
        info.reserved = source.reserved
        info.volume = source.volume
    info.compress_type = (
        source.compress_type
        if source is not None
        else (zipfile.ZIP_STORED if directory else zipfile.ZIP_DEFLATED)
    )
    if directory:
        public_mode = 0o40755
    elif git_mode is None:
        public_mode = 0o100644
    elif git_mode in {"100644", "100755", "120000"}:
        public_mode = int(git_mode, 8)
    else:
        raise PackageError("source member has an unsupported Git mode")
    info.external_attr = public_mode << 16
    info.internal_attr = source.internal_attr if source is not None else 0
    info.extra = (
        strip_zip64_extra(source.extra)
        if source is not None and payload_changed
        else (source.extra if source is not None else b"")
    )
    info.comment = source.comment if source is not None else b""
    if hasattr(info, "compress_level"):
        info.compress_level = ZIP_COMPRESSION_LEVEL
    else:  # Python 3.11 and earlier use the private storage name.
        info._compresslevel = ZIP_COMPRESSION_LEVEL
    return info


def member_contains_account_token(
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    account_token: bytes,
) -> bool:
    tail = b""
    variants = account_token_variants(account_token)
    tail_length = max(max((len(item) for item in variants), default=1) - 1, 0)
    with archive.open(info, mode="r") as handle:
        for chunk in iter(lambda: handle.read(HASH_CHUNK_SIZE), b""):
            scan = tail + chunk
            if any(variant in scan.lower() for variant in variants):
                return True
            tail = scan[-tail_length:] if tail_length else b""
    return False


def build_sanitized_git_archive(
    repository: Path,
    commit: str,
    tree: str,
    prefix: str,
    output: Path,
    *,
    account_token: bytes | None,
) -> tuple[dict[str, Any], dict[str, Mapping[str, Any]], dict[str, Any]]:
    """Build a complete deterministic source projection with declared redactions."""

    if account_token is None:
        raise PackageError(
            "cannot derive a local account token for fail-closed source sanitization"
        )
    if output.exists():
        raise PackageError("source archive output already exists")
    manifest_name = f"{prefix}{SOURCE_REDACTION_MANIFEST}"
    safe_member_name(manifest_name, directory_allowed=False)
    raw_output = output.with_name(f".{output.name}.git-archive")
    if raw_output.exists():
        raise PackageError("private git-archive scratch output already exists")

    transformed: dict[str, bytes] = {}
    redactions: list[dict[str, Any]] = []
    try:
        build_git_archive(repository, commit, prefix, raw_output)
        raw_identity = file_identity(raw_output, name="private-git-archive.zip")
        raw_check = inspect_zip(raw_output, required_prefix=prefix)
        tree_modes = git_tree_modes(repository, commit)
        expected_files: dict[str, Mapping[str, Any]] = {
            str(item["name"]): item for item in raw_check["members"]
        }
        archive_modes: dict[str, str] = {}
        for item in raw_check["members"]:
            archive_name = str(item["name"])
            relative_name = archive_name[len(prefix) :]
            if not relative_name or archive_name != f"{prefix}{relative_name}":
                raise PackageError("source member is outside the declared prefix")
            mode = tree_modes.get(relative_name)
            if mode is None:
                raise PackageError("source member is absent from the bound Git tree")
            archive_modes[archive_name] = mode

        with zipfile.ZipFile(raw_output, mode="r") as source_archive:
            assert_no_local_account_bytes(
                source_archive.comment,
                public_name="source ZIP archive comment",
                account_token=account_token,
            )
            infos = source_archive.infolist()
            names = [info.filename for info in infos]
            if manifest_name.casefold() in {name.casefold() for name in names}:
                raise PackageError("source tree collides with the redaction manifest")
            for info in infos:
                for metadata_name, metadata in (
                    ("member name", info.filename.encode("utf-8")),
                    ("member comment", info.comment),
                    ("member extra field", info.extra),
                ):
                    assert_no_local_account_bytes(
                        metadata,
                        public_name=f"source ZIP {metadata_name}",
                        account_token=account_token,
                    )
                if info.is_dir() or not member_contains_account_token(
                    source_archive, info, account_token
                ):
                    continue
                original = source_archive.read(info)
                validate_redactable_source_text(
                    info,
                    original,
                    git_mode=archive_modes[info.filename],
                )
                if any(
                    variant in original.lower()
                    for variant in account_token_variants(account_token)[1:]
                ):
                    raise PackageError(
                        f"encoded account token in source member {info.filename!r} "
                        "cannot be safely redacted"
                    )
                public, count = redact_account_token(original, account_token)
                if count <= 0 or account_token_occurs(public, account_token):
                    raise PackageError("source-member account redaction failed")
                transformed[info.filename] = public
                public_identity = {
                    "name": info.filename,
                    "bytes": len(public),
                    "sha256": sha256_bytes(public),
                }
                expected_files[info.filename] = public_identity
                redactions.append(
                    {
                        "name": info.filename,
                        "occurrences": count,
                        "original_bytes": len(original),
                        "original_sha256": sha256_bytes(original),
                        "public_bytes": len(public),
                        "public_sha256": public_identity["sha256"],
                    }
                )

            redactions.sort(key=lambda item: str(item["name"]))
            projection_manifest = {
                "schema": "unofficial-ai-integrated-stacks-source-projection/v1",
                "source": {"commit": commit, "tree": tree},
                "archive_prefix": prefix,
                "policy": (
                    "Complete commit-bound git-archive projection. The live local "
                    "account token is replaced by [LOCAL_ACCOUNT_REDACTED] in strict "
                    "UTF-8 regular-file members; names, metadata, binary members, "
                    "and alternate encodings must contain zero occurrences."
                ),
                "private_git_archive": {
                    "bytes": raw_identity["bytes"],
                    "sha256": raw_identity["sha256"],
                    "entry_count": raw_check["entry_count"],
                    "file_count": raw_check["file_count"],
                    "member_tuple_set_sha256": raw_check[
                        "member_tuple_set_sha256"
                    ],
                },
                "public_projection": {
                    "added_manifest_member": manifest_name,
                    "redacted_member_count": len(redactions),
                    "replacement_count": sum(
                        int(item["occurrences"]) for item in redactions
                    ),
                    "unchanged_file_count": raw_check["file_count"]
                    - len(redactions),
                },
                "redactions": redactions,
                "checks": {
                    "source_commit_and_tree_bound": True,
                    "source_member_order_preserved": True,
                    "source_member_timestamps_preserved": True,
                    "source_member_modes_reconstructed_from_git_tree": True,
                    "member_names_changed": 0,
                    "binary_members_redacted": 0,
                    "account_token_value_recorded": False,
                    "all_changes_declared": True,
                },
            }
            manifest_data = json_bytes(projection_manifest)
            assert_no_local_path_bytes(
                manifest_data,
                public_name=SOURCE_REDACTION_MANIFEST,
                account_token=account_token,
            )
            expected_files[manifest_name] = {
                "name": manifest_name,
                "bytes": len(manifest_data),
                "sha256": sha256_bytes(manifest_data),
            }

            try:
                with zipfile.ZipFile(
                    output,
                    mode="x",
                    compression=zipfile.ZIP_DEFLATED,
                    compresslevel=ZIP_COMPRESSION_LEVEL,
                    allowZip64=True,
                    strict_timestamps=True,
                ) as public_archive:
                    public_archive.comment = source_archive.comment
                    for source_info in infos:
                        output_info = projected_zip_info(
                            name=source_info.filename,
                            source=source_info,
                            directory=source_info.is_dir(),
                            payload_changed=source_info.filename in transformed,
                            git_mode=(
                                None
                                if source_info.is_dir()
                                else archive_modes[source_info.filename]
                            ),
                        )
                        if source_info.is_dir():
                            public_archive.writestr(output_info, b"")
                            continue
                        member_data = transformed.get(source_info.filename)
                        if member_data is None:
                            member_data = source_archive.read(source_info)
                        public_archive.writestr(output_info, member_data)
                    manifest_info = projected_zip_info(
                        name=manifest_name,
                        directory=False,
                    )
                    public_archive.writestr(manifest_info, manifest_data)
            except (OSError, zipfile.BadZipFile) as exc:
                raise PackageError(
                    "could not create deterministic sanitized source ZIP"
                ) from exc

        source_check = inspect_zip(
            output,
            expected_files=expected_files,
            required_prefix=prefix,
            scan_public_text=True,
            allow_redacted_provenance_paths=True,
            account_token=account_token,
        )
        if source_check["entry_count"] != raw_check["entry_count"] + 1:
            raise PackageError("source projection has an unexpected entry count")
        with zipfile.ZipFile(raw_output, mode="r") as original_archive, zipfile.ZipFile(
            output, mode="r"
        ) as public_archive:
            if original_archive.comment != public_archive.comment:
                raise PackageError("source projection did not preserve archive metadata")
            original_infos = original_archive.infolist()
            public_infos = public_archive.infolist()
            if [item.filename for item in public_infos[:-1]] != [
                item.filename for item in original_infos
            ] or public_infos[-1].filename != manifest_name:
                raise PackageError("source projection did not preserve member order")
            for original_info, public_info in zip(original_infos, public_infos[:-1]):
                expected_extra = (
                    strip_zip64_extra(original_info.extra)
                    if original_info.filename in transformed
                    else original_info.extra
                )
                expected_mode = (
                    0o40755
                    if original_info.is_dir()
                    else int(archive_modes[original_info.filename], 8)
                )
                if (
                    public_info.create_system != 3
                    or public_info.external_attr != expected_mode << 16
                    or original_info.internal_attr != public_info.internal_attr
                    or original_info.date_time != public_info.date_time
                    or original_info.create_version != public_info.create_version
                    or original_info.extract_version != public_info.extract_version
                    or original_info.comment != public_info.comment
                    or expected_extra != public_info.extra
                ):
                    raise PackageError(
                        "source projection did not preserve declared source metadata"
                    )
        return projection_manifest, expected_files, source_check
    finally:
        try:
            raw_output.unlink(missing_ok=True)
        except OSError:
            pass


def deterministic_zip(
    output: Path,
    members: Sequence[tuple[str, Path]],
) -> None:
    if output.exists():
        raise PackageError("deterministic ZIP output already exists")
    ordered = sorted(members, key=lambda item: item[0])
    if len({name.casefold() for name, _ in ordered}) != len(ordered):
        raise PackageError("ZIP input member names are not unique")
    try:
        with zipfile.ZipFile(
            output,
            mode="x",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=ZIP_COMPRESSION_LEVEL,
            allowZip64=True,
            strict_timestamps=True,
        ) as archive:
            archive.comment = b""
            for member_name, source in ordered:
                safe_member_name(member_name, directory_allowed=False)
                info = zipfile.ZipInfo(member_name, date_time=ZIP_TIMESTAMP)
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                info.internal_attr = 0
                info.extra = b""
                info.comment = b""
                if hasattr(info, "compress_level"):
                    info.compress_level = ZIP_COMPRESSION_LEVEL
                else:  # Python 3.11 and earlier use the private storage name.
                    info._compresslevel = ZIP_COMPRESSION_LEVEL
                with source.open("rb") as source_handle, archive.open(
                    info, mode="w", force_zip64=True
                ) as member_handle:
                    shutil.copyfileobj(
                        source_handle,
                        member_handle,
                        length=HASH_CHUNK_SIZE,
                    )
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageError("could not create deterministic ZIP") from exc


def inspect_zip(
    path: Path,
    *,
    expected_files: Mapping[str, Mapping[str, Any]] | None = None,
    required_prefix: str | None = None,
    scan_public_text: bool = False,
    allow_redacted_provenance_paths: bool = False,
    account_token: bytes | None = None,
) -> dict[str, Any]:
    members: list[dict[str, Any]] = []
    try:
        with zipfile.ZipFile(path, mode="r") as archive:
            if scan_public_text:
                assert_no_local_account_bytes(
                    archive.comment,
                    public_name=f"archive {path.name!r} comment",
                    account_token=account_token,
                )
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)) or len(names) != len(
                {name.casefold() for name in names}
            ):
                raise PackageError(f"archive {path.name!r} has duplicate members")
            for info in infos:
                safe_member_name(info.filename, directory_allowed=True)
                if scan_public_text:
                    for metadata_name, metadata in (
                        ("member name", info.filename.encode("utf-8")),
                        ("member comment", info.comment),
                        ("member extra field", info.extra),
                    ):
                        assert_no_local_account_bytes(
                            metadata,
                            public_name=f"archive {metadata_name}",
                            account_token=account_token,
                        )
                    if not allow_redacted_provenance_paths:
                        assert_no_local_path_bytes(
                            info.filename.encode("utf-8"),
                            public_name="archive member name",
                            account_token=None,
                        )
                if required_prefix is not None and not info.filename.startswith(
                    required_prefix
                ):
                    raise PackageError(
                        f"archive {path.name!r} has a member outside its prefix"
                    )
                if info.flag_bits & 0x1:
                    raise PackageError(f"archive {path.name!r} has an encrypted member")
                if info.is_dir():
                    continue
                digest = hashlib.sha256()
                account_tail = b""
                path_tail = b""
                token_variants = account_token_variants(account_token)
                account_tail_length = max(
                    max((len(item) for item in token_variants), default=1) - 1,
                    0,
                )
                with archive.open(info, mode="r") as handle:
                    for chunk in iter(lambda: handle.read(HASH_CHUNK_SIZE), b""):
                        digest.update(chunk)
                        if scan_public_text:
                            account_scan = account_tail + chunk
                            assert_no_local_account_bytes(
                                account_scan,
                                public_name=info.filename,
                                account_token=account_token,
                            )
                            account_tail = (
                                account_scan[-account_tail_length:]
                                if account_tail_length
                                else b""
                            )
                            if (
                                is_public_text_member(info.filename)
                                and not allow_redacted_provenance_paths
                            ):
                                path_scan = path_tail + chunk
                                assert_no_local_path_bytes(
                                    path_scan,
                                    public_name=info.filename,
                                    account_token=None,
                                )
                                path_tail = path_scan[-512:]
                members.append(
                    {
                        "name": info.filename,
                        "bytes": info.file_size,
                        "sha256": digest.hexdigest().upper(),
                    }
                )
    except PackageError:
        raise
    except (OSError, EOFError, RuntimeError, zipfile.BadZipFile) as exc:
        raise PackageError(f"archive {path.name!r} failed reopen validation") from exc

    actual = {str(item["name"]): item for item in members}
    if expected_files is not None:
        if set(actual) != set(expected_files):
            raise PackageError(f"archive {path.name!r} has the wrong member listing")
        for name, expected in expected_files.items():
            observed = actual[name]
            if (
                int(observed["bytes"]) != int(expected["bytes"])
                or str(observed["sha256"]).upper()
                != str(expected["sha256"]).upper()
            ):
                raise PackageError(
                    f"archive {path.name!r} member {name!r} failed identity validation"
                )
    ordered = sorted(members, key=lambda item: str(item["name"]))
    return {
        "entry_count": len(infos),
        "file_count": len(ordered),
        "member_tuple_set_sha256": canonical_member_digest(ordered),
        "members": ordered,
    }


def load_json_receipt(
    path: Path,
    *,
    role: str,
    account_token: bytes | None,
) -> tuple[bytes, dict[str, Any]]:
    if not path.is_file():
        raise PackageError(f"{role} is missing")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise PackageError(f"{role} is unreadable") from exc
    assert_no_local_path_bytes(
        raw,
        public_name=path.name,
        account_token=account_token,
    )
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError(f"{role} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise PackageError(f"{role} must contain a JSON object")
    return raw, value


def validate_build_artifacts(
    build_receipt: Mapping[str, Any],
    build_output_root: Path,
) -> list[dict[str, Any]]:
    if build_receipt.get("status") != "PASS":
        raise PackageError("build receipt status is not PASS")
    raw_artifacts = build_receipt.get("artifacts")
    if not isinstance(raw_artifacts, list) or len(raw_artifacts) != EXPECTED_PDF_COUNT:
        raise PackageError(
            f"build receipt must describe exactly {EXPECTED_PDF_COUNT} PDF artifacts"
        )
    if not build_output_root.is_dir():
        raise PackageError("build-output root is missing")

    observed: list[dict[str, Any]] = []
    seen_stems: set[str] = set()
    for raw in raw_artifacts:
        if not isinstance(raw, dict):
            raise PackageError("build receipt has a malformed artifact entry")
        stem = raw.get("stem")
        expected_bytes = raw.get("bytes")
        expected_sha = raw.get("sha256")
        pages = raw.get("pages")
        if (
            not isinstance(stem, str)
            or not SAFE_LABEL_RE.fullmatch(stem)
            or stem in {".", ".."}
            or stem.casefold() in seen_stems
        ):
            raise PackageError("build receipt has an invalid or duplicate PDF stem")
        seen_stems.add(stem.casefold())
        if not isinstance(expected_bytes, int) or expected_bytes <= 0:
            raise PackageError(f"PDF artifact {stem!r} has an invalid byte count")
        if not isinstance(expected_sha, str) or not re.fullmatch(
            r"[0-9A-Fa-f]{64}", expected_sha
        ):
            raise PackageError(f"PDF artifact {stem!r} has an invalid SHA-256")
        if not isinstance(pages, int) or pages <= 0:
            raise PackageError(f"PDF artifact {stem!r} has an invalid page count")
        pdf = build_output_root / f"{stem}.pdf"
        if not pdf.is_file():
            raise PackageError(f"expected PDF {stem + '.pdf'!r} is missing")
        try:
            with pdf.open("rb") as handle:
                magic = handle.read(5)
            actual_bytes = pdf.stat().st_size
        except OSError as exc:
            raise PackageError(f"expected PDF {stem + '.pdf'!r} is unreadable") from exc
        if magic != b"%PDF-":
            raise PackageError(f"artifact {stem + '.pdf'!r} is not a PDF")
        actual_sha = sha256_file(pdf)
        if actual_bytes != expected_bytes or actual_sha != expected_sha.upper():
            raise PackageError(f"PDF artifact {stem + '.pdf'!r} does not match its receipt")
        observed.append(
            {
                "name": f"{stem}.pdf",
                "stem": stem,
                "pages": pages,
                "bytes": actual_bytes,
                "sha256": actual_sha,
                "source": pdf,
            }
        )

    direct_pdfs = {
        item.name.casefold()
        for item in build_output_root.glob("*.pdf")
        if item.is_file()
    }
    expected_names = {str(item["name"]).casefold() for item in observed}
    if direct_pdfs != expected_names:
        raise PackageError(
            "build-output root PDF listing does not exactly match the build receipt"
        )

    build = build_receipt.get("build")
    if isinstance(build, dict):
        chapter_count = build.get("chapter_count")
        if chapter_count is not None and chapter_count != EXPECTED_PDF_COUNT:
            raise PackageError("build receipt chapter count is inconsistent")
        tuple_lines = [
            "|".join(
                (
                    str(item["stem"]),
                    str(item["pages"]),
                    str(item["bytes"]),
                    str(item["sha256"]),
                )
            )
            for item in sorted(observed, key=lambda value: str(value["stem"]))
        ]
        tuple_digest = sha256_bytes(
            (("\n".join(tuple_lines)) + "\n").encode("utf-8")
        )
        recorded_digest = build.get("artifact_tuple_set_sha256")
        if recorded_digest is not None and str(recorded_digest).upper() != tuple_digest:
            raise PackageError("build receipt artifact tuple digest is inconsistent")
    return sorted(observed, key=lambda item: str(item["name"]))


def receipt_members(
    build_receipt_path: Path,
    validation_receipt_paths: Sequence[Path],
    *,
    account_token: bytes | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    paths = [build_receipt_path, *validation_receipt_paths]
    unique_paths: list[Path] = []
    resolved_seen: set[str] = set()
    for path in paths:
        try:
            resolved = os.path.normcase(os.fspath(path.resolve(strict=False)))
        except OSError as exc:
            raise PackageError("validation receipt path cannot be resolved") from exc
        if resolved in resolved_seen:
            continue
        resolved_seen.add(resolved)
        unique_paths.append(path)

    basename_seen: set[str] = set()
    loaded: list[dict[str, Any]] = []
    build_value: dict[str, Any] | None = None
    for index, path in enumerate(unique_paths):
        name = path.name
        safe_member_name(name, directory_allowed=False)
        if not name.lower().endswith(".json"):
            raise PackageError("validation receipts must use .json filenames")
        if name.casefold() in basename_seen:
            raise PackageError("validation receipt basenames must be unique")
        basename_seen.add(name.casefold())
        raw, value = load_json_receipt(
            path,
            role="build receipt" if index == 0 else "validation receipt",
            account_token=account_token,
        )
        identity = {
            "name": name,
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
            "source": path,
        }
        loaded.append(identity)
        if index == 0:
            build_value = value
    if build_value is None:
        raise PackageError("build receipt is required")
    return build_value, sorted(loaded, key=lambda item: str(item["name"]))


def build_readme(
    *,
    display_label: str,
    commit: str,
    tree: str,
    source_name: str,
    pdf_name: str,
    validation_name: str,
    artifacts: Sequence[Mapping[str, Any]],
    receipt_names: Sequence[str],
    official_baseline: str | None,
    source_redacted_members: int,
    source_redaction_count: int,
) -> bytes:
    pages = sum(int(item["pages"]) for item in artifacts)
    pdf_bytes = sum(int(item["bytes"]) for item in artifacts)
    baseline_text = (
        f"The official Stacks baseline recorded by the build is commit\n"
        f"`{official_baseline}`. "
        if official_baseline
        else "The source archive records the exact official Stacks baseline. "
    )
    receipts = ", ".join(f"`{name}`" for name in receipt_names)
    text = f"""# {PROJECT_TITLE} — {display_label} validated checkpoint

This preservation release captures the validated {display_label} fixed point of the
[{PROJECT_TITLE}]({PROJECT_URL}) at source commit `{commit}` (tree `{tree}`).

The project is an unofficial, AI-written integration built on the original
Stacks Project. It does not claim upstream endorsement, affiliation, review,
approval, or official Stacks tags for local additions.

## Validation

- {len(artifacts)} fixed-point chapter PDFs
- {pages:,} total pages
- {pdf_bytes:,} total PDF bytes
- every PDF byte count and SHA-256 matched the build receipt
- every ZIP was reopened and its complete listing and member hashes validated
- validation receipts preserved: {receipts}

The EGA integration program remains incomplete and resumes at EGA I section
6.4.1. This release does not claim complete EGA integration or machine-formal
verification.

## Files

- `{source_name}` — deterministic complete source projection of the bound Git
  commit; {source_redaction_count} live-account-token occurrence(s) in
  {source_redacted_members} strict-UTF-8 provenance member(s) were replaced,
  all changes are hash-bound in the embedded `{SOURCE_REDACTION_MANIFEST}`, and
  every unchanged source member remains byte-identical to `git archive`
- `{pdf_name}` — the 25 validated chapter PDFs
- `{validation_name}` — the supplied build and validation receipts
- `RELEASE.json` — machine-readable release and archive identities
- `SHA256SUMS.txt` — SHA-256 inventory for the other five release assets

## Provenance and license

{baseline_text}The integrated project and this preservation
release are distributed under GNU Free Documentation License 1.2 only; see
`COPYING` in the source archive. The historical-source Verdier contribution is
independently worded and claims neither an official Stacks tag nor upstream
endorsement.

Permanent preservation uses the existing Zenodo concept DOI
[{ZENODO_CONCEPT_DOI}](https://doi.org/{ZENODO_CONCEPT_DOI}).
"""
    return text.encode("utf-8")


def safe_mapping_value(mapping: Mapping[str, Any], *keys: str) -> Any:
    value: Any = mapping
    for key in keys:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def public_pdf_member(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "name": str(item["name"]),
        "pages": int(item["pages"]),
        "bytes": int(item["bytes"]),
        "sha256": str(item["sha256"]),
    }


def public_file_member(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "name": str(item["name"]),
        "bytes": int(item["bytes"]),
        "sha256": str(item["sha256"]),
    }


def prepare_release(
    *,
    label: str,
    display_label: str,
    release_id: str,
    created_utc: str,
    commit: str,
    tree: str,
    source_binding: Mapping[str, Any],
    build_receipt: Mapping[str, Any],
    build_receipt_identity: Mapping[str, Any],
    artifacts: Sequence[Mapping[str, Any]],
    receipt_identities: Sequence[Mapping[str, Any]],
    source_zip_identity: Mapping[str, Any],
    pdf_zip_identity: Mapping[str, Any],
    validation_zip_identity: Mapping[str, Any],
    readme_identity: Mapping[str, Any],
    source_check: Mapping[str, Any],
    source_projection: Mapping[str, Any],
    pdf_check: Mapping[str, Any],
    validation_check: Mapping[str, Any],
) -> dict[str, Any]:
    composition = build_receipt.get("composition")
    if not isinstance(composition, Mapping):
        composition = {}
    build = build_receipt.get("build")
    if not isinstance(build, Mapping):
        build = {}
    official_baseline = composition.get("authority_commit")
    integration: dict[str, Any] = {
        "overlay_or_version_label": label,
        "last_composed_errata": composition.get("last_admitted_overlay"),
        "registry_cutoff": composition.get("registry_cutoff_commit"),
        "registered_overlays": composition.get("registered_overlays"),
        "registered_stable_ids": composition.get("registered_stable_ids"),
        "affected_source_stems": composition.get("affected_source_stems"),
    }
    integration = {key: value for key, value in integration.items() if value is not None}
    pages = sum(int(item["pages"]) for item in artifacts)
    pdf_bytes = sum(int(item["bytes"]) for item in artifacts)
    return {
        "schema": "unofficial-ai-integrated-stacks-preservation-package/v2",
        "release": release_id,
        "created_utc": created_utc,
        "title": f"{PROJECT_TITLE} — validated {display_label} checkpoint",
        "source": {
            "repository": PROJECT_URL,
            "commit": commit,
            "tree": tree,
            **(
                {"official_stacks_baseline": official_baseline}
                if isinstance(official_baseline, str)
                else {}
            ),
            "license": LICENSE_ID,
        },
        "integration": integration,
        "validation": {
            "status": "PASS",
            "build_chapters": len(artifacts),
            "pages": pages,
            "pdf_bytes": pdf_bytes,
            "fixed_point_sweep": build.get("global_fixed_point_sweep"),
            "artifact_tuple_set_sha256": build.get(
                "artifact_tuple_set_sha256"
            ),
            "release_source_binding": dict(source_binding),
            "build_receipt": public_file_member(build_receipt_identity),
            "receipts": [public_file_member(item) for item in receipt_identities],
        },
        "archives": {
            "source": {
                "name": source_zip_identity["name"],
                "entry_count": source_check["entry_count"],
                "file_count": source_check["file_count"],
                "member_tuple_set_sha256": source_check[
                    "member_tuple_set_sha256"
                ],
                "reopen_and_listing": "PASS",
                "local_account_name_scan": "PASS",
                "provenance_path_policy": (
                    "complete commit-bound privacy-sanitized Git projection; "
                    "already-redacted path-shaped provenance strings may remain"
                ),
                "privacy_redaction_manifest": source_projection[
                    "public_projection"
                ]["added_manifest_member"],
                "redacted_member_count": source_projection["public_projection"][
                    "redacted_member_count"
                ],
                "replacement_count": source_projection["public_projection"][
                    "replacement_count"
                ],
                "private_git_archive_member_tuple_set_sha256": source_projection[
                    "private_git_archive"
                ]["member_tuple_set_sha256"],
                "unchanged_source_members_byte_identical": True,
            },
            "pdfs": {
                "name": pdf_zip_identity["name"],
                "member_count": pdf_check["file_count"],
                "member_tuple_set_sha256": pdf_check[
                    "member_tuple_set_sha256"
                ],
                "members": [public_pdf_member(item) for item in artifacts],
                "reopen_listing_and_member_hashes": "PASS",
            },
            "validation": {
                "name": validation_zip_identity["name"],
                "member_count": validation_check["file_count"],
                "member_tuple_set_sha256": validation_check[
                    "member_tuple_set_sha256"
                ],
                "members": [public_file_member(item) for item in receipt_identities],
                "reopen_listing_and_member_hashes": "PASS",
            },
        },
        "preservation": {
            "zenodo_concept_doi": ZENODO_CONCEPT_DOI,
            "license": LICENSE_ID,
            "nonendorsement": (
                "Unofficial independent work; no Stacks Project affiliation, "
                "review, approval, or endorsement is claimed."
            ),
        },
        "assets": [
            public_file_member(readme_identity),
            public_file_member(source_zip_identity),
            public_file_member(pdf_zip_identity),
            public_file_member(validation_zip_identity),
        ],
        "scope_note": (
            "EGA integration remains partial and resumes at EGA I section "
            "6.4.1; complete EGA integration and formal verification are not "
            "claimed."
        ),
    }


def write_new(path: Path, data: bytes, *, role: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
    except FileExistsError as exc:
        raise PackageError(f"{role} already exists") from exc
    except OSError as exc:
        raise PackageError(f"could not write {role}") from exc


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-commit",
        required=True,
        help="Git commit (full or unambiguous hexadecimal prefix) to archive",
    )
    parser.add_argument(
        "--version-label",
        "--label",
        "--overlay-label",
        dest="version_label",
        required=True,
        help="safe release/overlay label used in public names (for example r26)",
    )
    parser.add_argument(
        "--build-receipt",
        type=Path,
        required=True,
        help="fixed-point build receipt describing the 24 PDF identities",
    )
    parser.add_argument(
        "--validation-receipt",
        dest="validation_receipts",
        action="append",
        type=Path,
        default=[],
        help="additional JSON receipt to preserve; repeat for each receipt",
    )
    parser.add_argument(
        "--validation-receipts",
        dest="validation_receipts",
        action="extend",
        nargs="+",
        type=Path,
        help="one or more additional JSON receipts to preserve",
    )
    parser.add_argument(
        "--build-output-root",
        type=Path,
        required=True,
        help="directory whose top level contains exactly the 24 receipt-bound PDFs",
    )
    parser.add_argument(
        "--staging-dir",
        type=Path,
        required=True,
        help="new or empty directory that will receive the six release assets",
    )
    parser.add_argument(
        "--package-receipt",
        "--receipt",
        type=Path,
        help=(
            "sanitized package-build receipt path; defaults beside the staging "
            "directory"
        ),
    )
    parser.add_argument(
        "--receipt-in-staging",
        action="store_true",
        help=(
            "write PACKAGE_RECEIPT.json inside staging as non-release "
            "administrative evidence"
        ),
    )
    parser.add_argument(
        "--repository",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Git repository to archive (default: repository containing this tool)",
    )
    parser.add_argument(
        "--created-utc",
        help=(
            "deterministic ISO-8601 release time; defaults to the source commit "
            "time"
        ),
    )
    args = parser.parse_args(argv)
    if args.receipt_in_staging and args.package_receipt is not None:
        parser.error("--receipt-in-staging and --package-receipt are mutually exclusive")
    return args


def is_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except (OSError, ValueError):
        return False
    return True


def verify_checksum_inventory(
    data: bytes,
    expected: Sequence[Mapping[str, Any]],
) -> None:
    expected_lines = [
        f"{item['sha256']}  {item['name']}"
        for item in sorted(expected, key=lambda value: str(value["name"]))
    ]
    try:
        actual_lines = data.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise PackageError("SHA256SUMS.txt is not ASCII") from exc
    if actual_lines != expected_lines:
        raise PackageError("SHA256SUMS.txt failed inventory validation")


def run(args: argparse.Namespace) -> dict[str, Any]:
    label = args.version_label
    if not SAFE_LABEL_RE.fullmatch(label) or label in {".", ".."}:
        raise PackageError("version label contains unsafe characters")
    display_label = label.upper() if re.fullmatch(r"r\d+", label, re.I) else label
    repository = args.repository.resolve(strict=False)
    staging = args.staging_dir.resolve(strict=False)
    if staging == staging.parent:
        raise PackageError("staging directory cannot be a filesystem root")
    if staging.exists():
        if not staging.is_dir():
            raise PackageError("staging destination is not a directory")
        try:
            if any(staging.iterdir()):
                raise PackageError("staging directory must be empty")
        except OSError as exc:
            raise PackageError("staging directory is not readable") from exc

    if args.receipt_in_staging:
        receipt_path = staging / "PACKAGE_RECEIPT.json"
    elif args.package_receipt is not None:
        receipt_path = args.package_receipt.resolve(strict=False)
    else:
        receipt_path = staging.with_name(f"{staging.name}-package-receipt.json")
    receipt_inside_staging = is_within(receipt_path, staging)
    if receipt_inside_staging and receipt_path.parent != staging:
        raise PackageError("an in-staging package receipt must be a direct child")
    if receipt_path.exists():
        raise PackageError("package receipt destination already exists")

    account_token = local_account_token()
    commit, tree, commit_time = resolve_commit(repository, args.source_commit)
    created_utc = (
        normalize_created_utc(args.created_utc)
        if args.created_utc is not None
        else commit_time
    )
    release_id = f"{display_label}-{created_utc[:10]}"

    build_receipt, receipt_inputs = receipt_members(
        args.build_receipt,
        args.validation_receipts,
        account_token=account_token,
    )
    artifacts = validate_build_artifacts(
        build_receipt,
        args.build_output_root,
    )
    source_binding = validate_release_source_binding(
        repository,
        release_commit=commit,
        release_tree=tree,
        build_receipt=build_receipt,
    )
    build_receipt_identity = next(
        item
        for item in receipt_inputs
        if item["source"].resolve(strict=False)
        == args.build_receipt.resolve(strict=False)
    )

    short_commit = commit[:8]
    source_name = f"{PROJECT_SLUG}-{label}-source-{short_commit}.zip"
    pdf_name = f"{PROJECT_SLUG}-{label}-pdfs.zip"
    validation_name = f"{PROJECT_SLUG}-{label}-validation.zip"
    release_asset_names = {
        "README.md",
        "RELEASE.json",
        "SHA256SUMS.txt",
        source_name,
        pdf_name,
        validation_name,
    }
    if len({name.casefold() for name in release_asset_names}) != 6:
        raise PackageError("release asset names collide")
    if receipt_inside_staging and receipt_path.name.casefold() in {
        name.casefold() for name in release_asset_names
    }:
        raise PackageError("package receipt name collides with a release asset")

    staging.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(prefix=".errata-package-", dir=staging.parent)
    )
    moved: list[Path] = []
    staging_created = False
    external_receipt_written = False
    try:
        source_zip = temporary / source_name
        pdf_zip = temporary / pdf_name
        validation_zip = temporary / validation_name
        source_projection, source_expectations, source_check = (
            build_sanitized_git_archive(
                repository,
                commit,
                tree,
                f"{PROJECT_SLUG}-{label}/",
                source_zip,
                account_token=account_token,
            )
        )
        deterministic_zip(
            pdf_zip,
            [(str(item["name"]), item["source"]) for item in artifacts],
        )
        deterministic_zip(
            validation_zip,
            [(str(item["name"]), item["source"]) for item in receipt_inputs],
        )

        source_check = inspect_zip(
            source_zip,
            expected_files=source_expectations,
            required_prefix=f"{PROJECT_SLUG}-{label}/",
            scan_public_text=True,
            allow_redacted_provenance_paths=True,
            account_token=account_token,
        )
        artifact_expectations = {
            str(item["name"]): item for item in artifacts
        }
        pdf_check = inspect_zip(pdf_zip, expected_files=artifact_expectations)
        receipt_expectations = {
            str(item["name"]): item for item in receipt_inputs
        }
        validation_check = inspect_zip(
            validation_zip,
            expected_files=receipt_expectations,
            scan_public_text=True,
            account_token=account_token,
        )

        source_identity = file_identity(source_zip)
        pdf_identity = file_identity(pdf_zip)
        validation_identity = file_identity(validation_zip)

        official_baseline = safe_mapping_value(
            build_receipt, "composition", "authority_commit"
        )
        if not isinstance(official_baseline, str):
            official_baseline = None
        readme_data = build_readme(
            display_label=display_label,
            commit=commit,
            tree=tree,
            source_name=source_name,
            pdf_name=pdf_name,
            validation_name=validation_name,
            artifacts=artifacts,
            receipt_names=[str(item["name"]) for item in receipt_inputs],
            official_baseline=official_baseline,
            source_redacted_members=source_projection["public_projection"][
                "redacted_member_count"
            ],
            source_redaction_count=source_projection["public_projection"][
                "replacement_count"
            ],
        )
        assert_no_local_path_bytes(
            readme_data,
            public_name="README.md",
            account_token=account_token,
        )
        readme_path = temporary / "README.md"
        write_new(readme_path, readme_data, role="README.md")
        readme_identity = file_identity(readme_path)

        release_value = prepare_release(
            label=label,
            display_label=display_label,
            release_id=release_id,
            created_utc=created_utc,
            commit=commit,
            tree=tree,
            source_binding=source_binding,
            build_receipt=build_receipt,
            build_receipt_identity=build_receipt_identity,
            artifacts=artifacts,
            receipt_identities=receipt_inputs,
            source_zip_identity=source_identity,
            pdf_zip_identity=pdf_identity,
            validation_zip_identity=validation_identity,
            readme_identity=readme_identity,
            source_check=source_check,
            source_projection=source_projection,
            pdf_check=pdf_check,
            validation_check=validation_check,
        )
        release_data = json_bytes(release_value)
        assert_no_local_path_bytes(
            release_data,
            public_name="RELEASE.json",
            account_token=account_token,
        )
        release_path = temporary / "RELEASE.json"
        write_new(release_path, release_data, role="RELEASE.json")
        release_identity = file_identity(release_path)

        checksum_inputs = [
            readme_identity,
            release_identity,
            pdf_identity,
            source_identity,
            validation_identity,
        ]
        checksum_lines = [
            f"{item['sha256']}  {item['name']}"
            for item in sorted(
                checksum_inputs, key=lambda value: str(value["name"])
            )
        ]
        checksum_data = (("\n".join(checksum_lines)) + "\n").encode("ascii")
        verify_checksum_inventory(checksum_data, checksum_inputs)
        checksum_path = temporary / "SHA256SUMS.txt"
        write_new(checksum_path, checksum_data, role="SHA256SUMS.txt")
        checksum_identity = file_identity(checksum_path)

        release_assets = sorted(
            [
                readme_identity,
                release_identity,
                checksum_identity,
                pdf_identity,
                source_identity,
                validation_identity,
            ],
            key=lambda value: str(value["name"]),
        )
        package_receipt_value = {
            "schema": (
                "unofficial-ai-integrated-stacks-preservation-package-build/v2"
            ),
            "status": "PASS",
            "created_utc": created_utc,
            "release": release_id,
            "source": {"commit": commit, "tree": tree},
            "release_source_binding": source_binding,
            "release_assets": [
                public_file_member(item) for item in release_assets
            ],
            "archives": {
                "source": {
                    "name": source_name,
                    "entry_count": source_check["entry_count"],
                    "file_count": source_check["file_count"],
                    "member_tuple_set_sha256": source_check[
                        "member_tuple_set_sha256"
                    ],
                    "privacy_redaction_manifest": source_projection[
                        "public_projection"
                    ]["added_manifest_member"],
                    "redacted_member_count": source_projection[
                        "public_projection"
                    ]["redacted_member_count"],
                    "replacement_count": source_projection["public_projection"][
                        "replacement_count"
                    ],
                    "private_git_archive": source_projection[
                        "private_git_archive"
                    ],
                    "redactions": source_projection["redactions"],
                },
                "pdfs": {
                    "name": pdf_name,
                    "member_count": pdf_check["file_count"],
                    "member_tuple_set_sha256": pdf_check[
                        "member_tuple_set_sha256"
                    ],
                    "members": [public_pdf_member(item) for item in artifacts],
                },
                "validation": {
                    "name": validation_name,
                    "member_count": validation_check["file_count"],
                    "member_tuple_set_sha256": validation_check[
                        "member_tuple_set_sha256"
                    ],
                    "members": [
                        public_file_member(item) for item in receipt_inputs
                    ],
                },
            },
            "checks": {
                "release_asset_count": 6,
                "source_projection_reopen_and_listing": "PASS",
                "pdf_listing_and_member_hashes": "PASS",
                "validation_listing_and_member_hashes": "PASS",
                "checksum_inventory": "PASS",
                "release_metadata_and_validation_local_absolute_paths_absent": True,
                "public_text_local_account_names_absent": True,
                "source_archive_local_account_names_absent": True,
                "source_archive_is_commit_bound_sanitized_projection": True,
                "source_archive_differs_only_by_declared_redactions_and_manifest": True,
                "source_archive_unchanged_members_byte_identical": True,
                "source_archive_account_redacted_provenance_paths_allowed": True,
                "package_receipt_is_release_asset": False,
                "release_commit_descends_from_build_source": True,
                "build_relevant_intervening_changes": 0,
            },
        }
        package_receipt_data = json_bytes(package_receipt_value)
        assert_no_local_path_bytes(
            package_receipt_data,
            public_name="package receipt",
            account_token=account_token,
        )
        if receipt_inside_staging:
            write_new(
                temporary / receipt_path.name,
                package_receipt_data,
                role="package receipt",
            )

        staged_files = [temporary / name for name in sorted(release_asset_names)]
        if receipt_inside_staging:
            staged_files.append(temporary / receipt_path.name)
        if not staging.exists():
            staging.mkdir(parents=True)
            staging_created = True
        for source in staged_files:
            destination = staging / source.name
            if destination.exists():
                raise PackageError("staging destination changed during packaging")
            os.replace(source, destination)
            moved.append(destination)

        for identity in release_assets:
            final_path = staging / str(identity["name"])
            final_identity = file_identity(final_path)
            if (
                final_identity["bytes"] != identity["bytes"]
                or final_identity["sha256"] != identity["sha256"]
            ):
                raise PackageError("a staged release asset failed final identity check")
        verify_checksum_inventory(
            (staging / "SHA256SUMS.txt").read_bytes(), checksum_inputs
        )

        if not receipt_inside_staging:
            write_new(receipt_path, package_receipt_data, role="package receipt")
            external_receipt_written = True

        return {
            "status": "PASS",
            "release": release_id,
            "source_commit": commit,
            "source_tree": tree,
            "release_asset_count": 6,
            "pdf_members": pdf_check["file_count"],
            "validation_members": validation_check["file_count"],
            "source_archive_entries": source_check["entry_count"],
            "package_receipt": (
                "inside staging" if receipt_inside_staging else "outside staging"
            ),
        }
    except Exception:
        if external_receipt_written:
            try:
                receipt_path.unlink(missing_ok=True)
            except OSError:
                pass
        for path in reversed(moved):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        if staging_created:
            try:
                staging.rmdir()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = run(args)
    except PackageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
