#!/usr/bin/env python3
"""Generate metadata-only Stacks candidates for the EGA topic scaffold."""

import bisect
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ega"
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
SECTION_RE = re.compile(r"\\(section|subsection|subsubsection)\s*\{")
TITLE_RE = re.compile(r"\\title\s*\{")
COMMENT_RE = re.compile(r"(?<!\\)%.*$")
COMMAND_RE = re.compile(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?")
SPACE_RE = re.compile(r"\s+")


def sha(data):
    return hashlib.sha256(data).hexdigest().upper()


def brace_arg(text, open_brace):
    depth = 0
    for pos in range(open_brace, len(text)):
        char = text[pos]
        if char == "{" and (pos == 0 or text[pos - 1] != "\\"):
            depth += 1
        elif char == "}" and (pos == 0 or text[pos - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[open_brace + 1:pos], pos + 1
    raise ValueError(f"unclosed braced argument at {open_brace}")


def plain(text, limit=320):
    lines = [COMMENT_RE.sub("", line) for line in text.splitlines()]
    value = " ".join(lines)
    value = re.sub(r"\\['\"`^~=.Hckruvbdt]\s*\{?([A-Za-z])\}?", r"\1", value)
    value = LABEL_RE.sub(" ", value)
    value = re.sub(r"\\begin\{[^}]+\}|\\end\{[^}]+\}", " ", value)
    value = COMMAND_RE.sub(" ", value)
    value = value.translate(str.maketrans("{}$~^_&", "       "))
    value = unicodedata.normalize("NFKC", value)
    return SPACE_RE.sub(" ", value).strip()[:limit]


def line_starts(text):
    starts = [0]
    starts.extend(match.end() for match in re.finditer("\n", text))
    return starts


def line_at(starts, pos):
    return bisect.bisect_right(starts, pos)


def section_events(text):
    events = []
    for match in SECTION_RE.finditer(text):
        title, end = brace_arg(text, match.end() - 1)
        label = LABEL_RE.search(text, end, min(len(text), end + 500))
        events.append({
            "pos": match.start(),
            "kind": match.group(1),
            "title": plain(title, 180),
            "label": label.group(1) if label else "",
        })
    return events


def verbatim_ranges(text):
    ranges = []
    start_token = "\\begin{verbatim}"
    end_token = "\\end{verbatim}"
    cursor = 0
    while True:
        start = text.find(start_token, cursor)
        if start < 0:
            return ranges
        end = text.find(end_token, start + len(start_token))
        if end < 0:
            ranges.append((start, len(text)))
            return ranges
        ranges.append((start, end + len(end_token)))
        cursor = end + len(end_token)


def inside(pos, ranges):
    return any(start <= pos < end for start, end in ranges)


def enclosing_text(text, short_label, pos):
    kind = short_label.split("-", 1)[0]
    if kind in {"section", "subsection", "subsubsection"}:
        start = text.rfind(f"\\{kind}", 0, pos)
        return text[max(0, start):pos + 200]
    begin = f"\\begin{{{kind}}}"
    end = f"\\end{{{kind}}}"
    start = text.rfind(begin, 0, pos)
    if start >= 0:
        stop = text.find(end, pos)
        if stop >= 0:
            return text[start:stop + len(end)]
    left = text.rfind("\n", 0, max(0, pos - 500))
    right = text.find("\n", min(len(text), pos + 500))
    return text[max(0, left):right if right >= 0 else len(text)]


def git_blob(commit, path):
    return subprocess.check_output(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT
    )


def root_tex_paths(commit):
    output = subprocess.check_output(
        ["git", "ls-tree", "--name-only", commit], cwd=ROOT, text=True
    )
    return sorted(
        path for path in output.splitlines()
        if "/" not in path and path.endswith(".tex")
    )


def load_tags(commit):
    tags = {}
    errors = []
    data = git_blob(commit, "tags/tags")
    for number, raw in enumerate(data.decode("utf-8").splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        if "," not in raw:
            errors.append(f"malformed tag line {number}")
            continue
        tag, full_label = raw.split(",", 1)
        if full_label in tags:
            errors.append(f"duplicate tag label {full_label}")
        tags[full_label] = tag
    return tags, errors, data


def build_index(commit):
    tags, errors, tags_data = load_tags(commit)
    warnings = []
    rows = []
    seen = set()
    tex_manifest = []
    for name in root_tex_paths(commit):
        data = git_blob(commit, name)
        text = data.decode("utf-8")
        tex_manifest.append(f"{name}\t{len(data)}\t{sha(data)}\n")
        starts = line_starts(text)
        sections = section_events(text)
        positions = [event["pos"] for event in sections]
        literals = verbatim_ranges(text)
        title_match = TITLE_RE.search(text)
        stem = Path(name).stem
        chapter = stem
        if title_match:
            chapter = plain(brace_arg(text, title_match.end() - 1)[0], 120)
        for match in LABEL_RE.finditer(text):
            if inside(match.start(), literals):
                continue
            short = match.group(1)
            full = f"{stem}-{short}"
            if full in seen:
                errors.append(f"duplicate TeX full label {full}")
            seen.add(full)
            sec_index = bisect.bisect_right(positions, match.start()) - 1
            section = sections[sec_index] if sec_index >= 0 else None
            body = plain(enclosing_text(text, short, match.start()))
            rows.append({
                "tag": tags.get(full, ""),
                "full_label": full,
                "file": name,
                "line": str(line_at(starts, match.start())),
                "kind": short.split("-", 1)[0],
                "short_label": short,
                "chapter": chapter,
                "section_label": section["label"] if section else "",
                "section_title": section["title"] if section else "",
                "text_sha256": sha(body.encode("utf-8")),
                "_text": body,
            })
    missing_tex = sorted(set(tags) - seen)
    for full in missing_tex:
        if not full.startswith("book-part-"):
            errors.append(f"tag points outside chapter TeX: {full}")
    for full in sorted(seen - set(tags)):
        warnings.append(f"TeX label has no official tag: {full}")
    return (rows, errors, warnings,
            sha("".join(tex_manifest).encode("utf-8")), sha(tags_data))


def load_topics():
    with (OUT / "topics.csv").open(encoding="utf-8", newline="") as handle:
        topics = list(csv.DictReader(handle))
    ids = [row["topic_id"] for row in topics]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate topic ID")
    return topics


def candidate_rows(index, topics, cap=80):
    output = []
    counts = Counter()
    for topic in topics:
        pattern = re.compile(topic["discovery_pattern"], re.I)
        matches = []
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
            score = (90 if "label" in hit_fields else 0) + (70 if "section" in hit_fields else 0)
            score += (45 if "chapter" in hit_fields else 0) + (20 if "text" in hit_fields else 0)
            score += min(20, sum(len(pattern.findall(value)) for value in fields.values()))
            matches.append((score, row["full_label"], row, hit_fields))
        matches.sort(key=lambda item: (-item[0], item[1]))
        for score, _, row, hit_fields in matches[:cap]:
            output.append({
                "topic_id": topic["topic_id"],
                "rank": counts[topic["topic_id"]] + 1,
                "score": score,
                "hit_fields": ";".join(hit_fields),
                "official_tag": row["tag"],
                "full_label": row["full_label"],
                "file": row["file"],
                "line": row["line"],
                "kind": row["kind"],
                "section_label": row["section_label"],
                "text_sha256": row["text_sha256"],
                "status": "lexical_candidate_only",
            })
            counts[topic["topic_id"]] += 1
    return output, counts


def csv_bytes(fields, rows):
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true",
        help="verify generated artifacts without writing them")
    args = parser.parse_args()
    errors = []
    warnings = []
    scope = json.loads((OUT / "scope.json").read_text(encoding="utf-8"))
    upstream = scope["stacks_upstream"]
    resolved_upstream = subprocess.check_output(
        ["git", "rev-parse", f"{upstream}^{{commit}}"], cwd=ROOT, text=True
    ).strip()
    if resolved_upstream != upstream:
        errors.append("declared scaffold upstream does not resolve to its exact commit")
    index, index_errors, index_warnings, tex_tree, tags_sha = build_index(upstream)
    errors.extend(index_errors)
    warnings.extend(index_warnings)
    topics = load_topics()
    candidates, counts = candidate_rows(index, topics)
    fields = ["topic_id", "rank", "score", "hit_fields", "official_tag",
              "full_label", "file", "line", "kind", "section_label",
              "text_sha256", "status"]
    candidate_data = csv_bytes(fields, candidates)
    result = {
        "schema": "ega-stacks-candidate-map-v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "upstream": upstream,
        "tags_sha256": tags_sha,
        "tex_tree_sha256": tex_tree,
        "labels": len(index),
        "official_tag_joins": sum(bool(row["tag"]) for row in index),
        "topics": len(topics),
        "candidates": len(candidates),
        "candidate_counts": dict(sorted(counts.items())),
        "reviewed_mappings": 0,
        "official_tags_assigned_by_scaffold": 0,
        "copied_stacks_prose": False,
    }
    result_data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    artifact_errors = []
    if args.check:
        for path, expected in (
                (OUT / "cand.csv", candidate_data),
                (OUT / "map.json", result_data)):
            if not path.is_file() or path.read_bytes() != expected:
                artifact_errors.append(f"generated artifact differs: {path.name}")
    else:
        (OUT / "cand.csv").write_bytes(candidate_data)
        (OUT / "map.json").write_bytes(result_data)
    print(json.dumps(result, indent=2, sort_keys=True))
    for error in artifact_errors:
        print(error)
    raise SystemExit(1 if errors or artifact_errors else 0)


if __name__ == "__main__":
    main()
