# Unofficial Stacks Project AI Drafts

[![Repository validation](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/actions/workflows/validate.yml/badge.svg)](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/actions/workflows/validate.yml)

## Why this project exists

We think AI is capable of contributing useful mathematics. This project is a
practical test of that belief: cooperating AI agents read historical sources,
compare them with the Stacks Project, and write draft statements and proofs
in Stacks-style LaTeX.

The inputs include editable LaTeX editions of major French-school works:

- **Serre, FAC — *Faisceaux algébriques cohérents*:** [French diplomatic TeX](https://zenodo.org/records/22074486/files/01b_FAC_French_Diplomatic_Body.tex?download=1) · [complete French/English source package](https://zenodo.org/records/22074486/files/19_FAC_Project_English_and_French_TeX_Source_Layers.zip?download=1).
- **Grothendieck, Tôhoku — *Sur quelques points d’algèbre homologique*:** [LaTeX source package](https://zenodo.org/records/22087339/files/src-p119-221.zip?download=1).
- **Serre, GAGA — *Géométrie algébrique et géométrie analytique*:** [French diplomatic TeX](https://zenodo.org/records/22087259/files/16_GAGA_French_diplomatic_body.tex?download=1) · [compilation driver](https://zenodo.org/records/22087259/files/15_GAGA_French_shared_driver_for_diplomatic_and_corrected.tex?download=1).
- **Grothendieck, FGA — *Fondements de la géométrie algébrique*:** [French LaTeX source and provenance package](https://github.com/KokunoYumeto/fga-fr/blob/main/releases/2026-08-30-r1/fga-fr-canon-errata-0001-0017-source-provenance.zip).
- **Grothendieck–Dieudonné, EGA — *Éléments de géométrie algébrique*:** [French LaTeX tree](https://github.com/KokunoYumeto/ega-fr/tree/main/source) · [English discovery edition](https://github.com/KokunoYumeto/ega-en/tree/main/source).
- **Verdier, *Des catégories dérivées des catégories abéliennes*:** [editable source package](https://zenodo.org/records/21968574/files/source.zip?download=1).

These are independently maintained transcriptions or editions, not original
author-produced LaTeX. The integration records pin the particular source
versions used; the linked editions may continue to develop.

The intended output is material that Stacks contributors—or any other
mathematician—can inspect, correct, reuse, or mine for ideas if they find it
worthwhile. It is not a request that the Stacks Project adopt AI. Maintaining
mathematics requires people who can understand, explain, repair, and extend
the proofs; producing a plausible draft does not transfer that understanding
to its future maintainers. That is a legitimate consideration regardless of
what any particular maintainer thinks about AI.

> [!IMPORTANT]
> This is an unofficial, independently maintained draft derivative of the
> [Stacks Project](https://stacks.math.columbia.edu/), not a competing canonical
> edition. All additions and integration work beyond the pinned upstream
> source are written by cooperating AI agents; the original Stacks text is
> the work of its authors. The Stacks Project and its maintainers have not
> reviewed, approved, or endorsed this project. “Draft formalization” here
> means mathematical statements and written proofs in LaTeX—not
> proof-assistant-checked mathematics. Automated checks and AI review do not
> certify mathematical correctness.

[Read the draft PDFs](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/releases/latest) ·
[Browse the source](chapters.tex) ·
[Compare with Stacks](CHANGES_FROM_UPSTREAM.md) ·
[Detailed status](STATUS.md) ·
[Sources and history](PROVENANCE.md) ·
[Validation](VALIDATION.md)

## What is actually in the draft?

The examples below name classical results and explain what was added here.
They are not claims that the underlying mathematics is new. **Integrated**
means the statement and proof are present in this branch’s readable LaTeX,
not merely mentioned in a tracking file.

### FAC: new explicit statements, proofs, and source corrections — integrated

The full article has been compared with Stacks. Results already covered were
mapped rather than rewritten; selected missing formulations and proofs were
added. Notable examples include:

- **Graded local duality** — Chapter III §4, no. 72, Theorem 1: an explicit
  graded-module formulation relating Koszul–Čech cohomology to graded Ext,
  including the exceptional kernel–cokernel sequence and its degree range.
  [Statement and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/more-algebra.tex#L7692).
- **Cohomology of projective complete intersections** — Chapter III §5,
  no. 78, Proposition 5: calculations for all twists, intermediate-cohomology
  vanishing, and top-cohomology duality. The draft separates the
  zero-dimensional exception to the source’s section-isomorphism claim and
  supplies the appropriate exact sequence.
  [Statement, correction, and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/coherent.tex#L4774).
- **Degree of the Hilbert polynomial equals dimension of support** —
  Chapter III §6, no. 81, Proposition 6: a consolidated statement and proof
  over an arbitrary field, assembled from existing Stacks ingredients.
  [Statement and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/varieties.tex#L7018).

[Full FAC comparison and integration record](fac/STATUS.md).

### GAGA: the projective algebraic–analytic comparison — integrated chapter

The new [GAGA chapter](gaga.tex) develops Serre’s three central theorems from
§3, no. 12:

- **Cohomology comparison:** algebraic and analytic coherent-sheaf cohomology
  agree on complex projective varieties.
  [Theorem 1](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1051) · [proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1236).
- **Full faithfulness:** analytic homomorphisms between analytified coherent
  sheaves come uniquely from algebraic homomorphisms.
  [Theorem 2](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1071) · [proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1309).
- **Algebraization:** every coherent analytic sheaf on a complex projective
  variety comes from an algebraic coherent sheaf. The argument develops
  analytic twisting and global generation before algebraizing a finite
  presentation.
  [Theorem 3](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1087) · [global-generation argument](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1444).

Applications include [Chow’s theorem](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1660) and
[algebraicity of holomorphic maps](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/gaga.tex#L1748).
This does **not** reconstruct every analytic foundation: Oka–Cartan coherence,
Weierstrass theory, Dolbeault computations, and related external inputs are
identified explicitly. [Scope and source comparison](gaga_r3/STATUS.md).

### FGA: Quot schemes, algebraization, and categorical foundations — integrated

- **Projective Quot schemes** — Exposé 221, Theorem 3.2 and Proposition 3.8:
  a Grassmannian construction proves that the fixed-Hilbert-polynomial Quot
  space is a projective scheme, with a very ample determinant bundle. This
  strengthens the inherited proper-algebraic-space conclusion in this setting.
  [Theorem and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/moduli.tex#L1573).
- **Algebraizing formal families and lifting smooth varieties** — Exposé
  182, Theorem 4 and Corollaries 3–4: algebraization with projective special
  fibre and vanishing second structure-sheaf cohomology, followed by a
  deformation-theoretic lifting criterion and the smooth-curve case.
  [Algebraization](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/coherent.tex#L9031) ·
  [lifting criterion](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/defos.tex#L2536) ·
  [curves](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/defos.tex#L2603).
- **Recovering categories and groupoids from their nerves** — Exposé 212,
  Proposition 4.1 and Corollary 4.2: full faithfulness of the nerve, the Segal
  characterization of its image, and the equivalence “groupoid iff nerve is
  Kan,” including an internal finite-limit version.
  [Nerve and Segal theorem](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/simplicial.tex#L953) ·
  [groupoid/Kan theorem](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/simplicial.tex#L5796).

[Full FGA comparison and notation-normalization record](fga/README.md).

### EGA: selected scheme-theoretic additions — partial, ongoing

EGA is **not fully integrated**. Source-by-source review is public through
EGA I §6.6.3 and continues at §6.6.4. Concrete additions already in the draft
include:

- **The Jacobson-radical neighbourhood lemma** — EGA I, Proposition 1.1.15:
  an open subset of an affine spectrum containing the closed set of an ideal
  in the Jacobson radical is the whole spectrum.
  [Named lemma and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/algebra.tex#L3628).
- **A spectrum-embedding criterion** — EGA I, Corollary 1.2.4:
  a unit-times-image condition on a ring map makes its spectrum map a
  homeomorphism onto its image.
  [Statement and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/algebra.tex#L3172).
- **Four equivalent quasi-coherence criteria** — EGA I, Theorem 1.4.1:
  a consolidated theorem for quasi-compact opens of affine schemes, relating
  extension from an ambient module and localization of global sections.
  [Statement and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/properties.tex#L2483).

[Detailed coverage and remaining work](ega/README.md).

### Verdier: an obstruction to functorial cones — one proposition integrated

**Astérisque 239, Chapter II, Proposition 1.2.13:** a functorial choice of
distinguished cone triangles, together with countable products or coproducts,
forces every morphism to decompose as a split projection followed by a split
inclusion. The draft adds the functoriality argument and connects it to
existing Stacks results on splitting idempotents and decomposability.
[Statement and proof](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/blob/6c5f549dcdec6051dfeaf0e5300faf3b80576830/derived.tex#L825).
This is one bounded contribution, not an integration of the whole thesis.

### Tôhoku: substantial comparison and draft-proof work — not fully integrated

The preserved research dossier records work on difficult parts of
Grothendieck’s paper, including **right satellites under injective-effacement
hypotheses** (Theorem 2.2.2), **Leray spectral sequences with families of
supports** (Theorem 3.7.3), and **equivariant Čech comparison and Ext spectral
sequences** (Theorems 5.5.6 and 5.6.3).

However, several proofs referenced by that historical dossier are absent from
this branch’s current LaTeX. The composite-functor spectral sequence here also
still has stronger hypotheses than the dossier’s proposed version.
**The entire paper must not be counted as integrated.** Results already in
official Stacks—such as enough injectives in a Grothendieck category—are
existing coverage, not AI contributions.
[Preserved dossier](tohoku_r71/STATUS.md) ·
[Concrete integration gap](ROADMAP.md#tohoku-source-integration-gap).

### Corrections to the inherited Stacks text — integrated with comparisons

The draft also corrects mathematical typing, indices, references, and prose.
Examples include:

- **Naive cotangent-complex functoriality:** correcting which cotangent
  complex is pulled back and which is the target of the comparison map.
  [Original and replacement](CHANGES_FROM_UPSTREAM.md#mc-stk-err-1214).
- **Localization at an object of a site:** using the sheaf category of the
  slice site in place of an unrelated quotient topos in the proof.
  [Original and replacement](CHANGES_FROM_UPSTREAM.md#mc-stk-err-1287).
- **Functoriality of derived internal Hom:** restoring a missing arrow in a
  distinguished triangle and correcting the direction of a comparison map.
  [Triangle](CHANGES_FROM_UPSTREAM.md#mc-stk-err-1297) ·
  [comparison map](CHANGES_FROM_UPSTREAM.md#mc-stk-err-1312).
- **Commutative-algebra proofs:** repairing mismatched ring indices,
  localization subscripts, and the use of all minimal primes in a
  reduced-ring injection. These are local corrections, not replacement
  proofs of the entire chapter.
  [Chapter-by-chapter comparisons](ai-integrated/changes/index.html).

Not every edit is a mathematical error correction: some improve prose or
normalize equivalent notation. For example, the two summation conventions
in [MC-STK-ERR-1345](CHANGES_FROM_UPSTREAM.md#mc-stk-err-1345) mean the same
thing. [The classification clarification](ai-integrated/registry/admission-receipts/r38-clarification-0001.json)
records that distinction explicitly.

[Browse every recorded correction](CHANGES_FROM_UPSTREAM.md). This comparison
places the pinned original beside the replacement and links the source,
rationale, and review evidence. The [offline HTML browser](ai-integrated/changes/index.html)
adds search and chapter filters. The original
[official Stacks snapshot](https://github.com/stacks/stacks-project/tree/a04446e57ec1fbc252a871afcec7752fb2807b14)
remains directly accessible.

## Read, inspect, and reproduce

Start with a theorem above, inspect its proof and dependencies, then compare it
with the historical source and the upstream Stacks text. There is no expectation
that a reader accept a result because an AI or an automated check produced it.

- [Latest readable PDF/source package](https://github.com/KokunoYumeto/unofficial-stacks-project-ai-drafts/releases/latest)
  · [Zenodo preservation lineage](https://doi.org/10.5281/zenodo.22135180).
- [Latest EGA review checkpoint: I §6.6.3](validation/ega-i-6.6.3-semantic-checkpoint-2026-08-30.json)
  · [archived version](https://doi.org/10.5281/zenodo.22177421).
- [Build and validation instructions](VALIDATION.md)
  · [exact current build evidence](validation/README.md).
- [Complete project status](STATUS.md) · [roadmap](ROADMAP.md)
  · [source provenance and preserved histories](PROVENANCE.md).

The inherited build entry point remains:

~~~sh
make pdfs
~~~

The repository integrity check is:

~~~sh
python tools/validate_unified_repository.py --pre-publication
~~~

## Attribution and licensing

The pinned Stacks source and this modified source are distributed under the
GNU Free Documentation License 1.2; see [COPYING](COPYING).
Registry metadata and schemas have the separate, narrow rights statement in
[ai-integrated/RIGHTS.md](ai-integrated/RIGHTS.md). Source-edition links above
do not imply common licensing or endorsement by the original authors.
