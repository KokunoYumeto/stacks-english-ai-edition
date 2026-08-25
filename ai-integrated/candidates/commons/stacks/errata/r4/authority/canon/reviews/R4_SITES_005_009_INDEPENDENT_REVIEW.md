# Independent R4 review: `SITES-005` through `SITES-009`

## Scope and frozen evidence

This review independently evaluates only the five hypotheses `SITES-005` through
`SITES-009`. It does not alter the frozen Stacks authority, any translation, or
any candidate correction payload.

- Authority: `sites.tex`, Stacks commit
  `a04446e57ec1fbc252a871afcec7752fb2807b14`
  - recomputed size: 424,197 bytes
  - recomputed SHA-256:
    `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
- Frozen intake: `ERRATA_R4_SUPPLEMENT_SITES_005_009_20260822.json`
  - recomputed size: 4,454 bytes
  - recomputed SHA-256:
    `305FCC9DB876A898491A6C60BA83E08B9ABE6C78F136513D34163C4408008E82`
- Optional French producer note, used only as a locator and adverse-evidence
  witness: `sites_part_e_notes.md`
  - recomputed size: 4,667 bytes
  - recomputed SHA-256:
    `CD1F3666C02B38776CE71994180574B7A71173CE002F12B2DF2DDD588EF4A295`

The three identities match the frozen intake. Every disposition below was then
derived from the cited English authority context rather than inherited from the
producer's classification.

## Aggregate disposition

| ID | Disposition | Class |
|---|---|---|
| `SITES-005` | **ACCEPTED** | section-typing / grammar defect |
| `SITES-006` | **ACCEPTED** | typographical defect |
| `SITES-007` | **ACCEPTED** | substantive typed-formula defect, two occurrences |
| `SITES-008` | **ACCEPTED** | grammar defect |
| `SITES-009` | **ACCEPTED** | typographical defect |

Totals: **5 accepted, 0 rejected, 0 deferred**.

## Itemized findings

### `SITES-005` — ACCEPTED

- Exact locus: `sites.tex:3354-3360`, specifically lines 3356-3359.
- Authority text:
  `such that \text{id}_U lifts to a section of $s_c$ of
  $h_{U_{\iota(c)}}^\#$ over $V_c$.`
- Reasoning: the phrase has two successive possessive uses of “of” and gives no
  prior object named `s_c`. The immediately following line types `s_c` as an
  element of `h_{U_{\iota(c)}}(V_c)` mapping to `\text{id}_U`; line 3360 then
  identifies that element with the represented morphism
  `s_c : V_c \to U_{\iota(c)}` over `U`. Thus `s_c` is the section produced by
  the lift, not an object of which another unnamed section is taken.
- Adverse evidence considered: one could parse “a section of `s_c`” if `s_c`
  were a previously defined morphism admitting a section. It is not previously
  defined, and that reading contradicts the explicit element/morphism typing on
  lines 3359-3360.
- Smallest exact replacement: replace
  `lifts to a section of $s_c$ of` with
  `lifts to a section $s_c$ of`.

### `SITES-006` — ACCEPTED

- Exact locus: `sites.tex:3405`.
- Authority text:
  `Finite copoducts of sheaves conserve quasi-compactness.`
- Reasoning: the lemma statement on lines 3407-3410 uses the categorical
  coproduct `\coprod`; “copoducts” is not the intended categorical noun and is
  a one-letter omission.
- Adverse evidence considered: no distinct technical term “copoduct” is being
  introduced, and the displayed construction makes “coproducts” unambiguous.
  The separate stylistic choice “conserve” versus “preserve” is outside this
  hypothesis and is not needed to repair the typo.
- Smallest exact replacement: replace `copoducts` with `coproducts`.

### `SITES-007` — ACCEPTED

- Exact locus: `sites.tex:3460-3474`, with erroneous occurrences on lines 3472
  and 3474.
- Authority data on lines 3424-3426: a filtered diagram
  `i \mapsto \mathcal F_i` of sheaves of sets.
- Authority elements on lines 3461-3466:
  `s \in \mathcal F_i(U)` and
  `s' \in \mathcal F_{i'}(U)`, with indices `i_a \geq i,i'` and equality
  `\varphi_{ii_a}(s)=\varphi_{i'i_a}(s')` after passing to the stated covering.
- Authority conclusion on lines 3472-3474 applies
  `\varphi_{i'i''}` to `s` twice.

#### Explicit type check

For comparable indices `j \leq k`, evaluation on `U` of the transition map has
type

`\varphi_{jk}(U): \mathcal F_j(U) \longrightarrow \mathcal F_k(U)`.

After line 3470 chooses `i'' \geq i_{\alpha(b)} \geq i,i'`, the two expressions
that can be compared in `\mathcal F_{i''}(U)` are therefore

- `\varphi_{ii''}(s)`, because `s \in \mathcal F_i(U)`; and
- `\varphi_{i'i''}(s')`, because `s' \in \mathcal F_{i'}(U)`.

By functoriality of the transition maps, the equality at the common stage
`i_{\alpha(b)}` transports to

`\varphi_{ii''}(s)|_{V_b} =
 \varphi_{i'i''}(s')|_{V_b}`.

Since the `V_b` cover `U`, the sheaf condition then gives the same equality in
`\mathcal F_{i''}(U)`. In contrast,
`\varphi_{i'i''}(s)` is not typeable from the stated data: its map has domain
`\mathcal F_{i'}(U)`, while `s` was supplied only as an element of
`\mathcal F_i(U)`.

- Adverse evidence considered: no equality `i=i'`, no map identifying
  `\mathcal F_i(U)` with `\mathcal F_{i'}(U)`, and no implicit coercion of `s`
  into the latter set is assumed. Even an unstated comparability between `i`
  and `i'` would require applying an explicit transition map; it would not make
  the printed expression well typed. Acceptance is therefore based on the
  directed-system types and transition compatibility, not merely on surface
  symmetry between `s` and `s'`.
- Smallest exact replacements, both required:
  1. line 3472:
     `\varphi_{i'i''}(s)` -> `\varphi_{i'i''}(s')`;
  2. line 3474:
     `\varphi_{i'i''}(s)` -> `\varphi_{i'i''}(s')`.

### `SITES-008` — ACCEPTED

- Exact locus: `sites.tex:3622-3628`, specifically line 3626.
- Authority text: `This is done shown in the next paragraph`.
- Reasoning: “is done shown” combines two incompatible passive constructions.
  The next paragraph indeed supplies the promised demonstration by introducing
  the maps `a_{i'}`, `b_{i'}` and their equalizers, so “is shown” accurately
  states the forward reference.
- Adverse evidence considered: “done” could instead be retained by rewriting
  the sentence as “This is done in the next paragraph”, but it cannot coexist
  with “shown” in the printed construction. The producer's proposed form is the
  smaller clear repair and preserves the intended meaning.
- Smallest exact replacement: replace `This is done shown in the next
  paragraph` with `This is shown in the next paragraph` (equivalently, delete
  `done `).

### `SITES-009` — ACCEPTED

- Exact locus: `sites.tex:3738-3744`, specifically line 3741.
- Authority text: `Since the cardinality if $I \times I$ is also less than ...`.
- Reasoning: the noun “cardinality” takes the preposition “of” here. The
  mathematical argument also parallels lines 3727-3728, which compare the
  cofinality of `\beta` with the cardinality of `I`; it now needs the
  cardinality of the pair-index set `I \times I` to choose one common upper
  stage for all `\alpha_{i,j}`.
- Adverse evidence considered: “if” cannot function as a conditional in this
  sentence because it occurs between the noun and its mathematical argument,
  and no consequent clause is introduced.
- Smallest exact replacement: replace `cardinality if` with `cardinality of`.

## Review boundary

This record proves the five dispositions against the frozen authority bytes. It
does not admit an overlay, alter the canonical translations, certify any
language edition, contact upstream, or establish correctness beyond these five
exact loci. Any derived English correction still requires the enclosing R4
closure, replay, and admission gates.
