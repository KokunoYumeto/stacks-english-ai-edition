from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R9_ALG_342_371_ADJUDICATION_SPEC.json"


def op(start: int, end: int, old: str, new: str) -> dict:
    return {
        "source_start_line": start,
        "source_end_line": end,
        "old_text": old,
        "replacement_text": new,
    }


def unit(producer: int, stable: int, classification: str, locus: str,
         disposition: str, result: str, operations: list[dict]) -> dict:
    return {
        "producer_id": f"ALGEBRA-{producer}",
        "stable_id": f"MC-STK-ERR-{stable:04d}",
        "class": classification,
        "locus": f"algebra.tex:{locus}",
        "disposition": disposition,
        "result": result,
        "operations": operations,
    }


ACCEPTED = [
    unit(342, 686, "inconsistent_component_order", "44590;44607;44617",
         "Normalize the two reversed category-object triples to the declared field-first order.",
         "confirmed_notation_error", [
        op(44607, 44607,
           "$((R_i, k_i, \\phi_i), \\psi_{ii'})$ is a system over $I$, see",
           "$((k_i, R_i, \\phi_i), \\psi_{ii'})$ is a system over $I$, see"),
        op(44617, 44617, "$(R', k', \\phi')$ is an", "$(k', R', \\phi')$ is an"),
    ]),
    unit(343, 687, "missing_r_algebra_compatibility", "44595-44603",
         "Require transition morphisms to be R-algebra maps so the colimit R-structure and flatness claim are defined.",
         "confirmed_type_and_proof_gap", [
        op(44596, 44596,
           "given by ring maps $\\psi : R_1 \\to R_2$ such that",
           "given by $R$-algebra maps $\\psi : R_1 \\to R_2$ such that"),
    ]),
    unit(345, 688, "missing_base_field_in_generated_subfield", "44625-44629",
         "Define K(x) as the subfield generated over k by the initial segment.",
         "confirmed_definition_gap", [
        op(44625, 44626,
           "For $x \\in K$ we let $K(x)$ be the subfield of $K$ generated\n"
           "by all elements of $K$ which are $\\leq x$.",
           "For $x \\in K$ we let $K(x)$ be the subfield of $K$ generated\n"
           "over $k$ by all elements of $K$ which are $\\leq x$."),
    ]),
    unit(346, 689, "polynomial_ring_notation_for_field_adjunction", "44631;44637",
         "Use field-adjunction parentheses at both loci.",
         "confirmed_notation_error", [
        op(44631, 44631,
           "Namely, if $x$ has a predecessor $x'$, then $K(x) = K(x')[x]$",
           "Namely, if $x$ has a predecessor $x'$, then $K(x) = K(x')(x)$"),
        op(44637, 44637,
           "Since $K(x) = K'(x)[x]$ we see that we can use the construction of the",
           "Since $K(x) = K'(x)(x)$ we see that we can use the construction of the"),
    ]),
    unit(347, 690, "missing_least_element_base_case", "44634-44638",
         "Initialize the least-element branch with R'(x)=R and K'(x)=k before using the nonleast limit construction.",
         "confirmed_base_case_gap", [
        op(44633, 44636,
           "If $x$ does not\n"
           "have a predecessor, then we first set\n"
           "$R'(x) = \\colim_{x' < x} R(x')$ as in the third paragraph\n"
           "of the proof. The residue field of $R'(x)$ is $K'(x) = \\bigcup_{x' < x} K(x')$.",
           "If $x$ does not\n"
           "have a predecessor, then we set $R'(x) = R$ and $K'(x) = k$\n"
           "if $x$ is the least element. Otherwise, we set\n"
           "$R'(x) = \\colim_{x' < x} R(x')$ as in the third paragraph\n"
           "of the proof. In this case the residue field of $R'(x)$ is\n"
           "$K'(x) = \\bigcup_{x' < x} K(x')$."),
    ]),
    unit(348, 691, "missing_terminal_colimit", "44624-44639;44652-44656",
         "Choose the well-order with a greatest element and identify its constructed ring as the required extension with residue field K.",
         "confirmed_terminal_construction_gap", [
        op(44624, 44624,
           "To get around this problem we choose a well ordering on $K$.",
           "To get around this problem we choose a well ordering on $K$ with a greatest\n"
           "element."),
        op(44638, 44639,
           "first paragraph of the proof to produce $R'(x) \\subset R(x)$.\n"
           "This finishes the proof of the lemma.",
           "first paragraph of the proof to produce $R'(x) \\subset R(x)$.\n"
           "For the greatest element $x$ of the chosen ordering we have $K(x) = K$.\n"
           "Thus $R(x)$ is the extension required by the lemma."),
    ]),
    unit(349, 692, "omitted_locality_descent", "44661-44671",
         "Prove locality of the descended finite-etale algebra and every later base change by faithfully flat descent.",
         "confirmed_proof_gap", [
        op(44664, 44667,
           "there exists an $i$ and a finite \\'etale extension $R_i \\to R_{i, 1}$\n"
           "such that $R_{\\alpha + 1} = R_\\alpha \\otimes_{R_i} R_{i, 1}$.\n"
           "Thus $R_{\\alpha + 1} = \\colim_{i' \\geq i} R_{i'} \\otimes_{R_i} R_{i, 1}$\n"
           "and the result holds for $\\alpha + 1$. Suppose $\\alpha$ is not a successor",
           "there exists an $i$ and a finite \\'etale extension $R_i \\to R_{i, 1}$\n"
           "such that $R_{\\alpha + 1} = R_\\alpha \\otimes_{R_i} R_{i, 1}$.\n"
           "The map $R_i \\to R_\\alpha$ is flat local, hence faithfully flat. Since\n"
           "$R_{\\alpha + 1}$ is the base change of $R_{i, 1}$, faithfully flat\n"
           "descent of locality shows that $R_{i, 1}$ is local. More generally,\n"
           "for every $i' \\geq i$, the map $R_{i'} \\to R_\\alpha$ is flat local,\n"
           "hence faithfully flat, and the base change of\n"
           "$R_{i'} \\otimes_{R_i} R_{i, 1}$ to $R_\\alpha$ is $R_{\\alpha + 1}$.\n"
           "Hence all these rings are local, and\n"
           "$R_{\\alpha + 1} = \\colim_{i' \\geq i} R_{i'} \\otimes_{R_i} R_{i, 1}$.\n"
           "Thus the result holds for $\\alpha + 1$. Suppose $\\alpha$ is not a successor"),
    ]),
    unit(350, 693, "malformed_logical_coordination", "44669-44671",
         "Remove the malformed and after the Since-clause and insert the needed comma.",
         "confirmed_grammar_error", [
        op(44670, 44670,
           "for some $\\beta < \\alpha$ and we see that $E$ is contained in a finite \\'etale",
           "for some $\\beta < \\alpha$, we see that $E$ is contained in a finite \\'etale"),
    ]),
    unit(351, 694, "wrong_induction_preposition", "44685",
         "Change induction of the degree to induction on the degree.",
         "confirmed_grammar_error", [
        op(44685, 44685,
           "By induction of the degree of $\\kappa(\\mathfrak p) \\subset L$.",
           "By induction on the degree of $\\kappa(\\mathfrak p) \\subset L$."),
    ]),
    unit(352, 695, "nondecreasing_induction_and_grammar", "44687-44691",
         "Require a proper nontrivial intermediate field and replace then construction by then constructing.",
         "confirmed_induction_gap_and_grammar_error", [
        op(44687, 44691,
           "In general, if there exists a sub extension\n"
           "$\\kappa(\\mathfrak p) \\subset L' \\subset L$ then we win by induction\n"
           "on the degree (by first constructing $R \\subset S'$ corresponding\n"
           "to $L'/\\kappa(\\mathfrak p)$ and then construction $S' \\subset S$\n"
           "corresponding to $L/L'$). Thus we may assume that",
           "In general, if there exists a sub extension\n"
           "$\\kappa(\\mathfrak p) \\subset L' \\subset L$ with both inclusions strict,\n"
           "then we win by induction\n"
           "on the degree (by first constructing $R \\subset S'$ corresponding\n"
           "to $L'/\\kappa(\\mathfrak p)$ and then constructing $S' \\subset S$\n"
           "corresponding to $L/L'$). Thus we may assume that"),
    ]),
    unit(353, 696, "typographical_error", "44748",
         "Correct choicse to choices.", "confirmed_typographical_error", [
        op(44748, 44748,
           "Given these choicse, we let $E_{k + 1} \\subset B$ be the $A$-subalgebra",
           "Given these choices, we let $E_{k + 1} \\subset B$ be the $A$-subalgebra"),
    ]),
    unit(354, 697, "malformed_cardinality_phrase", "44755-44756",
         "Change has at most cardinality to has cardinality at most.",
         "confirmed_grammar_error", [
        op(44755, 44756,
           "Some set theory (omitted) shows that $E_{k + 1}$ has at most\n"
           "cardinality $\\kappa$ (this uses that we inductively know",
           "Some set theory (omitted) shows that $E_{k + 1}$ has cardinality\n"
           "at most $\\kappa$ (this uses that we inductively know"),
    ]),
    unit(355, 698, "zero_ring_counterexample_to_quotient_claim", "44813",
         "Restrict the assertion to quotients by proper ideals.",
         "confirmed_scope_error", [
        op(44813, 44813,
           "Any quotient of $R$ is also a Noetherian complete local ring.",
           "Any quotient of $R$ by a proper ideal is also a Noetherian complete local ring."),
    ]),
    unit(356, 699, "malformed_given_then_construction", "44814",
         "Delete then from the malformed Given construction.",
         "confirmed_grammar_error", [
        op(44814, 44814,
           "Given a finite ring map $R \\to S$, then $S$ is a product of",
           "Given a finite ring map $R \\to S$, $S$ is a product of"),
    ]),
    unit(357, 700, "missing_copula", "44873-44874",
         "State explicitly that the uniformizer p is a prime number.",
         "confirmed_grammar_error", [
        op(44873, 44874,
           "A {\\it Cohen ring} is a complete discrete valuation ring with\n"
           "uniformizer $p$ a prime number.",
           "A {\\it Cohen ring} is a complete discrete valuation ring whose\n"
           "uniformizer $p$ is a prime number."),
    ]),
    unit(358, 701, "ill_typed_arrow_label", "44994",
         "Declare the overloaded notation for reduction modulo p^(n-1) followed by phi_(n-1).",
         "confirmed_type_error", [
        op(44985, 44986,
           "for $n = 1$. If $n > 1$, let $\\varphi_{n - 1}$ be given.\n"
           "The ring map $\\mathbf{Z}/p^n\\mathbf{Z} \\to \\Lambda/p^n\\Lambda$",
           "for $n = 1$. If $n > 1$, let $\\varphi_{n - 1}$ be given, and also\n"
           "write $\\varphi_{n - 1}$ for the composite\n"
           "$\\Lambda/p^n\\Lambda \\to \\Lambda/p^{n - 1}\\Lambda\n"
           "\\xrightarrow{\\varphi_{n - 1}} R/\\mathfrak m^{n - 1}$.\n"
           "The ring map $\\mathbf{Z}/p^n\\mathbf{Z} \\to \\Lambda/p^n\\Lambda$"),
    ]),
    unit(359, 702, "mismatched_adic_ideals", "45016-45019",
         "Name the respective source (x_i)-adic and target (y_i)-adic ideals.",
         "confirmed_notation_and_proof_gap", [
        op(45016, 45019,
           "Since both sides are $(x_1, \\ldots, x_n)$-adically complete\n"
           "this map is surjective by Lemma \\ref{lemma-completion-generalities}\n"
           "as it is surjective modulo $(x_1, \\ldots, x_n)$ by\n"
           "construction.",
           "Since the source and target are complete with respect to the ideals\n"
           "$(x_1, \\ldots, x_n)$ and $(y_1, \\ldots, y_n) = \\mathfrak m$,\n"
           "respectively, this map is surjective by\n"
           "Lemma \\ref{lemma-completion-generalities} as the induced map modulo\n"
           "these respective ideals is surjective by construction."),
    ]),
    unit(360, 703, "missing_head_noun", "45067",
         "Insert subring before R_0.", "confirmed_grammar_error", [
        op(45067, 45067,
           "Then there exists a $R_0 \\subset R$ with the following properties",
           "Then there exists a subring $R_0 \\subset R$ with the following properties"),
    ]),
    unit(361, 704, "premature_proof_closure", "45099-45102",
         "Replace the premature whole-lemma closure by This proves Case I.",
         "confirmed_proof_structure_error", [
        op(45098, 45102,
           "$R_0 \\to R$ is injective (see Lemma \\ref{lemma-integral-dim-up}),\n"
           "and the lemma is proved.\n\n"
           "\\medskip\\noindent\n"
           "Case II: $\\Lambda$ is a Cohen ring. Let $d + 1 = \\dim(R)$.",
           "$R_0 \\to R$ is injective (see Lemma \\ref{lemma-integral-dim-up}).\n"
           "This proves Case I.\n\n"
           "\\medskip\\noindent\n"
           "Case II: $\\Lambda$ is a Cohen ring. Let $d + 1 = \\dim(R)$."),
    ]),
    unit(362, 705, "ambiguous_footnote_attachment", "44799-44802",
         "Split the finite-generation and Noetherian-completion assertions.",
         "confirmed_editorial_ambiguity", [
        op(44799, 44802,
           "This does not happen when $\\mathfrak m$ is finitely generated, see\n"
           "Lemma \\ref{lemma-hathat-finitely-generated} in which\n"
           "case the completion is Noetherian, see\n"
           "Lemma \\ref{lemma-completion-Noetherian}.}.",
           "This does not happen when $\\mathfrak m$ is finitely generated; see\n"
           "Lemma \\ref{lemma-hathat-finitely-generated}. In this\n"
           "case the completion is Noetherian; see\n"
           "Lemma \\ref{lemma-completion-Noetherian}.}."),
    ]),
    unit(363, 706, "malformed_invariant_subfield_apposition", "45311-45312",
         "Identify L^G as the invariant subfield of L with a grammatical apposition.",
         "confirmed_grammar_error", [
        op(45311, 45312,
           "with fraction field $K = L^G$ the $G$-invariants in the fraction field\n"
           "$L$ of $A$.",
           "with fraction field $K = L^G$, the subfield of $G$-invariants in the\n"
           "fraction field $L$ of $A$."),
    ]),
    unit(364, 707, "unstated_fraction_field_extension_of_derivation", "45325-45326",
         "State that the unique extension of D to the fraction field satisfies D(a) nonzero.",
         "confirmed_type_gap", [
        op(45325, 45326,
           "Let $a \\in K$ be an element such that there exists a derivation\n"
           "$D : R \\to R$ with $D(a) \\not = 0$. Then the integral closure",
           "Let $a \\in K$ be an element such that there exists a derivation\n"
           "$D : R \\to R$ whose unique extension to the fraction field satisfies\n"
           "$D(a) \\not = 0$. Then the integral closure"),
    ]),
    unit(365, 708, "omitted_normality_argument", "45364-45366",
         "State that the integral difference lies in the fraction field and hence in R by normality.",
         "confirmed_proof_gap", [
        op(45364, 45366,
           "Hence $D(a)^{i + 1}a_0$ is also in $R$ because it is the\n"
           "difference of $D(a)^{i + 1}y$ and $\\sum_{j > 0} D(a)^{i + 1}a_jx^j$ which\n"
           "are integral over $R$ (since $x$ is integral over $R$ as $a \\in R$).",
           "Hence $D(a)^{i + 1}a_0$ is also in $R$: it is the\n"
           "difference of $D(a)^{i + 1}y$ and $\\sum_{j > 0} D(a)^{i + 1}a_jx^j$, both\n"
           "of which are integral over $R$ (since $x$ is integral over $R$ as\n"
           "$a \\in R$). Their difference also lies in the fraction field, so\n"
           "normality shows that it belongs to the ring."),
    ]),
    unit(366, 709, "mis_scoped_purely_inseparable_extension", "45429-45431",
         "Quantify the finite purely inseparable field extension and its integral closure unambiguously.",
         "confirmed_scope_error", [
        op(45429, 45431,
           "In characteristic $p > 0$ we have to show that the integral\n"
           "closure of $R[x]$ is finite in any finite purely inseparable extension\n"
           "of $L/K(x)$ where $K$ is the fraction field of $R$. There",
           "In characteristic $p > 0$ we have to show that the integral\n"
           "closure of $R[x]$ in every finite purely inseparable field extension\n"
           "$L/K(x)$ is finite, where $K$ is the fraction field of $R$. There"),
    ]),
    unit(367, 710, "missing_relative_clause", "45435-45437",
         "Introduce the integral closure R' with an explicit relative clause.",
         "confirmed_grammar_error", [
        op(45436, 45437,
           "is equal to $R'[x^{1/q}]$ with $R \\subset R' \\subset L'$ the integral\n"
           "closure of $R$ in $L'$.",
           "is equal to $R'[x^{1/q}]$ with $R \\subset R' \\subset L'$, where the middle\n"
           "ring is the integral closure of $R$ in $L'$."),
    ]),
    unit(368, 711, "wrong_alternative_connective", "45458-45464",
         "Join the two Serre-criterion alternatives with or.",
         "confirmed_logical_connective_error", [
        op(45460, 45462,
           "\\item Case I: $\\text{depth}(R_{\\mathfrak q}) < 2$\n"
           "and $\\dim(R_{\\mathfrak q}) \\geq 2$, and\n"
           "\\item Case II: $R_{\\mathfrak q}$ is not regular",
           "\\item Case I: $\\text{depth}(R_{\\mathfrak q}) < 2$\n"
           "and $\\dim(R_{\\mathfrak q}) \\geq 2$, or\n"
           "\\item Case II: $R_{\\mathfrak q}$ is not regular"),
    ]),
    unit(369, 712, "malformed_denote_construction", "45509",
         "Repair the denote construction.", "confirmed_grammar_error", [
        op(45509, 45509,
           "For such a ring $R'$ denote $Z_{R'} \\subset \\Spec(R)$ this image.",
           "For such a ring $R'$, denote this image by $Z_{R'} \\subset \\Spec(R)$."),
    ]),
    unit(370, 713, "omitted_contraction_and_normality_localization_argument", "45523-45529",
         "Define the contractions and use an intermediate localization to justify the normality equality safely.",
         "confirmed_proof_gap", [
        op(45527, 45529,
           "Namely, every prime $\\mathfrak p'$ lies over a prime $\\mathfrak p'_i$\n"
           "such that $(R'_i)_{\\mathfrak p'_i}$ is normal. This implies\n"
           "that $R'_{\\mathfrak p'} = (R'_i)_{\\mathfrak p'_i}$ is normal too.",
           "Namely, let $\\mathfrak p' \\in \\Spec(R')$ and set\n"
           "$\\mathfrak p = \\mathfrak p' \\cap R$. Choose $i$ such that\n"
           "$\\mathfrak p \\not \\in Z_{R'_i}$ and set\n"
           "$\\mathfrak p'_i = \\mathfrak p' \\cap R'_i$. Then\n"
           "$(R'_i)_{\\mathfrak p'_i}$ is normal. Set\n"
           "$T = R'_i \\setminus \\mathfrak p'_i$. The extension\n"
           "$R'_i \\subset R'$ is integral, and hence $T^{-1}R'$ is integral over\n"
           "$(R'_i)_{\\mathfrak p'_i}$. Both rings are contained in $K$, the fraction\n"
           "field of $(R'_i)_{\\mathfrak p'_i}$, so normality gives\n"
           "$T^{-1}R' = (R'_i)_{\\mathfrak p'_i}$. Localizing at $\\mathfrak p'$ gives\n"
           "$R'_{\\mathfrak p'} = (R'_i)_{\\mathfrak p'_i}$, which is normal."),
    ]),
    unit(371, 714, "omitted_reduction_after_field_enlargement", "45561-45563",
         "Justify reduction from the enlarged purely inseparable field back to the original normalization.",
         "confirmed_proof_gap", [
        op(45562, 45563,
           "By enlarging $L$ if necessary we may assume there exists\n"
           "an element $y \\in L$ such that $y^q = x$.",
           "Choose a $q$th root $y$ of $x$ in an algebraic closure of $K$, set\n"
           "$\\widetilde L = L(y)$, and let $\\widetilde S$ be the integral closure\n"
           "of $R$ in $\\widetilde L$. Then $\\widetilde L/K$ is a finite purely\n"
           "inseparable extension and $\\widetilde L^q \\subset K$. Moreover,\n"
           "$S = \\widetilde S \\cap L$, so $S$ is an $R$-submodule of $\\widetilde S$.\n"
           "Thus, if $\\widetilde S$ is finite over $R$, then $S$ is finite over $R$\n"
           "because $R$ is Noetherian. Replacing $L$ by $\\widetilde L$ and $S$ by\n"
           "$\\widetilde S$, we may therefore assume that $y \\in L$ and $y^q = x$."),
    ]),
]


SPEC = {
    "schema": "mathematics-commons-stacks-r9-adjudication-spec/v1",
    "candidate_id": "stacks-errata-a04446e-r9",
    "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
    "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
    "authority_sha256": "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3",
    "accepted": ACCEPTED,
    "rejected": [{
        "producer_id": "ALGEBRA-344",
        "reason": "In the explicitly informal counterfactual sentence, was is acceptable contemporary usage; were would be optional register polishing rather than a source correction.",
    }],
}


if __name__ == "__main__":
    if OUT.exists():
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(SPEC, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8", newline="")
    print(json.dumps({"accepted": len(ACCEPTED), "path": str(OUT)}))
