from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "builds" / "validation.json"
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_HASHES = {
    "authority/COPYING": "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85",
    "authority/upstream.lock.json": "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D",
    "authority/source/brauer.tex": "B2504820D769EBE4E9E33B8ADD78753FB30ACA6E8A7F75C8D54DDA885EDCD682",
    "authority/source/stacks-limits.tex": "F4F5EBF02BB5922A8DFF70EA507ED6F821F992C697D9C9A984B9513C39FEC57A",
    "authority/canon/ERRATA_LEDGER.jsonl": "A1713294427EC2520A313A54F674F324FB90CA4DA58E08F5D0481CFC10737100",
    "authority/canon/ERRATA_R2_PROOFS.md": "474EF7ED07DBC0F139A528AA7F0FBD2C9C6D37F2B91231C47287F83C94F4CDD4",
    "authority/canon/INTAKE_P02_CH11_20260821.json": "7DABA01CC441F6406EF8AB16F4205A4F95B422260C0B476606A31464C84B45A3",
    "authority/canon/INTAKE_P12_CH102_20260821.json": "5AF5BB6F92EA2228B46041BE71103B280349358E56DCA7C7EA577BF628059E32",
    "authority/producer/QA_ZH_CH11.json": "94CE6E9BB178A3CF26FCB08B1ECA2278D5F882138553A594A716C6CE9111A145",
    "authority/producer/CH102_ZH_QA.json": "FE0D6D2D5D5E3D64F592A035A8B8F61BE7B44F1F33C31BC800FDBE6FB327A121",
}
PAYLOAD_HASHES = {
    "brauer.tex": "7D14F300ED13295728D3BA0B08ABEB5449B93D4E64244FA91680BEA9DA785BBD",
    "stacks-limits.tex": "0FBB14083DB31197467F9A638216D3273BAE7520623E99B9ED884B043BF12003",
}
REPLACEMENTS = {
    "brauer.tex": [
        ("spitting field.", "splitting field."),
        (
            "To get a contradiction assume no element of $K$ is separable over $k$.",
            "To get a contradiction assume no element of $K$ outside $k$ is separable over $k$.",
        ),
    ],
    "stacks-limits.tex": [
        (
            "of affine schemes over $U$,\nthe functor",
            "of affine schemes over $S$,\nthe functor",
        ),
        (r"\phi : f(x) \to y_i|V", r"\phi : p(x) \to y_i|V"),
        ("fibre categories of $[U/T]$", "fibre categories of $[U/R]$"),
        (
            "We assume that $X_i$ is quasi-compact and quasi-separated",
            "We assume that $Y_i$ is quasi-compact and quasi-separated",
        ),
        ("two morpisms", "two morphisms"),
        ("a proper morphisms", "a proper morphism"),
        (
            "shows that this is the morphism is the same as",
            "shows that this morphism is the same as",
        ),
        (
            r"$T' \subset |X \times_Y Z'|$",
            r"$T' \subset |\mathcal{X} \times_Y Z'|$",
        ),
        (
            r"the map $|\mathcal{X} \times_Y Z| \to |Z|$ is closed, and",
            r"the map $|\mathcal{X} \times_{\mathcal{Y}} Z| \to |Z|$ is closed, and",
        ),
        (
            r"$\mathcal{X} \times_Y V \to V$ is universally closed,",
            r"$\mathcal{X} \times_{\mathcal{Y}} V \to V$ is universally closed,",
        ),
        (
            r"of $|X \times_Y Z|$ is the pullback",
            r"of $|\mathcal{X} \times_Y Z|$ is the pullback",
        ),
        (
            r"$|\mathbf{A}^n \times Y|$. Since the assumption",
            r"$|\mathbf{A}^n \times \mathcal{X}|$. Since the assumption",
        ),
        (
            r"of $T'$ in $|\mathbf{A}^n \times X|$ is closed",
            r"of $T'$ in $|\mathbf{A}^n \times Y|$ is closed",
        ),
    ],
}
STRUCTURE_PATTERNS = {
    "labels": re.compile(r"\\label\{[^{}]+\}"),
    "references": re.compile(r"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(
        r"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"
    ),
    "environments": re.compile(r"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(
        r"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(f"{path}:{line_number}: {exc}") from exc
    return rows


def exact_payload(name: str) -> dict:
    authority_path = ROOT / "authority" / "source" / name
    payload_path = ROOT / "payload" / name
    authority = authority_path.read_text(encoding="utf-8")
    payload = payload_path.read_text(encoding="utf-8")
    expected = authority
    mapped = []
    for old, new in REPLACEMENTS[name]:
        count = expected.count(old)
        if count != 1:
            raise AssertionError(
                f"{name}: old span occurs {count} times instead of once: {old!r}"
            )
        expected = expected.replace(old, new, 1)
        mapped.append({"old": old, "new": new, "count": 1})
    if payload != expected:
        raise AssertionError(f"{name}: payload changes extend beyond mapped spans")
    structure = {}
    for key, pattern in STRUCTURE_PATTERNS.items():
        before = pattern.findall(authority)
        after = pattern.findall(payload)
        if before != after:
            raise AssertionError(f"{name}: ordered {key} sequence changed")
        structure[key] = len(before)
    if authority.count("$$") != payload.count("$$"):
        raise AssertionError(f"{name}: display-math delimiter count changed")
    if authority.count(r"\xymatrix") != payload.count(r"\xymatrix"):
        raise AssertionError(f"{name}: xymatrix count changed")
    return {
        "authority_sha256": sha256(authority_path),
        "payload_sha256": sha256(payload_path),
        "authority_bytes": authority_path.stat().st_size,
        "payload_bytes": payload_path.stat().st_size,
        "mapped_replacements": mapped,
        "structure": structure,
        "display_delimiters": authority.count("$$"),
        "xymatrix_count": authority.count(r"\xymatrix"),
    }


def public_hygiene() -> dict:
    markers = (
        "C:" + chr(92) + "Users" + chr(92),
        "C:/" + "Users/",
        "Flo" + "ris",
        "Documents" + chr(92) + "interlanguage",
    )
    checked = 0
    for pattern in ("*.md", "*.json", "*.jsonl", "*.log", "*.txt", "*.py"):
        for path in ROOT.rglob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(marker.lower() in text.lower() for marker in markers):
                raise AssertionError(
                    f"public artifact retains private local marker: {path.relative_to(ROOT)}"
                )
            checked += 1
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    if caches:
        raise AssertionError(f"Python caches remain in candidate: {caches}")
    return {"passed": True, "text_files": checked, "python_caches": 0}


def main() -> int:
    completed = json.loads(
        (ROOT / "builds" / "build-execution.json").read_text(encoding="utf-8")
    )["completed_at_utc"]
    report = {
        "schema": "mathematics-commons-stacks-errata-validation/v1",
        "candidate_id": "stacks-errata-a04446e-r2",
        "authority_commit": AUTHORITY_COMMIT,
        "generated_at_utc": completed,
        "verifier_sha256": sha256(Path(__file__)),
        "passed": False,
        "checks": {},
    }
    try:
        for relative, expected in AUTHORITY_HASHES.items():
            actual = sha256(ROOT / relative)
            if actual != expected:
                raise AssertionError(
                    f"authority hash mismatch: {relative}: {actual} != {expected}"
                )
        report["checks"]["authority_hashes"] = {
            "passed": True,
            "files": len(AUTHORITY_HASHES),
        }

        stable = json.loads(
            (ROOT / "stable-units.json").read_text(encoding="utf-8")
        )
        expected_ids = [
            f"MC-STK-ERR-{number:04d}" for number in range(16, 29)
        ]
        ids = [unit["id"] for unit in stable["units"]]
        if stable["unit_count"] != 13 or ids != expected_ids:
            raise AssertionError("stable unit inventory is not the exact R2 set")
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        if [row["unit_id"] for row in source_map] != expected_ids:
            raise AssertionError("source map is not the ordered exact R2 set")
        report["checks"]["unit_closure"] = {
            "passed": True,
            "expected": 13,
            "manifested": 13,
        }

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if (
            lease["lease_id"] != "stacks-lease-000005-errata-r2"
            or lease["writer_task"] != "01a0256d-5693-77c1-96b2-cf37101e0c6c"
            or lease["upstream_commit"] != AUTHORITY_COMMIT
        ):
            raise AssertionError("candidate lease identity mismatch")
        inventory = json.loads(
            (ROOT / "formula-diagram-inventory.json").read_text(
                encoding="utf-8"
            )
        )
        if (
            inventory["unit_count"] != 13
            or inventory["unmapped_formula_or_diagram_changes"] != 0
            or inventory["diagram_units"] != ["MC-STK-ERR-0028"]
        ):
            raise AssertionError("formula/diagram inventory closure mismatch")
        report["checks"]["lease_and_inventory"] = {
            "passed": True,
            "units": 13,
            "diagram_units": 1,
        }

        for path in (
            ROOT / "decisions.jsonl",
            ROOT / "rejections.jsonl",
            ROOT / "authority" / "canon" / "ERRATA_LEDGER.jsonl",
        ):
            load_jsonl(path)
        proofs = (
            ROOT / "authority" / "canon" / "ERRATA_R2_PROOFS.md"
        ).read_text(encoding="utf-8")
        for unit_id in expected_ids:
            if unit_id not in proofs:
                raise AssertionError(f"proof dossier omits {unit_id}")
        report["checks"]["jsonl_and_proof_parse"] = {
            "passed": True,
            "jsonl_files": 3,
            "proved_units": 13,
        }

        payloads = {}
        for name in REPLACEMENTS:
            payloads[name] = exact_payload(name)
            if payloads[name]["payload_sha256"] != PAYLOAD_HASHES[name]:
                raise AssertionError(f"payload hash mismatch after replay: {name}")
        report["checks"]["exact_payloads"] = {
            "passed": True,
            "files": payloads,
        }

        build_receipt_path = ROOT / "builds" / "build-receipt.json"
        build_receipt = json.loads(build_receipt_path.read_text(encoding="utf-8"))
        execution_path = ROOT / "builds" / "build-execution.json"
        if (
            not build_receipt["passed"]
            or build_receipt["execution"]["sha256"] != sha256(execution_path)
            or [chapter["stem"] for chapter in build_receipt["chapters"]]
            != ["brauer", "stacks-limits"]
        ):
            raise AssertionError("bounded chapter build receipt failed or stale")
        for chapter in build_receipt["chapters"]:
            if (
                not chapter["passed"]
                or not chapter["execution_binding_matches"]
                or not chapter["undefined_target_multisets_match_authority"]
            ):
                raise AssertionError(
                    f"chapter build binding failed: {chapter['stem']}"
                )
        report["checks"]["chapter_builds"] = {
            "passed": True,
            "chapters": 2,
            "receipt_sha256": sha256(build_receipt_path),
        }

        visual_path = ROOT / "builds" / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if not visual["passed"] or len(visual["pdfs"]) != 2:
            raise AssertionError("visual PDF QA is incomplete")
        visual_units = []
        for pdf in visual["pdfs"]:
            path = ROOT / pdf["path"]
            if (
                sha256(path) != pdf["sha256"]
                or path.stat().st_size != pdf["bytes"]
                or pdf["unembedded_fonts"]
                or pdf["fonts_without_tounicode"]
                or pdf["malformed_link_rectangles"]
                or pdf["out_of_bounds_link_rectangles"]
            ):
                raise AssertionError(f"visual PDF binding or gate failed: {path}")
            visual_units.extend(pdf["covered_units"])
        if sorted(visual_units) != expected_ids:
            raise AssertionError("visual QA does not cover every R2 unit")
        report["checks"]["visual_pdf_qa"] = {
            "passed": True,
            "pdfs": 2,
            "direct_units": 13,
            "receipt_sha256": sha256(visual_path),
        }
        report["checks"]["public_hygiene"] = public_hygiene()
        report["passed"] = True
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"passed": report["passed"], "report": str(REPORT)}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
