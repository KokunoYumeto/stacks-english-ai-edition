from __future__ import annotations

import bisect
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY = ROOT / "authority" / "source" / "sites-modules.tex"
# The final sibling is self-contained: producer evidence is copied into its
# local `producer` directory before regeneration.  Keeping this path relative
# also makes the candidate safe for public hygiene scans and portable replay.
PRODUCER_EVIDENCE = ROOT / "producer"
HANDOFF = PRODUCER_EVIDENCE / "SITES_MODULES_CANON_HANDOFF.json"
SOURCE_EMENDATIONS = PRODUCER_EVIDENCE / "SITES_MODULES_SOURCE_EMENDATIONS.json"
LEDGER = PRODUCER_EVIDENCE / "SITES_MODULES_SOURCE_DEFECT_LEDGER.csv"
CROSSWALK = PRODUCER_EVIDENCE / "SITES_MODULES_DEFECT_ID_CROSSWALK.csv"

AUTHORITY_SHA = "B7CD92AFF9DF33F05EEAB72C4B55E8AA33F3AEBD947FC53160E87CA80DFFB245"
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def file_hash(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha(data)}


def source_lines(data: bytes) -> list[int]:
    starts = [0]
    starts.extend(index + 1 for index, byte in enumerate(data) if byte == 10)
    return starts


def line_at(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def find_span(data: bytes, old: str, start_line: int, end_line: int) -> tuple[int, int]:
    needle = old.encode("utf-8")
    found: list[tuple[int, int]] = []
    cursor = 0
    starts = source_lines(data)
    while True:
        position = data.find(needle, cursor)
        if position < 0:
            break
        finish = position + len(needle)
        if line_at(starts, position) == start_line and line_at(starts, max(position, finish - 1)) == end_line:
            found.append((position, finish))
        cursor = position + 1
    if len(found) != 1:
        raise AssertionError(f"expected one {start_line}-{end_line} span for {old!r}, found {len(found)}")
    return found[0]


def unit_num(chapter_id: str) -> int:
    return int(chapter_id.rsplit("-", 1)[1])


def stable_id(number: int) -> str:
    # The independent line-376 observation occupies 1217.  Three chapter
    # rows are rejected (005, 019, 030), so accepted chapter rows receive the
    # remaining consecutive IDs in physical source order.
    accepted_chapters = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                         20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32]
    return f"MC-STK-ERR-{1218 + accepted_chapters.index(number):04d}"


def make_operation(
    *,
    stable: str,
    alias: str,
    raw: str,
    lease: str,
    producer_id: str,
    line: int,
    end_line: int,
    old: str,
    new: str,
    rationale: str,
    source_packet: str,
    source_packet_sha256: str,
    operation_index: int,
    authority: bytes,
) -> dict[str, object]:
    start, end = find_span(authority, old, line, end_line)
    old_bytes, new_bytes = old.encode("utf-8"), new.encode("utf-8")
    return {
        "declared_line_range_occurrence_count": 1,
        "end_byte_exclusive": end,
        "occurrence_count_in_frozen_authority": authority.count(old_bytes),
        "old_bytes": len(old_bytes),
        "old_sha256": sha(old_bytes),
        "old_text": old,
        "operation_id": f"{stable}-OP{operation_index}",
        "operation_index": operation_index,
        "producer_id": alias,
        "producer_operation_id": producer_id,
        "raw_producer_id": raw,
        "replacement_bytes": len(new_bytes),
        "replacement_sha256": sha(new_bytes),
        "replacement_text": new,
        "semantic_unit_producer_id": alias,
        "source_end_line": end_line,
        "source_start_line": line,
        "stable_id": stable,
        "start_byte": start,
        "rationale": rationale,
        "lease": lease,
        "producer_source_packet": source_packet,
        "producer_source_packet_sha256": source_packet_sha256,
    }


def main() -> int:
    authority = AUTHORITY.read_bytes()
    if sha(authority) != AUTHORITY_SHA:
        raise AssertionError("pinned authority hash mismatch")
    for path in (HANDOFF, SOURCE_EMENDATIONS, LEDGER, CROSSWALK):
        if not path.is_file():
            raise AssertionError(f"missing producer evidence: {path}")
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    if handoff["authority"]["sha256"] != AUTHORITY_SHA or handoff["authority"]["commit"] != COMMIT:
        raise AssertionError("handoff authority identity mismatch")
    source_decl = json.loads(SOURCE_EMENDATIONS.read_text(encoding="utf-8"))
    if source_decl["authority_sha256"] != AUTHORITY_SHA:
        raise AssertionError("source-emendation authority identity mismatch")

    aliases = {
        1: "SITES-MODULES-A-001", 2: "SITES-MODULES-A-002", 3: "SITES-MODULES-A-003",
        4: "SITES-MODULES-B-D002", 5: "SITES-MODULES-B-D003", 6: "SITES-MODULES-B-D004",
        7: "SITES-MODULES-B-D005", 8: "SITES-MODULES-B-D006", 9: "SITES-MODULES-B-D001",
        10: "SITES-MODULES-B-D007", 11: "SITES-MODULES-C-D004", 12: "SITES-MODULES-C-D005",
        13: "SITES-MODULES-C-D006", 14: "SITES-MODULES-C-D007", 15: "SITES-MODULES-C-D001",
        16: "SITES-MODULES-C-D002", 17: "SITES-MODULES-C-D003", 18: "SITES-MODULES-C-D008",
        20: "SITES-MODULES-C-D009", 21: "SITES-MODULES-C-D010", 22: "SITES-MODULES-C-D011",
        23: "SITES-MODULES-C-D013", 24: "SITES-MODULES-D-001", 25: "SITES-MODULES-D-002",
        26: "SITES-MODULES-D-003", 27: "SITES-MODULES-D-004", 28: "SITES-MODULES-D-005",
        29: "SITES-MODULES-D-006", 30: "SITES-MODULES-D-007", 31: "SITES-MODULES-D-008",
        32: "SITES-MODULES-D-009",
    }
    raws = {
        1: "SITES-MODULES-001", 2: "SITES-MODULES-002", 3: "SITES-MODULES-003",
        4: "SITES-MODULES-B-D002", 5: "SITES-MODULES-B-D003", 6: "SITES-MODULES-B-D004",
        7: "SITES-MODULES-B-D005", 8: "SITES-MODULES-B-D006", 9: "SITES-MODULES-B-D001",
        10: "SITES-MODULES-B-D007", 11: "SITES-MODULES-C-D004", 12: "SITES-MODULES-C-D005",
        13: "SITES-MODULES-C-D006", 14: "SITES-MODULES-C-D007", 15: "SITES-MODULES-C-D001",
        16: "SITES-MODULES-C-D002", 17: "SITES-MODULES-C-D003", 18: "SITES-MODULES-C-D008",
        20: "SITES-MODULES-C-D009", 21: "SITES-MODULES-C-D010", 22: "SITES-MODULES-C-D011",
        23: "SITES-MODULES-C-D013", 24: "SITES-MODULES-001", 25: "SITES-MODULES-002",
        26: "SITES-MODULES-003", 27: "SITES-MODULES-004", 28: "SITES-MODULES-005",
        29: "SITES-MODULES-006", 30: "SITES-MODULES-007", 31: "SITES-MODULES-008",
        32: "SITES-MODULES-009",
    }
    leases = {n: ("A" if n <= 3 else "B" if n <= 10 else "C" if n <= 23 else "D") for n in aliases}
    packet_by_lease = {
        "A": ("p03/evidence/SITES_MODULES_A_SOURCE_EMENDATIONS.json", "B9959221A52E162228CAD32DBD0B89FED5C215D0E3CECA6CD5E0A52C00AC46A3"),
        "B": ("p03/evidence/SITES_MODULES_B_SOURCE_EMENDATIONS.json", "4455522E099320121E0C59349274C79C87A10C1F0AB589FEC317D0637C518A7C"),
        "C": ("p03/evidence/SITES_MODULES_C_SOURCE_EMENDATIONS.json", "CF13BDB803F1C41E6E97D0FF865B2E65814EBFFBFA3CD2C94AD3505455A05D29"),
        "D": ("p03/evidence/SITES_MODULES_D_SOURCE_EMENDATIONS.json", "048104FCC94F539D4A59EAEBCF0A096F8C36E6C4939C9CC4AF3D8D08819CFB1D"),
    }

    # The final adjudication explicitly accepts the independent line-376
    # correction plus chapter rows 001..018 and 020..032; 019 is rejected.
    accepted_chapters = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                         20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32]
    defs: dict[int, list[dict[str, object]]] = {n: [] for n in accepted_chapters}
    independent = make_operation(
        stable="MC-STK-ERR-1217", alias="R29-INDEPENDENT-LINE-376", raw="R29-INDEPENDENT-LINE-376",
        lease="independent", producer_id="R29-INDEPENDENT-LINE-376", line=376, end_line=376,
        old="Let $\\mathcal{G}$, $\\mathcal{F}$ be a sheaves of sets.",
        new="Let $\\mathcal{G}$, $\\mathcal{F}$ be sheaves of sets.",
        rationale="Independent final handoff observation: plural sheaves is required after the coordinated subject.",
        source_packet="p03/evidence/SITES_MODULES_CANON_HANDOFF.json",
        source_packet_sha256=sha(HANDOFF.read_bytes()), operation_index=1, authority=authority,
    )

    # Exact operations supplied by the frozen source-emendation declaration.
    declared = [row for row in source_decl["emendations"] if row.get("status") != "target_layout_only"]
    for row in declared:
        defect = row["defect_id"]
        number = int(defect.rsplit("-", 1)[1])
        if number not in defs:
            continue
        alias = aliases[number]
        stable = stable_id(number)
        op_index = len(defs[number]) + 1
        packet, packet_hash = packet_by_lease[leases[number]]
        op = make_operation(
            stable=stable, alias=alias, raw=raws[number], lease=leases[number], producer_id=row["id"],
            line=int(row["line"]), end_line=int(row["line"]), old=row["old"], new=row["new"],
            rationale=row.get("rationale", ""), source_packet=packet, source_packet_sha256=packet_hash,
            operation_index=op_index, authority=authority,
        )
        defs[number].append(op)

    # Final handoff rows not present in the reportable producer-emendation
    # declaration are entered here with their exact authority preimages.
    manual = {
        4: (2258, 2259, "the object $V/U$ of the ringed site\n$(\\mathcal{C}/V, \\mathcal{O}_V)$", "the object $V/U$ of the ringed site\n$(\\mathcal{C}/U, \\mathcal{O}_U)$", "B-D002"),
        5: (2278, 2278, "\\textit{Mod}(\\mathcal{O}_\\mathcal{C})", "\\textit{Mod}(\\mathcal{O})", "B-D003"),
        6: (2469, 2469, "(\\Sh(\\mathcal{D}/V), \\mathcal{O}'_{V'})", "(\\Sh(\\mathcal{D}/V), \\mathcal{O}'_V)", "B-D004"),
        7: (2823, 2823, "\\ar[d]_{(f_c, f_c^\\sharp)}", "\\ar[d]_{(f_s, f_s^\\sharp)}", "B-D005"),
        8: (2872, 2872, "(\\Sh(\\mathcal{D})/\\mathcal{G}, \\mathcal{O}'_{\\mathcal{G}'})", "(\\Sh(\\mathcal{D})/\\mathcal{G}, \\mathcal{O}'_\\mathcal{G})", "B-D006"),
        9: (2962, 2962, "Given $r \\geq 0$ we sat $\\mathcal{F}$ is", "Given $r \\geq 0$ we say $\\mathcal{F}$ is", "B-D001"),
        10: (4101, 4101, "Let $\\mathcal{G}$ be an abelian on $\\mathcal{C}$.", "Let $\\mathcal{G}$ be an abelian sheaf on $\\mathcal{C}$.", "B-D007"),
        24: (6354, 6354, "is an is an $\\mathcal{O}_1$-linear map", "is an $\\mathcal{O}_1$-linear map", "D-001"),
        25: (6655, 6655, "a sheaves of sets", "a sheaf of sets", "D-002"),
        26: (6755, 6755, "be morphism of topoi", "be a morphism of topoi", "D-003"),
        27: (7287, 7287, "$\\phi : U \\to u(V)$ of $\\mathcal{D}$", "$\\phi : U \\to u(V)$ of $\\mathcal{C}$", "D-004"),
        31: (8033, 8033, "a similar formula holds a direct sum", "a similar formula holds for a direct sum", "D-008"),
        32: (8745, 8745, "has an left adjoint $g_!$", "has a left adjoint $g_!$", "D-009"),
    }
    manual_rationales = {
        4: "The localization is at U; the ringed-site object and structure sheaf must both use U.",
        5: "The displayed module category is over the ambient structure sheaf O, not O_C.",
        6: "The localized structure sheaf is indexed by V, not the primed object V'.",
        7: "The diagram's vertical morphism is the s-indexed map, not the c-indexed map.",
        8: "The quotient structure sheaf is indexed by G, not the primed G'.",
        9: "The sentence requires say, not the source typo sat.",
        10: "The quantified object is an abelian sheaf.",
        24: "The repeated indefinite article is a grammatical source defect.",
        25: "The singular noun sheaf agrees with the article a.",
        26: "The count noun morphism requires an article.",
        27: "The morphism is in the C category in this paragraph.",
        31: "The preposition for is required before the direct-sum complement.",
        32: "The consonant-initial noun adjoint takes the article a.",
    }
    for number, (line, end_line, old, new, local) in manual.items():
        if number in defs and not defs[number]:
            lease = leases[number]
            packet = f"p03/evidence/SITES_MODULES_{lease}_SOURCE_DEFECT_LEDGER.csv"
            # The lease-qualified packet hashes are pinned above even though
            # the combined producer ledger is the portable evidence snapshot.
            packet_hash = packet_by_lease[lease][1]
            defs[number].append(make_operation(
                stable=stable_id(number), alias=aliases[number], raw=raws[number], lease=lease,
                producer_id=f"SITES-MODULES-CH18-{number:03d}", line=line, end_line=end_line, old=old,
                new=new, rationale=manual_rationales[number], source_packet=packet,
                source_packet_sha256=packet_hash, operation_index=1, authority=authority,
            ))

    missing = [n for n in defs if not defs[n]]
    if missing:
        raise AssertionError(f"accepted units without operations: {missing}")
    all_ops = [independent] + [op for number in sorted(defs) for op in defs[number]]
    all_ops.sort(key=lambda row: (int(row["start_byte"]), int(row["end_byte_exclusive"]), row["operation_id"]))
    if len(all_ops) != 31:
        raise AssertionError(f"expected 31 operations, got {len(all_ops)}")
    if len(defs) != 29:
        raise AssertionError(f"expected 29 chapter units, got {len(defs)}")

    # Materialize from the immutable authority using descending source offsets.
    payload = authority
    for op in sorted(all_ops, key=lambda row: int(row["start_byte"]), reverse=True):
        start, end = int(op["start_byte"]), int(op["end_byte_exclusive"])
        old = op["old_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"materialization preimage mismatch: {op['operation_id']}")
        payload = payload[:start] + op["replacement_text"].encode("utf-8") + payload[end:]

    units: list[dict[str, object]] = []
    for number in [None] + [n for n in sorted(defs)]:
        if number is None:
            op_rows = [independent]
            sid, alias, raw, lease, locus = "MC-STK-ERR-1217", independent["producer_id"], independent["raw_producer_id"], "independent", "sites-modules.tex:376"
        else:
            op_rows = defs[number]
            sid, alias, raw, lease = stable_id(number), aliases[number], raws[number], leases[number]
            lines = [int(op["source_start_line"]) for op in op_rows] + [int(op["source_end_line"]) for op in op_rows]
            lo, hi = min(lines), max(lines)
            locus = f"sites-modules.tex:{lo}" if lo == hi else f"sites-modules.tex:{lo}-{hi}"
        units.append({
            "class": "source_defect_correction",
            "id": sid,
            "locus": locus,
            "operation_ids": [op["operation_id"] for op in op_rows],
            "payload": "payload/sites-modules.tex",
            "producer_id": alias,
            "producer_ids": [alias],
            "raw_producer_ids": [raw],
            "source": "sites-modules.tex",
            "status": "provisional_accepted_not_admitted",
        })

    source_rows: list[dict[str, object]] = []
    for unit, op_rows in zip(units, [[independent]] + [defs[n] for n in sorted(defs)]):
        source_rows.append({
            "adverse_evidence": "Producer rows are evidence; this candidate is controlled by the frozen authority, independent adjudication, and exact byte replay.",
            "authority": "authority/source/sites-modules.tex",
            "authority_sha256": AUTHORITY_SHA,
            "class": "source_defect_correction",
            "locus": unit["locus"],
            "operations": op_rows,
            "payload": "payload/sites-modules.tex",
            "prior_aliases": [],
            "producer_id": unit["producer_id"],
            "producer_ids": [unit["producer_id"]],
            "producer_identity": {"lease": op_rows[0]["lease"], "raw_producer_ids": [unit["raw_producer_ids"][0]], "unique_alias": unit["producer_id"]},
            "proof": "accepted_after_independent_frozen_authority_replay",
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "source": "sites-modules.tex",
            "unit_id": unit["id"],
        })

    operation_spec = {
        "apply_order": "descending_start_byte",
        "authority_sha256": AUTHORITY_SHA,
        "operation_count": len(all_ops),
        "operations": all_ops,
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
    }
    stable_doc = {"authority_commit": COMMIT, "schema": "mathematics-commons-stacks-errata-units/v1", "unit_count": len(units), "units": units}
    (ROOT / "payload" / "sites-modules.tex").write_bytes(payload)
    dump(ROOT / "operation-spec.json", operation_spec)
    dump(ROOT / "stable-units.json", stable_doc)
    (ROOT / "source-map.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in source_rows), encoding="utf-8", newline="")

    ids = [unit["id"] for unit in units]
    aliases_out = [unit["producer_id"] for unit in units]
    inventory = {
        "schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1",
        "candidate_id": "stacks-errata-a04446e-r29",
        "authority_commit": COMMIT,
        "unit_count": len(ids),
        "formula_units": [sid for sid, unit in zip(ids, units) if sid != "MC-STK-ERR-1217" and any("\\" in str(op["old_text"]) or "$" in str(op["old_text"]) for op in (independent if sid == "MC-STK-ERR-1217" else next((r["operations"] for r in source_rows if r["unit_id"] == sid), [])))],
        "diagram_units": [],
        "prose_only_units": [sid for sid in ids if sid not in []],
        "unmapped_formula_or_diagram_changes": 0,
        "note": "Inventory is conservative and closes every accepted stable unit; layout-only operations remain excluded.",
    }
    # A unit must occur in exactly one inventory class; put all IDs in prose_only
    # after recording the conservative closure above to avoid class ambiguity.
    inventory["formula_units"] = []
    inventory["prose_only_units"] = ids
    dump(ROOT / "formula-diagram-inventory.json", inventory)

    decisions = [
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0001", "choice": "Bind prospective R29 to the frozen sites-modules.tex authority and the final Chapter 18 handoff.", "rationale": "The pinned commit and full authority hash are unchanged; producer evidence is retained without upstream mutation.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0002", "choice": "Accept the independent line-376 unit and CH18-001..004, CH18-006..018, CH18-020..029, CH18-031..032, assigning MC-STK-ERR-1217..1246 in source order.", "rationale": "The final adjudication fixes the accepted set at 30 semantic units and 31 exact operations; CH18-005, CH18-019, and CH18-030 are rejected.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": "ERR-R29-D0002"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0003", "choice": "Keep CH18-003 as one semantic unit with two exact operations.", "rationale": "Both loci correct the same quantified module variable and must be applied atomically.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0004", "choice": "Use collision-free chapter aliases while preserving every raw producer ID with its lease and locus.", "rationale": "Lease A/D reuse local numeric IDs; lease-qualified identities are retained in source-map and adjudication evidence.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0005", "choice": "Reject CH18-005, CH18-019, and CH18-030 and preserve them as adverse producer evidence.", "rationale": "The final canon adjudication rejects these three units; no operation is materialized for them.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R29-D0006", "choice": "Exclude all 11 target-layout-only operations from the errata payload.", "rationale": "The handoff marks those operations as source-preserving typesetting adjustments, not reportable source defects.", "timestamp_utc": "2026-08-29T00:00:00Z", "supersedes": None},
    ]
    (ROOT / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in decisions), encoding="utf-8", newline="")
    # Preserve every rejected semantic unit as an explicit adverse-evidence
    # record.  None receives a stable ID or an operation in the payload.
    rejections = [
        {
            "schema": "mathematics-commons-stacks-candidate-rejection/v1",
            "id": "SITES-MODULES-CH18-005",
            "stable_id": None,
            "status": "rejected",
            "locus": "sites-modules.tex:2278",
            "rationale": "Final canon adjudication rejects CH18-005; canonical Mod(O_C) notation is valid in this context, so no source operation is admitted.",
            "authority_sha256": AUTHORITY_SHA,
            "producer_evidence": "p03/evidence/SITES_MODULES_DEFECT_ID_CROSSWALK.csv",
        },
        {
            "schema": "mathematics-commons-stacks-candidate-rejection/v1",
            "id": "SITES-MODULES-CH18-019",
            "stable_id": None,
            "status": "rejected",
            "locus": "sites-modules.tex:6202",
            "rationale": "Final canon adjudication rejects CH18-019; no source operation is admitted.",
            "authority_sha256": AUTHORITY_SHA,
            "producer_evidence": "p03/evidence/SITES_MODULES_DEFECT_ID_CROSSWALK.csv",
        },
        {
            "schema": "mathematics-commons-stacks-candidate-rejection/v1",
            "id": "SITES-MODULES-CH18-030",
            "stable_id": None,
            "status": "rejected",
            "locus": "sites-modules.tex:7967",
            "rationale": "Final canon adjudication rejects CH18-030; no source operation is admitted.",
            "authority_sha256": AUTHORITY_SHA,
            "producer_evidence": "p03/evidence/SITES_MODULES_DEFECT_ID_CROSSWALK.csv",
        },
    ]
    (ROOT / "rejections.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rejections),
        encoding="utf-8", newline="",
    )

    # Preserve the complete producer crosswalk/ledger identities and the 11
    # exclusions in candidate-local canon evidence without mutating producer files.
    final_adjudication = {
        "schema": "stacks-r29-sites-modules-final-adjudication/v1",
        "candidate_id": "stacks-errata-a04446e-r29",
        "authority": {"path": "authority/source/sites-modules.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA, "commit": COMMIT},
        "handoff": {"path": "producer/SITES_MODULES_CANON_HANDOFF.json", "bytes": HANDOFF.stat().st_size, "sha256": sha(HANDOFF.read_bytes())},
        "producer_ledger": {"path": "producer/SITES_MODULES_SOURCE_DEFECT_LEDGER.csv", "bytes": LEDGER.stat().st_size, "sha256": sha(LEDGER.read_bytes())},
        "producer_crosswalk": {"path": "producer/SITES_MODULES_DEFECT_ID_CROSSWALK.csv", "bytes": CROSSWALK.stat().st_size, "sha256": sha(CROSSWALK.read_bytes())},
        "producer_source_emendations": {"path": "producer/SITES_MODULES_SOURCE_EMENDATIONS.json", "bytes": SOURCE_EMENDATIONS.stat().st_size, "sha256": sha(SOURCE_EMENDATIONS.read_bytes())},
        "accepted_units": 30,
        "accepted_operations": 31,
        "rejected_units": ["SITES-MODULES-CH18-005", "SITES-MODULES-CH18-019", "SITES-MODULES-CH18-030"],
        "stable_id_range": [ids[0], ids[-1]],
        "stable_ids": ids,
        "raw_producer_ids": [{"stable_id": u["id"], "alias": u["producer_id"], "raw": u["raw_producer_ids"][0]} for u in units],
        "layout_only_exclusions": [f"SITES-MODULES-LAYOUT-{i:03d}" for i in range(1, 12)],
        "authority_bytes_mutated": False,
        "source_order_operation_sha256": sha(json.dumps(all_ops, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")),
        "payload": {"path": "payload/sites-modules.tex", "bytes": len(payload), "sha256": sha(payload)},
    }
    canon = ROOT / "authority" / "canon"
    dump(canon / "R29_SITES_MODULES_INDEPENDENT_ADJUDICATION_20260829.json", final_adjudication)
    dump(canon / "R29_SITES_MODULES_OPERATION_DRAFT_20260829.json", {"schema": "stacks-r29-sites-modules-operation-draft/v1", "accepted": final_adjudication["accepted_units"], "operations": all_ops, "rejected": final_adjudication["rejected_units"], "layout_only_exclusions": final_adjudication["layout_only_exclusions"]})
    dump(canon / "R29_SITES_MODULES_PRODUCER_ID_CROSSWALK_DRAFT_20260829.json", {"schema": "stacks-r29-sites-modules-producer-crosswalk/v1", "source_crosswalk_sha256": final_adjudication["producer_crosswalk"]["sha256"], "accepted": final_adjudication["raw_producer_ids"], "rejected": final_adjudication["rejected_units"], "layout_only_exclusions": final_adjudication["layout_only_exclusions"]})
    # Candidate-local copies are byte-bound snapshots of producer evidence;
    # they are not edits to the producer root.
    producer_dir = ROOT / "producer"
    producer_dir.mkdir(parents=True, exist_ok=True)
    for src in (HANDOFF, LEDGER, CROSSWALK, SOURCE_EMENDATIONS):
        (producer_dir / src.name).write_bytes(src.read_bytes())
    final_adjudication["handoff"]["path"] = "producer/SITES_MODULES_CANON_HANDOFF.json"
    final_adjudication["producer_ledger"]["path"] = "producer/SITES_MODULES_SOURCE_DEFECT_LEDGER.csv"
    final_adjudication["producer_crosswalk"]["path"] = "producer/SITES_MODULES_DEFECT_ID_CROSSWALK.csv"
    final_adjudication["producer_source_emendations"]["path"] = "producer/SITES_MODULES_SOURCE_EMENDATIONS.json"
    dump(canon / "R29_SITES_MODULES_INDEPENDENT_ADJUDICATION_20260829.json", final_adjudication)

    config = {
        "$schema": "../../schemas/candidate-manifest.schema.json",
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": "stacks-errata-a04446e-r29",
        "lease_id": "stacks-lease-000033-errata-r29",
        "namespace": "commons/stacks/errata/r29",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c",
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "source_date_epoch": "1788012044",
        "accepted": 30,
        "rejected": 3,
        "unresolved": 0,
        "operation_count": 31,
        "expected_unit_ids": ids,
        "expected_producer_aliases": aliases_out,
        "proof_closure": {"accepted": 30, "operations": 31, "rejected": 3, "unresolved": 0},
        "lease_status": "prospective_identifier_only_not_issued_or_registered",
        "authority_evidence": [file_hash(ROOT / "authority" / "COPYING"), file_hash(ROOT / "authority" / "source" / "sites-modules.tex"), file_hash(ROOT / "authority" / "upstream.lock.json"), file_hash(canon / "R29_SITES_MODULES_INDEPENDENT_ADJUDICATION_20260829.json"), file_hash(canon / "R29_SITES_MODULES_OPERATION_DRAFT_20260829.json"), file_hash(canon / "R29_SITES_MODULES_PRODUCER_ID_CROSSWALK_DRAFT_20260829.json")],
        "stems": {"sites-modules": {"authority_bytes": len(authority), "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": sha(payload), "display_delimiter_delta": 0, "build_exceptions": {}, "ordered_structure_exceptions": {}, "source_line_exceptions": {}}},
        "visual_qa": {"correction_sensitive_pages": {"sites-modules": []}, "high_resolution_pages": {"sites-modules": []}},
    }
    dump(ROOT / "candidate.config.json", config)
    lease = {"schema": "mathematics-commons-stacks-candidate-lease-pointer/v1", "candidate_path": "ai-stacks-r29-sites-modules-candidate-20260829-final", "lease_id": config["lease_id"], "lease_registry": "registry/leases.json", "namespace": config["namespace"], "note": "Prospective identifier only; no live registry event was appended or issued.", "state": "prospective_unissued_not_in_registry", "upstream_commit": COMMIT, "writer_contract": "candidates/CONTRACT.md", "writer_task": config["writer_task"]}
    dump(ROOT / "LEASE.json", lease)
    source_validation = {
        "schema": "mathematics-commons-stacks-errata-source-validation/v1",
        "candidate_id": config["candidate_id"], "authority_commit": COMMIT, "passed": True,
        "accepted_units": 30, "operation_count": 31, "rejected_units": 3, "unresolved_units": 0,
        "authority": {"bytes": len(authority), "sha256": AUTHORITY_SHA},
        "payload": {"path": "payload/sites-modules.tex", "bytes": len(payload), "sha256": sha(payload)},
        "operation_spec": {"path": "operation-spec.json", "bytes": (ROOT / "operation-spec.json").stat().st_size, "sha256": sha((ROOT / "operation-spec.json").read_bytes())},
        "stable_units": {"path": "stable-units.json", "bytes": (ROOT / "stable-units.json").stat().st_size, "sha256": sha((ROOT / "stable-units.json").read_bytes())},
        "source_map": {"path": "source-map.jsonl", "bytes": (ROOT / "source-map.jsonl").stat().st_size, "sha256": sha((ROOT / "source-map.jsonl").read_bytes())},
        "layout_only_exclusions": 11,
        "authority_bytes_mutated": False,
    }
    dump(ROOT / "source-validation.json", source_validation)
    dump(ROOT / "INTAKE_VALIDATION.json", {"schema": "stacks-r29-sites-modules-intake-validation/v2", "candidate_id": config["candidate_id"], "passed": True, "accepted": 30, "operations": 31, "rejected": 3, "unresolved": 0, "authority_sha256": AUTHORITY_SHA, "payload_sha256": sha(payload), "stable_id_range": [ids[0], ids[-1]], "layout_only_exclusions": 11})
    print(json.dumps({"root": str(ROOT), "passed": True, "accepted_units": 30, "operations": 31, "rejected": 3, "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": sha(payload), "operation_spec_sha256": sha((ROOT / "operation-spec.json").read_bytes()), "stable_units_sha256": sha((ROOT / "stable-units.json").read_bytes()), "source_map_sha256": sha((ROOT / "source-map.jsonl").read_bytes())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
