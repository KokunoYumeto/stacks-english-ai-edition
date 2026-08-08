#!/usr/bin/env python3
"""Verify a frozen EGA English manifest and emit metadata-only inventories."""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
PAGE_RE = re.compile(r"\\oldpage(?:\[([^]]+)\])?\{([^}]+)\}")
SECTION_RE = re.compile(r"\\(part|chapter|section|subsection|subsubsection)\*?\{")
BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}(?:\[([^]]+)\])?")
END_RE = re.compile(r"\\end\{([^}]+)\}")
XYMATRIX_RE = re.compile(r"\\xymatrix\b")
SECTION_LABEL_MAX_GAP = 4

STATEMENT_KINDS = {
    "env": "statement",
    "definition": "definition",
    "theorem": "theorem",
    "proposition": "proposition",
    "lemma": "lemma",
    "corollary": "corollary",
    "remark": "remark",
    "remarks": "remarks",
    "example": "example",
    "examples": "examples",
    "notation": "notation",
}
FORMULA_KINDS = {"equation": "equation", "align": "equation", "align*": "equation",
                 "gather": "equation", "gather*": "equation"}


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def active_tex(line):
    """Remove TeX comments while retaining escaped percent signs."""
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def write_csv(path, fields, data):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def logical_volume_from(path, label=""):
    """Return the logical EGA volume, independently of the printed witness page.

    An erratum incorporated into EGA I can have an ``oldpage[II]`` locator.
    That page-volume is provenance for the witness, not the volume containing
    the semantic unit.
    """
    match = re.search(r"(?:^|:)(0|IV|III|II|I)(?:[.:]|$)", label)
    if match:
        return match.group(1)
    part = path.parts[0] if path.parts else ""
    return {"ega0": "0", "ega1": "I", "ega2": "II", "ega3": "III",
            "source_aligned": "IV"}.get(part, "")


def printed_volume_major(volume):
    """Collapse witness-volume variants to the logical EGA major volume."""
    if volume.startswith("0"):
        return "0"
    for major in ("IV", "III", "II", "I"):
        if volume.startswith(major):
            return major
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", default=Path(__file__).resolve().parent, type=Path)
    args = parser.parse_args()

    errors = []
    raw_manifest = args.manifest.read_bytes()
    manifest = json.loads(raw_manifest.decode("utf-8"))
    expected_files = manifest.get("files", [])
    if manifest.get("file_count") != len(expected_files):
        errors.append("manifest file_count does not equal files length")

    file_rows = []
    file_text = {}
    canonical = []
    for entry in expected_files:
        rel = Path(entry["relative_path"])
        path = args.source / rel
        if not path.is_file():
            errors.append(f"missing source file: {rel.as_posix()}")
            continue
        data = path.read_bytes()
        actual = sha(data)
        if len(data) != entry["bytes"] or actual != entry["sha256"]:
            errors.append(f"identity mismatch: {rel.as_posix()}")
        canonical.append(f"{rel.as_posix()}\t{len(data)}\t{actual}\n")
        name = rel.name.lower()
        if rel.suffix.lower() == ".bib":
            role = "bibliography"
        elif name.startswith("ega4_reference_v2_"):
            role = "reference_registry"
        elif name in {"ega_english_global_0_iv.tex", "preamble.tex", "preamble-base.tex"} or name.startswith("global_volume_"):
            role = "support"
        elif any(token in name for token in ("backmatter", "bibliography", "indexes-and-contents")):
            role = "backmatter"
        elif "errata" in name:
            role = "errata"
        elif rel.suffix.lower() == ".tex":
            role = "content"
        else:
            role = "support"
        file_rows.append({
            "relative_path": rel.as_posix(),
            "bytes": len(data),
            "sha256": actual,
            "role": role,
        })
        if role in {"content", "errata"}:
            file_text[rel.as_posix()] = data.decode("utf-8")

    tree = sha("".join(canonical).encode("utf-8"))
    if tree != manifest.get("canonical_tree_sha256"):
        errors.append("canonical tree SHA-256 mismatch")

    units = []
    labels_seen = {}
    kind_counts = Counter()
    proof_counts = defaultdict(int)
    diagram_counts = defaultdict(int)
    xymatrix_counts = defaultdict(int)

    for rel, text in file_text.items():
        rel_path = Path(rel)
        file_volume = logical_volume_from(rel_path)
        page_volume = ""
        page_number = ""
        env_stack = []
        pending_section = None
        current_section = ""
        current_subsection = ""
        last_statement = ""
        last_statement_container = ""

        def add_unit(unit_id, kind, line_no, source_label="", source_number="", parent_id="", anchor=""):
            if unit_id in labels_seen:
                errors.append(f"duplicate unit ID {unit_id}: {rel}:{line_no} and {labels_seen[unit_id]}")
                return
            labels_seen[unit_id] = f"{rel}:{line_no}"
            volume = logical_volume_from(
                rel_path, source_label or parent_id or unit_id)
            units.append({
                "unit_id": unit_id,
                "volume": volume,
                "kind": kind,
                "source_number": source_number or source_label,
                "source_label": source_label,
                "parent_id": parent_id,
                "printed_page": f"{page_volume}:{page_number}" if page_number else "",
                "source_file": rel,
                "line": line_no,
                "anchor_sha256": sha(anchor.encode("utf-8")),
                "authority_state": "english_discovery",
                "review_state": "unreviewed",
            })
            kind_counts[kind] += 1

        lines = text.splitlines(keepends=True)
        for line_no, line in enumerate(lines, 1):
            active = active_tex(line)
            if (pending_section and
                    line_no - pending_section[1] > SECTION_LABEL_MAX_GAP):
                pending_section = None
            page = PAGE_RE.search(active)
            if page:
                explicit_volume = page.group(1) or ""
                foreign_volume = (
                    explicit_volume and file_volume and
                    printed_volume_major(explicit_volume) != file_volume
                )
                body_page_active = (
                    printed_volume_major(page_volume) == file_volume
                )
                statement_frame = next((
                    frame for frame in reversed(env_stack)
                    if frame["env"] in STATEMENT_KINDS
                ), None)
                if (foreign_volume and body_page_active and
                        statement_frame is not None):
                    # Translator-supplied errata can carry a foreign witness
                    # page inside one semantic statement.  Bind that locator
                    # retroactively to the whole statement, then restore the
                    # surrounding body page when its environment closes.
                    if statement_frame["page_restore"] is None:
                        statement_frame["page_restore"] = (
                            page_volume, page_number)
                    page_volume = explicit_volume
                    page_number = page.group(2)
                    printed_page = f"{page_volume}:{page_number}"
                    for row in units[statement_frame["unit_start"]:]:
                        row["printed_page"] = printed_page
                else:
                    if explicit_volume:
                        page_volume = explicit_volume
                    page_number = page.group(2)

            section = SECTION_RE.search(active)
            if section:
                pending_section = (section.group(1), line_no)
                last_statement = ""
                last_statement_container = ""

            for begin in BEGIN_RE.finditer(active):
                env = begin.group(1)
                number = begin.group(2) or ""
                frame = {
                    "env": env,
                    "number": number,
                    "primary": "",
                    "page_restore": None,
                    "unit_start": len(units),
                }
                env_stack.append(frame)
                if env == "proof":
                    parent = last_statement or current_subsection or current_section
                    proof_counts[parent or rel] += 1
                    suffix = proof_counts[parent or rel]
                    base = parent or f"ega:file:{rel.replace('/', ':')}"
                    unit_id = f"{base}:proof" + (f":{suffix}" if suffix > 1 else "")
                    add_unit(unit_id, "proof", line_no, source_number="proof",
                             parent_id=parent, anchor=line)
                elif env == "tikzcd":
                    parent = last_statement or current_subsection or current_section
                    diagram_counts[parent or rel] += 1
                    suffix = diagram_counts[parent or rel]
                    base = parent or f"ega:file:{rel.replace('/', ':')}"
                    unit_id = f"{base}:diagram:{suffix}"
                    add_unit(unit_id, "diagram", line_no, source_number=str(suffix),
                             parent_id=parent, anchor=line)

            # The source corpus overwhelmingly uses native Xy-pic diagrams
            # rather than tikz-cd.  Register every command occurrence even
            # when it carries an @-option such as \xymatrix@C=...{...}.
            for _ in XYMATRIX_RE.finditer(active):
                container = current_subsection or current_section
                parent = (last_statement if last_statement_container == container
                          else "") or container
                xymatrix_counts[parent or rel] += 1
                suffix = xymatrix_counts[parent or rel]
                base = parent or f"ega:file:{rel.replace('/', ':')}"
                unit_id = f"{base}:diagram:xymatrix:{suffix}"
                add_unit(unit_id, "diagram", line_no,
                         source_number=f"xymatrix:{suffix}",
                         parent_id=parent, anchor=line)

            for label_match in LABEL_RE.finditer(active):
                label = label_match.group(1)
                unit_id = f"ega:{label}"
                found_volume = logical_volume_from(rel_path, label)
                parent = current_subsection or current_section or (
                    f"ega:volume:{found_volume}" if found_volume else "ega:corpus")
                kind = "label"
                number = label

                if pending_section:
                    kind = pending_section[0]
                    pending_section = None
                    if kind in {"subsection", "subsubsection"}:
                        parent = current_section or parent
                        current_subsection = unit_id
                    elif kind in {"section", "chapter", "part"}:
                        found_volume = logical_volume_from(rel_path, label)
                        parent = f"ega:volume:{found_volume}" if found_volume else "ega:corpus"
                        current_section = unit_id
                        current_subsection = ""
                elif env_stack:
                    frame = env_stack[-1]
                    env = frame["env"]
                    number = frame["number"] or label
                    if env in STATEMENT_KINDS:
                        if not frame["primary"]:
                            kind = STATEMENT_KINDS[env]
                            frame["primary"] = unit_id
                            last_statement = unit_id
                            last_statement_container = current_subsection or current_section
                        else:
                            kind = "subitem"
                            parent = frame["primary"]
                    elif env in FORMULA_KINDS:
                        kind = FORMULA_KINDS[env]
                        parent = last_statement or current_subsection or current_section
                    elif env == "tikzcd":
                        kind = "diagram_label"
                        parent = last_statement or current_subsection or current_section

                add_unit(unit_id, kind, line_no, source_label=label,
                         source_number=number, parent_id=parent, anchor=line)

            for end in END_RE.finditer(active):
                env = end.group(1)
                for index in range(len(env_stack) - 1, -1, -1):
                    if env_stack[index]["env"] == env:
                        for frame in reversed(env_stack[index:]):
                            if frame["page_restore"] is not None:
                                page_volume, page_number = frame["page_restore"]
                        del env_stack[index:]
                        break

    prefix_units = [{
        "unit_id": "ega:corpus", "volume": "", "kind": "corpus",
        "source_number": "EGA 0-IV", "source_label": "", "parent_id": "",
        "printed_page": "", "source_file": "", "line": 0,
        "anchor_sha256": "", "authority_state": "english_discovery",
        "review_state": "unreviewed",
    }]
    kind_counts["corpus"] += 1
    for volume in ["0", "I", "II", "III", "IV"]:
        prefix_units.append({
            "unit_id": f"ega:volume:{volume}", "volume": volume, "kind": "volume",
            "source_number": volume, "source_label": "", "parent_id": "ega:corpus",
            "printed_page": "", "source_file": "", "line": 0,
            "anchor_sha256": "", "authority_state": "english_discovery",
            "review_state": "unreviewed",
        })
        kind_counts["volume"] += 1
    units = prefix_units + units

    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out / "files.csv", ["relative_path", "bytes", "sha256", "role"], file_rows)
    unit_fields = ["unit_id", "volume", "kind", "source_number", "source_label",
                   "parent_id", "printed_page", "source_file", "line",
                   "anchor_sha256", "authority_state", "review_state"]
    write_csv(args.out / "units.csv", unit_fields, units)

    result = {
        "schema": "ega-english-discovery-intake-v3",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "manifest": {
            "bytes": len(raw_manifest),
            "sha256": sha(raw_manifest),
            "declared": manifest.get("schema"),
        },
        "source": {
            "files": len(file_rows),
            "bytes": sum(row["bytes"] for row in file_rows),
            "tree_sha256": tree,
        },
        "units": len(units),
        "kind_counts": dict(sorted(kind_counts.items())),
        "copied_source_text": False,
    }
    (args.out / "intake.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
