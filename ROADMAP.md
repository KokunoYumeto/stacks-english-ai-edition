# Integration roadmap

This roadmap describes the intended order of future corpus integration for the
[Unofficial AI-Integrated Stacks Project](README.md). It is a sequence of
bounded, evidence-gated milestones—not a claim that the listed material has
already been integrated. Current admitted coverage is recorded in
[Project status](STATUS.md), while detailed EGA evidence and its exact semantic
cursor live in the [EGA integration dossier](ega/README.md).

## Current maintenance baseline

The current validated composition contains **24 overlays / 652 stable IDs** at
R23 admission cutoff `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
`a67a8529b853da8834502456e8ca75afe71aa78c`. Its Stacks errata component is
R1–R23: 23 batches, 640 correction IDs, and 697 exact v2 operations. The 22nd
overlay, `stacks-verdier-a04446e-1-2-13-r1`, remains a separately admitted,
independently written historical-source contribution with 12 non-official
stable units. It inserts one manifest-bound lemma into cumulative `derived.tex`;
no official Stacks tag or upstream endorsement is claimed.

R22 and R23 add 93 correction IDs and 106 manifest-bound operations affecting
only `more-algebra.tex`. Their registry content is composed in order at source
`3a1100a79abc76315592711c9f2c86ad21b5f6a9`, tree
`28980ba358cadddecc67d5013c7a9b624fee6305`, without replacing the cumulative
source wholesale. The exact authority, registry, operation, source, and
preservation identities are recorded in the
[current composition receipt](validation/composition-current.json).

The composed source passed two linked-worktree fixed-point builds at source
`1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`: 22 readable PDFs, 2,343 pages,
24,389,773 PDF bytes, global fixed point on sweep four, and zero fatal or listed
serious diagnostics. All 406 affected `more-algebra.pdf` pages passed visual
review, with 63 correction-locus pages inspected at high resolution. All 22 PDF
identities match exactly between the two builds. The preceding Verdier content
release remains preserved as historical evidence for its own exact scope.

The R22/R23 content release is public at
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`; exact-head CI and anonymous
readback of 138 checked files totaling 25,024,008 bytes pass.

## Queued registry-order maintenance

R24 was subsequently admitted in the external registry lane at
`6df734ecb3bef8f35770819d17a8d3e267b8e07a` and awaits source composition
after the published R23 fixed point. Successor registry head
`53c517215ef542cfc987e2445a07bb23c7b120fb` materializes the active R25 lease.
Neither R24 nor R25 is part of the current generated source. The 29-row French
`MORE-ALGEBRA-L` packet remains unadmitted intake evidence, not an admitted
overlay or part of the current fixed point. The rejected R23 producer
`MORE-ALGEBRA-J-006` likewise remains excluded from the integrated source.

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
