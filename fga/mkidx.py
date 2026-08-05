#!/usr/bin/env python3
"""Build a deterministic Stacks label index and FGA topic candidates."""

from __future__ import annotations

import bisect
import csv
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "fga"
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
SECTION_RE = re.compile(
    r"\\(section|subsection|subsubsection)\s*\{", re.MULTILINE
)
TITLE_RE = re.compile(r"\\title\s*\{")
COMMENT_RE = re.compile(r"(?<!\\)%.*$")
COMMAND_RE = re.compile(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?")
SPACE_RE = re.compile(r"\s+")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def brace_arg(text: str, open_brace: int) -> tuple[str, int]:
    depth = 0
    for pos in range(open_brace, len(text)):
        char = text[pos]
        if char == "{" and (pos == 0 or text[pos - 1] != "\\"):
            depth += 1
        elif char == "}" and (pos == 0 or text[pos - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[open_brace + 1 : pos], pos + 1
    raise ValueError(f"unclosed braced argument at byte {open_brace}")


def plain(text: str, limit: int = 280) -> str:
    lines = [COMMENT_RE.sub("", line) for line in text.splitlines()]
    value = " ".join(lines)
    value = re.sub(r"\\['\"`^~=.Hckruvbdt]\s*\{?([A-Za-z])\}?", r"\1", value)
    value = LABEL_RE.sub(" ", value)
    value = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", value)
    value = COMMAND_RE.sub(" ", value)
    value = value.translate(str.maketrans("{}$~^_&", "       "))
    value = unicodedata.normalize("NFKC", value)
    value = SPACE_RE.sub(" ", value).strip()
    return value[:limit]


def line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer("\n", text))
    return starts


def line_at(starts: list[int], pos: int) -> int:
    return bisect.bisect_right(starts, pos)


def section_events(text: str) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for match in SECTION_RE.finditer(text):
        title, end = brace_arg(text, match.end() - 1)
        label_match = LABEL_RE.search(text, end, min(len(text), end + 500))
        events.append(
            {
                "pos": match.start(),
                "kind": match.group(1),
                "title": plain(title, 180),
                "label": label_match.group(1) if label_match else "",
            }
        )
    return events


def verbatim_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start_token = "\\begin{verbatim}"
    end_token = "\\end{verbatim}"
    cursor = 0
    while True:
        start = text.find(start_token, cursor)
        if start < 0:
            break
        end = text.find(end_token, start + len(start_token))
        if end < 0:
            ranges.append((start, len(text)))
            break
        ranges.append((start, end + len(end_token)))
        cursor = end + len(end_token)
    return ranges


def inside_ranges(pos: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in ranges)


def enclosing_text(text: str, short_label: str, pos: int) -> str:
    kind = short_label.split("-", 1)[0]
    if kind in {"section", "subsection", "subsubsection"}:
        start = text.rfind("\\section", 0, pos)
        if kind != "section":
            start = text.rfind(f"\\{kind}", 0, pos)
        return text[max(0, start) : pos + 200]
    begin = f"\\begin{{{kind}}}"
    end = f"\\end{{{kind}}}"
    start = text.rfind(begin, 0, pos)
    if start >= 0:
        stop = text.find(end, pos)
        if stop >= 0:
            return text[start : stop + len(end)]
    left = text.rfind("\n", 0, max(0, pos - 500))
    right = text.find("\n", min(len(text), pos + 500))
    return text[max(0, left) : right if right >= 0 else len(text)]


def load_tags() -> tuple[dict[str, str], list[str]]:
    tags: dict[str, str] = {}
    errors: list[str] = []
    path = ROOT / "tags" / "tags"
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        try:
            tag, full_label = raw.split(",", 1)
        except ValueError:
            errors.append(f"malformed tag line {number}")
            continue
        if full_label in tags:
            errors.append(f"duplicate full label in tags: {full_label}")
        tags[full_label] = tag
    return tags, errors


def build_index() -> tuple[
    list[dict[str, str]], list[str], list[str], dict[str, str]
]:
    tags, errors = load_tags()
    warnings: list[str] = []
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    tex_hashes: dict[str, str] = {}
    for path in sorted(ROOT.glob("*.tex"), key=lambda item: item.name):
        text = path.read_text(encoding="utf-8")
        tex_hashes[path.name] = sha256(path)
        starts = line_starts(text)
        sections = section_events(text)
        literals = verbatim_ranges(text)
        section_positions = [int(item["pos"]) for item in sections]
        title_match = TITLE_RE.search(text)
        chapter = path.stem
        if title_match:
            chapter, _ = brace_arg(text, title_match.end() - 1)
            chapter = plain(chapter, 120)
        for match in LABEL_RE.finditer(text):
            if inside_ranges(match.start(), literals):
                continue
            short_label = match.group(1)
            full_label = f"{path.stem}-{short_label}"
            if full_label in seen:
                errors.append(f"duplicate TeX full label: {full_label}")
            seen.add(full_label)
            sec_index = bisect.bisect_right(section_positions, match.start()) - 1
            section = sections[sec_index] if sec_index >= 0 else None
            body = plain(enclosing_text(text, short_label, match.start()))
            rows.append(
                {
                    "tag": tags.get(full_label, ""),
                    "full_label": full_label,
                    "file": path.name,
                    "line": str(line_at(starts, match.start())),
                    "kind": short_label.split("-", 1)[0],
                    "short_label": short_label,
                    "chapter": chapter,
                    "section_label": str(section["label"]) if section else "",
                    "section_title": str(section["title"]) if section else "",
                    "text_sha256": hashlib.sha256(
                        body.encode("utf-8")
                    ).hexdigest().upper(),
                    "_text": body,
                }
            )
    missing_tex = sorted(set(tags) - seen)
    missing_tags = sorted(seen - set(tags))
    for full_label in missing_tex:
        if full_label.startswith("book-part-"):
            warnings.append(f"generated book label is outside chapter TeX: {full_label}")
        else:
            errors.append(f"tag points outside indexed TeX: {full_label}")
    for full_label in missing_tags:
        warnings.append(f"TeX label has no official tag in this snapshot: {full_label}")
    return rows, errors, warnings, tex_hashes


def load_topics() -> list[dict[str, str]]:
    with (OUT / "topics.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["topic_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate topic_id in topics.csv")
    return rows


def candidate_rows(
    index: list[dict[str, str]], topics: list[dict[str, str]]
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for topic in topics:
        pattern = re.compile(topic["pattern"], re.IGNORECASE)
        matches: list[tuple[int, str, dict[str, str], list[str]]] = []
        for row in index:
            fields = {
                "label": f"{row['short_label']} {row['full_label']}",
                "chapter": row["chapter"],
                "section": row["section_title"],
                "text": row["_text"],
            }
            hit_fields = [name for name, value in fields.items() if pattern.search(value)]
            if not hit_fields:
                continue
            score = 0
            score += 90 if "label" in hit_fields else 0
            score += 70 if "section" in hit_fields else 0
            score += 45 if "chapter" in hit_fields else 0
            score += 20 if "text" in hit_fields else 0
            score += min(20, sum(len(pattern.findall(value)) for value in fields.values()))
            matches.append((score, row["full_label"], row, hit_fields))
        matches.sort(key=lambda item: (-item[0], item[1]))
        for score, _, row, hit_fields in matches[: int(topic["cap"])]:
            output.append(
                {
                    "topic_id": topic["topic_id"],
                    "score": str(score),
                    "hit_fields": ";".join(hit_fields),
                    "tag": row["tag"],
                    "full_label": row["full_label"],
                    "file": row["file"],
                    "line": row["line"],
                    "kind": row["kind"],
                    "section_title": row["section_title"],
                    "snippet": row["_text"],
                    "status": "lexical_candidate_only",
                }
            )
    return output


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    index, errors, warnings, tex_hashes = build_index()
    topics = load_topics()
    candidates = candidate_rows(index, topics)
    index_path = OUT / "stx.csv"
    candidate_path = OUT / "tcand.csv"
    check_path = OUT / "check.json"
    write_csv(
        index_path,
        index,
        [
            "tag",
            "full_label",
            "file",
            "line",
            "kind",
            "short_label",
            "chapter",
            "section_label",
            "section_title",
            "text_sha256",
        ],
    )
    write_csv(
        candidate_path,
        candidates,
        [
            "topic_id",
            "score",
            "hit_fields",
            "tag",
            "full_label",
            "file",
            "line",
            "kind",
            "section_title",
            "snippet",
            "status",
        ],
    )
    check = {
        "schema": "fga-stacks-index-v1",
        "source_commit": git_commit(),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "tex_files": len(tex_hashes),
            "labels": len(index),
            "official_tags_joined": sum(1 for row in index if row["tag"]),
            "topics": len(topics),
            "topic_candidates": len(candidates),
        },
        "sha256": {
            "tags/tags": sha256(ROOT / "tags" / "tags"),
            "fga/topics.csv": sha256(OUT / "topics.csv"),
            "fga/stx.csv": sha256(index_path),
            "fga/tcand.csv": sha256(candidate_path),
        },
        "tex_sha256": tex_hashes,
    }
    check_path.write_text(
        json.dumps(check, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
