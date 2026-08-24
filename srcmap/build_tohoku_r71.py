#!/usr/bin/env python3
"""Seal and replay the frozen D1029-D1031 zero-gap Tohoku r71 transaction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import types
from pathlib import Path
from typing import Any, Mapping


SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent
ENGINE_PATH = ROOT / "srcmap" / "build_tohoku_r70.py"
CONTRACT_PATH = ROOT / "srcmap" / "tohoku_r71_contract.json"
ENGINE_IDENTITY = (50028, "A4AADA6ECFC96AAEA8343A8B420F6871FAF4E97E6C0CCFF7FF0A16D2DF8F11EA")
CONTRACT_ID = "D1029-D1031-r71-D001063-D001066-I000033-v1"
DESIGN_SPEC = ("tmp/d1031_final_four_gap_batch_design.json", 26070, "37AC8B57BF83C04900BC6350E8EA7CBF235B3EBD39C7096E336DB196901CED04")

EXPECTED_R70_RECEIPT = (13877, "1B8EC4673FAFA9472DB78FDA179E7E01FDA9C8C55B74FFFD4C8F109BE207A169")
EXPECTED_R70_FILES = {
    "STATUS.md": (984, "4802A347A73F911C6F458C11B27BAE3A18FD1AA4406C9969E15CA225C06E9F0A"),
    "cfg.json": (5151, "2C1917E032CAE4B174E89319E4BC860D4CB04967899F1B0679C0527B95E952D7"),
    "check.json": (83847, "07C5D80259067698B473D2D9A0B7EE95FCAA10081F8F2258BE73BC83AA7C3258"),
    "dec.csv": (406725, "2D8D386A770F9FCF46009647B46B9F05F7AC8B0C91213F83930147CD216F1E15"),
    "intake.json": (1578, "7E2B1F451113D57041FB676A4BE85F6C8AE51783FC8A559691AD5D6DCCF9271F"),
    "issues.csv": (34015, "2D60F1DB762808C5EFCD62AAB74394D8772C190DCB3150F3F82984DE3B9D7EB1"),
    "map.csv": (499089, "FC5B419371E2551296FD3D4A91DB7278C5C4B90D6C06D947A3025E748904F675"),
    "mcheck.json": (73645, "3C5F98C966D9B13BFAB856C50ACF4E141E08A26A7A2413C73FE6CE4B316DD32B"),
    "stx.csv": (5290688, "86D4B13F8189D71ABC67EB7C40A79EE6F1AC86D564812F120506A2F4321C01DC"),
    "tcand.csv": (489828, "6811DEB4478A0EDCEF25B6742920E9DC65878BDAD7436D79D419E0D7CF1B2320"),
    "tmap.csv": (2424, "DEB05561CA297574E3FC54D9E36CB8628A092C280BDFAB53E79C0F198C29C9A1"),
    "topics.csv": (2453, "AA62558CA4292B914D75A63BC4436586D88B754C9D08618DC8E67554C58B6B5C"),
    "ucand.csv": (120, "D7D823C01798DC15596F2C67D1177F427A50EE39CDD4F4B6B437FBD56A86D1A4"),
    "units.csv": (393225, "6AAAD1470DDA82604F84D697EC1833FAC4BEE16342FAD8EB415BA17CFB018262"),
}
EXPECTED_SCAN = {
    "cfg.json": (5151, "2C1917E032CAE4B174E89319E4BC860D4CB04967899F1B0679C0527B95E952D7"),
    "check.json": (84174, "4ABB22388571D56C410E36811D86EB3EAA2B9AE814C5FEE4F5461F8867C39F61"),
    "stx.csv": (5291400, "3A27F8EE563AF2521071EC5D1EFE6BF6E8DA1E5B194B98CC0C0D450B6CB00118"),
    "tcand.csv": (489828, "EA279CAB0FDF739C87884E0228036A3E0E5ACC3BE3F93F0A22DCB67B40591513"),
    "tmap.csv": (2424, "DEB05561CA297574E3FC54D9E36CB8628A092C280BDFAB53E79C0F198C29C9A1"),
    "topics.csv": (2453, "AA62558CA4292B914D75A63BC4436586D88B754C9D08618DC8E67554C58B6B5C"),
}
EXPECTED_SCAN_COUNTS = {
    "labels": 22116,
    "official_tags_joined": 21437,
    "tex_files": 119,
    "topic_candidates": 1287,
    "topic_coverage": {"direct": 13},
    "topics": 13,
}
EXPECTED_SCAN_TOTAL_BYTES = 5875430
EXPECTED_PROJECTED = {
    "dec.csv": (410467, "9295BCD5D3BCF93376BC4DC6A565B9D515ABD2E608BA2B000B67824DD7943D79"),
    "issues.csv": (35465, "E8E7A81AEF7E1509CF05E746D0CA32597F6DDF2B77909195A17F43A32BB43C25"),
    "map.csv": (501183, "A4BDB33261A9AA950BD23C7046AC5E1FF9959EF6FE23DBA41B369F2EE2E52680"),
}
EXPECTED_DECISION_APPEND = (3742, "53EC78E78D3504FF34D1F76B5AC997C6791810899383327533F4966FF51A4EC7")
EXPECTED_ISSUE_APPEND = (1450, "ABB8BE14713E6ECCCD33F30F2C8A3BE5BB1B1FBEEB1C22EDB73C3813B1327C9B")
EXPECTED_TOOL_MAP = (501183, "C787784A513C959DD538590984F568E988C1F7F383F028CEE6D61EEBC3744083")
TOOL_TAG_ORDER_DELTAS = {
    "tohoku:section:2.3": ("0157;015A;013I;013K;05TI;05TH;0644;0646;06XQ;06XR;06XV;0149;06XS;01DU", "013I;013K;0149;0157;015A;01DU;05TH;05TI;0644;0646;06XQ;06XR;06XS;06XV"),
    "tohoku:section:2.4": ("0121;0122;011N;0AMI;012U;012Y;0130;0132;015H;015I;015J;015K;015M;015N;015E;015C;07K7;07K8;010T", "010T;011N;0121;0122;012U;012Y;0130;0132;015C;015E;015H;015I;015J;015K;015M;015N;07K7;07K8;0AMI"),
    "tohoku:section:3.3": ("09SW;0FKS;09SX;015E;01DG;01DI;006X;0079", "006X;0079;015E;01DG;01DI;09SW;09SX;0FKS"),
    "tohoku:section:3.4": ("09V1;02FN;0BE0;01X1", "01X1;02FN;09V1;0BE0"),
    "tohoku:section:3.6": ("02UX;02UZ;01AQ;01B2;0055;0051", "0051;0055;01AQ;01B2;02UX;02UZ"),
}

ROOT_BINDINGS = {
    "batch_design": DESIGN_SPEC,
    "source_repair": ("D1029_SOURCE_REPAIR_CHECK.json", 23296, "E996D56A24B4BCF4776CFE9351F2932E66E9B7ACB3B0493C877DEDCD13C63E02"),
    "d1029_review": ("tmp/d1029_post_live_independent_review_r1.json", 11808, "861F1C59B8091BEF7304E6E6249F3941AA05DECE48BB43B29D4872D5E319910D"),
    "d1030_review": ("tmp/d1030_post_live_independent_review_r1.json", 7590, "8C70D8029A5816C17AF91590455F519D623524348CF9DAFD3A078CCFE46D4D15"),
    "d1031_review": ("tmp/d1031_post_live_independent_review_r1.json", 7042, "B2D363CEADA81D1B279DD80B9F14FF561EC3B948CEB3FB0DA11A00C1B4D0E0AD"),
    "d1029_check": ("D1029_CHECK.json", 5995, "0CAD062C244D2FC3066AE163FF7D137D8B1139337C0144C80E108EB8D0466356"),
    "d1030_check": ("D1030_CHECK.json", 4843, "6182FBBD43AAF6D05EFA0FE22833D703F7D09694A3708B6B0249B01C7B481514"),
    "d1031_check": ("D1031_CHECK.json", 4123, "6551E7C7912F99143798E0380FB154A0B70D17336CD22F0527C41EB6DF65AD45"),
    "final_scan_check": ("D1031_FINAL_SCAN_CHECK.json", 3723, "74DFE06F44036508CB184FC0792AABED83F3D4184FC008E298CEEBB022FB9FD6"),
}

EXPECTED_COUNTS = {
    "units": 991,
    "decisions": 1066,
    "decided_units": 679,
    "source_issues": 33,
    "active_source_issues": 0,
    "review_units": 0,
    "candidate_units": 0,
    "unit_candidates": 0,
    "graph_corrections": 0,
    "active_graph_corrections": 0,
    "dispositions": {
        "example_or_remark": 84,
        "existing_equivalent": 401,
        "existing_stronger": 41,
        "historical_reference": 33,
        "structural_only": 432,
    },
}
PROJECTED_COUNTS = {
    "decisions": 1066,
    "decided_units": 679,
    "issues": 33,
    "active_issues": 0,
    "existing_equivalent": 401,
    "existing_weaker": 0,
    "extend_existing": 0,
    "new_section": 0,
    "new_statement": 0,
    "structural_only": 432,
    "remaining_gap_class_dispositions": 0,
    "source_repairs_appended": 1,
    "mapping_closures_appended": 4,
    "changed_map_rows": 4,
}

STATUS_BYTES = (
    "# Tohoku Stacks mapping status\n\n"
    "- The sealed r70 dossier is preserved exactly; D001063-D001066 close its final four gap-class rows in one atomic no-overwrite r71 successor.\n"
    "- D001063 binds the frozen p.188 corrected-source chain, live Ext-center lemma, strict build/visual review, and appends resolved I000033 without changing I000032.\n"
    "- D001064 closes Proposition 3.4.1; D001065 then closes its section 3.4 parent; D001066 closes the bounded projective-effacement duality remark.\n"
    "- Exactly four decision rows, one resolved issue row, and four map-row replacements are admitted; no live TeX, PDF, canonical source, or cursor is modified.\n"
    "- The final scanner indexes 119 top-level TeX files with 22,116 labels, 688 warnings, and no errors.\n"
    "- There are 1,066 decisions, 679 decided units, 33 resolved source issues, and zero gap-class dispositions remain.\n"
    "- No release, publication, DOI, remote-freshness, rights, or whole-paper completion is claimed.\n"
).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def identity(data: bytes) -> tuple[int, str]:
    return len(data), digest(data)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_engine() -> types.ModuleType:
    payload = ENGINE_PATH.read_bytes()
    require(identity(payload) == ENGINE_IDENTITY, "r70 transaction engine identity drift")
    module = types.ModuleType("tohoku_r71_engine")
    module.__file__ = str(ENGINE_PATH)
    exec(compile(payload, str(ENGINE_PATH), "exec"), module.__dict__)
    require(identity(ENGINE_PATH.read_bytes()) == ENGINE_IDENTITY, "r70 engine changed during load")
    return module


M = load_engine()
E = M.E


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes().decode("utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def bound(spec: tuple[str, int, str]) -> dict[str, Any]:
    return {"path": spec[0], "bytes": spec[1], "sha256": spec[2]}


def derive_design() -> tuple[dict[str, Any], list[dict[str, str]], dict[str, str], dict[str, dict[str, Any]], dict[str, str]]:
    path = ROOT / DESIGN_SPEC[0]
    E.require_identity(path, DESIGN_SPEC[1:], "r71 batch design")
    design = strict_json(path)
    require(design.get("schema") == "tohoku-stacks-final-four-gap-batch-design-v1", "r71 design schema drift")
    require(design.get("authorization", {}).get("design_verdict") == "STRICT_PASS_CONDITIONAL_BATCH_DESIGN", "r71 design authorization drift")
    require(design.get("decision_order", {}).get("ids") == ["D001063", "D001064", "D001065", "D001066"], "r71 decision order drift")
    decisions: list[dict[str, str]] = []
    tags: dict[str, str] = {}
    specs: dict[str, dict[str, Any]] = {}
    for item in design["decisions"]:
        successor = item["successor"]
        row = {key: str(successor[key]) for key in E.DEC_FIELDS}
        decisions.append(row)
        tags[row["decision_id"]] = str(successor["stacks_tags"])
        predecessor = item["predecessor"]
        specs[row["unit_id"]] = {
            "physical_line": int(predecessor["map_physical_line"]),
            "source_loc": predecessor["source_locator"],
            "predecessor_decision": predecessor["decision_id"],
            "predecessor_disposition": predecessor["disposition"],
            "predecessor_review": predecessor["review_state"],
            "predecessor_labels": predecessor["stacks_labels"],
            "predecessor_tags": predecessor["stacks_tags"],
            "predecessor_row": (int(predecessor["map_row_bytes_with_lf"]), predecessor["map_row_sha256_with_lf"]),
            "predecessor_decision_line": int(predecessor["decision_physical_line"]),
            "predecessor_decision_row": (int(predecessor["decision_row_bytes_with_lf"]), predecessor["decision_row_sha256_with_lf"]),
            "successor_row": (int(item["projected_map_row"]["bytes_with_lf"]), item["projected_map_row"]["sha256_with_lf"]),
            "successor_decision_row": (int(item["projected_decision_row"]["bytes_with_lf"]), item["projected_decision_row"]["sha256_with_lf"]),
        }
    issue = {key: str(design["exact_issue_append"]["row"][key]) for key in E.ISSUE_FIELDS}
    require(issue["issue_id"] == "I000033" and issue["resolution_decision"] == "D001063", "r71 issue template drift")
    absolute = design["projected_counts"]["absolute_successor"]
    require(all(absolute.get(k) == PROJECTED_COUNTS[k] for k in ("decisions", "decided_units", "issues", "active_issues", "existing_equivalent", "existing_weaker", "extend_existing", "new_section", "new_statement", "structural_only", "remaining_gap_class_dispositions")), "r71 design count projection drift")
    return design, decisions, tags, specs, issue


DESIGN, DECISIONS, OFFICIAL_TAGS, MAP_SPECS, ISSUE = derive_design()


def scanner_contract() -> dict[str, Any]:
    return {
        "oracle_path": "tmp/d1031_final_scan_probe_r1",
        "replay_path": "tmp/d1031_final_scan_probe_replay_r1",
        "files": {name: {"bytes": spec[0], "sha256": spec[1]} for name, spec in EXPECTED_SCAN.items()},
        "counts": {**EXPECTED_SCAN_COUNTS, "warnings": 688, "errors": 0},
        "inventory": {"files": 6, "bytes": EXPECTED_SCAN_TOTAL_BYTES},
    }


def map_contract() -> dict[str, Any]:
    return {
        unit: {
            "physical_line": spec["physical_line"],
            "predecessor_row": {"bytes": spec["predecessor_row"][0], "sha256": spec["predecessor_row"][1]},
            "successor_row": {"bytes": spec["successor_row"][0], "sha256": spec["successor_row"][1]},
        }
        for unit, spec in MAP_SPECS.items()
    }


def load_contract() -> dict[str, Any]:
    require(CONTRACT_PATH.is_file() and not CONTRACT_PATH.is_symlink(), "r71 contract missing or unsafe")
    contract = strict_json(CONTRACT_PATH)
    require(contract.get("schema") == "tohoku-r71-transaction-contract-v1" and contract.get("contract_id") == CONTRACT_ID, "r71 contract identity mismatch")
    script = contract.get("script", {})
    require(script.get("path") == "srcmap/build_tohoku_r71.py" and identity(SCRIPT_PATH.read_bytes()) == (script.get("bytes"), script.get("sha256")), "r71 script pin mismatch")
    engine = contract.get("engine", {})
    require(engine == {"path": "srcmap/build_tohoku_r70.py", "bytes": ENGINE_IDENTITY[0], "sha256": ENGINE_IDENTITY[1]}, "r71 engine pin mismatch")
    require(contract.get("predecessor") == {"path": "tohoku_r70/r70-check.json", "bytes": EXPECTED_R70_RECEIPT[0], "sha256": EXPECTED_R70_RECEIPT[1]}, "r71 predecessor contract mismatch")
    require(contract.get("frozen_prerequisites") == [bound(ROOT_BINDINGS[key]) for key in ROOT_BINDINGS], "r71 frozen prerequisites mismatch")
    require(contract.get("scanner_probe") == scanner_contract(), "r71 scanner contract mismatch")
    require(contract.get("decision_order") == [row["decision_id"] + ":" + row["unit_id"] for row in DECISIONS], "r71 decision-order contract mismatch")
    require(contract.get("decision_append") == {"bytes": EXPECTED_DECISION_APPEND[0], "sha256": EXPECTED_DECISION_APPEND[1]}, "r71 decision append contract mismatch")
    require(contract.get("issue_append") == {"issue_id": "I000033", "bytes": EXPECTED_ISSUE_APPEND[0], "sha256": EXPECTED_ISSUE_APPEND[1]}, "r71 issue append contract mismatch")
    require(contract.get("projected_counts") == PROJECTED_COUNTS, "r71 projected-count contract mismatch")
    require(contract.get("projected_files") == {name: {"bytes": spec[0], "sha256": spec[1]} for name, spec in EXPECTED_PROJECTED.items()}, "r71 projected-file contract mismatch")
    require(contract.get("tool_map_normalization") == {"raw_map": {"bytes": EXPECTED_TOOL_MAP[0], "sha256": EXPECTED_TOOL_MAP[1]}, "field": "stacks_tags", "deltas": {unit: {"raw": pair[0], "authorized": pair[1]} for unit, pair in TOOL_TAG_ORDER_DELTAS.items()}, "rule": "preserve four inherited r70 canonical tag orders and freeze the authorized section 3.4 order; every delta has the same unique tag set"}, "r71 map normalization contract mismatch")
    require(contract.get("map_rows") == map_contract() and contract.get("target") == "tohoku_r71", "r71 map/target contract mismatch")
    txn = contract.get("transaction", {})
    require(txn.get("source") == "tohoku_r70" and txn.get("stage") == "tohoku_r71.__stage__", "r71 transaction path mismatch")
    require(all(txn.get(key) is True for key in ("no_overwrite", "atomic_directory_rename", "post_promotion_replay", "rollback_on_failed_replay", "partial_successor_forbidden")), "r71 transaction guarantees missing")
    return {
        "script": E.record(SCRIPT_PATH, "srcmap/build_tohoku_r71.py"),
        "contract": E.record(CONTRACT_PATH, "srcmap/tohoku_r71_contract.json"),
        "engine": E.record(ENGINE_PATH, "srcmap/build_tohoku_r70.py"),
        "python": E.record(Path(sys.executable).resolve(), "python.exe"),
    }


def expected_cfg_bytes() -> bytes:
    data = (E.SOURCE / "cfg.json").read_bytes()
    require(identity(data) == EXPECTED_SCAN["cfg.json"], "inherited r71 cfg drift")
    return data


def expected_decision_bytes() -> bytes:
    fields, rows = E.load_csv(E.SOURCE / "dec.csv")
    require(fields == E.DEC_FIELDS and len(rows) == 1062 and rows[-1]["decision_id"] == "D001062", "r70 decision schema/count/tail drift")
    append = E.csv_bytes(E.DEC_FIELDS, DECISIONS, header=False)
    require(identity(append) == EXPECTED_DECISION_APPEND, "r71 decision append drift")
    data = (E.SOURCE / "dec.csv").read_bytes() + append
    require(identity(data) == EXPECTED_PROJECTED["dec.csv"], "r71 projected decisions drift")
    return data


def expected_issue_bytes() -> bytes:
    fields, rows = E.load_csv(E.SOURCE / "issues.csv")
    require(fields == E.ISSUE_FIELDS and len(rows) == 32 and rows[-1]["issue_id"] == "I000032", "r70 issue schema/count/tail drift")
    append = E.csv_bytes(E.ISSUE_FIELDS, [ISSUE], header=False)
    require(identity(append) == EXPECTED_ISSUE_APPEND, "I000033 append drift")
    data = (E.SOURCE / "issues.csv").read_bytes() + append
    require(identity(data) == EXPECTED_PROJECTED["issues.csv"], "r71 projected issues drift")
    return data


def expected_map_bytes() -> bytes:
    fields, rows = E.load_csv(E.SOURCE / "map.csv")
    require(fields == E.MAP_FIELDS and len(rows) == 991, "r70 map schema/count drift")
    by_unit = {row["unit_id"]: row for row in DECISIONS}
    replacements: dict[str, dict[str, str]] = {}
    for unit, spec in MAP_SPECS.items():
        selected = E.one_row(rows, "unit_id", unit, "r70 map")
        require(selected["decision_id"] == spec["predecessor_decision"] and selected["disposition"] == spec["predecessor_disposition"] and selected["review_state"] == spec["predecessor_review"], f"r70 predecessor state drift: {unit}")
        require(selected["stacks_labels"] == spec["predecessor_labels"] and selected["stacks_tags"] == spec["predecessor_tags"] and selected["source_loc"] == spec["source_loc"], f"r70 predecessor labels/tags/locator drift: {unit}")
        decision = by_unit[unit]
        replacement = selected.copy()
        replacement.update({
            "decision_id": decision["decision_id"],
            "disposition": decision["disposition"],
            "review_state": decision["review_state"],
            "stacks_labels": decision["stacks_labels"],
            "stacks_tags": OFFICIAL_TAGS[decision["decision_id"]],
            "rationale": decision["rationale"],
        })
        replacements[unit] = replacement
    data = E.csv_bytes(fields, [replacements.get(row["unit_id"], row) for row in rows])
    require(identity(data) == EXPECTED_PROJECTED["map.csv"], "r71 projected map drift")
    return data


def verify_predecessor() -> dict[str, Any]:
    receipt = E.SOURCE / "r70-check.json"
    E.require_identity(receipt, EXPECTED_R70_RECEIPT, "r70 receipt")
    for name, spec in EXPECTED_R70_FILES.items():
        E.require_identity(E.SOURCE / name, spec, f"r70/{name}")
    value = strict_json(receipt)
    require(value.get("schema") == "tohoku-stacks-mapping-successor-r70-v1" and value.get("status") == "PASS" and value.get("errors") == [], "r70 receipt state drift")
    require(value.get("deltas", {}).get("remaining_gap_class_dispositions") == 4, "r70 gap count drift")
    require({row.get("name"): (row.get("bytes"), row.get("sha256")) for row in value.get("files", [])} == EXPECTED_R70_FILES, "r70 receipt inventory drift")
    for unit, spec in MAP_SPECS.items():
        require(E.line_identity(E.SOURCE / "map.csv", spec["physical_line"]) == spec["predecessor_row"], f"r70 target map-row drift: {unit}")
        require(E.line_identity(E.SOURCE / "dec.csv", spec["predecessor_decision_line"]) == spec["predecessor_decision_row"], f"r70 predecessor decision-row drift: {unit}")
    return {"receipt": E.record(receipt, "tohoku_r70/r70-check.json"), "files": [E.record(E.SOURCE / name, f"tohoku_r70/{name}") for name in sorted(EXPECTED_R70_FILES)]}


def verify_external() -> dict[str, Any]:
    execution = load_contract()
    predecessor = verify_predecessor()
    records: dict[str, Any] = {}
    for role, spec in ROOT_BINDINGS.items():
        path = ROOT / spec[0]
        E.require_identity(path, spec[1:], role)
        records[role] = E.record(path, spec[0])
    repair = strict_json(ROOT / ROOT_BINDINGS["source_repair"][0])
    require(repair.get("schema") == "tohoku-d1029-p188-source-repair-chain-check-v1" and repair.get("status") == "PASS_FROZEN_SOURCE_REPAIR_CHAIN" and repair.get("errors") == [], "D1029 source-repair gate drift")
    reviews = {
        "d1029": strict_json(ROOT / ROOT_BINDINGS["d1029_review"][0]),
        "d1030": strict_json(ROOT / ROOT_BINDINGS["d1030_review"][0]),
        "d1031": strict_json(ROOT / ROOT_BINDINGS["d1031_review"][0]),
    }
    require(reviews["d1029"].get("verdict") == "STRICT_PASS" and reviews["d1029"].get("errors") == [] and reviews["d1029"].get("actionable_edits") == [], "D1029 post-live review drift")
    require(reviews["d1030"].get("verdict") == "STRICT_PASS" and reviews["d1030"].get("actionable_findings") == [], "D1030 post-live review drift")
    require(reviews["d1031"].get("verdict") == "STRICT_PASS" and reviews["d1031"].get("status") == "PASS_LIVE_SOURCE_BUILD_DEPENDENCIES_AND_VISUAL_QA", "D1031 post-live review drift")
    checks = [strict_json(ROOT / ROOT_BINDINGS[f"d{number}_check"][0]) for number in (1029, 1030, 1031)]
    expected_states = [
        ("tohoku-stacks-d1029-check-v1", "STRICT_PASS_SOURCE_REPAIR_R71_MAPPING_AND_I000033_AUTHORIZED"),
        ("tohoku-stacks-d1030-check-v1", "STRICT_PASS_R71_CHILD_AND_PARENT_MAPPING_AUTHORIZED"),
        ("tohoku-stacks-d1031-check-v1", "STRICT_PASS_R71_MAPPING_AUTHORIZED"),
    ]
    live_records: list[dict[str, Any]] = []
    build_records: list[dict[str, Any]] = []
    for check, (schema, status) in zip(checks, expected_states):
        require(check.get("schema") == schema and check.get("status") == status and check.get("errors") == [], f"{schema} gate drift")
        require(check.get("predecessor_receipt") == {"path": "tohoku_r70/r70-check.json", "bytes": EXPECTED_R70_RECEIPT[0], "sha256": EXPECTED_R70_RECEIPT[1], "status": "PASS"}, f"{schema} predecessor binding drift")
        for item in check.get("frozen_inputs", []):
            E.require_identity(ROOT / item["path"], (item["bytes"], item["sha256"]), f"{schema} frozen input")
        live = check["live_insertion"]
        E.require_identity(ROOT / live["path"], (live["bytes"], live["sha256"]), f"{schema} live source")
        candidate = next(item for item in check["frozen_inputs"] if item["path"].endswith("candidate.tex"))
        require((ROOT / live["path"]).read_bytes().count((ROOT / candidate["path"]).read_bytes()) == 1 and live["candidate_occurrences"] == 1 and live["label_occurrences"] == 1, f"{schema} live candidate occurrence drift")
        live_records.append(E.record(ROOT / live["path"], live["path"]))
        build = check["build"]
        require(build.get("exit_code") == 0 and build["pdf"].get("open") == "PASS" and build["log"].get("errors") == 0 and build["log"].get("warnings") == 0 and build["log"].get("undefined_references") == 0, f"{schema} build gate drift")
        for key in ("aux", "log", "pdf"):
            item = build[key]
            E.require_identity(ROOT / item["path"], (item["bytes"], item["sha256"]), f"{schema} build {key}")
            build_records.append(E.record(ROOT / item["path"], item["path"]))
        qa = check["visual_qa"]
        require(qa.get("independent_verdict") == "STRICT_PASS" and all(qa.get(key) == 0 for key in ("clipping", "overlap", "bad_breaks", "missing_glyphs", "malformed_math")), f"{schema} visual gate drift")
        require(check["scanner"].get("status") == "PASS_BYTE_IDENTICAL_ORACLE_AND_REPLAY" and check["scanner"].get("errors") == 0, f"{schema} scanner gate drift")
    auth29 = checks[0]["mapping_authorization"]
    require(auth29.get("decision_id") == "D001063" and auth29.get("unit_id") == DECISIONS[0]["unit_id"] and auth29.get("labels") == DECISIONS[0]["stacks_labels"] and auth29.get("tags") == OFFICIAL_TAGS["D001063"] and auth29.get("supersedes") == DECISIONS[0]["supersedes"], "D1029 mapping authorization drift")
    require(checks[0]["issue_authorization"].get("row_sha256_with_lf") == EXPECTED_ISSUE_APPEND[1] and checks[0]["issue_authorization"].get("issue_id") == "I000033", "D1029 issue authorization drift")
    require(checks[1]["mapping_authorization"]["child"].get("decision_id") == "D001064" and checks[1]["mapping_authorization"]["parent"].get("decision_id") == "D001065", "D1030 child/parent authorization drift")
    require(checks[2]["mapping_authorization"].get("decision_id") == "D001066" and checks[2]["mapping_authorization"].get("labels") == DECISIONS[3]["stacks_labels"], "D1031 mapping authorization drift")
    final_scan = strict_json(ROOT / ROOT_BINDINGS["final_scan_check"][0])
    require(final_scan.get("schema") == "tohoku-stacks-final-three-live-scanner-check-v1" and final_scan.get("status") == "STRICT_PASS_BYTE_IDENTICAL_ORACLE_AND_REPLAY" and final_scan.get("authorization") == "PASS_FINAL_SCANNER_GATE_FOR_ATOMIC_R71_TRANSACTION", "final scanner audit drift")
    return {"execution": execution, "predecessor": predecessor, "frozen": records, "live_sources": live_records, "build_artifacts": build_records}


def verify_scan(root: Path, oracle_surface: bool = False) -> dict[str, Any]:
    if oracle_surface:
        require({path.name for path in root.iterdir() if path.is_file()} == set(EXPECTED_SCAN) and not any(path.is_dir() for path in root.iterdir()), f"scanner surface drift: {root}")
    for name, spec in EXPECTED_SCAN.items():
        E.require_identity(root / name, spec, f"{root.name}/{name}")
    check = strict_json(root / "check.json")
    require(check.get("status") == "PASS" and check.get("errors") == [] and check.get("counts") == EXPECTED_SCAN_COUNTS and len(check.get("warnings", [])) == 688, "r71 scanner state/count drift")
    expected_tex = {
        "cohomology.tex": "028EE1CCEAF173129AA34BC3A407C9D8EE08324F233449E81405D699E58314F9",
        "divisors.tex": "6AFD21925A593A1D302776825ABB176768BDB7E5966982EC04542FAF637AF86C",
        "homology.tex": "7520BDAD32E68DB449A671802A5D0B2EFAA6EE4EDEC94206F313AB23AB1B6908",
    }
    require(all(check.get("tex_sha256", {}).get(name) == sha for name, sha in expected_tex.items()), "r71 scanner live-TeX binding drift")
    _, rows = E.load_csv(root / "stx.csv")
    new_rows = [
        ("cohomology-lemma-ext-center-actions-left-modules", "cohomology.tex", "15192", 3531, (226, "490265F4F43F58ACF09A55705465F2868EF64042B2E24F21423B0BB3873A72E6"), "CF4444C677BA519B8901A1503FF8F439762D24540A289DCACD2C074576757DEC"),
        ("divisors-lemma-locally-UFD-projective-linear-torsors-lift", "divisors.tex", "6869", 6169, (242, "D2EA25BF58D15347830E0D3A8F1E0011DD73E9B396EF8F68B5D8F736E3341ADF"), "96C11001AE948835FAFC680669F2BF30E3BE9CDDE3861BF2DCF160729DC2A4D1"),
        ("homology-lemma-projective-effacement-opposite-category", "homology.tex", "10315", 10052, (244, "D887FE44FCC11E8AF82F713C7E407E5D4E4A213F66AF03E4B80C9147A2175504"), "814BA8AFE87A3EAB594E8DE6B681E9D2AD38267B0C3954E31BA2F2D579FD9493"),
    ]
    for label, file, line, physical, row_id, text_sha in new_rows:
        row = E.one_row(rows, "full_label", label, "r71 scanner label")
        require(row["file"] == file and row["line"] == line and row["tag"] == "" and row["text_sha256"] == text_sha, f"r71 scanner label drift: {label}")
        require(E.line_identity(root / "stx.csv", physical) == row_id, f"r71 scanner row identity drift: {label}")
    labels = {row["full_label"] for row in rows}
    require({label for decision in DECISIONS for label in decision["stacks_labels"].split(";") if label} <= labels, "r71 authorized scanner label missing")
    return check


def verify_oracles() -> dict[str, Any]:
    for root in (E.ORACLE, E.ORACLE_REPLAY):
        require(root.is_dir() and not root.is_symlink(), f"scanner oracle missing or unsafe: {root}")
        verify_scan(root, oracle_surface=True)
    for name in EXPECTED_SCAN:
        require((E.ORACLE / name).read_bytes() == (E.ORACLE_REPLAY / name).read_bytes(), f"r71 scanner replay differs: {name}")
    return {
        "oracle": [E.record(E.ORACLE / name, f"tmp/d1031_final_scan_probe_r1/{name}") for name in sorted(EXPECTED_SCAN)],
        "replay": [E.record(E.ORACLE_REPLAY / name, f"tmp/d1031_final_scan_probe_replay_r1/{name}") for name in sorted(EXPECTED_SCAN)],
    }


def verify_tool_stage(root: Path) -> None:
    require(root.is_dir() and not root.is_symlink(), "missing or unsafe raw r71 stage")
    require({path.name for path in root.iterdir() if path.is_file()} == E.PAYLOAD and not any(path.is_dir() for path in root.iterdir()), "raw r71 stage surface drift")
    require((root / "cfg.json").read_bytes() == expected_cfg_bytes(), "raw r71 cfg drift")
    for name in ("intake.json", "units.csv", "topics.csv"):
        require((root / name).read_bytes() == (E.SOURCE / name).read_bytes(), f"raw inherited r71 payload drift: {name}")
    require((root / "dec.csv").read_bytes() == expected_decision_bytes() and (root / "issues.csv").read_bytes() == expected_issue_bytes(), "raw r71 decision/issue drift")
    E.require_identity(root / "map.csv", EXPECTED_TOOL_MAP, "raw r71 map-tool output")
    require((root / "STATUS.md").read_bytes() == STATUS_BYTES, "raw r71 STATUS drift")
    verify_scan(root)
    mcheck = strict_json(root / "mcheck.json")
    require(mcheck.get("status") == "PASS" and mcheck.get("errors") == [] and mcheck.get("counts") == EXPECTED_COUNTS and len(mcheck.get("warnings", [])) == 688, "raw r71 mapping check drift")


def normalize_tool_map(root: Path) -> None:
    verify_tool_stage(root)
    fields, raw_rows = E.load_csv(root / "map.csv")
    reader = csv.DictReader(io.StringIO(expected_map_bytes().decode("utf-8"), newline=""))
    expected_rows = [dict(row) for row in reader]
    require(reader.fieldnames == fields and len(raw_rows) == len(expected_rows), "r71 normalization schema drift")
    deltas = []
    for raw, expected in zip(raw_rows, expected_rows):
        require(raw["unit_id"] == expected["unit_id"], "r71 normalization row order drift")
        for field in fields:
            if raw[field] != expected[field]:
                deltas.append((raw["unit_id"], field, raw[field], expected[field]))
    require(deltas == [(unit, "stacks_tags", pair[0], pair[1]) for unit, pair in TOOL_TAG_ORDER_DELTAS.items()], "r71 normalization delta drift")
    require(all(set(raw.split(";")) == set(authorized.split(";")) and len(raw.split(";")) == len(set(raw.split(";"))) for raw, authorized in TOOL_TAG_ORDER_DELTAS.values()), "r71 normalization tag-set drift")
    temporary = root / ".map-authorized-order.tmp"
    require(not temporary.exists(), "r71 normalization temp exists")
    E.exclusive_write(temporary, expected_map_bytes())
    temporary.replace(root / "map.csv")
    E.require_identity(root / "map.csv", EXPECTED_PROJECTED["map.csv"], "normalized r71 map")


def verify_stage(root: Path, receipt_mode: bool = False) -> dict[str, Any]:
    require(root.is_dir() and not root.is_symlink(), f"missing or unsafe r71 output: {root}")
    require({path.name for path in root.iterdir() if path.is_file()} == E.PAYLOAD | ({"r71-check.json"} if receipt_mode else set()) and not any(path.is_dir() for path in root.iterdir()), "r71 output surface drift")
    require((root / "cfg.json").read_bytes() == expected_cfg_bytes(), "r71 cfg drift")
    for name in ("intake.json", "units.csv", "topics.csv"):
        require((root / name).read_bytes() == (E.SOURCE / name).read_bytes(), f"r71 inherited payload drift: {name}")
    require((root / "dec.csv").read_bytes() == expected_decision_bytes(), "r71 decision drift")
    require((root / "issues.csv").read_bytes() == expected_issue_bytes(), "r71 issue drift")
    require((root / "map.csv").read_bytes() == expected_map_bytes(), "r71 map drift")
    require((root / "STATUS.md").read_bytes() == STATUS_BYTES, "r71 STATUS drift")
    E.require_identity(root / "ucand.csv", EXPECTED_R70_FILES["ucand.csv"], "r71/ucand.csv")
    verify_scan(root)
    mcheck = strict_json(root / "mcheck.json")
    require(mcheck.get("status") == "PASS" and mcheck.get("errors") == [] and mcheck.get("counts") == EXPECTED_COUNTS and len(mcheck.get("warnings", [])) == 688, "r71 mapping state/count drift")
    _, decisions = E.load_csv(root / "dec.csv")
    _, issues = E.load_csv(root / "issues.csv")
    _, mapping = E.load_csv(root / "map.csv")
    require([row["decision_id"] for row in decisions] == [f"D{n:06d}" for n in range(1, 1067)] and decisions[-4:] == DECISIONS, "r71 decision sequence/tail drift")
    require([row["issue_id"] for row in issues] == [f"I{n:06d}" for n in range(1, 34)] and issues[-1] == ISSUE, "r71 issue sequence/tail drift")
    by_unit = {row["unit_id"]: row for row in DECISIONS}
    for unit, spec in MAP_SPECS.items():
        row = E.one_row(mapping, "unit_id", unit, "r71 map")
        decision = by_unit[unit]
        require(row["decision_id"] == decision["decision_id"] and row["disposition"] == decision["disposition"] and row["review_state"] == decision["review_state"] and row["stacks_labels"] == decision["stacks_labels"] and row["stacks_tags"] == OFFICIAL_TAGS[decision["decision_id"]], f"r71 target state drift: {unit}")
        require(E.line_identity(root / "map.csv", spec["physical_line"]) == spec["successor_row"], f"r71 target row identity drift: {unit}")
    deltas = E.map_row_delta()
    expected_fields = {
        "tohoku:remark:ext-center-modules": {"decision_id", "disposition", "review_state", "stacks_labels", "stacks_tags", "rationale"},
        "tohoku:prop:3.4.1": {"decision_id", "disposition", "review_state", "stacks_labels", "rationale"},
        "tohoku:section:3.4": {"decision_id", "disposition", "review_state", "stacks_labels", "stacks_tags", "rationale"},
        "tohoku:thm:1.10.1:remark:4": {"decision_id", "disposition", "review_state", "stacks_labels", "rationale"},
    }
    require(len(deltas) == 22 and {row["unit_id"] for row in deltas} == set(MAP_SPECS), "r71 map delta cardinality/scope drift")
    require({unit: {row["field"] for row in deltas if row["unit_id"] == unit} for unit in MAP_SPECS} == expected_fields, "r71 map changed-field drift")
    gaps = sum(1 for row in mapping if row["disposition"] in {"existing_weaker", "extend_existing", "new_section", "new_statement"})
    require(gaps == 0, "r71 zero-gap projection drift")
    result = {
        "status": "PASS",
        "errors": [],
        "decisions": 1066,
        "decisions_appended": [row["decision_id"] for row in DECISIONS],
        "issues_appended": ["I000033"],
        "mapping_counts": EXPECTED_COUNTS,
        "scan_counts": {**EXPECTED_SCAN_COUNTS, "warnings": 688, "errors": 0},
        "remaining_gap_class_dispositions": 0,
        "source_repairs_appended": 1,
        "mapping_closures_appended": 4,
        "map_delta": {"changed_units": 4, "changed_fields": 22, "unchanged_units": 987},
        "semantic_inventory_generation": "sem/r18",
        "corrected_semantic_authority": "sem/r22 for D1029 only",
        "source_change": "D1029_D1030_D1031_FINAL_LIVE_SURFACE",
        "scanner_payload_change": "THREE_NEW_UNTAGGED_LABELS",
    }
    if receipt_mode:
        require(strict_json(root / "r71-check.json") == receipt_payload(root, result), "r71 receipt replay mismatch")
    return result


def receipt_payload(root: Path, deltas: Mapping[str, Any]) -> dict[str, Any]:
    external = verify_external()
    oracles = verify_oracles()
    return {
        "schema": "tohoku-stacks-mapping-successor-r71-v1",
        "status": "PASS",
        "errors": [],
        "execution": external["execution"],
        "predecessor": external["predecessor"],
        "formalization": {
            "batch_design": external["frozen"]["batch_design"],
            "D1029": {"source_repair": external["frozen"]["source_repair"], "post_live_review": external["frozen"]["d1029_review"], "audit": external["frozen"]["d1029_check"]},
            "D1030": {"post_live_review": external["frozen"]["d1030_review"], "audit": external["frozen"]["d1030_check"]},
            "D1031": {"post_live_review": external["frozen"]["d1031_review"], "audit": external["frozen"]["d1031_check"]},
            "final_scanner_audit": external["frozen"]["final_scan_check"],
            "live_sources": external["live_sources"],
            "build_artifacts": external["build_artifacts"],
            "change_class": "four_atomic_mapping_closures_one_resolved_issue_and_bound_external_source_repair",
        },
        "scanner_oracle": oracles["oracle"],
        "scanner_replay": oracles["replay"],
        "deltas": dict(deltas),
        "files": E.output_records(root),
        "nonclaims": [
            "The sem/r18 inventory and source locators remain fixed; sem/r22 is bound only as D1029's corrected authority.",
            "I000033 records the p.188 source error; I000032 and every predecessor issue remain byte-identical.",
            "No live TeX, PDF, source ledger, cursor, release, publication, DOI, remote freshness, rights, or whole-paper completion is claimed by this mapping transaction.",
        ],
    }


def configure_engine() -> None:
    E.SOURCE = ROOT / "tohoku_r70"
    E.TARGET = ROOT / "tohoku_r71"
    E.STAGE = ROOT / "tohoku_r71.__stage__"
    E.ORACLE = ROOT / "tmp" / "d1031_final_scan_probe_r1"
    E.ORACLE_REPLAY = ROOT / "tmp" / "d1031_final_scan_probe_replay_r1"
    E.CONTRACT_PATH = CONTRACT_PATH
    E.CONTRACT_ID = CONTRACT_ID
    E.EXPECTED_R60_RECEIPT = EXPECTED_R70_RECEIPT
    E.EXPECTED_R60_FILES = EXPECTED_R70_FILES
    E.EXPECTED_SCAN = EXPECTED_SCAN
    E.EXPECTED_SCAN_COUNTS = EXPECTED_SCAN_COUNTS
    E.EXPECTED_PROJECTED = EXPECTED_PROJECTED
    E.EXPECTED_APPEND_ROWS = {"decision": EXPECTED_DECISION_APPEND, "issue": EXPECTED_ISSUE_APPEND}
    E.EXPECTED_COUNTS = EXPECTED_COUNTS
    E.STATUS_BYTES = STATUS_BYTES
    E.DECISION = DECISIONS[-1]
    E.ISSUE = ISSUE
    E.load_contract = load_contract
    E.expected_cfg_bytes = expected_cfg_bytes
    E.expected_decision_bytes = expected_decision_bytes
    E.expected_issue_bytes = expected_issue_bytes
    E.expected_map_bytes = expected_map_bytes
    E.verify_predecessor = verify_predecessor
    E.verify_external = verify_external
    E.verify_scan = verify_scan
    E.verify_oracles = verify_oracles
    E.verify_stage = verify_stage
    E.receipt_payload = receipt_payload


configure_engine()


def oracle() -> None:
    load_contract()
    require(not E.TARGET.exists() and not E.STAGE.exists(), "r71 target or stage already exists")
    print(json.dumps({"schema": "tohoku-r71-scanner-oracle-v1", "status": "PASS_REPLAY", "errors": [], "scanner_oracles": verify_oracles(), "counts": {**EXPECTED_SCAN_COUNTS, "warnings": 688, "errors": 0}}, indent=2, sort_keys=True))


def preflight() -> None:
    require(not E.TARGET.exists() and not E.STAGE.exists(), "r71 target or stage already exists")
    external = verify_external()
    oracles = verify_oracles()
    projection = {name: identity(data) for name, data in {
        "cfg.json": expected_cfg_bytes(), "dec.csv": expected_decision_bytes(), "issues.csv": expected_issue_bytes(), "map.csv": expected_map_bytes(), "STATUS.md": STATUS_BYTES,
    }.items()}
    print(json.dumps({"schema": "tohoku-r71-static-input-audit-v1", "status": "PASS", "errors": [], "external": external, "scanner_oracles": oracles, "projection": projection, "decisions": [row["decision_id"] for row in DECISIONS], "issue": "I000033", "remaining_gaps": 0}, indent=2, sort_keys=True))


def execute() -> None:
    if E.TARGET.exists():
        replay()
        return
    if E.STAGE.exists():
        verify_external()
        verify_oracles()
        verify_tool_stage(E.STAGE)
    else:
        E.build_stage()
        verify_tool_stage(E.STAGE)
    normalize_tool_map(E.STAGE)
    deltas = verify_stage(E.STAGE)
    E.exclusive_write(E.STAGE / "r71-check.json", E.json_bytes(receipt_payload(E.STAGE, deltas)))
    verify_stage(E.STAGE, receipt_mode=True)
    require(not E.TARGET.exists(), "r71 target appeared before promotion")
    E.STAGE.rename(E.TARGET)
    try:
        verify_stage(E.TARGET, receipt_mode=True)
    except BaseException as exc:
        if E.TARGET.exists() and not E.STAGE.exists():
            E.TARGET.rename(E.STAGE)
        raise RuntimeError("post-promotion r71 replay failed; target rolled back") from exc
    print(json.dumps({"schema": "tohoku-r71-transaction-result-v1", "status": "PASS_COMMITTED", "errors": [], "target": "tohoku_r71", "receipt": E.record(E.TARGET / "r71-check.json"), "remaining_gaps": 0}, indent=2, sort_keys=True))


def replay() -> None:
    require(E.TARGET.is_dir() and not E.TARGET.is_symlink() and not E.STAGE.exists(), "r71 target/stage state invalid")
    result = verify_stage(E.TARGET, receipt_mode=True)
    print(json.dumps({"schema": "tohoku-r71-replay-v1", "status": "PASS_REPLAY", "errors": [], "receipt": E.record(E.TARGET / "r71-check.json"), "deltas": result}, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("oracle", "preflight", "execute", "replay"))
    args = parser.parse_args()
    try:
        {"oracle": oracle, "preflight": preflight, "execute": execute, "replay": replay}[args.mode]()
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
