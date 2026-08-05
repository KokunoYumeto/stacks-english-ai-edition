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

from mkidx import OUT, build_index, git_commit, plain, sha256, write_csv


EXPECTED_SHA = "D5E898D40B5AA51824ADF77EE6BA5E41DDF4FFA7B42E3754FBB91B81BA5F42FB"
EXPECTED_UNITS = 1253
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


def intake_rows(units: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in units:
        kind = row["unit_type"]
        if kind in STRUCTURAL:
            disposition = "structural_only"
            state = "classified"
            rationale = "Source or corpus structure; no independent Stacks object."
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
                "disposition": disposition,
                "review_state": state,
                "stacks_labels": "",
                "stacks_tags": "",
                "rationale": rationale,
            }
        )
    return output


def bm25_candidates(
    units: list[dict[str, str]], index: list[dict[str, str]], limit: int = 12
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
        if unit["unit_type"] in STRUCTURAL | HISTORICAL:
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
    if len(sys.argv) != 2:
        print("usage: python fga/mkmap.py PATH/TO/units.csv", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    units, errors = load_units(source)
    index, index_errors, index_warnings, _ = build_index()
    errors.extend(index_errors)
    mapped = intake_rows(units)
    candidates = bm25_candidates(units, index)
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
    errors.extend(privacy_errors([map_path, candidate_path]))
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
        "schema": "fga-stacks-map-v1",
        "source_commit": git_commit(),
        "source": {
            "name": source.name,
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        },
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": index_warnings,
        "counts": {
            "units": len(units),
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
        },
        "sha256": {
            "fga/map.csv": sha256(map_path),
            "fga/ucand.csv": sha256(candidate_path),
        },
    }
    check_path.write_text(
        json.dumps(check, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
