from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "source-validation.json"
GENERATED_AT = "2026-08-27T21:34:00Z"
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1046, 1177)]
EXPECTED_PRODUCER_IDS = [f"P11-E{number:04d}" for number in range(200, 340)]
REJECTED_IDS = ["P11-E0202", "P11-E0215", "P11-E0217"]
STRUCTURE_PATTERNS = {
    "labels": re.compile(rb"\\label\{[^{}]+\}"),
    "references": re.compile(rb"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(rb"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
    "environments": re.compile(rb"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(rb"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
}
REFINEMENTS = {
    "P11-E0208": [("algebraic spaces, see (insert future reference here).", "algebraic spaces.")],
    "P11-E0210": [
        ("\\mathcal{X}_Y \\times_{\\mathcal{Y}_Y} \\mathcal{Z}_Y", "\\mathcal{X}_Y \\times_{\\mathcal{X}_X} \\mathcal{X}_{X'}"),
        ("\\mathcal{X}_X \\times_{\\mathcal{Y}_X} \\mathcal{Z}_X", "\\mathcal{Y}_Y \\times_{\\mathcal{Y}_X} \\mathcal{Y}_{X'}"),
        ("\\mathcal{X}_{X'} \\times_{\\mathcal{Y}_{X'}} \\mathcal{Z}_{X'}", "\\mathcal{Z}_Y \\times_{\\mathcal{Z}_X} \\mathcal{Z}_{X'}"),
    ],
    "P11-E0211": [
        ("$(x_Y, x_{Y'}, \\alpha)$", "$(x_Y, x_{X'}, \\alpha)$"),
        ("$(z_Y, z_{Y'}, \\beta)$", "$(z_Y, z_{X'}, \\beta)$"),
    ],
    "P11-E0240": [("(insert future reference here; see also discussion in", "(see also discussion in")],
    "P11-E0265": [("We will develop this theory later (insert future reference here).", "We will develop this theory later.")],
    "P11-E0317": [("$\\xi|_U = \\tilde \\xi_\\lambda|_U$", "$\\xi|_{\\tilde V} = \\tilde \\xi_\\lambda|_{\\tilde V}$")],
    "P11-E0320": [("$\\tilde g' :", "$\\tilde g :")],
    "P11-E0329": [("$\\Coker(\\alpha)$", "$\\Coker(A \\to C)$")],
    "P11-E0333": [("\\times_{\\hat x, W}", "\\times_{g, W}")],
    "P11-E0334": [("Smoothness of $V \\to W$", "Smoothness of $g : V_{/Z} \\to W$")],
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.name}:{line_number}: {exc}") from exc
    return rows


def operation_identity(row: dict) -> tuple:
    keys = (
        "operation_id",
        "producer_id",
        "source_start_line",
        "source_end_line",
        "start_byte",
        "end_byte_exclusive",
        "occurrence_count_in_frozen_authority",
        "old_text",
        "replacement_text",
        "old_sha256",
        "replacement_sha256",
    )
    return tuple(row[key] for key in keys)


def verify_refinements(mapped_operations: list[dict]) -> dict:
    by_producer: dict[str, set[tuple[str, str]]] = {}
    for operation in mapped_operations:
        by_producer.setdefault(operation["producer_id"], set()).add(
            (operation["old_text"], operation["replacement_text"])
        )
    for producer_id, expected_pairs in REFINEMENTS.items():
        missing = set(expected_pairs) - by_producer.get(producer_id, set())
        if missing:
            raise AssertionError(f"{producer_id}: required refinement missing: {sorted(missing)!r}")
    return {"passed": True, "producer_ids": sorted(REFINEMENTS), "required_operations": sum(map(len, REFINEMENTS.values()))}


def verify_payload(config: dict, source_map: list[dict]) -> dict:
    authority = (ROOT / "authority/source/artin.tex").read_bytes()
    payload = (ROOT / "payload/artin.tex").read_bytes()
    operations: list[tuple[int, int, bytes, bytes, str]] = []
    operation_ids: list[str] = []
    for unit in source_map:
        if (
            unit["source"] != "artin.tex"
            or unit["authority"] != "authority/source/artin.tex"
            or unit["payload"] != "payload/artin.tex"
            or unit["authority_sha256"] != sha_bytes(authority)
        ):
            raise AssertionError("R25 source map contains an unexpected source binding")
        for operation in unit["operations"]:
            start = operation["start_byte"]
            end = operation["end_byte_exclusive"]
            old = operation["old_text"].encode("utf-8")
            replacement = operation["replacement_text"].encode("utf-8")
            if authority[start:end] != old:
                raise AssertionError(f"{operation['operation_id']}: authority interval mismatch")
            actual_start_line = authority[:start].count(b"\n") + 1
            actual_end_line = authority[: max(start, end - 1)].count(b"\n") + 1
            if (actual_start_line, actual_end_line) != (
                operation["source_start_line"],
                operation["source_end_line"],
            ):
                raise AssertionError(f"{operation['operation_id']}: source-line metadata mismatch")
            if authority.count(old) != operation["occurrence_count_in_frozen_authority"]:
                raise AssertionError(f"{operation['operation_id']}: authority occurrence-count mismatch")
            if sha_bytes(old) != operation["old_sha256"] or sha_bytes(replacement) != operation["replacement_sha256"]:
                raise AssertionError(f"{operation['operation_id']}: span hash mismatch")
            operations.append((start, end, old, replacement, operation["operation_id"]))
            operation_ids.append(operation["operation_id"])

    if len(operation_ids) != len(set(operation_ids)):
        raise AssertionError("duplicate operation ID")
    ascending = sorted(operations)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[4]} / {right[4]}")
    replay = authority
    for start, end, old, replacement, operation_id in sorted(operations, reverse=True):
        if replay[start:end] != old:
            raise AssertionError(f"{operation_id}: descending replay interval changed")
        replay = replay[:start] + replacement + replay[end:]
    if replay != payload:
        raise AssertionError("payload contains changes outside the 154 mapped operations")

    stem = config["stems"]["artin"]
    structure: dict[str, dict[str, int]] = {}
    for name, pattern in STRUCTURE_PATTERNS.items():
        before = pattern.findall(authority)
        after = pattern.findall(payload)
        if before != after:
            raise AssertionError(f"ordered {name} changed")
        structure[name] = {"authority": len(before), "payload": len(after)}
    display_delta = payload.count(b"$$") - authority.count(b"$$")
    if display_delta != stem["display_delimiter_delta"]:
        raise AssertionError("display-delimiter delta mismatch")
    if payload.count(rb"\xymatrix") != authority.count(rb"\xymatrix"):
        raise AssertionError("xymatrix count changed")
    observed = {
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
        "operation_count": len(operations),
        "ordered_structure": structure,
        "display_delimiter_delta": display_delta,
        "xymatrix_count": authority.count(rb"\xymatrix"),
    }
    expected_fields = ("authority_bytes", "authority_sha256", "payload_bytes", "payload_sha256")
    if any(observed[field] != stem[field] for field in expected_fields):
        raise AssertionError("configured source identity mismatch")
    return observed


def public_hygiene() -> dict:
    private_root = re.compile(re.escape("C:") + r"(?:\\+|/+)" + "Us" + "ers" + r"(?:\\+|/+)", re.I)
    checked = 0
    for pattern in ("*.md", "*.json", "*.jsonl", "*.csv", "*.txt", "*.py"):
        for path in ROOT.rglob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            if private_root.search(text):
                raise AssertionError(f"private local marker remains: {path.relative_to(ROOT)}")
            if path.suffix.lower() == ".json":
                json.loads(text)
            elif path.suffix.lower() == ".jsonl":
                for line in text.splitlines():
                    if line.strip():
                        json.loads(line)
            checked += 1
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    if caches:
        raise AssertionError(f"Python caches remain: {caches}")
    return {"passed": True, "text_files": checked, "python_caches": 0}


def main() -> int:
    config = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
    report = {
        "schema": "mathematics-commons-stacks-errata-source-validation/v1",
        "candidate_id": config["candidate_id"],
        "authority_commit": config["authority_commit"],
        "generated_at_utc": GENERATED_AT,
        "verifier_sha256": file_sha(Path(__file__)),
        "scope": "source_only_no_build_render_admission_registry_git_or_publication",
        "passed": False,
        "checks": {},
    }
    try:
        for evidence in config["authority_evidence"]:
            path = ROOT / evidence["path"]
            if not path.is_file() or path.stat().st_size != evidence["bytes"] or file_sha(path) != evidence["sha256"]:
                raise AssertionError(f"authority evidence mismatch: {evidence['path']}")
        report["checks"]["authority_evidence"] = {"passed": True, "files": len(config["authority_evidence"])}

        spec_input = ROOT / "R25_ARTIN_ADJUDICATION_SPEC.input.json"
        spec_generated = ROOT / "R25_ARTIN_ADJUDICATION_SPEC.json"
        spec = json.loads(spec_generated.read_text(encoding="utf-8"))
        intake = json.loads((ROOT / "INTAKE_VALIDATION.json").read_text(encoding="utf-8"))
        if (
            spec_input.read_bytes() != spec_generated.read_bytes()
            or file_sha(spec_input) != intake["adjudication_spec_sha256"]
            or intake["status"] != "PASS"
            or spec["semantic_unit_count"] != 131
            or spec["operation_count"] != 154
            or spec["producer_row_count"] != 140
            or spec["accepted_producer_row_count"] != 137
            or spec["rejected_producer_row_count"] != 3
            or (ROOT / "P11_ARTIN_ERRATA_R25.input.jsonl").read_bytes()
            != (ROOT / "authority/canon/P11_ARTIN_ERRATA_R25.jsonl").read_bytes()
        ):
            raise AssertionError("sealed adjudication/intake identity mismatch")
        report["checks"]["sealed_intake"] = {
            "passed": True,
            "spec_sha256": file_sha(spec_generated),
            "units": 131,
            "operations": 154,
            "producer_rows": 140,
        }

        expected_ids = config["expected_unit_ids"]
        if expected_ids != EXPECTED_IDS:
            raise AssertionError("configured stable IDs are not contiguous 1046..1176")
        stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        producer_rows = load_jsonl(ROOT / "authority/canon/P11_ARTIN_ERRATA_R25.jsonl")
        stable_ids = [row["id"] for row in stable["units"]]
        map_ids = [row["unit_id"] for row in source_map]
        primary_producers = [row["producer_id"] for row in source_map]
        all_producers = [producer for row in source_map for producer in row["producer_ids"]]
        stable_all_producers = [producer for row in stable["units"] for producer in row["producer_ids"]]
        expected_accepted = set(EXPECTED_PRODUCER_IDS) - set(REJECTED_IDS)
        if (
            stable["unit_count"] != 131
            or stable_ids != expected_ids
            or map_ids != expected_ids
            or primary_producers != config["expected_producer_ids"]
            or all_producers != config["expected_all_producer_ids"]
            or stable_all_producers != all_producers
            or len(all_producers) != 137
            or len(set(all_producers)) != 137
            or set(all_producers) != expected_accepted
            or [row["id"] for row in producer_rows] != EXPECTED_PRODUCER_IDS
            or any(row.get("source_path") != "artin.tex" for row in producer_rows)
        ):
            raise AssertionError("stable-unit/source-map/producer closure mismatch")
        report["checks"]["unit_closure"] = {
            "passed": True,
            "units": len(stable_ids),
            "accepted_producer_ids": len(all_producers),
            "rejected_producer_ids": len(REJECTED_IDS),
            "first_id": stable_ids[0],
            "last_id": stable_ids[-1],
        }

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if (
            lease["lease_id"] != config["lease_id"]
            or lease["writer_task"] != config["writer_task"]
            or lease["upstream_commit"] != config["authority_commit"]
        ):
            raise AssertionError("candidate lease mismatch")
        decisions = load_jsonl(ROOT / "decisions.jsonl")
        rejections = load_jsonl(ROOT / "rejections.jsonl")
        inventory = json.loads((ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8"))
        classified = inventory["formula_units"] + inventory["diagram_units"] + inventory["prose_only_units"]
        closure = config["proof_closure"]
        if (
            len(decisions) != 6
            or [row["producer_id"] for row in rejections] != REJECTED_IDS
            or sorted(classified) != expected_ids
            or len(classified) != len(set(classified))
            or closure != {
                "accepted": 131,
                "accepted_producer_rows": 137,
                "intentionally_absent": 0,
                "operations": 154,
                "packet_duplicates": 0,
                "prior_aliases": 0,
                "producer_rows": 140,
                "rejected": 3,
                "unresolved": 0,
            }
        ):
            raise AssertionError("decision/rejection/inventory closure mismatch")
        report["checks"]["lease_ledgers_inventory"] = {
            "passed": True,
            "decisions": len(decisions),
            "rejections": len(rejections),
            "formula_units": len(inventory["formula_units"]),
            "diagram_units": len(inventory["diagram_units"]),
            "prose_only_units": len(inventory["prose_only_units"]),
        }

        operation_spec = json.loads((ROOT / "operation-spec.json").read_text(encoding="utf-8"))
        mapped_operations = [operation for row in source_map for operation in row["operations"]]
        stable_operation_ids = [operation_id for row in stable["units"] for operation_id in row["operation_ids"]]
        if (
            operation_spec["apply_order"] != "descending_start_byte"
            or operation_spec["operation_count"] != 154
            or operation_spec["authority_sha256"] != config["stems"]["artin"]["authority_sha256"]
            or [operation_identity(row) for row in operation_spec["operations"]]
            != [operation_identity(row) for row in mapped_operations]
            or stable_operation_ids != [row["operation_id"] for row in mapped_operations]
        ):
            raise AssertionError("operation-spec/source-map/stable-unit mismatch")
        report["checks"]["required_refinements"] = verify_refinements(mapped_operations)
        payload = verify_payload(config, source_map)
        if payload["operation_count"] != 154:
            raise AssertionError("exact payload operation-count mismatch")
        report["checks"]["exact_payload"] = {"passed": True, "artin": payload}
        report["checks"]["public_hygiene"] = public_hygiene()
        report["passed"] = True
    except Exception as exc:
        report["failure"] = f"{type(exc).__name__}: {exc}"

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({"passed": report["passed"], "report": REPORT.name}, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
