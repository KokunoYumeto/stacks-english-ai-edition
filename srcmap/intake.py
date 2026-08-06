#!/usr/bin/env python3
"""Convert frozen corpus scaffolds to a common source-unit inventory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "fga"))
import mkidx as fidx  # noqa: E402


FIELDS = [
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
    "source_file",
    "source_line",
    "topics",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify(path: Path, expected: dict[str, object]) -> dict[str, object]:
    actual = {
        "name": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    if actual["bytes"] != int(expected["bytes"]):
        raise RuntimeError(f"Input byte mismatch: {expected['name']}")
    if actual["sha256"] != expected["sha256"]:
        raise RuntimeError(f"Input hash mismatch: {expected['name']}")
    return actual


def nearest_parent(unit_id: str, ids: set[str], root_id: str) -> str:
    parts = unit_id.split(":")
    for size in range(len(parts) - 1, 0, -1):
        candidate = ":".join(parts[:size])
        if candidate in ids:
            return candidate
    return root_id


def topic_ids(text: str, rules: list[dict[str, str]]) -> str:
    hits = [
        rule["topic_id"]
        for rule in rules
        if re.search(rule["pattern"], text, re.IGNORECASE)
    ]
    return ";".join(sorted(set(hits)))


def target_units(
    rows: list[dict[str, str]], cfg: dict, adapter: str
) -> list[dict[str, str]]:
    id_field = "target_id"
    ids = {row[id_field] for row in rows}
    root_id = cfg["root_id"]
    rules = cfg.get("topic_rules", [])
    authority = cfg["authority"][0]["sha256"]
    output: list[dict[str, str]] = []
    for row in rows:
        unit_id = row[id_field]
        if adapter == "fac_targets":
            raw_type = row["target_type"]
            visible = row["visible_locator"]
            source_file = row["source_file"]
            source_line = row["source_line"]
            item = row.get("fac_number", "") or unit_id
        else:
            raw_type = row["target_class"]
            visible = row["visible_anchor"]
            source_file = row["source_file"]
            source_line = row["source_line"]
            item = unit_id
            if raw_type == "semantic_anchor":
                if ":item:" in unit_id:
                    raw_type = "subitem"
                else:
                    code = (
                        unit_id.split(":")[1]
                        if ":" in unit_id
                        else "result"
                    )
                    raw_type = {
                        "def": "definition",
                        "prop": "proposition",
                        "lemma": "lemma",
                        "cor": "corollary",
                        "thm": "theorem",
                        "remark": "remark",
                        "eq": "equation",
                    }.get(code, "semantic_anchor")
        title = fidx.plain(visible, 260) or unit_id.replace(":", " ")
        search = " ".join([unit_id, raw_type, visible, source_file])
        output.append(
            {
                "id": unit_id,
                "work": cfg["corpus"],
                "item": item,
                "unit_type": raw_type,
                "parent_id": nearest_parent(unit_id, ids, root_id),
                "title_en": title,
                "summary_en": title,
                "source_start": f"{source_file}:{source_line}",
                "source_end": f"{source_file}:{source_line}",
                "authority_sha256": authority,
                "source_file": source_file,
                "source_line": source_line,
                "topics": topic_ids(search, rules),
            }
        )
    return output


def tohoku_units(rows: list[dict[str, str]], cfg: dict) -> list[dict[str, str]]:
    rules = cfg.get("topic_rules", [])
    first_auth = cfg["authority"][0]["sha256"]
    second_auth = cfg["authority"][1]["sha256"]
    output: list[dict[str, str]] = []
    for number, row in enumerate(rows, 2):
        first = int(row["first_page"]) if row["first_page"] else 0
        last = int(row["last_page"]) if row["last_page"] else first
        if last and last <= 183:
            authority = first_auth
        elif first and first >= 185:
            authority = second_auth
        else:
            authority = f"{first_auth};{second_auth}"
        title = fidx.plain(row["en_label"], 260) or row["node_id"].replace(":", " ")
        search = " ".join(
            [row["node_id"], row["node_type"], row["en_label"], row["provenance"]]
        )
        output.append(
            {
                "id": row["node_id"],
                "work": cfg["corpus"],
                "item": row["pages"],
                "unit_type": row["node_type"],
                "parent_id": row["parent_id"] or cfg["root_id"],
                "title_en": title,
                "summary_en": fidx.plain(row["provenance"], 280),
                "source_start": row["first_page"],
                "source_end": row["last_page"],
                "authority_sha256": authority,
                "source_file": "sem/r7/nodes.csv",
                "source_line": str(number),
                "topics": topic_ids(search, rules),
            }
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_dir", type=Path)
    parser.add_argument("primary", type=Path)
    parser.add_argument("--extra", action="append", default=[])
    args = parser.parse_args()
    corpus_dir = args.corpus_dir.resolve()
    cfg_path = corpus_dir / "cfg.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    inputs = [verify(args.primary.resolve(), cfg["inputs"]["primary"])]
    for value in args.extra:
        key, raw_path = value.split("=", 1)
        inputs.append(verify(Path(raw_path).resolve(), cfg["inputs"][key]))
    source_rows = load_csv(args.primary.resolve())
    adapter = cfg["adapter"]
    if adapter in {"fac_targets", "gaga_targets"}:
        units = target_units(source_rows, cfg, adapter)
    elif adapter == "tohoku_nodes":
        units = tohoku_units(source_rows, cfg)
    else:
        raise RuntimeError(f"Unknown adapter: {adapter}")

    errors: list[str] = []
    ids = [row["id"] for row in units]
    if len(ids) != len(set(ids)):
        errors.append("duplicate unit IDs")
    known = set(ids) | {cfg["root_id"]}
    for row in units:
        if row["parent_id"] not in known:
            errors.append(f"unknown parent: {row['id']} -> {row['parent_id']}")
    if len(units) != int(cfg["expected_units"]):
        errors.append(f"expected {cfg['expected_units']} units, found {len(units)}")
    declared_topics = {
        row["topic_id"] for row in load_csv(corpus_dir / "topics.csv")
    }
    used_topics = {
        topic
        for row in units
        for topic in row["topics"].split(";")
        if topic
    }
    for topic in sorted(used_topics - declared_topics):
        errors.append(f"unknown generated topic: {topic}")

    units_path = corpus_dir / "units.csv"
    write_csv(units_path, units)
    result = {
        "schema": "historical-source-intake-v1",
        "corpus": cfg["corpus"],
        "adapter": adapter,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "inputs": inputs,
        "counts": {
            "units": len(units),
            "units_with_topics": sum(1 for row in units if row["topics"]),
        },
        "outputs": {
            "units.csv": {
                "bytes": units_path.stat().st_size,
                "sha256": sha256(units_path),
            }
        },
    }
    (corpus_dir / "intake.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
