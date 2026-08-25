# R4 independent review: `sheaves.tex`, SHEAVES-024--SHEAVES-051

Date of review: 2026-08-22 (Europe/Berlin)

## Authority and review boundary

This review is limited to the following frozen English authority and to the exact local contexts and in-file definitions or lemmas needed to decide SHEAVES-024--SHEAVES-051:

- repository identity: `stacks/stacks-project`
- commit identity supplied by the frozen authority/intakes: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- authority file: `sheaves.tex`
- exact local path: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sheaves.tex`
- recomputed bytes: `184841`
- recomputed SHA-256: `AC4F9EDC7DB85E66329806EC9EA42816187A469772844BAEA663E1C9A9F00B38`

The recomputed authority identity agrees with both new intakes. No Git operation was used.

## Frozen intake identities

These byte counts and hashes were independently recomputed from the exact local intake files.

| Intake | Bytes | SHA-256 | IDs |
|---|---:|---|---|
| `ERRATA_R4_SUPPLEMENT_SHEAVES_024_045_20260822.json` | 9848 | `AF6BE3060162A8DEEA9343029253750942F766CD51CF4D85024425414126EF86` | 024--045 |
| `ERRATA_R4_SUPPLEMENT_SHEAVES_046_051_20260822.json` | 4751 | `B354547FE7BC37D108253544106D58AABB81AC43A5C6DE110A7C2FD24A54FCF5` | 046--051 |

## Disposition summary and deduplication

“Accepted” means an objective mathematical, typing, grammatical, or typographical defect is present in the frozen authority at the cited locus. “Rejected” would mean only optional style or defensible intentional notation; no hypothesis in this batch falls into that class. No item requires evidence outside this file, so none is deferred.

| Disposition | Count | IDs |
|---|---:|---|
| Accepted | 28 | 024--051 |
| Rejected | 0 | none |
| Deferred | 0 | none |

Linked occurrences are not multiplied into new hypotheses: SHEAVES-043 covers both identical singular-image/agreement errors in the same proof; SHEAVES-046 covers both unparenthesized `i_*\mathcal F` stalk expressions; and SHEAVES-050 is the single terminology/number finding for the four singular gluing-object references. SHEAVES-025 and SHEAVES-026 remain separate because the former is a malformed sentence around the correctly typed composite, whereas the latter is a later summary that actually omits a required map.

## Per-hypothesis decisions

### SHEAVES-024 — ACCEPTED (assignment notation/type)

**Locus:** lines 2435--2437.

The sentence calls both expressions object assignments defining functors. The first correctly uses `\mathcal F\mapsto f_*\mathcal F`; the second uses `\mathcal G\to f_p\mathcal G`. A right arrow denotes a morphism, but these two objects live on different spaces and no such morphism is being defined. The immediately preceding formulas, lines 2424--2429, define the object function of `f_p`, so `\mapsto` is forced by both parallel grammar and type.

**Adverse evidence considered:** arrows are sometimes used informally to describe mappings, and the word “assignments” lets a reader recover the intent. Here the adjacent parallel expression fixes the notation and the bare right arrow otherwise asserts a nonexistent cross-category morphism.

**Smallest exact replacement:**

```text
OLD: $\mathcal{G} \to f_p\mathcal{G}$
NEW: $\mathcal{G} \mapsto f_p\mathcal{G}$
```

### SHEAVES-025 — ACCEPTED (successive finite predicates)

**Locus:** lines 2455--2464.

The clause first says that “the corresponding map ... **is** the map” displayed as `f_*\psi\circ i_\mathcal G`, then immediately gives the same subject a second predicate, “**is also** a map,” without ending or coordinating the first construction. Removing the redundant pre-identification leaves one subject and one finite predicate; the displayed composite already includes its domain and codomain.

**Adverse evidence considered:** the mathematical composite is correct and completely typed. This is a sentence-level defect only, but the two uncoordinated occurrences of “is” cannot form one grammatical clause.

**Smallest coherent exact replacement:**

```text
OLD: then the corresponding map
     $\mathcal{G} \to f_*\mathcal{F}$ is the map
     $f_*\psi \circ i_\mathcal{G} :
     \mathcal{G} \to f_* f_p \mathcal{G} \to f_* \mathcal{F}$
     is also a map of abelian presheaves.
NEW: then the corresponding map
     $f_*\psi \circ i_\mathcal{G} :
     \mathcal{G} \to f_* f_p \mathcal{G} \to f_* \mathcal{F}$
     is also a map of abelian presheaves.
```

### SHEAVES-026 — ACCEPTED (substantive ill-typed adjunction summary)

**Locus:** lines 2455--2476.

The types are

```text
\psi : f_p\mathcal G \to \mathcal F,
f_*\psi : f_*f_p\mathcal G \to f_*\mathcal F,
i_\mathcal G : \mathcal G \to f_*f_p\mathcal G.
```

Thus `f_*\psi` alone does not belong to the claimed target Hom set
`\operatorname{Mor}(\mathcal G,f_*\mathcal F)`; its source is `f_*f_p\mathcal G`, not `\mathcal G`. Precomposition with the unit gives the typed adjunct
`f_*\psi\circ i_\mathcal G : \mathcal G\to f_*\mathcal F`, exactly as lines 2461--2463 state. The summary at line 2474 drops this indispensable factor.

**Adverse evidence considered:** the full construction earlier in the paragraph is correct, so the adjunction proof is recoverable. That confines the defect to the summary but does not make the summary map typeable.

**Smallest exact replacement:**

```text
OLD: $\psi \mapsto f_*\psi$
NEW: $\psi \mapsto f_*\psi \circ i_\mathcal{G}$
```

### SHEAVES-027 — ACCEPTED (substantive variance reversal)

**Locus:** lines 2479--2483.

For `f:X\to Y`, the file defines `f_*\mathcal F(V)=\mathcal F(f^{-1}V)` at lines 2424--2429. Therefore `\mathcal F` must be on `X`, while `f_*\mathcal F` is on `Y`. The Hom categories at lines 2490--2496 independently confirm `f_*:\mathit{Ab}(X)\to\mathit{Ab}(Y)`. The source sentence reverses both spaces and is not typeable as written.

**Adverse evidence considered:** the surrounding formulas make the intended variance unmistakable, but recoverability does not cure the two false object classifications.

**Smallest exact replacement:**

```text
OLD: If $\mathcal{F}$ is an abelian sheaf on $Y$, then $f_*\mathcal{F}$
     is an abelian sheaf on $X$.
NEW: If $\mathcal{F}$ is an abelian sheaf on $X$, then $f_*\mathcal{F}$
     is an abelian sheaf on $Y$.
```

### SHEAVES-028 — ACCEPTED (subject–predicate comma)

**Locus:** lines 2686--2690.

The complete subject is “the natural setting for defining the pullback and pushforward functors”; “is” is its predicate. A comma cannot separate that subject from its verb. “The natural setting” is singular, so the existing verb number is correct and only the comma must be removed.

**Adverse evidence considered:** a speaker might pause after the long subject, but that rhetorical pause is not a grammatical comma in this declarative sentence.

**Smallest exact replacement:**

```text
OLD: the pullback and pushforward functors, is the setting
NEW: the pullback and pushforward functors is the setting
```

### SHEAVES-029 — ACCEPTED (double finite construction)

**Locus:** lines 2708--2710.

After imperative “Let,” a predicate adjective is introduced with infinitive “be”: “Let `V` be open.” The source combines that construction with finite “is,” yielding two incompatible finite frames.

**Adverse evidence considered:** the intended open subset is obvious and the following formula is correctly typed. The local clause remains ungrammatical.

**Smallest exact replacement:**

```text
OLD: Let $V \subset Y$ is open.
NEW: Let $V \subset Y$ be open.
```

### SHEAVES-030 — ACCEPTED (double finite construction)

**Locus:** lines 2741--2743.

The same grammatical derivation as SHEAVES-029 applies: “Let” selects “be,” not the finite verb “is.” Here the subsequent colimit also confirms that `U` is an open subset of `X`.

**Adverse evidence considered:** none beyond immediate recoverability of the intended condition.

**Smallest exact replacement:**

```text
OLD: Let $U \subset X$ is open.
NEW: Let $U \subset X$ be open.
```

### SHEAVES-031 — ACCEPTED (sentence-boundary fragment)

**Locus:** lines 2802--2809.

The displayed equality ends with a period, so “according to Section ...” begins a new lowercase prepositional fragment with no subject or verb. Removing that display-final period attaches the citation to “we have [equality]” and leaves the period after the citation as the single sentence terminator.

**Adverse evidence considered:** displayed mathematics can be followed by a continuation beginning in lowercase, but only when its punctuation does not already close the sentence.

**Smallest exact replacement:**

```text
OLD: \Mor_{\textit{PAb}(Y)}(\mathcal{G}, f_*\mathcal{F}).
NEW: \Mor_{\textit{PAb}(Y)}(\mathcal{G}, f_*\mathcal{F})
```

### SHEAVES-032 — ACCEPTED (substantive presheaf/sheaf misclassification)

**Loci:** lines 2835--2838 and 2871--2873.

The lemma assumes `\mathcal F` is a **presheaf** of `\mathcal O`-modules and all three Hom sets are in `\mathit{PMod}`. Consequently
`f_*(\mathcal F_{f_pf_*\mathcal O})=f_*\mathcal F` is an equality of underlying abelian presheaves. Nothing in the proof sheafifies either side.

The distinction is substantive. Take `f=\mathrm{id}`, a nonzero constant ring presheaf, and its nonzero constant module presheaf. Its value on the empty open is nonterminal/nonzero, so by Remark `remark-confusion` (lines 527--542) it is not a sheaf. It nevertheless satisfies the lemma’s presheaf hypotheses. Hence “abelian sheaves” is false for allowed inputs.

**Adverse evidence considered:** the equality and linearity are correct; only the object class is wrong, and nearby categories reveal the intended word.

**Smallest exact replacement:**

```text
OLD: of abelian sheaves which is $f_*\mathcal{O}$-linear.
NEW: of abelian presheaves which is $f_*\mathcal{O}$-linear.
```

### SHEAVES-033 — ACCEPTED (sentence fragment and reference number)

**Locus:** lines 2952--2962.

The display closes with a period. Lowercase “where” therefore starts a relative fragment rather than continuing the preceding sentence. In addition, “Lemmas” is plural but introduces exactly one reference, `\ref{lemma-adjoint-push-pull-presheaves-modules}`. Beginning an independent sentence and making the citation noun singular fixes both objective defects.

**Adverse evidence considered:** removing the display period could instead attach a `where`-clause, but the producer’s sentence already contains the complete command “Argue by the equalities”; an independent explanatory sentence is clearer and no larger in mathematical content.

**Smallest coherent exact replacement:**

```text
OLD: where the second is
     Lemmas \ref{lemma-adjoint-push-pull-presheaves-modules}
NEW: The second equality is
     Lemma \ref{lemma-adjoint-push-pull-presheaves-modules}
```

### SHEAVES-034 — ACCEPTED (lowercase relative fragment)

**Locus:** lines 2986--2998.

The displayed equalities end with a period, so lowercase “which” has no antecedent in its sentence and cannot stand as an independent subject. Replacing it with the explicit subject “These equalities” yields a complete sentence; plural “equalities” also agrees with “are.”

**Adverse evidence considered:** deleting the display-final period would also make the relative clause attach to “equalities.” The explicit-subject repair is exact and avoids relying on punctuation across a long display.

**Smallest exact replacement:**

```text
OLD: which are a combination of
NEW: These equalities are a combination of
```

### SHEAVES-035 — ACCEPTED (broken parallel syntax; typed module structure)

**Locus:** lines 3122--3128.

The relative clause has one finite predicate, “which ... equals `f_*\mathcal F`,” followed by the nonparallel phrase “and with module structure given.” No verb governs the second conjunct. Mathematically, Lemma `lemma-pushforward-module` first makes `f_*\mathcal F` an `f_*\mathcal O_X`-module, and the map
`f^\sharp:\mathcal O_Y\to f_*\mathcal O_X` then restricts scalars to give the required `\mathcal O_Y`-module. Naming the underlying abelian sheaf and module structure in parallel “whose” clauses records exactly those types.

**Adverse evidence considered:** the intended construction is recoverable from the cited lemma and ring map, so no mathematical operation must change. The written relative clause is nevertheless incomplete.

**Smallest coherent exact replacement:**

```text
OLD: sheaf of $\mathcal{O}_Y$-modules which as a sheaf
     of abelian groups equals $f_*\mathcal{F}$ and with
     module structure given by the restriction
     via $f^\sharp : \mathcal{O}_Y \to f_*\mathcal{O}_X$
     of the module structure given
     in Lemma \ref{lemma-pushforward-module}.
NEW: sheaf of $\mathcal{O}_Y$-modules whose underlying sheaf
     of abelian groups is $f_*\mathcal{F}$ and whose
     module structure is obtained by restriction of scalars
     via $f^\sharp : \mathcal{O}_Y \to f_*\mathcal{O}_X$
     from the module structure given
     in Lemma \ref{lemma-pushforward-module}.
```

### SHEAVES-036 — ACCEPTED (malformed three-part introductory list)

**Locus:** lines 3206--3211.

“Given” governs three hypotheses: a morphism, a sheaf `\mathcal F`, and a sheaf `\mathcal G`. The source inserts “and” before the second item but no conjunction or repeated governing word before the third, making `\mathcal G` an unattached noun phrase. Parallel comma-separated items with “and” before the last restore the grammar.

**Adverse evidence considered:** the types of `\mathcal F` and `\mathcal G` are clear from their module rings, so this is not a mathematical ambiguity. It is still an objective coordination defect.

**Smallest exact replacement:**

```text
OLD: Given a morphism of ringed spaces
     $(f, f^\sharp) : (X, \mathcal{O}_X) \to (Y, \mathcal{O}_Y)$,
     and a sheaf of $\mathcal{O}_X$-modules $\mathcal{F}$,
     a sheaf of $\mathcal{O}_Y$-modules $\mathcal{G}$ on $Y$,
NEW: Given a morphism of ringed spaces
     $(f, f^\sharp) : (X, \mathcal{O}_X) \to (Y, \mathcal{O}_Y)$,
     a sheaf of $\mathcal{O}_X$-modules $\mathcal{F}$, and
     a sheaf of $\mathcal{O}_Y$-modules $\mathcal{G}$ on $Y$,
```

### SHEAVES-037 — ACCEPTED (missing boundary after introductory data)

**Locus:** lines 3230--3236.

The initial participial phrase supplies two data: an `f`-map and a point `x`. A comma must close that phrase before the main subject “the induced map on stalks.” The existing comma before “and” incorrectly splits a two-item coordination while no comma marks its end.

**Adverse evidence considered:** the display and following verb “is” let a reader reconstruct the boundary. Punctuation recovery does not make the written sentence grammatical.

**Smallest exact replacement:**

```text
OLD: as above, and $x \in X$ the induced map on stalks
NEW: as above and $x \in X$, the induced map on stalks
```

### SHEAVES-038 — ACCEPTED (missing complement marker)

**Locus:** lines 3273--3278.

Standard English permits “denote the inclusion by `i_x`” or “denote by `i_x` the inclusion,” but not the double-object construction “Denote `i_x` the inclusion map.” Using “Let ... be ...” gives the symbol a grammatical predicate and preserves the exact mathematical definition.

**Adverse evidence considered:** the same compressed “Denote symbol object” pattern occurs elsewhere in this file, so the intent is established house usage. Recurrence makes it recoverable, not standard English grammar; the queue item is accepted as a copyedit, not a mathematical defect.

**Smallest exact replacement:**

```text
OLD: Denote $i_x : \{x\} \to X$ the inclusion map.
NEW: Let $i_x : \{x\} \to X$ be the inclusion map.
```

### SHEAVES-039 — ACCEPTED (missing copula)

**Locus:** lines 3331--3335.

In “let `x\in X` a point,” “a point” is the predicate nominative and requires “be” after imperative “let.” The comma before “and let” does not supply that copula.

**Adverse evidence considered:** the previous lemma uses the compact apposition “`x\in X` a point” inside a list, but after the finite directive “let” the missing “be” is objective.

**Smallest exact replacement:**

```text
OLD: let $x \in X$ a point.
NEW: let $x \in X$ be a point.
```

### SHEAVES-040 — ACCEPTED (missing conjunction)

**Locus:** lines 3341--3343.

The statement announces two parallel cases, abelian groups and algebraic structures. A comma alone does not coordinate the final two items of a two-item list; “and” is required.

**Adverse evidence considered:** punctuation makes the intended enumeration visible, but the absent coordinator remains a grammatical omission.

**Smallest exact replacement:**

```text
OLD: abelian groups, algebraic structures.
NEW: abelian groups and algebraic structures.
```

### SHEAVES-041 — ACCEPTED (substantive free index)

**Locus:** lines 3511--3521.

The proof selects and numerically reindexes a finite cover as
`U=\bigcup_{j=1,\ldots,m}U_j`. The next line quantifies intersections over `j,j'\in J`, but no `J` is defined in this proof paragraph and the actual family now has index set `{1,\ldots,m}`. Subsequent symbols `i_j`, `s_j`, and `i_{jj'}` all use the numerical indexing, proving the intended range.

The lemma statement’s part (4) uses `J` as a generic index set for a member of a cofinal system, but once the chosen finite cover is explicitly relabelled `1,\ldots,m`, an unexplained `J` does not type the indices of the displayed `U_j` family. Reading `J={1,\ldots,m}` is possible only by supplying an unstated identification.

**Adverse evidence considered:** the earlier generic `J` makes the typo easy to recover and the proof remains mathematically sound after that inference. The free index is still a formal defect.

**Smallest exact replacement:**

```text
OLD: quasi-compact for all $j, j' \in J$ and
NEW: quasi-compact for all $1 \leq j, j' \leq m$ and
```

### SHEAVES-042 — ACCEPTED (substantive untypeable composition order)

**Locus:** lines 3587--3592.

The diagram convention at lines 3558--3562 is: for `a:j\to i`,
`f_a:X_j\to X_i`. Given `b:k\to j`, the composable categorical arrow is
`a\circ b:k\to i`, so the corresponding space map is
`f_{a\circ b}:X_k\to X_i`. The proof correctly uses
`f_{a\circ b}^{-1}` at lines 3581 and 3621. By contrast, `b\circ a` would require the codomain `i` of `a` to equal the domain `k` of `b`; it is not defined in the stated diagram. Consequently `f_{b\circ a}` at line 3591 has no type.

**Adverse evidence considered:** a reader can infer the intended order from the preceding formula and the projection point `p_k(x)`. That supplies the correction but does not type the written composite.

**Smallest exact replacement:**

```text
OLD: $(f_{b \circ a}^{-1}\mathcal{G})_{p_k(x)}$
NEW: $(f_{a \circ b}^{-1}\mathcal{G})_{p_k(x)}$
```

### SHEAVES-043 — ACCEPTED (number/agreement; two linked occurrences)

**Primary locus:** lines 3587--3591. **Linked identical occurrence:** lines 3582--3584.

Two sections, `s` and `s'`, have two stalk images that are compared. Singular “the image” would denote one collective image and requires singular “is”; the existing plural verb “are” and the binary comparison “different” force plural “images.” The same exact error appears once in the definition of `Z_k` and once in the contradiction on the inverse limit, so both are one repeated finding under this ID.

**Adverse evidence considered:** ellipsis can suppress the second noun in “the image of `s` and [the image of] `s'`,” but then the overt head should still be repeated or pluralized to agree with “are.”

**Smallest exact replacement, applied at both occurrences:**

```text
OLD: the image of $s$ and $s'$
NEW: the images of $s$ and $s'$
```

### SHEAVES-044 — ACCEPTED (missing copula and noun number)

**Locus:** lines 3606--3608.

After “we may assume,” the first complement is the full clause “`L` is finite.” The coordinated second complement has plural subject “`W_l` and `V_{l,i}`” but no verb. It requires “are”; because it classifies two open subsets, the count noun is plural “opens.”

**Adverse evidence considered:** “quasi-compact open” is standard as a singular mathematical noun phrase, but two separately named subsets cannot take that bare singular phrase without a copula.

**Smallest exact replacement:**

```text
OLD: we may assume $L$ is finite and $W_l$ and $V_{l, i}$ quasi-compact open
NEW: we may assume $L$ is finite and $W_l$ and $V_{l, i}$ are quasi-compact opens
```

### SHEAVES-045 — ACCEPTED (missing complement marker)

**Locus:** lines 3615--3618.

In the notation-setting construction “write symbol for expression,” the preposition “for” marks what the new symbol denotes. Without it, “the restriction” is an unattached second noun phrase. The types confirm that `s_{l,j}` is being defined to be the stated restricted pullback.

**Adverse evidence considered:** compressed notation makes the intended definition unambiguous, but standard English does not license “Write `s` the restriction.”

**Smallest exact replacement:**

```text
OLD: Write $s_{l, j}$ the restriction
NEW: Write $s_{l, j}$ for the restriction
```

### SHEAVES-046 — ACCEPTED (stalk parenthesization/type; two occurrences)

**Loci:** lines 4940--4947 and 5041--5046.

The lemma concerns the stalk at `x` of the pushforward sheaf, whose typed expression is `(i_*\mathcal F)_x`. In the bare expression `i_*\mathcal F_x`, ordinary subscript binding first forms `\mathcal F_x` and then appears to apply `i_*` to it. That parse is impossible: `i_*` takes a sheaf on `Z`, while `\mathcal F_x` is a set and is not even defined when the displayed case assumes `x\notin Z`. The nearby line 5041 uses `(i_*\mathcal F)_x` unambiguously and fixes the intended grouping.

**Adverse evidence considered:** experts may give functor application wider informal precedence and infer the stalk of the pushforward from the prose. The alternate standard parse is ill-typed, so parentheses are warranted rather than merely cosmetic.

**Smallest exact replacement, applied to the `\mathcal F` expression at lines 4942 and 5045:**

```text
OLD: $i_*\mathcal{F}_x$
NEW: $(i_*\mathcal{F})_x$
```

### SHEAVES-047 — ACCEPTED (wrong part of speech)

**Locus:** lines 4990--4993.

“Faithfulness” is a noun. The property that a functor is both full and faithful is the compound noun phrase “full faithfulness,” using adjective “full.” “Fully” is an adverb and cannot directly modify the noun “faithfulness” in this construction.

**Adverse evidence considered:** “fully faithful” is correct when both words form an adjectival predicate, as in the lemma. Nominalizing that phrase changes “fully” to “full.”

**Smallest exact replacement:**

```text
OLD: Fully faithfulness
NEW: Full faithfulness
```

### SHEAVES-048 — ACCEPTED (substantive undefined and ill-typed section)

**Locus:** lines 5123--5135.

At the start of the proof, `s\in\mathcal F(U)`. The desired naturality identity is explicitly
`(\varphi_U(s))|_V=\varphi_V(s|_V)` at lines 5123--5127. No symbol `s_V` is defined anywhere in the argument. Moreover, `\varphi_V` has domain `\mathcal F(V)`, so its input must be the restriction `s|_V\in\mathcal F(V)`. The preceding line 5133 likewise uses `s|_{V\cap U_i}`, and restricting `\varphi_V(s|_V)` to `V\cap U_i` gives exactly that local term.

**Adverse evidence considered:** `s_V` is sometimes informal notation for a restriction, but this file established `s|_V` as its restriction notation at lines 106--109, and the current proof itself uses that notation throughout. No local definition licenses the new subscript.

**Smallest exact replacement:**

```text
OLD: $\varphi_V(s_{V})|_{V \cap U_i}$
NEW: $\varphi_V(s|_V)|_{V \cap U_i}$
```

### SHEAVES-049 — ACCEPTED (missing article/linking syntax)

**Locus:** lines 5136--5140.

“Open subset” is a singular count-noun phrase. In “given `U\subset X` open subset” it has neither a determiner nor a copula/appositive marker. Moving the adjective before the noun and adding “an” produces the standard quantified phrase.

**Adverse evidence considered:** postpositive shorthand “given `U\subset X` open” is common. Appending the bare singular noun “subset” makes the actual source phrase grammatically incomplete.

**Smallest exact replacement:**

```text
OLD: since given $U \subset X$ open subset
NEW: since given an open subset $U \subset X$
```

### SHEAVES-050 — ACCEPTED (singular datum/plural data; linked occurrences)

**Loci:** lines 5186--5189, 5191--5197, 5233--5238, and 5252--5259.

The pair of families `(\mathcal F_i,\varphi_{ij})` satisfying the cocycle condition is one gluing object. In edited mathematical English its singular is “datum” and its plural is “data.” The phrases “a ... data” at lines 5188, 5236, and 5256 are objectively incompatible with treating “data” as an ordinary plural; even modern mass-noun usage does not normally license the count article “a data.” Line 5195 quantifies one such object, so “any gluing datum” gives the terminology a consistent singular. Later references to a collection or category of gluing data, such as lines 5287--5300, correctly retain plural “data.”

**Adverse evidence considered:** modern English often treats “data” as a mass singular, and “any gluing data” at line 5195 is defensible in isolation. That defence cannot license the three explicit `a data` constructions, while `datum` supplies the smallest one-word repair and cleanly distinguishes one descent object from a plural collection.

**Smallest exact replacements, bundled under this one ID:**

```text
OLD: a {\it glueing data for sheaves of sets
NEW: a {\it glueing datum for sheaves of sets

OLD: Given any glueing data $(\mathcal{F}_i, \varphi_{ij})$
NEW: Given any glueing datum $(\mathcal{F}_i, \varphi_{ij})$

OLD: the definition of a glueing data
NEW: the definition of a glueing datum

OLD: be a glueing data
NEW: be a glueing datum
```

### SHEAVES-051 — ACCEPTED (spurious article before gerund)

**Locus:** lines 5224--5228.

After preposition “by,” the gerund “restricting” directly introduces the means: “by restricting each ...”. The article “the” could introduce a nominalized construction only with an `of` phrase (“by the restricting of ...”), which is not the syntax here. It therefore has no grammatical head.

**Adverse evidence considered:** none; deleting the article preserves the exact operation and yields the standard construction.

**Smallest exact replacement:**

```text
OLD: are defined by the restricting each of the $s_i$
NEW: are defined by restricting each of the $s_i$
```

## No-source-mutation and no-contact boundary

This is an evidentiary review only. No byte of `sheaves.tex`, either intake JSON, any translation, or any other authority/control artifact was edited. No overlay admission was made, no Git operation was run, and no upstream Stacks contact, issue, or pull request was initiated. The only filesystem mutation made for this task is creation of this requested private review file.
