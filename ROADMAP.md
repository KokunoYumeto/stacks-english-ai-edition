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

The current validated composition contains **27 overlays / 846 stable IDs** at
R26 admission cutoff `a7c4a3c52b9a32e96e0f4b98f9579369026d9e1b`, tree
`93af84d65d7b250fe0f4d660782ccf330b9e4743`. Its Stacks errata component is
R1–R26: 26 batches, 834 correction IDs, and 947 exact v2 operations. The 22nd
overlay, `stacks-verdier-a04446e-1-2-13-r1`, remains a separately admitted,
independently written historical-source contribution with 12 non-official
stable units. It inserts one manifest-bound lemma into cumulative `derived.tex`;
no official Stacks tag or upstream endorsement is claimed.

R22 and R23 add 93 correction IDs and 106 manifest-bound operations affecting
only `more-algebra.tex`. R24 adds 38 IDs and 57 operations affecting only
`spaces-duality.tex`; R25 adds 131 IDs and 154 operations affecting only
`artin.tex`; R26 adds 25 IDs and 39 operations affecting only `smoothing.tex`.
All are composed in registry order without replacing cumulative source
wholesale. The R26 source composition is commit
`47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
`cbad56973a9e594743b596a5fd0fa291b490ae26`. The exact authority, registry,
operation, source, and preservation identities are recorded in the
[current composition receipt](validation/composition-current.json).

The current R26 source passed two linked-worktree fixed-point builds at source
`c90a50300dcec156e9ea5fe0c8802c8e36bde81e`, tree
`651fff448fa41a4e7c38970eec169328002ac4f6`: 24 readable PDFs, 2,437 pages,
25,862,999 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 37 affected `smoothing.pdf` pages passed review,
including 15 correction-locus pages at high resolution. All 24 PDF identities match
exactly between the two builds. Earlier R24, R22/R23, Verdier, and R21 receipts
remain preserved as historical evidence for their exact scopes.

The current R26 preservation release is public at tag commit
`7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`; exact-head CI passes. Its
six-asset preservation package is byte-identical on GitHub and Zenodo version
DOI `10.5281/zenodo.22146844` under concept DOI
`10.5281/zenodo.22135180`: 172,480,328 bytes per host, 12 successful anonymous
downloads, and zero mismatches. The commit-bound source projection contains
2,169 entries and a hash-bound manifest for six privacy replacements in four
historical provenance files.

The historical R22/R23 content release is public at
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`; exact-head CI and anonymous
readback of 138 checked files totaling 25,024,008 bytes pass.

## Registry-order maintenance state

R26 is admitted and composed into the generated source at
`47c6b78e476e5644f5a7d0ca2ce4816b144a2411`. Its 25 stable units and 39 exact
operations affect only `smoothing.tex`. The adjudication accepted 31 producer
identities, aliased `SMOOTHING-002/003/004` to existing R1 corrections,
rejected `SMOOTHING-010`, and merged four repeated semantic groups. The rejected
R23 producer `MORE-ALGEBRA-J-006` likewise remains excluded from the integrated
source.

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
