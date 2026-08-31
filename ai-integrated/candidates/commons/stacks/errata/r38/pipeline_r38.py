from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
WORKSPACE = REPO.parent
UPSTREAM_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
UPSTREAM_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_SHA = "0106554339E8966FE04411B2AE9F9CD856B165849FEEF0C7BC37634819064708"
PAYLOAD_SHA = "B4D8BF24D64BF7D5A50E4BC0791D02DDC19849F34A24FB4857CED6CB143DD196"
PAYLOAD_BYTES = 1492132
EVIDENCE_SHA = "B21321A9AEF236773E290B7AA390332843BAE42284911B7928AEE0FD57EC2FE7"
INVARIANTS_SHA = "3C4945C9E73223872308289D6E5919E4F8728A53ADCD66F67F6312A96D2289DD"
CANDIDATE_ID = "stacks-errata-a04446e-r38"
LEASE_ID = "stacks-lease-000042-errata-r38"
WRITER_TASK = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
GENERATED_AT = "2026-08-31T02:15:00Z"
SOURCE_DATE_EPOCH = "1788142500"

AUTHORITY_EXTERNAL = WORKSPACE / (
    "03_projects/language_management/cjk/03_working_translations/stacks_cjk_20260821/"
    "upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/more-algebra.tex"
)
COPYING_EXTERNAL = AUTHORITY_EXTERNAL.parent / "COPYING"
EVIDENCE_ROOT = WORKSPACE / (
    "03_projects/language_management/romance/03_working_translations/"
    "stacks_fr_20260821/p02/evidence"
)
PRODUCER_EMENDATIONS = EVIDENCE_ROOT / "MORE_ALGEBRA_L_SOURCE_EMENDATIONS.json"
PRODUCER_INVARIANTS = EVIDENCE_ROOT / "MORE_ALGEBRA_L_INVARIANTS.json"
PRODUCER_LIVE_MANIFEST = EVIDENCE_ROOT / "MORE_ALGEBRA_LIVE_PART_MANIFEST.json"
REGISTRAR_REVIEW = WORKSPACE / (
    "03_projects/language_management/romance/00_lane_control/"
    "MORE_ALGEBRA_L_R38_INDEPENDENT_REVIEW_20260831.json"
)

GROUPS = [
    ("MC-STK-ERR-1336", ["MORE-ALGEBRA-L-001"], "spelling_typo"),
    ("MC-STK-ERR-1337", ["MORE-ALGEBRA-L-002"], "missing_localization_preposition"),
    ("MC-STK-ERR-1338", ["MORE-ALGEBRA-L-003"], "extraneous_preposition"),
    ("MC-STK-ERR-1339", ["MORE-ALGEBRA-L-004", "MORE-ALGEBRA-L-006"], "wrong_local_factor_index"),
    ("MC-STK-ERR-1340", ["MORE-ALGEBRA-L-005"], "undefined_principal_kernel_generator"),
    ("MC-STK-ERR-1341", ["MORE-ALGEBRA-L-007"], "wrong_indefinite_article"),
    ("MC-STK-ERR-1342", ["MORE-ALGEBRA-L-008"], "missing_preposition"),
    ("MC-STK-ERR-1343", ["MORE-ALGEBRA-L-009", "MORE-ALGEBRA-L-017"], "repeated_missing_localization_subscript"),
    ("MC-STK-ERR-1344", ["MORE-ALGEBRA-L-010", "MORE-ALGEBRA-L-018"], "repeated_wrong_associated_prime_terminal_index"),
    ("MC-STK-ERR-1345", ["MORE-ALGEBRA-L-011"], "malformed_summation_range"),
    ("MC-STK-ERR-1346", ["MORE-ALGEBRA-L-012", "MORE-ALGEBRA-L-013"], "wrong_terminal_parameter_index"),
    ("MC-STK-ERR-1347", ["MORE-ALGEBRA-L-014", "MORE-ALGEBRA-L-015", "MORE-ALGEBRA-L-030", "MORE-ALGEBRA-L-031"], "incomplete_minimal_prime_product_range"),
    ("MC-STK-ERR-1348", ["MORE-ALGEBRA-L-016"], "undefined_parameter_ideal_symbol"),
    ("MC-STK-ERR-1349", ["MORE-ALGEBRA-L-019"], "wrong_initial_parameter_index"),
    ("MC-STK-ERR-1350", ["MORE-ALGEBRA-L-020"], "wrong_quotient_dimension"),
    ("MC-STK-ERR-1351", ["MORE-ALGEBRA-L-021", "MORE-ALGEBRA-L-022"], "repeated_missing_fraktur_prime_notation"),
    ("MC-STK-ERR-1352", ["MORE-ALGEBRA-L-023"], "extraneous_indefinite_article"),
    ("MC-STK-ERR-1353", ["MORE-ALGEBRA-L-024"], "number_agreement"),
    ("MC-STK-ERR-1354", ["MORE-ALGEBRA-L-025"], "missing_relative_clause_verb"),
    ("MC-STK-ERR-1355", ["MORE-ALGEBRA-L-026"], "missing_list_separator"),
    ("MC-STK-ERR-1356", ["MORE-ALGEBRA-L-027"], "missing_preposition"),
    ("MC-STK-ERR-1357", ["MORE-ALGEBRA-L-028"], "wrong_ambient_module"),
    ("MC-STK-ERR-1358", ["MORE-ALGEBRA-L-029"], "spelling_typo"),
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def dump(path: Path, value: object, *, sort_keys: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=sort_keys) + "\n",
        encoding="utf-8",
        newline="",
    )


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8", newline="")


def artifact(path: Path, display: str | None = None) -> dict:
    return {
        "path": display or path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    }


def manifest_artifact(path: Path, display: str | None = None) -> dict:
    return {"path": display or path.relative_to(ROOT).as_posix(), "sha256": sha(path)}


def copy_exact(source: Path, target: Path, expected_sha: str | None = None) -> None:
    data = source.read_bytes()
    if expected_sha and sha_bytes(data) != expected_sha:
        raise AssertionError(f"input hash mismatch: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def sanitized_json_copy(source: Path, target: Path, expected_sha: str) -> None:
    raw = source.read_bytes()
    if sha_bytes(raw) != expected_sha:
        raise AssertionError(f"sanitized input hash mismatch: {source}")
    value = json.loads(raw.decode("utf-8"))

    def scrub(item):
        if isinstance(item, dict):
            return {key: scrub(val) for key, val in item.items()}
        if isinstance(item, list):
            return [scrub(val) for val in item]
        if isinstance(item, str):
            prefix = str(WORKSPACE)
            if item.lower().startswith(prefix.lower()):
                relative = item[len(prefix):].lstrip("\\/").replace("\\", "/")
                return f"<WORKSPACE>/{relative}"
        return item

    value = scrub(value)
    if not isinstance(value, dict):
        raise AssertionError("sanitized producer evidence must be an object")
    value["original_private_transport_identity"] = {
        "bytes": len(raw),
        "sha256": expected_sha,
        "private_paths_published": False,
    }
    dump(target, value)


def load_packet() -> tuple[dict, dict[str, dict]]:
    packet = json.loads(PRODUCER_EMENDATIONS.read_text(encoding="utf-8"))
    if sha(PRODUCER_EMENDATIONS) != EVIDENCE_SHA or len(packet["emendations"]) != 31:
        raise AssertionError("current 31-operation producer packet identity mismatch")
    rows = {row["id"]: row for row in packet["emendations"]}
    expected = {f"MORE-ALGEBRA-L-{i:03d}" for i in range(1, 32)}
    if set(rows) != expected:
        raise AssertionError("producer evidence ID closure mismatch")
    return packet, rows


def locate_operations(authority: bytes, evidence: dict[str, dict]) -> list[dict]:
    text = authority.decode("utf-8")
    lines = text.splitlines(keepends=True)
    if len(lines) != 39222 or b"\r" in authority:
        raise AssertionError("authority line ending or line count mismatch")
    starts: list[int] = []
    cursor = 0
    for line in lines:
        starts.append(cursor)
        cursor += len(line.encode("utf-8"))
    producer_to_stable = {}
    stable_to_class = {}
    for stable, producers, cls in GROUPS:
        stable_to_class[stable] = cls
        for producer in producers:
            producer_to_stable[producer] = stable
    counters: Counter[str] = Counter()
    operations = []
    for index in range(1, 32):
        producer = f"MORE-ALGEBRA-L-{index:03d}"
        row = evidence[producer]
        line_number = int(row["line"])
        line = lines[line_number - 1]
        old = row["old"]
        new = row["new"]
        if line.count(old) != 1:
            raise AssertionError(f"declared-line preimage is not unique: {producer}")
        local_char = line.index(old)
        local_byte = len(line[:local_char].encode("utf-8"))
        start = starts[line_number - 1] + local_byte
        old_bytes = old.encode("utf-8")
        new_bytes = new.encode("utf-8")
        if authority[start:start + len(old_bytes)] != old_bytes:
            raise AssertionError(f"byte preimage mismatch: {producer}")
        stable = producer_to_stable[producer]
        counters[stable] += 1
        operations.append({
            "operation_id": f"{stable}-OP{counters[stable]}",
            "stable_id": stable,
            "producer_id": producer,
            "origin": "registrar_additive_alias" if producer in {"MORE-ALGEBRA-L-030", "MORE-ALGEBRA-L-031"} else "producer_packet",
            "class": stable_to_class[stable],
            "source": "more-algebra.tex",
            "source_start_line": line_number,
            "source_end_line": line_number,
            "declared_line_occurrences": 1,
            "file_occurrences": text.count(old),
            "start_byte": start,
            "end_byte_exclusive": start + len(old_bytes),
            "old_text": old,
            "replacement_text": new,
            "old_bytes": len(old_bytes),
            "old_sha256": sha_bytes(old_bytes),
            "replacement_bytes": len(new_bytes),
            "replacement_sha256": sha_bytes(new_bytes),
        })
    intervals = sorted((row["start_byte"], row["end_byte_exclusive"], row["operation_id"]) for row in operations)
    for left, right in zip(intervals, intervals[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")
    return operations


def apply_operations(authority: bytes, operations: list[dict]) -> bytes:
    payload = authority
    for operation in sorted(operations, key=lambda row: row["start_byte"], reverse=True):
        start = operation["start_byte"]
        end = operation["end_byte_exclusive"]
        old = operation["old_text"].encode("utf-8")
        new = operation["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"descending replay preimage mismatch: {operation['operation_id']}")
        payload = payload[:start] + new + payload[end:]
    if len(payload) != PAYLOAD_BYTES or sha_bytes(payload) != PAYLOAD_SHA:
        raise AssertionError("effective payload identity mismatch")
    return payload


def prior_dedup(operations: list[dict]) -> dict:
    maps = sorted((REPO / "candidates/commons/stacks/errata").glob("r*/source-map.jsonl"))
    prior_rows: list[dict] = []
    checked_maps = 0
    for path in maps:
        if path.parent == ROOT:
            continue
        checked_maps += 1
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                prior_rows.append(json.loads(line))
    prior_ops = []
    legacy_change_count = 0
    for row in prior_rows:
        for op in row.get("operations", []):
            prior_ops.append((row, op))
        if "operations" not in row:
            legacy_change_count += int(row.get("change_count", 0))
    same_locus = []
    same_old_new = []
    same_producer = []
    incoming_producers = {op["producer_id"] for op in operations}
    for incoming in operations:
        for row, op in prior_ops:
            if row.get("source") == "more-algebra.tex" and int(op.get("source_start_line", -1)) == incoming["source_start_line"]:
                same_locus.append([incoming["operation_id"], row.get("unit_id"), op.get("operation_id")])
            if op.get("old_text") == incoming["old_text"] and op.get("replacement_text") == incoming["replacement_text"] and row.get("source") == "more-algebra.tex":
                same_old_new.append([incoming["operation_id"], row.get("unit_id"), op.get("operation_id")])
        for producer in row.get("producer_ids", []):
            if producer in incoming_producers:
                same_producer.append([producer, row.get("unit_id")])
    overlays = REPO / "registry/overlays.json"
    registry = json.loads(overlays.read_text(encoding="utf-8"))
    entries = registry.get("registered_entries", [])
    stable_ids = [stable for entry in entries for stable in entry.get("stable_ids", [])]
    return {
        "registry": artifact(overlays, "registry/overlays.json"),
        "registered_entries": len(entries),
        "source_map_files_checked": checked_maps,
        "registered_units_checked": len(prior_rows),
        "registered_operations_checked": len(prior_ops),
        "legacy_change_spans_checked": legacy_change_count,
        "total_explicit_operations_and_legacy_change_spans_checked": len(prior_ops) + legacy_change_count,
        "stable_ids_checked": len(stable_ids),
        "maximum_numeric_stable_id": "MC-STK-ERR-1335",
        "same_locus_matches": same_locus,
        "same_old_new_matches": same_old_new,
        "same_producer_id_matches": same_producer,
        "novel": not same_locus and not same_old_new and not same_producer,
    }


def structure(text: str) -> dict:
    patterns = {
        "labels": r"\\label\{[^{}]+\}",
        "refs": r"\\(?:ref|eqref|pageref)\{[^{}]+\}",
        "cites": r"\\cite(?:\[[^\]]*\])?\{[^{}]+\}",
        "begins": r"\\begin\{[^{}]+\}",
        "ends": r"\\end\{[^{}]+\}",
        "items": r"\\item\b",
        "xymatrix": r"\\xymatrix\b",
    }
    result = {name: re.findall(pattern, text) for name, pattern in patterns.items()}
    result["open_braces"] = text.count("{")
    result["close_braces"] = text.count("}")
    result["dollar_delimiters"] = len(re.findall(r"(?<!\\)\$", text))
    return result


def write_static_texts() -> None:
    (ROOT / ".gitattributes").write_text("* -text\n", encoding="utf-8", newline="")
    lease = {
        "schema": "mathematics-commons-stacks-candidate-lease/v1",
        "lease_event": "lease-event-000080",
        "lease_id": LEASE_ID,
        "namespace": "commons/stacks/errata/r38",
        "candidate_path": "candidates/commons/stacks/errata/r38",
        "writer_task": WRITER_TASK,
        "status": "active",
        "issued_at_utc": "2026-08-31T02:03:12Z",
        "authority_commit": UPSTREAM_COMMIT,
        "authority_tree": UPSTREAM_TREE,
        "write_boundary": "candidate subtree only; no registry, generated source, producer target, Git, or publication mutation",
    }
    dump(ROOT / "LEASE.json", lease)
    (ROOT / "README.md").write_text(
        "# Stacks errata candidate R38\n\n"
        "R38 is a source-bound English correction candidate for `more-algebra.tex` at the frozen Stacks commit "
        f"`{UPSTREAM_COMMIT}`. It admits 23 semantic units (`MC-STK-ERR-1336..1358`) represented by 31 exact operations. "
        "The 29 original producer allegations are preserved; L-030/L-031 are additive aliases inside MC-STK-ERR-1347. "
        "The original one-operation L-015 proposal is preserved as mathematically correct but incomplete adverse history.\n\n"
        "This candidate does not mutate the official authority, the French producer target, the registry, generated source, Git, or a public release. "
        "Its payload is deterministically reconstructed from the frozen authority and the exact operation specification.\n",
        encoding="utf-8", newline="",
    )
    (ROOT / "BUILD.md").write_text(
        "# R38 build and replay\n\n"
        "Run `python pipeline_r38.py materialize` to reproduce the source-level closure. Then use the bound R23-derived helpers in two distinct fresh roots: "
        "`python replay-build.py --upstream-root FROZEN_TREE --work-root NEW_ROOT --private-evidence-root PRIVATE_ROOT`; repeat with a second fresh root, "
        "run `deterministic-replay.py`, `build-receipt.py`, derive SyncTeX page mappings, render every page, inspect every contact sheet and correction-sensitive page, "
        "run `visual-qa.py`, then finalize the independent replay and schema-conformant manifest. Candidate and authority use pdflatex, bibtex, pdflatex, pdflatex.\n",
        encoding="utf-8", newline="",
    )


def copy_build_helpers() -> None:
    source_root = REPO / "candidates/commons/stacks/errata/r23"
    names = [
        "replay-build.py", "deterministic-replay.py", "build-receipt.py",
        "derive-visual-pages.py", "render-qa.py", "visual-qa.py",
    ]
    for name in names:
        text = (source_root / name).read_text(encoding="utf-8")
        text = text.replace(".r23-build-work.json", ".r38-build-work.json")
        text = text.replace("R23 source loci", "R38 source loci")
        (ROOT / name).write_text(text, encoding="utf-8", newline="")


def materialize() -> dict:
    write_static_texts()
    copy_build_helpers()
    copy_exact(AUTHORITY_EXTERNAL, ROOT / "authority/source/more-algebra.tex", AUTHORITY_SHA)
    copy_exact(COPYING_EXTERNAL, ROOT / "authority/COPYING", "4B2C8FC390F802CD92F0622DC00A708A588BEC54D0145D2EE135D6D7672BFE85")
    copy_exact(REPO / "upstream/stacks.lock.json", ROOT / "authority/upstream.lock.json", "B195ECC83AB0F32C574A60D1FDBA9B0DA4D35B04E0DF7CB106DC9C0FDAD99C0D")
    copy_exact(PRODUCER_EMENDATIONS, ROOT / "authority/producer/MORE_ALGEBRA_L_SOURCE_EMENDATIONS.json", EVIDENCE_SHA)
    sanitized_json_copy(PRODUCER_INVARIANTS, ROOT / "authority/producer/MORE_ALGEBRA_L_INVARIANTS.json", INVARIANTS_SHA)
    sanitized_json_copy(PRODUCER_LIVE_MANIFEST, ROOT / "authority/producer/MORE_ALGEBRA_LIVE_PART_MANIFEST.json", "2324C5ED142D7BD8CE5D88ABA770FC7C96F75FF4EC25E16225C647DC0E521319")
    sanitized_json_copy(REGISTRAR_REVIEW, ROOT / "authority/registrar/MORE_ALGEBRA_L_R38_INDEPENDENT_REVIEW_20260831.json", "D2A93C491B5FB7DE23DAF452B78F066C0349AFB62716F546F0745505A3583805")
    authority = (ROOT / "authority/source/more-algebra.tex").read_bytes()
    packet, evidence = load_packet()
    operations = locate_operations(authority, evidence)
    payload = apply_operations(authority, operations)
    (ROOT / "payload").mkdir(parents=True, exist_ok=True)
    (ROOT / "payload/more-algebra.tex").write_bytes(payload)
    dedup = prior_dedup(operations)
    if not dedup["novel"]:
        raise AssertionError("R38 is not novel against admitted registry source maps")

    operations_by_stable: dict[str, list[dict]] = {stable: [] for stable, _, _ in GROUPS}
    for operation in operations:
        operations_by_stable[operation["stable_id"]].append(operation)
    stable_units = []
    source_map = []
    for stable, producer_ids, cls in GROUPS:
        ops = operations_by_stable[stable]
        canonical = [p for p in producer_ids if p not in {"MORE-ALGEBRA-L-030", "MORE-ALGEBRA-L-031"}]
        aliases = [p for p in producer_ids if p in {"MORE-ALGEBRA-L-030", "MORE-ALGEBRA-L-031"}]
        locus = "more-algebra.tex:" + ";".join(str(op["source_start_line"]) for op in ops)
        unit = {
            "class": cls,
            "id": stable,
            "locus": locus,
            "operation_ids": [op["operation_id"] for op in ops],
            "payload": "payload/more-algebra.tex",
            "producer_id": canonical[0],
            "producer_ids": canonical,
            "producer_aliases": aliases,
            "source": "more-algebra.tex",
            "status": "accepted_materialized_source_replay_pass",
        }
        stable_units.append(unit)
        source_map.append({
            "schema": "mathematics-commons-stacks-source-map/v2",
            "unit_id": stable,
            "producer_id": canonical[0],
            "producer_ids": canonical,
            "producer_aliases": aliases,
            "source": "more-algebra.tex",
            "authority": "authority/source/more-algebra.tex",
            "authority_sha256": AUTHORITY_SHA,
            "payload": "payload/more-algebra.tex",
            "locus": locus,
            "class": cls,
            "proof": "Independent authority replay confirmed exact preimages, mathematical or grammatical necessity, and no R1-R37 duplicate.",
            "adverse_evidence": (
                "The original one-operation L-015 proposal is preserved as correct but incomplete; linked product bounds at lines 38321 and 38325 are required."
                if stable == "MC-STK-ERR-1347" else None
            ),
            "operations": ops,
        })

    op_spec = {
        "schema": "mathematics-commons-stacks-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA,
        "payload_sha256": PAYLOAD_SHA,
        "operation_count": len(operations),
        "apply_order": "descending_start_byte",
        "operations": operations,
    }
    dump(ROOT / "operation-spec.input.json", {
        "schema": op_spec["schema"],
        "authority_sha256": AUTHORITY_SHA,
        "operation_count": len(operations),
        "operations": [{k: op[k] for k in ("stable_id", "producer_id", "source_start_line", "source_end_line", "old_text", "replacement_text")} for op in operations],
    })
    dump(ROOT / "operation-spec.json", op_spec)
    stable_doc = {"schema": "mathematics-commons-stacks-stable-units/v1", "authority_commit": UPSTREAM_COMMIT, "unit_count": len(stable_units), "units": stable_units}
    dump(ROOT / "stable-units.input.json", stable_doc)
    dump(ROOT / "stable-units.json", stable_doc)
    dump_jsonl(ROOT / "source-map.input.jsonl", source_map)
    dump_jsonl(ROOT / "source-map.jsonl", source_map)

    decisions = [
        {"schema":"mathematics-commons-stacks-decision/v1","id":"R38-D001","timestamp_utc":GENERATED_AT,"choice":"admit_23_semantic_units_from_29_original_producer_allegations","rationale":"All 29 original allegations are novel, exact, and independently correct; repeated or linked allegations are grouped by semantic unit.","supersedes":None},
        {"schema":"mathematics-commons-stacks-decision/v1","id":"R38-D002","timestamp_utc":GENERATED_AT,"choice":"expand_minimal_prime_product_unit","rationale":"MC-STK-ERR-1347 requires p_t to p_s at line 38314 and product bounds t to s at lines 38318, 38321, and 38325; t remains correct at lines 38341-38342 for top-dimensional components.","supersedes":"the incomplete one-operation MORE-ALGEBRA-L-015 submission"},
        {"schema":"mathematics-commons-stacks-decision/v1","id":"R38-D003","timestamp_utc":GENERATED_AT,"choice":"preserve_additive_aliases","rationale":"MORE-ALGEBRA-L-030 and L-031 are registrar/canon additive aliases inside MC-STK-ERR-1347 and consume no new stable IDs.","supersedes":None},
        {"schema":"mathematics-commons-stacks-decision/v1","id":"R38-D004","timestamp_utc":GENERATED_AT,"choice":"candidate_only_no_admission_or_composition","rationale":"This materialization remains within the active candidate lease; registry admission and generated-source composition are separate transitions.","supersedes":None},
    ]
    dump_jsonl(ROOT / "decisions.input.jsonl", decisions)
    dump_jsonl(ROOT / "decisions.jsonl", decisions)
    dump_jsonl(ROOT / "rejections.input.jsonl", [])
    dump_jsonl(ROOT / "rejections.jsonl", [])

    formula_ids = []
    prose_ids = []
    for row in source_map:
        changed = " ".join(op["old_text"] + op["replacement_text"] for op in row["operations"])
        (formula_ids if ("$" in changed or "\\" in changed) else prose_ids).append(row["unit_id"])
    inventory = {
        "schema": "mathematics-commons-stacks-formula-diagram-inventory/v1",
        "candidate_id": CANDIDATE_ID,
        "stable_unit_count": 23,
        "formula_units": formula_ids,
        "diagram_units": [],
        "prose_units": prose_ids,
        "mapped_units": len(formula_ids) + len(prose_ids),
        "unmapped_formula_or_diagram_changes": 0,
    }
    dump(ROOT / "formula-diagram-inventory.json", inventory)

    authority_structure = structure(authority.decode("utf-8"))
    payload_structure = structure(payload.decode("utf-8"))
    parity_keys = ["labels", "refs", "cites", "begins", "ends", "items", "xymatrix"]
    parity = {key: authority_structure[key] == payload_structure[key] for key in parity_keys}
    validation = {
        "schema": "mathematics-commons-stacks-source-validation/v1",
        "candidate_id": CANDIDATE_ID,
        "passed": all(parity.values()),
        "authority": artifact(ROOT / "authority/source/more-algebra.tex"),
        "payload": artifact(ROOT / "payload/more-algebra.tex"),
        "operation_spec": artifact(ROOT / "operation-spec.json"),
        "stable_unit_count": 23,
        "original_producer_allegations": 29,
        "registrar_additive_aliases": 2,
        "operation_count": 31,
        "declared_line_preimages_exactly_once": 31,
        "overlapping_operation_intervals": 0,
        "descending_replay_payload_match": True,
        "structure_parity": parity,
        "brace_balance": {
            "authority": [authority_structure["open_braces"], authority_structure["close_braces"]],
            "payload": [payload_structure["open_braces"], payload_structure["close_braces"]],
        },
        "deduplication": dedup,
        "retained_t_scope": {
            "line_38341_retains_top_dimensional_t": (
                "$i = 1, \\ldots, t$" in authority.decode("utf-8").splitlines()[38340]
                and authority.decode("utf-8").splitlines()[38340] == payload.decode("utf-8").splitlines()[38340]
            ),
            "line_38342_continuation_unchanged": (
                authority.decode("utf-8").splitlines()[38341] == payload.decode("utf-8").splitlines()[38341]
            ),
        },
        "producer_invariants": artifact(ROOT / "authority/producer/MORE_ALGEBRA_L_INVARIANTS.json"),
    }
    if not validation["passed"] or not all(validation["retained_t_scope"].values()):
        raise AssertionError("source validation failed")
    dump(ROOT / "source-validation.json", validation)

    adverse = {
        "schema":"mathematics-commons-stacks-adverse-history/v1",
        "status":"SUPERSEDED_INCOMPLETE_EVIDENCE",
        "original_submission":{
            "producer_ids":"MORE-ALGEBRA-L-001..029",
            "emendations_bytes":8459,
            "emendations_sha256":"3979731D70953EF119F6BA50398FDF6E3B82D7FA368879A44543C0CC52EB9E89",
            "invariants_bytes":17245,
            "invariants_sha256":"70E31567B3A20362757E4870CE98CF50B931C841E92342F1FE6CE6B6B7999AB1",
        },
        "incomplete_proposal":{
            "producer_id":"MORE-ALGEBRA-L-015","line":38318,"old":"_{i = 1}^t","new":"_{i = 1}^s",
            "disposition":"correct but insufficient alone; superseded by the four-operation MC-STK-ERR-1347 unit"
        },
        "current_repair":{
            "emendations":artifact(ROOT / "authority/producer/MORE_ALGEBRA_L_SOURCE_EMENDATIONS.json"),
            "invariants":artifact(ROOT / "authority/producer/MORE_ALGEBRA_L_INVARIANTS.json"),
            "aliases":["MORE-ALGEBRA-L-030","MORE-ALGEBRA-L-031"]
        }
    }
    dump(ROOT / "authority/adverse/ORIGINAL_L015_INCOMPLETE_SUBMISSION.json", adverse)
    adjudication = {
        "schema":"mathematics-commons-stacks-r38-adjudication/v1",
        "candidate_id":CANDIDATE_ID,
        "authority_commit":UPSTREAM_COMMIT,
        "authority_sha256":AUTHORITY_SHA,
        "result":"ACCEPT_23_SEMANTIC_UNITS_31_OPERATIONS",
        "stable_ids":[stable for stable,_,_ in GROUPS],
        "original_producer_ids":[f"MORE-ALGEBRA-L-{i:03d}" for i in range(1,30)],
        "additive_aliases":["MORE-ALGEBRA-L-030","MORE-ALGEBRA-L-031"],
        "rejected":[],
        "grouping":[{"stable_id":stable,"producer_ids":[p for p in producers if int(p[-3:])<=29],"aliases":[p for p in producers if int(p[-3:])>=30],"class":cls} for stable,producers,cls in GROUPS],
        "deduplication":dedup,
    }
    dump(ROOT / "authority/registrar/R38_ADJUDICATION_SPEC.json", adjudication)

    config = {
        "schema":"mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id":CANDIDATE_ID,"lease_id":LEASE_ID,"lease_status":"active; bound to registrar-issued LEASE.json",
        "namespace":"commons/stacks/errata/r38","writer_task":WRITER_TASK,
        "authority_commit":UPSTREAM_COMMIT,"authority_tree":UPSTREAM_TREE,
        "accepted":23,"rejected":0,"unresolved":0,"operation_count":31,
        "expected_unit_ids":[stable for stable,_,_ in GROUPS],
        "expected_producer_ids":[f"MORE-ALGEBRA-L-{i:03d}" for i in range(1,30)],
        "producer_aliases":["MORE-ALGEBRA-L-030","MORE-ALGEBRA-L-031"],
        "payload_expected_bytes":PAYLOAD_BYTES,"payload_expected_sha256":PAYLOAD_SHA,
        "source_date_epoch":SOURCE_DATE_EPOCH,
        "build_render_admission_status":"source_materialized_build_pending",
        "private_render_logical_path":"canon/private_evidence/errata-r38-20260831T021500Z/render",
        "stems":{"more-algebra":{"authority_bytes":len(authority),"authority_sha256":AUTHORITY_SHA,"payload_bytes":len(payload),"payload_sha256":PAYLOAD_SHA,"build_exceptions":{"candidate_page_delta":0},"display_delimiter_delta":0,"ordered_structure_exceptions":{}}},
        "visual_qa":{"correction_sensitive_pages":{"more-algebra":[]},"high_resolution_pages":{"more-algebra":[]}},
        "proof_closure":{"accepted":23,"operations":31,"producer_rows":29,"registrar_additive_aliases":2,"rejected":0,"unresolved":0},
        "authority_evidence":[artifact(path) for path in sorted((ROOT / "authority").rglob("*")) if path.is_file()],
    }
    dump(ROOT / "candidate.config.input.json", config)
    dump(ROOT / "candidate.config.json", config)

    review = {
        "schema":"mathematics-commons-stacks-independent-review/v1",
        "candidate_id":CANDIDATE_ID,"reviewed_at_utc":GENERATED_AT,"passed":True,
        "scope":"sealed source-level authority, exact operation, semantic adjudication, and registry deduplication replay; build and visual gates are recorded separately",
        "inputs":{"authority":artifact(ROOT / "authority/source/more-algebra.tex"),"producer_packet":artifact(ROOT / "authority/producer/MORE_ALGEBRA_L_SOURCE_EMENDATIONS.json"),"producer_invariants":artifact(ROOT / "authority/producer/MORE_ALGEBRA_L_INVARIANTS.json"),"registrar_review":artifact(ROOT / "authority/registrar/MORE_ALGEBRA_L_R38_INDEPENDENT_REVIEW_20260831.json")},
        "closure":{"stable_units":23,"original_producer_allegations":29,"additive_aliases":2,"operations":31,"rejections":0,"unresolved":0,"stable_id_start":"MC-STK-ERR-1336","stable_id_end":"MC-STK-ERR-1358"},
        "grouping":[{"stable_id":stable,"producer_ids":[p for p in producers if int(p[-3:])<=29],"aliases":[p for p in producers if int(p[-3:])>=30]} for stable,producers,_ in GROUPS],
        "source_replay":{"payload":artifact(ROOT / "payload/more-algebra.tex"),"validation":artifact(ROOT / "source-validation.json"),"deduplication_novel":True,"t_retained_at_lines_38341_38342":True},
        "adverse_history":artifact(ROOT / "authority/adverse/ORIGINAL_L015_INCOMPLETE_SUBMISSION.json"),
        "constraints":{"authority_mutated":False,"producer_target_mutated":False,"registry_mutated":False,"generated_source_mutated":False,"git_mutated":False,"publication_performed":False},
        "result":"PASS_SOURCE_GATE_BUILD_VISUAL_GATE_PENDING",
    }
    dump(ROOT / "replay/independent-review.json", review)

    regeneration = {
        "schema":"mathematics-commons-stacks-r38-regeneration-receipt/v1",
        "candidate_id":CANDIDATE_ID,"generated_at_utc":GENERATED_AT,"passed":True,
        "authority":artifact(ROOT / "authority/source/more-algebra.tex"),"payload":artifact(ROOT / "payload/more-algebra.tex"),
        "stable_units":artifact(ROOT / "stable-units.json"),"operation_spec":artifact(ROOT / "operation-spec.json"),
        "source_map":artifact(ROOT / "source-map.jsonl"),"decisions":artifact(ROOT / "decisions.jsonl"),
        "source_validation":artifact(ROOT / "source-validation.json"),"independent_review":artifact(ROOT / "replay/independent-review.json"),
        "constraints":{"registry_mutated":False,"generated_source_mutated":False,"git_mutated":False},
    }
    dump(ROOT / "REGENERATION_RECEIPT.json", regeneration)
    return {"passed":True,"payload_sha256":PAYLOAD_SHA,"stable_units":23,"operations":31,"dedup_novel":True}


def bind_visual_pages() -> dict:
    config_path = ROOT / "candidate.config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    page_map = json.loads((ROOT / "builds/source-page-map.json").read_text(encoding="utf-8"))
    pages = page_map["unique_pages"]
    if not pages or pages != sorted(set(pages)):
        raise AssertionError("invalid source-page map")
    config["visual_qa"] = {
        "correction_sensitive_pages":{"more-algebra":pages},
        "high_resolution_pages":{"more-algebra":pages},
        "source_page_map":artifact(ROOT / "builds/source-page-map.json"),
    }
    config["build_render_admission_status"] = "build_deterministic_replay_pass_visual_pending"
    dump(config_path, config)
    return {"passed":True,"pages":pages}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("materialize", "bind-visual-pages"))
    args = parser.parse_args()
    result = materialize() if args.command == "materialize" else bind_visual_pages()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
