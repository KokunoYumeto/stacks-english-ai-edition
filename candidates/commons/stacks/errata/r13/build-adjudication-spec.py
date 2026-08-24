from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "authority" / "canon" / "R13_ALG_392_394_ADJUDICATION_SPEC.json"
SPEC = {
    "schema": "mathematics-commons-stacks-r13-adjudication-spec/v1",
    "candidate_id": "stacks-errata-a04446e-r13",
    "authority_commit": "a04446e57ec1fbc252a871afcec7752fb2807b14",
    "authority_tree": "3feeb703b931a6e7259782c10e7d1575adc83e5e",
    "authority_sha256": "FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3",
    "accepted": [
        {
            "producer_id": "ALGEBRA-392",
            "stable_id": "MC-STK-ERR-0735",
            "class": "incorrect_tensor_base_field",
            "locus": "algebra.tex:47042",
            "disposition": "Tensor A and L over the shared base field k, not over the fraction field K.",
            "result": "confirmed_mathematical_type_error",
            "operations": [{
                "source_start_line": 47042,
                "source_end_line": 47042,
                "old_text": "$A \\otimes_K L$",
                "replacement_text": "$A \\otimes_k L$",
            }],
        },
        {
            "producer_id": "ALGEBRA-393",
            "stable_id": "MC-STK-ERR-0736",
            "class": "compound_number_agreement",
            "locus": "algebra.tex:47011,47023",
            "disposition": "Use the singular compound fraction fields at both repeated loci.",
            "result": "confirmed_grammar_error",
            "operations": [
                {
                    "source_start_line": 47011,
                    "source_end_line": 47011,
                    "old_text": "fractions fields",
                    "replacement_text": "fraction fields",
                },
                {
                    "source_start_line": 47023,
                    "source_end_line": 47023,
                    "old_text": "fractions fields",
                    "replacement_text": "fraction fields",
                },
            ],
        },
        {
            "producer_id": "ALGEBRA-394",
            "stable_id": "MC-STK-ERR-0737",
            "class": "closed_compound_spelling",
            "locus": "algebra.tex:47013,47015,47016",
            "disposition": "Use the closed compound subalgebra in all three adjacent occurrences.",
            "result": "confirmed_spelling_error",
            "operations": [
                {
                    "source_start_line": 47013,
                    "source_end_line": 47013,
                    "old_text": "sub algebras",
                    "replacement_text": "subalgebras",
                },
                {
                    "source_start_line": 47015,
                    "source_end_line": 47015,
                    "old_text": "sub algebra",
                    "replacement_text": "subalgebra",
                },
                {
                    "source_start_line": 47016,
                    "source_end_line": 47016,
                    "old_text": "sub algebra",
                    "replacement_text": "subalgebra",
                },
            ],
        },
    ],
    "rejected": [],
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
    print(json.dumps({"accepted": len(SPEC["accepted"]), "path": str(OUT)}))
