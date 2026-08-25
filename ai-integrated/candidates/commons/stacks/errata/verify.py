from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "builds" / "validation.json"

AUTHORITY_HASHES = {
    "authority/COPYING": "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85",
    "authority/upstream.lock.json": "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D",
    "authority/scripts/add_tags.py": "0DABED0680C4D0CEAF673CAF145B19ED9A838D936C4E5E1688DE508CC58DEB91",
    "authority/scripts/functions.py": "6E26FB192D0DB45CD533BE8719A26DFF4D353956B9EF615C269491813DFE0382",
    "authority/source/smoothing.tex": "FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068",
    "authority/source/crystalline.tex": "466C0634A5E8E3899B157A42A4B4BB5F4357199F96708CAF5854F5A92BE58054",
    "authority/source/spaces-cohomology.tex": "63F19991B7B2BCE90B5FB30FCDBB8A3B06CBBFFEC42FA7C413776C29AE4B69C5",
    "authority/source/relative-cycles.tex": "F2050896436CD590D25869AFF1B6024C1B49D8A763D08EBBDC747F2815618750",
    "authority/source/more-morphisms.tex": "30F7B685A426BD02518CD30BE6F3D8E03646C3D9C1BB7B247B983C739ECB278F",
    "authority/source/topology.tex": "C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872",
    "authority/tags/tags": "098F77CCE75F8359F1EACB22B7AA0088099B09E5B3FFCAD2DE513CBD1A8A9F1C",
    "authority/ERRATA_LEDGER.jsonl": "23A9DDA3B5419E31A81598FDC95F5DBAAC6B65AF54E1B0EAC80D06ADB107F332",
    "authority/producer-hashes.json": "916A6DC09AB996DEE4CBE213D7EA271E60D6B4B0695C797F0BE58DCCF8894D55",
}

REPLACEMENTS = {
    "smoothing.tex": [
        (
            "let $A = R[x_1, \\ldots, x_n]/(f_1, \\ldots, f_m)$, $c$, and $a' \\in A$",
            "let $A = R[x_1, \\ldots, x_n]/(f_1, \\ldots, f_m)$ and $c$",
        ),
        (
            "There exists finite type $R$-algebra map $A \\to C$ which has a",
            "There exists a finite type $R$-algebra map $A \\to C$ which has a",
        ),
        (
            "$f_1, \\ldots, f_c \\in R[y_1, \\ldots, y_c]$ lifting",
            "$f_1, \\ldots, f_c \\in R[y_1, \\ldots, y_m]$ lifting",
        ),
        (
            "Choose an enumerations $E = \\{a_1, \\ldots, a_n\\}$",
            "Choose an enumeration $E = \\{a_1, \\ldots, a_n\\}$",
        ),
        (
            "correspond $a_i/1$ where $a_1, \\ldots, a_m \\in A$ are generators of $A$",
            "correspond to $a_i/1$ where $a_1, \\ldots, a_m \\in A$ are generators of $A$",
        ),
    ],
    "crystalline.tex": [
        (
            "$t', t \\in I$.",
            "$t', t \\in T$.",
        )
    ],
    "spaces-cohomology.tex": [
        (
            "Then $Z \\to X$ is a finite morphism of schemes and the result is",
            "Then $X \\to Y$ is a finite morphism of schemes and the result is",
        ),
        (
            "\\otimes_{\\mathcal{B}_{\\overline{x}}}",
            "\\otimes_{\\mathcal{B}_{\\overline{y}}}",
        ),
        (
            "the behaviour of stalks under pushforward along a closed immersion",
            "the behaviour of stalks under pushforward along a finite morphism",
        ),
        (
            "$h_{U''}^\\# \\to h_U^\\# \\times h_{u'}^\\#$",
            "$h_{U''}^\\# \\to h_U^\\# \\times h_{U'}^\\#$",
        ),
        (
            "the sheaf $f_!$ is the sheafification of the presheaf",
            "the sheaf $f_!\\mathcal{G}$ is the sheafification of the presheaf",
        ),
        (
            "\\mathcal{G} \\otimes_\\mathbf{Z} \\underline{\\mathbf{Z}}(\\chi_p))$",
            "\\mathcal{G} \\otimes_\\mathbf{Z} \\underline{\\mathbf{Z}}(\\chi_p)$",
        ),
        (
            "$\\textit{Ab}(U_p)$",
            "$\\textit{Ab}(U_{p, \\etale})$",
        ),
    ],
}

NEW_TAGS = [
    "0HB4,topology-lemma-dense-in-constructible",
    "0HB5,more-morphisms-lemma-weighting-specialization",
    "0HB6,more-morphisms-lemma-weighting-on-dense-set",
    "0HB7,relative-cycles-section-weightings",
    "0HB8,relative-cycles-lemma-weightings-pre",
    "0HB9,relative-cycles-example-n-must-be-positive-sometimes",
    "0HBA,relative-cycles-example-Merkurjev",
    "0HBB,relative-cycles-lemma-flat-pullback-as-action",
    "0HBC,relative-cycles-lemma-flat-pullback-as-composition",
]

NEW_TAG_LABEL_SOURCES = {
    "topology-lemma-dense-in-constructible": ("topology.tex", "lemma-dense-in-constructible"),
    "more-morphisms-lemma-weighting-specialization": ("more-morphisms.tex", "lemma-weighting-specialization"),
    "more-morphisms-lemma-weighting-on-dense-set": ("more-morphisms.tex", "lemma-weighting-on-dense-set"),
    "relative-cycles-section-weightings": ("relative-cycles.tex", "section-weightings"),
    "relative-cycles-lemma-weightings-pre": ("relative-cycles.tex", "lemma-weightings-pre"),
    "relative-cycles-example-n-must-be-positive-sometimes": ("relative-cycles.tex", "example-n-must-be-positive-sometimes"),
    "relative-cycles-example-Merkurjev": ("relative-cycles.tex", "example-Merkurjev"),
    "relative-cycles-lemma-flat-pullback-as-action": ("relative-cycles.tex", "lemma-flat-pullback-as-action"),
    "relative-cycles-lemma-flat-pullback-as-composition": ("relative-cycles.tex", "lemma-flat-pullback-as-composition"),
}

STRUCTURE_PATTERNS = {
    "labels": re.compile(r"\\label\{[^{}]+\}"),
    "references": re.compile(r"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(r"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
    "environments": re.compile(r"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(r"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(f"{path}:{line_number}: {exc}") from exc
    return rows


def assert_exact_payload(name: str) -> dict:
    authority_path = ROOT / "authority" / "source" / name
    payload_path = ROOT / "payload" / name
    authority = authority_path.read_text(encoding="utf-8")
    payload = payload_path.read_text(encoding="utf-8")
    expected = authority
    applied = []
    for old, new in REPLACEMENTS[name]:
        count = expected.count(old)
        if count != 1:
            raise AssertionError(f"{name}: expected old span exactly once, observed {count}: {old!r}")
        expected = expected.replace(old, new, 1)
        applied.append({"old": old, "new": new, "count": 1})
    if payload != expected:
        raise AssertionError(f"{name}: payload has changes outside the mapped replacements")
    structure = {}
    for key, pattern in STRUCTURE_PATTERNS.items():
        before = pattern.findall(authority)
        after = pattern.findall(payload)
        if before != after:
            raise AssertionError(f"{name}: ordered {key} sequence changed")
        structure[key] = len(before)
    if authority.count("$$") != payload.count("$$"):
        raise AssertionError(f"{name}: display-math delimiter count changed")
    return {
        "authority_sha256": sha256(authority_path),
        "payload_sha256": sha256(payload_path),
        "authority_bytes": authority_path.stat().st_size,
        "payload_bytes": payload_path.stat().st_size,
        "mapped_replacements": applied,
        "structure": structure,
        "inline_dollar_delta": payload.count("$") - authority.count("$"),
    }


def assert_tags() -> dict:
    authority_path = ROOT / "authority" / "tags" / "tags"
    payload_path = ROOT / "payload" / "tags" / "tags"
    before = authority_path.read_text(encoding="utf-8").splitlines()
    after = payload_path.read_text(encoding="utf-8").splitlines()
    if after[: len(before)] != before:
        raise AssertionError("tags/tags: authority prefix changed")
    if after[len(before) :] != NEW_TAGS:
        raise AssertionError("tags/tags: appended records differ from allocator output")
    parsed = [line.split(",", 1) for line in after if line and not line.startswith("#")]
    tags = [row[0] for row in parsed]
    labels = [row[1] for row in parsed]
    if len(tags) != len(set(tags)):
        raise AssertionError("tags/tags: duplicate permanent tag code")
    if len(labels) != len(set(labels)):
        raise AssertionError("tags/tags: duplicate full label")
    authority_labels = {line.split(",", 1)[1] for line in before if line and not line.startswith("#")}
    for full_label, (source_name, local_label) in NEW_TAG_LABEL_SOURCES.items():
        if full_label in authority_labels:
            raise AssertionError(f"tags/tags: supposedly missing label already registered: {full_label}")
        source_text = (ROOT / "authority" / "source" / source_name).read_text(encoding="utf-8")
        marker = f"\\label{{{local_label}}}"
        if source_text.count(marker) != 1:
            raise AssertionError(f"{source_name}: expected exactly one live label {marker}")
    return {
        "authority_sha256": sha256(authority_path),
        "payload_sha256": sha256(payload_path),
        "authority_records": len(before),
        "payload_records": len(after),
        "appended_records": NEW_TAGS,
        "unique_tag_codes": True,
        "unique_full_labels": True,
        "live_source_labels_verified": len(NEW_TAG_LABEL_SOURCES),
    }


def assert_public_hygiene() -> dict:
    checked = []
    markers = [
        "C:" + chr(92) + "Users" + chr(92),
        "C:/" + "Users/",
        "Flo" + "ris",
        "Documents" + chr(92) + "interlanguage",
    ]
    wrapped_user = re.compile(r"(?i)F\s*l\s*o\s*r\s*i\s*s")
    paths = [
        ROOT / "README.md",
        ROOT / "BUILD.md",
        ROOT / "decisions.jsonl",
        ROOT / "rejections.jsonl",
        *sorted((ROOT / "builds").glob("*.json")),
        *sorted((ROOT / "builds").glob("*.log")),
        *sorted((ROOT / "builds").glob("*.txt")),
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        if any(marker.lower() in lower for marker in markers) or wrapped_user.search(text):
            raise AssertionError(f"public artifact retains a private local-path marker: {path.relative_to(ROOT)}")
        checked.append(path.relative_to(ROOT).as_posix())
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    if caches:
        raise AssertionError(f"disposable Python caches remain in candidate: {caches}")
    return {"passed": True, "text_files": len(checked), "python_caches": 0}


def main() -> int:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    execution_timestamp = json.loads(
        (ROOT / "builds" / "build-execution.json").read_text(encoding="utf-8")
    )["completed_at_utc"]
    report = {
        "schema": "mathematics-commons-stacks-errata-validation/v1",
        "candidate_id": "stacks-errata-a04446e-r1",
        "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
        "generated_at_utc": execution_timestamp,
        "verifier_sha256": sha256(Path(__file__)),
        "passed": False,
        "checks": {},
    }
    try:
        for relative, expected in AUTHORITY_HASHES.items():
            actual = sha256(ROOT / relative)
            if actual != expected:
                raise AssertionError(f"authority hash mismatch: {relative}: {actual} != {expected}")
        report["checks"]["authority_hashes"] = {
            "passed": True,
            "files": len(AUTHORITY_HASHES),
        }

        stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
        ids = [unit["id"] for unit in stable["units"]]
        expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(1, 16) if number != 4]
        if stable["unit_count"] != 14 or ids != expected_ids:
            raise AssertionError("stable unit inventory is not the ordered complete 14-unit proved set")
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        if [row["unit_id"] for row in source_map] != expected_ids:
            raise AssertionError("source map is not the ordered complete 14-unit proved set")
        report["checks"]["unit_closure"] = {"passed": True, "expected": 14, "manifested": 14, "rejected": ["MC-STK-ERR-0004"]}

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if lease["lease_id"] != "stacks-lease-000004-errata":
            raise AssertionError("candidate lease ID mismatch")
        if lease["writer_task"] != "01a0256d-5693-77c1-96b2-cf37101e0c6c":
            raise AssertionError("candidate writer task mismatch")
        if lease["upstream_commit"] != report["authority_commit"]:
            raise AssertionError("candidate lease upstream mismatch")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        if inventory["unit_count"] != 14 or inventory["diagram_units"]:
            raise AssertionError("formula/diagram inventory closure mismatch")
        producer_hashes = json.loads((ROOT / "authority" / "producer-hashes.json").read_text(encoding="utf-8"))
        if len(producer_hashes["ledgers"]) != 3 or producer_hashes["rejected_after_canon_proof"] != ["MC-STK-ERR-0004"]:
            raise AssertionError("producer evidence-hash closure mismatch")
        report["checks"]["lease_and_inventory"] = {"passed": True, "units": 14, "diagrams": 0}

        for path in [
            ROOT / "decisions.jsonl",
            ROOT / "rejections.jsonl",
            ROOT / "authority" / "ERRATA_LEDGER.jsonl",
        ]:
            load_jsonl(path)
        proofs = (ROOT / "proofs.md").read_text(encoding="utf-8")
        for unit_id in expected_ids:
            if unit_id not in proofs:
                raise AssertionError(f"proof dossier omits {unit_id}")
        if "Rejected `MC-STK-ERR-0004`" not in proofs:
            raise AssertionError("proof dossier omits rejected MC-STK-ERR-0004")
        report["checks"]["jsonl_and_proof_parse"] = {"passed": True, "jsonl_files": 3, "proved_units": 14, "rejected_units": 1}
        report["checks"]["public_hygiene"] = assert_public_hygiene()

        payloads = {}
        for name in REPLACEMENTS:
            payloads[name] = assert_exact_payload(name)
        report["checks"]["exact_payloads"] = {"passed": True, "files": payloads}
        report["checks"]["permanent_tags"] = {"passed": True, **assert_tags()}
        tag_receipt = json.loads((ROOT / "builds" / "tag-allocator.json").read_text(encoding="utf-8"))
        if not tag_receipt["passed"] or tag_receipt["before"]["records"] != NEW_TAGS or tag_receipt["after"]["count"] != 0:
            raise AssertionError("tag allocator receipt does not prove exact closure")
        report["checks"]["tag_allocator_replay"] = {"passed": True, "before": 9, "after": 0}
        build_receipt_path = ROOT / "builds" / "build-receipt.json"
        build_receipt = json.loads(build_receipt_path.read_text(encoding="utf-8"))
        if not build_receipt["passed"]:
            raise AssertionError("bounded chapter build receipt failed")
        execution_path = ROOT / "builds" / "build-execution.json"
        if build_receipt["execution"]["sha256"] != sha256(execution_path):
            raise AssertionError("build receipt does not bind the final execution receipt")
        if [chapter["stem"] for chapter in build_receipt["chapters"]] != [
            "smoothing",
            "crystalline",
            "spaces-cohomology",
        ]:
            raise AssertionError("bounded chapter build set mismatch")
        for chapter in build_receipt["chapters"]:
            if not chapter["execution_binding_matches"]:
                raise AssertionError(f"build execution binding failed: {chapter['stem']}")
            expected_payload = sha256(ROOT / "payload" / f"{chapter['stem']}.tex")
            if chapter["candidate_source"]["sha256"] != expected_payload:
                raise AssertionError(f"build receipt source hash is stale: {chapter['stem']}")
        report["checks"]["chapter_builds"] = {
            "passed": True,
            "receipt_sha256": sha256(build_receipt_path),
            "chapters": 3,
        }
        visual_path = ROOT / "builds" / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if not visual["passed"] or len(visual["pdfs"]) != 3:
            raise AssertionError("visual PDF QA receipt is incomplete or failed")
        visual_units = []
        for pdf in visual["pdfs"]:
            path = ROOT / pdf["path"]
            if sha256(path) != pdf["sha256"] or path.stat().st_size != pdf["bytes"]:
                raise AssertionError(f"visual QA PDF binding is stale: {pdf['path']}")
            if pdf["unembedded_fonts"] or pdf["fonts_without_tounicode"]:
                raise AssertionError(f"visual QA font gate failed: {pdf['path']}")
            if pdf["malformed_link_rectangles"] or pdf["out_of_bounds_link_rectangles"]:
                raise AssertionError(f"visual QA link-geometry gate failed: {pdf['path']}")
            visual_units.extend(pdf["covered_units"])
        if sorted(visual_units) != sorted(unit for unit in expected_ids if unit != "MC-STK-ERR-0008"):
            raise AssertionError("visual QA does not cover every direct correction unit")
        report["checks"]["visual_pdf_qa"] = {
            "passed": True,
            "receipt_sha256": sha256(visual_path),
            "pdfs": 3,
            "direct_units": 13,
        }
        report["passed"] = True
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"

    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "report": str(REPORT)}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
