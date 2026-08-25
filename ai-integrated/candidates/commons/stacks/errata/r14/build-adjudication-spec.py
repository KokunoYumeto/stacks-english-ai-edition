from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R14_ALG_395_402_ADJUDICATION_SPEC.json"
SPEC = {
    "schema": "mathematics-commons-stacks-r14-adjudication-spec/v1",
    "candidate_id": "stacks-errata-a04446e-r14",
    "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
    "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
    "authority_sha256": "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3",
    "accepted": [
        {
            "producer_id": "ALGEBRA-395",
            "stable_id": "MC-STK-ERR-0738",
            "class": "incorrect_colimit_field_identity",
            "locus": "algebra.tex:47214",
            "disposition": "The finite extension is chosen so that k-prime is the scalar extension of k, not so that k_i equals that scalar extension.",
            "result": "confirmed_mathematical_identity_error",
            "operations": [{
                "source_start_line": 47214,
                "source_end_line": 47214,
                "old_text": "$k_i = k \\otimes_{k_i} k_i'$",
                "replacement_text": "$k' = k \\otimes_{k_i} k_i'$",
            }],
        },
        {
            "producer_id": "ALGEBRA-396",
            "stable_id": "MC-STK-ERR-0739",
            "class": "determiner_number_agreement",
            "locus": "algebra.tex:47344",
            "disposition": "Remove the singular article before the plural noun phrase ring maps.",
            "result": "confirmed_grammar_error",
            "operations": [{
                "source_start_line": 47344,
                "source_end_line": 47344,
                "old_text": "together with a ring maps",
                "replacement_text": "together with ring maps",
            }],
        },
        {
            "producer_id": "ALGEBRA-397",
            "stable_id": "MC-STK-ERR-0740",
            "class": "malformed_flat_locus_sentence",
            "locus": "algebra.tex:47394-47396",
            "disposition": "State the openness theorem as the set of primes at which M_lambda is flat being open.",
            "result": "confirmed_omitted_words_error",
            "operations": [{
                "source_start_line": 47394,
                "source_end_line": 47396,
                "old_text": "By Theorem \\ref{theorem-openness-flatness} we get an open subset\n$U_\\lambda \\subset \\Spec(S_\\lambda)$ such that $M_\\lambda$\nflat over $R_\\lambda$ at all the primes of $U_\\lambda$.",
                "replacement_text": "By Theorem \\ref{theorem-openness-flatness}, the set\n$U_\\lambda \\subset \\Spec(S_\\lambda)$ of primes at which $M_\\lambda$\nis flat over $R_\\lambda$ is open.",
            }],
        },
        {
            "producer_id": "ALGEBRA-398",
            "stable_id": "MC-STK-ERR-0741",
            "class": "inconsistent_index_bound",
            "locus": "algebra.tex:47410",
            "disposition": "Index the chosen s_i by the same bound r as the f_i appearing in the sum.",
            "result": "confirmed_mathematical_index_error",
            "operations": [{
                "source_start_line": 47410,
                "source_end_line": 47410,
                "old_text": "$s_1, \\ldots, s_n \\in S$",
                "replacement_text": "$s_1, \\ldots, s_r \\in S$",
            }],
        },
        {
            "producer_id": "ALGEBRA-399",
            "stable_id": "MC-STK-ERR-0742",
            "class": "missing_preposition",
            "locus": "algebra.tex:47488",
            "disposition": "Use the idiom replaced by Z.",
            "result": "confirmed_grammar_error",
            "operations": [{
                "source_start_line": 47488,
                "source_end_line": 47488,
                "old_text": "with $R$ replaced $\\mathbf{Z}$",
                "replacement_text": "with $R$ replaced by $\\mathbf{Z}$",
            }],
        },
        {
            "producer_id": "ALGEBRA-401",
            "stable_id": "MC-STK-ERR-0743",
            "class": "incorrect_prime_label",
            "locus": "algebra.tex:47852",
            "disposition": "Quasi-finiteness is asserted at the prime q-prime of S-prime, not at q of S.",
            "result": "confirmed_mathematical_notation_error",
            "operations": [{
                "source_start_line": 47852,
                "source_end_line": 47852,
                "old_text": "quasi-finite at $\\mathfrak q$ as the local ring",
                "replacement_text": "quasi-finite at $\\mathfrak q'$ as the local ring",
            }],
        },
        {
            "producer_id": "ALGEBRA-402",
            "stable_id": "MC-STK-ERR-0744",
            "class": "incorrect_quotient_parenthesization",
            "locus": "algebra.tex:47855",
            "disposition": "Place the full sum of ideals in the denominator of the localized quotient.",
            "result": "confirmed_mathematical_parenthesization_error",
            "operations": [{
                "source_start_line": 47855,
                "source_end_line": 47855,
                "old_text": "S_{\\mathfrak q}/(f_1, \\ldots, f_d) + \\mathfrak pS_{\\mathfrak q} =",
                "replacement_text": "S_{\\mathfrak q}/\\big((f_1, \\ldots, f_d) + \\mathfrak pS_{\\mathfrak q}\\big) =",
            }],
        },
    ],
    "rejected": [
        {
            "producer_id": "ALGEBRA-400",
            "class": "redundant_localization_not_defect",
            "locus": "algebra.tex:47851",
            "result": "rejected_not_a_defect",
            "reason": "In S' = S_g/(f_1,...,f_d), the image of g is already a unit, so S'_g is canonically S'. The displayed map S_g to S'_g is redundant notation but mathematically valid.",
        }
    ],
}


if __name__ == "__main__":
    if OUT.exists():
        raise FileExistsError(f"refusing to overwrite {OUT}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(SPEC, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )
    print(json.dumps({
        "accepted": len(SPEC["accepted"]),
        "rejected": len(SPEC["rejected"]),
        "path": str(OUT),
    }))
