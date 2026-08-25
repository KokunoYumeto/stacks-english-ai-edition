# Independent review: R4 Sites hypotheses SITES-001--004

Date: 2026-08-22

Scope: independent canon-side review of exactly four French-lane hypotheses against the frozen Stacks authority. This review does not modify the authority, any translation, or any candidate payload.

## Evidence identities recomputed before review

- Authority: `upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/sites.tex`
  - bytes: 424,197
  - SHA-256: `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
  - identity result: exact match to the frozen authority named by the intake
- Intake: `canon/control/ERRATA_R4_SUPPLEMENT_SITES_001_004_20260822.json`
  - bytes: 3,624
  - SHA-256: `24D9E603AB5E035BD8AFED54F15ADE974130FEC1F26854161BA09562E0A8C541`
  - identity result: exact match

Review method: each cited locus was reopened in the authority with its surrounding lemma or proof. Grammar-only and typographical findings were separated from mathematical-content findings. Awkward but grammatically and mathematically recoverable prose was not promoted to verified erratum merely because a rewrite might read better.

## Aggregate disposition

- ACCEPTED: 3 (`SITES-001`, `SITES-002`, `SITES-004`)
- REJECTED: 1 (`SITES-003`)
- DEFERRED: 0

## Item reviews

### SITES-001 -- ACCEPTED

- Exact locus: `sites.tex:2580-2582`, lemma `lemma-adjoint-sheaves`.
- Authority text:

  ```tex
  In the situation of Lemma \ref{lemma-pushforward-sheaf}.
  The functor $u_s : \mathcal{G} \mapsto (u_p \mathcal{G})^\#$
  is a left adjoint to $u^s$.
  ```

- Reasoning: `In the situation of Lemma ...` is a prepositional phrase, not an independent clause. The full stop therefore leaves an objective sentence fragment at the start of a lemma statement. Joining it to the following clause changes no mathematical content: the referenced lemma supplies the sites and continuous functor, while the present lemma asserts the adjunction.
- Adverse evidence considered: a fragment can sometimes function as a displayed heading or label, but this occurrence is ordinary running prose inside a lemma and has neither heading markup nor a colon. The following capitalized sentence does not repair the missing predicate.
- Smallest exact replacement:

  ```tex
  In the situation of Lemma \ref{lemma-pushforward-sheaf}, the functor
  $u_s : \mathcal{G} \mapsto (u_p \mathcal{G})^\#$
  is a left adjoint to $u^s$.
  ```

- Classification: verified grammar defect; no formula or claim changes.

### SITES-002 -- ACCEPTED

- Exact locus: `sites.tex:2595-2597`, lemma `lemma-technical-up`.
- Authority text:

  ```tex
  In the situation of Lemma \ref{lemma-pushforward-sheaf}.
  For any presheaf $\mathcal{G}$ on $\mathcal{C}$
  we have $(u_p\mathcal{G})^\# = (u_p(\mathcal{G}^\#))^\#$.
  ```

- Reasoning: this is the same objectively incomplete prepositional fragment as SITES-001. The intended scope is unambiguous from the referenced lemma and the quantified presheaf in the next line. Joining the phrase to the quantification restores one grammatical sentence without altering the equality.
- Adverse evidence considered: as in SITES-001, there is no structural signal that the fragment is intended as a heading. Retaining two sentences cannot be defended as a complete grammatical construction.
- Smallest exact replacement:

  ```tex
  In the situation of Lemma \ref{lemma-pushforward-sheaf}, for any presheaf
  $\mathcal{G}$ on $\mathcal{C}$
  we have $(u_p\mathcal{G})^\# = (u_p(\mathcal{G}^\#))^\#$.
  ```

- Classification: verified grammar defect; no formula or claim changes.

### SITES-003 -- REJECTED

- Exact locus: `sites.tex:2811-2824`, especially `2821-2823`, proof of `lemma-directed-morphism`.
- Authority text:

  ```tex
  And since sheafification commutes with finite limits as well
  (Lemma \ref{lemma-sheafification-exact}) we conclude because
  $u_s = \# \circ u_p$.
  ```

- Reasoning: the prose is awkward, but the claimed objective incompleteness is not established. In mathematical prose, `we conclude` can be used intransitively with the pending conclusion supplied by the immediately preceding proof goal. Here lines 2814-2815 explicitly say that it suffices to prove that `u_s` commutes with finite limits; lines 2816-2820 establish that `u_p` does so; lines 2821-2823 add exactness of sheafification and the identity `u_s = \# \circ u_p`. The conclusion and its two premises are therefore fully recoverable and correctly typed.
- Adverse evidence considered: the same authority uses the intransitive construction `Then we conclude using ...` at `sites.tex:2151-2152`. Replacing `because` by `using`, or recasting the sentence as `..., we conclude using $u_s = \# \circ u_p$`, would be a reasonable copy-edit, but it would improve style rather than repair a proven grammatical or mathematical defect.
- Disposition consequence: no admitted correction. Preserve the frozen wording unless a later editorial policy explicitly admits optional style normalization.
- Classification: optional proof-prose copy-edit, not a verified erratum; the mathematical argument is sound.

### SITES-004 -- ACCEPTED

- Exact locus: `sites.tex:2832-2834`, item 1 of `proposition-get-morphism`.
- Authority text:

  ```tex
  \item the category $\mathcal{C}$ has a final object $X$ and
  $u(X)$ is a final object of $\mathcal{D}$ , and
  ```

- Reasoning: the literal space between the closing math delimiter and the comma is an objective TeX-source typography defect. It can introduce interword glue before the punctuation and is inconsistent with ordinary punctuation placement. Deleting it changes neither the proposition's hypothesis nor its notation.
- Adverse evidence considered: source line wrapping and TeX's treatment of some whitespace can make such defects visually subtle, but there is no grammatical or mathematical reason to place a space before an English comma.
- Smallest exact replacement:

  ```tex
  $u(X)$ is a final object of $\mathcal{D}$, and
  ```

- Classification: verified typography defect; no mathematical content changes.

## Canon-side conclusion

The review proves three narrow non-mathematical corrections and rejects one merely stylistic rewrite. None of the four items warrants a change to a formula, hypothesis, conclusion, or proof dependency. Admission, if later authorized by the R4 closure and replay gates, should include only SITES-001, SITES-002, and SITES-004 with the exact replacements above.
