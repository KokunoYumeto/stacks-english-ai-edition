#!/usr/bin/env python3
"""Apply append-only decisions to one common source-unit inventory."""

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
import mkmap as fmap  # noqa: E402


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_dir", type=Path)
    args = parser.parse_args()
    out = args.corpus_dir.resolve()
    cfg = json.loads((out / "cfg.json").read_text(encoding="utf-8"))
    intake = json.loads((out / "intake.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    units_path = out / "units.csv"
    if fidx.sha256(units_path) != intake["outputs"]["units.csv"]["sha256"]:
        errors.append("units.csv differs from the frozen intake")
    units = load_csv(units_path)
    if len(units) != int(cfg["expected_units"]):
        errors.append("unit count changed")
    index, index_errors, warnings, _ = fidx.build_index()
    errors.extend(index_errors)
    topics = load_csv(out / "topics.csv")
    topic_rows, topic_errors, topic_warnings = fidx.topic_map_rows(index, topics)
    errors.extend(topic_errors)
    warnings.extend(topic_warnings)
    topic_map = {row["topic_id"]: row for row in topic_rows}
    structural = set(cfg.get("structural_types", []))
    embedded = set(cfg.get("embedded_types", []))
    historical = set(cfg.get("historical_types", []))
    mapped: list[dict[str, str]] = []
    for unit in units:
        topic_ids = [value for value in unit["topics"].split(";") if value]
        unknown = sorted(set(topic_ids) - set(topic_map))
        if unknown:
            errors.append(f"unknown topics for {unit['id']}: {';'.join(unknown)}")
        labels = sorted(
            {
                label
                for topic in topic_ids
                if topic in topic_map
                for label in topic_map[topic]["evidence_labels"].split(";")
                if label
            }
        )
        tags = sorted(
            {
                tag
                for topic in topic_ids
                if topic in topic_map
                for tag in topic_map[topic]["evidence_tags"].split(";")
                if tag
            }
        )
        kind = unit["unit_type"]
        if kind in structural:
            disposition = "structural_only"
            state = "classified"
            rationale = "Source structure; no independent Stacks object."
        elif kind in embedded:
            disposition = "structural_only"
            state = "inherits_parent"
            rationale = "Embedded source component; inherit the parent disposition."
        elif kind in historical:
            disposition = "historical_reference"
            state = "needs_link_review"
            rationale = "Historical or bibliographic unit requiring source linkage."
        else:
            disposition = "needs_review"
            state = "generated_intake"
            rationale = "Requires statement-level mathematical comparison."
        mapped.append(
            {
                "unit_id": unit["id"],
                "item": unit["item"],
                "unit_type": kind,
                "parent_id": unit["parent_id"],
                "source_start": unit["source_start"],
                "source_end": unit["source_end"],
                "source_loc": f"{unit['source_file']}:{unit['source_line']}",
                "authority_sha256": unit["authority_sha256"],
                "source_topics": ";".join(topic_ids),
                "topic_evidence_labels": ";".join(labels),
                "topic_evidence_tags": ";".join(tags),
                "decision_id": "",
                "disposition": disposition,
                "review_state": state,
                "stacks_labels": "",
                "stacks_tags": "",
                "rationale": rationale,
            }
        )
    decisions, decision_errors = fmap.load_decisions(out / "dec.csv", mapped, index)
    errors.extend(decision_errors)
    fmap.apply_decisions(mapped, decisions)
    issues, issue_errors = fmap.load_issues(out / "issues.csv", mapped, index, decisions)
    errors.extend(issue_errors)
    review_ids = {
        row["unit_id"] for row in mapped if row["disposition"] == "needs_review"
    }
    candidates = fmap.bm25_candidates(units, index, review_ids)
    candidate_ids = {row["unit_id"] for row in candidates}
    if candidate_ids != review_ids:
        errors.append("candidate unit set differs from review unit set")
    map_path = out / "map.csv"
    candidate_path = out / "ucand.csv"
    fidx.write_csv(
        map_path,
        mapped,
        [
            "unit_id", "item", "unit_type", "parent_id", "source_start",
            "source_end", "source_loc", "authority_sha256", "source_topics",
            "topic_evidence_labels", "topic_evidence_tags", "decision_id",
            "disposition", "review_state", "stacks_labels", "stacks_tags",
            "rationale",
        ],
    )
    fidx.write_csv(
        candidate_path,
        candidates,
        [
            "unit_id", "unit_type", "unit_title", "rank", "score", "overlap",
            "tag", "full_label", "file", "line", "kind", "section_title",
            "snippet", "query_sha256", "status",
        ],
    )
    errors.extend(
        fmap.privacy_errors(
            [map_path, candidate_path, out / "dec.csv", out / "issues.csv"]
        )
    )
    result = {
        "schema": "historical-source-stacks-map-v1",
        "corpus": cfg["corpus"],
        "official_upstream": cfg["official_upstream"],
        "integration_base": cfg["integration_base"],
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "units": len(units),
            "decisions": len(decisions),
            "decided_units": sum(1 for row in mapped if row["decision_id"]),
            "source_issues": len(issues),
            "active_source_issues": sum(1 for row in issues if row["status"] != "resolved"),
            "review_units": len(review_ids),
            "candidate_units": len(candidate_ids),
            "unit_candidates": len(candidates),
            "dispositions": dict(sorted(Counter(row["disposition"] for row in mapped).items())),
        },
        "sha256": {
            f"{out.name}/cfg.json": fidx.sha256(out / "cfg.json"),
            f"{out.name}/intake.json": fidx.sha256(out / "intake.json"),
            f"{out.name}/units.csv": fidx.sha256(units_path),
            f"{out.name}/dec.csv": fidx.sha256(out / "dec.csv"),
            f"{out.name}/issues.csv": fidx.sha256(out / "issues.csv"),
            f"{out.name}/map.csv": fidx.sha256(map_path),
            f"{out.name}/ucand.csv": fidx.sha256(candidate_path),
        },
    }
    (out / "mcheck.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
