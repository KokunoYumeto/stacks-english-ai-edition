from __future__ import annotations

import hashlib
import csv
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
    "authority/source/sets.tex": "9BCC55E7F11CF36B0665AE549D5BA76BE6A0EDD00F7FCA36A567E367099603F9",
    "authority/source/topology.tex": "C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872",
    "authority/source/categories.tex": "62F7611AF4C3FEEBD041DB4728B42C7112004CFBB9FA5ECB643C6F5D90DB3F25",
    "authority/canon/ERRATA_R3_INTAKE_FRENCH_20260822.json": "1CBD6FC2A3F503AD86F2ADCF480FD04FE22B37B633590ECF6BCEA079D55FF160",
    "authority/canon/ERRATA_R3_PROOFS.md": "2DB6FC82A46EE3454A07337AD5F5D0C4E6A61A2381F0F45892B2E4137457897E",
    "authority/canon/R3_TOPOLOGY_018_023_INDEPENDENT_REVIEW.md": "E92AB3262E4D5506DBABF36CF5522F8D323ABA3CD379258B6E65D872838B1FB3",
    "authority/producer/SOURCE_DEFECT_LEDGER.csv": "CD91D317D52D999D5174E945F735D32E831DB9F3DB6B8F121B83EF9D6F260F45",
}
PAYLOAD_HASHES = {
    "sets.tex": "A4D8072BDFFEEF9B8EF1D058499761DA1E1F31EABC11BB04B8EA37D04B866D41",
    "topology.tex": "67115451F19CE981FD591F77E6CA16A4DE64A20C71105D2E5215E41FD8F8EB8D",
    "categories.tex": "124F381C9DD01898B8DBB3969B7771190B64E8B2B9CE73E24E7DD1FB0727E2C1",
}
REPLACEMENTS = {
    "sets.tex": [
        (
            r"""\item If $\{U_i \to U\}_{i\in I}
\in \text{Cov}(\mathcal{C})_{\kappa, \alpha}$
and $W \to U$ is a morphism of $\mathcal{C}$, then""",
            r"""\item If $\{U_i \to U\}_{i\in I}
\in \text{Cov}(\mathcal{C})_{\kappa, f(\alpha)}$
and $W \to U$ is a morphism of $\mathcal{C}$, then""",
            1,
        ),
        (
            r"$\text{size}(\coprod_a \coprod_{i \in I_a} W_{i, a}) \leq \text{size}(X)$",
            r"$\text{size}(\coprod_a \coprod_{i \in I_a} W_{a, i}) \leq \text{size}(X)$",
            1,
        ),
        (
            r"$\beta_0 = \sup_{T \in S_\tau} \beta(T)$.",
            r"$\beta_0 = \sup_{T \in \mathcal{S}_\tau} \beta(T)$.",
            1,
        ),
        (
            r"$f$ contained in $\text{Cov}(\mathcal{C})_{\kappa, f(\beta + 1)}$",
            r"$f$ contained in $\text{Cov}(\mathcal{C})_{\kappa, f(\beta(\mathcal{U}) + 1)}$",
            1,
        ),
        (
            r"""Finally, for the second condition, suppose that $\{U_i \to U\}_{i\in I}
\in \text{Cov}(\mathcal{C})_{\kappa, f(\alpha)}$
and for each $i$ we have""",
            r"""Finally, for the second condition, suppose that $\{U_i \to U\}_{i\in I}
\in \text{Cov}(\mathcal{C})_{\kappa, \alpha}$
and for each $i$ we have""",
            1,
        ),
        (
            r"""$\mathcal{W}_i = \{W_{ij} \to U_i\}_{j\in J_i}
\in \text{Cov}(\mathcal{C})_{\kappa, f(\alpha)}$.
Consider the function""",
            r"""$\mathcal{W}_i = \{W_{ij} \to U_i\}_{j\in J_i}
\in \text{Cov}(\mathcal{C})_{\kappa, \alpha}$.
Consider the function""",
            1,
        ),
        (
            r"""of $\beta_2$ is $> \kappa \geq |I|$ the image of this function cannot be a
cofinal subset. Hence there exists a $\beta < \beta_1$ such""",
            r"""of $\beta_2$ is $> \kappa \geq |I|$ the image of this function cannot be a
cofinal subset. Hence there exists a $\beta < \beta_2$ such""",
            1,
        ),
        (
            r"""cofinal subset. Hence there exists a $\beta < \beta_2$ such
that $\mathcal{W}_i \in \text{Cov}_{\kappa, f(\beta)}$ for all $i \in I$.
It follows that""",
            r"""cofinal subset. Hence there exists a $\beta < \beta_2$ such
that $\mathcal{W}_i \in \text{Cov}_{\kappa, f(\beta)}$ for all $i \in I$.
After increasing $\beta$ to at least $\beta(\mathcal{U})$ if necessary,
which still leaves $\beta < \beta_2$, we may also assume that
$\mathcal{U} \in \text{Cov}_{\kappa, f(\beta)}$.
It follows that""",
            1,
        ),
    ],
    "topology.tex": [
        (r"$j, j' \in E$ with maximal distance", r"$j, j' \in V$ with maximal distance", 1),
        (
            r"""The set $A$ is partially ordered by inclusion: $\alpha \leq \alpha'
\Leftrightarrow Z_{\alpha} \subset Z_{\alpha'}$.""",
            r"""The set $A$ is partially ordered by inclusion: $Z \leq Z'
\Leftrightarrow Z \subset Z'$ for $Z, Z' \in A$.""",
            1,
        ),
        (r"$X \setminus U \cup V$", r"$X \setminus (U \cup V)$", 1),
        (
            r"$(X \setminus U \cup V) \cap Z_\alpha",
            r"$(X \setminus (U \cup V)) \cap Z_\alpha",
            1,
        ),
        (
            r"(X \setminus U_{i_1} \cup U_{i_2})",
            r"(X \setminus (U_{i_1} \cup U_{i_2}))",
            1,
        ),
        (r"$J \subset I$ and opens", r"$J \subset \Ob(\mathcal{I})$ and opens", 1),
        (
            r"$E = \bigcup E \cap V_j$ is a finite union",
            r"$E = \bigcup_{j = 1}^m (E \cap V_j)$ is a finite union",
            1,
        ),
        (
            r"$U_K := \{J\subset I \mid J \in Z, \ K\subset J \})$.",
            r"$U_K := \{J\subset I \mid J \in Z, \ K\subset J \}$.",
            1,
        ),
        (
            r"of irreducible closed subsets of $X$. Let $\xi_e \in X$ be a point",
            r"of irreducible closed subsets of $Y$. Let $\xi_e \in X$ be a point",
            1,
        ),
        (
            r"$\text{codim}(Y, Y') \leq \delta(\xi) - \delta(\xi') < \infty$.",
            r"$\text{codim}(Y, Y') \leq \delta(\xi') - \delta(\xi) < \infty$.",
            1,
        ),
        (
            r"""$\xi_i \leadsto \xi_{i + 1}$ is an immediate specialization.
Hence we see that $e = \delta(\xi) - \delta(\xi')$ as desired.""",
            r"""$\xi_{i + 1} \leadsto \xi_i$ is an immediate specialization.
Hence we see that $e = \delta(\xi') - \delta(\xi)$ as desired.""",
            1,
        ),
        (r"(not necessarily closed). We claim", r"(not necessarily open). We claim", 1),
        (
            r"say $T = T_1 \cup \ldots \cup T_n$, and $T$ is nowhere dense in $X$.",
            r"say $T = T_1 \cup \ldots \cup T_n$, and $T$ has empty interior in $X$.",
            1,
        ),
        (
            r"point of the closure of $p(X)$ and let $y \in Y$ be the generic",
            r"point of the closure of $p(Z)$ and let $y \in Y$ be the generic",
            1,
        ),
        (r"point of the closure of $q(Y)$.", r"point of the closure of $q(Z)$.", 1),
        (
            r"By construction the map $f : X \to Y$ is spectral.",
            r"By construction the map $f : X \to \prod\nolimits_U W$ is spectral.",
            1,
        ),
        (r"Thus $Z' = \lim Z_i$ is quasi-compact", r"Thus $Z' = \lim Z'_i$ is quasi-compact", 1),
        (
            r"Using that the spectral topology on $Z$",
            r"Using that the constructible topology on $Z$",
            1,
        ),
        (
            r"$W \setminus E = \lim U_i \setminus E$",
            r"$W \setminus E = \lim (U_i \setminus E)$",
            1,
        ),
        (
            r"identifies $X$ with an open subspace of $X$.",
            r"identifies $X$ with an open subspace of $X^*$.",
            1,
        ),
        (
            r"$E = X \setminus U \cap f^{-1}(V)$.",
            r"$E = X \setminus (U \cap f^{-1}(V))$.",
            1,
        ),
        (
            r"""we can find a continuous map $g : X' \to X''$ over $X$.
Observe that $g$ is a closed map (Lemma \ref{lemma-closed-map}).
Hence $g(X') \subset X''$ is a closed subset surjecting onto $X$
and we conclude $g(X') = X''$ by minimality of $X''$.
On the other hand, if $E \subset X'$ is a proper closed subset,
then $g(E) \not = X''$ as $E$ does not map onto $X$ by minimality
of $X'$. By Lemma \ref{lemma-isomorphism} we see that $g$ is an isomorphism.""",
            r"""we can find a continuous map $g : E \to X''$ over $X$.
Observe that $g$ is a closed map (Lemma \ref{lemma-closed-map}).
Hence $g(E) \subset X''$ is a closed subset surjecting onto $X$
and we conclude $g(E) = X''$ by minimality of $X''$.
On the other hand, if $T \subset E$ is a proper closed subset,
then $g(T) \not = X''$ as $T$ does not map onto $X$ by minimality
of $E$. By Lemma \ref{lemma-isomorphism} we see that $g$ is an isomorphism.""",
            1,
        ),
        (
            r"""and all $U_j$ and $U_j \cap U_{j'}$ quasi-compact,
\item add more here.
\end{enumerate}""",
            r"""and all $U_j$ and $U_j \cap U_{j'}$ quasi-compact,
\end{enumerate}""",
            1,
        ),
        (
            r"""Given two partitions of $X$ we say one {\it refines} the other if
the parts of one are unions of parts of the other.""",
            r"""Given two partitions $\mathcal{P}$ and $\mathcal{Q}$ of $X$, we say
$\mathcal{P}$ {\it refines} $\mathcal{Q}$ if every part of $\mathcal{Q}$
is a union of parts of $\mathcal{P}$.""",
            1,
        ),
        (
            r"$N = \bigcap_{i = 1, \ldots, n} g_iHg_i^{-1}$",
            r"$N = \bigcap_{i = 1, \ldots, n} g_i^{-1}Hg_i$",
            1,
        ),
        (
            r"$\mathcal{I} \to \textit{Top}$, $i \mapsto G_i$",
            r"$\mathcal{I} \to \textit{TopGroup}$, $i \mapsto G_i$",
            1,
        ),
    ],
    "categories.tex": [
        (
            r"directly lift $g \circ f$ to",
            r"directly lift $f \circ g$ to",
            1,
        ),
        (r"\alpha_{f, g}", r"\alpha_{g, f}", 1),
        (
            r"$I_\mathcal{S} \to \mathcal{S}",
            r"$\mathcal{I}_\mathcal{S} \to \mathcal{S}",
            1,
        ),
        (
            r"$d \to b \circ c$. Finally",
            r"$d \to c \circ b$. Finally",
            1,
        ),
        (r"\mathcal{C}/U \times V", r"\mathcal{C}/(U \times V)", 3),
        (
            r"1 \circ (a \otimes b) \circ \circ 1^{-1}",
            r"1 \circ (a \otimes b) \circ 1^{-1}",
            1,
        ),
        (
            r"$\otimes : \mathcal{C} \otimes \mathcal{C} \to \mathcal{C}$ is a functor,",
            r"$\otimes : \mathcal{C} \times \mathcal{C} \to \mathcal{C}$ is a functor,",
            1,
        ),
    ],
}
STRUCTURE_PATTERNS = {
    "labels": re.compile(r"\\label\{[^{}]+\}"),
    "references": re.compile(r"\\(?:ref|eqref|pageref|autoref)\{[^{}]+\}"),
    "citations": re.compile(r"\\cite[a-zA-Z]*?(?:\[[^\]]*\])?\{[^{}]+\}"),
    "environments": re.compile(r"\\(?:begin|end)\{[^{}]+\}"),
    "sections": re.compile(r"\\(?:part|chapter|section|subsection|subsubsection)\*?\{[^{}]*\}"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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
    for old, new, expected_count in REPLACEMENTS[name]:
        count = expected.count(old)
        if count != expected_count:
            raise AssertionError(
                f"{name}: old span occurs {count} times instead of {expected_count}: {old!r}"
            )
        expected = expected.replace(old, new)
        mapped.append({"old": old, "new": new, "count": expected_count})
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
    for pattern in ("*.md", "*.json", "*.jsonl", "*.csv", "*.log", "*.txt", "*.py"):
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
        "candidate_id": "stacks-errata-a04446e-r3",
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

        stable = json.loads((ROOT / "stable-units.json").read_text(encoding="utf-8"))
        expected_ids = [f"MC-STK-ERR-{number:04d}" for number in range(29, 63)]
        ids = [unit["id"] for unit in stable["units"]]
        if stable["unit_count"] != 34 or ids != expected_ids:
            raise AssertionError("stable unit inventory is not the exact R3 set")
        source_map = load_jsonl(ROOT / "source-map.jsonl")
        if [row["unit_id"] for row in source_map] != expected_ids:
            raise AssertionError("source map is not the ordered exact R3 set")
        report["checks"]["unit_closure"] = {
            "passed": True,
            "expected": 34,
            "manifested": 34,
        }

        lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
        if (
            lease["lease_id"] != "stacks-lease-000006-errata-r3"
            or lease["writer_task"] != "01a0256d-5693-77c1-96b2-cf37101e0c6c"
            or lease["upstream_commit"] != AUTHORITY_COMMIT
        ):
            raise AssertionError("candidate lease identity mismatch")
        inventory = json.loads(
            (ROOT / "formula-diagram-inventory.json").read_text(encoding="utf-8")
        )
        if (
            inventory["unit_count"] != 34
            or inventory["unmapped_formula_or_diagram_changes"] != 0
            or inventory["diagram_units"] != ["MC-STK-ERR-0062"]
        ):
            raise AssertionError("formula/diagram inventory closure mismatch")
        report["checks"]["lease_and_inventory"] = {
            "passed": True,
            "units": 34,
            "diagram_units": 1,
        }

        for path in (ROOT / "decisions.jsonl", ROOT / "rejections.jsonl"):
            load_jsonl(path)
        proofs = (ROOT / "authority" / "canon" / "ERRATA_R3_PROOFS.md").read_text(
            encoding="utf-8"
        )
        for unit_id in expected_ids:
            if unit_id not in proofs:
                raise AssertionError(f"proof dossier omits {unit_id}")
        intake = json.loads(
            (ROOT / "authority" / "canon" / "ERRATA_R3_INTAKE_FRENCH_20260822.json").read_text(
                encoding="utf-8"
            )
        )
        if (
            intake["status"]
            != "proof_closed_after_failed_replay_revision_pending_new_independent_replay"
            or intake["proof_closure"]["proved_units"] != 34
        ):
            raise AssertionError("R3 intake does not record proof closure")
        packet_source_ids = [
            row.get("source_id") for row in intake["packet_candidates"]
        ]
        producer_rows = list(
            csv.DictReader(
                (ROOT / "authority" / "producer" / "SOURCE_DEFECT_LEDGER.csv")
                .read_text(encoding="utf-8")
                .splitlines()
            )
        )
        producer_ids = [row["id"] for row in producer_rows]
        if (
            len(packet_source_ids) != 34
            or any(not source_id for source_id in packet_source_ids)
            or len(set(packet_source_ids)) != 34
            or set(packet_source_ids) != set(producer_ids)
            or any(
                row["id"] != f"FR-R3-{row['source_id']}"
                for row in intake["packet_candidates"]
            )
        ):
            raise AssertionError("R3 intake source_id closure does not match producer ledger")
        report["checks"]["ledgers_and_proof_parse"] = {
            "passed": True,
            "jsonl_files": 2,
            "proved_units": 34,
            "producer_source_ids": 34,
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
            != ["sets", "topology", "categories"]
        ):
            raise AssertionError("bounded chapter build receipt failed or stale")
        for chapter in build_receipt["chapters"]:
            stem = chapter["stem"]
            if (
                not chapter["passed"]
                or not chapter["execution_binding_matches"]
                or not chapter["undefined_target_multisets_match_authority"]
                or chapter["candidate_source"]["sha256"]
                != PAYLOAD_HASHES[f"{stem}.tex"]
                or chapter["authority_source"]["sha256"]
                != AUTHORITY_HASHES[f"authority/source/{stem}.tex"]
            ):
                raise AssertionError(f"chapter build binding failed: {stem}")
        if (
            build_receipt["runner"]["sha256"] != sha256(ROOT / "replay-build.py")
            or build_receipt["recipe"]["sha256"] != sha256(ROOT / "BUILD.md")
        ):
            raise AssertionError("build receipt does not bind the current runner and recipe")
        report["checks"]["chapter_builds"] = {
            "passed": True,
            "chapters": 3,
            "receipt_sha256": sha256(build_receipt_path),
        }

        visual_path = ROOT / "builds" / "visual-qa.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        if not visual["passed"] or len(visual["pdfs"]) != 3:
            raise AssertionError("visual PDF QA is incomplete")
        visual_units = []
        for pdf in visual["pdfs"]:
            path = ROOT / pdf["path"]
            if (
                sha256(path) != pdf["sha256"]
                or path.stat().st_size != pdf["bytes"]
                or pdf["unembedded_fonts"]
                or pdf["malformed_link_rectangles"]
                or pdf["out_of_bounds_link_rectangles"]
            ):
                raise AssertionError(f"visual PDF binding or gate failed: {path}")
            visual_units.extend(pdf["covered_units"])
        if sorted(visual_units) != expected_ids:
            raise AssertionError("visual QA does not cover every R3 unit")
        report["checks"]["visual_pdf_qa"] = {
            "passed": True,
            "pdfs": 3,
            "direct_units": 34,
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
