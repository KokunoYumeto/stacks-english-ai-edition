#!/usr/bin/env python3
"""Create the complete FGA unit intake and lexical Stacks candidates."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from mkidx import (
    OUT,
    build_index,
    load_topics,
    plain,
    sha256,
    topic_map_rows,
    upstream_commit,
    write_csv,
)


EXPECTED_SHA = "D5E898D40B5AA51824ADF77EE6BA5E41DDF4FFA7B42E3754FBB91B81BA5F42FB"
EXPECTED_UNITS = 1253
EXPECTED_TERMS_SHA = "D93D861C338DD62C56624A551A41CBBB216DB302087F47AA7B02CD44546F6622"
EXPECTED_TERMS = 1612
ITEMS = {
    "149",
    "e149",
    "182",
    "e182",
    "190",
    "e190",
    "195",
    "e195",
    "212",
    "e212",
    "221",
    "e221",
    "232",
    "e232",
    "236",
    "e236",
    "com",
}
STRUCTURAL = {
    "expose",
    "source_page",
    "bibliography",
    "bibliography_item",
}
HISTORICAL = {"erratum", "comment"}
EMBEDDED = {"equation", "subitem", "diagram"}
DOC_KINDS = {
    "section",
    "subsection",
    "subsubsection",
    "theorem",
    "proposition",
    "lemma",
    "definition",
    "remark",
    "remarks",
    "example",
    "exercise",
    "situation",
}
TOKEN_RE = re.compile(r"[a-z][a-z0-9-]{1,}")
STOP = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "can",
    "corollary",
    "does",
    "each",
    "equation",
    "every",
    "following",
    "for",
    "from",
    "has",
    "have",
    "hence",
    "here",
    "into",
    "isomorphism",
    "lemma",
    "let",
    "more",
    "not",
    "one",
    "only",
    "over",
    "proposition",
    "section",
    "set",
    "such",
    "suppose",
    "than",
    "that",
    "the",
    "their",
    "then",
    "theorem",
    "there",
    "these",
    "this",
    "those",
    "through",
    "under",
    "where",
    "which",
    "with",
}


def tokens(text: str) -> list[str]:
    value = plain(text, limit=max(280, len(text))).lower()
    return [token for token in TOKEN_RE.findall(value) if token not in STOP]


def load_units(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    if sha256(path) != EXPECTED_SHA:
        errors.append("units.csv SHA-256 does not match the published FGA inventory")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "id",
        "work",
        "item",
        "unit_type",
        "parent_id",
        "title_en",
        "summary_en",
        "source_start",
        "source_end",
        "authority_sha256",
        "fr_file",
        "fr_line",
        "en_file",
        "en_line",
    }
    if rows and not required.issubset(rows[0]):
        errors.append("units.csv is missing required columns")
    if len(rows) != EXPECTED_UNITS:
        errors.append(f"expected {EXPECTED_UNITS} units, found {len(rows)}")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate FGA unit IDs")
    known = set(ids) | {"fga"}
    for row in rows:
        if row["work"] != "FGA":
            errors.append(f"non-FGA work in unit {row['id']}")
        if row["item"] not in ITEMS:
            errors.append(f"out-of-scope item in unit {row['id']}")
        if row["parent_id"] not in known:
            errors.append(f"unknown parent for unit {row['id']}")
    return rows, errors


def load_terms(
    path: Path, unit_ids: set[str], topic_ids: set[str]
) -> tuple[dict[str, set[str]], list[str], int]:
    errors: list[str] = []
    if sha256(path) != EXPECTED_TERMS_SHA:
        errors.append("terms.csv SHA-256 does not match the published FGA inventory")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_TERMS:
        errors.append(f"expected {EXPECTED_TERMS} term links, found {len(rows)}")
    links: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        unit_id = row.get("unit_id", "")
        topic_id = row.get("concept_id", "")
        if unit_id not in unit_ids:
            errors.append(f"unknown unit in terms.csv: {unit_id}")
            continue
        if topic_id not in topic_ids:
            errors.append(f"unknown topic in terms.csv: {topic_id}")
            continue
        links[unit_id].add(topic_id)
    return links, errors, len(rows)


def intake_rows(
    units: list[dict[str, str]],
    term_links: dict[str, set[str]],
    topic_map: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in units:
        kind = row["unit_type"]
        topics = sorted(term_links.get(row["id"], set()))
        topic_labels = sorted(
            {
                label
                for topic in topics
                for label in topic_map[topic]["evidence_labels"].split(";")
                if label
            }
        )
        topic_tags = sorted(
            {
                tag
                for topic in topics
                for tag in topic_map[topic]["evidence_tags"].split(";")
                if tag
            }
        )
        if kind in STRUCTURAL:
            disposition = "structural_only"
            state = "classified"
            rationale = "Source or corpus structure; no independent Stacks object."
        elif kind in EMBEDDED:
            disposition = "structural_only"
            state = "inherits_parent"
            rationale = "Embedded component; use the parent unit's semantic disposition."
        elif kind in HISTORICAL:
            disposition = "historical_reference"
            state = "needs_link_review"
            rationale = "Correction or historical framing; link to affected units."
        else:
            disposition = "needs_review"
            state = "generated_intake"
            rationale = "Requires statement-level mathematical comparison."
        output.append(
            {
                "unit_id": row["id"],
                "item": row["item"],
                "unit_type": kind,
                "parent_id": row["parent_id"],
                "source_start": row["source_start"],
                "source_end": row["source_end"],
                "fr_loc": f"{row['fr_file']}:{row['fr_line']}",
                "en_loc": f"{row['en_file']}:{row['en_line']}",
                "authority_sha256": row["authority_sha256"],
                "fga_topics": ";".join(topics),
                "topic_evidence_labels": ";".join(topic_labels),
                "topic_evidence_tags": ";".join(topic_tags),
                "disposition": disposition,
                "review_state": state,
                "stacks_labels": "",
                "stacks_tags": "",
                "rationale": rationale,
            }
        )
    return output


def bm25_candidates(
    units: list[dict[str, str]],
    index: list[dict[str, str]],
    include_ids: set[str],
    limit: int = 12,
) -> list[dict[str, str]]:
    docs = [row for row in index if row["kind"] in DOC_KINDS]
    doc_tokens: list[list[str]] = []
    postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for number, row in enumerate(docs):
        text = " ".join(
            [
                row["chapter"],
                row["section_title"],
                row["short_label"].replace("-", " "),
                row["_text"],
            ]
        )
        values = tokens(text)
        doc_tokens.append(values)
        for term, frequency in Counter(values).items():
            postings[term].append((number, frequency))
    document_count = len(docs)
    average_length = sum(map(len, doc_tokens)) / max(1, document_count)
    output: list[dict[str, str]] = []
    for unit in units:
        if unit["id"] not in include_ids:
            continue
        if unit["unit_type"] in STRUCTURAL | HISTORICAL | EMBEDDED:
            continue
        query_text = " ".join([unit["title_en"], unit["summary_en"]])
        query = Counter(tokens(query_text))
        scores: dict[int, float] = defaultdict(float)
        overlap: dict[int, set[str]] = defaultdict(set)
        for term, query_frequency in query.items():
            posting = postings.get(term, [])
            if not posting:
                continue
            document_frequency = len(posting)
            inverse = math.log(
                1 + (document_count - document_frequency + 0.5)
                / (document_frequency + 0.5)
            )
            for number, frequency in posting:
                length = len(doc_tokens[number])
                normalizer = frequency + 1.5 * (
                    1 - 0.75 + 0.75 * length / max(1, average_length)
                )
                scores[number] += (
                    inverse * frequency * 2.5 / normalizer
                    * min(2, query_frequency)
                )
                overlap[number].add(term)
        ranked = sorted(
            scores,
            key=lambda number: (-scores[number], docs[number]["full_label"]),
        )[:limit]
        query_hash = hashlib.sha256(query_text.encode("utf-8")).hexdigest().upper()
        if not ranked:
            output.append(
                {
                    "unit_id": unit["id"],
                    "unit_type": unit["unit_type"],
                    "unit_title": plain(unit["title_en"], 160),
                    "rank": "0",
                    "score": "0.000000",
                    "overlap": "",
                    "tag": "",
                    "full_label": "",
                    "file": "",
                    "line": "",
                    "kind": "",
                    "section_title": "",
                    "snippet": "",
                    "query_sha256": query_hash,
                    "status": "no_lexical_candidate",
                }
            )
            continue
        for rank, number in enumerate(ranked, 1):
            row = docs[number]
            output.append(
                {
                    "unit_id": unit["id"],
                    "unit_type": unit["unit_type"],
                    "unit_title": plain(unit["title_en"], 160),
                    "rank": str(rank),
                    "score": f"{scores[number]:.6f}",
                    "overlap": ";".join(sorted(overlap[number])),
                    "tag": row["tag"],
                    "full_label": row["full_label"],
                    "file": row["file"],
                    "line": row["line"],
                    "kind": row["kind"],
                    "section_title": row["section_title"],
                    "snippet": row["_text"],
                    "query_sha256": query_hash,
                    "status": "lexical_candidate_only",
                }
            )
    return output


def load_decisions(
    path: Path,
    mapped: list[dict[str, str]],
    index: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    allowed = {
        "existing_equivalent",
        "existing_stronger",
        "existing_weaker",
        "extend_existing",
        "new_statement",
        "new_section",
        "example_or_remark",
        "historical_reference",
        "outside_scope",
        "structural_only",
        "needs_review",
    }
    unit_ids = {row["unit_id"] for row in mapped}
    stack_rows = {row["full_label"]: row for row in index}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        decisions = list(csv.DictReader(handle))
    errors: list[str] = []
    seen_ids: set[str] = set()
    current: dict[str, str] = {}
    for row in decisions:
        decision_id = row.get("decision_id", "")
        unit_id = row.get("unit_id", "")
        action = row.get("action", "")
        if not re.fullmatch(r"D[0-9]{6}", decision_id):
            errors.append(f"invalid decision ID: {decision_id}")
        if decision_id in seen_ids:
            errors.append(f"duplicate decision ID: {decision_id}")
        seen_ids.add(decision_id)
        if unit_id not in unit_ids:
            errors.append(f"unknown decision unit: {unit_id}")
        if row.get("disposition", "") not in allowed:
            errors.append(f"invalid disposition in {decision_id}")
        if not row.get("rationale", ""):
            errors.append(f"missing rationale in {decision_id}")
        if not row.get("review_state", ""):
            errors.append(f"missing review state in {decision_id}")
        prior = current.get(unit_id, "")
        if action == "set":
            if prior:
                errors.append(f"silent replacement of {unit_id} in {decision_id}")
            if row.get("supersedes", ""):
                errors.append(f"set decision has supersedes in {decision_id}")
        elif action == "replace":
            if not prior or row.get("supersedes", "") != prior:
                errors.append(f"bad supersession chain in {decision_id}")
        else:
            errors.append(f"invalid action in {decision_id}: {action}")
        labels = [value for value in row.get("stacks_labels", "").split(";") if value]
        tags: list[str] = []
        for label in labels:
            if label not in stack_rows:
                errors.append(f"unknown Stacks label in {decision_id}: {label}")
                continue
            if stack_rows[label]["tag"]:
                tags.append(stack_rows[label]["tag"])
        row["_stacks_tags"] = ";".join(tags)
        current[unit_id] = decision_id
    return decisions, errors


def apply_decisions(
    mapped: list[dict[str, str]], decisions: list[dict[str, str]]
) -> None:
    by_unit = {row["unit_id"]: row for row in mapped}
    for decision in decisions:
        row = by_unit[decision["unit_id"]]
        row["decision_id"] = decision["decision_id"]
        row["disposition"] = decision["disposition"]
        row["review_state"] = decision["review_state"]
        row["stacks_labels"] = decision["stacks_labels"]
        row["stacks_tags"] = decision["_stacks_tags"]
        row["rationale"] = decision["rationale"]


def privacy_errors(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    patterns = (
        re.compile(r"[a-z]:\\users\\", re.IGNORECASE),
        re.compile(r"/home/[^/]+/", re.IGNORECASE),
    )
    for path in paths:
        value = path.read_text(encoding="utf-8")
        for pattern in patterns:
            if pattern.search(value):
                errors.append(f"private path in {path.name}")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: python fga/mkmap.py PATH/TO/units.csv PATH/TO/terms.csv",
            file=sys.stderr,
        )
        return 2
    source = Path(sys.argv[1]).resolve()
    terms_source = Path(sys.argv[2]).resolve()
    units, errors = load_units(source)
    index, index_errors, index_warnings, _ = build_index()
    errors.extend(index_errors)
    topics = load_topics()
    topic_rows, topic_errors, topic_warnings = topic_map_rows(index, topics)
    errors.extend(topic_errors)
    index_warnings.extend(topic_warnings)
    topic_map = {row["topic_id"]: row for row in topic_rows}
    term_links, term_errors, term_count = load_terms(
        terms_source,
        {row["id"] for row in units},
        set(topic_map),
    )
    errors.extend(term_errors)
    mapped = intake_rows(units, term_links, topic_map)
    decisions, decision_errors = load_decisions(OUT / "dec.csv", mapped, index)
    errors.extend(decision_errors)
    apply_decisions(mapped, decisions)
    review_ids = {
        row["unit_id"] for row in mapped if row["disposition"] == "needs_review"
    }
    candidates = bm25_candidates(units, index, review_ids)
    map_path = OUT / "map.csv"
    candidate_path = OUT / "ucand.csv"
    check_path = OUT / "mcheck.json"
    write_csv(
        map_path,
        mapped,
        [
            "unit_id",
            "item",
            "unit_type",
            "parent_id",
            "source_start",
            "source_end",
            "fr_loc",
            "en_loc",
            "authority_sha256",
            "fga_topics",
            "topic_evidence_labels",
            "topic_evidence_tags",
            "decision_id",
            "disposition",
            "review_state",
            "stacks_labels",
            "stacks_tags",
            "rationale",
        ],
    )
    write_csv(
        candidate_path,
        candidates,
        [
            "unit_id",
            "unit_type",
            "unit_title",
            "rank",
            "score",
            "overlap",
            "tag",
            "full_label",
            "file",
            "line",
            "kind",
            "section_title",
            "snippet",
            "query_sha256",
            "status",
        ],
    )
    errors.extend(privacy_errors([map_path, candidate_path, OUT / "dec.csv"]))
    review_units = sum(
        1 for row in mapped if row["disposition"] == "needs_review"
    )
    candidate_units = len({row["unit_id"] for row in candidates})
    if candidate_units != review_units:
        errors.append(
            f"candidate coverage {candidate_units} does not equal review units "
            f"{review_units}"
        )
    check = {
        "schema": "fga-stacks-map-v2",
        "upstream_commit": upstream_commit(),
        "sources": [
            {
                "name": source.name,
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
            },
            {
                "name": terms_source.name,
                "bytes": terms_source.stat().st_size,
                "sha256": sha256(terms_source),
            },
        ],
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": index_warnings,
        "counts": {
            "units": len(units),
            "term_links": term_count,
            "decisions": len(decisions),
            "decided_units": sum(1 for row in mapped if row.get("decision_id")),
            "units_with_topics": len(term_links),
            "structural_units": sum(
                1 for row in mapped if row["disposition"] == "structural_only"
            ),
            "historical_units": sum(
                1 for row in mapped if row["disposition"] == "historical_reference"
            ),
            "review_units": review_units,
            "candidate_units": candidate_units,
            "unit_candidates": len(candidates),
            "no_lexical_candidate_units": sum(
                1 for row in candidates if row["status"] == "no_lexical_candidate"
            ),
            "dispositions": dict(
                sorted(Counter(row["disposition"] for row in mapped).items())
            ),
        },
        "sha256": {
            "fga/dec.csv": sha256(OUT / "dec.csv"),
            "fga/map.csv": sha256(map_path),
            "fga/ucand.csv": sha256(candidate_path),
        },
    }
    with check_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(check, indent=2, sort_keys=True) + "\n")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
