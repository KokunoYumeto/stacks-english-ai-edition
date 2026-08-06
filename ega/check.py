#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ERRORS = []


def rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


scope = json.loads((ROOT / "scope.json").read_text(encoding="utf-8"))
if scope.get("status") != "discovery_scaffold":
    ERRORS.append("scope status must remain discovery_scaffold")
if scope.get("stacks_upstream") != "a04446e57ec1fbc252a871afcec7752fb2807b14":
    ERRORS.append("unexpected upstream identity")

interface = json.loads((ROOT / "interface.json").read_text(encoding="utf-8"))
if interface.get("status") != "active" or interface.get("ownership", {}).get("cross_tree_writes") is not False:
    ERRORS.append("edition interface is not active/read-only")
if interface.get("english_discovery", {}).get("manifest_sha256") != scope["inputs"]["english_discovery"]["manifest_sha256"]:
    ERRORS.append("edition interface English manifest mismatch")
if interface.get("french_cursor", {}).get("page_gate_sha256") != scope["inputs"]["french_authority"]["page_gate_sha256"]:
    ERRORS.append("edition interface French page-gate mismatch")

tables = {
    "src.csv": ("source_id", re.compile(r"ega\.[a-z0-9.-]+$")),
    "topics.csv": ("topic_id", re.compile(r"ega-topic-[a-z0-9-]+$")),
    "dec.csv": ("decision_id", re.compile(r"D\d{6}$")),
    "issues.csv": ("issue_id", re.compile(r"I\d{6}$")),
    "fb.csv": ("feedback_id", re.compile(r"F\d{6}$")),
}

counts = {}

generated = {
    "files.csv": "relative_path",
    "units.csv": "unit_id",
}
for name, field in generated.items():
    path = ROOT / name
    if path.exists():
        data = rows(name)
        counts[name] = len(data)
        values = [row[field] for row in data]
        if len(values) != len(set(values)):
            ERRORS.append(f"duplicate {field} in {name}")

if (ROOT / "units.csv").exists() and (ROOT / "files.csv").exists():
    unit_rows = rows("units.csv")
    unit_ids = {row["unit_id"] for row in unit_rows}
    file_ids = {row["relative_path"] for row in rows("files.csv")}
    logical_volumes = {"0", "I", "II", "III", "IV"}
    for row in unit_rows:
        if row["parent_id"] and row["parent_id"] not in unit_ids:
            ERRORS.append(f"missing parent {row['parent_id']} for {row['unit_id']}")
        if row["source_file"] and row["source_file"] not in file_ids:
            ERRORS.append(f"missing source file {row['source_file']} for {row['unit_id']}")
        if row["authority_state"] != "english_discovery":
            ERRORS.append(f"unexpected authority promotion for {row['unit_id']}")
        if row["review_state"] != "unreviewed":
            ERRORS.append(f"unexpected review promotion for {row['unit_id']}")
        if row["kind"] != "corpus" and row["volume"] not in logical_volumes:
            ERRORS.append(
                f"invalid logical volume {row['volume']!r} for {row['unit_id']}")

intake_path = ROOT / "intake.json"
if intake_path.exists():
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    if intake.get("status") != "PASS" or intake.get("errors"):
        ERRORS.append("intake receipt is not PASS/errors[]")
    if intake.get("source", {}).get("tree_sha256") != scope["inputs"]["english_discovery"]["tree_sha256"]:
        ERRORS.append("intake tree does not match scope")
    if intake.get("units") != scope["inputs"]["english_discovery"]["discovery_units"]:
        ERRORS.append("intake unit count does not match scope")

map_path = ROOT / "map.json"
if map_path.exists():
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    if mapping.get("status") != "PASS" or mapping.get("errors"):
        ERRORS.append("candidate-map receipt is not PASS/errors[]")
    if mapping.get("upstream") != scope["stacks_upstream"]:
        ERRORS.append("candidate-map upstream does not match scope")
    if mapping.get("reviewed_mappings") != 0:
        ERRORS.append("initial candidate map must not claim reviewed mappings")
    if mapping.get("official_tags_assigned_by_scaffold") != 0:
        ERRORS.append("candidate map claims assigned official tags")
    snapshot = scope.get("mapping_snapshot", {})
    expected_snapshot = {
        "stacks_labels": mapping.get("labels"),
        "official_tag_joins": mapping.get("official_tag_joins"),
        "topics": mapping.get("topics"),
        "lexical_candidates": mapping.get("candidates"),
        "reviewed_mappings": mapping.get("reviewed_mappings"),
        "official_tags_assigned_by_scaffold": mapping.get("official_tags_assigned_by_scaffold"),
    }
    if snapshot != expected_snapshot:
        ERRORS.append("scope mapping snapshot does not match candidate map")

cand_path = ROOT / "cand.csv"
if cand_path.exists():
    candidates = rows("cand.csv")
    counts["cand.csv"] = len(candidates)
    topic_ids = {row["topic_id"] for row in rows("topics.csv")}
    seen_candidates = set()
    for row in candidates:
        key = (row["topic_id"], row["full_label"])
        if key in seen_candidates:
            ERRORS.append(f"duplicate candidate {key}")
        seen_candidates.add(key)
        if row["topic_id"] not in topic_ids:
            ERRORS.append(f"candidate has unknown topic {row['topic_id']}")
        if row["status"] != "lexical_candidate_only":
            ERRORS.append(f"candidate promoted without review {key}")

tmap_path = ROOT / "tmap.csv"
existing_tags_referenced = set()
if tmap_path.exists():
    reviewed = rows("tmap.csv")
    counts["tmap.csv"] = len(reviewed)
    map_ids = [row["map_id"] for row in reviewed]
    if len(map_ids) != len(set(map_ids)):
        ERRORS.append("duplicate map_id in tmap.csv")
    for map_id in map_ids:
        if not re.fullmatch(r"M\d{6}", map_id):
            ERRORS.append(f"invalid map_id {map_id!r}")

    topic_ids = {row["topic_id"] for row in rows("topics.csv")}
    unit_ids = {row["unit_id"] for row in rows("units.csv")}
    tag_map = {}
    with (ROOT.parent / "tags" / "tags").open(encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.rstrip("\n")
            if not raw or "," not in raw:
                continue
            tag, label = raw.split(",", 1)
            tag_map[label] = tag
    french_sha = interface["french_cursor"]["manifest_sha256"]
    upstream = scope["stacks_upstream"]
    source_units = set()
    touched_topics = set()
    for row in reviewed:
        source_units.add(row["source_unit"])
        touched_topics.add(row["topic_id"])
        if row["topic_id"] not in topic_ids:
            ERRORS.append(f"reviewed mapping has unknown topic {row['topic_id']}")
        if row["source_unit"] not in unit_ids:
            ERRORS.append(f"reviewed mapping has unknown unit {row['source_unit']}")
        if row["authority_state"] != "french_admitted":
            ERRORS.append(f"reviewed mapping lacks French admission {row['map_id']}")
        if row["source_receipt_sha256"] != french_sha:
            ERRORS.append(f"reviewed mapping has wrong French receipt {row['map_id']}")
        if row["stacks_commit"] != upstream:
            ERRORS.append(f"reviewed mapping has wrong Stacks commit {row['map_id']}")
        if row["relation"] != "split":
            ERRORS.append(f"first review slice overclaims relation {row['map_id']}")
        if row["granularity"] != "source_subsection_to_stacks_section":
            ERRORS.append(f"unexpected mapping granularity {row['map_id']}")
        if row["review_state"] != "reviewed_existing":
            ERRORS.append(f"unexpected mapping state {row['map_id']}")
        if row["coverage_claim"] != "topical_overlap_only":
            ERRORS.append(f"first review slice overclaims coverage {row['map_id']}")

        target = ROOT.parent / row["stacks_file"]
        if not target.is_file():
            ERRORS.append(f"missing Stacks target {row['stacks_file']}")
        else:
            local_label = row["stacks_label"]
            prefix = target.stem + "-"
            if not local_label.startswith(prefix):
                ERRORS.append(f"target label/file mismatch {row['map_id']}")
            else:
                raw_label = local_label[len(prefix):]
                marker = "\\label{" + raw_label + "}"
                if marker not in target.read_text(encoding="utf-8"):
                    ERRORS.append(f"target label absent from file {row['map_id']}")
        if tag_map.get(row["stacks_label"]) != row["official_tag"]:
            ERRORS.append(f"official tag mismatch {row['map_id']}")
        else:
            existing_tags_referenced.add(row["official_tag"])

    review_snapshot = scope.get("review_snapshot", {})
    actual_review = {
        "file": "tmap.csv",
        "section_topic_rows": len(reviewed),
        "source_subsections": len(source_units),
        "topics_touched": len(touched_topics),
        "existing_official_tags_referenced": len(existing_tags_referenced),
        "theorem_equivalences_claimed": 0,
    }
    if review_snapshot != actual_review:
        ERRORS.append("scope review snapshot does not match tmap.csv")

for name, (field, pattern) in tables.items():
    data = rows(name)
    counts[name] = len(data)
    values = [row[field] for row in data]
    if len(values) != len(set(values)):
        ERRORS.append(f"duplicate {field} in {name}")
    for value in values:
        if not pattern.fullmatch(value):
            ERRORS.append(f"invalid {field} {value!r} in {name}")

allowed = {"unreviewed", "candidate", "reviewed_existing", "reviewed_gap",
           "integrated_local", "built", "remote_checkpoint",
           "upstream_feedback", "upstream_accepted"}
for row in rows("topics.csv"):
    if row["review_state"] not in allowed:
        ERRORS.append(f"invalid topic state for {row['topic_id']}")
    if row["evidence_labels"].strip():
        ERRORS.append(f"initial scaffold must not assert labels: {row['topic_id']}")

findings_path = ROOT.parent / "reports" / "findings.jsonl"
finding_fields = set(interface.get("required_finding_fields", []))
finding_ids = set()
finding_count = 0
if not findings_path.exists():
    ERRORS.append("missing findings channel")
else:
    for number, raw in enumerate(findings_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        finding_count += 1
        try:
            finding = json.loads(raw)
        except json.JSONDecodeError:
            ERRORS.append(f"malformed findings JSON line {number}")
            continue
        missing = finding_fields - set(finding)
        if missing:
            ERRORS.append(f"findings line {number} missing {sorted(missing)}")
        stable_id = finding.get("stable_id", "")
        if stable_id in finding_ids:
            ERRORS.append(f"duplicate finding stable_id {stable_id}")
        finding_ids.add(stable_id)
counts["findings.jsonl"] = finding_count

private_parts = [
    r"C:" + r"[/\\]" + "Users" + r"[/\\]",
    "Documents" + r"[/\\]" + "interlanguage",
    "Flo" + "ris",
]
privacy = re.compile("|".join(private_parts), re.I)
public_files = list(ROOT.iterdir()) + list((ROOT.parent / "reports").iterdir())
for path in public_files:
    if path.is_file() and path.suffix in {".md", ".json", ".jsonl", ".csv", ".py"}:
        if privacy.search(path.read_text(encoding="utf-8")):
            ERRORS.append(f"private path/name in {path.name}")

result = {
    "schema": "ega-stacks-scaffold-check-v1",
    "status": "PASS" if not ERRORS else "FAIL",
    "errors": ERRORS,
    "counts": counts,
    "official_tags_assigned_by_scaffold": 0,
    "existing_official_tags_referenced": len(existing_tags_referenced),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(1 if ERRORS else 0)
