# Integration roadmap

This roadmap describes the intended order of future corpus integration for the
[Unofficial AI-Integrated Stacks Project](README.md). It is a sequence of
bounded, evidence-gated milestones—not a claim that the listed material has
already been integrated. Current admitted coverage is recorded in
[Project status](STATUS.md), while detailed EGA evidence and its exact semantic
cursor live in the [EGA integration dossier](ega/README.md).

## Current maintenance baseline

The current release baseline contains **22 overlays / 559 stable IDs** at the
Verdier admission cutoff
`60f1d97ecbd376ff7a91298d17e1f162b9996c3a`. Its first 21 overlays are the
historical Stacks errata batches R1–R21: 547 correction IDs and 591 exact v2
operations at prior cutoff `13ca6aaaca454f5930c4885c93f427e30cf21959`.
The 22nd overlay, `stacks-verdier-a04446e-1-2-13-r1`, is a separately admitted,
independently written historical-source contribution. It inserts one
manifest-bound lemma into cumulative `derived.tex`; no official Stacks tag or
upstream endorsement is claimed. The exact source, registry, operation, and
byte identities are recorded in the
[current composition receipt](validation/composition-current.json).

The Verdier source passed two independent linked-worktree fixed-point builds at
source `7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`: 22 readable PDFs, 2,343 pages,
24,390,066 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 130 affected `derived.pdf` pages passed visual review,
with pages 9–11 inspected at high resolution around the page-10 insertion. All
22 PDF identities match exactly between the two builds.

## Queued registry-order maintenance

Later admissions do not move the frozen Verdier release cutoff. They are queued
for the next source-composition cycle in this exact order:

1. **R22** — `stacks-errata-a04446e-r22`, admission
   `cec63f082819c0580c43f59790ab441260fe1ccc`: 83 stable units
   (`MC-STK-ERR-0915`–`0997`) and 94 manifest-bound operations affecting only
   `more-algebra.tex`; manifest SHA-256
   `8C519D72AFB3496DD3EB0116EB64FBF3ACF2946A809FED070E4F5D7554A52F8B`.
2. **R23** — `stacks-errata-a04446e-r23`, admission
   `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`: 10 stable units
   (`MC-STK-ERR-0998`–`1007`) and 12 nonoverlapping manifest-bound operations
   affecting only `more-algebra.tex`; manifest SHA-256
   `4E8E588698926FD7A47D9CFFB1496CB7305D8EB698C571AD9660FC4C81F80A5C`.

R22 must be composed before R23, and neither isolated payload may overwrite the
cumulative source wholesale. The rejected producer `MORE-ALGEBRA-J-006` remains
excluded. A later 29-row French `MORE-ALGEBRA-L` packet was independently
deduplicated against R22/R23: 27 rows are directly new and admissible; two rows
form a conditional bundle that also requires the linked `t`→`s` repairs at
authority lines 38321 and 38325. That packet remains intake evidence, not an
admitted overlay or part of the current fixed point.

## Recommended order

| Stage | Bounded milestone | Why it comes here |
| --- | --- | --- |
| **1. Complete EGA I** | Review EGA I §§6.2–6.3, then §§6.4–6.6, followed by staged checkpoints through §10. | This continues from the exact existing cursor, preserves statement order, and finishes the language-of-schemes layer before later corpora depend on it. |
| **2. Integrate EGA II** | Begin with §1 on affine morphisms; continue through §§2–4 on `Proj`, projective bundles, and ample sheaves; then close §§5–8 on quasi-projective, proper, projective, finite, and quasi-finite morphisms, valuative criteria, blowups, and contractions. | EGA II is the shortest path from scheme language to the global morphism machinery used by EGA III and substantial parts of SGA1. |
| **3. Integrate the foundations of SGA1** | Treat Exposés I–V first, then the fibred-category bridge in Exposé VI and the descent layer in Exposés VIII–IX. The revised edition contains no Exposé VII. | This yields a coherent foundation in étale, smooth, and flat morphisms, Galois categories, fibred categories, and descent without prematurely taking on the advanced specialization and cohomological material. |
| **4. Integrate EGA III** | Proceed in source order through coherent cohomology, projective and proper finiteness, formal functions, base change, and existence results. | EGA III can reuse EGA II's projective/proper foundation and the project's existing FAC, Tôhoku, GAGA, and FGA integrations. It also supplies leverage for the advanced part of SGA1. |
| **5. Complete advanced SGA1** | Integrate Exposés X–XIII: specialization, examples and complements, algebraic–analytic comparison, and cohomological properness. | These exposés have wider dependency surfaces and become more directly verifiable after EGA III; the existing GAGA integration provides an additional comparison layer for Exposé XII. |
| **6. Integrate EGA IV** | Work fascicle by fascicle, with separately sealed subsection-level milestones. | EGA IV is the broadest and most technically entangled EGA layer. Deferring it avoids turning one very large corpus into a gate for the smaller, higher-leverage milestones above. |

## Immediate milestones

The next semantic cursor is **EGA I §6.2.1**. The first two checkpoints are
deliberately small enough to review, validate, and publish independently:

1. **EGA I §§6.2–6.3** — 13 semantic statements in the current discovery
   inventory: two in §6.2 and eleven in §6.3, covering printed pages 143–147.
2. **EGA I §§6.4–6.6** — 26 further semantic statements, closing EGA I §6.
3. **EGA I §§7–10** — advance in source order through separately sealed
   section or subsection checkpoints until EGA I is complete.
4. **EGA II §1** — seven subsections on affine morphisms, printed pages 5–18.
   This is the first post–EGA I checkpoint and lies wholly within the currently
   sealed direct-authority range.
5. **EGA II §§2–8** — proceed in bounded source-order tranches, beginning with
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
  integrations, making notation reconciliation and gap detection incremental;
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
