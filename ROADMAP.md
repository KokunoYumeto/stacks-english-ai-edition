# Integration roadmap

This roadmap describes the intended order of future corpus integration for the
[Unofficial AI-Integrated Stacks Project](README.md). It is a sequence of
bounded, evidence-gated milestones—not a claim that the listed material has
already been integrated. Current admitted coverage is recorded in
[Project status](STATUS.md), while detailed EGA evidence and its exact semantic
cursor live in the [EGA integration dossier](ega/README.md). EGA is only
partially composed into the root source; its complete English discovery and
French diplomatic editions remain separate read-only inputs.

## Current maintenance baseline

The current validated composition contains **31 overlays / 931 stable IDs** at
R30 admission cutoff `256846d6a4193f21cd6e1af675dc09e6950aa3d6`, tree
`9a4f0ba1bd342cde5bf3f8f36a2d68cd7792aef3`. Its Stacks errata component is
R1–R30: 30 batches, 919 correction IDs, and 1,033 exact v2 operations. The 22nd
overlay, `stacks-verdier-a04446e-1-2-13-r1`, remains a separately admitted,
independently written historical-source contribution with 12 non-official
stable units. It inserts one manifest-bound lemma into cumulative `derived.tex`;
no official Stacks tag or upstream endorsement is claimed.

R22 and R23 add 93 correction IDs and 106 manifest-bound operations affecting
only `more-algebra.tex`. R24 adds 38 IDs and 57 operations affecting only
`spaces-duality.tex`; R25 adds 131 IDs and 154 operations affecting only
`artin.tex`; R26 adds 25 IDs and 39 operations affecting only `smoothing.tex`;
R27 adds 14 IDs and 14 operations affecting only `modules.tex`. R28 adds one
operation affecting only `smoothing.tex`, explicitly superseding R26 operation
`MC-STK-ERR-1183-OP1`. R29 adds 30 IDs and 31 operations affecting only
`sites-modules.tex`; R30 adds 40 IDs and 40 operations affecting only
`injectives.tex`. All are composed in registry order without replacing
cumulative source wholesale. The R29/R30 registry import is
`6df0e967030bcf818f3c49584fa5e9a992278d75`; source composition is
`3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
`c4ce1faf96257fe11c0123ca649c9c020982aa33`, followed by validation binding
`c521604343534f94c7a59086c94b99712eb1d754`. The exact authority, registry,
operation, source, and preservation identities are recorded in the
[current composition receipt](validation/composition-current.json).

The current R30 source passed two linked-worktree fixed-point builds at source
`c521604343534f94c7a59086c94b99712eb1d754`, tree
`4fe26c45da3edc493b8406824f90db06ef3df28c`: 26 readable PDFs, 2,572 pages,
27,531,529 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 111 affected `sites-modules.pdf` and `injectives.pdf`
pages passed review, with all 42 correction-locus pages at 180 DPI. All 26 PDF identities
match exactly between the two builds. Earlier R26, R24, R22/R23, Verdier, and R21 receipts
remain preserved as historical evidence for their exact scopes.

R30 is the current public errata preservation checkpoint at source head
`e3def48650c66c0d65978a04f67dea88bd8b42ac`, tree
`62bee382516e4a06df6746c5aa61a54b2fe6622f`, and tag
[`ai-integrated-stacks-r30-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r30-2026-08-29).
Its six-asset package totals 178,510,756 bytes on each of GitHub and Zenodo;
all 12 anonymous downloads matched by filename, byte count, and SHA-256. The
Zenodo version DOI is
[`10.5281/zenodo.22166456`](https://doi.org/10.5281/zenodo.22166456) under
concept DOI `10.5281/zenodo.22135180`. The package preserves 26 PDFs, 2,572
pages, and 27,531,529 PDF bytes. The
[R30 release receipt](validation/stacks-errata-a04446e-r30-release-2026-08-29.json)
binds the transaction and readback.

R28 remains published as the preceding historical release at tag
[`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28)
at commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
`fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, and as Zenodo version DOI
[`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under
concept DOI `10.5281/zenodo.22135180`. Exact-head workflow run `33212304694`,
attempt 1, passed. The six-asset package is byte-identical on both hosts:
174,673,433 bytes per host, 12 successful anonymous downloads, and zero
mismatches. The commit-bound source archive is 154,766,484 bytes and contains
2,312 entries. The
[R28 release receipt](validation/stacks-errata-a04446e-r28-release-2026-08-28.json)
binds the transaction and readback.

R27 remains published as an earlier historical tag
[`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28)
at commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
`a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, and as Zenodo version DOI
[`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under
concept DOI `10.5281/zenodo.22135180`. Exact-head workflow run `33198300432`,
attempt 2, passed. The six-asset package is byte-identical on both hosts:
174,411,900 bytes per host, 12 successful anonymous downloads, and zero
mismatches. The commit-bound source archive is 154,505,160 bytes and contains
2,245 entries. The
[R27 release receipt](validation/stacks-errata-a04446e-r27-release-2026-08-28.json)
binds the transaction and readback. R26 is the preceding historical release.

The historical R22/R23 content release is public at
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`; exact-head CI and anonymous
readback of 138 checked files totaling 25,024,008 bytes pass.

## Registry-order maintenance state

R29 is admitted at `8b70e94d7d9a1f28041445e52df03bffd2980435` and its
append-only transport repair is preserved at the R30 cutoff `256846d6…`.
R30 is directly admitted at that same cutoff. Their cumulative source
composition is `3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`; its 71 exact
operations affect only `sites-modules.tex` and `injectives.tex`. R29's final
manifest SHA-256 is
`52920239C887757CE937267C5505AD98980464329BC6BBBD62086ED4E1D98CE5`;
R30's is `C903DFCA06DA4063782BB88B2F2AC5FCF56352CF948CF03382D77F1A54A48C9E`.
The rejected R26 producer `SMOOTHING-010` and R23 producer
`MORE-ALGEBRA-J-006` remain excluded from the integrated source.

## Recommended order

| Stage | Bounded milestone | Why it comes here |
| --- | --- | --- |
| **1. Complete EGA I** | Continue at EGA I §6.5.1 through §§6.5–6.6, followed by staged checkpoints through §10. | This continues from the exact existing cursor, preserves statement order, and finishes the language-of-schemes layer before later corpora depend on it. |
| **2. Integrate EGA II** | Begin with §1 on affine morphisms; continue through §§2–4 on `Proj`, projective bundles, and ample sheaves; then close §§5–8 on quasi-projective, proper, projective, finite, and quasi-finite morphisms, valuative criteria, blowups, and contractions. | EGA II is the shortest path from scheme language to the global morphism machinery used by EGA III and substantial parts of SGA1. |
| **3. Integrate the foundations of SGA1** | Treat Exposés I–V first, then the fibred-category bridge in Exposé VI and the descent layer in Exposés VIII–IX. The revised edition contains no Exposé VII. | This yields a coherent foundation in étale, smooth, and flat morphisms, Galois categories, fibred categories, and descent without prematurely taking on the advanced specialization and cohomological material. |
| **4. Integrate EGA III** | Proceed in source order through coherent cohomology, projective and proper finiteness, formal functions, base change, and existence results. | EGA III can reuse EGA II's projective/proper foundation, the existing FAC, GAGA, and FGA source integrations, and the closed Tôhoku dossier-only mapping. It also supplies leverage for the advanced part of SGA1. |
| **5. Complete advanced SGA1** | Integrate Exposés X–XIII: specialization, examples and complements, algebraic–analytic comparison, and cohomological properness. | These exposés have wider dependency surfaces and become more directly verifiable after EGA III; the existing GAGA integration provides an additional comparison layer for Exposé XII. |
| **6. Integrate EGA IV** | Work fascicle by fascicle, with separately sealed subsection-level milestones. | EGA IV is the broadest and most technically entangled EGA layer. Deferring it avoids turning one very large corpus into a gate for the smaller, higher-leverage milestones above. |

## Immediate milestones

The next semantic cursor is **EGA I §6.5.1**. EGA I §6.4 is complete through
§6.4.13: all 20 mathematical units are source-bound and routed, with no
duplicate root addition and no root TeX or PDF change. The checkpoint is public
at GitHub tag
[`ega-i-6.4-semantic-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.4-semantic-2026-08-29)
and Zenodo version DOI [`10.5281/zenodo.22161051`](https://doi.org/10.5281/zenodo.22161051),
with the exact transaction in the
[semantic release receipt](validation/ega-i-6.4-semantic-release-2026-08-29.json).
The next checkpoints remain deliberately small enough to review, validate, and
publish independently:

1. **EGA I §§6.5–6.6** — continue in source order and close EGA I §6.
2. **EGA I §§7–10** — advance in source order through separately sealed
   section or subsection checkpoints until EGA I is complete.
3. **EGA II §1** — seven subsections on affine morphisms, printed pages 5–18.
   This is the first post–EGA I checkpoint and lies wholly within the currently
   sealed direct-authority range.
4. **EGA II §§2–8** — proceed in bounded source-order tranches, beginning with
   homogeneous spectra and relative `Proj` rather than treating the volume as
   a single release.

## Why EGA II precedes SGA1

EGA II has greater immediate dependency leverage and lower setup risk:

- the repository already has stable EGA source-unit identities, deterministic
  intake, semantic-map validation, residual tracking, and direct-authority
  bindings that extend into EGA II;
- its affine, projective, proper, finite, quasi-finite, and valuative machinery
  is reused by both EGA III and later SGA1 exposés;
- its subject matter directly overlaps the project's completed FAC and FGA
  source integrations and the closed Tôhoku dossier-only mapping, making
  notation reconciliation and gap detection incremental;
- starting SGA1 first would require a new corpus-level authority and mapping
  scaffold while immediately crossing étale, descent, fundamental-group,
  analytic-comparison, and nonabelian cohomological boundaries.

This ordering does not rank EGA II as mathematically more important than
SGA1. It places the reusable dependency layer first so that SGA1 can be
integrated in smaller, more testable exposé groups.

## Evidence gate for every milestone

A milestone is complete only when all applicable gates pass:

1. Every promoted claim is bound to an exact primary-source locus and a pinned
   Stacks source identity.
2. Every source statement has an explicit disposition: existing coverage,
   stronger or split coverage, residual, source issue, or justified local
   integration.
3. Lexical similarity alone never establishes mathematical equivalence, and
   local labels are never presented as official Stacks tags.
4. Any source addition is proved, normalized to surrounding Stacks notation,
   checked for duplicate or superseding coverage, and validated with its
   affected chapters.
5. Deterministic mapping, structural, reference, and build checks pass before
   the milestone is described as admitted coverage.

## Primary references

- [EGA II: *Étude globale élémentaire de quelques classes de morphismes* — NUMDAM](https://archive.numdam.org/item/PMIHES_1961__8__5_0/)
- [SGA1: *Revêtements étales et groupe fondamental*, revised edition — arXiv](https://arxiv.org/abs/math/0206203)
- [The Stacks Project table of contents](https://stacks.math.columbia.edu/browse)
- [Local EGA discovery, authority, mapping, and validation dossier](ega/README.md)

The authoritative completion record remains [Project status](STATUS.md). This
roadmap may evolve as exact source comparison exposes dependencies, duplicate
coverage, or higher-value bounded gaps.
