#!/usr/bin/env python3
"""Build the no-overwrite, zero-open-gap GAGA r3 successor."""

from __future__ import annotations

import csv
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from build_gaga_r1 import csv_rows, identity, record, require, run, strict_json


ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "gaga_r2"
STAGE = ROOT / "gaga_r3.__stage__"
FINAL = ROOT / "gaga_r3"
SCAN_ORACLE = ROOT / "tmp" / "gaga_final_scan_oracle_r3"
SCAN_REPLAY = ROOT / "tmp" / "gaga_final_scan_replay_r3"
VISUAL_ROOT = ROOT / "tmp" / "pdfs" / "gaga_english_final_r3"

DECISION_FIELDS = [
    "decision_id",
    "unit_id",
    "action",
    "disposition",
    "stacks_labels",
    "rationale",
    "review_state",
    "supersedes",
]

PREDECESSOR_IDENTITIES = {
    "cfg.json": (2331, "B96D86DB7E186D8A748CBEE9602EEF4E980BC1CA1499795F6AC3FADF0D0295C7"),
    "check.json": (86546, "ADF9D89437FBD2E9E2C2C05ADC164B306424BE6BCD74FA73A02B70627DD9CEBB"),
    "dec.csv": (10775, "E322FB982E1CF81A9AFEFE830D7247B7EC9F13D0C5014A847DFCB8E888E61815"),
    "intake.json": (1200, "281322CD558109A475AE9FCF1A9FC3A246B2ED670BF11A57D9FD881B69C4990C"),
    "issues.csv": (88, "30C973E3978577AEBA6DE60B941DC4D88CACE6C3FCC3DDA50F6EB5F43D8BE9F5"),
    "map.csv": (66689, "9A94D3697176BCB177D830A1856ADB5F7E131FC3C91BE3DD8593E9F417DBA3B2"),
    "mcheck.json": (76096, "86364D728942CC823667279DB32D25D3D61D4D9C6498D0DBA3F7292F06AB3F6E"),
    "R1_CHECK.json": (11536, "90ABB05D7CDCA4710370E354F40DCF08429B2A7E4949BFCAC2C7DF2BE4CAC06B"),
    "R2_CHECK.json": (9058, "E68E9D515A0400CF5E6B809993A984D6B5FB02334B82A619388AC86B93724158"),
    "STATUS.md": (388, "DEC6402EF26ED4E6B77678F55494A3C25C3C3BCF1C021FCB0DD93A1714D57A9C"),
    "stx.csv": (5296860, "C68BFCDF8B1B2FCE9C2A03B48B4795A95CBC6E7108DFBF6D375FAD3A7D5ABFED"),
    "tcand.csv": (248118, "8D49B1053D911F968E6321A1C223081E1C2244709EE894293A627A3A449A677D"),
    "tmap.csv": (1792, "E1798EA106C06DC3E5E04B8A9C659B24409DCE9FD7A451119723C6776027FD99"),
    "topics.csv": (1875, "B603A8EE4DB16870D2F2E82ED03A7BFC34D88329CFB9DC612ADDD3BF7A061CF8"),
    "ucand.csv": (354357, "5251F7FD705A4B4BD6D5A268465AB34930E64B3081876905FA1A2535563D5AE5"),
    "units.csv": (60100, "8F8DB43D6732A1987ACD9A02BD47E96697CFDC35DFECDF9C6207977B1D515C9B"),
}

SOURCE_IDENTITIES = {
    "gaga_source_r1/english_source_aligned_workpass/components/02_associated_analytic_space.tex": (
        23350, "1EE5AED7FF6912F3CFE4D262951334A45C6FBC8F67A81DDDC15251BF02CEDE81"
    ),
    "gaga_source_r1/english_source_aligned_workpass/components/03_sheaf_correspondence_nos09_12.tex": (
        11808, "2A454DDF3F34EC17E71B7889CE59E2D64D422BE3CFD7AABF79E549E90BCC7447"
    ),
    "gaga_source_r1/english_source_aligned_workpass/components/04_proofs_theorems1_3_nos13_17.tex": (
        22613, "167DE10CD53AB8A2C4609DE4276B970B51A6C8D8169D2D5930EB45A77762D5A0"
    ),
    "gaga_source_r1/english_source_aligned_workpass/components/05_applications_nos18_20.tex": (
        16586, "57A91545836BD1CF09BB66BA8C1BE02227E46D0DEB20B8F4A27D55D4086402F3"
    ),
}

DESIGN_IDENTITIES = {
    "tmp/gaga_analytification_5_8_design.json": (
        35473, "A638E7B50B51659A2360D616DE5D1436BB12683F384849A2A6ED957EF87EB7ED"
    ),
    "tmp/gaga_sheaf_9_12_design.json": (
        45459, "63DDF7FF15AD92B53929904B0C30F509D44850B9C83911C270CEEB4BE103E183"
    ),
    "tmp/gaga_proofs_13_17_design.json": (
        49321, "2906E9B1BB03B75E9042135E475EFF47A2A9AB38047ABB3321975827747615B7"
    ),
    "tmp/gaga_applications_18_20_design.json": (
        12131, "7312A28003357C9EA6D9788C0A94F400AF15B51F8CEE4836EB076ABE8BFB26C3"
    ),
}

CANDIDATE_IDENTITIES = {
    "tmp/gaga_analytification_5_8_candidate.tex": (
        21726, "C465951DB15EEDAA888147A4D7AEC01076C5F0A7E59937E66B172DFA7EF0DAA9"
    ),
    "tmp/gaga_sheaf_9_12_candidate.tex": (
        9254, "4F9776E16E447171EDCF11AEB94FDBBF9A984559F582541F838CD439F531D446"
    ),
    "tmp/gaga_proofs_13_17_candidate.tex": (
        18173, "BB8C97D69A2A877A3D270EED01976A77798BAE501E1A997C52B9FFC6021E5530"
    ),
    "tmp/gaga_applications_18_20_candidate.tex": (
        16516, "393BBF45B93F0CC25AD267DB2E7ED2502B5943887E82A2CCEDBB95B71FF67F8F"
    ),
}

LIVE_IDENTITIES = {
    "gaga.tex": (79740, "BBCCEE29FE3AF084E8435F3E32F8537EE3DDED2558E1A9FCD2940F8664BB5201"),
    "preamble.tex": (8807, "8D6E0CD5B4CD6187E96A0FA289BD1A8C3B185310F22F4AAFAD39BE62ADF1BA65"),
    "chapters.tex": (8735, "C79BC934FA6DD52DB2A8AF11EECF3667CC3C682FA30239408679D62C4D49B299"),
    "my.bib": (220937, "953C5DFAEE8F1176A1F154B40B99C751EE206D41F030299E0DE7D9807F5128E8"),
    "Makefile": (7935, "5F185F219D5DCCD96483F6BADA73B4C450A208F2916CFE89C76433A59FD28C4C"),
    "tags/Makefile": (2434, "BEC02700270D972098655F7BAB91E1DC716DEBF098990AEA514DC9749793E9A8"),
}

BUILD_IDENTITIES = {
    "gaga.pdf": (496076, "93B61241CF64C402DDA3CB2CCD19909F5030E69244BFE8C455B5A95BC246BEC0"),
    "output/pdf/gaga-english.pdf": (496076, "93B61241CF64C402DDA3CB2CCD19909F5030E69244BFE8C455B5A95BC246BEC0"),
    "gaga.aux": (12020, "302FC15505F55F726CE0C80FF6C8B19F629E8F2297EB5D9314CFEF3750793599"),
    "gaga.out": (5659, "29F2D648721CD0188838B8316F143030F452310631EE12FCCDB8B55166958521"),
    "gaga.toc": (2287, "1696045525C8FC56178EA6B9A09A0B1A9F1B58E9F687EBB448C8CBD4C4EBAF16"),
    "gaga.log": (33737, "CD46D960816142021D6C4BC52A4ABF6866BC63A059599FE01FDC122D1F0F59B3"),
}

SCAN_IDENTITIES = {
    "cfg.json": (2331, "B96D86DB7E186D8A748CBEE9602EEF4E980BC1CA1499795F6AC3FADF0D0295C7"),
    "topics.csv": (1875, "B603A8EE4DB16870D2F2E82ED03A7BFC34D88329CFB9DC612ADDD3BF7A061CF8"),
    "check.json": (93387, "4AEAE7DFC4428E2146DAA41E71F5F8599623791EAB318EFE82A2685EBCFDFA0A"),
    "stx.csv": (5315575, "019EF2094A8E752C17BF7859B10E2C5212654619F12DD37E8796CEFB01D991A6"),
    "tcand.csv": (334451, "B23B4F9C29502CB1364BA63D5247C93DA0256785844FE4BAC40FF91FA9865C57"),
    "tmap.csv": (1792, "E1798EA106C06DC3E5E04B8A9C659B24409DCE9FD7A451119723C6776027FD99"),
}

ANALYTIC_EXISTING_STRONGER = {
    "gaga:lemma:2": [
        "morphisms-lemma-chevalley",
        "topology-lemma-dense-in-constructible",
        "gaga-lemma-dense-image-contains-open",
    ],
    "gaga:lemma:3": [
        "algebra-lemma-reduced-ring-sub-product-fields",
        "algebra-lemma-total-ring-fractions-no-embedded-points",
        "gaga-lemma-total-fractions-reduced",
    ],
}


def verify_identities(root: Path, expected: dict[str, tuple[int, str]]) -> None:
    for name, wanted in expected.items():
        path = root / name
        require(path.is_file() and identity(path) == wanted, f"Identity drift: {path}")


def artifact_records(expected: dict[str, tuple[int, str]]) -> list[dict[str, Any]]:
    return [record(ROOT / name, name) for name in expected]


def collect_decision_specs() -> tuple[list[dict[str, str]], dict[str, Any]]:
    verify_identities(ROOT, SOURCE_IDENTITIES)
    verify_identities(ROOT, DESIGN_IDENTITIES)
    verify_identities(ROOT, CANDIDATE_IDENTITIES)

    analytic = strict_json(ROOT / "tmp/gaga_analytification_5_8_design.json")
    sheaf = strict_json(ROOT / "tmp/gaga_sheaf_9_12_design.json")
    proofs = strict_json(ROOT / "tmp/gaga_proofs_13_17_design.json")
    applications = strict_json(ROOT / "tmp/gaga_applications_18_20_design.json")

    require(len(analytic.get("unit_audit", [])) == 18, "Analytification unit audit drift")
    require(len(sheaf.get("unit_decisions", [])) == 10, "Sheaf unit audit drift")
    require(len(proofs.get("projected_mapping_transaction", [])) == 10, "Proof projection drift")
    require(len(applications.get("projected_mapping_transaction", [])) == 17, "Applications projection drift")

    candidate_metadata = [
        analytic.get("candidate", {}),
        sheaf.get("candidate_artifact", {}),
        proofs.get("candidate", {}),
        applications.get("evidence", {}).get("candidate", {}),
    ]
    for metadata, (name, wanted) in zip(candidate_metadata, CANDIDATE_IDENTITIES.items(), strict=True):
        require(metadata.get("bytes") == wanted[0] and metadata.get("sha256") == wanted[1],
                f"Design-to-candidate identity drift: {name}")

    specs: list[dict[str, str]] = []
    for row in analytic["unit_audit"]:
        labels = row.get("planned_full_labels") or ANALYTIC_EXISTING_STRONGER.get(row["unit_id"], [])
        require(labels, f"Missing analytification successor labels: {row['unit_id']}")
        specs.append({
            "unit_id": row["unit_id"],
            "labels": ";".join(labels),
            "rationale": (
                "The integrated analytification continuation supplies the audited successor labels and "
                f"closes the pre-integration gap: {row['rationale']}"
            ),
        })

    full_by_local = {row["local"]: row["full"] for row in sheaf["planned_local_and_full_labels"]}
    require(len(full_by_local) == 16, "Sheaf planned-label inventory drift")
    for row in sheaf["unit_decisions"]:
        labels = [full_by_local[label] for label in row["planned_blocks"]]
        specs.append({
            "unit_id": row["unit_id"],
            "labels": ";".join(labels),
            "rationale": (
                "The integrated sheaf-correspondence continuation supplies the audited successor labels. "
                f"{row['rationale']}"
            ),
        })

    for row in proofs["projected_mapping_transaction"]:
        specs.append({
            "unit_id": row["unit_id"],
            "labels": row["stacks_labels"],
            "rationale": row["rationale"],
        })

    for row in applications["projected_mapping_transaction"]:
        labels = row.get("labels", [])
        require(labels, f"Missing application successor labels: {row['unit_id']}")
        specs.append({
            "unit_id": row["unit_id"],
            "labels": ";".join(labels),
            "rationale": row["rationale"],
        })

    require(len(specs) == 55 and len({row["unit_id"] for row in specs}) == 55,
            "Successor decision coverage drift")
    return specs, {
        "sources": artifact_records(SOURCE_IDENTITIES),
        "designs": artifact_records(DESIGN_IDENTITIES),
        "candidates": artifact_records(CANDIDATE_IDENTITIES),
        "component_units": {"analytification": 18, "sheaves_and_statements": 10,
                            "proofs": 10, "applications": 17},
    }


def verify_live_integration() -> dict[str, Any]:
    verify_identities(ROOT, LIVE_IDENTITIES)
    live = (ROOT / "gaga.tex").read_text(encoding="utf-8")
    for name in CANDIDATE_IDENTITIES:
        fragment = (ROOT / name).read_text(encoding="utf-8")
        require(live.count(fragment) == 1, f"Candidate not integrated exactly once: {name}")
    require(len(re.findall(r"(?m)^\\input\{chapters\}\s*$", live)) == 1,
            "Unique terminal chapter input drift")
    require(not re.search(r"(?m)^\+", live), "Literal integration marker remains in gaga.tex")
    return {
        "files": artifact_records(LIVE_IDENTITIES),
        "candidate_substrings": "PASS_ALL_FOUR_EXACTLY_ONCE",
        "terminal_chapter_input": "PASS_UNIQUE",
        "literal_integration_markers": 0,
    }


def verify_build() -> dict[str, Any]:
    verify_identities(ROOT, BUILD_IDENTITIES)
    log_text = (ROOT / "gaga.log").read_text(encoding="utf-8", errors="replace")
    for phrase in (
        "undefined references", "undefined citations", "Label(s) may have changed",
        "Rerun to get cross-references right", "Fatal error", "Emergency stop",
        "Overfull", "Underfull",
    ):
        require(phrase not in log_text, f"Forbidden final GAGA diagnostic: {phrase}")
    require("\\bibitem[Ser56]{GAGA}" in (ROOT / "gaga.bbl").read_text(encoding="utf-8"),
            "GAGA bibliography item missing")
    info = run(["pdfinfo", str(ROOT / "output/pdf/gaga-english.pdf")]).stdout
    require(re.search(r"^Pages:\s+22\s*$", info, re.MULTILINE) is not None,
            "English GAGA page count drift")
    pages = sorted(VISUAL_ROOT.glob("page-*.png"), key=lambda path: path.name)
    require([path.name for path in pages] == [f"page-{page:02d}.png" for page in range(1, 23)],
            "English visual-review page inventory drift")
    return {
        "files": artifact_records(BUILD_IDENTITIES),
        "pages": 22,
        "fixed_point_auxiliary_sha256": {
            name: BUILD_IDENTITIES[name][1] for name in ("gaga.aux", "gaga.out", "gaga.toc")
        },
        "diagnostics": "PASS_NO_UNDEFINED_RERUN_FATAL_OR_BOX_WARNINGS",
        "visual_review": {
            "status": "PASS_ALL_22_PAGES_PRIMARY_AGENT",
            "pages": [record(path, f"tmp/pdfs/gaga_english_final_r3/{path.name}") for path in pages],
        },
    }


def verify_scan(specs: list[dict[str, str]]) -> dict[str, Any]:
    verify_identities(SCAN_ORACLE, SCAN_IDENTITIES)
    verify_identities(SCAN_REPLAY, SCAN_IDENTITIES)
    check = strict_json(SCAN_ORACLE / "check.json")
    require(check.get("status") == "PASS" and check.get("errors") == [], "R3 scanner not PASS")
    require(check.get("counts") == {
        "labels": 22207,
        "official_tags_joined": 21437,
        "tex_files": 120,
        "topic_candidates": 870,
        "topic_coverage": {"direct": 4, "no_direct": 3, "partial": 2},
        "topics": 9,
    }, "R3 scanner counts drift")
    fields, rows = csv_rows(SCAN_ORACLE / "stx.csv")
    require("full_label" in fields, "Scanner label field missing")
    gaga_labels = [row for row in rows if row["file"] == "gaga.tex"]
    require(len(gaga_labels) == 90 and len({row["full_label"] for row in gaga_labels}) == 90,
            "Final GAGA label inventory drift")
    all_labels = {row["full_label"] for row in rows}
    mapped_labels = {label for spec in specs for label in spec["labels"].split(";")}
    require(mapped_labels.issubset(all_labels),
            f"Mapped labels absent from scanner: {sorted(mapped_labels - all_labels)}")
    return {
        "status": "PASS_BYTE_IDENTICAL_ORACLE_AND_REPLAY",
        "counts": check["counts"],
        "warnings": len(check.get("warnings", [])),
        "gaga_labels": 90,
        "mapped_labels_verified": len(mapped_labels),
        "files": [record(SCAN_ORACLE / name, f"scanner/{name}") for name in SCAN_IDENTITIES],
    }


def append_decisions(path: Path, specs: list[dict[str, str]]) -> list[dict[str, str]]:
    fields, rows = csv_rows(path)
    require(fields == DECISION_FIELDS and len(rows) == 24, "Predecessor decision ledger drift")
    require([row["decision_id"] for row in rows] == [f"D{n:06d}" for n in range(1, 25)],
            "Predecessor decision sequence drift")
    for offset, item in enumerate(specs, start=25):
        rows.append({
            "decision_id": f"D{offset:06d}",
            "unit_id": item["unit_id"],
            "action": "set",
            "disposition": "existing_equivalent",
            "stacks_labels": item["labels"],
            "rationale": item["rationale"],
            "review_state": "reviewed_source_stacks_integrated_build_scan_and_mapping",
            "supersedes": "",
        })
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DECISION_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def verify_mapping(base_map: list[dict[str, str]], decisions: list[dict[str, str]]) -> dict[str, Any]:
    mcheck = strict_json(STAGE / "mcheck.json")
    require(mcheck.get("status") == "PASS" and mcheck.get("errors") == [], "R3 mapping not PASS")
    counts = mcheck["counts"]
    require(counts.get("units") == 126 and counts.get("decisions") == 79
            and counts.get("decided_units") == 79, "R3 mapping count drift")
    require(counts.get("review_units") == 0 and counts.get("candidate_units") == 0,
            "R3 still has open review units")
    require(counts.get("dispositions") == {
        "existing_equivalent": 79,
        "historical_reference": 20,
        "structural_only": 27,
    }, "R3 disposition histogram drift")
    fields, mapped = csv_rows(STAGE / "map.csv")
    require(len(mapped) == len(base_map) == 126, "R3 map size drift")
    new_by_unit = {row["unit_id"]: row for row in decisions[24:]}
    changed_units: list[str] = []
    required = {"decision_id", "disposition", "review_state", "stacks_labels", "rationale"}
    for old, new in zip(base_map, mapped, strict=True):
        require(old["unit_id"] == new["unit_id"], "R3 map order drift")
        changed = {field for field in fields if old[field] != new[field]}
        decision = new_by_unit.get(new["unit_id"])
        if decision is None:
            require(not changed, f"Unauthorized R3 map delta: {new['unit_id']} {sorted(changed)}")
        else:
            require(changed in (required, required | {"stacks_tags"}),
                    f"Unexpected R3 map delta: {new['unit_id']} {sorted(changed)}")
            require(new["decision_id"] == decision["decision_id"]
                    and new["disposition"] == "existing_equivalent"
                    and new["review_state"] == decision["review_state"]
                    and new["stacks_labels"] == decision["stacks_labels"]
                    and new["rationale"] == decision["rationale"],
                    f"R3 decision projection drift: {new['unit_id']}")
            changed_units.append(new["unit_id"])
    expected_order = [row["unit_id"] for row in decisions[24:]]
    require(changed_units == expected_order, "R3 changed-unit order drift")
    return {
        "counts": counts,
        "changed_units": changed_units,
        "changed_rows": 55,
        "unchanged_rows": 71,
        "gaga_true_gaps_after": 0,
        "remaining_needs_review": 0,
    }


def main() -> int:
    require(not STAGE.exists() and not FINAL.exists(), "No-overwrite R3 target exists")
    verify_identities(BASE, PREDECESSOR_IDENTITIES)
    predecessor = strict_json(BASE / "R2_CHECK.json")
    require(predecessor.get("status") == "STRICT_PASS", "R2 predecessor not PASS")
    _, base_map = csv_rows(BASE / "map.csv")
    review_order = [row["unit_id"] for row in base_map if row["disposition"] == "needs_review"]
    require(len(review_order) == 55, "Predecessor needs-review inventory drift")

    specs, source = collect_decision_specs()
    require([row["unit_id"] for row in specs] == review_order,
            "Component decision order differs from predecessor needs-review order")
    integration = verify_live_integration()
    build = verify_build()
    scan = verify_scan(specs)

    shutil.copytree(BASE, STAGE)
    for name in SCAN_IDENTITIES:
        shutil.copy2(SCAN_ORACLE / name, STAGE / name)
    decisions = append_decisions(STAGE / "dec.csv", specs)
    run([sys.executable, str(ROOT / "srcmap" / "map.py"), str(STAGE)])
    first = {name: identity(STAGE / name) for name in ("map.csv", "ucand.csv", "mcheck.json")}
    run([sys.executable, str(ROOT / "srcmap" / "map.py"), str(STAGE)])
    second = {name: identity(STAGE / name) for name in ("map.csv", "ucand.csv", "mcheck.json")}
    require(first == second, "R3 mapping replay not byte-identical")
    mapping = verify_mapping(base_map, decisions)

    status = (
        "# GAGA r3\n\n"
        "- Inherits the strictly sealed GAGA r2 foundation successor.\n"
        "- Integrates analytification, coherent sheaves, the three comparison proofs, and applications.\n"
        "- All 126 source units are now classified; all 79 substantive units have reviewed decisions.\n"
        "- The 22-page English chapter, deterministic scanner replay, and mapping replay pass.\n"
        "- No GAGA needs-review or substantive statement gaps remain.\n"
    )
    (STAGE / "STATUS.md").write_text(status, encoding="utf-8", newline="\n")
    receipt = {
        "schema": "gaga-stacks-mapping-successor-r3-v1",
        "status": "STRICT_PASS",
        "errors": [],
        "predecessor": {
            "receipt": record(BASE / "R2_CHECK.json", "gaga_r2/R2_CHECK.json"),
            "map": record(BASE / "map.csv", "gaga_r2/map.csv"),
            "mcheck": record(BASE / "mcheck.json", "gaga_r2/mcheck.json"),
        },
        "source_and_design": source,
        "integration": integration,
        "build": build,
        "scanner": scan,
        "mapping": mapping,
        "mapping_replay": {
            "status": "PASS_BYTE_IDENTICAL",
            "files": [record(STAGE / name, name) for name in ("map.csv", "ucand.csv", "mcheck.json")],
        },
        "files_before_receipt": [
            record(path, path.name)
            for path in sorted(STAGE.iterdir(), key=lambda item: item.name)
            if path.is_file() and path.name != "R3_CHECK.json"
        ],
        "terminal_condition": {
            "gaga_true_statement_gaps": 0,
            "remaining_gaga_needs_review": 0,
            "english_pages_visually_reviewed": 22,
            "next": "Build and audit the Japanese and Simplified-Chinese editions, then publish.",
        },
    }
    (STAGE / "R3_CHECK.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    require(strict_json(STAGE / "R3_CHECK.json").get("status") == "STRICT_PASS",
            "R3 receipt reread failed")
    STAGE.rename(FINAL)
    result = {
        "status": "STRICT_PASS",
        "path": str(FINAL),
        "receipt": record(FINAL / "R3_CHECK.json", "gaga_r3/R3_CHECK.json"),
        "gaga_true_statement_gaps": 0,
        "remaining_needs_review": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
