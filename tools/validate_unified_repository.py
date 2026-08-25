#!/usr/bin/env python3
"""Fast fail-closed validation for the unified AI-integrated Stacks tree."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "a04446e57ec1fbc252a871afcec7752fb2807b14"
SOURCE_UNION = "ad58625f60e6816905ff217d21d91b07b2722fcf"
EGA_EXPORT = "91df7f1c96bd4973264c29b0e121253a05d1d361"
REGISTRY_HEAD = "9b73f1917e76dfff296b259f7ed56a9565952170"
ERRATA_R1_R16 = "8ca593fa03e1271a523fc269d9586b1b81375915"

PUBLIC_MARKDOWN = (
    "README.md",
    "STATUS.md",
    "PROVENANCE.md",
    "VALIDATION.md",
    "CONTRIBUTING.md",
    "ai-integrated/README.md",
)

REQUIRED_PATHS = (
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
    "ai-integrated/upstream/stacks.lock.json",
)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def candidate_dir(overlay_id: str) -> Path:
    suffix = overlay_id.rsplit("-r", 1)[1]
    base = ROOT / "ai-integrated/candidates/commons/stacks/errata"
    return base if suffix == "1" else base / f"r{suffix}"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.relative_to(ROOT)}:{number}: {exc}") from exc
    return rows


def literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"missing literal assignment {name} in {path.relative_to(ROOT)}")


def validate_links(errors: list[str]) -> None:
    link_re = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for relative in PUBLIC_MARKDOWN:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        for raw_target in link_re.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"broken link in {relative}: {raw_target}")


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_PATHS + PUBLIC_MARKDOWN:
        if not (ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")

    for commit, label in (
        (UPSTREAM, "pinned upstream"),
        (SOURCE_UNION, "FAC/Tohoku/GAGA/FGA source union"),
        (EGA_EXPORT, "EGA export"),
        (REGISTRY_HEAD, "complete registry history"),
        (ERRATA_R1_R16, "cumulative admitted errata R1-R16"),
    ):
        result = git("merge-base", "--is-ancestor", commit, "HEAD")
        if result.returncode != 0:
            errors.append(f"missing {label} ancestor: {commit}")

    registry_path = ROOT / "ai-integrated/registry/overlays.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entries = registry.get("registered_entries", [])
    if len(entries) != 16:
        errors.append(f"expected 16 registered overlays, found {len(entries)}")

    registered_ids: list[str] = []
    v2_operations = 0
    v1_replacements = 0
    tag_additions = 0
    for entry in entries:
        raw_ids = entry.get("stable_ids", "")
        ids = raw_ids if isinstance(raw_ids, list) else raw_ids.split()
        registered_ids.extend(ids)
        directory = candidate_dir(entry["id"])
        manifest = directory / "candidate.manifest.json"
        manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest().upper()
        if manifest_hash != entry.get("manifest_sha256", "").upper():
            errors.append(f"candidate manifest hash mismatch for {entry['id']}")
        review = ROOT / "ai-integrated" / entry["review_receipt"]
        if not review.is_file():
            errors.append(f"missing independent replay receipt for {entry['id']}")
        source_map = directory / "source-map.jsonl"
        if not source_map.is_file():
            errors.append(f"missing source map: {source_map.relative_to(ROOT)}")
            continue
        rows = read_jsonl(source_map)
        mapped_ids = [row.get("unit_id") for row in rows]
        if mapped_ids != ids:
            errors.append(f"registry/source-map ID mismatch for {entry['id']}")
        for row in rows:
            operations = row.get("operations", [])
            if not operations:
                continue
            source = ROOT / row["source"]
            if not source.is_file():
                errors.append(f"missing composed source: {row['source']}")
                continue
            source_text = source.read_text(encoding="utf-8")
            for operation in operations:
                v2_operations += 1
                replacement = operation["replacement_text"]
                if replacement not in source_text:
                    errors.append(
                        f"missing composed replacement {operation['operation_id']} "
                        f"in {row['source']}"
                    )

    for round_number in (1, 2, 3):
        overlay_id = f"stacks-errata-a04446e-r{round_number}"
        directory = candidate_dir(overlay_id)
        replacements = literal_assignment(directory / "verify.py", "REPLACEMENTS")
        if not isinstance(replacements, dict):
            errors.append(f"REPLACEMENTS is not a mapping for R{round_number}")
            continue
        for source_name, rows in replacements.items():
            source_text = (ROOT / source_name).read_text(encoding="utf-8")
            for row in rows:
                replacement_text = row[1]
                v1_replacements += 1
                if replacement_text not in source_text:
                    errors.append(
                        f"missing composed R{round_number} replacement in {source_name}: "
                        f"{replacement_text!r}"
                    )

    new_tags = literal_assignment(candidate_dir("stacks-errata-a04446e-r1") / "verify.py", "NEW_TAGS")
    tag_lines = set((ROOT / "tags/tags").read_text(encoding="utf-8").splitlines())
    for line in new_tags:
        tag_additions += 1
        if line not in tag_lines:
            errors.append(f"missing composed R1 tag record: {line}")

    if len(registered_ids) != 416:
        errors.append(f"expected 416 registered stable IDs, found {len(registered_ids)}")
    if len(set(registered_ids)) != len(registered_ids):
        errors.append("registered stable IDs are not unique")

    injectives = (ROOT / "injectives.tex").read_text(encoding="utf-8")
    corrected = r"$S_Y = \{\phi \in \Mor(U,X) : \phi\text{ factors through }Y\}$."
    malformed = r"$S_Y = \{\phi \in \Mor(U,X) : \phi)\text{ factors through }Y\}$."
    if corrected not in injectives or malformed in injectives:
        errors.append("independent injectives.tex parenthesis correction is absent")

    for relative in (
        "ai-integrated/registry/leases.json",
        "ai-integrated/registry/locales.json",
        "ai-integrated/registry/overlays.json",
        "ai-integrated/registry/releases.json",
        "ai-integrated/upstream/stacks.lock.json",
    ):
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {relative}: {exc}")

    marker_paths = [ROOT / item for item in PUBLIC_MARKDOWN]
    marker_paths.extend(ROOT.glob("*.tex"))
    for path in marker_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "<<<<<<< " in text or ">>>>>>> " in text:
            errors.append(f"unresolved merge marker: {path.relative_to(ROOT)}")

    validate_links(errors)

    if errors:
        print("Unified repository validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Unified repository validation: PASS")
    print(f"- registered overlays: {len(entries)}")
    print(f"- registered stable IDs: {len(registered_ids)}")
    print(f"- exact v2 operations checked: {v2_operations}")
    print(f"- exact R1-R3 replacements checked: {v1_replacements}")
    print(f"- R1 tag additions checked: {tag_additions}")
    print(f"- public Markdown documents checked: {len(PUBLIC_MARKDOWN)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
