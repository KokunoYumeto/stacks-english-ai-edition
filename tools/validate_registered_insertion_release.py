#!/usr/bin/env python3
"""Validate the v4 registered-insertion composition and its release evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote
from urllib.request import Request, urlopen


SCHEMA = "unofficial-ai-integrated-stacks-composition/v4"
MODE = "registered insertion rebased through unique unchanged context"
OVERLAY_ID = "stacks-verdier-a04446e-1-2-13-r1"
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
SOURCE_UNION_COMMIT = "ad58625f60e6816905ff217d21d91b07b2722fcf"
EGA_EXPORT_COMMIT = "91df7f1c96bd4973264c29b0e121253a05d1d361"
PREVIOUS_MAIN_COMMIT = "522951e96168ebc13dfeeca7ce60032f5bcd8938"
PREVIOUS_MAIN_TREE = "d71776e121ee8db7fca362050eff41ff835ef1b1"
PREVIOUS_REGISTRY_COMMIT = "ea6ed0f430e8adfbd500aab71927e99f7e0f324f"
PREVIOUS_REGISTRY_TREE = "44268da85d61b9e26ccbf1b99422d87d86bc0d74"
PREVIOUS_LAST_OVERLAY = "stacks-errata-a04446e-r21"
CANDIDATE_COMMIT = "ae3a1b76e557a528ad346ac336124ff113d9022f"
CANDIDATE_TREE = "888fab43da3790dfcaf8d792e2b248661514991c"
CANDIDATE_SUBTREE = "94738667238babcdbd3488c76ea13529fbf24fc4"
MANIFEST_SHA256 = "1FDC18620B255DDFD59CB967C82AF9F1FA3E75D6ACE748808BF3F18A91913CB7"
WRITER_TASK = "019fca5a-c80e-7890-a46b-4948ff443e6d"
LEASE_ID = "stacks-lease-000026-verdier"
LEASE_EVENT_ID = "lease-event-000048"
LEASE_PREDECESSOR_ID = "lease-event-000047"
ADMISSION_UTC = "2026-08-26T03:13:02Z"
NAMESPACE = "commons/stacks/verdier"
RIGHTS_STATE = (
    "Historical-source evidence is limited to locators, hashes, and independent "
    "paraphrase. No verbatim source prose is included, no source-work license is "
    "asserted or granted by this candidate, and no upstream content is relicensed. "
    "The proposed Stacks payload is independently written, subject to GFDL "
    "compatibility at composition, and is not reviewed, approved, affiliated with, "
    "or endorsed by the Stacks Project."
)
COMPOSITION_PATH = Path("validation/composition-current.json")
BUILD_PATH = Path(
    "validation/stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json"
)
VISUAL_PATH = Path(
    "validation/stacks-verdier-a04446e-1-2-13-r1-visual-qa-2026-08-26.json"
)
SECOND_BUILD_PATH = Path(
    "validation/stacks-verdier-a04446e-1-2-13-r1-reproducibility-second-2026-08-26.json"
)
REPRO_PATH = Path(
    "validation/stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json"
)
RELEASE_PATH = Path(
    "validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json"
)
EXPECTED_STEMS = (
    "sets",
    "categories",
    "topology",
    "sheaves",
    "sites",
    "algebra",
    "brauer",
    "derived",
    "simplicial",
    "homology",
    "more-algebra",
    "smoothing",
    "schemes",
    "properties",
    "morphisms",
    "more-morphisms",
    "crystalline",
    "spaces-cohomology",
    "stacks-limits",
    "injectives",
    "gaga",
    "moduli",
)
FIXED_POINT_SUFFIXES = (
    ".aux",
    ".bbl",
    ".idx",
    ".ind",
    ".lof",
    ".lot",
    ".out",
    ".toc",
    ".pdf",
)
DIAGNOSTIC_KEYS = (
    "fatal_markers",
    "missing_glyph_markers",
    "undefined_reference_markers",
    "external_reference_markers",
    "undefined_citation_markers",
    "multiply_defined_markers",
    "rerun_required_markers",
    "destination_warning_markers",
)
PUBLIC_MARKDOWN = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "PROVENANCE.md",
    "VALIDATION.md",
    "CONTRIBUTING.md",
    "ai-integrated/README.md",
    "validation/README.md",
)
CURRENT_REQUIRED_PATHS = (
    "chapters.tex",
    "COPYING",
    "fac/STATUS.md",
    "tohoku_r71/STATUS.md",
    "gaga_r3/STATUS.md",
    "gaga.tex",
    "fga/README.md",
    "fga/audit.json",
    "ega/README.md",
    "ega/smap.csv",
    "ai-integrated/registry/overlays.json",
    "ai-integrated/registry/leases.json",
    "ai-integrated/registry/locales.json",
    "ai-integrated/upstream/stacks.lock.json",
    "ai-integrated/registry/releases.json",
    "validation/unification-release-2026-08-25.json",
    "validation/errata-r18-r19-release-2026-08-25.json",
    "validation/unified-fixed-point-2026-08-25-r19.json",
    "validation/visual-qa-r21.json",
    "validation/reproducibility-r21.json",
    "validation/reproducibility-second-r21.json",
    "tools/compose_overlay_projection.py",
    "tools/verify_overlay_projection.py",
    "tools/compose_registered_insertion.py",
    "tools/build_fixed_point.py",
    "tools/validate_unified_repository.py",
    "tools/validate_registered_insertion_release.py",
    COMPOSITION_PATH.as_posix(),
    "tags/tags",
)


class ValidationError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git(root: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValidationError(detail or f"git {' '.join(args)} failed")
    return completed.stdout


def git_text(
    root: Path, *args: str, input_bytes: bytes | None = None
) -> str:
    return git(root, *args, input_bytes=input_bytes).decode(
        "utf-8", errors="strict"
    ).strip()


def git_optional(root: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def commit_bytes(root: Path, revision: str, path: str) -> bytes:
    return git(root, "show", f"{revision}:{path}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_commit(root: Path, value: object, label: str) -> str:
    require(
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
        and git_optional(root, "cat-file", "-e", f"{value}^{{commit}}") is not None,
        f"missing or invalid {label} commit: {value!r}",
    )
    return value


def require_tree(root: Path, commit: str, value: object, label: str) -> str:
    require(
        isinstance(value, str) and git_text(root, "rev-parse", f"{commit}^{{tree}}") == value,
        f"{label} tree mismatch",
    )
    return value


def require_parent(root: Path, commit: str, parent: str, label: str) -> None:
    parents = git_text(root, "rev-list", "--parents", "-n", "1", commit).split()
    require(parents == [commit, parent], f"{label} is not a single-parent child of {parent}")


def require_ancestor(root: Path, ancestor: str, descendant: str, label: str) -> None:
    completed = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(completed.returncode == 0, f"ancestry check failed: {label}")


def require_linear_suffix(root: Path, ancestor: str, descendant: str, label: str) -> None:
    rows = git_text(root, "rev-list", "--parents", f"{ancestor}..{descendant}").splitlines()
    for row in rows:
        require(len(row.split()) == 2, f"{label} contains a merge commit: {row.split()[0]}")


def validate_historical_r21_snapshot(root: Path) -> None:
    """Re-run the frozen, already-published v3 gate at its exact public head."""
    temporary = Path(tempfile.mkdtemp(prefix="stacks-r21-validation-"))
    added = False
    try:
        completed = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "worktree",
                "add",
                "--detach",
                "--quiet",
                str(temporary),
                PREVIOUS_MAIN_COMMIT,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=60,
        )
        require(
            completed.returncode == 0,
            "could not materialize the frozen R21 validation snapshot: "
            + completed.stderr.strip(),
        )
        added = True
        historical = subprocess.run(
            [
                sys.executable,
                str(temporary / "tools/validate_unified_repository.py"),
            ],
            cwd=temporary,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=180,
        )
        require(
            historical.returncode == 0
            and "Unified repository validation: PASS" in historical.stdout,
            "frozen R21 historical validation failed: "
            + (historical.stderr.strip() or historical.stdout.strip()),
        )
    finally:
        if added:
            cleanup = subprocess.run(
                ["git", "-C", str(root), "worktree", "remove", "--force", str(temporary)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=60,
            )
            require(
                cleanup.returncode == 0,
                "could not remove historical validation worktree: "
                + cleanup.stderr.strip(),
            )
        elif temporary.exists():
            shutil.rmtree(temporary)


def validate_current_surface(root: Path, pre_publication: bool) -> None:
    for ancestor, label in (
        (AUTHORITY_COMMIT, "pinned upstream"),
        (SOURCE_UNION_COMMIT, "FAC/Tohoku/GAGA/FGA source union"),
        (EGA_EXPORT_COMMIT, "EGA export"),
    ):
        require_ancestor(root, ancestor, "HEAD", label)

    required = set(CURRENT_REQUIRED_PATHS + PUBLIC_MARKDOWN)
    required.update(
        (
            BUILD_PATH.as_posix(),
            VISUAL_PATH.as_posix(),
            SECOND_BUILD_PATH.as_posix(),
            REPRO_PATH.as_posix(),
        )
    )
    if not pre_publication:
        required.add(RELEASE_PATH.as_posix())
    committed: dict[str, bytes] = {
        path: require_clean_committed_path(root, path) for path in sorted(required)
    }
    for path in (
        "fga/audit.json",
        "ai-integrated/registry/leases.json",
        "ai-integrated/registry/locales.json",
        "ai-integrated/registry/overlays.json",
        "ai-integrated/registry/releases.json",
        "ai-integrated/upstream/stacks.lock.json",
        "validation/unification-release-2026-08-25.json",
        "validation/errata-r18-r19-release-2026-08-25.json",
        BUILD_PATH.as_posix(),
        VISUAL_PATH.as_posix(),
        SECOND_BUILD_PATH.as_posix(),
        REPRO_PATH.as_posix(),
    ):
        try:
            parsed = json.loads(committed[path].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError(f"invalid current JSON artifact {path}: {exc}") from exc
        require(isinstance(parsed, (dict, list)), f"invalid JSON root type: {path}")

    root_entries = git_text(root, "ls-tree", "--name-only", "HEAD").splitlines()
    marker_paths = list(PUBLIC_MARKDOWN) + [
        path for path in root_entries if path.endswith(".tex")
    ]
    for path in marker_paths:
        raw = committed.get(path) or commit_bytes(root, "HEAD", path)
        text = raw.decode("utf-8", errors="replace")
        require(
            "<<<<<<< " not in text and ">>>>>>> " not in text,
            f"unresolved merge marker: {path}",
        )

    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in PUBLIC_MARKDOWN:
        text = committed[path].decode("utf-8", errors="strict")
        parent = posixpath.dirname(path)
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            normalized = posixpath.normpath(posixpath.join(parent, target))
            require(
                normalized not in (".", "..")
                and not normalized.startswith("../")
                and git_optional(root, "cat-file", "-e", f"HEAD:{normalized}") is not None,
                f"broken link in {path}: {raw_target}",
            )

    changed_root_tex = [
        path
        for path in git_text(
            root,
            "diff",
            "--name-only",
            f"{PREVIOUS_MAIN_COMMIT}..HEAD",
            "--",
            ":(top,glob)*.tex",
        ).splitlines()
        if path
    ]
    require(
        changed_root_tex == ["derived.tex"],
        f"Verdier release changed unexpected root TeX sources: {changed_root_tex}",
    )

    def root_label_counts(revision: str) -> Counter[str]:
        labels: Counter[str] = Counter()
        for path in git_text(root, "ls-tree", "--name-only", revision).splitlines():
            if not path.endswith(".tex"):
                continue
            text = commit_bytes(root, revision, path).decode("utf-8", errors="replace")
            labels.update(re.findall(r"\\label\{([^}]+)\}", text))
        return labels

    historical_labels = root_label_counts(PREVIOUS_MAIN_COMMIT)
    current_labels = root_label_counts("HEAD")
    proposed_label = "lemma-functorial-triangles-decomposable"
    expected_labels = historical_labels.copy()
    expected_labels[proposed_label] += 1
    require(
        current_labels == expected_labels,
        "current permanent-label inventory differs from R21 by more than the one Verdier label",
    )
    require(
        git_text(root, "rev-parse", f"{PREVIOUS_MAIN_COMMIT}:tags/tags")
        == git_text(root, "rev-parse", "HEAD:tags/tags")
        and proposed_label.encode("utf-8") not in committed["tags/tags"],
        "Verdier release altered the official tag table or claimed an official tag",
    )
    preserved_paths = (
        "fac",
        "tohoku_r71",
        "gaga_r3",
        "fga",
        "ega",
        "ai-integrated/candidates/commons/stacks/errata",
        "ai-integrated/upstream",
        "ai-integrated/registry/locales.json",
        "ai-integrated/registry/releases.json",
        "tags/tags",
        "validation/unification-release-2026-08-25.json",
        "validation/errata-r18-r19-release-2026-08-25.json",
        "validation/unified-fixed-point-2026-08-25-r19.json",
        "validation/visual-qa-r21.json",
        "validation/reproducibility-r21.json",
        "validation/reproducibility-second-r21.json",
    )
    for path in preserved_paths:
        require(
            git_text(root, "rev-parse", f"{PREVIOUS_MAIN_COMMIT}:{path}")
            == git_text(root, "rev-parse", f"HEAD:{path}"),
            f"historical R21 evidence changed under the Verdier release: {path}",
        )


def require_clean_committed_path(root: Path, path: str) -> bytes:
    require(Path(path).as_posix() == path and ".." not in Path(path).parts, f"unsafe path: {path}")
    require(git_optional(root, "ls-files", "--error-unmatch", "--", path) == path, f"untracked path: {path}")
    for cached in (False, True):
        command = ["git", "-C", str(root), "diff", "--quiet"]
        if cached:
            command.append("--cached")
        command.extend(["--", path])
        completed = subprocess.run(command, check=False)
        require(completed.returncode == 0, f"dirty committed path: {path}")
    # Git's clean-path checks above are authoritative across checkout newline
    # policies. Parse the committed blob so CRLF conversion cannot make the
    # validator platform-dependent.
    return commit_bytes(root, "HEAD", path)


def load_committed_json(root: Path, path: Path, label: str) -> tuple[dict, bytes]:
    raw = require_clean_committed_path(root, path.as_posix())
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid {label}: {exc}") from exc
    require(isinstance(value, dict), f"{label} is not a JSON object")
    return value, raw


def file_identity(root: Path, revision: str, path: str) -> dict[str, object]:
    data = commit_bytes(root, revision, path)
    return {
        "bytes": len(data),
        "sha256": sha256(data),
        "git_blob": git_text(root, "rev-parse", f"{revision}:{path}"),
    }


def check_identity(observed: dict[str, object], expected: dict, label: str) -> None:
    for key in ("bytes", "sha256", "git_blob"):
        require(observed.get(key) == expected.get(key), f"{label} {key} mismatch")


def run_bound_command(
    root: Path,
    binding: object,
    expected_path: str,
    expected_arguments: tuple[str, ...],
    expected_schema: str,
) -> dict:
    require(isinstance(binding, dict) and binding.get("status") == "PASS", "invalid verifier binding")
    command = binding.get("command")
    path = binding.get("path")
    require(
        isinstance(command, str)
        and path == expected_path
        and not Path(expected_path).is_absolute()
        and ".." not in Path(expected_path).parts,
        "incomplete or unsafe verifier binding",
    )
    tokens = shlex.split(command, posix=True)
    require(
        tuple(tokens) == ("python", expected_path, *expected_arguments),
        "verifier executable or argument vector mismatch",
    )
    require_clean_committed_path(root, expected_path)
    completed = subprocess.run(
        [sys.executable, str(root / expected_path), *expected_arguments],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    require(
        completed.returncode == 0,
        f"receipt-bound verifier failed: {completed.stderr.strip() or completed.stdout.strip()}",
    )
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"verifier returned invalid JSON: {exc}") from exc
    require(
        isinstance(report, dict)
        and report.get("schema") == expected_schema
        and report.get("status") == "PASS",
        "verifier report schema or pass state mismatch",
    )
    return report


def validate_composition(root: Path) -> tuple[dict, bytes, dict[str, object]]:
    receipt, receipt_bytes = load_committed_json(root, COMPOSITION_PATH, "composition receipt")
    require(receipt.get("schema") == SCHEMA and receipt.get("status") == "PASS", "invalid v4 composition receipt")
    authority = receipt.get("authority")
    previous = receipt.get("previous_cutoff")
    registry_state = receipt.get("registry")
    composition = receipt.get("composition")
    require(all(isinstance(item, dict) for item in (authority, previous, registry_state, composition)), "composition receipt sections are incomplete")
    assert isinstance(authority, dict)
    assert isinstance(previous, dict)
    assert isinstance(registry_state, dict)
    assert isinstance(composition, dict)
    require(composition.get("mode") == MODE, "unexpected composition mode")

    head = git_text(root, "rev-parse", "HEAD")
    authority_commit = require_commit(root, authority.get("commit"), "authority")
    require_tree(root, authority_commit, authority.get("tree"), "authority")
    require(
        authority_commit == AUTHORITY_COMMIT and authority.get("tree") == AUTHORITY_TREE,
        "pinned upstream authority changed",
    )
    previous_main = require_commit(root, previous.get("public_main_head"), "previous public main")
    require_tree(root, previous_main, previous.get("public_main_tree"), "previous public main")
    previous_registry = require_commit(root, previous.get("registry_commit"), "previous registry")
    require_tree(root, previous_registry, previous.get("registry_tree"), "previous registry")
    require(
        previous_main == PREVIOUS_MAIN_COMMIT
        and previous.get("public_main_tree") == PREVIOUS_MAIN_TREE
        and previous_registry == PREVIOUS_REGISTRY_COMMIT
        and previous.get("registry_tree") == PREVIOUS_REGISTRY_TREE
        and previous.get("last_admitted_overlay") == PREVIOUS_LAST_OVERLAY,
        "previous R21 public-main or registry cutoff identity mismatch",
    )
    cutoff = require_commit(root, registry_state.get("cutoff_commit"), "registry cutoff")
    require_tree(root, cutoff, registry_state.get("cutoff_tree"), "registry cutoff")
    import_commit = require_commit(root, registry_state.get("linear_import_commit"), "registry import")
    require_tree(root, import_commit, registry_state.get("linear_import_tree"), "registry import")
    source_commit = require_commit(root, composition.get("source_commit"), "composition source")
    require_tree(root, source_commit, composition.get("source_tree"), "composition source")
    require(composition.get("base_commit") == import_commit, "composition base/import commit mismatch")
    require(composition.get("base_tree") == registry_state.get("linear_import_tree"), "composition base/import tree mismatch")
    require_parent(root, import_commit, previous_main, "registry import")
    require_parent(root, source_commit, import_commit, "composition source")
    require_ancestor(root, authority_commit, import_commit, "authority to registry import")
    for ancestor, label in ((previous_main, "previous main"), (import_commit, "import"), (source_commit, "source")):
        require_ancestor(root, ancestor, head, label + " to HEAD")
    require_linear_suffix(root, source_commit, head, "protected publication suffix")

    registry_paths = {
        "overlays": "ai-integrated/registry/overlays.json",
        "leases": "ai-integrated/registry/leases.json",
    }
    registry_values: dict[str, dict] = {}
    for kind, canonical_path in registry_paths.items():
        require(registry_state.get(f"{kind}_path") == canonical_path, f"{kind} registry path mismatch")
        expected = {
            "bytes": registry_state.get(f"{kind}_bytes"),
            "sha256": registry_state.get(f"{kind}_sha256"),
            "git_blob": registry_state.get(f"{kind}_git_blob"),
        }
        for revision, path in (("HEAD", canonical_path), (import_commit, canonical_path), (cutoff, f"registry/{kind}.json")):
            check_identity(file_identity(root, revision, path), expected, f"{kind} registry at {revision}")
        registry_values[kind] = json.loads(commit_bytes(root, "HEAD", canonical_path).decode("utf-8"))

    entries = registry_values["overlays"].get("registered_entries")
    require(isinstance(entries, list) and entries, "overlay registry lacks entries")
    stable_ids: list[str] = []
    for entry in entries:
        require(isinstance(entry, dict), "invalid overlay registry entry")
        raw = entry.get("stable_ids")
        ids = raw if isinstance(raw, list) else raw.split() if isinstance(raw, str) else []
        require(ids and all(isinstance(item, str) and item for item in ids), "invalid stable-ID inventory")
        stable_ids.extend(ids)
    require(len(entries) == registry_state.get("registered_overlays") == 22, "registered overlay count mismatch")
    require(len(stable_ids) == registry_state.get("registered_stable_ids") == 559, "registered stable-ID count mismatch")
    require(len(set(stable_ids)) == len(stable_ids), "registered stable IDs are not unique")
    require(entries[-1].get("id") == registry_state.get("last_admitted_overlay") == OVERLAY_ID, "registry cutoff overlay mismatch")

    previous_overlay_registry = json.loads(
        commit_bytes(root, previous_registry, "registry/overlays.json").decode("utf-8")
    )
    previous_entries = previous_overlay_registry["registered_entries"]
    require(entries[:-1] == previous_entries, "overlay registry did not append exactly one entry")
    lease_events = registry_values["leases"].get("events")
    require(isinstance(lease_events, list) and lease_events, "lease registry lacks events")
    previous_lease_registry = json.loads(
        commit_bytes(root, previous_registry, "registry/leases.json").decode("utf-8")
    )
    previous_lease_events = previous_lease_registry.get("events")
    require(
        isinstance(previous_lease_events, list)
        and lease_events[:-1] == previous_lease_events,
        "lease registry did not append exactly one event",
    )
    final_lease = lease_events[-1]
    require(
        isinstance(final_lease, dict)
        and final_lease.get("event_id") == LEASE_EVENT_ID
        and final_lease.get("event") == "released"
        and final_lease.get("lease_id") == LEASE_ID
        and final_lease.get("namespace") == NAMESPACE
        and final_lease.get("candidate_path") == f"candidates/{NAMESPACE}"
        and final_lease.get("writer_task") == WRITER_TASK
        and final_lease.get("upstream_commit") == AUTHORITY_COMMIT
        and final_lease.get("upstream_tree") == AUTHORITY_TREE
        and final_lease.get("issued_at_utc") == ADMISSION_UTC
        and final_lease.get("state") == "released",
        "Verdier lease lifecycle is not released",
    )
    require(
        final_lease.get("supersedes_event_id") == LEASE_PREDECESSOR_ID
        and final_lease.get("writer_contract") == "candidates/CONTRACT.md",
        "Verdier release event does not supersede the issued lease exactly",
    )

    new_overlays = receipt.get("new_overlays")
    require(isinstance(new_overlays, list) and len(new_overlays) == 1, "expected one new overlay")
    overlay = new_overlays[0]
    require(isinstance(overlay, dict) and overlay.get("id") == OVERLAY_ID, "new overlay identity mismatch")
    require(overlay.get("topology") == "independent_candidate_direct_admission", "new overlay topology mismatch")
    require(overlay.get("stable_ids") == 12 and overlay.get("operations") == 1, "new overlay counts mismatch")
    require(entries[-1].get("manifest_sha256", "").upper() == overlay.get("manifest_sha256"), "registry/transition manifest mismatch")
    candidate = require_commit(root, overlay.get("candidate_commit"), "candidate")
    require_tree(root, candidate, overlay.get("candidate_tree"), "candidate")
    require(
        candidate == CANDIDATE_COMMIT
        and overlay.get("candidate_tree") == CANDIDATE_TREE
        and overlay.get("candidate_subtree") == CANDIDATE_SUBTREE
        and overlay.get("manifest_sha256") == MANIFEST_SHA256,
        "final reviewed candidate identity mismatch",
    )
    admission = require_commit(root, overlay.get("admission_commit"), "admission")
    require_tree(root, admission, overlay.get("admission_tree"), "admission")
    require(admission == cutoff, "admission/cutoff commit mismatch")
    require(overlay.get("admission_parent") == previous_registry, "recorded admission parent mismatch")
    require_parent(root, admission, previous_registry, "direct admission")
    admitted_entry = entries[-1]
    namespace = admitted_entry.get("namespace")
    require(isinstance(namespace, str) and namespace == NAMESPACE, "Verdier namespace mismatch")
    require(
        admitted_entry.get("id") == OVERLAY_ID
        and admitted_entry.get("writer") == WRITER_TASK
        and admitted_entry.get("source_commit") == AUTHORITY_COMMIT
        and admitted_entry.get("source_tree") == AUTHORITY_TREE
        and admitted_entry.get("manifest_sha256") == MANIFEST_SHA256
        and admitted_entry.get("rights_state") == RIGHTS_STATE
        and admitted_entry.get("review_receipt")
        == f"candidates/{NAMESPACE}/replay/independent-review.json",
        "Verdier admission record identity, rights, or review binding mismatch",
    )
    require(
        admitted_entry.get("admitted_at_utc") == ADMISSION_UTC,
        "Verdier admission timestamp mismatch",
    )
    candidate_path = f"candidates/{namespace}"
    imported_path = f"ai-integrated/{candidate_path}"
    subtree = git_text(root, "rev-parse", f"{candidate}:{candidate_path}")
    require(subtree == overlay.get("candidate_subtree"), "candidate subtree identity mismatch")
    require(git_text(root, "rev-parse", f"{admission}:{candidate_path}") == subtree, "admission changed candidate subtree")
    require(git_text(root, "rev-parse", f"{import_commit}:{imported_path}") == subtree, "main import changed candidate subtree")
    require(git_text(root, "rev-parse", f"HEAD:{imported_path}") == subtree, "HEAD changed candidate subtree")

    manifest_path = f"{candidate_path}/candidate.manifest.json"
    manifest_bytes = commit_bytes(root, candidate, manifest_path)
    require(sha256(manifest_bytes) == overlay.get("manifest_sha256"), "candidate manifest hash mismatch")
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    require(
        manifest.get("schema") == "mathematics-commons-stacks-candidate-manifest/v1"
        and manifest.get("candidate_id") == OVERLAY_ID
        and manifest.get("namespace") == NAMESPACE
        and manifest.get("lease_id") == LEASE_ID
        and manifest.get("writer_task") == WRITER_TASK
        and manifest.get("upstream")
        == {
            "commit": AUTHORITY_COMMIT,
            "lock": "upstream/stacks.lock.json",
            "tree": AUTHORITY_TREE,
        }
        and manifest.get("review_state") == "performed"
        and manifest.get("independent_replay") == "passed"
        and manifest.get("unresolved_defects") == [],
        "candidate manifest identity or lifecycle mismatch",
    )
    raw_builds = manifest.get("builds")
    require(isinstance(raw_builds, list), "candidate manifest lacks build bindings")
    builds: dict[str, str] = {}
    for item in raw_builds:
        require(
            isinstance(item, dict)
            and isinstance(item.get("path"), str)
            and isinstance(item.get("sha256"), str)
            and len(item["sha256"]) == 64
            and all(character in "0123456789ABCDEFabcdef" for character in item["sha256"]),
            "candidate manifest contains an invalid build binding",
        )
        path = item["path"]
        require(
            not Path(path).is_absolute()
            and ".." not in Path(path).parts
            and Path(path).as_posix() == path
            and path not in builds,
            f"candidate manifest contains an unsafe or duplicate build binding: {path!r}",
        )
        builds[path] = item["sha256"].upper()
    references = dict(builds)
    for field in (
        "decision_ledger",
        "formula_diagram_inventory",
        "rejection_ledger",
        "source_authorities",
        "source_map",
        "stable_unit_manifest",
    ):
        raw_binding = manifest.get(field)
        bindings = raw_binding if isinstance(raw_binding, list) else [raw_binding]
        require(
            bindings
            and all(
                isinstance(binding, dict)
                and isinstance(binding.get("path"), str)
                and isinstance(binding.get("sha256"), str)
                for binding in bindings
            ),
            f"candidate manifest lacks the {field} binding",
        )
        for binding in bindings:
            path = binding["path"]
            digest = binding["sha256"].upper()
            require(
                not Path(path).is_absolute()
                and ".." not in Path(path).parts
                and Path(path).as_posix() == path
                and path not in references
                and len(digest) == 64
                and all(character in "0123456789ABCDEF" for character in digest),
                f"candidate manifest has an unsafe, duplicate, or invalid {field} binding",
            )
            references[path] = digest
    require(len(references) == 27, "candidate manifest does not bind exactly 27 references")
    for path, digest in references.items():
        require(
            sha256(commit_bytes(root, candidate, f"{candidate_path}/{path}")) == digest,
            f"candidate manifest reference hash mismatch: {path}",
        )
    candidate_files = git_text(
        root, "ls-tree", "-r", "--name-only", f"{candidate}:{candidate_path}"
    ).splitlines()
    expected_candidate_files = sorted(
        ["candidate.manifest.json"] + list(references)
    )
    require(
        sorted(candidate_files) == expected_candidate_files,
        "candidate subtree is not closed by the manifest's 27 references",
    )
    for key, field in (
        ("payload_path", "payload_sha256"),
        ("composition_path", "composition_sha256"),
        ("review_receipt_path", "review_receipt_sha256"),
    ):
        relative = overlay.get(key)
        expected_sha = overlay.get(field)
        require(isinstance(relative, str) and builds.get(relative) == expected_sha, f"manifest {key} binding mismatch")
        require(sha256(commit_bytes(root, candidate, f"{candidate_path}/{relative}")) == expected_sha, f"candidate {key} hash mismatch")
    review = json.loads(commit_bytes(root, candidate, f"{candidate_path}/{overlay['review_receipt_path']}").decode("utf-8"))
    review_checks = review.get("check_results")
    require(
        review.get("schema") == "mathematics-commons-stacks-independent-review/v1"
        and review.get("candidate_id") == OVERLAY_ID
        and review.get("status") == "PASS"
        and review.get("passed") is True
        and review.get("review_state") == "performed"
        and review.get("independent_replay") == "passed"
        and review.get("unresolved_defects") == []
        and isinstance(review_checks, list)
        and len(review_checks) == 17
        and all(isinstance(row, dict) and row.get("passed") is True for row in review_checks),
        "independent replay is not exactly passing all 17 checks",
    )

    source_rows = [
        json.loads(line)
        for line in commit_bytes(root, candidate, f"{candidate_path}/source-map.jsonl").decode("utf-8").splitlines()
        if line.strip()
    ]
    require([row.get("unit_id") for row in source_rows] == entries[-1].get("stable_ids"), "candidate source-map/registry IDs mismatch")
    stable_units = json.loads(
        commit_bytes(root, candidate, f"{candidate_path}/stable-units.json").decode("utf-8")
    )
    unit_rows = stable_units.get("units")
    require(
        stable_units.get("candidate_id") == OVERLAY_ID
        and stable_units.get("unit_count") == 12
        and isinstance(unit_rows, list)
        and [row.get("id") for row in unit_rows if isinstance(row, dict)]
        == admitted_entry.get("stable_ids")
        and len(source_rows) == 12,
        "candidate 12-unit manifest/source-map/registry join mismatch",
    )

    changed = git_text(root, "diff", "--name-only", f"{import_commit}..{source_commit}").splitlines()
    require(changed == ["derived.tex"], f"composition changed-path inventory mismatch: {changed}")
    affected = composition.get("affected_sources")
    require(isinstance(affected, dict) and list(affected) == ["derived.tex"], "affected-source inventory mismatch")
    evidence = affected["derived.tex"]
    check_identity(file_identity(root, previous_main, "derived.tex"), {
        "bytes": evidence.get("before_bytes"),
        "sha256": evidence.get("before_sha256"),
        "git_blob": evidence.get("before_git_blob"),
    }, "previous derived source")
    check_identity(file_identity(root, import_commit, "derived.tex"), {
        "bytes": evidence.get("before_bytes"),
        "sha256": evidence.get("before_sha256"),
        "git_blob": evidence.get("before_git_blob"),
    }, "composition base source")
    check_identity(file_identity(root, authority_commit, "derived.tex"), {
        "bytes": evidence.get("authority_bytes"),
        "sha256": evidence.get("authority_sha256"),
        "git_blob": evidence.get("authority_git_blob"),
    }, "authority derived source")
    check_identity(file_identity(root, source_commit, "derived.tex"), {
        "bytes": evidence.get("composed_bytes"),
        "sha256": evidence.get("composed_sha256"),
        "git_blob": evidence.get("composed_git_blob"),
    }, "composed derived source")
    require(
        evidence.get("before_bytes") == 449715
        and evidence.get("before_sha256")
        == "66D17FBE6743002D29A78543E46122CD3ED34AA5A5574B14718C1189ACEB456F"
        and evidence.get("context_bytes") == 803
        and evidence.get("context_sha256")
        == "C51A1835EF6B490131498A4F71195A75913DCE687C97309351098F98A9CF7ADC"
        and evidence.get("rebased_byte_offset") == 27437
        and evidence.get("payload_bytes") == 2339
        and evidence.get("payload_sha256")
        == "FCF51C107444D5ED31C32ABC73F19ECC05AAFA5C3FD078CF29B5A743C2A414B1"
        and evidence.get("composed_bytes") == 452054
        and evidence.get("composed_sha256")
        == "8B389993D3B364A926C7DCD7AD598E5B8245D8E92BCC5A23646069F9AD617860",
        "registered insertion preimage/context/payload/postimage identity mismatch",
    )
    require(evidence.get("committed_matches_composition") is True and evidence.get("prefix_unchanged") is True and evidence.get("suffix_unchanged") is True, "composition closure flags are not passing")
    require(composition.get("existing_errata_v2_operations") == 591, "historical errata operation count changed")
    require(composition.get("new_operations") == composition.get("registered_insertion_operations") == 1, "registered insertion operation count mismatch")

    errata_report = run_bound_command(
        root,
        receipt.get("errata_projection_verifier"),
        "tools/compose_overlay_projection.py",
        (
            "--existing-rounds", "18", "19",
            "--target-rounds", "18", "19", "20", "21",
            "--base-revision", "e3b28d7d7068eb45d3348a57e201c49044826e86",
            "--check-revision", "ef467614041d569e56a6c1758b8fe74b51d99f4a",
        ),
        "unofficial-ai-integrated-stacks-overlay-composition/v1",
    )
    require(
        errata_report.get("base_revision") == "e3b28d7d7068eb45d3348a57e201c49044826e86"
        and errata_report.get("check_revision") == "ef467614041d569e56a6c1758b8fe74b51d99f4a"
        and errata_report.get("existing_rounds") == [18, 19]
        and errata_report.get("target_rounds") == [18, 19, 20, 21]
        and errata_report.get("operations") == 120
        and errata_report.get("new_operations") == 43,
        "historical errata verifier report mismatch",
    )
    insertion_report = run_bound_command(
        root,
        receipt.get("projection_verifier"),
        "tools/compose_registered_insertion.py",
        (
            "--overlay-id", OVERLAY_ID,
            "--base-revision", import_commit,
            "--check-revision", source_commit,
        ),
        "unofficial-ai-integrated-stacks-registered-insertion-composition/v1",
    )
    canonical = insertion_report.get("canonical_composition")
    require(
        insertion_report.get("overlay_id") == OVERLAY_ID
        and insertion_report.get("base_revision") == import_commit
        and insertion_report.get("check_revision") == source_commit
        and insertion_report.get("frozen_contract") == composition.get("frozen_contract")
        and isinstance(canonical, dict)
        and canonical.get("before_bytes") == evidence.get("before_bytes")
        and canonical.get("before_sha256") == evidence.get("before_sha256")
        and canonical.get("before_blob") == evidence.get("before_git_blob")
        and canonical.get("context_occurrences") == 1
        and canonical.get("context_bytes") == evidence.get("context_bytes")
        and canonical.get("context_sha256") == evidence.get("context_sha256")
        and canonical.get("rebased_byte_offset") == evidence.get("rebased_byte_offset")
        and canonical.get("payload_bytes") == evidence.get("payload_bytes")
        and canonical.get("payload_sha256") == evidence.get("payload_sha256")
        and canonical.get("composed_bytes") == evidence.get("composed_bytes")
        and canonical.get("composed_sha256") == evidence.get("composed_sha256")
        and canonical.get("composed_blob") == evidence.get("composed_git_blob")
        and canonical.get("payload_occurrences_after") == 1
        and canonical.get("label_occurrences_after") == 1
        and canonical.get("prefix_unchanged") is True
        and canonical.get("suffix_unchanged") is True,
        "registered insertion verifier report mismatch",
    )
    require(tuple(receipt.get("required_build_stems", [])) == EXPECTED_STEMS, "full build profile mismatch")

    state = {
        "head": head,
        "source_commit": source_commit,
        "source_tree": composition.get("source_tree"),
        "import_commit": import_commit,
        "cutoff": cutoff,
        "composition_sha256": sha256(receipt_bytes),
        "composition_bytes": len(receipt_bytes),
        "composition_git_blob": git_text(root, "rev-parse", f"HEAD:{COMPOSITION_PATH.as_posix()}"),
        "affected": affected,
        "verifier_reports": {
            "registered_insertion": insertion_report,
            "historical_errata": errata_report,
        },
        "registry_identities": {
            kind: {
                "path": path,
                **file_identity(root, "HEAD", path),
            }
            for kind, path in registry_paths.items()
        },
    }
    return receipt, receipt_bytes, state


def validate_build(root: Path, path: Path, state: dict[str, object]) -> tuple[dict, bytes, list[dict]]:
    receipt, raw = load_committed_json(root, path, "fixed-point build receipt")
    require(receipt.get("schema") == "unofficial-ai-integrated-stacks-fixed-point-build/v1" and receipt.get("status") == "PASS", "fixed-point build did not pass")
    source = receipt.get("source")
    require(isinstance(source, dict), "build receipt lacks source identity")
    source_commit = require_commit(root, source.get("commit"), "build source")
    require_tree(root, source_commit, source.get("tree"), "build source")
    require_ancestor(root, state["source_commit"], source_commit, "composition source to build source")
    require_ancestor(root, source_commit, "HEAD", "build source to HEAD")
    for relative, evidence in state["affected"].items():
        check_identity(
            file_identity(root, source_commit, relative),
            {
                "bytes": evidence.get("composed_bytes"),
                "sha256": evidence.get("composed_sha256"),
                "git_blob": evidence.get("composed_git_blob"),
            },
            f"build-source protected composition {relative}",
        )
    for identity in state["registry_identities"].values():
        check_identity(
            file_identity(root, source_commit, identity["path"]),
            identity,
            f"build-source protected registry {identity['path']}",
        )
    check_identity(
        file_identity(root, source_commit, COMPOSITION_PATH.as_posix()),
        {
            "bytes": len(commit_bytes(root, "HEAD", COMPOSITION_PATH.as_posix())),
            "sha256": state["composition_sha256"],
            "git_blob": state["composition_git_blob"],
        },
        "build-source composition receipt",
    )
    builder = receipt.get("builder")
    require(isinstance(builder, dict) and builder.get("path") == "tools/build_fixed_point.py", "build receipt lacks builder binding")
    builder_identity = file_identity(root, source_commit, "tools/build_fixed_point.py")
    require(builder.get("git_blob") == builder_identity["git_blob"] and builder.get("sha256") == builder_identity["sha256"], "builder identity mismatch")
    composition = receipt.get("composition")
    require(
        isinstance(composition, dict)
        and composition.get("schema") == SCHEMA
        and composition.get("receipt") == COMPOSITION_PATH.as_posix()
        and composition.get("receipt_sha256") == state["composition_sha256"]
        and composition.get("receipt_git_blob") == state["composition_git_blob"]
        and composition.get("composition_source_commit") == state["source_commit"]
        and composition.get("registry_cutoff_commit") == state["cutoff"]
        and composition.get("last_admitted_overlay") == OVERLAY_ID,
        "build/composition binding mismatch",
    )
    require(
        composition.get("verifier_reports") == state["verifier_reports"],
        "build receipt does not bind the rerun verifier reports",
    )
    build = receipt.get("build")
    require(isinstance(build, dict), "build receipt lacks build state")
    require(
        build.get("strategy") == "sequential-prime-bibtex-global-state-sweeps"
        and build.get("fixed_point_suffixes") == list(FIXED_POINT_SUFFIXES)
        and build.get("stem_selection") == "composition_receipt"
        and build.get("stems") == list(EXPECTED_STEMS)
        and build.get("chapter_count") == len(EXPECTED_STEMS)
        and build.get("worktree_kind") == "linked"
        and build.get("primary_worktree_override") is False,
        "build strategy, profile, or isolation mismatch",
    )
    require(type(build.get("global_fixed_point_sweep")) is int and 1 <= build["global_fixed_point_sweep"] <= 6, "invalid fixed-point sweep")
    require(build.get("pdfinfo_readable") == len(EXPECTED_STEMS), "not all PDFs were readable")
    diagnostics = build.get("diagnostics")
    require(
        isinstance(diagnostics, dict)
        and tuple(diagnostics) == DIAGNOSTIC_KEYS
        and all(type(value) is int and value >= 0 for value in diagnostics.values()),
        "build diagnostics are incomplete or invalid",
    )
    for key in DIAGNOSTIC_KEYS:
        if key == "external_reference_markers":
            continue
        require(diagnostics.get(key) == 0, f"nonzero build diagnostic: {key}")
    artifacts = receipt.get("artifacts")
    require(isinstance(artifacts, list) and [row.get("stem") for row in artifacts if isinstance(row, dict)] == list(EXPECTED_STEMS), "build artifact inventory mismatch")
    artifact_diagnostic_totals = {key: 0 for key in DIAGNOSTIC_KEYS}
    for artifact in artifacts:
        artifact_diagnostics = artifact.get("diagnostics") if isinstance(artifact, dict) else None
        external = artifact.get("external_references") if isinstance(artifact, dict) else None
        require(
            isinstance(artifact, dict)
            and type(artifact.get("pages")) is int
            and artifact["pages"] > 0
            and type(artifact.get("bytes")) is int
            and artifact["bytes"] > 0
            and isinstance(artifact.get("sha256"), str)
            and len(artifact["sha256"]) == 64
            and all(character in "0123456789ABCDEF" for character in artifact["sha256"])
            and isinstance(artifact_diagnostics, dict)
            and tuple(artifact_diagnostics) == DIAGNOSTIC_KEYS
            and all(type(value) is int and value >= 0 for value in artifact_diagnostics.values())
            and isinstance(external, dict)
            and external.get("count") == artifact_diagnostics.get("external_reference_markers")
            and isinstance(external.get("sha256"), str)
            and len(external["sha256"]) == 64
            and all(character in "0123456789ABCDEF" for character in external["sha256"]),
            "invalid build artifact identity",
        )
        for key in DIAGNOSTIC_KEYS:
            artifact_diagnostic_totals[key] += artifact_diagnostics[key]
    require(
        artifact_diagnostic_totals == diagnostics,
        "aggregate build diagnostics do not equal per-artifact diagnostics",
    )
    tuple_lines = [
        "|".join(
            (str(row["stem"]), str(row["pages"]), str(row["bytes"]), str(row["sha256"]))
        )
        for row in sorted(artifacts, key=lambda item: str(item["stem"]))
    ]
    tuple_sha = sha256((("\n".join(tuple_lines)) + "\n").encode("utf-8"))
    require(
        build.get("artifact_tuple_set_sha256") == tuple_sha,
        "build artifact-tuple digest mismatch",
    )
    require(receipt.get("pdfs_committed") is False, "build PDFs should not be committed")
    return receipt, raw, artifacts


def validate_qa_and_repro(
    root: Path,
    build_path: Path,
    build: dict,
    build_raw: bytes,
    artifacts: list[dict],
    state: dict[str, object],
) -> tuple[dict, bytes, dict, bytes, dict, bytes]:
    second, second_raw, second_artifacts = validate_build(root, SECOND_BUILD_PATH, state)
    require(second.get("source") == build.get("source"), "second build source differs")
    require(second.get("builder") == build.get("builder"), "second build builder differs")
    require(second.get("environment") == build.get("environment"), "second build environment differs")
    require(second.get("composition") == build.get("composition"), "second build composition differs")
    require(second.get("build") == build.get("build"), "second build state differs")
    require(second_artifacts == artifacts, "second build artifact identities differ")
    first_created = build.get("created_utc")
    second_created = second.get("created_utc")
    require(
        isinstance(first_created, str)
        and isinstance(second_created, str)
        and first_created != second_created,
        "parallel reproducibility builds do not identify distinct invocations",
    )

    visual, visual_raw = load_committed_json(root, VISUAL_PATH, "visual-QA receipt")
    require(visual.get("schema") == "unofficial-ai-integrated-stacks-visual-qa/v1" and visual.get("status") == "PASS", "visual QA did not pass")
    require(visual.get("source") == build.get("source"), "visual-QA source mismatch")
    build_binding = visual.get("build_receipt")
    require(
        isinstance(build_binding, dict)
        and build_binding.get("path") == build_path.as_posix()
        and build_binding.get("bytes") == len(build_raw)
        and build_binding.get("sha256") == sha256(build_raw)
        and build_binding.get("status") == "PASS",
        "visual-QA build binding mismatch",
    )
    scope = visual.get("scope")
    require(
        isinstance(scope, dict)
        and scope.get("affected_chapters") == ["derived"],
        "visual-QA affected scope mismatch",
    )
    high = scope.get("high_resolution_locus_pages")
    require(isinstance(high, dict) and high.get("derived") == [9, 10, 11], "visual-QA high-resolution locus mismatch")
    derived_artifact = next(row for row in artifacts if row.get("stem") == "derived")
    require(
        scope.get("full_page_render_count") == derived_artifact.get("pages")
        and scope.get("full_page_contact_sheet_review_count") == derived_artifact.get("pages")
        and scope.get("high_resolution_locus_page_count") == 3,
        "visual-QA page-review counts mismatch",
    )
    visual_artifact = visual.get("artifacts", {}).get("derived") if isinstance(visual.get("artifacts"), dict) else None
    require(isinstance(visual_artifact, dict), "visual-QA derived artifact missing")
    for key in ("pages", "bytes", "sha256"):
        require(visual_artifact.get(key) == derived_artifact.get(key), f"visual-QA derived {key} mismatch")
    require(
        visual_artifact.get("pdf") == "derived.pdf"
        and visual_artifact.get("encrypted") is False
        and visual_artifact.get("pages_without_ink") == 0
        and visual_artifact.get("duplicate_render_hashes") == 0,
        "visual-QA derived PDF/render inventory mismatch",
    )
    checks = visual.get("checks")
    require(isinstance(checks, dict), "visual-QA checks missing")
    for key in ("all_pages_rendered", "all_pages_manually_inspected", "all_manifest_bound_locus_pages_inspected_at_high_resolution", "page_dimensions_consistent", "headers_and_page_numbers_consistent", "text_and_formulas_legible", "diagrams_intact"):
        require(checks.get(key) is True, f"visual-QA check did not pass: {key}")
    for key in ("clipped_content", "overlapping_content", "blank_pages", "corrupted_pages", "missing_or_unreadable_glyphs", "broken_diagrams"):
        require(checks.get(key) == 0, f"visual-QA defect count is nonzero: {key}")
    protocol = visual.get("render_protocol")
    require(
        isinstance(protocol, dict)
        and "Poppler" in str(protocol.get("renderer"))
        and type(protocol.get("full_page_dpi")) is int
        and protocol["full_page_dpi"] >= 72
        and type(protocol.get("high_resolution_dpi")) is int
        and protocol["high_resolution_dpi"] >= 144
        and protocol.get("render_intermediates_published") is False,
        "visual-QA render protocol is incomplete",
    )

    repro, repro_raw = load_committed_json(root, REPRO_PATH, "reproducibility receipt")
    require(repro.get("schema") == "unofficial-ai-integrated-stacks-clean-build-reproducibility/v1" and repro.get("status") == "PASS", "reproducibility did not pass")
    require(repro.get("source") == build.get("source") and repro.get("builder") == build.get("builder") and repro.get("environment") == build.get("environment"), "reproducibility identity mismatch")
    require(repro.get("artifacts") == artifacts, "reproducibility artifact inventory mismatch")
    require(
        repro.get("scope")
        == {
            "overlay": OVERLAY_ID,
            "registry_cutoff_commit": state["cutoff"],
            "source_commit": build.get("source", {}).get("commit"),
            "source_tree": build.get("source", {}).get("tree"),
            "composition_receipt": COMPOSITION_PATH.as_posix(),
            "composition_receipt_sha256": state["composition_sha256"],
        },
        "reproducibility scope mismatch",
    )
    method = repro.get("method")
    require(
        method
        == {
            "execution_model": "parallel_independent_linked_worktrees",
            "first_worktree_kind": build.get("build", {}).get("worktree_kind"),
            "second_worktree_kind": second.get("build", {}).get("worktree_kind"),
            "builder_path": build.get("builder", {}).get("path"),
            "builder_git_blob": build.get("builder", {}).get("git_blob"),
            "builder_sha256": build.get("builder", {}).get("sha256"),
        },
        "reproducibility method binding mismatch",
    )
    runs = repro.get("runs")
    require(isinstance(runs, dict), "reproducibility runs are missing")
    for key, path, raw, receipt in (
        ("first", build_path, build_raw, build),
        ("second", SECOND_BUILD_PATH, second_raw, second),
    ):
        row = runs.get(key)
        require(
            isinstance(row, dict)
            and row.get("receipt") == path.as_posix()
            and row.get("created_utc") == receipt.get("created_utc")
            and row.get("bytes") == len(raw)
            and row.get("sha256") == sha256(raw)
            and row.get("status") == "PASS"
            and row.get("global_fixed_point_sweep") == receipt.get("build", {}).get("global_fixed_point_sweep"),
            f"reproducibility {key}-run binding mismatch",
        )
    comparison = repro.get("comparison")
    require(
        isinstance(comparison, dict)
        and comparison.get("chapter_count") == len(EXPECTED_STEMS)
        and comparison.get("matched_artifact_count") == len(EXPECTED_STEMS)
        and comparison.get("different_artifact_count") == 0
        and comparison.get("different_artifacts") == []
        and comparison.get("all_artifact_identities_exactly_equal") is True
        and comparison.get("source_identity_equal") is True
        and comparison.get("builder_identity_equal") is True
        and comparison.get("environment_identity_equal") is True,
        "reproducibility comparison mismatch",
    )
    require(
        comparison.get("fixed_point_sweep_equal") is True
        and comparison.get("total_pages_each_run")
        == sum(int(row["pages"]) for row in artifacts)
        and comparison.get("total_pdf_bytes_each_run")
        == sum(int(row["bytes"]) for row in artifacts)
        and comparison.get("artifact_tuple_set_sha256_each_run")
        == build.get("build", {}).get("artifact_tuple_set_sha256"),
        "reproducibility fixed-point or artifact-tuple comparison mismatch",
    )
    return visual, visual_raw, repro, repro_raw, second, second_raw


def anonymous_public_main_head() -> str:
    completed = subprocess.run(
        [
            "git",
            "ls-remote",
            "https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project.git",
            "refs/heads/main",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    parts = completed.stdout.strip().split()
    require(
        completed.returncode == 0
        and len(parts) == 2
        and parts[1] == "refs/heads/main"
        and len(parts[0]) == 40
        and all(character in "0123456789abcdef" for character in parts[0]),
        "anonymous public main readback failed: " + completed.stderr.strip(),
    )
    return parts[0]


def anonymous_raw_bytes(commit: str, path: str) -> bytes:
    url = (
        "https://raw.githubusercontent.com/"
        "KokunoYumeto/unofficial-ai-integrated-stacks-project/"
        f"{commit}/{quote(path, safe='/')}"
    )
    request = Request(url, headers={"User-Agent": "stacks-release-validator/1"})
    try:
        with urlopen(request, timeout=60) as response:
            require(response.status == 200, f"public raw readback returned HTTP {response.status}: {path}")
            return response.read()
    except OSError as exc:
        raise ValidationError(f"public raw readback failed for {path}: {exc}") from exc


def anonymous_json(url: str, label: str) -> dict:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "stacks-release-validator/1",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            require(response.status == 200, f"{label} returned HTTP {response.status}")
            value = json.loads(response.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"anonymous {label} readback failed: {exc}") from exc
    require(isinstance(value, dict), f"anonymous {label} response is not an object")
    return value


def validate_release(
    root: Path,
    state: dict[str, object],
    build_path: Path,
    build: dict,
    build_raw: bytes,
    artifacts: list[dict],
    visual: dict,
    visual_raw: bytes,
    repro: dict,
    repro_raw: bytes,
    second: dict,
    second_raw: bytes,
) -> dict:
    release, _ = load_committed_json(root, RELEASE_PATH, "Verdier release receipt")
    require(release.get("schema") == "unofficial-ai-integrated-stacks-verdier-release/v1" and release.get("status") == "PUBLICATION_COMPLETE", "Verdier release is not publication-complete")
    publication = release.get("release")
    require(
        isinstance(publication, dict)
        and publication.get("repository") == "KokunoYumeto/unofficial-ai-integrated-stacks-project"
        and publication.get("default_branch") == "main",
        "Verdier release destination mismatch",
    )
    content_head = require_commit(root, publication.get("content_head"), "published content")
    require_tree(root, content_head, publication.get("content_tree"), "published content")
    metadata_head = require_commit(root, publication.get("metadata_head"), "release metadata")
    require_tree(root, metadata_head, publication.get("metadata_tree"), "release metadata")
    require_ancestor(root, state["source_commit"], content_head, "composition to content release")
    require_ancestor(root, content_head, metadata_head, "content to metadata release")
    require_ancestor(root, metadata_head, "HEAD", "metadata release to HEAD")
    require(
        publication.get("previous_public_main_head") == PREVIOUS_MAIN_COMMIT
        and publication.get("registry_cutoff_commit") == state["cutoff"]
        and publication.get("overlay") == OVERLAY_ID
        and publication.get("registered_overlays") == 22
        and publication.get("registered_stable_ids") == 559,
        "Verdier release scope or registry counts mismatch",
    )

    require(
        release.get("candidate")
        == {
            "commit": CANDIDATE_COMMIT,
            "tree": CANDIDATE_TREE,
            "subtree": CANDIDATE_SUBTREE,
            "manifest_sha256": MANIFEST_SHA256,
            "stable_units": 12,
            "manifest_references": 27,
            "rights_state": RIGHTS_STATE,
            "official_stacks_tag_claimed": False,
            "upstream_endorsement_claimed": False,
        },
        "release candidate identity or disclaimer mismatch",
    )
    expected_composition = {
        "path": COMPOSITION_PATH.as_posix(),
        "bytes": state["composition_bytes"],
        "sha256": state["composition_sha256"],
        "git_blob": state["composition_git_blob"],
        "source_commit": state["source_commit"],
        "source_tree": state["source_tree"],
    }
    require(release.get("composition") == expected_composition, "release composition binding mismatch")
    build_state = build.get("build", {})
    expected_build = {
        "receipt_path": build_path.as_posix(),
        "receipt_bytes": len(build_raw),
        "receipt_sha256": sha256(build_raw),
        "source_commit": build.get("source", {}).get("commit"),
        "source_tree": build.get("source", {}).get("tree"),
        "chapters": len(artifacts),
        "pages": sum(int(row["pages"]) for row in artifacts),
        "pdf_bytes": sum(int(row["bytes"]) for row in artifacts),
        "global_fixed_point_sweep": build_state.get("global_fixed_point_sweep"),
        "artifact_tuple_set_sha256": build_state.get("artifact_tuple_set_sha256"),
        "diagnostics": build_state.get("diagnostics"),
    }
    require(release.get("build") == expected_build, "release build binding mismatch")
    expected_visual = {
        "status": "PASS",
        "receipt_path": VISUAL_PATH.as_posix(),
        "receipt_bytes": len(visual_raw),
        "receipt_sha256": sha256(visual_raw),
        "receipt_git_blob": git_text(root, "rev-parse", f"HEAD:{VISUAL_PATH.as_posix()}"),
        "full_page_reviews": visual.get("scope", {}).get("full_page_render_count"),
        "high_resolution_pages": visual.get("scope", {}).get("high_resolution_locus_page_count"),
        "defects": sum(
            int(visual.get("checks", {}).get(key, 0))
            for key in (
                "clipped_content",
                "overlapping_content",
                "blank_pages",
                "corrupted_pages",
                "missing_or_unreadable_glyphs",
                "broken_diagrams",
            )
        ),
    }
    require(release.get("visual_qa") == expected_visual, "release visual-QA binding mismatch")
    expected_repro = {
        "status": "PASS",
        "summary_path": REPRO_PATH.as_posix(),
        "summary_bytes": len(repro_raw),
        "summary_sha256": sha256(repro_raw),
        "summary_git_blob": git_text(root, "rev-parse", f"HEAD:{REPRO_PATH.as_posix()}"),
        "second_receipt_path": SECOND_BUILD_PATH.as_posix(),
        "second_receipt_bytes": len(second_raw),
        "second_receipt_sha256": sha256(second_raw),
        "second_receipt_git_blob": git_text(root, "rev-parse", f"HEAD:{SECOND_BUILD_PATH.as_posix()}"),
        "matched_artifacts": len(artifacts),
        "different_artifacts": 0,
        "artifact_tuple_set_sha256": build_state.get("artifact_tuple_set_sha256"),
    }
    require(release.get("reproducibility") == expected_repro, "release reproducibility binding mismatch")
    readback = release.get("public_readback")
    require(isinstance(readback, dict) and readback.get("status") == "PASS" and readback.get("commit") == content_head, "public readback did not pass")
    rows = readback.get("checked_paths")
    require(isinstance(rows, list) and rows, "public readback inventory is empty")
    candidate_prefix = "ai-integrated/candidates/commons/stacks/verdier"
    expected_decisive: dict[str, dict[str, object]] = {
        "derived.tex": {
            "bytes": state["affected"]["derived.tex"]["composed_bytes"],
            "sha256": state["affected"]["derived.tex"]["composed_sha256"],
            "git_blob": state["affected"]["derived.tex"]["composed_git_blob"],
        },
        COMPOSITION_PATH.as_posix(): {
            "bytes": state["composition_bytes"],
            "sha256": state["composition_sha256"],
            "git_blob": state["composition_git_blob"],
        },
        build_path.as_posix(): {
            "bytes": len(build_raw),
            "sha256": sha256(build_raw),
            "git_blob": git_text(root, "rev-parse", f"{content_head}:{build_path.as_posix()}"),
        },
        VISUAL_PATH.as_posix(): {
            "bytes": len(visual_raw),
            "sha256": sha256(visual_raw),
            "git_blob": git_text(root, "rev-parse", f"{content_head}:{VISUAL_PATH.as_posix()}"),
        },
        SECOND_BUILD_PATH.as_posix(): {
            "bytes": len(second_raw),
            "sha256": sha256(second_raw),
            "git_blob": git_text(root, "rev-parse", f"{content_head}:{SECOND_BUILD_PATH.as_posix()}"),
        },
        REPRO_PATH.as_posix(): {
            "bytes": len(repro_raw),
            "sha256": sha256(repro_raw),
            "git_blob": git_text(root, "rev-parse", f"{content_head}:{REPRO_PATH.as_posix()}"),
        },
    }
    for identity in state["registry_identities"].values():
        expected_decisive[identity["path"]] = identity
    for relative in (
        "candidate.manifest.json",
        "payload/fragments/derived-functorial-triangles.tex",
        "composition.jsonl",
        "replay/independent-review.json",
    ):
        public_path = f"{candidate_prefix}/{relative}"
        expected_decisive[public_path] = file_identity(root, content_head, public_path)
    seen: set[str] = set()
    total_bytes = 0
    for row in rows:
        require(isinstance(row, dict) and isinstance(row.get("path"), str), "invalid public readback row")
        path = row["path"]
        require(path not in seen and ".." not in Path(path).parts and not Path(path).is_absolute(), "unsafe or duplicate public readback path")
        seen.add(path)
        if path in expected_decisive:
            check_identity(expected_decisive[path], row, f"validated release binding {path}")
        observed = file_identity(root, content_head, path)
        check_identity(observed, row, f"public readback {path}")
        remote = anonymous_raw_bytes(content_head, path)
        check_identity(
            {
                "bytes": len(remote),
                "sha256": sha256(remote),
                "git_blob": git_text(root, "hash-object", "--stdin", input_bytes=remote),
            },
            row,
            f"anonymous HTTPS readback {path}",
        )
        total_bytes += int(row["bytes"])
    require(readback.get("checked_file_count") == len(rows) and readback.get("checked_total_bytes") == total_bytes, "public readback totals mismatch")
    required = {
        "derived.tex",
        "ai-integrated/registry/overlays.json",
        "ai-integrated/registry/leases.json",
        "ai-integrated/candidates/commons/stacks/verdier/candidate.manifest.json",
        "ai-integrated/candidates/commons/stacks/verdier/payload/fragments/derived-functorial-triangles.tex",
        "ai-integrated/candidates/commons/stacks/verdier/composition.jsonl",
        "ai-integrated/candidates/commons/stacks/verdier/replay/independent-review.json",
        COMPOSITION_PATH.as_posix(),
        "tools/compose_registered_insertion.py",
        "tools/build_fixed_point.py",
        "tools/validate_registered_insertion_release.py",
        "tools/validate_unified_repository.py",
        BUILD_PATH.as_posix(),
        VISUAL_PATH.as_posix(),
        SECOND_BUILD_PATH.as_posix(),
        REPRO_PATH.as_posix(),
        "README.md",
        "STATUS.md",
        "ROADMAP.md",
        "PROVENANCE.md",
        "VALIDATION.md",
        "CONTRIBUTING.md",
        "ai-integrated/README.md",
        "validation/README.md",
        "validation/unification-release-2026-08-25.json",
        "validation/errata-r18-r19-release-2026-08-25.json",
        ".github/workflows/validate.yml",
    }
    require(required.issubset(seen), "public readback omits a decisive release path")
    require(
        set(expected_decisive).issubset(seen),
        "public readback omits a validated build/composition/candidate identity",
    )
    workflow = release.get("workflow")
    require(
        isinstance(workflow, dict)
        and workflow.get("name") == "Unified repository validation"
        and workflow.get("status") == "completed"
        and workflow.get("conclusion") == "success"
        and workflow.get("head_sha") == metadata_head
        and isinstance(workflow.get("run_id"), int)
        and workflow.get("url")
        == f"https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/actions/runs/{workflow.get('run_id')}",
        "release workflow binding did not pass",
    )
    workflow_api = anonymous_json(
        "https://api.github.com/repos/"
        "KokunoYumeto/unofficial-ai-integrated-stacks-project/actions/runs/"
        f"{workflow['run_id']}",
        "GitHub Actions run",
    )
    require(
        workflow_api.get("name") == workflow.get("name")
        and workflow_api.get("head_sha") == metadata_head
        and workflow_api.get("status") == "completed"
        and workflow_api.get("conclusion") == "success"
        and workflow_api.get("html_url") == workflow.get("url")
        and isinstance(workflow_api.get("repository"), dict)
        and workflow_api["repository"].get("full_name")
        == "KokunoYumeto/unofficial-ai-integrated-stacks-project",
        "anonymous GitHub Actions run readback does not match the release receipt",
    )
    require(
        anonymous_public_main_head() == git_text(root, "rev-parse", "HEAD"),
        "validated HEAD is not the anonymous public main head",
    )
    return release


def validate_v4(
    root: Path,
    build_receipt: Path,
    pre_publication: bool,
) -> int:
    try:
        root = root.resolve()
        validate_historical_r21_snapshot(root)
        _, _, state = validate_composition(root)
        build_path = build_receipt if not build_receipt.is_absolute() else build_receipt.relative_to(root)
        require(
            build_path.as_posix() == BUILD_PATH.as_posix(),
            f"unexpected Verdier build receipt path: {build_path.as_posix()}",
        )
        build, build_raw, artifacts = validate_build(root, build_path, state)
        visual, visual_raw, repro, repro_raw, second, second_raw = validate_qa_and_repro(
            root, build_path, build, build_raw, artifacts, state
        )
        validate_current_surface(root, pre_publication)
        if not pre_publication:
            validate_release(
                root,
                state,
                build_path,
                build,
                build_raw,
                artifacts,
                visual,
                visual_raw,
                repro,
                repro_raw,
                second,
                second_raw,
            )
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
        ValidationError,
    ) as exc:
        print("Unified registered-insertion validation: FAIL", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1

    print("Unified registered-insertion validation: PASS")
    print("- registered overlays: 22")
    print("- registered stable IDs: 559")
    print("- registered insertion operations: 1")
    print(f"- fixed-point chapters: {len(EXPECTED_STEMS)}")
    print("- visual-QA affected chapters: 1")
    print(f"- reproducible PDF identities: {len(EXPECTED_STEMS)}")
    print(f"- publication receipt checked: {not pre_publication}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository worktree root (default: parent of tools/)",
    )
    parser.add_argument(
        "--build-receipt",
        type=Path,
        default=BUILD_PATH,
        help="Verdier fixed-point build receipt",
    )
    parser.add_argument(
        "--pre-publication",
        action="store_true",
        help="skip only the current Verdier public-release/readback receipt",
    )
    args = parser.parse_args(argv)
    return validate_v4(args.root, args.build_receipt, args.pre_publication)


if __name__ == "__main__":
    raise SystemExit(main())
