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

The current validated composition contains **28 overlays / 860 stable IDs** at
R27 admission cutoff `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
`110a3006fcbb27b94c4170639aab56db507f9a89`. Its Stacks errata component is
R1–R27: 27 batches, 848 correction IDs, and 961 exact v2 operations. The 22nd
overlay, `stacks-verdier-a04446e-1-2-13-r1`, remains a separately admitted,
independently written historical-source contribution with 12 non-official
stable units. It inserts one manifest-bound lemma into cumulative `derived.tex`;
no official Stacks tag or upstream endorsement is claimed.

R22 and R23 add 93 correction IDs and 106 manifest-bound operations affecting
only `more-algebra.tex`. R24 adds 38 IDs and 57 operations affecting only
`spaces-duality.tex`; R25 adds 131 IDs and 154 operations affecting only
`artin.tex`; R26 adds 25 IDs and 39 operations affecting only `smoothing.tex`;
R27 adds 14 IDs and 14 operations affecting only `modules.tex`. All are
composed in registry order without replacing cumulative source wholesale. The
R27 source composition is commit
`5a42b7d2a04c4d08be7861ec91306d8be05d631e`, tree
`ecbad57ee36b4fb290c80cb4d1f83eab50a47460`. The exact authority, registry,
operation, source, and preservation identities are recorded in the
[current composition receipt](validation/composition-current.json).

The current R27 source passed two linked-worktree fixed-point builds at source
`dc849731c9768048b993eb5a9df218118b817f40`, tree
`b3462d130dedb3b3c0625cab0d7a2d406114e17f`: 25 readable PDFs, 2,492 pages,
26,609,586 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 55 affected `modules.pdf` pages passed review,
including 10 correction-locus pages at high resolution. All 25 PDF identities
match exactly between the two builds. Earlier R26, R24, R22/R23, Verdier, and R21 receipts
remain preserved as historical evidence for their exact scopes.

R27 is published as tag
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

R27 is admitted and composed into the generated source at
`5a42b7d2a04c4d08be7861ec91306d8be05d631e`. Its 14 stable units and 14 exact
operations affect only cumulative FAC-expanded `modules.tex`. The lease,
candidate, and admission chain is bound as
`1f05772d6f46ab851cdecdf53b70c11ea698cb14` →
`77fcc9fc2341e72b077224399743f1062e73b228` →
`8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`; the exact manifest SHA-256 is
`A4D03B8B47A1005B6DAC8B0EE4B9D0F4361E065E51D324B9634F38B51053DE3C`.
The rejected R26 producer `SMOOTHING-010` and R23 producer
`MORE-ALGEBRA-J-006` remain excluded from the integrated source.

## Recommended order

| Stage | Bounded milestone | Why it comes here |
| --- | --- | --- |
| **1. Complete EGA I** | Continue at EGA I §6.4.1 through §§6.4–6.6, followed by staged checkpoints through §10. | This continues from the exact existing cursor, preserves statement order, and finishes the language-of-schemes layer before later corpora depend on it. |
| **2. Integrate EGA II** | Begin with §1 on affine morphisms; continue through §§2–4 on `Proj`, projective bundles, and ample sheaves; then close §§5–8 on quasi-projective, proper, projective, finite, and quasi-finite morphisms, valuative criteria, blowups, and contractions. | EGA II is the shortest path from scheme language to the global morphism machinery used by EGA III and substantial parts of SGA1. |
| **3. Integrate the foundations of SGA1** | Treat Exposés I–V first, then the fibred-category bridge in Exposé VI and the descent layer in Exposés VIII–IX. The revised edition contains no Exposé VII. | This yields a coherent foundation in étale, smooth, and flat morphisms, Galois categories, fibred categories, and descent without prematurely taking on the advanced specialization and cohomological material. |
| **4. Integrate EGA III** | Proceed in source order through coherent cohomology, projective and proper finiteness, formal functions, base change, and existence results. | EGA III can reuse EGA II's projective/proper foundation, the existing FAC, GAGA, and FGA source integrations, and the closed Tôhoku dossier-only mapping. It also supplies leverage for the advanced part of SGA1. |
| **5. Complete advanced SGA1** | Integrate Exposés X–XIII: specialization, examples and complements, algebraic–analytic comparison, and cohomological properness. | These exposés have wider dependency surfaces and become more directly verifiable after EGA III; the existing GAGA integration provides an additional comparison layer for Exposé XII. |
| **6. Integrate EGA IV** | Work fascicle by fascicle, with separately sealed subsection-level milestones. | EGA IV is the broadest and most technically entangled EGA layer. Deferring it avoids turning one very large corpus into a gate for the smaller, higher-leverage milestones above. |

## Immediate milestones

The next semantic cursor is **EGA I §6.4.1**. EGA I §6.3 is complete with all
eleven statements routed to existing Stacks material and no duplicate root
addition. Its two diagrams retain explicit visual-evidence residuals without
blocking source-order semantic work. The next checkpoints remain deliberately
small enough to review, validate, and publish independently:

1. **EGA I §§6.4–6.6** — 26 further semantic statements, closing EGA I §6.
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
