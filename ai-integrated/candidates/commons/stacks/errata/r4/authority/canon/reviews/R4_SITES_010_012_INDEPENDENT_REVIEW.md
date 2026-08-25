# Independent R4 review: SITES-010–012

Date: 2026-08-22  
Review scope: three frozen Sites hypotheses only  
Disposition authority: this review establishes whether the hypotheses are supportable for the derived English-AI errata queue. It does **not** alter or certify the frozen Stacks authority, any translation, or any candidate payload.

## Recomputed inputs

- Frozen authority: `upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/sites.tex`
  - bytes: `424197`
  - SHA-256: `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
  - relevant authority commit encoded in the path: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- Frozen intake: `canon/control/ERRATA_R4_SUPPLEMENT_SITES_010_012_20260822.json`
  - bytes: `3084`
  - SHA-256: `26C8AF31EB3315E1BC2141CC603997B398568ABDBB6897345F06AF39FE971DF8`

Both identities exactly match the expected identities supplied for this review. Decisions below come from reopening the authority contexts, not from accepting the intake claims.

## Aggregate result

| ID | Disposition | Exact defective locus | Smallest accepted replacement |
|---|---|---|---|
| SITES-010 | **ACCEPTED** | `sites.tex:1272–1274`, specifically line 1273 | `U_{\alpha(i)} \times_U U_{\alpha(i')}` → `U_{\alpha(j)} \times_U U_{\alpha(j')}` |
| SITES-011 | **ACCEPTED** | `sites.tex:2200` | `of $\mathcal{D}$` → `of $\mathcal{C}$` |
| SITES-012 | **ACCEPTED** | `sites.tex:267` | `\Ob(C)` → `\Ob(\mathcal{C})` |

Aggregate: **3 ACCEPTED, 0 REJECTED, 0 DEFERRED**.

## SITES-010 — ACCEPTED

### Exact context and type check

The lemma declares at `sites.tex:1247–1250`:

- two families `\mathcal V = \{V_j \to U\}_{j\in J}` and `\mathcal U = \{U_i \to U\}_{i\in I}`;
- a function `\alpha:J\to I`; and
- for each `j\in J`, a morphism `f_j:V_j\to U_{\alpha(j)}` over `U`.

The proof then fixes `j,j'\in J` and invokes the morphism induced by `f_j` and `f_{j'}` on fibre products (`sites.tex:1271–1274`). The universal property gives exactly

`f_j \times_U f_{j'} : V_j\times_U V_{j'} \longrightarrow U_{\alpha(j)}\times_U U_{\alpha(j')}`.

The printed target at line 1273 instead uses `\alpha(i)` and `\alpha(i')`. This fails in two independent ways:

1. The morphism named `f_{jj'}` must be determined by `f_j` and `f_{j'}`, so its two target factors must be their respective codomains `U_{\alpha(j)}` and `U_{\alpha(j')}`.
2. Here `\alpha` has domain `J`, while the preceding dummy indices `i,i'` range over `I` at lines 1268–1269. Thus `\alpha(i)` and `\alpha(i')` are not even typed from the declared data. They also are not bound as functions of the fixed pair `j,j'` in the sentence defining `f_{jj'}`.

The following equalities at lines 1277–1279 independently confirm the intended codomain: both pullbacks are explicitly from sections restricted to `U_{\alpha(j)}\times_U U_{\alpha(j')}`. Those pullbacks would be typed only when `f_{jj'}` has that same target.

### Adverse evidence considered

The immediately preceding sentence uses arbitrary `i,i'\in I`, which could tempt a reader to treat them as still available. That does not rescue the formula: `\alpha:J\to I` cannot generally be applied to members of `I`, and arbitrary `i,i'` do not encode the fixed `j,j'` whose maps induce `f_{jj'}`. No alternative convention in the reopened local context changes the declared variance.

### Smallest correction

At line 1273 replace only

`U_{\alpha(i)} \times_U U_{\alpha(i')}`

with

`U_{\alpha(j)} \times_U U_{\alpha(j')}`.

No surrounding proof change is required.

## SITES-011 — ACCEPTED

### Exact context and ambient-category check

The governing lemma at `sites.tex:2182–2187` starts `Let $\mathcal C$ be a site`, puts `\mathcal F` and `\mathcal G` on `\mathcal C`, and defines `\mathcal B` as a collection of objects in `\Ob(\mathcal C)`. Its proof fixes `U\in\Ob(\mathcal C)` at line 2191. At lines 2193–2201 it explicitly invokes `lemma-sections-sheafification`.

That cited lemma, at `sites.tex:2155–2175`, also has the sole ambient site `\mathcal C`; its clause (2) says verbatim that `\{U_{ijk}\to U_i\times_U U_j\}` is a covering **of `\mathcal C`** (`sites.tex:2167–2169`). The proof under review repeats that clause but prints **of `\mathcal D`** at line 2200.

No `\mathcal D` is introduced in the statement or proof of `lemma-isomorphism-sheafifications`. The objects `U`, `U_i`, `U_j`, and `U_{ijk}`, the presheaves, and the covering operations throughout this local argument all live on `\mathcal C`. Therefore the printed category identifier is both locally unbound and inconsistent with the cited result being applied.

### Adverse evidence considered

The authority file uses `\mathcal D` in other, separate lemmas about functors between two categories or sites. Those declarations do not bind `\mathcal D` in this standalone lemma and proof. There is no two-site construction at this locus, so reading line 2200 as an intentional second ambient site has no typed support.

### Smallest correction

At line 2200 replace only

`of $\mathcal{D}$`

with

`of $\mathcal{C}$`.

## SITES-012 — ACCEPTED

### Exact context and ambient-category check

The lemma at `sites.tex:253–262` declares `\mathcal C` to be a category and declares `\varphi:\mathcal F\to\mathcal G` to be a morphism of presheaves on `\mathcal C`. The construction in its proof defines

`\mathcal G'(U)=\varphi_U(\mathcal F(U))`

for every object `U` of the presheaves' domain. Such a `U` must therefore lie in `\Ob(\mathcal C)`. Line 267 instead prints `U\in\Ob(C)`, where plain italic `C` is not the category declared by the lemma and is not otherwise introduced in this local context.

This is not merely a preference for calligraphic typography: `\mathcal C` is the actual domain of `\mathcal F` and `\mathcal G`, so membership in its object class is required for `\mathcal F(U)`, `\mathcal G(U)`, and `\varphi_U` to be defined. The same section consistently uses `\Ob(\mathcal C)` for this ambient category, including lines 234 and 242 immediately before the lemma.

### Adverse evidence considered

Because the prose meaning is obvious, a reader can silently infer that plain `C` was intended to denote `\mathcal C`; that makes the defect low-risk in exposition but does not make the printed identifier bound or exact. No local declaration identifies `C` with `\mathcal C`.

### Smallest correction

At line 267 replace only

`\Ob(C)`

with

`\Ob(\mathcal{C})`.

## Review boundary

This review independently supports all three entries as exact source-level corrections for a later R4 derived overlay. It does not authorize silent correction in canonical CJK or French translations, does not admit an overlay, and makes no claim about any other Sites or Sheaves hypothesis.
