from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R10_ALG_372_381_ADJUDICATION_SPEC.json"


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
    unit(372, 715, "zero_localization_outside_n2_domain", "45748-45751",
         "Restrict the localization claim to f_i outside the prime and state that the surviving images generate the unit ideal.",
         "confirmed_definition_domain_error", [
        op(45748, 45751,
           "$\\mathfrak p \\subset R$ is a prime, then we see each\n"
           "$R_{f_i}/\\mathfrak pR_{f_i} = (R/\\mathfrak p)_{f_i}$ is N-2\n"
           "and hence we conclude $R/\\mathfrak p$ is N-2 by\n"
           "Lemma \\ref{lemma-Japanese-local}. This proves (2).",
           "$\\mathfrak p \\subset R$ is a prime, then for every $i$ such that\n"
           "$f_i \\not \\in \\mathfrak p$ we see\n"
           "$R_{f_i}/\\mathfrak pR_{f_i} = (R/\\mathfrak p)_{f_i}$ is N-2.\n"
           "The images of these $f_i$ in $R/\\mathfrak p$ generate the unit ideal, and\n"
           "hence we conclude $R/\\mathfrak p$ is N-2 by\n"
           "Lemma \\ref{lemma-Japanese-local}. This proves (2)."),
    ]),
    unit(373, 716, "article_agreement", "45877",
         "Correct the indefinite article before R-completion-submodule.",
         "confirmed_grammar_error", [
        op(45877, 45877, "is a $R^\\wedge$-submodule", "is an $R^\\wedge$-submodule"),
    ]),
    unit(374, 717, "rescaling_fails_at_closed_prime", "46042-46051",
         "Split off the field case and rescale every generator by one fixed element of m outside p.",
         "confirmed_proof_gap", [
        op(46042, 46043,
           "To prove (1) we have to show that the integral closure of $R/\\mathfrak p$\n"
           "is finite over $R/\\mathfrak p$. Choose $x_1, \\ldots, x_n \\in L$",
           "To prove (1) we have to show that the integral closure of $R/\\mathfrak p$\n"
           "is finite over $R/\\mathfrak p$. If $\\mathfrak p = \\mathfrak m$, then\n"
           "$R/\\mathfrak p$ is a field and the assertion is immediate. Thus we may\n"
           "assume $\\mathfrak p \\not = \\mathfrak m$ and choose\n"
           "$g \\in \\mathfrak m \\setminus \\mathfrak p$. Choose $x_1, \\ldots, x_n \\in L$"),
        op(46049, 46051,
           "$a_{i, j} \\in R/\\mathfrak p$. In fact, after further multiplying\n"
           "by elements of $\\mathfrak m$, we may assume\n"
           "$a_{i, j} \\in \\mathfrak m/\\mathfrak p \\subset R/\\mathfrak p$ for all $i, j$.",
           "$a_{i, j} \\in R/\\mathfrak p$. After further replacing each $x_i$\n"
           "by $g x_i$, we may assume\n"
           "$a_{i, j} \\in \\mathfrak m/\\mathfrak p \\subset R/\\mathfrak p$ for all $i, j$."),
    ]),
    unit(375, 718, "unjustified_normality_restriction", "46110",
         "Remove normal from the arbitrary Nagata-domain reduction.",
         "confirmed_logical_restriction_error", [
        op(46110, 46110, "Step 4. Let $R$ be a normal Nagata domain and", "Step 4. Let $R$ be a Nagata domain and"),
    ]),
    unit(376, 719, "missing_subject", "46143",
         "Insert the missing subject in the localization reduction.",
         "confirmed_grammar_error", [
        op(46143, 46143, "and $S$ by $S_a$, may assume", "and $S$ by $S_a$, we may assume"),
    ]),
    unit(377, 720, "wrong_polynomial_indeterminate", "46144",
         "Use R[X] for the polynomial indeterminate.",
         "confirmed_notation_error", [
        op(46144, 46144, "in $R[x]$ with", "in $R[X]$ with"),
    ]),
    unit(378, 721, "overbroad_maximal_ideal_quantifier", "46152-46154",
         "Restrict to maximal ideals of S' lying over the fixed maximal ideal.",
         "confirmed_quantifier_error", [
        op(46152, 46154,
           "Moreover, $S'$ is finite over $S$. If for every maximal ideal\n"
           "$\\mathfrak m'$ of $S'$ the local ring $S'_{\\mathfrak m'}$ is\n"
           "N-1, then $S'_{\\mathfrak m}$ is N-1 by",
           "Moreover, $S'$ is finite over $S$. If for every maximal ideal\n"
           "$\\mathfrak m'$ of $S'$ lying over $\\mathfrak m$ the local ring\n"
           "$S'_{\\mathfrak m'}$ is N-1, then $S'_{\\mathfrak m}$ is N-1 by"),
    ]),
    unit(379, 722, "missing_zero_branch", "46170",
         "Dispose of x=0 before invoking the nonzero-element criterion.",
         "confirmed_missing_case", [
        op(46170, 46170,
           "We have to show $S_{\\mathfrak m}$ is N-1.",
           "We have to show $S_{\\mathfrak m}$ is N-1. If $x = 0$, then $S = R$\n"
           "and there is nothing to prove. Thus we may and do assume $x \\not = 0$."),
    ]),
    unit(380, 723, "missing_plus_sign", "46185",
         "Insert the missing plus sign after the polynomial ellipsis.",
         "confirmed_formula_typo", [
        op(46185, 46185, "+ \\ldots a_1 X +", "+ \\ldots + a_1 X +"),
    ]),
    unit(381, 724, "unstated_locality_and_topology_agreement", "46280",
         "Prove B is local and that its maximal-adic and mB-adic topologies agree before applying the completion lemma.",
         "confirmed_proof_gap", [
        op(46280, 46280,
           "$B = A[x]/(x^p - a)$ is a domain because $K[x]/(x^p - a)$ is a field.",
           "$B = A[x]/(x^p - a)$ is a domain because $K[x]/(x^p - a)$ is a field.\n"
           "The ring $B$ is local because its special fibre\n"
           "$B/\\mathfrak mB = \\kappa(\\mathfrak m)[x]/(x^p - \\overline{a})$ has a unique\n"
           "prime ideal. Moreover, the maximal-adic and $\\mathfrak mB$-adic topologies\n"
           "on $B$ agree."),
    ]),
]


SPEC = {
    "schema": "mathematics-commons-stacks-r10-adjudication-spec/v1",
    "candidate_id": "stacks-errata-a04446e-r10",
    "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
    "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
    "authority_sha256": "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3",
    "accepted": ACCEPTED,
    "rejected": [],
}


if __name__ == "__main__":
    if OUT.exists():
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(SPEC, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8", newline="")
    print(json.dumps({"accepted": len(ACCEPTED), "path": str(OUT)}))
