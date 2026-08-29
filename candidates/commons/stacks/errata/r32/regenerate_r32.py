from __future__ import annotations

import bisect
import csv
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
# This narrow registry worktree is a direct child of the shared workspace.
# Deriving the workspace root keeps the replay script portable and prevents
# local account paths from entering the public candidate.
WORKSPACE = ROOT.parents[5]
REPOSITORY = ROOT.parents[4]
FROZEN = WORKSPACE / "03_projects/language_management/cjk/03_working_translations/stacks_cjk_20260821/upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14"
PRODUCER = WORKSPACE / "03_projects/language_management/romance/03_working_translations/stacks_fr_20260821"
CONTROL = WORKSPACE / "03_projects/language_management/romance/00_lane_control"
MASTER = CONTROL / "STACKS_CANON_INTAKE_MASTER.jsonl"
LEDGER = PRODUCER / "00_control/SOURCE_DEFECT_LEDGER.csv"
FIELDS_DECL = PRODUCER / "p01/evidence/FIELDS_SOURCE_EMENDATIONS.json"
CATEGORIES_DECL = PRODUCER / "p01/evidence/CATEGORIES_SOURCE_EMENDATIONS.json"

COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
WRITER = "01a0256d-5693-77c1-96b2-cf37101e0c6c"
CANDIDATE = "stacks-errata-a04446e-r32"
NAMESPACE = "commons/stacks/errata/r32"
LEASE_ID = "stacks-lease-000036-errata-r32"
STAMP = "2026-08-29T20:30:00Z"

EXPECTED_STABLE = [
    *(f"MC-STK-ERR-{n:04d}" for n in range(338, 346)),
    "MC-STK-ERR-0396",
    *(f"MC-STK-ERR-{n:04d}" for n in range(399, 493)),
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="")


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def line_starts(data: bytes) -> list[int]:
    return [0] + [i + 1 for i, byte in enumerate(data) if byte == 10]


def line_at(starts: list[int], offset: int) -> int:
    return bisect.bisect_right(starts, offset)


def find_line_bound(data: bytes, old: str, first: int, last: int | None = None) -> tuple[int, int]:
    if last is None:
        last = first
    needle = old.encode("utf-8")
    starts = line_starts(data)
    found: list[tuple[int, int]] = []
    cursor = 0
    while True:
        pos = data.find(needle, cursor)
        if pos < 0:
            break
        end = pos + len(needle)
        actual_first = line_at(starts, pos)
        actual_last = line_at(starts, max(pos, end - 1))
        if actual_first == first and actual_last == last:
            found.append((pos, end))
        cursor = pos + 1
    if len(found) != 1:
        raise AssertionError(f"expected one line-bound preimage {first}-{last} {old!r}, found {len(found)}")
    return found[0]


def op(pid: str, first: int, old: str, new: str, last: int | None = None) -> dict:
    return {"producer_id": pid, "first": first, "last": last or first, "old": old, "new": new}


# These are the exact, already-adjudicated Algebra operations corresponding to
# MC-STK-ERR-0399..0492.  They are deliberately line-bound and replayed against
# the frozen authority; no contextual or whole-file replacement is permitted.
AOPS = [
    op("ALGEBRA-001", 31824, r"$(I, \leq)$", r"$(\Lambda, \leq)$"),
    op("ALGEBRA-002", 31801, "cofiltered", "filtered"),
    op("ALGEBRA-003", 32020, r"in $M \otimes_A R_i$", r"in $N \otimes_A R_i$"),
    op("ALGEBRA-004", 32036, r"\sum a_j x_j", r"\sum a_j y_j"),
    op("ALGEBRA-005", 32056, r"M \otimes_R R_i", r"M \otimes_A R_i"),
    op("ALGEBRA-005", 32057, r"N \otimes_R R_i", r"N \otimes_A R_i"),
    op("ALGEBRA-006", 32134, r"$B \otimes_A R = \colim_i B \otimes_A R_i$", r"$C \otimes_A R = \colim_i C \otimes_A R_i$"),
    op("ALGEBRA-006", 32136, r"in $B \otimes_A R_i$", r"in $C \otimes_A R_i$"),
    op("ALGEBRA-008", 32151, r"$K = \Ker(A[x_1, \ldots, x_m] \to N)$", r"$K = \Ker(A[x_1, \ldots, x_m] \to C)$"),
    op("ALGEBRA-009", 32152, r"x_j \mapsto \sum c_j", r"x_j \mapsto c_j"),
    op("ALGEBRA-010", 32162, r"$\xi_s = f_j(z_1, \ldots, z_m)$", r"$\xi_s = f_s(z_1, \ldots, z_m)$"),
    op("ALGEBRA-011", 32170, r"$v : B \otimes_A R \to C \otimes_A R$", r"$v : C \otimes_A R \to B \otimes_A R$"),
    op("ALGEBRA-012", 32173, r"B \otimes_R R_i", r"B \otimes_A R_i"),
    op("ALGEBRA-012", 32174, r"C \otimes_R R_i", r"C \otimes_A R_i"),
    op("ALGEBRA-013", 32197, r"$\varphi \otimes 1_R = \psi \otimes 1_R$", r"$\varphi_\lambda \otimes 1_R = \psi_\lambda \otimes 1_R$"),
    op("ALGEBRA-013", 32198, r"$\varphi \otimes 1_{R_\mu} = \psi \otimes 1_{R_\mu}$", r"$\varphi_\lambda \otimes 1_{R_\mu} = \psi_\lambda \otimes 1_{R_\mu}$"),
    op("ALGEBRA-014", 32531, "integral\nover $S$", "integral\nover $R$", 32532),
    op("ALGEBRA-015", 16531, r"$D(f) \cap \text{supp}(K) = 0$", r"$D(f) \cap \text{supp}(K) = \emptyset$"),
    op("ALGEBRA-016", 18416, r"$H_i(R(A)_\bullet))$", r"$H_i(R(A)_\bullet)$"),
    op("ALGEBRA-017", 18644, "cohomology groups", "homology groups"),
    op("ALGEBRA-018", 522, "an surjection", "a surjection"),
    op("ALGEBRA-019", 972, "zero on $H$", "zero in $H$"),
    op("ALGEBRA-020", 1148, "Denote by $m/s$ (or\n$\\frac{m}{s}$) be the equivalence class of $(m, s)$ and $S^{-1}M$ be\nthe set of all equivalence classes.", "Denote by $m/s$ (or\n$\\frac{m}{s}$) the equivalence class of $(m, s)$ and by $S^{-1}M$\nthe set of all equivalence classes.", 1150),
    op("ALGEBRA-021", 1150, "Define the addition and scalar\nmultiplication as follows\n$$\nm/s + n/t = (mt + ns)/st,\\quad\nm/s\\cdot n/t = mn/st", "For $a \\in A$, $m, n \\in M$, and $s, t \\in S$, define addition and scalar\nmultiplication by\n$$\nm/s + n/t = (mt + ns)/st,\\quad\n(a/s)\\cdot(m/t) = am/st", 1154),
    op("ALGEBRA-022", 1172, r"Let $S \subset R$ a multiplicative subset.", r"Let $S \subset R$ be a multiplicative subset."),
    op("ALGEBRA-023", 1187, "a given R-linear map", "a given $R$-linear map"),
    op("ALGEBRA-024", 1308, r"given a $A$-module M", r"given an $A$-module $M$"),
    op("ALGEBRA-025", 1322, "independent the choice", "independent of the choice"),
    op("ALGEBRA-026", 1327, r"an $A$ homomorphism", r"an $A$-module homomorphism"),
    op("ALGEBRA-027", 1375, "the preceding Corollary", "the preceding Lemma"),
    op("ALGEBRA-028", 1771, r"$(j\circ j') \circ g$", r"$(j'\circ j) \circ g$"),
    op("ALGEBRA-028", 1774, r"$(j'\circ j) \circ g'", r"$(j\circ j') \circ g'"),
    op("ALGEBRA-029", 1772, "satisfies the universal properties", "satisfy the universal properties"),
    op("ALGEBRA-030", 1808, r"an $R$-module T", r"an $R$-module $T$"),
    op("ALGEBRA-031", 1901, r"isomorphic as both as $A$-module and $B$-module", r"isomorphic both as $A$-modules and as $B$-modules"),
    op("ALGEBRA-032", 2059, r"to be {\it flat} $R$-module", r"to be a {\it flat} $R$-module"),
    op("ALGEBRA-033", 19526, r"a direct summand of $P_{2, f}$", r"a direct summand of $P_{1, f}$"),
    op("ALGEBRA-034", 2611, r"Then $x + fy$ is not contained in $\mathfrak p_1, \ldots, \mathfrak p_s$.", r"Then $x + fy$ does not belong to any of $\mathfrak p_1, \ldots, \mathfrak p_s$."),
    op("ALGEBRA-035", 2736, r"$A_1B = B A_1 = f$", r"$A_1B = B A_1 = fI_m$"),
    op("ALGEBRA-036", 2741, r"$A_1^{ij}$", r"$A_1^{jk}$"),
    op("ALGEBRA-037", 2867, r"$P = t^n + a_1 t^{n - 1} + \ldots + a_n \in R[T]$", r"$P = T^n + a_1 T^{n - 1} + \ldots + a_n \in R[T]$"),
    op("ALGEBRA-038", 2910, r"\sum_{j = 1, \ldots, n}", r"\sum_{j = 1}^{n}"),
    op("ALGEBRA-039", 3033, "Since 1 $\\notin I$ for all $I \\in A$, the union does not contain\n1 and thus is proper.", "Since $1 \\notin I$ for all $I \\in A$, the union does not contain\n$1$ and thus is proper.", 3034),
    op("ALGEBRA-040", 3075, r"either $I$ of $J$ is in $\mathfrak{p}$", r"either $I \subset \mathfrak{p}$ or $J \subset \mathfrak{p}$"),
    op("ALGEBRA-041", 3179, "let $\\mathfrak p$\nthe inverse image", "let $\\mathfrak p$ be\nthe inverse image", 3180),
    op("ALGEBRA-042", 3297, r"$U \cap V = \bigcup D(f_ig_j)$", r"$U \cap V = \bigcup_{1 \leq i \leq n,\ 1 \leq j \leq m} D(f_i g_j)$"),
    op("ALGEBRA-043", 21145, r"M_i \otimes_R M_j$", r"M_i \otimes_R N_j$"),
    op("ALGEBRA-043", 21151, r"$b : M_{j''} \to M_{j'}$", r"$b : N_{j''} \to N_{j'}$"),
    op("ALGEBRA-044", 3388, "The equivalence (1) and (2)", "The equivalence of (1) and (2)"),
    op("ALGEBRA-045", 3533, "Namely, there is an obvious ring map\n$F \\to S_\\mathfrak q \\otimes_{R_\\mathfrak p} \\kappa(\\mathfrak p)$\nwhich is easily seen to be isomorphic to $F \\to F_{\\overline{\\mathfrak q}}$.", "Namely, there is an obvious ring map\n$F \\to S_\\mathfrak q \\otimes_{R_\\mathfrak p} \\kappa(\\mathfrak p)$\nwhich, under the displayed isomorphism, identifies with $F \\to F_{\\overline{\\mathfrak q}}$.", 3535),
    op("ALGEBRA-046", 36374, r"$\overline{J} = J/\mathfrak m_R \cap J \subset \overline{S}$", r"$\overline{J} = J/(\mathfrak m_R S \cap J) \subset \overline{S}$"),
    op("ALGEBRA-047", 36391, r"$S/(f_1, \ldots, f_{\overline{c}}) + IS$", r"$S/((f_1, \ldots, f_{\overline{c}}) + IS)$"),
    op("ALGEBRA-047", 36392, r"$S/(f_1, \ldots, f_{\overline{c}}) + IS", r"$S/((f_1, \ldots, f_{\overline{c}}) + IS)"),
    op("ALGEBRA-048", 37001, r"$\mathfrak q' \subset S$", r"$\mathfrak q' \subset S'$"),
    op("ALGEBRA-048", 37008, r"$S_g \to S_{gg'}$", r"$S_g \to S'_{gg'}$"),
    op("ALGEBRA-048", 37009, r"$R \to S_{gg'}$", r"$R \to S'_{gg'}$"),
    op("ALGEBRA-049", 37027, r"\overline{S}_{g_i}", r"\overline{S}_{\overline{g}_i}"),
    op("ALGEBRA-049", 37036, r"\overline{S}_{g_i}", r"\overline{S}_{\overline{g}_i}"),
    op("ALGEBRA-049", 37766, r"\overline{S}_{g_i}", r"\overline{S}_{\overline{g}_i}"),
    op("ALGEBRA-049", 37774, r"\overline{S}_{g_i}", r"\overline{S}_{\overline{g}_i}"),
    op("ALGEBRA-050", 3680, "is\ninvertible element", "is an\ninvertible element", 3681),
    op("ALGEBRA-051", 3725, "generates $M_{st}$", "generate $M_{st}$"),
    op("ALGEBRA-052", 37945, r"\Omega_{P/R} \otimes_R S", r"\Omega_{P/R} \otimes_P S"),
    op("ALGEBRA-052", 38020, r"\NL_{P/R} \otimes_R S", r"\NL_{P/R} \otimes_P S"),
    op("ALGEBRA-052", 38138, r"\Omega_{P/R} \otimes_R S", r"\Omega_{P/R} \otimes_P S"),
    op("ALGEBRA-053", 37957, r"\text{d}\lambda \mu", r"\text{d}(\lambda\mu)"),
    op("ALGEBRA-054", 21757, r"since $\Ker(\varphi)$", r"since $\Im(\varphi)$"),
    op("ALGEBRA-055", 21937, r"\colim_{j \in J}", r"\colim_{j \in I}"),
    op("ALGEBRA-055", 21944, r"\colim_{j \in J} (Q \otimes_R M_j) \subset \colim_{j \in J}", r"\colim_{j \in I} (Q \otimes_R M_j) \subset \colim_{j \in I}"),
    op("ALGEBRA-056", 22068, "is a countable,", "is a countable set,"),
    op("ALGEBRA-057", 22073, "if $\\ell$\nis odd", "if $\\ell$\nis even", 22074),
    op("ALGEBRA-057", 22074, r"if $\ell$ is even", r"if $\ell$ is odd"),
    op("ALGEBRA-058", 22491, "\\Im(P\n\\otimes_R S \\to M \\otimes_R S)", "\\Im(P\n\\otimes_R S \\to (M/M_{\\alpha}) \\otimes_R S)", 22492),
    op("ALGEBRA-059", 22508, r"ordinal $S$", r"ordinal $\gamma$"),
    op("ALGEBRA-059", 22508, r"$\alpha \in S$", r"$\alpha \in \gamma$"),
    op("ALGEBRA-059", 22509, r"$(M_{\alpha})_{\alpha \in S}$", r"$(M_{\alpha})_{\alpha \in \gamma}$"),
    op("ALGEBRA-059", 22512, r"$M = \bigoplus_{\alpha + 1 \in S}", r"$M = \bigoplus_{\alpha + 1 \in \gamma}"),
    op("ALGEBRA-060", 3902, "An idempotent\nis not nilpotent", "A nonzero idempotent\nis not nilpotent", 3903),
    op("ALGEBRA-061", 4020, "we have see", "we see"),
    op("ALGEBRA-062", 38572, r"$\dim(S_{\mathfrak m'})", r"$\dim(S'_{\mathfrak m'})"),
    op("ALGEBRA-063", 38585, r"$g \not \in \mathfrak m'$", r"$g' \not \in \mathfrak m'$"),
    op("ALGEBRA-064", 38905, "is a geometrically reduced", "is geometrically reduced"),
    op("ALGEBRA-065", 4355, r"$f_1, f_2, \ldots f_n\in R$", r"$f_1, f_2, \ldots, f_n \in R$"),
    op("ALGEBRA-066", 38880, r"x^p + y^2 + \alpha", r"x^p + y^2 + t"),
    op("ALGEBRA-066", 38882, r"(y, x^p + \alpha)$", r"(y, x^p + t)$"),
    op("ALGEBRA-067", 4556, r"hence it is a field", r"hence $R_{\mathfrak p}$ is a field"),
    op("ALGEBRA-068", 4624, r"is contained in $R \setminus \mathfrak q_i$", r"lies in $R \setminus \mathfrak q_i$"),
    op("ALGEBRA-069", 39012, r"\bigoplus\nolimits_{j = 1}^m", r"\bigoplus\nolimits_{j = 1}^n"),
    op("ALGEBRA-070", 39109, "these tensor product are", "these tensor products are"),
    op("ALGEBRA-071", 4770, "\\item every standard open $D(f) \\subset X$ is closed, and\n\\item add more here.", "\\item every standard open $D(f) \\subset X$ is closed.", 4771),
    op("ALGEBRA-072", 39193, r"\dim_{\kappa(m)}", r"\dim_{\kappa(\mathfrak m)}"),
    op("ALGEBRA-073", 39440, r"\item we have $\mathfrak p S_{\mathfrak q}", r"\item $\mathfrak p S_{\mathfrak q}"),
    op("ALGEBRA-074", 39464, "a finite products of fields", "a finite product of fields"),
    op("ALGEBRA-075", 39496, "Replace $S$ by $S_g$ again we may\nassume", "Replacing $S$ by $S_g$ again, we may\nassume", 39497),
    op("ALGEBRA-076", 39536, "there exist an idempotent", "there exists an idempotent"),
    op("ALGEBRA-077", 39744, r"$\text{Res}_x(f, g)$", r"$\text{Res}_x(g, h)$"),
    op("ALGEBRA-078", 4877, "In this case, $\\mathfrak p$ must be generated by nonconstant polynomials", "In this case, if $\\mathfrak p = (0)$ there is nothing more to prove. Otherwise, $\\mathfrak p$ contains nonconstant polynomials"),
    op("ALGEBRA-079", 4904, r"obtain $p = af + bg$ for $p, a, b \in k[x]$.", r"obtain $p = af + bg$ for $0 \ne p \in k[x]$ and $a, b \in k[x, y]$."),
    op("ALGEBRA-080", 4907, r"for $ah, bh \in k[x]$", r"for $ah, bh \in k[x, y]$"),
    op("ALGEBRA-081", 4958, r"$h(z) = c_1z + c_0$", r"$g(z) = c_1z + c_0$"),
    op("ALGEBRA-082", 4961, r"$f(z) = A(z)^2h(z)+b_1B(z)+b_0A(z)$", r"$f(z) = A(z)^2h(z)+b_1B(z)+b_0A(z)+a$"),
    op("ALGEBRA-083", 4981, "for a ring T and a", "for a ring $T$ and a"),
    op("ALGEBRA-084", 4990, r"$D(f)\subset T$", r"$D(f)\subset \Spec(T)$"),
    op("ALGEBRA-085", 5049, r"2a-a", r"2a-2"),
    op("ALGEBRA-086", 5060, "is the localization of $\\mathbf{Q}[z]$\nat the maximal ideal $(z-a)$", "is the localization of $\\mathbf{Q}[z]$\nat the element $z-a$", 5061),
    op("ALGEBRA-086", 5062, r"Any localization $S^{-1}R$", r"Any proper localization $S^{-1}R$"),
    op("ALGEBRA-087", 5079, "that $(z-a)^{k + \\ell}$ can only be in $R$ for $k = \\ell = 0$; indeed, if\n$a = 1/2$, then this is in $R$ as long as $k + \\ell$ is even.", "that $(z-a)^n$ can belong to $R_a$ only for $n = 0$; indeed, if\n$a = 1/2$, then it belongs to $R_a$ whenever $n$ is even.", 5080),
    op("ALGEBRA-088", 23688, r"N \otimes_{R/} M/IM", r"N \otimes_{R/I} M/IM"),
    op("ALGEBRA-089", 23917, "surjection on cohomology", "surjection on homology"),
    op("ALGEBRA-090", 24226, "has a kernel", "has a nonzero kernel"),
    op("ALGEBRA-091", 24498, r"both $R$ and $S$", r"both $M$ and $S$"),
    op("ALGEBRA-092", 24504, r"$x_\alpha \in A$", r"$x_\alpha \in M$"),
    op("ALGEBRA-093", 24559, r"$\text{Tor}_1^S(IS, M)", r"$\text{Tor}_1^S(S/IS, M)"),
    op("ALGEBRA-094", 5281, "ideals that not principal", "ideals that are not principal"),
    op("ALGEBRA-095", 5335, "radical ideas", "radical ideals"),
]


def selected_rows() -> tuple[list[dict], dict[str, dict], dict[str, dict]]:
    master = jsonl(MASTER)
    selected = [row for row in master if row.get("normalized_state") == "provisionally_accepted_unmaterialized"]
    stable = [row["stable_ids"][0] for row in selected]
    if stable != EXPECTED_STABLE:
        raise AssertionError(f"live master no longer matches the 103-ID assignment: {stable[:3]} ... {stable[-3:]}")
    with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
        ledger_rows = {row["id"]: row for row in csv.DictReader(handle)}
    by_pid = {row["producer_id"]: row for row in selected}
    if len(by_pid) != 103 or any(pid not in ledger_rows for pid in by_pid):
        raise AssertionError("producer/master intake closure mismatch")
    return selected, by_pid, ledger_rows


def declared_ops(by_pid: dict[str, dict], ledger_rows: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    for path, wanted in (
        (FIELDS_DECL, {f"FIELDS-{n:03d}" for n in (33, 34, 35, 36, 37, 39, 40)} | {"FIELDS-041A", "FIELDS-041B"}),
        (CATEGORIES_DECL, {"CATEGORIES-065"}),
    ):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for item in doc["emendations"]:
            if item["id"] not in wanted:
                continue
            semantic = "FIELDS-041" if item["id"].startswith("FIELDS-041") else item["id"]
            rows.append(op(semantic, int(item["line"]), item["old"], item["new"]))
    rows.extend(AOPS)
    counts = defaultdict(int)
    for row in rows:
        if row["producer_id"] not in by_pid:
            raise AssertionError(f"operation has unselected producer ID {row['producer_id']}")
        counts[row["producer_id"]] += 1
        row["rationale"] = (
            ledger_rows[row["producer_id"]]["observation"] + " " +
            ledger_rows[row["producer_id"]]["proposed_smallest_correction"]
        )
    missing = sorted(set(by_pid) - set(counts))
    if missing:
        raise AssertionError(f"accepted units lack exact operations: {missing}")
    return rows


def main() -> int:
    selected, by_pid, ledger_rows = selected_rows()
    abstract = declared_ops(by_pid, ledger_rows)
    source_data: dict[str, bytes] = {}
    for source in ("fields.tex", "categories.tex", "algebra.tex"):
        data = (FROZEN / source).read_bytes()
        expected = next(row["authority_sha256"] for row in selected if row["source_file"] == source)
        if sha(data) != expected:
            raise AssertionError(f"frozen authority mismatch: {source}")
        source_data[source] = data
        target = ROOT / "authority" / "source" / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    shutil.copyfile(FROZEN / "COPYING", ROOT / "authority" / "COPYING")
    shutil.copyfile(REPOSITORY / "upstream" / "stacks.lock.json", ROOT / "authority" / "upstream.lock.json")

    stable_for_pid = {row["producer_id"]: row["stable_ids"][0] for row in selected}
    source_for_pid = {row["producer_id"]: row["source_file"] for row in selected}
    loc_for_pid = {row["producer_id"]: row["source_locator"] for row in selected}
    concrete: list[dict] = []
    per_unit_count = defaultdict(int)
    for item in abstract:
        pid = item["producer_id"]
        source = source_for_pid[pid]
        data = source_data[source]
        start, end = find_line_bound(data, item["old"], item["first"], item["last"])
        per_unit_count[pid] += 1
        stable = stable_for_pid[pid]
        old_b, new_b = item["old"].encode(), item["new"].encode()
        concrete.append({
            "operation_id": f"{stable}-OP{per_unit_count[pid]}",
            "operation_index_within_unit": per_unit_count[pid],
            "stable_id": stable,
            "producer_id": pid,
            "source": source,
            "source_start_line": item["first"],
            "source_end_line": item["last"],
            "start_byte": start,
            "end_byte_exclusive": end,
            "old_text": item["old"],
            "old_bytes": len(old_b),
            "old_sha256": sha(old_b),
            "replacement_text": item["new"],
            "replacement_bytes": len(new_b),
            "replacement_sha256": sha(new_b),
            "occurrence_count_in_frozen_authority": data.count(old_b),
            "declared_line_range_occurrence_count": 1,
            "rationale": item["rationale"],
            "adjudication_state": "accepted_before_materialization",
        })

    # Ensure nonoverlap and exact descending-byte replay independently per file.
    payload_hashes: dict[str, dict] = {}
    operations_by_source: dict[str, list[dict]] = defaultdict(list)
    for row in concrete:
        operations_by_source[row["source"]].append(row)
    for source, operations in operations_by_source.items():
        ascending = sorted(operations, key=lambda row: row["start_byte"])
        for left, right in zip(ascending, ascending[1:]):
            if left["end_byte_exclusive"] > right["start_byte"]:
                raise AssertionError(f"overlap: {left['operation_id']} and {right['operation_id']}")
        payload = source_data[source]
        for row in sorted(operations, key=lambda row: row["start_byte"], reverse=True):
            old = row["old_text"].encode()
            new = row["replacement_text"].encode()
            if payload[row["start_byte"]:row["end_byte_exclusive"]] != old:
                raise AssertionError(f"stale replay interval {row['operation_id']}")
            payload = payload[:row["start_byte"]] + new + payload[row["end_byte_exclusive"]:]
        target = ROOT / "payload" / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        payload_hashes[source] = {
            "authority_bytes": len(source_data[source]),
            "authority_sha256": sha(source_data[source]),
            "payload_bytes": len(payload),
            "payload_sha256": sha(payload),
            "operations": len(operations),
        }

    # Preserve only the bounded accepted rows and the exact declaration witnesses.
    producer_dir = ROOT / "authority" / "producer"
    producer_dir.mkdir(parents=True, exist_ok=True)
    fields = list(next(iter(ledger_rows.values())).keys())
    with (producer_dir / "accepted-unmaterialized.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in selected:
            writer.writerow(ledger_rows[row["producer_id"]])
    shutil.copyfile(FIELDS_DECL, producer_dir / "FIELDS_SOURCE_EMENDATIONS.json")
    shutil.copyfile(CATEGORIES_DECL, producer_dir / "CATEGORIES_SOURCE_EMENDATIONS.json")

    units = []
    source_map_rows = []
    for selected_row in selected:
        pid = selected_row["producer_id"]
        stable = stable_for_pid[pid]
        unit_ops = [row for row in concrete if row["producer_id"] == pid]
        unit = {
            "id": stable,
            "class": "source_defect_correction",
            "source": selected_row["source_file"],
            "payload": f"payload/{selected_row['source_file']}",
            "locus": selected_row["source_locator"],
            "operation_ids": [row["operation_id"] for row in unit_ops],
            "producer_id": pid,
            "status": "accepted_prior_round_materialized_r32",
        }
        units.append(unit)
        source_map_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable,
            "class": "source_defect_correction",
            "source": selected_row["source_file"],
            "authority": f"authority/source/{selected_row['source_file']}",
            "authority_sha256": selected_row["authority_sha256"],
            "payload": f"payload/{selected_row['source_file']}",
            "locus": selected_row["source_locator"],
            "producer_id": pid,
            "operations": unit_ops,
            "proof": "prior_acceptance_replayed_against_frozen_authority",
            "adverse_evidence": "The original provisional-acceptance status is preserved; R32 performs the previously missing exact materialization only.",
        })
    dump(ROOT / "stable-units.json", {"schema": "mathematics-commons-stacks-errata-units/v1", "authority_commit": COMMIT, "unit_count": len(units), "units": units})
    dump(ROOT / "operation-spec.json", {"schema": "mathematics-commons-stacks-errata-operation-spec/v1", "authority_commit": COMMIT, "apply_order": "descending_start_byte_per_source", "operation_count": len(concrete), "operations": concrete})
    (ROOT / "source-map.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in source_map_rows), encoding="utf-8", newline="")
    (ROOT / "rejections.jsonl").write_text("", encoding="utf-8", newline="")

    decisions = [
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R32-D0001", "timestamp_utc": STAMP, "choice": "Materialize exactly the 103 prior-accepted but unmaterialized stable units without reopening adjudication.", "rationale": "The live master intake identifies the closed set MC-STK-ERR-0338..0345, 0396, and 0399..0492."},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R32-D0002", "timestamp_utc": STAMP, "choice": "Bind every correction to exact UTF-8 preimages and line ranges on the pinned authority.", "rationale": "This prevents global replacement and proves payload closure by descending-byte replay."},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R32-D0003", "timestamp_utc": STAMP, "choice": "Preserve the nonconsecutive historical stable IDs and their producer identities in registry order.", "rationale": "The IDs were allocated during earlier adjudication and must not be renumbered."},
        {"schema": "mathematics-commons-stacks-candidate-decision/v1", "id": "ERR-R32-D0004", "timestamp_utc": STAMP, "choice": "Keep generated-source composition outside R32.", "rationale": "The composer owns cumulative English source; R32 is registry materialization only."},
    ]
    (ROOT / "decisions.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in decisions), encoding="utf-8", newline="")

    config = {
        "schema": "mathematics-commons-stacks-errata-candidate-config/v1",
        "candidate_id": CANDIDATE,
        "namespace": NAMESPACE,
        "lease_id": LEASE_ID,
        "writer_task": WRITER,
        "authority_commit": COMMIT,
        "authority_tree": TREE,
        "accepted": 103,
        "rejected": 0,
        "unresolved": 0,
        "operation_count": len(concrete),
        "expected_unit_ids": EXPECTED_STABLE,
        "expected_producer_ids": [row["producer_id"] for row in selected],
        "stems": payload_hashes,
        "materialization_only": True,
        "composition_performed": False,
    }
    dump(ROOT / "candidate.config.json", config)
    dump(ROOT / "LEASE.json", {"schema": "mathematics-commons-stacks-candidate-lease-pointer/v1", "candidate_path": "candidates/commons/stacks/errata/r32", "lease_id": LEASE_ID, "namespace": NAMESPACE, "state": "released_after_admission", "upstream_commit": COMMIT, "writer_contract": "candidates/CONTRACT.md", "writer_task": WRITER})
    dump(ROOT / "source-validation.json", {"schema": "mathematics-commons-stacks-errata-source-validation/v1", "candidate_id": CANDIDATE, "passed": True, "accepted_units": 103, "operation_count": len(concrete), "authority_commit": COMMIT, "stems": payload_hashes, "authority_bytes_mutated": False, "composition_performed": False})
    dump(ROOT / "formula-diagram-inventory.json", {"schema": "mathematics-commons-stacks-errata-formula-diagram-inventory/v1", "candidate_id": CANDIDATE, "unit_count": 103, "classified_units": EXPECTED_STABLE, "unmapped_formula_or_diagram_changes": 0, "note": "Classification is source-correction closure; formula, diagram, and prose units remain individually bound in source-map.jsonl."})
    print(json.dumps({"passed": True, "candidate_id": CANDIDATE, "units": 103, "operations": len(concrete), "stems": payload_hashes}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
