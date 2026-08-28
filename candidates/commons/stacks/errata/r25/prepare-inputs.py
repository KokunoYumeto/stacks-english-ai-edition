from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GENERATED_AT = "2026-08-27T21:34:00Z"
AUTHORITY_COMMIT = "a04446e57ec1fbc252a871afcec7752fb2807b14"
AUTHORITY_TREE = "3feeb703b931a6e7259782c10e7d1575adc83e5e"
AUTHORITY_PATH = "artin.tex"
AUTHORITY_BYTES = 254362
AUTHORITY_SHA256 = "EBA90A897B08EEBFF451E80925D13381B1A7F6AB883A34118733CD24CF061F47"
PRODUCER_LEDGER_BYTES = 111348
PRODUCER_LEDGER_SHA256 = "DA9BC0D8FA6CC73AC40BD8CAC7911BE7770CC8F0A823BC4491C55A6C97443F8A"
PRODUCER_GLOBAL_LEDGER_AT_INTAKE_BYTES = 600281
PRODUCER_GLOBAL_LEDGER_AT_INTAKE_SHA256 = "D3E69FB2195EF9DE2D843F3642B2AE8D99AB805163F05E36F628B6234FA6F373"
REJECTED_IDS = ["P11-E0202", "P11-E0215", "P11-E0217"]
MERGE_GROUPS = [
    ["P11-E0222", "P11-E0226"],
    ["P11-E0245", "P11-E0248"],
    ["P11-E0251", "P11-E0252"],
    ["P11-E0274", "P11-E0276"],
    ["P11-E0312", "P11-E0313"],
    ["P11-E0333", "P11-E0334"],
]
EXPECTED_IDS = [f"MC-STK-ERR-{number:04d}" for number in range(1046, 1177)]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="",
    )


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
            for row in rows
        ),
        encoding="utf-8",
        newline="",
    )


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def operation_table() -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {}

    def add(producer_id: str, start: int, end: int, old: str, new: str) -> None:
        rows.setdefault(producer_id, []).append({
            "producer_id": producer_id,
            "source_start_line": start,
            "source_end_line": end,
            "old_text": old,
            "replacement_text": new,
        })

    add("P11-E0200", 28, 28, "terminology in this chapter is awkward", "terminology in this chapter are awkward")
    add("P11-E0201", 104, 104, "This approximation uses the local rings", "This approximation uses that the local rings")
    add("P11-E0203", 156, 156, "separated of finite type over $S$", "separated and of finite type over $S$")
    add("P11-E0204", 170, 170, "thing to prove, instead", "thing to prove; instead")
    add("P11-E0205", 256, 256, "$\\Lambda$-algebra homomorphism", "a $\\Lambda$-algebra homomorphism")
    add("P11-E0206", 286, 286, "is equal the given map", "is equal to the given map")
    add("P11-E0207", 306, 306, "Let $k$ is a field", "Let $k$ be a field")
    add("P11-E0208", 394, 394, "algebraic spaces, see (insert future reference here).", "algebraic spaces.")
    add("P11-E0209", 422, 422, "Let $y'$ be an object of left hand side.", "Let $y'_1, y'_2$ be objects of the left hand side.")
    add("P11-E0209", 423, 423, "$\\mathit{Isom}(y', y')$", "$\\mathit{Isom}(y'_1, y'_2)$")
    add("P11-E0210", 572, 572, "\\mathcal{X}_Y \\times_{\\mathcal{Y}_Y} \\mathcal{Z}_Y", "\\mathcal{X}_Y \\times_{\\mathcal{X}_X} \\mathcal{X}_{X'}")
    add("P11-E0210", 574, 574, "\\mathcal{X}_X \\times_{\\mathcal{Y}_X} \\mathcal{Z}_X", "\\mathcal{Y}_Y \\times_{\\mathcal{Y}_X} \\mathcal{Y}_{X'}")
    add("P11-E0210", 577, 577, "\\mathcal{X}_{X'} \\times_{\\mathcal{Y}_{X'}} \\mathcal{Z}_{X'}", "\\mathcal{Z}_Y \\times_{\\mathcal{Z}_X} \\mathcal{Z}_{X'}")
    add("P11-E0211", 584, 584, "$(x_Y, x_{Y'}, \\alpha)$", "$(x_Y, x_{X'}, \\alpha)$")
    add("P11-E0211", 585, 585, "$(z_Y, z_{Y'}, \\beta)$", "$(z_Y, z_{X'}, \\beta)$")
    add("P11-E0212", 690, 690, "object of $\\mathcal{F}$", "object of $\\mathcal{X}$")
    add("P11-E0213", 691, 691, "Denote $x_{l, 0}$ the restriction", "Denote by $x_{l, 0}$ the restriction")
    add("P11-E0214", 715, 715, "Choosing pullback functor", "Choosing a pullback functor")
    add("P11-E0216", 887, 887, "Hence, choose an scheme", "Choose a scheme")
    add("P11-E0216", 888, 888, "$U' \\to R$ we see that", "$U' \\to R$. Then")
    add("P11-E0218", 932, 932, "$f_1, \\ldots, f_n$ hence", "$f_1, \\ldots, f_n$; hence")
    add("P11-E0219", 944, 944, "Denote $x_0, y_0, z_0$ the objects", "Denote by $x_0, y_0, z_0$ the objects")
    add("P11-E0220", 995, 995, "\\mathfrak m^n", "\\mathfrak m_R^n")
    add("P11-E0220", 995, 995, "\\mathfrak m^{n + 1}", "\\mathfrak m_R^{n + 1}")
    add("P11-E0220", 996, 996, "R/\\mathfrak m$", "R/\\mathfrak m_R$")
    add("P11-E0221", 1056, 1056, "$\\eta_n|_{\\Spec(R/\\mathfrak m^{n - 1})} \\cong \\eta_{n - 1}$", "$\\xi_n|_{\\Spec(R/\\mathfrak m^{n - 1})} \\cong \\xi_{n - 1}$")
    add("P11-E0221", 1057, 1057, "$F(\\eta_n) \\cong \\xi_n$", "$F(\\xi_n) \\cong \\eta_n$")
    add("P11-E0222", 1142, 1142, "fully faithfulness", "full faithfulness")
    add("P11-E0223", 1196, 1196, "Denote $x'$ the object", "Denote by $x'$ the object")
    add("P11-E0224", 1206, 1206, "product of spectra of Noetherian complete local rings", "product of Noetherian complete local rings")
    add("P11-E0225", 1207, 1207, "Denote $p_0, p_1", "Denote by $p_0, p_1")
    add("P11-E0226", 1208, 1208, "fully faithfulness", "full faithfulness")
    add("P11-E0227", 1216, 1216, "$x_n$", "$\\xi_n$")
    add("P11-E0228", 1315, 1315, "denote $\\mathfrak m'$ the kernel", "denote by $\\mathfrak m'$ the kernel")
    add("P11-E0229", 1368, 1368, "$a'_i, b'_i, c'_{ij}, k'_{ij} \\in B'$", "$a'_i, b'_i, c'_{ij}, k'_{ij} \\in B$")
    add("P11-E0230", 1379, 1379, "denote $\\mathfrak m_A$ the", "denote by $\\mathfrak m_A$ the")
    add("P11-E0231", 1422, 1422, "\\Lambda[x_1, \\ldots, x_n]", "\\Lambda[x_1, \\ldots, x_s]")
    add("P11-E0231", 1424, 1424, "\\Lambda[x_1, \\ldots, x_n]", "\\Lambda[x_1, \\ldots, x_s]")
    add("P11-E0232", 1502, 1502, "$x_i|_T \\cong T$", "$x_i|_T \\cong x$")
    add("P11-E0233", 1495, 1495, "$\\colim \\mathcal{X}_{T_i} \\to \\mathcal{X}_T$ is essentially surjective.", "$\\colim (\\mathcal{X} \\times_\\mathcal{Y} \\mathcal{Z})_{T_i} \\to\n(\\mathcal{X} \\times_\\mathcal{Y} \\mathcal{Z})_T$ is essentially surjective.")
    add("P11-E0233", 1511, 1512, "$\\colim \\mathcal{X}_{T_i} \\to \\mathcal{X}_T$\nis fully faithful in (2).", "$\\colim (\\mathcal{X} \\times_\\mathcal{Y} \\mathcal{Z})_{T_i} \\to\n(\\mathcal{X} \\times_\\mathcal{Y} \\mathcal{Z})_T$ is fully faithful in (2).")
    add("P11-E0234", 1551, 1551, "an affine scheme $V$ locally", "an affine scheme locally")
    add("P11-E0235", 1652, 1653, "Denote $x_0$\nthe pullback", "Denote by $x_0$\nthe pullback")
    add("P11-E0236", 1687, 1688, "With notation as in Definition \\ref{definition-versal}.\nLet $R", "With notation as in Definition \\ref{definition-versal}, let $R")
    add("P11-E0237", 1762, 1763, "with image $u_0$ such that\n$l/k = \\kappa(u_0)$ is finite.", "with image $u_0$, where\n$k = \\kappa(u_0)$ and $l/k$ is finite.")
    add("P11-E0238", 1833, 1834, "Denote $z_{l, 0}$, $v_{l, 0}$,\n$u_{l, 0}$, and $x_{l, 0}$ the objects", "Denote by $z_{l, 0}$, $v_{l, 0}$,\n$u_{l, 0}$, and $x_{l, 0}$ the objects")
    add("P11-E0239", 1953, 1953, "Let $\\mathcal{X} = \\mathcal{S}_F$ is the category", "Let $\\mathcal{X} = \\mathcal{S}_F$ be the category")
    add("P11-E0240", 1980, 1980, "(insert future reference here; see also discussion in", "(see also discussion in")
    add("P11-E0241", 2107, 2107, "Follows immediately from", "This follows immediately from")
    add("P11-E0242", 2117, 2117, "a $1$-morphisms", "a $1$-morphism")
    add("P11-E0243", 2124, 2124, "A reformulation of Lemma", "This is a reformulation of Lemma")
    add("P11-E0244", 2151, 2151, "\\times_{f, \\mathcal{X}, y}", "\\times_{f, \\mathcal{Y}, y}")
    add("P11-E0245", 2256, 2256, "is $\\leq$ than", "is $\\leq$")
    add("P11-E0246", 2288, 2288, "Denote $\\mathcal{X} = \\mathcal{S}_F$ the category", "Denote by $\\mathcal{X} = \\mathcal{S}_F$ the category")
    add("P11-E0247", 2306, 2306, "and functor $\\mathcal{C}_\\Lambda", "and functors $\\mathcal{C}_\\Lambda")
    add("P11-E0248", 2393, 2393, "is $\\leq$ than", "is $\\leq$")
    add("P11-E0249", 2460, 2460, "Denote $x_0$ the composition", "Denote by $x_0$ the composition")
    add("P11-E0250", 2559, 2560, "a finite type field over $S$. Denote $x_0 = y|_{\\Spec(k)}$\nthe pullback of $y$ by $v_0$.", "a finite type field over $S$. Set $x_0 = y|_{\\Spec(k)}$,\nthe pullback of $y$ by $v_0$.")
    add("P11-E0251", 2747, 2747, "a pair $(W, \\alpha)$", "a pair $(W, \\beta)$")
    add("P11-E0252", 2847, 2847, "morphism $\\alpha$", "morphism $\\beta$")
    add("P11-E0253", 2906, 2906, "comes the isomorphism", "comes from the isomorphism")
    add("P11-E0254", 2964, 2964, "be a finite type points", "be finite type points")
    add("P11-E0255", 3011, 3011, "a pair $(W, \\alpha)$", "a pair $(W, \\beta)$")
    add("P11-E0256", 3134, 3134, "comes the isomorphism", "comes from the isomorphism")
    add("P11-E0257", 3172, 3172, "of an category", "of a category")
    add("P11-E0258", 3256, 3256, "we denote $A[M]$ the $A$-algebra", "we denote by $A[M]$ the $A$-algebra")
    add("P11-E0259", 3418, 3418, "and let $M \\to N$ an $A$-linear map", "and let $M \\to N$ be an $A$-linear map")
    add("P11-E0260", 3499, 3500, "we ask the corresponding maps between\nthe kernels", "we ask that the corresponding maps between\nthe kernels")
    add("P11-E0261", 3517, 3517, "Denote $x, y, z$ the objects", "Denote by $x, y, z$ the objects")
    add("P11-E0261", 3518, 3518, "you get from $w$", "obtained from $w$")
    add("P11-E0262", 3640, 3640, "we can pullback $\\alpha$", "we can pull back $\\alpha$")
    add("P11-E0263", 3682, 3683, "and an $A$-linear\nmap $M \\to N$ an induced", "and an $A$-linear\nmap $M \\to N$ there is an induced")
    add("P11-E0264", 3707, 3707, "$\\mathcal{O}_x(A')$", "$\\mathcal{O}_x(I)$")
    add("P11-E0265", 3729, 3729, "We will develop this theory later (insert future reference here).", "We will develop this theory later.")
    add("P11-E0266", 3766, 3766, "Denote $M_n =", "Set $M_n =")
    add("P11-E0270", 3770, 3770, "(r_1, r_2, r_3 \\ldots)", "(r_1, r_2, r_3, \\ldots)")
    add("P11-E0271", 3794, 3795, "There exists\nelements", "There exist\nelements")
    add("P11-E0267", 3834, 3834, "$o_x(A') \\in \\mathcal{O}_x(A)$", "$o_x(A') \\in \\mathcal{O}_x(I)$")
    add("P11-E0268", 3862, 3862, "Denote $I$ the kernel", "Denote by $I$ the kernel")
    add("P11-E0269", 3867, 3867, "\\mathcal{O}_x(A')", "\\mathcal{O}_x(I)")
    add("P11-E0272", 3947, 3947, "be morphism of $D^{-}(A)$", "be a morphism of $D^{-}(A)$")
    add("P11-E0273", 3966, 3966, "\\Ker(A'' \\to A)", "\\Ker(A'' \\to A_f)")
    add("P11-E0274", 4054, 4054, "Assume that $x$ versal", "Assume that $x$ is versal")
    add("P11-E0275", 4063, 4063, "be kernel of the surjective map", "be the kernel of the surjective map")
    add("P11-E0276", 4085, 4085, "Assume that $x$ versal", "Assume that $x$ is versal")
    add("P11-E0280", 4087, 4087, "\\text{Ext}^0_A(E, k)", "\\Ext^0_A(E, k)")
    add("P11-E0280", 4094, 4094, "\\text{Ext}^0_A(E, k)", "\\Ext^0_A(E, k)")
    add("P11-E0277", 4107, 4109, "$H^0(E \\otimes_A^\\mathbf{L} k) \\to\nH^0(\\NL_{A/\\Lambda} \\otimes_A^\\mathbf{L} k)$\ninjective.", "$H^0(E \\otimes_A^\\mathbf{L} k) \\to\nH^0(\\NL_{A/\\Lambda} \\otimes_A^\\mathbf{L} k)$\nis injective.")
    add("P11-E0278", 4202, 4202, "a map $\\xi_x : E \\to", "a map $\\xi_x : E_x \\to")
    add("P11-E0279", 4247, 4247, "\\Hom_A(E_x, \\NL_{A/\\Lambda})", "\\Hom_A(E_x, \\NL_{A/A'})")
    add("P11-E0280", 4283, 4283, "\\text{Ext}^i_B(E_y, k)", "\\Ext^i_B(E_y, k)")
    add("P11-E0281", 4292, 4292, "(\\Sch/S)_{fppf}^{opp}", "(\\Sch/S)_{fppf}")
    add("P11-E0285", 4400, 4400, "In Situation \\ref{situation-dual}. Assume furthermore that", "In Situation \\ref{situation-dual}, assume furthermore that")
    add("P11-E0282", 4425, 4425, "Choose a $\\alpha", "Choose an $\\alpha")
    add("P11-E0283", 4443, 4443, "denote $x_C$ the", "denote by $x_C$ the")
    add("P11-E0284", 4518, 4518, "and denote $\\xi :", "and denote by $\\xi :")
    add("P11-E0286", 4558, 4558, "category $\\Sch_\\alpha/S$. Denote", "category $\\Sch_\\alpha/S$. Denote by")
    add("P11-E0287", 4674, 4674, "Denote $a : F \\to G$ the restriction", "Denote by $a : F \\to G$ the restriction")
    add("P11-E0288", 4695, 4695, "Denote $V' = V$ but viewed as", "Set $V' = V$, viewed as")
    add("P11-E0289", 4728, 4729, "Compatibility of the glueing maps with the maps\n$X_W \\to F'$ provide", "Compatibility of the glueing maps with the maps\n$X_W \\to F'$ provides")
    add("P11-E0290", 4742, 4742, "over an Noetherian scheme", "over a Noetherian scheme")
    add("P11-E0291", 4744, 4744, "Denote $V_i = V'_i$ but viewed as", "Set $V_i = V'_i$, viewed as")
    add("P11-E0292", 4745, 4746, "As $G'$\nis limit preserving can choose", "As $G'$\nis limit preserving, we can choose")
    add("P11-E0293", 4763, 4763, "Denote $X'_i = X_i$ but viewed as", "Set $X'_i = X_i$, viewed as")
    add("P11-E0294", 4765, 4765, "and the functors of points $h_{X'_i}$", "and the functor of points $h_{X'_i}$")
    add("P11-E0295", 4805, 4805, "$(\\textit{Noetherian}/S)_\\etale^{opp}$", "$(\\textit{Noetherian}/S)_\\etale$")
    add("P11-E0296", 4838, 4838, "This is axiom that the every formal object", "This is the axiom that every formal object")
    add("P11-E0297", 4877, 4877, "have the same underlying categories", "have the same underlying category")
    add("P11-E0298", 5007, 5007, "and $\\hat x$", "and $\\hat x'$")
    add("P11-E0299", 5033, 5033, "we are going use", "we are going to use")
    add("P11-E0300", 5052, 5052, "should induces a", "should induce a")
    add("P11-E0301", 5072, 5072, "(X'_{T'})^{rig}", "(X'_{/T'})^{rig}")
    add("P11-E0302", 5086, 5086, "a morphism $\\varphi", "morphism $\\varphi")
    add("P11-E0303", 5134, 5135, "we can take $\\hat x'$\nthe completion", "we can take $\\hat x'$ to be\nthe completion")
    add("P11-E0304", 5181, 5181, "which can served as", "which can serve as")
    add("P11-E0305", 5184, 5184, "Denote $h_X(-) = \\Mor_S(-, X)$ the functor", "Denote by $h_X(-) = \\Mor_S(-, X)$ the functor")
    add("P11-E0306", 5200, 5200, "$x_{/Z} :", "$\\tilde x_{/Z} :")
    add("P11-E0307", 5203, 5203, "V'_{/Z'}", "V'_{/Z}")
    add("P11-E0308", 5217, 5217, "pulls $T$ back to $Z$", "pulls $T$ back to $Z$.")
    add("P11-E0309", 5236, 5237, "In Situation \\ref{situation-contractions}.\nLet $V$", "In Situation \\ref{situation-contractions}, let $V$")
    add("P11-E0310", 5277, 5278, "$E'_{/Z} \\to E_W$\nis a triple", "$E'_{/Z} \\to E_W$\nform a triple")
    add("P11-E0311", 5342, 5343, "). Denote\n$J'' =", "). Set\n$J'' =")
    add("P11-E0312", 5431, 5431, "V_i", "V_\\lambda")
    add("P11-E0313", 5449, 5449, "after increasing $i$", "after increasing $\\lambda$")
    add("P11-E0314", 5455, 5456, "and\nand denote $Z$", "and\ndenote $Z$")
    add("P11-E0315", 5482, 5482, "morpisms", "morphisms")
    add("P11-E0316", 5548, 5548, "some an \\'etale morphism", "an \\'etale morphism")
    add("P11-E0317", 5551, 5551, "$\\xi|_U = \\tilde \\xi_\\lambda|_U$", "$\\xi|_{\\tilde V} = \\tilde \\xi_\\lambda|_{\\tilde V}$")
    add("P11-E0318", 5605, 5605, "with a finite affine \\'etale coverings", "with finite affine \\'etale coverings")
    add("P11-E0319", 5627, 5628, "Denote\n$\\tilde T' \\subset |\\tilde X'|$ the inverse image", "Let\n$\\tilde T' \\subset |\\tilde X'|$ denote the inverse image")
    add("P11-E0319", 5629, 5629, "Denote $\\tilde U' \\subset \\tilde X'$ the complementary", "Let $\\tilde U' \\subset \\tilde X'$ denote the complementary")
    add("P11-E0319", 5630, 5630, "Denote ", "Let ")
    add("P11-E0319", 5631, 5631, "the formal modification", "denote the formal modification")
    add("P11-E0320", 5630, 5630, "$\\tilde g' :", "$\\tilde g :")
    add("P11-E0321", 5638, 5638, "Denote $\\tilde F$ the functor", "Let $\\tilde F$ denote the functor")
    add("P11-E0322", 5652, 5652, "Denote $\\tilde Z \\subset \\tilde V$ the inverse image", "Let $\\tilde Z \\subset \\tilde V$ denote the inverse image")
    add("P11-E0323", 5677, 5677, "morphsms", "morphisms")
    add("P11-E0323", 5678, 5678, "and show this works", "and shows this works")
    add("P11-E0324", 5754, 5755, "Denote $I_\\mu \\subset A_\\mu$ and $I \\subset A$\nthe ideals", "Let $I_\\mu \\subset A_\\mu$ and $I \\subset A$\ndenote the ideals")
    add("P11-E0325", 5797, 5797, "kernel and cokernel of $A \\to C$ is supported", "kernel and cokernel of $A \\to C$ are supported")
    add("P11-E0326", 5806, 5808, "Denote $Z_n \\subset V$ the $n$th infinitesimal\nneighbourhood of $Z$ and denote $Z_{\\mu, n} \\subset V_\\mu$\nthe $n$th infinitesimal neighbourhood of $Z_\\mu$.", "Let $Z_n \\subset V$ and $Z_{\\mu, n} \\subset V_\\mu$ denote\nthe respective $n$th infinitesimal neighbourhoods of $Z$ and $Z_\\mu$.")
    add("P11-E0327", 5819, 5819, "are the completion with", "are the completions with")
    add("P11-E0328", 5834, 5834, "$V' \\to V$, $\\hat x'$, $x'$ witnesses", "$V' \\to V$, $\\hat x'$, $x'$ witness")
    add("P11-E0329", 5882, 5882, "$\\Coker(\\alpha)$", "$\\Coker(A \\to C)$")
    add("P11-E0330", 5891, 5891, "(b_1)$", "(b_j)$")
    add("P11-E0331", 5968, 5968, "spetruim", "spectrum")
    add("P11-E0332", 6106, 6109, "Then finally\nsetting $u' : V \\setminus Z \\to X'$ the restriction of $x'$ to\n$V \\setminus Z \\subset V'$ gives the third component of our\ndesired element $(Z, u', \\hat x) \\in F(V)$.", "Finally,\nset $u' : V \\setminus Z \\to U'$ to be the restriction of $x'$ to\n$V \\setminus Z \\subset V'$; this gives the second component of our\ndesired element $(Z, u', \\hat x) \\in F(V)$.")
    add("P11-E0333", 6135, 6135, "\\times_{\\hat x, W}", "\\times_{g, W}")
    add("P11-E0334", 6137, 6137, "Smoothness of $V \\to W$", "Smoothness of $g : V_{/Z} \\to W$")
    add("P11-E0335", 6195, 6195, "Denote $\\mathfrak m_1 \\subset A_1$ the maximal ideal", "Let $\\mathfrak m_1 \\subset A_1$ denote the maximal ideal")
    add("P11-E0336", 6215, 6215, "which is a a finite type", "which is a finite type")
    add("P11-E0337", 6229, 6229, "Hence $A_n \\to B_n$ is smooth", "Hence $B_n \\to A_n$ is smooth")
    add("P11-E0338", 6254, 6254, "the set of a points", "the set of points")
    add("P11-E0339", 6337, 6337, "separated case to the triples", "separated case to the triple")
    return rows


def bounded_offset(authority: bytes, operation: dict) -> tuple[int, int, int, int]:
    start_line = operation["source_start_line"]
    end_line = operation["source_end_line"]
    starts = [0]
    starts.extend(index + 1 for index, byte in enumerate(authority) if byte == 10)
    region_start = starts[start_line - 1]
    region_end = starts[end_line] if end_line < len(starts) else len(authority)
    old = operation["old_text"].encode("utf-8")
    region = authority[region_start:region_end]
    positions: list[int] = []
    cursor = 0
    while True:
        position = region.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + 1
    if len(positions) != 1:
        raise AssertionError(
            f"{operation['producer_id']}: preimage count on lines {start_line}-{end_line} "
            f"is {len(positions)} for {operation['old_text']!r}"
        )
    start = region_start + positions[0]
    end = start + len(old)
    actual_start_line = authority[:start].count(b"\n") + 1
    actual_end_line = authority[: max(start, end - 1)].count(b"\n") + 1
    return start, end, actual_start_line, actual_end_line


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic R25 Artin source-intake inputs.")
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--producer-ledger", type=Path, required=True)
    args = parser.parse_args()

    authority = args.authority.read_bytes()
    producer_ledger = args.producer_ledger.read_bytes()
    if len(authority) != AUTHORITY_BYTES or sha_bytes(authority) != AUTHORITY_SHA256:
        raise AssertionError("frozen artin.tex authority mismatch")
    if b"\r" in authority or not authority.endswith(b"\n"):
        raise AssertionError("authority must be LF-only UTF-8 with terminal LF")
    if len(producer_ledger) != PRODUCER_LEDGER_BYTES or sha_bytes(producer_ledger) != PRODUCER_LEDGER_SHA256:
        raise AssertionError("frozen p11 producer ledger mismatch")

    all_rows = load_jsonl(args.producer_ledger)
    producer_rows = [
        row for row in all_rows
        if re.fullmatch(r"P11-E\d{4}", row.get("id", ""))
        and 200 <= int(row["id"][5:]) <= 339
    ]
    expected_producer_ids = [f"P11-E{number:04d}" for number in range(200, 340)]
    if [row["id"] for row in producer_rows] != expected_producer_ids:
        raise AssertionError("producer packet is not exact contiguous P11-E0200..0339")
    if any(row["source_sha256"] != AUTHORITY_SHA256 for row in producer_rows):
        raise AssertionError("producer source identity mismatch")

    operations_by_producer = operation_table()
    accepted_ids = [producer_id for producer_id in expected_producer_ids if producer_id not in REJECTED_IDS]
    if set(operations_by_producer) != set(accepted_ids):
        missing = sorted(set(accepted_ids) - set(operations_by_producer))
        extra = sorted(set(operations_by_producer) - set(accepted_ids))
        raise AssertionError(f"operation closure mismatch; missing={missing}; extra={extra}")

    merged_members = {member for group in MERGE_GROUPS for member in group}
    groups: list[list[str]] = []
    for producer_id in accepted_ids:
        if producer_id in merged_members:
            group = next(group for group in MERGE_GROUPS if producer_id in group)
            if group not in groups:
                groups.append(group)
        else:
            groups.append([producer_id])

    def first_line(group: list[str]) -> int:
        return min(op["source_start_line"] for producer_id in group for op in operations_by_producer[producer_id])

    groups.sort(key=lambda group: (first_line(group), group[0]))
    if len(groups) != 131:
        raise AssertionError(f"expected 131 semantic units, observed {len(groups)}")

    row_by_id = {row["id"]: row for row in producer_rows}
    accepted: list[dict] = []
    operation_spec_rows: list[dict] = []
    source_map_rows: list[dict] = []
    stable_rows: list[dict] = []
    all_intervals: list[tuple[int, int, str]] = []
    for stable_id, producer_ids in zip(EXPECTED_IDS, groups):
        mapped_operations: list[dict] = []
        flat_operations = [op for producer_id in producer_ids for op in operations_by_producer[producer_id]]
        for operation_index, operation in enumerate(flat_operations, 1):
            start, end, actual_start_line, actual_end_line = bounded_offset(authority, operation)
            if (actual_start_line, actual_end_line) != (
                operation["source_start_line"], operation["source_end_line"]
            ):
                raise AssertionError(f"{operation['producer_id']}: exact line metadata mismatch")
            old = operation["old_text"].encode("utf-8")
            replacement = operation["replacement_text"].encode("utf-8")
            operation_id = f"{stable_id}-OP{operation_index}"
            mapped = {
                **operation,
                "operation_id": operation_id,
                "start_byte": start,
                "end_byte_exclusive": end,
                "occurrence_count_in_frozen_authority": authority.count(old),
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
            }
            mapped_operations.append(mapped)
            operation_spec_rows.append({
                "stable_id": stable_id,
                "semantic_unit_producer_id": producer_ids[0],
                "operation_index": operation_index,
                **mapped,
            })
            all_intervals.append((start, end, operation_id))

        loci = sorted({line for op in flat_operations for line in (op["source_start_line"], op["source_end_line"])})
        locus = f"artin.tex:{loci[0]}" if loci[0] == loci[-1] else f"artin.tex:{loci[0]}-{loci[-1]}"
        rationale = " ".join(row_by_id[producer_id]["defect"] for producer_id in producer_ids)
        unit = {
            "stable_id": stable_id,
            "producer_ids": producer_ids,
            "class": "source_defect_correction",
            "locus": locus,
            "operations": flat_operations,
            "rationale": rationale,
        }
        accepted.append(unit)
        operation_ids = [op["operation_id"] for op in mapped_operations]
        stable_rows.append({
            "class": unit["class"],
            "id": stable_id,
            "locus": locus,
            "operation_ids": operation_ids,
            "payload": "payload/artin.tex",
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "artin.tex",
            "status": "provisional_accepted_not_admitted",
        })
        source_map_rows.append({
            "schema": "mathematics-commons-stacks-errata-map/v2",
            "unit_id": stable_id,
            "producer_id": producer_ids[0],
            "producer_ids": producer_ids,
            "source": "artin.tex",
            "authority": "authority/source/artin.tex",
            "authority_sha256": AUTHORITY_SHA256,
            "payload": "payload/artin.tex",
            "locus": locus,
            "class": unit["class"],
            "proof": "accepted_after_independent_frozen_authority_replay",
            "prior_aliases": [],
            "adverse_evidence": "Producer rows are allegation evidence only; the frozen authority, exact bounded preimages, and independent adjudication are controlling.",
            "operations": mapped_operations,
        })

    ascending = sorted(all_intervals)
    for left, right in zip(ascending, ascending[1:]):
        if left[1] > right[0]:
            raise AssertionError(f"overlapping operations: {left[2]} / {right[2]}")
    if [min(op["start_byte"] for op in row["operations"]) for row in source_map_rows] != sorted(
        min(op["start_byte"] for op in row["operations"]) for row in source_map_rows
    ):
        raise AssertionError("stable units do not follow first physical source locus")

    payload = authority
    for start, end, operation_id in sorted(all_intervals, reverse=True):
        operation = next(row for row in operation_spec_rows if row["operation_id"] == operation_id)
        old = operation["old_text"].encode("utf-8")
        replacement = operation["replacement_text"].encode("utf-8")
        if payload[start:end] != old:
            raise AssertionError(f"descending replay mismatch: {operation_id}")
        payload = payload[:start] + replacement + payload[end:]

    sanitized_producer_rows: list[dict] = []
    for row in producer_rows:
        sanitized = dict(row)
        sanitized["source_path"] = "artin.tex"
        sanitized_producer_rows.append(sanitized)
    write_jsonl(ROOT / "P11_ARTIN_ERRATA_R25.input.jsonl", sanitized_producer_rows)

    rejected_rows: list[dict] = []
    rejection_reasons = {
        "P11-E0202": "Rejected as a permissible deictic use of 'that category'; replacing it by 'the category' is an optional editorial preference, not a certain defect.",
        "P11-E0215": "Rejected because the proposed comma after the embedded section-reference modifier is optional punctuation and its absence does not impair the sentence.",
        "P11-E0217": "Rejected because 'deformation space associated to' is intelligible informal prose in context; replacing it by 'deformation category' is not compelled by the authority.",
    }
    rejection_classes = {
        "P11-E0202": "permissible_deictic_wording_not_source_defect",
        "P11-E0215": "optional_punctuation_not_source_defect",
        "P11-E0217": "intelligible_informal_terminology_not_source_defect",
    }
    rejection_operations = {
        "P11-E0202": {
            "producer_id": "P11-E0202",
            "source_start_line": 131,
            "source_end_line": 131,
            "old_text": "that category",
            "replacement_text": "the category",
        },
        "P11-E0215": {
            "producer_id": "P11-E0215",
            "source_start_line": 822,
            "source_end_line": 823,
            "old_text": "Section \\ref{section-predeformation-categories}\nthe tangent",
            "replacement_text": "Section \\ref{section-predeformation-categories},\nthe tangent",
        },
        "P11-E0217": {
            "producer_id": "P11-E0217",
            "source_start_line": 914,
            "source_end_line": 915,
            "old_text": "deformation\nspace associated to",
            "replacement_text": "deformation\ncategory associated to",
        },
    }
    for producer_id in REJECTED_IDS:
        row = row_by_id[producer_id]
        proposed = rejection_operations[producer_id]
        start, end, actual_start_line, actual_end_line = bounded_offset(authority, proposed)
        if (actual_start_line, actual_end_line) != (
            proposed["source_start_line"], proposed["source_end_line"]
        ):
            raise AssertionError(f"{producer_id}: rejected proposal line metadata mismatch")
        old = proposed["old_text"].encode("utf-8")
        replacement = proposed["replacement_text"].encode("utf-8")
        rejected_rows.append({
            "schema": "mathematics-commons-stacks-errata-rejection/v1",
            "producer_id": producer_id,
            "producer_ids": [producer_id],
            "source": "artin.tex",
            "locus": (
                f"artin.tex:{proposed['source_start_line']}"
                if proposed["source_start_line"] == proposed["source_end_line"]
                else f"artin.tex:{proposed['source_start_line']}-{proposed['source_end_line']}"
            ),
            "class": rejection_classes[producer_id],
            "result": "rejected_after_independent_authority_review",
            "rationale": rejection_reasons[producer_id],
            "prior_aliases": [],
            "proposed_operation": {
                "source_start_line": proposed["source_start_line"],
                "source_end_line": proposed["source_end_line"],
                "old_text": proposed["old_text"],
                "replacement_text": proposed["replacement_text"],
                "start_byte": start,
                "end_byte_exclusive": end,
                "old_bytes": len(old),
                "old_sha256": sha_bytes(old),
                "replacement_bytes": len(replacement),
                "replacement_sha256": sha_bytes(replacement),
                "applied": False,
            },
        })

    spec = {
        "schema": "mathematics-commons-stacks-r25-adjudication-spec/v1",
        "candidate_id": "stacks-errata-a04446e-r25",
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "authority_path": AUTHORITY_PATH,
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_source": "P11_ARTIN_ERRATA_R25.input.jsonl",
        "producer_ledger_bytes": len(producer_ledger),
        "producer_ledger_sha256": sha_bytes(producer_ledger),
        "producer_global_ledger_at_intake_bytes": PRODUCER_GLOBAL_LEDGER_AT_INTAKE_BYTES,
        "producer_global_ledger_at_intake_sha256": PRODUCER_GLOBAL_LEDGER_AT_INTAKE_SHA256,
        "producer_row_count": 140,
        "accepted_producer_row_count": 137,
        "rejected_producer_row_count": 3,
        "semantic_unit_count": len(accepted),
        "operation_count": len(operation_spec_rows),
        "stable_id_range": [EXPECTED_IDS[0], EXPECTED_IDS[-1]],
        "deduplication": {
            "admitted_units_reviewed": 678,
            "prior_rounds": "root/R1 and R2-R24",
            "matching_artin_units": 0,
            "result": "accepted_units_new; three style_or_terminology_proposals_rejected",
        },
        "accepted": accepted,
        "rejected": rejected_rows,
        "unresolved": [],
    }
    spec_path = ROOT / "R25_ARTIN_ADJUDICATION_SPEC.input.json"
    write_json(spec_path, spec)
    spec_bytes = spec_path.read_bytes()

    lease = json.loads((ROOT / "LEASE.json").read_text(encoding="utf-8"))
    flattened_producers = [producer for unit in accepted for producer in unit["producer_ids"]]
    config_input = {
        "schema": "mathematics-commons-stacks-errata-candidate-config-input/v1",
        "candidate_id": spec["candidate_id"],
        "authority_commit": AUTHORITY_COMMIT,
        "authority_tree": AUTHORITY_TREE,
        "namespace": lease["namespace"],
        "writer_task": lease["writer_task"],
        "lease_id": lease["lease_id"],
        "accepted": 131,
        "rejected": 3,
        "unresolved": 0,
        "operation_count": len(operation_spec_rows),
        "expected_unit_ids": EXPECTED_IDS,
        "expected_producer_ids": [unit["producer_ids"][0] for unit in accepted],
        "expected_all_producer_ids": flattened_producers,
        "rejected_producer_ids": REJECTED_IDS,
        "intentionally_absent_producer_ids": [],
        "payload_expected_bytes": len(payload),
        "payload_expected_sha256": sha_bytes(payload),
        "build_render_admission_status": "not_run_by_source_materialization",
    }
    operation_spec = {
        "schema": "mathematics-commons-stacks-errata-operation-spec/v1",
        "authority_sha256": AUTHORITY_SHA256,
        "operations": operation_spec_rows,
    }
    stable_units = {
        "schema": "mathematics-commons-stacks-errata-units/v1",
        "authority_commit": AUTHORITY_COMMIT,
        "unit_count": len(stable_rows),
        "units": stable_rows,
    }
    decisions = [
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0001","timestamp_utc":GENERATED_AT,"choice":"Bind R25 to frozen artin.tex at commit a04446e57ec1fbc252a871afcec7752fb2807b14 without changing R24.","rationale":"Preserves immutable authority and the completed MC-STK-ERR-1008..1045 assignment.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0002","timestamp_utc":GENERATED_AT,"choice":"Assign MC-STK-ERR-1046..1176 to 131 accepted semantic units in first-locus physical source order.","rationale":"The range begins immediately after R24 and contains no reused or skipped stable ID.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0003","timestamp_utc":GENERATED_AT,"choice":"Merge the six linked producer groups sealed in the R25 adjudication specification.","rationale":"Each group records repeated or jointly typed loci of one bounded semantic defect and consumes one canon ID.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0004","timestamp_utc":GENERATED_AT,"choice":"Accept 137 producer identities, reject P11-E0202, P11-E0215, and P11-E0217, and leave none unresolved.","rationale":"Every accepted allegation replays against its exact frozen-authority locus; the rejected rows are optional style or terminology preferences rather than certain defects.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0005","timestamp_utc":GENERATED_AT,"choice":"Use only the exact old/new operations sealed in R25_ARTIN_ADJUDICATION_SPEC.input.json, including the independently refined placeholder, RS-target, restriction, cokernel, and smoothness repairs.","rationale":"This prevents broad replacement and binds every correction to a unique authority preimage.","supersedes":None},
        {"schema":"mathematics-commons-stacks-candidate-decision/v1","id":"ERR-R25-D0006","timestamp_utc":GENERATED_AT,"choice":"Materialize and statically replay the source candidate only; leave build, render, admission, registry, Git, publication, and generated-source transitions unexecuted.","rationale":"This produces the bounded deterministic candidate requested for later gates.","supersedes":None},
    ]
    validation = {
        "schema": "mathematics-commons-stacks-r25-intake-validation/v1",
        "status": "PASS",
        "authority_bytes": len(authority),
        "authority_sha256": sha_bytes(authority),
        "producer_ledger_bytes": len(producer_ledger),
        "producer_ledger_sha256": sha_bytes(producer_ledger),
        "adjudication_spec_bytes": len(spec_bytes),
        "adjudication_spec_sha256": sha_bytes(spec_bytes),
        "semantic_units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "accepted_producer_ids": len(flattened_producers),
        "rejected_producer_ids": len(REJECTED_IDS),
        "unresolved": 0,
        "stable_id_first": EXPECTED_IDS[0],
        "stable_id_last": EXPECTED_IDS[-1],
        "r24_predecessor_stable_id_last": "MC-STK-ERR-1045",
        "stable_ids_unique_and_contiguous": True,
        "stable_ids_follow_first_physical_source_locus": True,
        "bounded_preimages_unique_on_declared_lines": True,
        "operations_nonoverlapping": True,
        "payload_preview_bytes": len(payload),
        "payload_preview_sha256": sha_bytes(payload),
        "merged_producer_groups": MERGE_GROUPS,
        "rejected_ids": REJECTED_IDS,
        "closure": {
            "all_140_producer_ids_accounted_for_exactly_once": True,
            "operation_ids_equal_stable_unit_operation_ids": True,
            "source_map_units_equal_stable_units": True,
            "accepted_rejected_and_unresolved_disjoint": True,
        },
        "r24_touched": False,
        "prohibited_transitions_executed": [],
    }
    review = f"""# R25 Artin intake review

This source-only intake binds 131 accepted semantic units and {len(operation_spec_rows)} exact operations to frozen `artin.tex` at commit `{AUTHORITY_COMMIT}`. The stable range is contiguous from `MC-STK-ERR-1046` through `MC-STK-ERR-1176` in first-locus physical source order.

The packet contains exactly 140 producer identities `P11-E0200` through `P11-E0339`. Independent review accepts 137 identities, rejects `P11-E0202`, `P11-E0215`, and `P11-E0217` as optional style or terminology proposals, merges six linked pairs, and leaves no row unresolved. No predecessor unit through R24 names `artin.tex`.

Every accepted old-text preimage occurs exactly once on its declared authority line interval. All UTF-8 byte intervals are pairwise nonoverlapping and replay deterministically in descending byte order. The exact audit refinements delete unresolved placeholders while retaining valid surrounding references, repair the three genuine RS targets, name the fibre-product functor in both the essential-surjectivity and full-faithfulness steps, normalize every repeated `\\Ext` operator in the affected map, use the standing input objects before constructing outputs, restrict both sides to `\\tilde V`, define `\\tilde g` consistently, identify the cokernel as `\\Coker(A \\to C)`, give `u'` the required codomain `U'`, and use the standing map `g` in the final fibre-product smoothness argument.

No TeX build, render, candidate admission, registry mutation, Git operation, publication, or generated-source composition is performed by this source-materialization stage.
"""

    write_json(ROOT / "candidate.config.input.json", config_input)
    write_json(ROOT / "operation-spec.input.json", operation_spec)
    write_json(ROOT / "stable-units.input.json", stable_units)
    write_jsonl(ROOT / "source-map.input.jsonl", source_map_rows)
    write_jsonl(ROOT / "decisions.input.jsonl", decisions)
    write_jsonl(ROOT / "rejections.input.jsonl", rejected_rows)
    write_json(ROOT / "INTAKE_VALIDATION.json", validation)
    (ROOT / "R25_ARTIN_REVIEW.md").write_text(review, encoding="utf-8", newline="")

    print(json.dumps({
        "passed": True,
        "units": len(stable_rows),
        "operations": len(operation_spec_rows),
        "accepted_producer_ids": len(flattened_producers),
        "rejected_producer_ids": len(REJECTED_IDS),
        "payload_bytes": len(payload),
        "payload_sha256": sha_bytes(payload),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
