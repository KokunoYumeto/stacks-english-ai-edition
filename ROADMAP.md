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

The current validated composition contains **34 overlays / 1,042 stable IDs** at
the R33 successor `acb48c7edaf9595b542b003ed360399870188b7f`, tree
`8356ae1652ae4ce6a22a457855072c5a3e7b3ad4`. Its Stacks errata component is
R1–R33: 33 batches, 1,030 correction IDs, and 1,166 exact v2 operations. The 22nd
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
`injectives.tex`; R31 adds one operation to `sites-modules.tex`; and R32 adds
125 operations across `fields.tex`, `categories.tex`, and `algebra.tex`. All
are composed in registry order without replacing cumulative source wholesale.
The R33 registry import is
`b2ffa008fc27bfdb8b93c431f4df0c3e197d3440`; source composition is
`9100eefe0819f9632c6129e6d6f19a4101d223d1`, tree
`d786a8604e7c0be79fab77c380247bd971555520`, followed by the validated build
binding at `1c90a67eb42de28884be05abd8fb58f781aed7db`. The exact authority, registry,
operation, source, and preservation identities are recorded in the
[current composition receipt](validation/composition-current.json).

The current R33 source passed two linked-worktree fixed-point builds at source
`1c90a67eb42de28884be05abd8fb58f781aed7db`, tree
`3c292f9a4b94162ede69d2633b1272b057a498c3`: 28 readable PDFs, 2,730 pages,
29,277,302 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 116 affected-chapter pages passed review, with all 5
correction-locus pages at 180 DPI. All 28 PDF identities
match exactly between the two builds. Earlier R26, R24, R22/R23, Verdier, and R21 receipts
remain preserved as historical evidence for their exact scopes.

R33 is the current public errata preservation checkpoint at content head
`a52883a83081348d0ea4927a03d5fd8aa036890b`, tree
`2d686e92dacdc8e01d6c6950bf81f250e657cd8f`, and tag
[`ai-integrated-stacks-r33-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r33-2026-08-30).
Its six current assets total 184,010,318 bytes on each host. All six GitHub
assets and all nine Zenodo files passed anonymous byte/hash readback. The
Zenodo version DOI is
[`10.5281/zenodo.22182175`](https://doi.org/10.5281/zenodo.22182175) under
concept DOI `10.5281/zenodo.22135180`. The current package preserves 28 PDFs,
2,730 pages, and 29,277,302 PDF bytes. The
[R33 release receipt](validation/stacks-errata-a04446e-r33-release-2026-08-30.json)
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
| **1. Complete EGA I** | Continue at EGA I §6.6.4 through §§6.6–10 in source order, using staged checkpoints. | This continues from the exact existing cursor, preserves statement order, and finishes the language-of-schemes layer before later corpora depend on it. |
| **2. Integrate EGA II** | Begin with §1 on affine morphisms; continue through §§2–4 on `Proj`, projective bundles, and ample sheaves; then close §§5–8 on quasi-projective, proper, projective, finite, and quasi-finite morphisms, valuative criteria, blowups, and contractions. | EGA II is the shortest path from scheme language to the global morphism machinery used by EGA III and substantial parts of SGA1. |
| **3. Integrate the foundations of SGA1** | Treat Exposés I–V first, then the fibred-category bridge in Exposé VI and the descent layer in Exposés VIII–IX. The revised edition contains no Exposé VII. | This yields a coherent foundation in étale, smooth, and flat morphisms, Galois categories, fibred categories, and descent without prematurely taking on the advanced specialization and cohomological material. |
| **4. Integrate EGA III** | Proceed in source order through coherent cohomology, projective and proper finiteness, formal functions, base change, and existence results. | EGA III can reuse EGA II's projective/proper foundation, the existing FAC, GAGA, and FGA source integrations, and the closed Tôhoku dossier-only mapping. It also supplies leverage for the advanced part of SGA1. |
| **5. Complete advanced SGA1** | Integrate Exposés X–XIII: specialization, examples and complements, algebraic–analytic comparison, and cohomological properness. | These exposés have wider dependency surfaces and become more directly verifiable after EGA III; the existing GAGA integration provides an additional comparison layer for Exposé XII. |
| **6. Integrate EGA IV** | Work fascicle by fascicle, with separately sealed subsection-level milestones. | EGA IV is the broadest and most technically entangled EGA layer. Deferring it avoids turning one very large corpus into a gate for the smaller, higher-leverage milestones above. |

## Immediate milestones

The current semantic cursor is **EGA I §6.6.4**. EGA I §6.6.3 is the latest
source-bound semantic checkpoint, public at GitHub tag
[`ega-i-6.6.3-semantic-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.6.3-semantic-2026-08-30)
and Zenodo version DOI [`10.5281/zenodo.22177421`](https://doi.org/10.5281/zenodo.22177421),
with the exact checkpoint in
[`ega-i-6.6.3-semantic-checkpoint-2026-08-30.json`](validation/ega-i-6.6.3-semantic-checkpoint-2026-08-30.json).
It changes no root TeX or PDF and does not create a new errata round. Earlier
6.4 and 6.5.x receipts remain preserved as historical evidence.
The next checkpoints remain deliberately small enough to review, validate, and
publish independently:

1. **EGA I §6.6.4 and the remainder of §6** — continue in source order and
   close EGA I §6.
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
