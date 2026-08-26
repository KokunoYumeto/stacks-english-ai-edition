from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AUTHORITY = (
    ROOT.parents[6]
    / "upstream"
    / "src"
    / "stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14"
    / "more-algebra.tex"
)
LEDGER = (
    ROOT.parents[9]
    / "romance"
    / "03_working_translations"
    / "stacks_fr_20260821"
    / "00_control"
    / "SOURCE_DEFECT_LEDGER.csv"
)
AUTHORITY_SHA256 = "0106554339E8966FE04411B2AE9F9CD856B165849FEEF0C7BC37634819064708"
AUTHORITY_BYTES = 1_492_039
COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
GENERATED_AT = "2026-08-26T03:45:00Z"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def op(line: int, old: str, new: str, end_line: int | None = None) -> dict:
    return {"source_start_line": line, "source_end_line": end_line or line, "old_text": old, "replacement_text": new}


ROWS = [
    ("MORE-ALGEBRA-001", "more-algebra.tex:11360", "editorial_placeholder", ["P02-E0175"], [op(11360, " (insert future reference here)", "")]),
    ("MORE-ALGEBRA-002", "more-algebra.tex:11408", "wrong_purely_inseparable_polynomial", ["P02-E0176"], [op(11408, "L[z]/(z^p - x)", "L[z]/(z^p - x^p)")]),
    ("MORE-ALGEBRA-003", "more-algebra.tex:11554", "wrong_terminal_variable_index", ["P02-E0179"], [op(11554, "[y_1^p, \\ldots, y_d^p]", "[y_1^p, \\ldots, y_m^p]")]),
    ("MORE-ALGEBRA-004", "more-algebra.tex:12171", "undefined_tensor_base", ["P02-E0184", "P02-E0883"], [op(12171, "\\otimes_{A/q}", "\\otimes_{A/\\mathfrak q}")]),
    ("MORE-ALGEBRA-005", "more-algebra.tex:12337", "wrong_completion_prime", ["P02-E0185", "P02-E0884"], [op(12337, "C_\\mathfrak r^\\wedge \\otimes_C L", "C_\\mathfrak q^\\wedge \\otimes_C L")]),
    ("MORE-ALGEBRA-006", "more-algebra.tex:12899", "wrong_fibre_algebra_base", ["P02-E0189"], [op(12899, "as $\\kappa(\\mathfrak q)$-algebras", "as $\\kappa(\\mathfrak p)$-algebras")]),
    ("MORE-ALGEBRA-007", "more-algebra.tex:13176", "undefined_product_terminal_index", ["P02-E0190", "P02-E0887"], [op(13176, "\\prod\\nolimits_{i = 1, \\ldots, t}", "\\prod\\nolimits_{i = 1, \\ldots, s}")]),
    ("MORE-ALGEBRA-008", "more-algebra.tex:14011", "wrong_derived_functor_variance", ["P02-E0197", "P02-E0894"], [op(14011, "right derived functor", "left derived functor")]),
    ("MORE-ALGEBRA-009", "more-algebra.tex:15399-15400", "editorial_placeholder", ["P02-E0222", "P02-E0914"], [op(15399, " (insert\nfuture reference here)", "", 15400)]),
    ("MORE-ALGEBRA-010", "more-algebra.tex:15706", "wrong_filtered_stage_index", ["P02-E0231", "P02-E0920"], [op(15706, "H^n(F^if_n)", "H^n(F^if_m)")]),
    ("MORE-ALGEBRA-011", "more-algebra.tex:15717", "wrong_complex_subscript", ["P02-E0232", "P02-E0921"], [op(15717, "d_{P_m}(\\eta_z)", "d_{P_{m + 1}}(\\eta_z)")]),
    ("MORE-ALGEBRA-012", "more-algebra.tex:15749", "wrong_limit_map_subscript", ["P02-E0233", "P02-E0922"], [op(15749, "H^n(F^if_n)", "H^n(F^if)")]),
    ("MORE-ALGEBRA-013", "more-algebra.tex:16072", "wrong_induction_degree", [], [op(16072, "with $F^{n_0}$ a finite free $R$-module", "with $F^{n - 1}$ a finite free $R$-module")]),
    ("MORE-ALGEBRA-014", "more-algebra.tex:16115", "reversed_complex_differential", [], [op(16115, "\\Ker(F^n \\to F^{n - 1})", "\\Ker(F^n \\to F^{n + 1})")]),
    ("MORE-ALGEBRA-015", "more-algebra.tex:16117", "missing_noun", ["P02-E0236"], [op(16117, "We extend our of complexes to", "We extend our map of complexes to")]),
    ("MORE-ALGEBRA-016", "more-algebra.tex:16129", "spelling", ["P02-E0237"], [op(16129, "Dnote again", "Denote again")]),
    ("MORE-ALGEBRA-017", "more-algebra.tex:16139-16140", "malformed_parallel_clause", ["P02-E0238"], [op(16139, "and the\nto $\\xi_i$", "and\nto $\\xi_i$", 16140)]),
    ("MORE-ALGEBRA-018", "more-algebra.tex:16369", "wrong_projectivity_ring", ["P02-E0239"], [op(16369, "projective $R$-modules", "projective $A$-modules")]),
    ("MORE-ALGEBRA-F-001", "more-algebra.tex:17250", "unmatched_opening_parenthesis", ["P02-E0241"], [op(17250, "((M", "(M")]),
    ("MORE-ALGEBRA-F-002", "more-algebra.tex:17455-17456", "duplicated_article", ["P02-E0242"], [op(17455, "choose a\na complex", "choose a\ncomplex", 17456)]),
    ("MORE-ALGEBRA-F-003", "more-algebra.tex:17632", "wrong_ext_ring", ["P02-E0243"], [op(17632, "\\Ext^i_A(N, K)", "\\Ext^i_R(N, K)")]),
    ("MORE-ALGEBRA-F-004", "more-algebra.tex:17750", "reversed_coordinate_indices", ["P02-E0245"], [op(17750, "a_{ij}", "a_{ji}")]),
    ("MORE-ALGEBRA-F-005", "more-algebra.tex:17757", "wrong_identity_object", [], [op(17757, "the identity on $R$", "its identity")]),
    ("MORE-ALGEBRA-F-006", "more-algebra.tex:17775-17776", "missing_ext_vanishing_predicate", [], [op(17775, "$\\Ext^1_R(P, N)$", "$\\Ext^1_R(P, N) = 0$")]),
    ("MORE-ALGEBRA-F-007", "more-algebra.tex:18287", "wrong_sign_indices", ["P02-E0248"], [op(18287, "\\epsilon_{p, r, s}", "\\epsilon_{p, q, r}")]),
    ("MORE-ALGEBRA-F-008", "more-algebra.tex:18316", "wrong_internal_hom_target", ["P02-E0249"], [op(18316, "hom(L^\\bullet, K^\\bullet)", "hom(L^\\bullet, M^\\bullet)")]),
    ("MORE-ALGEBRA-F-009", "more-algebra.tex:18489", "wrong_cohomological_index_form", ["P02-E0250"], [op(18489, "\\text{id}_{M_n}", "\\text{id}_{M^n}")]),
    ("MORE-ALGEBRA-F-010", "more-algebra.tex:19063-19064", "undefined_complex_symbol", ["P02-E0256"], [op(19063, "$M^a \\otimes_R L^b$", "$K^a \\otimes_R L^b$"), op(19063, "$M^a$ and $L^b$", "$K^a$ and $L^b$", 19064)]),
    ("MORE-ALGEBRA-F-011", "more-algebra.tex:20082-20083", "duplicated_equivalence_node", ["P02-E0268"], [op(20082, "\\Leftrightarrow (3) \\Leftrightarrow (3)", "\\Leftrightarrow (3)")]),
    ("MORE-ALGEBRA-G-001", "more-algebra.tex:20318-20321", "wrong_cohomological_term_notation", ["P02-E0273"], [op(20318, "M_b[-b]", "M^b[-b]"), op(20318, "M_b[-b + 1]", "M^b[-b + 1]"), op(20321, "M_b[-b]", "M^b[-b]")]),
    ("MORE-ALGEBRA-G-002", "more-algebra.tex:20460", "extraneous_copula", ["P02-E0275"], [op(20460, "with $L^i$ is finite free", "with $L^i$ finite free")]),
    ("MORE-ALGEBRA-G-003", "more-algebra.tex:20634", "orphaned_citation_fragment", ["P02-E0281"], [op(20634, "Derived Categories. ", "")]),
    ("MORE-ALGEBRA-G-004", "more-algebra.tex:20724", "wrong_differential_degree", ["P02-E0283"], [op(20724, "\\xrightarrow{d^1}", "\\xrightarrow{d^{-n + 1}}")]),
    ("MORE-ALGEBRA-G-005", "more-algebra.tex:21040", "wrong_localized_module", ["P02-E0290"], [op(21040, "$M_f$", "$M_g$")]),
    ("MORE-ALGEBRA-G-006", "more-algebra.tex:21043", "missing_matrix_operand", ["P02-E0291"], [op(21043, "$(x_0f - )I_t$", "$(x_0f - 1)I_t$")]),
    ("MORE-ALGEBRA-G-007", "more-algebra.tex:21053", "undefined_base_change_algebra", ["P02-E0292"], [op(21053, "M \\otimes_A A'", "M \\otimes_A (A \\otimes_R R')")]),
    ("MORE-ALGEBRA-G-008", "more-algebra.tex:21093", "extraneous_polynomial_variable", ["P02-E0293"], [op(21093, "R[x_0, x_1", "R[x_1")]),
    ("MORE-ALGEBRA-G-009", "more-algebra.tex:21526", "wrong_localization_element", ["P02-E0307"], [op(21526, "A_f", "A_g")]),
    ("MORE-ALGEBRA-G-010", "more-algebra.tex:21583", "wrong_polynomial_variable_bound", ["P02-E0311"], [op(21583, "A[y_1, \\ldots, y_n]", "A[y_1, \\ldots, y_m]")]),
    ("MORE-ALGEBRA-G-011", "more-algebra.tex:21703-21710", "lost_pseudo_coherence_qualifier", ["P02-E0316"], [op(21707, "$K^\\bullet$ is pseudo-coherent", "$K^\\bullet$ is $m$-pseudo-coherent"), op(21710, "$K^\\bullet$ is pseudo-coherent", "$K^\\bullet$ is $m$-pseudo-coherent")]),
    ("MORE-ALGEBRA-G-012", "more-algebra.tex:21911", "reversed_surjection", ["P02-E0323"], [op(21911, "$A \\to B$ is surjective", "$B \\to A$ is surjective")]),
    ("MORE-ALGEBRA-G-013", "more-algebra.tex:22352", "ill_typed_homotopy_differential", [], [op(22352, "h^0 \\circ d^{-1}_K", "h^0 \\circ d^{-1}_M")]),
    ("MORE-ALGEBRA-G-014", "more-algebra.tex:22361", "wrong_enumeration_reference", ["P02-E0332"], [op(22361, "\\item In (2)", "\\item In (3)")]),
    ("MORE-ALGEBRA-G-015", "more-algebra.tex:22705", "lost_subscripts_in_exponent", ["P02-E0337"], [op(22705, "I^{c2c3}", "I^{c_2c_3}")]),
    ("MORE-ALGEBRA-G-016", "more-algebra.tex:22717-22722", "reversed_composition_order", ["P02-E0339"], [op(22717, "\\varphi \\circ \\psi", "\\psi \\circ \\varphi"), op(22722, "\\varphi \\circ \\psi", "\\psi \\circ \\varphi")]),
    ("MORE-ALGEBRA-G-017", "more-algebra.tex:22730", "wrong_matrix_case", ["P02-E0341"], [op(22730, "\\det(a)", "\\det(A)")]),
    ("MORE-ALGEBRA-G-018", "more-algebra.tex:22965", "wrong_conjunction", ["P02-E0347"], [op(22965, "of $R^1\\lim_n", "if $R^1\\lim_n")]),
    ("MORE-ALGEBRA-G-019", "more-algebra.tex:22985", "undefined_derived_functor_symbol", ["P02-E0348"], [op(22985, "$RF$", "$R\\lim$")]),
    ("MORE-ALGEBRA-G-020", "more-algebra.tex:23047", "wrong_indefinite_article", ["P02-E0351"], [op(23047, "A inverse system", "An inverse system")]),
    ("MORE-ALGEBRA-G-021", "more-algebra.tex:23106", "spelling", ["P02-E0354"], [op(23106, "transitition", "transition")]),
    ("MORE-ALGEBRA-G-022", "more-algebra.tex:23209", "wrong_adverb", ["P02-E0355"], [op(23209, "the we obtain", "then we obtain")]),
    ("MORE-ALGEBRA-G-023", "more-algebra.tex:23398", "wrong_participle", ["P02-E0357"], [op(23398, "can also been seen", "can also be seen")]),
]


# Lease I is ordered by frozen-authority locus.  I-039 was appended late by the
# producer but belongs at line 28099.  Linked producer rows below describe one
# semantic defect and therefore consume one canon ID with multiple operations.
LEASE_I_ROWS = [
    ("MORE-ALGEBRA-I-001", "more-algebra.tex:27167", "wrong_infinitive", ["P02-E0437"], [op(27167, "is the show", "is to show")]),
    ("MORE-ALGEBRA-I-002", "more-algebra.tex:27183", "wrong_inverse_system_exponent", ["P02-E0438"], [op(27183, "A/(f_1^m, \\ldots, f_r^m)", "A/(f_1^n, \\ldots, f_r^n)")]),
    ("MORE-ALGEBRA-I-003", "more-algebra.tex:27268", "missing_copula", ["P02-E0441"], [op(27268, "$H^n(K)$ a finite $A$-module", "$H^n(K)$ is a finite $A$-module")]),
    ("MORE-ALGEBRA-I-004", "more-algebra.tex:27371", "malformed_equivalence_wording", ["P02-E0443"], [op(27371, "the usual $=$ derived completions", "the usual (equivalently, derived) completions")]),
    ("MORE-ALGEBRA-I-005", "more-algebra.tex:27507", "wrong_inferential_adverb", ["P02-E0446"], [op(27507, "This we get a surjection", "Thus we get a surjection")]),
    ("MORE-ALGEBRA-I-006", "more-algebra.tex:27715", "spelling", ["P02-E0450"], [op(27715, "compostion", "composition")]),
    ("MORE-ALGEBRA-I-039", "more-algebra.tex:28099", "missing_complex_component_grouping", ["P02-E0456"], [op(28099, "$\\eta_fM^i$", "$(\\eta_fM)^i$")]),
    ("MORE-ALGEBRA-I-007", "more-algebra.tex:28118;28120", "wrong_eta_complex_operation", ["P02-E0457"], [
        op(28118, "g^iN^i \\otimes g^{i + 1}N^{i + 1}", "g^iN^i \\oplus g^{i + 1}N^{i + 1}"),
        op(28120, "g^iN^i \\otimes g^{i + 1}N^{i + 1}", "g^iN^i \\oplus g^{i + 1}N^{i + 1}"),
    ]),
    ("MORE-ALGEBRA-I-010", "more-algebra.tex:28175", "wrong_complex_in_principality_conclusion", ["P02-E0460"], [op(28175, "$I_i(M^\\bullet, f)$ is a principal ideal", "$I_i(N^\\bullet, f)$ is a principal ideal")]),
    ("MORE-ALGEBRA-I-011", "more-algebra.tex:28259", "wrong_local_obstruction_conclusion", ["P02-E0461"], [op(28259, "$I_\\mathfrak p = fA_\\mathfrak p$", "$J(M^\\bullet, f)_\\mathfrak p = 0$")]),
    ("MORE-ALGEBRA-I-012", "more-algebra.tex:28278;28297", "wrong_eta_component_degree", ["P02-E0462"], [
        op(28278, "f^{i + 1}M^i \\oplus f^{i + 2}M^{i + 2}", "f^{i + 1}M^{i + 1} \\oplus f^{i + 2}M^{i + 2}"),
        op(28297, "f^{i + 1}M^i \\otimes_A C \\oplus f^{i + 2}M^{i + 2} \\otimes_A C", "f^{i + 1}M^{i + 1} \\otimes_A C \\oplus f^{i + 2}M^{i + 2} \\otimes_A C"),
    ]),
    ("MORE-ALGEBRA-I-014", "more-algebra.tex:28305", "wrong_cohomology_quotient_degree", ["P02-E0463"], [op(28305, "$K^{i + 1}/L^i$", "$K^i/L^{i - 1}$")]),
    ("MORE-ALGEBRA-I-015", "more-algebra.tex:28843;28845", "undefined_rhom_argument", ["P02-E0474"], [
        op(28843, "R\\Hom_R(K, L)", "R\\Hom_R(K, M)"),
        op(28845, "R\\Hom_R(K, L \\otimes_R^\\mathbf{L} R')", "R\\Hom_R(K, M \\otimes_R^\\mathbf{L} R')"),
    ]),
    ("MORE-ALGEBRA-I-017", "more-algebra.tex:28953", "spelling", ["P02-E0476"], [op(28953, "the cass of $z$", "the class of $z$")]),
    ("MORE-ALGEBRA-I-018", "more-algebra.tex:29085", "wrong_hom_exactness", ["P02-E0483"], [op(29085, "the right exact functor $\\Hom_A(-, N)$", "the left exact functor $\\Hom_A(-, N)$")]),
    ("MORE-ALGEBRA-I-019", "more-algebra.tex:29101", "stray_editorial_fragment", ["P02-E0484"], [op(29101, "by [art part (6)", "by part (6)")]),
    ("MORE-ALGEBRA-I-020", "more-algebra.tex:29227", "malformed_relative_clause", ["P02-E0487"], [op(29227, "these maps which witness", "these maps witness")]),
    ("MORE-ALGEBRA-I-021", "more-algebra.tex:29303", "spelling", ["P02-E0489"], [op(29303, "annihilated buy $I^c$", "annihilated by $I^c$")]),
    ("MORE-ALGEBRA-I-022", "more-algebra.tex:29316", "wrong_ext_base_ring", ["P02-E0490"], [op(29316, "I^c\\Ext^i_{A_n}(M_m, N_m)/I^n\\Ext^i_{A_n}(M_m, N_m) \\to", "I^c\\Ext^i_{A_m}(M_m, N_m)/I^n\\Ext^i_{A_m}(M_m, N_m) \\to")]),
    ("MORE-ALGEBRA-I-023", "more-algebra.tex:29352", "missing_module_subscript", ["P02-E0492"], [op(29352, "$N[x^{n - 1}] = \\Ker(x^{n - 1} : N_n \\to N_n)$", "$N_n[x^{n - 1}] = \\Ker(x^{n - 1} : N_n \\to N_n)$")]),
    ("MORE-ALGEBRA-I-024", "more-algebra.tex:29362", "wrong_quantifier_index", ["P02-E0493"], [op(29362, "for all $r$", "for all $n$")]),
    ("MORE-ALGEBRA-I-025", "more-algebra.tex:29377", "wrong_module_base_and_missing_finiteness", ["P02-E0494"], [op(29377, "Let $M, N$ be $A$-modules.", "Let $M, N$ be finite $B$-modules.")]),
    ("MORE-ALGEBRA-I-026", "more-algebra.tex:29392", "spelling", ["P02-E0495"], [op(29392, "$B$-modues", "$B$-modules")]),
    ("MORE-ALGEBRA-I-028", "more-algebra.tex:29596-29598", "undefined_resolution_complex", ["P02-E0500"], [
        op(29596, "\\Hom_A(F^{-p + 1}, M)", "\\Hom_A(P^{-p + 1}, M)"),
        op(29597, "\\Hom_A(F^{-p}, M)", "\\Hom_A(P^{-p}, M)"),
        op(29598, "\\Hom_A(F^{-p - 1}, M)", "\\Hom_A(P^{-p - 1}, M)"),
    ]),
    ("MORE-ALGEBRA-I-031", "more-algebra.tex:29746", "wrong_participle", ["P02-E0503"], [op(29746, "can also been seen", "can also be seen")]),
    ("MORE-ALGEBRA-I-032", "more-algebra.tex:29917", "wrong_cohomology_degree", ["P02-E0505"], [op(29917, "H^2(N_2^\\bullet)", "H^i(N_2^\\bullet)")]),
    ("MORE-ALGEBRA-I-033", "more-algebra.tex:29928", "undefined_cardinality_operand", ["P02-E0506"], [op(29928, "\\max(\\kappa, |M_1^\\bullet|, |M_2^\\bullet|)", "\\max(\\kappa, |M_1^\\bullet|, |N_1^\\bullet|)")]),
    ("MORE-ALGEBRA-I-034", "more-algebra.tex:29946", "wrong_generated_subcomplex", ["P02-E0507"], [op(29946, "$F^i \\subset M_2(E, F)^i$", "$F^i \\subset N_1(E, F)^i$")]),
    ("MORE-ALGEBRA-I-035", "more-algebra.tex:29951", "wrong_generated_subcomplex_bound", ["P02-E0508"], [op(29951, "|M_2(E, F)^\\bullet| \\leq \\max(\\kappa, |M_2^\\bullet|)", "|N_1(E, F)^\\bullet| \\leq \\max(\\kappa, |M_1^\\bullet|, |N_1^\\bullet|)")]),
    ("MORE-ALGEBRA-I-036", "more-algebra.tex:29963", "wrong_cochain_index_form", ["P02-E0509"], [op(29963, "by free $A$-modules $F_i$ with $|F_i| \\leq \\kappa$", "by free $A$-modules $F^i$ with $|F^i| \\leq \\kappa$")]),
    ("MORE-ALGEBRA-I-037", "more-algebra.tex:29986;29988", "malformed_cohomology_argument", ["P02-E0510"], [
        op(29986, "$H^i(N_1(E_\\eta, F_\\eta)$", "$H^i(N_1(E_\\eta, F_\\eta)^\\bullet)$"),
        op(29988, "H^i(N_1(E_\\eta, F_\\eta)$", "H^i(N_1(E_\\eta, F_\\eta)^\\bullet)$"),
    ]),
]

LINKED_PRODUCER_IDS = {
    "MORE-ALGEBRA-I-007": ["MORE-ALGEBRA-I-007", "MORE-ALGEBRA-I-008"],
    "MORE-ALGEBRA-I-012": ["MORE-ALGEBRA-I-012", "MORE-ALGEBRA-I-013"],
    "MORE-ALGEBRA-I-015": ["MORE-ALGEBRA-I-015", "MORE-ALGEBRA-I-016"],
    "MORE-ALGEBRA-I-028": ["MORE-ALGEBRA-I-028", "MORE-ALGEBRA-I-029", "MORE-ALGEBRA-I-030"],
    "MORE-ALGEBRA-I-037": ["MORE-ALGEBRA-I-037", "MORE-ALGEBRA-I-038"],
}
OPERATION_PRODUCER_IDS = {
    ("MORE-ALGEBRA-I-007", 2): "MORE-ALGEBRA-I-008",
    ("MORE-ALGEBRA-I-012", 2): "MORE-ALGEBRA-I-013",
    ("MORE-ALGEBRA-I-015", 2): "MORE-ALGEBRA-I-016",
    ("MORE-ALGEBRA-I-028", 2): "MORE-ALGEBRA-I-029",
    ("MORE-ALGEBRA-I-028", 3): "MORE-ALGEBRA-I-030",
    ("MORE-ALGEBRA-I-037", 2): "MORE-ALGEBRA-I-038",
}

ALL_ROWS = ROWS + LEASE_I_ROWS
REJECTED = [{
    "producer_id": "MORE-ALGEBRA-I-027",
    "producer_ids": ["MORE-ALGEBRA-I-027"],
    "locus": "more-algebra.tex:29495",
    "class": "proposed_scope_extension_not_required",
    "result": "rejected_after_independent_frozen_authority_review",
    "rationale": "The lemma deliberately states the positive-degree case used downstream; the proof's p = 0 paragraph supplies an induction base and does not require widening the published statement.",
    "prior_p02_aliases": [],
    "proposed_operation": op(29495, "$p > 0$", "$p \\geq 0$"),
}]
INTENTIONALLY_ABSENT = ["MORE-ALGEBRA-I-009"]


def main() -> int:
    authority = AUTHORITY.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen more-algebra.tex identity mismatch")
    if len(ROWS) != 52 or len(LEASE_I_ROWS) != 31 or len(ALL_ROWS) != 83:
        raise AssertionError("semantic-unit partition is not exactly 52 prior plus 31 Lease-I units")
    if len({row[0] for row in ALL_ROWS}) != 83:
        raise AssertionError("accepted producer primaries are not unique")
    starts = [0] + [m.end() for m in re.finditer(b"\n", authority)]
    accepted = []
    mapped = []
    for number, (producer_id, locus, cls, aliases, operations) in enumerate(ALL_ROWS, 915):
        stable_id = f"MC-STK-ERR-{number:04d}"
        producer_ids = LINKED_PRODUCER_IDS.get(producer_id, [producer_id])
        unit_ops = []
        for index, raw in enumerate(operations, 1):
            operation_producer_id = OPERATION_PRODUCER_IDS.get((producer_id, index), producer_id)
            scope_start = starts[raw["source_start_line"] - 1]
            scope_end = starts[raw["source_end_line"]]
            old = raw["old_text"].encode()
            new = raw["replacement_text"].encode()
            scope = authority[scope_start:scope_end]
            if scope.count(old) != 1:
                raise AssertionError(f"{producer_id} OP{index}: preimage count in bounded lines is {scope.count(old)}")
            start = scope_start + scope.index(old)
            row = dict(raw)
            row.update({
                "operation_id": f"{stable_id}-OP{index}",
                "start_byte": start,
                "end_byte_exclusive": start + len(old),
                "occurrence_count_in_frozen_authority": authority.count(old),
                "old_bytes": len(old), "old_sha256": sha(old),
                "replacement_bytes": len(new), "replacement_sha256": sha(new),
            })
            unit_ops.append({**raw, "producer_id": operation_producer_id})
            mapped.append({
                "producer_id": operation_producer_id,
                "semantic_unit_producer_id": producer_id,
                "stable_id": stable_id,
                "operation_index": index,
                **row,
            })
        accepted.append({
            "producer_id": producer_id,
            "producer_ids": producer_ids,
            "stable_id": stable_id,
            "locus": locus,
            "class": cls,
            "result": "accepted_after_independent_frozen_authority_replay",
            "disposition": "Apply only the exact bounded operations listed here; P02 aliases are deduplicated evidence, not additional units.",
            "prior_p02_aliases": aliases,
            "operations": unit_ops,
        })
    if len(mapped) != 94:
        raise AssertionError("accepted operation partition is not exactly 94")
    first_loci = [min(row["start_byte"] for row in mapped if row["stable_id"] == unit["stable_id"]) for unit in accepted]
    if first_loci != sorted(first_loci):
        raise AssertionError("stable IDs do not follow physical authority-source order")
    ordered = sorted(mapped, key=lambda row: row["start_byte"])
    for left, right in zip(ordered, ordered[1:]):
        if left["end_byte_exclusive"] > right["start_byte"]:
            raise AssertionError(f"overlap: {left['operation_id']} / {right['operation_id']}")
    payload = authority
    for row in reversed(ordered):
        old = row["old_text"].encode()
        start, end = row["start_byte"], row["end_byte_exclusive"]
        if payload[start:end] != old:
            raise AssertionError(f"replay mismatch: {row['operation_id']}")
        payload = payload[:start] + row["replacement_text"].encode() + payload[end:]
    aliases = {row["producer_id"]: row["prior_p02_aliases"] for row in accepted if row["prior_p02_aliases"]}
    rejected = []
    for rejection in REJECTED:
        raw = rejection["proposed_operation"]
        scope_start = starts[raw["source_start_line"] - 1]
        scope_end = starts[raw["source_end_line"]]
        old = raw["old_text"].encode()
        new = raw["replacement_text"].encode()
        scope = authority[scope_start:scope_end]
        if scope.count(old) != 1:
            raise AssertionError(f"{rejection['producer_id']}: rejected preimage count is {scope.count(old)}")
        start = scope_start + scope.index(old)
        rejected.append({
            **{k: v for k, v in rejection.items() if k != "proposed_operation"},
            "proposed_operation": {
                **raw,
                "start_byte": start,
                "end_byte_exclusive": start + len(old),
                "old_bytes": len(old),
                "old_sha256": sha(old),
                "replacement_bytes": len(new),
                "replacement_sha256": sha(new),
                "applied": False,
            },
        })
    spec = {
        "schema": "mathematics-commons-stacks-r22-adjudication-spec/v1",
        "candidate_id": "stacks-errata-a04446e-r22",
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "authority_path": "more-algebra.tex",
        "authority_bytes": len(authority),
        "authority_sha256": AUTHORITY_SHA256,
        "stable_id_range": "MC-STK-ERR-0915..MC-STK-ERR-0997",
        "semantic_unit_count": len(accepted),
        "operation_count": len(mapped),
        "duplicate_alias_count": sum(len(v) for v in aliases.values()),
        "accepted": accepted,
        "rejected": rejected,
        "intentionally_absent_producer_ids": INTENTIONALLY_ABSENT,
        "unresolved": [],
    }
    write_json(ROOT / "R22_MORE_ALGEBRA_ADJUDICATION_SPEC.json", spec)
    write_json(ROOT / "operation-spec.input.json", {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256,
        "operation_count": len(mapped),
        "apply_order": "descending_start_byte",
        "operations": mapped,
    })
    write_json(ROOT / "stable-units.input.json", {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": COMMIT,
        "unit_count": len(accepted),
        "units": [{
            "id": row["stable_id"], "producer_id": row["producer_id"], "producer_ids": row["producer_ids"], "class": row["class"],
            "source": "more-algebra.tex", "locus": row["locus"], "payload": "payload/more-algebra.tex",
            "operation_ids": [f"{row['stable_id']}-OP{i}" for i in range(1, len(row["operations"]) + 1)],
            "prior_p02_aliases": row["prior_p02_aliases"], "status": "provisional_accepted_not_materialized",
        } for row in accepted],
    })
    source_rows = []
    by_id = {row["stable_id"]: row for row in accepted}
    for stable_id in [row["stable_id"] for row in accepted]:
        unit = by_id[stable_id]
        source_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id, "producer_id": unit["producer_id"], "producer_ids": unit["producer_ids"], "source": "more-algebra.tex",
            "authority": "authority/source/more-algebra.tex", "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/more-algebra.tex", "locus": unit["locus"], "class": unit["class"],
            "proof": unit["result"], "prior_p02_aliases": unit["prior_p02_aliases"],
            "adverse_evidence": "Producer and P02 records are allegation evidence only; exact frozen-authority replay is controlling.",
            "operations": [{k: v for k, v in row.items() if k not in {"semantic_unit_producer_id", "stable_id", "operation_index"}}
                           for row in mapped if row["stable_id"] == stable_id],
        })
    (ROOT / "source-map.input.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in source_rows), encoding="utf-8", newline="")
    decisions = [
        ("ERR-R22-D0001", "Bind R22 to the active errata/r22 lease and frozen more-algebra.tex authority.", "Preserves the immutable authority and single-writer boundary."),
        ("ERR-R22-D0002", "Assign MC-STK-ERR-0915..0997 to the 83 accepted producer units in physical source order.", "Preserves the frozen 0915..0966 assignments and extends them contiguously through the 31 accepted Lease-I units; late producer row I-039 is placed by its earlier physical locus."),
        ("ERR-R22-D0003", "Collapse repeated P02 candidate records into prior_p02_aliases on their corresponding R22 semantic unit.", "Sidecar rediscovery does not create a second defect or consume a second stable ID."),
        ("ERR-R22-D0004", "Delete only the unresolved placeholder parentheticals for MORE-ALGEBRA-001 and prior E-lease row MORE-ALGEBRA-009; invent no cross-reference.", "This removes reader-facing editorial debris without fabricating an unsupported destination and is distinct from intentionally absent MORE-ALGEBRA-I-009."),
        ("ERR-R22-D0005", "Apply 94 exact, bounded, nonoverlapping UTF-8 operations in descending byte order.", "This includes the earlier D/E/F/G refinements plus 37 exact Lease-I operations, including the normalized I-004, I-025, and I-035 replacements."),
        ("ERR-R22-D0006", "Leave build, render, admission, registry, Git, and publication transitions unexecuted.", "This artifact is the requested non-build candidate intake skeleton only."),
        ("ERR-R22-D0007", "Merge the five linked Lease-I producer groups into one canon unit each and collapse each accepted unit to its exact P02 alias.", "The linked rows describe repeated loci of one semantic defect and therefore do not consume additional canon IDs."),
        ("ERR-R22-D0008", "Reject MORE-ALGEBRA-I-027 without assigning a stable ID; record MORE-ALGEBRA-I-009 as intentionally absent.", "The positive-degree statement need not be widened merely because the proof supplies a degree-zero induction base, and no I-009 allegation exists to adjudicate."),
    ]
    (ROOT / "decisions.input.jsonl").write_text("".join(json.dumps({"schema":"mathematics-commons-stacks-candidate-decision/v1","id":i,"timestamp_utc":GENERATED_AT,"choice":c,"rationale":r,"supersedes":None}, separators=(",", ":")) + "\n" for i,c,r in decisions), encoding="utf-8", newline="")
    (ROOT / "rejections.input.jsonl").write_text("".join(json.dumps({
        "schema": "mathematics-commons-stacks-errata-rejection/v1",
        **row,
    }, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rejected), encoding="utf-8", newline="")
    write_json(ROOT / "unresolved-intake.json", {"schema":"mathematics-commons-stacks-unresolved-intake/v1","candidate_id":"stacks-errata-a04446e-r22","count":0,"items":[]})
    write_json(ROOT / "candidate.config.input.json", {
        "schema": "mathematics-commons-stacks-errata-candidate-config-input/v1",
        "candidate_id": "stacks-errata-a04446e-r22", "lease_id": "stacks-lease-000025-errata-r22",
        "writer_task": "01a0256d-5693-77c1-96b2-cf37101e0c6c", "namespace": "commons/stacks/errata/r22",
        "authority_commit": COMMIT, "authority_tree": TREE,
        "expected_unit_ids": [f"MC-STK-ERR-{n:04d}" for n in range(915, 998)],
        "expected_producer_ids": [row["producer_id"] for row in accepted],
        "expected_all_producer_ids": [producer_id for row in accepted for producer_id in row["producer_ids"]],
        "intentionally_absent_producer_ids": INTENTIONALLY_ABSENT,
        "operation_count": len(mapped), "accepted": len(accepted), "rejected": len(rejected), "unresolved": 0,
        "payload_expected_bytes": len(payload), "payload_expected_sha256": sha(payload),
        "build_render_admission_status": "not_run_by_intake_skeleton",
    })
    write_json(ROOT / "INTAKE_VALIDATION.json", {
        "schema": "mathematics-commons-stacks-r22-intake-validation/v1", "status": "PASS",
        "authority_bytes": len(authority), "authority_sha256": sha(authority),
        "semantic_units": len(accepted), "operations": len(mapped), "stable_ids_unique": True,
        "stable_ids_follow_physical_source_order": True,
        "stable_id_first": "MC-STK-ERR-0915", "stable_id_last": "MC-STK-ERR-0997",
        "bounded_preimages_unique": True, "operations_nonoverlapping": True,
        "payload_preview_bytes": len(payload), "payload_preview_sha256": sha(payload),
        "p02_aliases_collapsed": aliases,
        "rejected_preimages_validated": len(rejected),
        "intentionally_absent_producer_ids": INTENTIONALLY_ABSENT,
        "unresolved": 0,
        "prohibited_transitions_executed": [],
    })
    review = (
        "# R22 More Algebra intake review\n\n"
        "This non-build skeleton independently binds 83 accepted semantic units and 94 exact operations to frozen `more-algebra.tex`. "
        "P02 rediscoveries are aliases only. The two unresolved-reference placeholders are deleted without inventing targets. "
        "The exact discrepancy resolutions are: all three `M_b` loci are repaired; only `I^{c2c3}` on line 22705 is changed; "
        "line 22965 changes `of` to `if`; and the E/F prose and delimiter operations use the bounded refinements recorded in the adjudication spec. "
        "Lease I adds 31 accepted units with 37 operations, merges five linked producer groups, rejects I-027 without an ID, "
        "and records I-009 as intentionally absent. The normalized Lease-I wording and formulas for I-004, I-025, and I-035 are exact.\n\n"
        "No TeX build, render, registry admission, commit, push, or publication has been performed.\n"
    )
    (ROOT / "R22_MORE_ALGEBRA_REVIEW.md").write_text(review, encoding="utf-8", newline="")
    print(json.dumps({"passed": True, "units": len(accepted), "operations": len(mapped), "payload_sha256": sha(payload)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
