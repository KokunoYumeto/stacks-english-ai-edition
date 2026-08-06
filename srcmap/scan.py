#!/usr/bin/env python3
"""Build a Stacks label index and bounded candidates for one corpus."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "fga"))
import mkidx as fidx  # noqa: E402


def read_topics(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["topic_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate topic IDs")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_dir", type=Path)
    args = parser.parse_args()
    out = args.corpus_dir.resolve()
    cfg = json.loads((out / "cfg.json").read_text(encoding="utf-8"))
    topics = read_topics(out / "topics.csv")
    index, errors, warnings, tex_hashes = fidx.build_index()
    candidates = fidx.candidate_rows(index, topics)
    topic_map, map_errors, map_warnings = fidx.topic_map_rows(index, topics)
    errors.extend(map_errors)
    warnings.extend(map_warnings)
    index_path = out / "stx.csv"
    candidate_path = out / "tcand.csv"
    topic_path = out / "tmap.csv"
    fidx.write_csv(
        index_path,
        index,
        [
            "tag", "full_label", "file", "line", "kind", "short_label",
            "chapter", "section_label", "section_title", "text_sha256",
        ],
    )
    fidx.write_csv(
        candidate_path,
        candidates,
        [
            "topic_id", "score", "hit_fields", "tag", "full_label", "file",
            "line", "kind", "section_title", "snippet", "status",
        ],
    )
    fidx.write_csv(
        topic_path,
        topic_map,
        [
            "topic_id", "label", "coverage", "confidence", "evidence_labels",
            "evidence_tags", "rationale", "review_state",
        ],
    )
    coverage = Counter(row["coverage"] for row in topic_map)
    result = {
        "schema": "historical-source-stacks-index-v1",
        "corpus": out.name,
        "official_upstream": cfg["official_upstream"],
        "integration_base": cfg["integration_base"],
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "tex_files": len(tex_hashes),
            "labels": len(index),
            "official_tags_joined": sum(1 for row in index if row["tag"]),
            "topics": len(topics),
            "topic_candidates": len(candidates),
            "topic_coverage": dict(sorted(coverage.items())),
        },
        "sha256": {
            "tags/tags": fidx.sha256(ROOT / "tags" / "tags"),
            f"{out.name}/topics.csv": fidx.sha256(out / "topics.csv"),
            f"{out.name}/stx.csv": fidx.sha256(index_path),
            f"{out.name}/tcand.csv": fidx.sha256(candidate_path),
            f"{out.name}/tmap.csv": fidx.sha256(topic_path),
        },
        "tex_sha256": tex_hashes,
    }
    (out / "check.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
