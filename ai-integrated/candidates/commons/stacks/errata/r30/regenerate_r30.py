from __future__ import annotations

import bisect
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUTHORITY = ROOT / "authority/source/injectives.tex"
LEDGER = ROOT / "producer/INJECTIVES_SOURCE_DEFECT_LEDGER.csv"
CROSSWALK = ROOT / "producer/INJECTIVES_ID_CROSSWALK.csv"
EMENDATIONS = ROOT / "producer/INJECTIVES_SOURCE_EMENDATIONS.json"
LANGUAGE_QA = ROOT / "producer/INJECTIVES_LANGUAGE_QA.json"

COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_SHA = "B1367E48800C53D72C495D386EEF2D4D6C400652F9D00E69F664F17418D26520"
HANDOFF_IDENTITY = {
    "original_path": "p03/evidence/INJECTIVES_CANON_HANDOFF.json",
    "original_bytes": 2761,
    "original_sha256": "63212E779580E867942489D40AF52A918DB16C7134CE804CDCA93729F0F63F78",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def starts(data: bytes) -> list[int]:
    return [0] + [i + 1 for i, byte in enumerate(data) if byte == 10]


def line_at(line_starts: list[int], offset: int) -> int:
    return bisect.bisect_right(line_starts, offset)


def find_exact(data: bytes, old: str, first_line: int, last_line: int) -> tuple[int, int]:
    needle = old.encode("utf-8")
    line_starts = starts(data)
    matches: list[tuple[int, int]] = []
    cursor = 0
    while True:
        position = data.find(needle, cursor)
        if position < 0:
            break
        end = position + len(needle)
        if line_at(line_starts, position) == first_line and line_at(line_starts, max(position, end - 1)) == last_line:
            matches.append((position, end))
        cursor = position + 1
    if len(matches) != 1:
        raise AssertionError(f"{first_line}-{last_line}: expected one exact preimage {old!r}, found {len(matches)}")
    return matches[0]


# Every entry is one semantic unit and one exact operation.  Producer rows use
# their canonical IDs; independent grammar observations use R30-INDEPENDENT-*.
UNITS = [
    (69, 69, "INJECTIVES-CH19-D001", "B_\\beta \\to \\colim_{\\beta \\in \\alpha} B_\\alpha", "B_\\beta \\to \\colim_{\\beta \\in \\alpha} B_\\beta", "The colimit is indexed by beta, so its varying object is B_beta."),
    (71, 71, "INJECTIVES-CH19-D002", "neither injective or surjective", "neither injective nor surjective", "The correlative conjunction requires nor."),
    (110, 111, "R30-INDEPENDENT-001", "Suppose that, in (\\ref{equation-compare}), $\\mathcal{C}$ is the category\nof sets and $A$ is a {\\it finite set}, then", "If, in (\\ref{equation-compare}), $\\mathcal{C}$ is the category\nof sets and $A$ is a {\\it finite set}, then", "Use the conditional If rather than the malformed Suppose that ... then construction."),
    (172, 172, "INJECTIVES-CH19-D003", "Let $\\kappa$ the cardinality", "Let $\\kappa$ be the cardinality", "The sentence requires the copula be."),
    (446, 446, "R30-INDEPENDENT-002", "we denote $j : A \\to J(A)$ the functorial", "we denote by $j : A \\to J(A)$ the functorial", "The construction denote by X the object requires by."),
    (506, 507, "R30-INDEPENDENT-003", "we denote\n$j : M \\to J_R(M)$ the functorial", "we denote by\n$j : M \\to J_R(M)$ the functorial", "The construction denote by X the object requires by."),
    (675, 677, "R30-INDEPENDENT-004", "Denote\n$i : \\textit{Ab}(\\mathcal{C}) \\longrightarrow \\textit{PAb}(\\mathcal{C})$\nthe forgetful functor", "Denote by\n$i : \\textit{Ab}(\\mathcal{C}) \\longrightarrow \\textit{PAb}(\\mathcal{C})$\nthe forgetful functor", "The construction denote by X the object requires by."),
    (741, 741, "INJECTIVES-CH19-D004", "Suppose that $\\mathcal{G}_i$, $i\\in I$ is set of abelian sheaves", "Suppose that the $\\mathcal{G}_i$, $i\\in I$, form a set of abelian sheaves", "The plural subject requires plural agreement and an article."),
    (781, 782, "R30-INDEPENDENT-005", "we denote $\\mathbf{Z}_X$\nthe presheaf of abelian groups", "we denote by $\\mathbf{Z}_X$\nthe presheaf of abelian groups", "The construction denote by X the object requires by."),
    (913, 913, "INJECTIVES-CH19-D005", "Insert here future reference to internal hom.", "See Modules on Sites, Section \\ref{sites-modules-section-internal-hom}.", "The pinned Modules on Sites authority defines the referenced section label."),
    (936, 936, "INJECTIVES-CH19-D006", "This because $\\mathcal{J}$ is an injective abelian sheaf.", "This is because $\\mathcal{J}$ is an injective abelian sheaf.", "The sentence lacks its copula."),
    (959, 960, "INJECTIVES-CH19-D007", "As $\\mathcal{J}$ is\nan injective $\\mathcal{O}$-module, this extends to a map", "As $\\mathcal{J}$ is\nan injective abelian sheaf, the underlying map extends to a map", "Only injectivity of the underlying abelian sheaf was established."),
    (973, 974, "INJECTIVES-CH19-D008", "The composition of $ev$ with this\nthe displayed map gives", "The composition of $ev$ with the displayed\nmap gives", "Remove the duplicated determiner."),
    (1230, 1231, "INJECTIVES-CH19-D009", "the push-out of an admissible monomorphism $i : A \\to B$ via\nany morphism $A \\to A'$ exist", "the push-out of an admissible monomorphism $i : A \\to B$ via\nany morphism $A \\to A'$ exists", "The singular subject takes exists."),
    (1233, 1234, "INJECTIVES-CH19-D010", "the base change of an admissible epimorphism $p : B \\to C$ via\nany morphism $C' \\to C$ exist", "the base change of an admissible epimorphism $p : B \\to C$ via\nany morphism $C' \\to C$ exists", "The singular subject takes exists."),
    (1371, 1371, "INJECTIVES-CH19-D011", "\\phi)", "\\phi", "Remove the unmatched parenthesis in the predicate."),
    (1494, 1494, "INJECTIVES-CH19-D012", "combined the define a morphism", "together they define a morphism", "Restore the grammatical coordinated predicate."),
    (1606, 1606, "R30-INDEPENDENT-006", "Denote $c$ the function of", "Denote by $c$ the function of", "The construction denote by X the object requires by."),
    (1644, 1644, "INJECTIVES-CH19-D013", "an $K$-injective complex", "a $K$-injective complex", "K is consonant-initial in this reading."),
    (1663, 1663, "INJECTIVES-CH19-D014", "$K_\\beta^\\bullet = \\colim K_\\alpha^\\bullet$.", "$K_\\alpha^\\bullet = \\colim_{\\beta < \\alpha} K_\\beta^\\bullet$.", "A limit stage defines K_alpha as the colimit of preceding K_beta."),
    (1711, 1712, "INJECTIVES-CH19-D015", "such\n\\begin{enumerate}", "such that\n\\begin{enumerate}", "The enumerated conditions require such that."),
    (1758, 1758, "INJECTIVES-CH19-D016", "a functorial injective embeddings", "functorial injective embeddings", "Remove the singular article before the plural noun."),
    (1760, 1760, "R30-INDEPENDENT-007", "denote $J^\\bullet(M^\\bullet)$ the complex", "denote by $J^\\bullet(M^\\bullet)$ the complex", "The construction denote by X the object requires by."),
    (1794, 1794, "INJECTIVES-CH19-D017", "d^n_{J^\\bullet(M)}", "d^n_{J^\\bullet(M^\\bullet)}", "The defined functor takes the complex M^bullet."),
    (1833, 1833, "R30-INDEPENDENT-008", "Denote $\\mathbf{M}^\\bullet(-)$ the functor", "Denote by $\\mathbf{M}^\\bullet(-)$ the functor", "The construction denote by X the object requires by."),
    (1835, 1835, "R30-INDEPENDENT-009", "Denote $\\mathbf{N}^\\bullet(-)$ the functor", "Denote by $\\mathbf{N}^\\bullet(-)$ the functor", "The construction denote by X the object requires by."),
    (1869, 1869, "INJECTIVES-CH19-D018", "$\\varphi$ factor through", "$\\varphi$ factors through", "Third-person singular agreement."),
    (1882, 1882, "INJECTIVES-CH19-D019", "$w$ factor through", "$w$ factors through", "Third-person singular agreement."),
    (1883, 1883, "INJECTIVES-CH19-D020", "$\\mathbf{T}^n_{\\alpha'}(M^\\bullet)$", "$\\mathbf{T}_{\\alpha'}(M^\\bullet)$", "The morphism factors through the whole complex, not one degree."),
    (1920, 1920, "INJECTIVES-CH19-D021", "$F : \\mathcal{A} \\to \\textit{Ab}$", "$F : \\mathcal{A}^{opp} \\to \\textit{Ab}$", "The functor remains contravariant."),
    (1956, 1956, "INJECTIVES-CH19-D022", "in other words the right square", "In other words the right square", "Sentence-initial capitalization."),
    (2149, 2149, "INJECTIVES-CH19-D023", "$\\alpha^p \\circ \\alpha^{p' p} = \\alpha^{p'}$", "$\\alpha^{p'} \\circ \\alpha^{p p'} = \\alpha^p$", "The corrected composition is typed by the displayed sources and targets."),
    (2206, 2206, "INJECTIVES-CH19-D024", "$I^{p, \\bullet} \\times \\prod_{p' > p} J^{p, \\bullet}$", "$I^{p, \\bullet} \\times \\prod_{p' > p} J^{p', \\bullet}$", "The product index p' must vary."),
    (2214, 2214, "INJECTIVES-CH19-D025", "$\\alpha^{p + 1p} \\circ \\alpha^{pp'} = \\alpha^{p + 1p'}$", "$\\alpha^{pp'} \\circ \\alpha^{p + 1p} = \\alpha^{p + 1p'}$", "Only the corrected order is composable."),
    (2247, 2249, "R30-INDEPENDENT-010", "denote $K$, $F^pK$, $\\text{gr}^pK$ the\nobject of $D(\\mathcal{A})$ represented by $K^\\bullet$,\n$F^pK^\\bullet$, $\\text{gr}^pK^\\bullet$", "denote by $K$, $F^pK$, $\\text{gr}^pK$ the\nobjects of $D(\\mathcal{A})$ represented by $K^\\bullet$,\n$F^pK^\\bullet$, $\\text{gr}^pK^\\bullet$", "Add by and agree the plural objects with the three names."),
    (2316, 2318, "R30-INDEPENDENT-011", "denote $M$, $M/F^pM$, $\\text{gr}^pM$ the\nobject of $D(\\mathcal{A})$ represented by $M^\\bullet$,\n$M^\\bullet/F^pM^\\bullet$, $\\text{gr}^pM^\\bullet$", "denote by $M$, $M/F^pM$, $\\text{gr}^pM$ the\nobjects of $D(\\mathcal{A})$ represented by $M^\\bullet$,\n$M^\\bullet/F^pM^\\bullet$, $\\text{gr}^pM^\\bullet$", "Add by and agree the plural objects with the three names."),
    (2410, 2410, "INJECTIVES-CH19-D026", "$\\varphi^i = \\delta \\circ \\varphi^{i - 1}$", "$\\varphi^i = \\varphi^{i - 1} \\circ \\delta$", "Only the corrected order has source G^i and target I."),
    (2560, 2561, "R30-INDEPENDENT-012", "denote $E$\na set of objects", "denote by $E$\na set of objects", "The construction denote by X the object requires by."),
    (2578, 2578, "INJECTIVES-CH19-D027", "an element $(A_i, f_i)$ of $E$", "an element $(A_i, f_i)$ of $I$", "I, not E, is the set of pairs."),
    (2786, 2786, "INJECTIVES-CH19-D028", "H(F(RG(A)) \\\\", "H(F(RG(A))) \\\\", "Close the outer H parenthesis."),
]


def main() -> int:
    authority = AUTHORITY.read_bytes()
    if len(authority) != 105120 or digest(authority) != AUTHORITY_SHA:
        raise AssertionError("frozen authority identity mismatch")
    if len(UNITS) != 40 or [row[0] for row in UNITS] != sorted(row[0] for row in UNITS):
        raise AssertionError("unit count or source order mismatch")
    with LEDGER.open(encoding="utf-8-sig", newline="") as stream:
        ledger_rows = list(csv.DictReader(stream))
    producer_ids = {row["canonical_defect_id"] for row in ledger_rows}
    if len(ledger_rows) != 28 or len(producer_ids) != 28:
        raise AssertionError("producer ledger closure mismatch")
    declared_ids = {row[2] for row in UNITS if row[2].startswith("INJECTIVES-CH19-")}
    if declared_ids != producer_ids:
        raise AssertionError(f"producer unit mismatch: missing={producer_ids-declared_ids}, extra={declared_ids-producer_ids}")

    operations = []
    stable_units = []
    source_rows = []
    for ordinal, (first, last, producer_id, old, new, rationale) in enumerate(UNITS, 1247):
        stable = f"MC-STK-ERR-{ordinal:04d}"
        start, end = find_exact(authority, old, first, last)
        old_b, new_b = old.encode(), new.encode()
        operation = {
            "operation_id": f"{stable}-OP1", "operation_index": 1, "stable_id": stable,
            "producer_id": producer_id, "source_start_line": first, "source_end_line": last,
            "start_byte": start, "end_byte_exclusive": end,
            "old_text": old, "old_bytes": len(old_b), "old_sha256": digest(old_b),
            "replacement_text": new, "replacement_bytes": len(new_b), "replacement_sha256": digest(new_b),
            "occurrence_count_in_frozen_authority": authority.count(old_b),
            "declared_line_range_occurrence_count": 1, "rationale": rationale,
        }
        operations.append(operation)
        locus = f"injectives.tex:{first}" if first == last else f"injectives.tex:{first}-{last}"
        stable_units.append({"id": stable, "class": "source_defect_correction", "source": "injectives.tex", "payload": "payload/injectives.tex", "locus": locus, "operation_ids": [operation["operation_id"]], "producer_id": producer_id, "status": "provisional_accepted_not_admitted"})
        source_rows.append({"schema": "mathematics-commons-stacks-errata-map/v2", "unit_id": stable, "class": "source_defect_correction", "source": "injectives.tex", "authority": "authority/source/injectives.tex", "authority_sha256": AUTHORITY_SHA, "payload": "payload/injectives.tex", "locus": locus, "producer_id": producer_id, "operations": [operation], "proof": "provisional_acceptance_after_exact_frozen_authority_replay", "adverse_evidence": "Producer evidence is preserved; registry admission and generated-source composition are separate later transitions."})

    payload = authority
    for operation in sorted(operations, key=lambda row: row["start_byte"], reverse=True):
        start, end = operation["start_byte"], operation["end_byte_exclusive"]
        old_b = operation["old_text"].encode()
        if payload[start:end] != old_b:
            raise AssertionError(f"preimage mismatch during replay: {operation['operation_id']}")
        payload = payload[:start] + operation["replacement_text"].encode() + payload[end:]
    (ROOT / "payload/injectives.tex").write_bytes(payload)
    dump(ROOT / "operation-spec.json", {"schema": "mathematics-commons-stacks-errata-operation-spec/v1", "authority_sha256": AUTHORITY_SHA, "apply_order": "descending_start_byte", "operation_count": 40, "operations": operations})
    dump(ROOT / "stable-units.json", {"schema": "mathematics-commons-stacks-errata-units/v1", "authority_commit": COMMIT, "unit_count": 40, "units": stable_units})
    (ROOT / "source-map.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in source_rows), encoding="utf-8", newline="")
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8")

    math_ids = [row["stable_id"] for row in operations if "$" in row["old_text"] or "\\mathcal" in row["old_text"] or "\\mathbf" in row["old_text"]]
    prose_ids = [unit["id"] for unit in stable_units if unit["id"] not in math_ids]
    dump(ROOT / "formula-diagram-inventory.json", {"schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1", "candidate_id": "stacks-errata-a04446e-r30", "authority_commit": COMMIT, "unit_count": 40, "formula_units": math_ids, "diagram_units": [], "prose_only_units": prose_ids, "unmapped_formula_or_diagram_changes": 0})

    decisions = [
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R30-D0001", "choice": "Bind R30 to the frozen injectives.tex authority at commit a04446e.", "rationale": "The authority byte count and SHA-256 were independently replayed.", "timestamp_utc": "2026-08-29T00:00:00Z"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R30-D0002", "choice": "Provisionally accept all 28 producer rows and twelve independent grammar units as MC-STK-ERR-1247..1286 in source order.", "rationale": "All 40 exact preimages occur once at their declared source loci and replay without overlap.", "timestamp_utc": "2026-08-29T00:00:00Z"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R30-D0003", "choice": "Resolve the line-913 placeholder with the existing Modules on Sites internal-Hom section label.", "rationale": "The pinned sites-modules.tex authority defines sites-modules-section-internal-hom.", "timestamp_utc": "2026-08-29T00:00:00Z"},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R30-D0004", "choice": "Retain only sanitized producer summaries and clean primary evidence in the prospective candidate.", "rationale": "Raw ancillary producer receipts contain private absolute paths or stale build bindings.", "timestamp_utc": "2026-08-29T00:00:00Z"},
    ]
    (ROOT / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in decisions), encoding="utf-8", newline="")

    evidence = {}
    for path in (LEDGER, CROSSWALK, EMENDATIONS, LANGUAGE_QA):
        data = path.read_bytes(); evidence[path.name] = {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": digest(data)}
    sanitized = {"schema": "stacks-r30-injectives-sanitized-producer-handoff/v1", "chapter": 19, "source_file": "injectives.tex", "original_handoff_identity": HANDOFF_IDENTITY, "authority": {"path": "authority/source/injectives.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA, "commit": COMMIT}, "producer_evidence": evidence, "producer_counts": {"defect_rows": 28, "crosswalk_rows": 120, "source_emendation_operations": 11}, "candidate_adjudication": {"accepted_units": 40, "accepted_operations": 40, "rejected": 0, "stable_id_range": ["MC-STK-ERR-1247", "MC-STK-ERR-1286"]}, "sanitization": {"private_paths_removed": True, "raw_handoff_not_copied": True, "original_identity_preserved": True}}
    dump(ROOT / "authority/canon/R30_INJECTIVES_SANITIZED_HANDOFF.json", sanitized)
    dump(ROOT / "authority/upstream.lock.json", {"schema": "mathematics-commons-stacks-upstream-lock/v1", "project": "The Stacks Project", "commit": COMMIT, "tree": TREE, "scope": "single_frozen_source_file_for_prospective_errata_r30", "source": {"path": "injectives.tex", "bytes": len(authority), "sha256": AUTHORITY_SHA}})

    ids = [unit["id"] for unit in stable_units]
    config = {"schema": "mathematics-commons-stacks-errata-candidate-config/v1", "candidate_id": "stacks-errata-a04446e-r30", "namespace": "commons/stacks/errata/r30", "lease_id": "stacks-lease-000034-errata-r30", "lease_status": "prospective_identifier_only_not_issued_or_registered", "authority_commit": COMMIT, "authority_tree": TREE, "accepted": 40, "rejected": 0, "unresolved": 0, "operation_count": 40, "expected_unit_ids": ids, "prospective_post_r30_stable_total": 931, "proof_closure": {"accepted": 40, "operations": 40, "rejected": 0, "unresolved": 0}, "stems": {"injectives": {"authority_bytes": len(authority), "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": digest(payload), "display_delimiter_delta": 0}}, "build_state": "not_run", "manifest_state": "not_created", "review_state": "not_run", "admission_state": "not_admitted"}
    dump(ROOT / "candidate.config.json", config)
    dump(ROOT / "LEASE.json", {"schema": "mathematics-commons-stacks-candidate-lease-pointer/v1", "candidate_path": ROOT.name, "lease_id": config["lease_id"], "namespace": config["namespace"], "state": "prospective_unissued_not_in_registry", "upstream_commit": COMMIT})
    validation = {"schema": "mathematics-commons-stacks-errata-source-validation/v1", "candidate_id": config["candidate_id"], "passed": True, "accepted_units": 40, "operation_count": 40, "rejected_units": 0, "unresolved_units": 0, "authority": {"bytes": len(authority), "sha256": AUTHORITY_SHA}, "payload": {"path": "payload/injectives.tex", "bytes": len(payload), "sha256": digest(payload)}, "authority_bytes_mutated": False, "build_or_review_claimed": False}
    dump(ROOT / "source-validation.json", validation)
    dump(ROOT / "INTAKE_VALIDATION.json", {"schema": "stacks-r30-injectives-intake-validation/v1", "candidate_id": config["candidate_id"], "passed": True, "accepted": 40, "operations": 40, "rejected": 0, "unresolved": 0, "authority_sha256": AUTHORITY_SHA, "payload_sha256": digest(payload), "stable_id_range": [ids[0], ids[-1]], "prospective_post_r30_stable_total": 931})
    print(json.dumps({"passed": True, "units": 40, "operations": 40, "authority_sha256": AUTHORITY_SHA, "payload_bytes": len(payload), "payload_sha256": digest(payload), "stable_id_range": [ids[0], ids[-1]]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
