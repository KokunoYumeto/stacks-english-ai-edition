#!/usr/bin/env python3
import csv
import hashlib
import json
import math
import re
import tempfile
import zlib
from pathlib import Path

from intake import PAGE_FIELDS, apply_page_evidence, load_page_evidence

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


def png_dimensions(raw):
    """Return dimensions only for a structurally valid, CRC-clean PNG."""
    if len(raw) < 45 or raw[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    offset = 8
    width = height = None
    saw_idat = False
    first = True
    while offset < len(raw):
        if offset + 12 > len(raw):
            return None
        length = int.from_bytes(raw[offset:offset + 4], "big")
        chunk_type = raw[offset + 4:offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        chunk_end = data_end + 4
        if chunk_end > len(raw):
            return None
        chunk_data = raw[data_start:data_end]
        expected_crc = int.from_bytes(raw[data_end:chunk_end], "big")
        if zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF != expected_crc:
            return None
        if first:
            if chunk_type != b"IHDR" or length != 13:
                return None
            width = int.from_bytes(chunk_data[0:4], "big")
            height = int.from_bytes(chunk_data[4:8], "big")
            bit_depth = chunk_data[8]
            colour_type = chunk_data[9]
            valid_depths = {
                0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8},
                4: {8, 16}, 6: {8, 16},
            }
            if (width <= 0 or height <= 0 or
                    bit_depth not in valid_depths.get(colour_type, set()) or
                    chunk_data[10] != 0 or chunk_data[11] != 0 or
                    chunk_data[12] not in {0, 1}):
                return None
            first = False
        elif chunk_type == b"IHDR":
            return None
        if chunk_type == b"IDAT":
            saw_idat = True
        if chunk_type == b"IEND":
            if length != 0 or not saw_idat or chunk_end != len(raw):
                return None
            return width, height
        offset = chunk_end
    return None


def check_page_evidence_atomicity():
    """Exercise blank legacy guards and fail-closed overlay application."""
    template = {
        "locator_id": "L000001",
        "unit_id": "unit:one",
        "parsed_page": "",
        "printed_page": "I:119",
        "source_receipt": "F8.json",
        "source_receipt_sha256": "A" * 64,
        "page_gate": "P119.json",
        "page_gate_sha256": "B" * 64,
        "evidence_id": "TEST-EVIDENCE-001",
        "decision_id": "D000001",
        "notes": "synthetic page-overlay regression",
        "supersedes": "",
    }

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "pages.csv"

        def write_page_rows(data):
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=PAGE_FIELDS, lineterminator="\n")
                writer.writeheader()
                writer.writerows(data)

        write_page_rows([template])
        errors = []
        _, _, active = load_page_evidence(path, errors)
        if errors or len(active) != 1:
            ERRORS.append("blank parsed-page guard regression did not load")
        replay_states = []
        for _ in range(2):
            units = [{"unit_id": "unit:one", "printed_page": ""}]
            apply_errors = []
            applied = apply_page_evidence(units, active, apply_errors)
            replay_states.append((applied, apply_errors, units[0]["printed_page"]))
        if replay_states != [
                (1, [], "I:119"), (1, [], "I:119")]:
            ERRORS.append("blank parsed-page guard replay is not deterministic")

        units = [{"unit_id": "unit:one", "printed_page": "I:118"}]
        apply_errors = []
        applied = apply_page_evidence(units, active, apply_errors)
        if applied != 0 or not apply_errors or units[0]["printed_page"] != "I:118":
            ERRORS.append("blank page guard accepted a nonblank raw locator")

        wrong_guard = dict(template, parsed_page="I:118")
        write_page_rows([wrong_guard])
        load_errors = []
        _, _, wrong_active = load_page_evidence(path, load_errors)
        units = [{"unit_id": "unit:one", "printed_page": "I:117"}]
        apply_errors = []
        applied = apply_page_evidence(units, wrong_active, apply_errors)
        if (load_errors or applied != 0 or not apply_errors or
                units[0]["printed_page"] != "I:117"):
            ERRORS.append("nonblank wrong page guard did not fail closed")

        blank_target = dict(template, printed_page="")
        write_page_rows([blank_target])
        load_errors = []
        _, _, blank_active = load_page_evidence(path, load_errors)
        if not load_errors or blank_active:
            ERRORS.append("blank authoritative page was accepted")

        second = dict(
            template, locator_id="L000002", unit_id="unit:two",
            parsed_page="I:118", evidence_id="TEST-EVIDENCE-002")
        write_page_rows([template, second])
        load_errors = []
        _, _, two_active = load_page_evidence(path, load_errors)
        units = [
            {"unit_id": "unit:one", "printed_page": ""},
            {"unit_id": "unit:two", "printed_page": "I:117"},
        ]
        apply_errors = []
        applied = apply_page_evidence(units, two_active, apply_errors)
        if (load_errors or applied != 0 or not apply_errors or units != [
                {"unit_id": "unit:one", "printed_page": ""},
                {"unit_id": "unit:two", "printed_page": "I:117"},
        ]):
            ERRORS.append("multi-row page failure was not atomic")


check_page_evidence_atomicity()


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
active_decision_rows, superseded_decisions = active_rows(
    decision_rows, "decision_id", "dec.csv")
decision_by_id = {row["decision_id"]: row for row in decision_rows}
active_decision_by_id = {
    row["decision_id"]: row for row in active_decision_rows
}
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
d154 = decision_by_id.get("D000154")
if d154 is None or not (
        d154.get("subject_id") == "ega:visual-qa" and
        d154.get("action") ==
        "admit_first_individual_authority_french_english_visual_batch" and
        d154.get("state") == "active"):
    ERRORS.append("missing or invalid D000154 visual-QA admission decision")
i49 = issue_by_id.get("I000049")
if i49 is None or not (
        i49.get("subject_id") == "ega:diagrams" and
        i49.get("kind") == "legacy_diagram_certification_below_new_floor" and
        i49.get("status") == "open" and
        i49.get("issue_id") not in superseded_issues):
    ERRORS.append("missing or invalid open corpus-wide visual-QA gate")
i50 = issue_by_id.get("I000050")
if i50 is None or not (
        i50.get("subject_id") == "ega:diagrams" and
        i50.get("kind") == "initial_mapped_visual_queue_certified" and
        i50.get("status") == "resolved" and
        not i50.get("supersedes")):
    ERRORS.append("missing or invalid bounded visual-QA completion issue")
a130 = next(
    (row for row in rows("agent.csv") if row.get("run_id") == "A000130"),
    None,
)
if a130 is None or not (
        a130.get("task_id") == "/root/ega_i_1111_1115" and
        a130.get("scope") ==
        "R184 typed-diagram and intricate-mathematics visual-certification inventory" and
        a130.get("status") == "completed" and
        a130.get("disposition") ==
        "accepted as read-only gate inventory; certification now supplied"):
    ERRORS.append("missing or invalid A000130 visual inventory audit")

tables = {
    "src.csv": ("source_id", re.compile(r"ega\.[a-z0-9.-]+$")),
    "topics.csv": ("topic_id", re.compile(r"ega-topic-[a-z0-9-]+$")),
    "dec.csv": ("decision_id", re.compile(r"D\d{6}$")),
    "issues.csv": ("issue_id", re.compile(r"I\d{6}$")),
    "fb.csv": ("feedback_id", re.compile(r"F\d{6}$")),
    "agent.csv": ("run_id", re.compile(r"A\d{6}$")),
    "pages.csv": ("locator_id", re.compile(r"L\d{6}$")),
    "vqa.csv": ("qa_id", re.compile(r"V\d{6}$")),
}

counts = {}

generated = {
    "files.csv": "relative_path",
    "units.csv": "unit_id",
}
page_evidence_summary = None
visual_qa_summary = None
vqa_active_by_item = {}
intake_path = ROOT / "intake.json"
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
        "ega:subsection:I.3.5": "I:114",
        "ega:I.3.5.1": "I:114",
        "ega:I.3.5.2": "I:115",
        "ega:I.3.5.2:proof": "I:115",
        "ega:I.3.5.3": "I:115",
        "ega:I.3.5.3:diagram:xymatrix:1": "I:115",
        "ega:I.3.5.3:proof": "I:115",
        "ega:I.3.5.4": "I:115",
        "ega:I.3.5.5": "I:115",
        "ega:I.3.5.5:diagram:xymatrix:1": "I:115",
        "ega:I.3.5.6": "I:116",
        "ega:I.3.5.6:proof": "I:116",
        "ega:I.3.5.7": "I:116",
        "ega:I.3.5.7:proof": "I:116",
        "ega:I.3.5.8": "I:116",
        "ega:I.3.5.8:proof": "I:116",
        "ega:I.3.5.9": "I:116",
        "ega:I.3.5.9:proof": "I:116",
        "ega:I.3.5.10": "I:116",
        "ega:I.3.5.10:proof": "I:116",
        "ega:I.3.5.10:diagram:xymatrix:1": "I:117",
        "ega:I.3.5.11": "I:117",
        "ega:subsection:I.3.6": "I:117",
        "ega:section:I.4": "I:119",
        "ega:subsection:I.4.1": "I:119",
        "ega:I.4.1.1": "I:119",
        "ega:I.4.1.2": "I:119",
        "ega:I.4.1.2:proof": "I:120",
    }
    for unit_id, expected_page in page_regressions.items():
        row = units_by_id.get(unit_id)
        if row is None:
            ERRORS.append(f"missing printed-page regression unit {unit_id}")
        elif row["printed_page"] != expected_page:
            ERRORS.append(
                f"printed-page regression for {unit_id}: "
                f"expected {expected_page}, got {row['printed_page']}")

    pages_path = ROOT / "pages.csv"
    if pages_path.exists():
        expected_pages_header = [
            "locator_id", "unit_id", "parsed_page", "printed_page",
            "source_receipt", "source_receipt_sha256", "page_gate",
            "page_gate_sha256", "evidence_id", "decision_id", "notes",
            "supersedes",
        ]
        raw_pages = pages_path.read_bytes()
        page_lines = raw_pages.decode("utf-8").splitlines()
        if (not page_lines or
                page_lines[0].split(",") != expected_pages_header):
            ERRORS.append("unexpected pages.csv header")
        all_page_rows = rows("pages.csv")
        page_ids = [row["locator_id"] for row in all_page_rows]
        if page_ids != [
                f"L{number:06d}"
                for number in range(1, len(page_ids) + 1)]:
            ERRORS.append("pages.csv IDs are not contiguous in append order")
        active_page_rows, superseded_page_rows = active_rows(
            all_page_rows, "locator_id", "pages.csv")
        active_page_units = [row["unit_id"] for row in active_page_rows]
        if len(active_page_units) != len(set(active_page_units)):
            ERRORS.append("multiple active page locators for one unit")
        admitted_page_gates = {
            (
                "EGA1_CHAPTER1_P115_VALIDATION_R38.json",
                "8D0C007424BBFAECD5F59CE33A25567EE6923C4A88D461BB87CE86ADA2496E1B",
            ): "I:115",
            (
                "EGA1_CHAPTER1_P116_VALIDATION_R39.json",
                "083D997689E74C8E7610C0894F978E643753D73DCCA4D8BB61B1FBA17A72339A",
            ): "I:116",
            (
                "EGA1_CHAPTER1_P119_VALIDATION_R42.json",
                "B82C5D63AF34111BBE4D94700582770A36CFF1A005E76C8C088E960421DE83CC",
            ): "I:119",
            (
                "EGA1_CHAPTER1_P120_VALIDATION_R43.json",
                "4721AB517C81B0770246C1F1CC1A4FF1C579FB50A0392A767E83DD9B51F5EF20",
            ): "I:120",
        }
        for row in all_page_rows:
            if None in row:
                ERRORS.append(
                    f"extra CSV field in page row {row.get('locator_id')}")
                continue
            for field in expected_pages_header[:-1]:
                if field == "parsed_page":
                    continue
                if not (row.get(field) or "").strip():
                    ERRORS.append(
                        f"blank {field} in page row {row['locator_id']}")
            if (row["parsed_page"] and not re.fullmatch(
                    r"(?:0|I|II|III|IV):[^,]+", row["parsed_page"])):
                ERRORS.append(
                    f"invalid parsed_page in page row {row['locator_id']}")
            if not re.fullmatch(
                    r"(?:0|I|II|III|IV):[^,]+", row["printed_page"]):
                ERRORS.append(
                    f"invalid printed_page in page row {row['locator_id']}")
            for field in ("source_receipt_sha256", "page_gate_sha256"):
                if not re.fullmatch(r"[0-9A-F]{64}", row[field]):
                    ERRORS.append(
                        f"invalid {field} in page row {row['locator_id']}")
            if (row["source_receipt"], row["source_receipt_sha256"]) not in admitted_receipts:
                ERRORS.append(
                    f"page row lacks admitted French receipt {row['locator_id']}")
            gate_page = admitted_page_gates.get(
                (row["page_gate"], row["page_gate_sha256"]))
            if gate_page is None:
                ERRORS.append(
                    f"page row lacks admitted page gate {row['locator_id']}")
            elif row["printed_page"] != gate_page:
                ERRORS.append(
                    f"page row contradicts its page gate {row['locator_id']}")
            if row["decision_id"] not in decision_by_id:
                ERRORS.append(
                    f"page row has unknown decision {row['locator_id']}")
        for row in active_page_rows:
            unit = units_by_id.get(row["unit_id"])
            if unit is None:
                ERRORS.append(
                    f"page row has unknown unit {row['locator_id']}")
            elif unit["printed_page"] != row["printed_page"]:
                ERRORS.append(
                    f"active page evidence not applied for {row['unit_id']}")
            if row["parsed_page"] == row["printed_page"]:
                ERRORS.append(
                    f"page row does not change parsed evidence {row['locator_id']}")
        page_evidence_summary = {
            "file": "pages.csv",
            "bytes": len(raw_pages),
            "sha256": hashlib.sha256(raw_pages).hexdigest().upper(),
            "physical_rows": len(all_page_rows),
            "active_rows": len(active_page_rows),
            "superseded_rows": len(superseded_page_rows),
            "applied_rows": len(active_page_rows),
        }
        scoped_page_summary = {
            field: page_evidence_summary[field]
            for field in ("file", "bytes", "sha256", "active_rows")
        }
        if (scope["inputs"]["english_discovery"].get("page_evidence") !=
                scoped_page_summary):
            ERRORS.append("scope page-evidence snapshot does not match pages.csv")
    else:
        ERRORS.append("missing pages.csv")

vqa_path = ROOT / "vqa.csv"
expected_vqa_header = [
    "qa_id", "item_id", "item_kind", "source_unit",
    "a_record", "a_pdf_sha256", "a_pdf_bytes", "a_page1", "a_box_pt", "a_file",
    "a_bytes", "a_sha256", "a_dpi",
    "f_record", "f_pdf_sha256", "f_pdf_bytes", "f_page1", "f_box_pt", "f_file",
    "f_bytes", "f_sha256", "f_dpi",
    "e_record", "e_pdf_sha256", "e_pdf_bytes", "e_page1", "e_box_pt", "e_file",
    "e_bytes", "e_sha256", "e_dpi",
    "profile", "mask", "signature", "difference", "status",
    "decision_id", "supersedes",
]
baseline_vqa_items = {
    "ega:I.1.3.9:proof:mathblock:1": "b01",
    "ega:I.1.3.9:proof:mathblock:2": "b02",
    "ega:I.1.7.3:diagram:xymatrix:1": "d01",
    "ega:I.2.4.1:diagram:xymatrix:1": "d02",
    "ega:I.2.5.2:diagram:xymatrix:1": "d03",
    "ega:I.3.3.2:diagram:xymatrix:1": "d04",
    "ega:I.3.3.6:diagram:xymatrix:1": "d05",
    "ega:I.3.3.9:diagram:xymatrix:1": "d06",
    "ega:I.3.3.11:diagram:xymatrix:1": "d07",
    "ega:I.3.4.3:diagram:xymatrix:1": "d08",
    "ega:I.3.4.8:diagram:xymatrix:1": "d09",
    "ega:I.3.5.3:diagram:xymatrix:1": "d10",
    "ega:I.3.5.5:diagram:xymatrix:1": "d11",
    "ega:I.3.5.10:diagram:xymatrix:1": "d12",
}
baseline_vqa_ids = {
    f"V{number:06d}": (item_id, short)
    for number, (item_id, short) in enumerate(
        baseline_vqa_items.items(), start=1)
}
if not vqa_path.exists():
    ERRORS.append("missing vqa.csv")
else:
    raw_vqa = vqa_path.read_bytes()
    vqa_lines = raw_vqa.decode("utf-8").splitlines()
    if not vqa_lines or vqa_lines[0].split(",") != expected_vqa_header:
        ERRORS.append("unexpected vqa.csv header")
    all_vqa_rows = rows("vqa.csv")
    counts["vqa.csv"] = len(all_vqa_rows)
    vqa_ids = [row["qa_id"] for row in all_vqa_rows]
    if vqa_ids != [f"V{number:06d}" for number in range(1, len(vqa_ids) + 1)]:
        ERRORS.append("vqa.csv IDs are not contiguous in append order")
    for row in all_vqa_rows:
        if None in row:
            ERRORS.append(f"extra CSV field in vqa row {row.get('qa_id')}")
        for field in expected_vqa_header[:-1]:
            if not (row.get(field) or "").strip():
                ERRORS.append(f"blank {field} in vqa row {row.get('qa_id')}")
        if row.get("supersedes") is None:
            ERRORS.append(
                f"vqa row lacks explicit supersedes field {row.get('qa_id')}")
    if len(vqa_lines) >= 15:
        first_batch = ("\n".join(vqa_lines[:15]) + "\n").encode("utf-8")
        if (len(first_batch) != 13674 or
                hashlib.sha256(first_batch).hexdigest().upper() !=
                "DD25067C21EE816D5243AA55846B667C3A1E075E331FEBB4A568EDD2FD2A81D3"):
            ERRORS.append("published V000001-V000014 visual-QA prefix changed")
    else:
        ERRORS.append("vqa.csv lacks the first fourteen certified rows")
    active_vqa_rows, superseded_vqa_rows = active_rows(
        all_vqa_rows, "qa_id", "vqa.csv")
    vqa_by_id = {row["qa_id"]: row for row in all_vqa_rows}
    for row in all_vqa_rows:
        prior_id = (row.get("supersedes") or "").strip()
        prior = vqa_by_id.get(prior_id)
        if prior is not None and row["item_id"] != prior["item_id"]:
            ERRORS.append(
                f"visual-QA successor changes item {row['qa_id']} -> {prior_id}")
    active_vqa_ids = {row["qa_id"] for row in active_vqa_rows}
    active_vqa_items = [row["item_id"] for row in active_vqa_rows]
    if len(active_vqa_items) != len(set(active_vqa_items)):
        ERRORS.append("multiple active visual-QA rows for one item")
    vqa_active_by_item = {row["item_id"]: row for row in active_vqa_rows}
    missing_baseline = set(baseline_vqa_items) - set(vqa_active_by_item)
    if missing_baseline:
        ERRORS.append(
            f"missing baseline visual-QA items {sorted(missing_baseline)}")

    record_expectations = {
        "a": (
            "NUMDAM:EGA_I_PMIHES_1960_4.pdf",
            "9ABA23020217535977E279BDD06A0413F48DA703086865BA4C00766C85DF4AE6",
            31680717,
        ),
        "f": (
            "zenodo:21859616/00_FR.pdf",
            "1D4332295C2F572B7D555B05E9A5786632BA9DCB9F329CEAF448CAFC2BDEC6C7",
            1974323,
        ),
        "e": (
            "zenodo:21859616/00_EN.pdf",
            "C70C13635EC53C10A2E1866EAB3BC9CA1B6F6601DCA8B344342DA901A70A0257",
            14589396,
        ),
    }
    record_page_counts = {"a": 227, "f": 165, "e": 1345}
    authority_page_geometry = {
        86: (536, 727),
        96: (543, 727),
        100: (538, 725),
        102: (531, 729),
        107: (604, 755),
        108: (608, 758),
        109: (595, 748),
        111: (606, 756),
        113: (603, 754),
        114: (602, 753),
        116: (607, 757),
    }
    baseline_vqa_pages = {
        "b01": (86, 60, 284), "b02": (86, 60, 284),
        "d01": (96, 66, 291), "d02": (100, 69, 297),
        "d03": (102, 71, 299), "d04": (107, 74, 303),
        "d05": (108, 74, 303), "d06": (108, 75, 304),
        "d07": (109, 75, 304), "d08": (111, 77, 306),
        "d09": (113, 78, 307), "d10": (114, 79, 308),
        "d11": (114, 79, 309), "d12": (116, 80, 310),
    }
    expected_masks = {
        "diagram": (
            "diagram-v1",
            "objects|edges|nonedges|directions|arrow_styles|hooks|equalities|"
            "labels|primes|bars|subscripts|geometry|label_sides",
        ),
        "mathblock": (
            "mathblock-v1",
            "terms|order|arrows|zeros|operators|primes|bars|subscripts|"
            "spacing|line_isolation",
        ),
    }
    allowed_differences = {
        "none", "english-trailing-comma-only",
        "english-trailing-period-only",
    }
    crop_paths = []
    active_crop_hashes = []
    active_crop_locators = []
    crop_bytes = 0
    certified_diagrams = 0
    certified_mathblocks = 0
    for row in all_vqa_rows:
        item_id = row["item_id"]
        baseline_entry = baseline_vqa_ids.get(row["qa_id"])
        if baseline_entry is not None:
            expected_item, expected_short = baseline_entry
            if item_id != expected_item:
                ERRORS.append(f"visual-QA baseline item mismatch {row['qa_id']}")
        else:
            expected_short = row["qa_id"].lower()
        source = units_by_id.get(row["source_unit"])
        if source is None:
            ERRORS.append(f"visual-QA row has unknown source unit {row['qa_id']}")
        if row["item_kind"] == "diagram":
            certified_diagrams += row["qa_id"] in active_vqa_ids
            if source is not None and source["kind"] != "diagram":
                ERRORS.append(f"visual-QA diagram source is not a diagram {row['qa_id']}")
            if row["item_id"] != row["source_unit"]:
                ERRORS.append(f"visual-QA diagram item/source mismatch {row['qa_id']}")
            if not row["signature"].endswith(
                    ";ordinary;no-hooks;no-equalities;no-other-edges"):
                ERRORS.append(f"incomplete diagram graph signature {row['qa_id']}")
        elif row["item_kind"] == "mathblock":
            certified_mathblocks += row["qa_id"] in active_vqa_ids
            suffix = row["item_id"].removeprefix(
                row["source_unit"] + ":mathblock:")
            if (not row["item_id"].startswith(
                    row["source_unit"] + ":mathblock:") or
                    not suffix.isdigit()):
                ERRORS.append(f"invalid visual-QA mathblock identity {row['qa_id']}")
            if source is not None and source["kind"] != "proof":
                ERRORS.append(f"visual-QA mathblock source is not a proof {row['qa_id']}")
        else:
            ERRORS.append(f"invalid visual-QA item kind {row['qa_id']}")
            continue
        profile, mask = expected_masks[row["item_kind"]]
        if row["profile"] != profile or row["mask"] != mask:
            ERRORS.append(f"wrong visual-QA profile or mask {row['qa_id']}")
        if row["difference"] not in allowed_differences:
            ERRORS.append(f"uncontrolled visual-QA difference {row['qa_id']}")
        if row["status"] != "certified":
            ERRORS.append(f"non-certified visual-QA row {row['qa_id']}")
        admission = active_decision_by_id.get(row["decision_id"])
        if admission is None:
            ERRORS.append(
                f"visual-QA row lacks an active decision {row['qa_id']}")
        elif (admission.get("subject_id") != "ega:visual-qa" or
                admission.get("state") != "active" or
                not admission.get("action", "").startswith("admit_")):
            ERRORS.append(
                f"visual-QA row cites a non-admission decision {row['qa_id']}")
        if baseline_entry is not None and row["decision_id"] != "D000154":
            ERRORS.append(f"visual-QA baseline row has wrong decision {row['qa_id']}")

        if baseline_entry is not None:
            try:
                actual_pages = tuple(
                    int(row[f"{language}_page1"])
                    for language in ("a", "f", "e")
                )
            except ValueError:
                actual_pages = None
            if actual_pages != baseline_vqa_pages[expected_short]:
                ERRORS.append(f"visual-QA baseline page mismatch {row['qa_id']}")

        for language in ("a", "f", "e"):
            record, pdf_sha, pdf_bytes = record_expectations[language]
            if (row[f"{language}_record"] != record or
                    row[f"{language}_pdf_sha256"] != pdf_sha or
                    row[f"{language}_pdf_bytes"] != str(pdf_bytes)):
                ERRORS.append(
                    f"visual-QA record identity mismatch {row['qa_id']} {language}")
            try:
                page1 = int(row[f"{language}_page1"])
                dpi = int(row[f"{language}_dpi"])
                box = [float(value) for value in row[f"{language}_box_pt"].split(";")]
            except ValueError:
                ERRORS.append(
                    f"invalid visual-QA numeric locator {row['qa_id']} {language}")
                continue
            if (page1 <= 0 or page1 > record_page_counts[language] or
                    dpi < 5000 or len(box) != 4 or
                    not all(math.isfinite(value) for value in box) or
                    box[0] < 0 or box[1] < 0 or box[2] <= 0 or box[3] <= 0):
                ERRORS.append(
                    f"visual-QA locator below gate {row['qa_id']} {language}")
                continue
            if language == "a":
                geometry = authority_page_geometry.get(page1)
            elif language == "f":
                geometry = (595.276, 841.89)
            else:
                geometry = (612, 792)
            if geometry is None:
                ERRORS.append(
                    f"unbound visual-QA page geometry {row['qa_id']} {language}")
                continue
            if (box[0] + box[2] > geometry[0] + 0.01 or
                    box[1] + box[3] > geometry[1] + 0.01):
                ERRORS.append(
                    f"visual-QA crop leaves page box {row['qa_id']} {language}")
                continue
            expected_path = f"qa/{language}/{expected_short}.png"
            relative_text = row[f"{language}_file"]
            if relative_text != expected_path:
                ERRORS.append(
                    f"visual-QA crop path mismatch {row['qa_id']} {language}")
            relative = Path(relative_text)
            if relative.is_absolute() or ".." in relative.parts:
                ERRORS.append(
                    f"unsafe visual-QA crop path {row['qa_id']} {language}")
                continue
            crop = ROOT / relative
            crop_paths.append(relative_text)
            if not crop.is_file():
                ERRORS.append(
                    f"missing visual-QA crop {row['qa_id']} {language}")
                continue
            expected_crop_root = (ROOT / "qa" / language).resolve()
            resolved_crop = crop.resolve()
            try:
                resolved_crop.relative_to(expected_crop_root)
            except ValueError:
                ERRORS.append(
                    f"visual-QA crop escapes language root {row['qa_id']} {language}")
                continue
            if crop.is_symlink():
                ERRORS.append(
                    f"visual-QA crop may not be a symlink {row['qa_id']} {language}")
                continue
            raw_crop = crop.read_bytes()
            crop_bytes += len(raw_crop)
            try:
                expected_bytes = int(row[f"{language}_bytes"])
            except ValueError:
                ERRORS.append(
                    f"invalid visual-QA byte count {row['qa_id']} {language}")
                continue
            if len(raw_crop) != expected_bytes:
                ERRORS.append(
                    f"visual-QA crop byte mismatch {row['qa_id']} {language}")
            if (not re.fullmatch(r"[0-9A-F]{64}", row[f"{language}_sha256"]) or
                    hashlib.sha256(raw_crop).hexdigest().upper() !=
                    row[f"{language}_sha256"]):
                ERRORS.append(
                    f"visual-QA crop hash mismatch {row['qa_id']} {language}")
            if row["qa_id"] in active_vqa_ids:
                active_crop_hashes.append(row[f"{language}_sha256"])
                active_crop_locators.append((
                    row[f"{language}_record"], row[f"{language}_pdf_sha256"],
                    page1, tuple(box),
                ))
            dimensions = png_dimensions(raw_crop)
            if dimensions is None:
                ERRORS.append(
                    f"visual-QA crop is not a valid CRC-clean PNG "
                    f"{row['qa_id']} {language}")
                continue
            width, height = dimensions
            expected_width = box[2] * dpi / 72
            expected_height = box[3] * dpi / 72
            if (abs(width - expected_width) > 3 or
                    abs(height - expected_height) > 3):
                ERRORS.append(
                    f"visual-QA crop dimensions contradict box/dpi "
                    f"{row['qa_id']} {language}")
            effective_dpi = min(width * 72 / box[2], height * 72 / box[3])
            if effective_dpi < 5000:
                ERRORS.append(
                    f"visual-QA effective scale below 5000 dpi "
                    f"{row['qa_id']} {language}")
    if len(crop_paths) != len(set(crop_paths)):
        ERRORS.append("visual-QA evidence reuses a crop file")
    if len(active_crop_hashes) != len(set(active_crop_hashes)):
        ERRORS.append("active visual-QA evidence reuses crop bytes")
    if len(active_crop_locators) != len(set(active_crop_locators)):
        ERRORS.append("active visual-QA evidence reuses a source locator")
    discovered_qa_files = {
        path.relative_to(ROOT).as_posix()
        for language in ("a", "f", "e")
        for path in (ROOT / "qa" / language).rglob("*")
        if path.is_file()
    }
    if discovered_qa_files != set(crop_paths):
        ERRORS.append("visual-QA directory and manifest file sets differ")
    visual_qa_summary = {
        "file": "vqa.csv",
        "bytes": len(raw_vqa),
        "sha256": hashlib.sha256(raw_vqa).hexdigest().upper(),
        "physical_rows": len(all_vqa_rows),
        "active_rows": len(active_vqa_rows),
        "superseded_rows": len(superseded_vqa_rows),
        "certified_diagrams": certified_diagrams,
        "certified_mathblocks": certified_mathblocks,
        "crop_files": len(crop_paths),
        "crop_bytes": crop_bytes,
    }
    if scope.get("visual_qa_snapshot") != visual_qa_summary:
        ERRORS.append("scope visual-QA snapshot does not match vqa.csv and crops")

if intake_path.exists():
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    if intake.get("status") != "PASS" or intake.get("errors"):
        ERRORS.append("intake receipt is not PASS/errors[]")
    if intake.get("source", {}).get("tree_sha256") != scope["inputs"]["english_discovery"]["tree_sha256"]:
        ERRORS.append("intake tree does not match scope")
    if intake.get("units") != scope["inputs"]["english_discovery"]["discovery_units"]:
        ERRORS.append("intake unit count does not match scope")
    if intake.get("schema") != "ega-english-discovery-intake-v4":
        ERRORS.append("intake schema does not include page evidence")
    if intake.get("page_evidence") != page_evidence_summary:
        ERRORS.append("intake page-evidence receipt does not match pages.csv")

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
    mapped_diagram_units = {
        row["source_unit"] for row in statement_edges
        if units_by_id.get(row["source_unit"], {}).get("kind") == "diagram"
    }
    missing_diagram_qa = mapped_diagram_units - set(vqa_active_by_item)
    if missing_diagram_qa:
        ERRORS.append(
            f"mapped diagrams lack active visual QA {sorted(missing_diagram_qa)}")

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
