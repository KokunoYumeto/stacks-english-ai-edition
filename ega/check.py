#!/usr/bin/env python3
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ERRORS = []


def rows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def active_rows(data, id_field, table_name):
    """Return the unsuperseded view while retaining every historical row."""
    positions = {row[id_field]: index for index, row in enumerate(data)}
    superseded = set()
    for index, row in enumerate(data):
        raw_prior = row.get("supersedes") or ""
        prior = raw_prior.strip()
        if raw_prior != prior:
            ERRORS.append(
                f"whitespace in supersedes for {row[id_field]} in {table_name}")
            continue
        if not prior:
            continue
        if prior not in positions:
            ERRORS.append(
                f"unknown superseded {id_field} {prior!r} in {table_name}")
        elif positions[prior] >= index:
            ERRORS.append(
                f"non-prior supersession {row[id_field]} -> {prior} in {table_name}")
        elif prior in superseded:
            ERRORS.append(
                f"multiple supersessions of {prior} in {table_name}")
        else:
            superseded.add(prior)
    return [row for row in data if row[id_field] not in superseded], superseded


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
admitted_receipts = {
    (entry.get("manifest"), entry.get("manifest_sha256"))
    for entry in interface.get("admitted_french_receipts", [])
}
current_receipt = (
    interface.get("french_cursor", {}).get("manifest"),
    interface.get("french_cursor", {}).get("manifest_sha256"),
)
if current_receipt not in admitted_receipts:
    ERRORS.append("current French manifest missing from admitted receipt registry")

decision_rows = rows("dec.csv")
issue_rows = rows("issues.csv")
active_rows(decision_rows, "decision_id", "dec.csv")
decision_by_id = {row["decision_id"]: row for row in decision_rows}
issue_by_id = {row["issue_id"]: row for row in issue_rows}
issue_positions = {
    row["issue_id"]: index for index, row in enumerate(issue_rows)
}
superseded_issues = set()
for index, row in enumerate(issue_rows):
    raw_link = row.get("supersedes") or ""
    link = raw_link.strip()
    if raw_link != link:
        ERRORS.append(f"whitespace in issue link for {row['issue_id']}")
    elif not link:
        continue
    elif link.startswith("D"):
        if link not in decision_by_id:
            ERRORS.append(
                f"unknown linked decision {link!r} for {row['issue_id']}")
    elif link.startswith("I"):
        if link not in issue_positions:
            ERRORS.append(
                f"unknown superseded issue {link!r} for {row['issue_id']}")
        elif issue_positions[link] >= index:
            ERRORS.append(
                f"non-prior issue supersession {row['issue_id']} -> {link}")
        elif link in superseded_issues:
            ERRORS.append(f"multiple issue supersessions of {link}")
        else:
            superseded_issues.add(link)
    else:
        ERRORS.append(
            f"invalid mixed-namespace issue link {link!r} for {row['issue_id']}")
d104 = decision_by_id.get("D000104")
if d104 is None or not (
        d104.get("subject_id") == "ega:scaffold" and
        d104.get("action") == "restore_append_only_graph_correction" and
        d104.get("supersedes") == "D000103"):
    ERRORS.append("missing or invalid D000104 append-only repair decision")
i41 = issue_by_id.get("I000041")
if i41 is None or not (
        i41.get("subject_id") == "ega:scaffold" and
        i41.get("kind") == "in_place_graph_correction_violated_append_only" and
        i41.get("status") == "resolved" and
        i41.get("supersedes") == "I000040"):
    ERRORS.append("missing or invalid I000041 append-only repair issue")

tables = {
    "src.csv": ("source_id", re.compile(r"ega\.[a-z0-9.-]+$")),
    "topics.csv": ("topic_id", re.compile(r"ega-topic-[a-z0-9-]+$")),
    "dec.csv": ("decision_id", re.compile(r"D\d{6}$")),
    "issues.csv": ("issue_id", re.compile(r"I\d{6}$")),
    "fb.csv": ("feedback_id", re.compile(r"F\d{6}$")),
    "agent.csv": ("run_id", re.compile(r"A\d{6}$")),
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
    units_by_id = {row["unit_id"]: row for row in unit_rows}
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
    page_regressions = {
        "ega:I.1.8.1": "II:217",
        "ega:I.1.8.1:proof": "II:218",
        "ega:I.1.8.2": "II:218",
        "ega:I.1.8.3": "II:219",
        "ega:I.1.8.6": "II:219",
        "ega:I.1.8.7": "II:220",
        "ega:I.1.8.9": "II:220",
        "ega:I.1.8.10": "II:221",
        "ega:I.3.2.9": "II:221",
        "ega:subsection:I.3.3": "I:108",
        "ega:I.3.3.1": "I:108",
        "ega:I.3.3.2": "I:108",
        "ega:I.3.3.2:diagram:xymatrix:1": "I:108",
        "ega:I.3.3.3": "I:108",
        "ega:I.3.3.3:proof": "I:108",
        "ega:I.3.3.4": "I:108",
        "ega:I.3.3.5": "I:108",
    }
    for unit_id, expected_page in page_regressions.items():
        row = units_by_id.get(unit_id)
        if row is None:
            ERRORS.append(f"missing printed-page regression unit {unit_id}")
        elif row["printed_page"] != expected_page:
            ERRORS.append(
                f"printed-page regression for {unit_id}: "
                f"expected {expected_page}, got {row['printed_page']}")

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
        if (row["source_receipt"], row["source_receipt_sha256"]) not in admitted_receipts:
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

smap_path = ROOT / "smap.csv"
if smap_path.exists():
    expected_smap_header = [
        "edge_id", "source_unit", "source_part", "authority_state",
        "source_receipt", "source_receipt_sha256", "stacks_commit",
        "stacks_file", "stacks_label", "official_tag", "relation",
        "review_state", "coverage_claim", "evidence", "decision_id",
        "notes", "supersedes",
    ]
    smap_lines = smap_path.read_text(encoding="utf-8").splitlines()
    if not smap_lines or smap_lines[0].split(",") != expected_smap_header:
        ERRORS.append("unexpected smap.csv header")
    all_statement_edges = rows("smap.csv")
    counts["smap.csv"] = len(all_statement_edges)
    for row_number, row in enumerate(all_statement_edges, 1):
        if None in row:
            ERRORS.append(f"extra CSV field in smap row {row.get('edge_id')}")
        missing = [
            field for field in expected_smap_header[:-1]
            if row.get(field) is None
        ]
        if missing:
            ERRORS.append(
                f"missing CSV fields {missing} in smap row {row.get('edge_id')}")
        if row_number > 335 and row.get("supersedes") is None:
            ERRORS.append(
                f"new smap row lacks explicit supersedes field {row['edge_id']}")
    legacy_smap = (
        ",".join(expected_smap_header[:-1]) + "\n" +
        "\n".join(smap_lines[1:336]) + "\n"
    ).encode("utf-8")
    if (len(legacy_smap) != 144616 or
            hashlib.sha256(legacy_smap).hexdigest().upper() !=
            "86DB212E45E51F7F7CB8613E4A205A9A07E68A82E173BBD2C5DD8167E350819C"):
        ERRORS.append("published S000001-S000335 prefix changed")
    edge_ids = [row["edge_id"] for row in all_statement_edges]
    if len(edge_ids) != len(set(edge_ids)):
        ERRORS.append("duplicate edge_id in smap.csv")
    if edge_ids != [f"S{number:06d}" for number in range(1, len(edge_ids) + 1)]:
        ERRORS.append("smap.csv IDs are not contiguous in append order")
    for edge_id in edge_ids:
        if not re.fullmatch(r"S\d{6}", edge_id):
            ERRORS.append(f"invalid edge_id {edge_id!r}")
    statement_edges, superseded_statement_edges = active_rows(
        all_statement_edges, "edge_id", "smap.csv")
    active_edge_ids = {row["edge_id"] for row in statement_edges}
    edge_by_id = {row["edge_id"]: row for row in all_statement_edges}
    attribution_edge_successors = {
        "S000331": "S000336",
        "S000332": "S000337",
        "S000333": "S000338",
        "S000334": "S000339",
    }
    for prior, successor in attribution_edge_successors.items():
        prior_row = edge_by_id.get(prior)
        successor_row = edge_by_id.get(successor)
        if prior_row is None or successor_row is None:
            ERRORS.append(f"missing attribution edge supersession {prior} -> {successor}")
        elif not (
                prior_row["source_unit"] == "ega:I.3.3.10:proof" and
                successor_row["source_unit"] == "ega:I.3.3.10" and
                (successor_row.get("supersedes") or "") == prior and
                prior not in active_edge_ids and successor in active_edge_ids):
            ERRORS.append(f"invalid attribution edge supersession {prior} -> {successor}")
        else:
            allowed_changes = {
                "edge_id", "source_unit", "decision_id", "supersedes"
            }
            for field in expected_smap_header:
                if field not in allowed_changes and (
                        (prior_row.get(field) or "") !=
                        (successor_row.get(field) or "")):
                    ERRORS.append(
                        f"non-attribution change in {prior} -> {successor}: {field}")
    semantic_edge_keys = [
        (row["source_unit"], row["source_part"], row["stacks_label"])
        for row in statement_edges
    ]
    if len(semantic_edge_keys) != len(set(semantic_edge_keys)):
        ERRORS.append("duplicate active semantic edge in smap.csv")

    unit_ids = {row["unit_id"] for row in rows("units.csv")}
    decision_ids = {row["decision_id"] for row in rows("dec.csv")}
    tag_map = {}
    with (ROOT.parent / "tags" / "tags").open(encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.rstrip("\n")
            if not raw or "," not in raw:
                continue
            tag, label = raw.split(",", 1)
            tag_map[label] = tag

    allowed_relations = {
        "equivalent", "split", "merged", "partial",
        "entailed_by_stronger",
    }
    allowed_coverage_claims = {
        "component", "full_statement", "covered_unlabelled",
        "covered_derived",
    }
    source_units = set()
    existing_tags = set()
    existing_tag_rows = 0
    local_untagged_rows = 0
    full_statement_equivalences = 0
    for row in all_statement_edges:
        is_active = row["edge_id"] in active_edge_ids
        if is_active:
            source_units.add(row["source_unit"])
        if row["source_unit"] not in unit_ids:
            ERRORS.append(f"statement edge has unknown unit {row['source_unit']}")
        if row["authority_state"] != "french_admitted":
            ERRORS.append(f"statement edge lacks French admission {row['edge_id']}")
        if (row["source_receipt"], row["source_receipt_sha256"]) not in admitted_receipts:
            ERRORS.append(f"statement edge has wrong French receipt {row['edge_id']}")
        if row["decision_id"] not in decision_ids:
            ERRORS.append(f"statement edge has unknown decision {row['edge_id']}")
        if row["relation"] not in allowed_relations:
            ERRORS.append(f"invalid statement relation {row['edge_id']}")
        if row["coverage_claim"] not in allowed_coverage_claims:
            ERRORS.append(f"invalid statement coverage claim {row['edge_id']}")
        for field in ("source_part", "evidence"):
            if not row[field].strip():
                ERRORS.append(
                    f"blank statement {field} for {row['edge_id']}")

        target = ROOT.parent / row["stacks_file"]
        if not target.is_file():
            ERRORS.append(f"missing statement target {row['stacks_file']}")
        else:
            prefix = target.stem + "-"
            if not row["stacks_label"].startswith(prefix):
                ERRORS.append(f"statement target label/file mismatch {row['edge_id']}")
            else:
                raw_label = row["stacks_label"][len(prefix):]
                marker = "\\label{" + raw_label + "}"
                if marker not in target.read_text(encoding="utf-8"):
                    ERRORS.append(f"statement target label absent {row['edge_id']}")

        if row["review_state"] == "reviewed_existing":
            if row["stacks_commit"] != scope["stacks_upstream"]:
                ERRORS.append(f"existing statement edge has wrong commit {row['edge_id']}")
            if not row["official_tag"]:
                ERRORS.append(f"existing statement edge lacks official tag {row['edge_id']}")
            elif tag_map.get(row["stacks_label"]) != row["official_tag"]:
                ERRORS.append(f"statement official tag mismatch {row['edge_id']}")
            elif is_active:
                existing_tag_rows += 1
                existing_tags.add(row["official_tag"])
        elif row["review_state"] == "integrated_local":
            if row["stacks_commit"] != "LOCAL_WORKTREE":
                ERRORS.append(f"local statement edge has wrong commit state {row['edge_id']}")
            if row["official_tag"]:
                ERRORS.append(f"local statement edge invents official tag {row['edge_id']}")
            if is_active:
                local_untagged_rows += 1
        else:
            ERRORS.append(f"invalid statement review state {row['edge_id']}")

        if (is_active and row["relation"] == "equivalent" and
                row["coverage_claim"] == "full_statement"):
            full_statement_equivalences += 1

    actual_statement_review = {
        "file": "smap.csv",
        "statement_edge_rows": len(statement_edges),
        "file_rows": len(all_statement_edges),
        "superseded_rows": len(superseded_statement_edges),
        "source_units": len(source_units),
        "existing_official_tag_rows": existing_tag_rows,
        "distinct_existing_official_tags": len(existing_tags),
        "local_untagged_rows": local_untagged_rows,
        "full_statement_equivalences": full_statement_equivalences,
    }
    if scope.get("statement_review_snapshot") != actual_statement_review:
        ERRORS.append("scope statement review snapshot does not match smap.csv")

residual_path = ROOT / "resid.csv"
if residual_path.exists():
    expected_resid_header = [
        "residual_id", "source_unit", "kind", "status", "evidence",
        "disposition", "decision_id", "supersedes",
    ]
    residual_lines = residual_path.read_text(encoding="utf-8").splitlines()
    if not residual_lines or residual_lines[0].split(",") != expected_resid_header:
        ERRORS.append("unexpected resid.csv header")
    all_residuals = rows("resid.csv")
    counts["resid.csv"] = len(all_residuals)
    for row_number, row in enumerate(all_residuals, 1):
        if None in row:
            ERRORS.append(
                f"extra CSV field in residual row {row.get('residual_id')}")
        missing = [
            field for field in expected_resid_header[:-1]
            if row.get(field) is None
        ]
        if missing:
            ERRORS.append(
                f"missing CSV fields {missing} in residual row "
                f"{row.get('residual_id')}")
        if row_number > 171 and row.get("supersedes") is None:
            ERRORS.append(
                "new residual row lacks explicit supersedes field "
                f"{row['residual_id']}")
    legacy_residuals = (
        ",".join(expected_resid_header[:-1]) + "\n" +
        "\n".join(residual_lines[1:172]) + "\n"
    ).encode("utf-8")
    if (len(legacy_residuals) != 46075 or
            hashlib.sha256(legacy_residuals).hexdigest().upper() !=
            "704D957786F45FE1F280C3303C59883DC50AAC9809CD2071FBB8C20369147303"):
        ERRORS.append("published R000001-R000171 prefix changed")
    residual_ids = [row["residual_id"] for row in all_residuals]
    if len(residual_ids) != len(set(residual_ids)):
        ERRORS.append("duplicate residual_id in resid.csv")
    if residual_ids != [
            f"R{number:06d}" for number in range(1, len(residual_ids) + 1)]:
        ERRORS.append("resid.csv IDs are not contiguous in append order")
    residuals, superseded_residuals = active_rows(
        all_residuals, "residual_id", "resid.csv")
    active_residual_ids = {row["residual_id"] for row in residuals}
    residual_by_id = {row["residual_id"]: row for row in all_residuals}
    attribution_residual_successors = {
        "R000165": "R000172",
        "R000166": "R000173",
        "R000167": "R000174",
    }
    for prior, successor in attribution_residual_successors.items():
        prior_row = residual_by_id.get(prior)
        successor_row = residual_by_id.get(successor)
        if prior_row is None or successor_row is None:
            ERRORS.append(
                f"missing attribution residual supersession {prior} -> {successor}")
        elif not (
                prior_row["source_unit"] == "ega:I.3.3.10:proof" and
                successor_row["source_unit"] == "ega:I.3.3.10" and
                (successor_row.get("supersedes") or "") == prior and
                prior not in active_residual_ids and
                successor in active_residual_ids):
            ERRORS.append(
                f"invalid attribution residual supersession {prior} -> {successor}")
        else:
            allowed_changes = {
                "residual_id", "source_unit", "decision_id", "supersedes"
            }
            for field in expected_resid_header:
                if field not in allowed_changes and (
                        (prior_row.get(field) or "") !=
                        (successor_row.get(field) or "")):
                    ERRORS.append(
                        "non-attribution change in residual "
                        f"{prior} -> {successor}: {field}")
    unit_ids = {row["unit_id"] for row in rows("units.csv")}
    decision_ids = {row["decision_id"] for row in rows("dec.csv")}
    allowed_residual_states = {
        "known_semantic_difference", "open_gap", "covered_unlabelled",
        "covered_by_stronger", "covered_derived",
        "integrated_local_pending_upstream",
    }
    residual_state_by_unit = {}
    for row in all_residuals:
        if not re.fullmatch(r"R\d{6}", row["residual_id"]):
            ERRORS.append(f"invalid residual_id {row['residual_id']!r}")
        if row["source_unit"] not in unit_ids:
            ERRORS.append(f"residual has unknown unit {row['residual_id']}")
        if row["decision_id"] not in decision_ids:
            ERRORS.append(f"residual has unknown decision {row['residual_id']}")
        if row["status"] not in allowed_residual_states:
            ERRORS.append(f"invalid residual state {row['residual_id']}")
        for field in ("kind", "evidence", "disposition"):
            if not row[field].strip():
                ERRORS.append(f"blank residual {field} for {row['residual_id']}")
        if row["residual_id"] in active_residual_ids:
            residual_state_by_unit.setdefault(row["source_unit"], set()).add(
                row["status"])

    if smap_path.exists():
        local_units = {
            row["source_unit"] for row in statement_edges
            if row["review_state"] == "integrated_local"
        }
        pending_local_units = {
            row["source_unit"] for row in residuals
            if row["status"] == "integrated_local_pending_upstream"
        }
        if local_units != pending_local_units:
            ERRORS.append(
                "local statement edges and upstream-pending residuals differ")
        for row in statement_edges:
            states = residual_state_by_unit.get(row["source_unit"], set())
            if row["relation"] == "partial" and not (
                    {"open_gap", "covered_derived"} & states):
                ERRORS.append(
                    f"partial statement edge lacks residual {row['edge_id']}")
            if row["relation"] == "entailed_by_stronger" and (
                    "covered_by_stronger" not in states):
                ERRORS.append(
                    f"stronger statement edge lacks residual {row['edge_id']}")
            if row["coverage_claim"] == "covered_unlabelled" and (
                    "covered_unlabelled" not in states):
                ERRORS.append(
                    f"unlabelled statement edge lacks residual {row['edge_id']}")
            if row["coverage_claim"] == "covered_derived" and (
                    "covered_derived" not in states):
                ERRORS.append(
                    f"derived statement edge lacks residual {row['edge_id']}")
    actual_residual_snapshot = {
        "file": "resid.csv",
        "rows": len(residuals),
        "file_rows": len(all_residuals),
        "superseded_rows": len(superseded_residuals),
        "open_gaps": sum(row["status"] == "open_gap" for row in residuals),
        "integrated_local_pending_upstream": sum(
            row["status"] == "integrated_local_pending_upstream"
            for row in residuals
        ),
    }
    if scope.get("residual_snapshot") != actual_residual_snapshot:
        ERRORS.append("scope residual snapshot does not match resid.csv")

agent_path = ROOT / "agent.csv"
if agent_path.exists():
    agent_rows = rows("agent.csv")
    task_scopes = [(row["task_id"], row["scope"]) for row in agent_rows]
    if len(task_scopes) != len(set(task_scopes)):
        ERRORS.append("duplicate task_id/scope in agent.csv")
    for row in agent_rows:
        if not (
                re.fullmatch(
                    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                    row["task_id"])
                or re.fullmatch(
                    r"/root(?:/[a-z0-9_]+)+", row["task_id"])):
            ERRORS.append(f"invalid agent task id {row['run_id']}")
        if row["status"] != "completed":
            ERRORS.append(f"non-completed recorded agent run {row['run_id']}")
        if row["duration_ms"] != "not_exposed":
            try:
                if int(row["duration_ms"]) <= 0:
                    ERRORS.append(f"invalid agent duration {row['run_id']}")
            except ValueError:
                ERRORS.append(f"non-integer agent duration {row['run_id']}")
        if row["writes"] != "none":
            ERRORS.append(f"unexpected agent writes {row['run_id']}")
        if row["model"] not in {
                "gpt-5.3-codex-spark", "inherited-parent"}:
            ERRORS.append(f"invalid agent model {row['run_id']}")
        if row["thinking"] not in {"xhigh", "inherited"}:
            ERRORS.append(f"invalid agent effort {row['run_id']}")
        for field in (
                "scope", "returned", "owner_check", "disposition"):
            if not row[field].strip():
                ERRORS.append(f"blank agent {field} for {row['run_id']}")

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
