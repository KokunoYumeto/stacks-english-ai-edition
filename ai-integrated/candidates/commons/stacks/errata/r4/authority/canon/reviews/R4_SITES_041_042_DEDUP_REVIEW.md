# R4 independent duplicate reconciliation: SITES-041–042

Date: 2026-08-22

## Scope and recomputed input identities

All four required inputs were read completely. Byte counts and SHA-256 digests were recomputed from the live files before reconciliation.

| Input | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `canon/control/ERRATA_R4_SUPPLEMENT_SITES_041_042_20260822.json` | 2,843 | 53 | `F4A87E2F2433FE28A52582D8E61B0827798F83BD2049E9A53383893CB757C9F7` |
| `upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/sites.tex` | 424,197 | 11,860 | `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D` |
| `canon/control/private/R4_SITES_010_012_INDEPENDENT_REVIEW.md` | 6,760 | 118 | `7D9A7271D81C089167CAF9BA94C3813E411C9D750FA163DAC86A9D76F1B7EF8B` |
| `canon/control/private/R4_SITES_013_INDEPENDENT_REVIEW.md` | 3,572 | 93 | `7C1986D50ABBAAF6E0E88E70A792EBA9D2ADFDF630986E00410CF31E7CDFCD3C` |

The authority identity is the same commit and byte stream used by both prior independent reviews. No authority-version normalization or cross-version inference is involved.

## Reconciliation rule

For this review, two producer rows identify the same correction exactly when all of the following agree:

1. frozen authority file identity;
2. defective source occurrence, including which occurrence is meant when text repeats;
3. smallest replacement;
4. typed or logical reason the replacement is required.

A larger quotation window or newly assigned producer ID does not create a new correction when those four identity fields coincide. A mathematically valid new producer row can therefore have row disposition **DUPLICATE** while the single correction it denotes remains **ACCEPTED** under its earlier canonical ID.

## Producer-row dispositions

| New producer row | Row disposition | Existing correction identity | Novel correction? |
|---|---|---|---|
| SITES-041 | **DUPLICATE OF SITES-011** | `sites.tex:2200`, final fragment `of $\mathcal{D}$` → `of $\mathcal{C}$` | No |
| SITES-042 | **DUPLICATE OF SITES-013** | `sites.tex:2221`, final occurrence `for $t_i$ and $t_j$` → `for $s_i$ and $s_j$` | No |

Neither duplicate row is rejected: each points to a real, already accepted defect. Neither is deferred: the identity match is complete.

## SITES-041 is exactly SITES-011

### Authority proof

The governing lemma begins at `sites.tex:2182`. Lines 2183–2187 declare only the site `\mathcal{C}`, presheaves on `\mathcal{C}`, objects of `\Ob(\mathcal{C})`, and coverings by such objects. The proof invokes `lemma-sections-sheafification` at line 2193. The cited lemma declares the same sole ambient site `\mathcal{C}` at line 2157 and states at lines 2167–2169 that the family

`\{U_{ijk} \to U_i \times_U U_j\}`

is a covering `of $\mathcal{C}$`.

Line 2200 repeats that exact family but prints `of $\mathcal{D}$`. No `\mathcal{D}` is bound in this lemma or proof. Replacing only `\mathcal{D}` by `\mathcal{C}` restores the cited clause and the ambient category required for all displayed objects and presheaf values.

### Exact identity with the prior correction

| Identity field | SITES-041 intake | Prior SITES-011 review | Match |
|---|---|---|---|
| Authority | Frozen `sites.tex`, commit `a04446e57ec1fbc252a871afcec7752fb2807b14`, SHA-256 `07AE…B1845D` | Same frozen file, commit, and digest | Exact |
| Occurrence | Line 2200, the category in `the covering … is a covering of $\mathcal{D}$` | Line 2200, fragment `of $\mathcal{D}$` | Exact; the intake merely quotes a larger window |
| Replacement | `\mathcal{D}` → `\mathcal{C}` | `of $\mathcal{D}$` → `of $\mathcal{C}$` | Exact edit |
| Reason | `\mathcal{D}` unbound; all data lie in `\mathcal{C}` | Same unbound-identifier and ambient-category proof | Exact |

Therefore SITES-041 contributes no new correction. It must bind to the already accepted SITES-011 correction identity.

## SITES-042 is exactly SITES-013

### Authority proof

At lines 2215–2218, bijectivity of `\mathcal{F}(U_i) \to \mathcal{G}(U_i)` gives unique lifts `t_i \in \mathcal{F}(U_i)` mapping to the already constructed `s_i \in \mathcal{G}(U_i)`. The goal begun at lines 2218–2219 is to prove agreement of the pullbacks of `t_i` and `t_j` on each `U_{ijk}`. Thus the final clause at lines 2220–2221 cannot use agreement of `t_i` and `t_j` as its premise; that is the conclusion currently being proved.

The known premise is the agreement of the pullbacks of `s_i` and `s_j`, established at lines 2199–2201 and preserved by the refinements at lines 2203–2214. Since `U_{ijk} \in \mathcal{B}`, the component `\mathcal{F}(U_{ijk}) \to \mathcal{G}(U_{ijk})` is injective. Naturality identifies the images of the two pulled-back lifts with the pulled-back `s_i` and `s_j`; their known agreement therefore implies agreement of the lifts. The smallest repair is to replace only the final `t_i` and `t_j` at line 2221 by `s_i` and `s_j`.

### Exact identity with the prior correction

| Identity field | SITES-042 intake | Prior SITES-013 review | Match |
|---|---|---|---|
| Authority | Frozen `sites.tex`, commit `a04446e57ec1fbc252a871afcec7752fb2807b14`, SHA-256 `07AE…B1845D` | Same frozen file, commit, and digest | Exact |
| Occurrence | Line 2221, explicitly the final `t_i` and `t_j` in `because we have the agreement …` | Line 2221, explicitly the final occurrence `for $t_i$ and $t_j$` | Exact |
| Replacement | Final `t_i,t_j` → `s_i,s_j` | Final `t_i,t_j` → `s_i,s_j` | Exact edit |
| Reason | Known compatibility belongs to the images `s_i,s_j`; injectivity then proves compatibility of lifts | Same naturality-and-injectivity proof and same circularity diagnosis | Exact |

The occurrence qualifier matters: the `t_i` and `t_j` at line 2218 correctly name the sections whose agreement is the conclusion, while only the final pair at line 2221 is defective. Both SITES-042 and the prior SITES-013 review select that same final occurrence. Therefore SITES-042 contributes no new correction and must bind to SITES-013.

## Row counts versus unique-correction counts

| Measure | Count |
|---|---:|
| Producer rows reviewed | 2 |
| Duplicate producer rows | **2** |
| Unique correction identities represented | 2 |
| Unique corrections already accepted under prior IDs | 2 |
| **Novel accepted corrections contributed by SITES-041–042** | **0** |
| Rejected producer rows | **0** |
| Deferred producer rows | **0** |

Operational disposition: retain the existing accepted correction identities SITES-011 and SITES-013; associate SITES-041 and SITES-042 as duplicate producer aliases only. Do not create duplicate edits or count either row as an additional accepted correction.

## Boundary

This document is an identity-level deduplication review only. It does not edit or authorize edits to the frozen authority, translations, candidate payloads, registries, or other control files.
