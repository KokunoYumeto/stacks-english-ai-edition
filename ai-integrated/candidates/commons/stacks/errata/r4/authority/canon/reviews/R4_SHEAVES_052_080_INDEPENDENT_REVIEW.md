# R4 independent review: `sheaves.tex`, SHEAVES-052--SHEAVES-080

Date of review: 2026-08-22 (Europe/Berlin)

## Authority, intake, and evidence boundary

This review is limited to SHEAVES-052--SHEAVES-080 and the exact frozen English authority:

- repository identity: `stacks/stacks-project`
- commit identity supplied by the frozen intake/path: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- authority path: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sheaves.tex`
- authority bytes, independently recomputed: `184841`
- authority SHA-256, independently recomputed: `AC4F9EDC7DB85E66329806EC9EA42816187A469772844BAEA663E1C9A9F00B38`

The sole intake reviewed was:

- `ERRATA_R4_SUPPLEMENT_SHEAVES_052_080_20260822.json`
- independently recomputed bytes: `12730`
- independently recomputed SHA-256: `A09E1CD5CF73E0D67821DD02444C64D25701DD173C72CE680E7CCCB0B165812C`

The intake binds two possible note witnesses, `sheaves_part_j_notes.md` (intake-declared SHA-256 `620FD44445334B43DFECCC791B99865DCC06D5E782674D24A4E3F59D8F1374F5`) and `sheaves_part_k_notes.md` (intake-declared SHA-256 `C33300EE3356ABEA1554C79667F726687D5BC2D13EA6068B13F3BDF0A8BC16CB`). Neither note was needed to decide any claim, so neither was opened or independently rehashed. Their hashes are recorded here only as the intake-bound identities, not as review evidence. All proofs below come from the exact authority file.

No Git operation was used.

## Aggregate disposition

“Accepted” means the frozen source has an objective mathematical, typing, grammatical, terminological, or typographical defect at the locus. “Rejected” means the proposed change would normalize defensible house notation, categorical shorthand, synonymy, or register rather than repair an error. No claim requires outside evidence, so none is deferred.

| Disposition | Count | IDs |
|---|---:|---|
| Accepted | 25 | 052, 054--055, 058--071, 073--080 |
| Rejected | 4 | 053, 056--057, 072 |
| Deferred | 0 | none |

Linked instances are deduplicated under their existing IDs: SHEAVES-059 has two occurrences; SHEAVES-063 has three; SHEAVES-068 has six occurrences across three loci; SHEAVES-073 has five stalk formulas; and SHEAVES-080 has two subject–verb commas.

## Per-hypothesis review

### SHEAVES-052 — ACCEPTED (missing conjunction between axioms)

**Locus:** lines 3705--3707.

The definition imposes two predicates on the restriction system: identities for equal inclusions and composition for triples. The first clause ends with `for all U\in\mathcal B` but has neither terminal punctuation nor a conjunction before finite “whenever ... we have.” Consequently two complete axiomatic clauses run together. The analogous algebraic-structure definition at lines 4007--4010 correctly has “and whenever.”

**Adverse reading considered:** a line break can visually separate formulas, but it is not grammatical punctuation and does not coordinate the predicates.

**Smallest exact replacement:**

```text
OLD: $\rho^U_U = \text{id}_{\mathcal{F}(U)}$ for all $U \in \mathcal{B}$
     whenever $W \subset V \subset U$ in $\mathcal{B}$ we have
NEW: $\rho^U_U = \text{id}_{\mathcal{F}(U)}$ for all $U \in \mathcal{B}$ and
     whenever $W \subset V \subset U$ in $\mathcal{B}$ we have
```

### SHEAVES-053 — REJECTED (quantified, type-resolved component notation)

**Loci:** lines 3708--3711 and 4011--4016.

Both definitions say that a **rule assigns to each** `U\in\mathcal B` a map/morphism with source `\mathcal F(U)` and target `\mathcal G(U)`. Thus the family is explicitly quantified, and the displayed source and target determine which component the generic symbol `\varphi` denotes. This is the same conventional suppression used in Definition `definition-presheaf`, lines 84--94, where the rule is quantified and the square labels every horizontal component `\varphi`.

**Adverse evidence recorded:** writing `\varphi_U` would be more explicit and later prose often does so. Unlike a definition with a free `U`, however, these sentences already supply the family binder; no map is missing and no expression is ill-typed. **No replacement warranted.**

### SHEAVES-054 — ACCEPTED (colimit/directed-system terminology)

**Locus:** lines 3718--3725.

Line 3721 defines `\mathcal F_x` with `\colim`, so calling it “this limit” reverses the construction. Directedness belongs to the neighbourhood index system (ordered by reverse inclusion), and the resulting construction is therefore a directed colimit. For two basis neighbourhoods `U,V` of `x`, the basis property supplies a basis neighbourhood `W` with `x\in W\subset U\cap V`, proving directedness of that indexing preorder.

**Adverse reading considered:** “direct limit” is older terminology for a filtered/directed colimit. The source does not say “direct limit”; it calls a displayed colimit a limit and predicates “directed” of the resulting object, so an explicit repair is warranted.

**Smallest coherent exact replacement:**

```text
OLD: As in the case of the stalk of a presheaf on $X$ this limit is
     directed. The reason is that the collection of $U\in \mathcal{B}$,
     $x \in U$ is a fundamental system of open neighbourhoods of $x$.
NEW: As in the case of the stalk of a presheaf on $X$, this is a
     directed colimit. The reason is that the collection of $U\in \mathcal{B}$,
     $x \in U$ is a directed fundamental system of open neighbourhoods of $x$.
```

### SHEAVES-055 — ACCEPTED (substantive undefined restrictions)

**Locus:** lines 3916--3920.

Here `\sigma_i\in\mathcal F(U_i)` and `\sigma_j\in\mathcal F(U_j)`. A restriction `\sigma_i|_{V_{ijy}}` exists only if `V_{ijy}\subset U_i`, and similarly for `j`. Equality of the two germs at `y` means, by the stalk equivalence relation, precisely that there is a basis neighbourhood
`y\in V_{ijy}\subset U_i\cap U_j` on which the restrictions agree. The source states only membership in the basis and `y\in V_{ijy}`, so the displayed restrictions are not typed by its written hypotheses.

**Adverse reading considered:** the containment follows from what equality in the stalk means and is therefore recoverable. That inference supplies missing data; it is not present in the sentence itself.

**Smallest exact replacement:**

```text
OLD: $y \in V_{ijy}$ such that
NEW: $y \in V_{ijy} \subset U_i \cap U_j$ such that
```

### SHEAVES-056 — REJECTED (standard categorical uniqueness shorthand)

**Loci:** lines 3938--3941 and 4054--4057.

Strict object equality is not forced: if an extension is replaced away from the basis by transported isomorphic copies, one obtains an isomorphic but not literally equal sheaf with the same restriction data. What restriction to a basis determines is a sheaf together with its identification on the basis, uniquely up to a unique compatible isomorphism. The equivalence statements at lines 3968--3985 and 4104--4125 are exactly the categorical formulation of that fact.

That strict observation does not make the two sentences erroneous in their context. “There exists a unique sheaf” is standard categorical shorthand for uniqueness up to unique isomorphism, just as representing and adjoint objects are routinely called unique. The proofs construct representatives and subsequent arguments use equivalence/isomorphism, never literal set-theoretic equality between arbitrary representatives.

**Adverse evidence recorded:** adding “up to unique isomorphism” would be formally more explicit and is mathematically accurate. It is an optional categorical expansion, not a forced source correction. **No replacement warranted.**

### SHEAVES-057 — REJECTED (defensible synonym, no object change)

**Loci:** lines 4017--4019, 4041--4043, and 4173--4175.

The functor `F` sends a `\mathcal C`-valued presheaf to the set-valued presheaf `U\mapsto F(\mathcal F(U))`; line 4019 names it the “underlying presheaf of sets.” Calling that same functorially associated object “the associated presheaf of sets” at lines 4042 and 4174 introduces no new construction, no change of type, and no ambiguity in the cited sheaf property. “Associated” is an ordinary descriptive synonym here, not a separately defined technical operation such as sheafification.

**Adverse evidence recorded:** repeating the defined word “underlying” would improve terminological consistency. Consistency alone is not an erratum when both phrases identify the same typed object. **No replacement warranted.**

### SHEAVES-058 — ACCEPTED (wrong local condition label)

**Witness locus:** lines 3947--3949. **Erroneous locus:** lines 4087--4090.

The set-valued extension is defined at lines 3947--3949 by families satisfying condition `(*)` of Lemma `lemma-condition-star-sections`, lines 3901--3905. In the algebraic-structure proof, “this construction on underlying sets is the same as the definition ... above” can only refer to that set-valued extension formula. Condition `(**)` instead labels the basis sheaf gluing axiom at lines 3745--3752, not the underlying-set construction being compared. The semantic antecedent therefore forces `(*)`.

**Adverse reading considered:** every eventual extension must also satisfy the sheaf axiom `(**)`, but that is not the “definition” of its underlying sets referenced in this sentence; those sets were defined using `(*)`.

**Smallest exact replacement:**

```text
OLD: sets is the same as the definition using $(**)$ above.
NEW: sets is the same as the definition using $(*)$ above.
```

### SHEAVES-059 — ACCEPTED (defined technical phrase; two occurrences)

**Loci:** lines 4255--4256 and 4322--4323.

Definition `definition-algebraic-structure`, lines 1184--1195, defines the pair `(\mathcal C,F)` with the singular technical term “a type of algebraic structure.” The two lemmas instantiate one such pair, so pluralizing the complement changes the established term. The same section uses the exact singular form at lines 3991, 4000, 4050, and 4108.

**Adverse reading considered:** generic prose can discuss “a type of algebraic structures,” meaning a class whose members are structures. These two lines explicitly invoke the defined pair and therefore should use its defined name.

**Smallest exact replacement, applied twice:**

```text
OLD: a type of algebraic structures
NEW: a type of algebraic structure
```

### SHEAVES-060 — ACCEPTED (substantive component-domain error)

**Locus:** lines 4352--4358, confirmed by lines 4372--4375.

The lemma supplies `\varphi_V^U` only for `V\in\mathcal B_Y` and suitable `U\in\mathcal B_X` (lines 4328--4336). The proof instead fixes an arbitrary open `V\subset Y` and immediately evaluates `\varphi_V^U(s)`. For an open outside the basis that symbol has not been defined. Line 4374 explicitly returns to varying `V\in\mathcal B_Y`, confirming the intended initial range; the later basis-extension lemma then constructs the full `f`-map.

**Adverse reading considered:** one might anticipate that the proof will extend the components to all opens, but that is the construction being proved and cannot be assumed before `\varphi_V` is built.

**Smallest exact replacement:**

```text
OLD: Fix $V \subset Y$ open.
NEW: Fix $V \in \mathcal{B}_Y$.
```

### SHEAVES-061 — ACCEPTED (substantive map-kind/variance error)

**Locus:** lines 4375--4380.

The constructed object is an `f`-map with components
`\mathcal G(V)\to\mathcal F(f^{-1}V)`; unless `f` is the identity, `\mathcal G` and `\mathcal F` live on different spaces and there is no ordinary same-space sheaf morphism `\mathcal G\to\mathcal F`. The proof itself says “desired `f`-map” at line 4376. Only later, at lines 4390--4395, does adjunction produce the associated ordinary morphism `f^{-1}\mathcal G\to\mathcal F`.

**Adverse reading considered:** authors sometimes say “map” generically for an `f`-map, and the induced stalk map is correctly described. Adding the missing `f` is nevertheless required to prevent the phrase “map of sheaves” from asserting the wrong Hom type.

**Smallest exact replacement:**

```text
OLD: the map of sheaves of sets so constructed
NEW: the $f$-map of sheaves of sets so constructed
```

### SHEAVES-062 — ACCEPTED (number/agreement)

**Locus:** lines 4387--4390.

For each point `x`, the construction gives a stalk map, so over all points there are plural “maps on stalks.” That plural subject cannot take singular “is”; moreover, each map is a morphism, so both subject and complement should be plural.

**Adverse reading considered:** line 4380 uses singular “the map on stalks” for a schematic fixed `x`. The source changes to plural “maps” at line 4389, so singularizing the entire phrase would also work; plural agreement is the smaller local repair.

**Smallest exact replacement:**

```text
OLD: the maps on stalks is a morphism of algebraic structures.
NEW: the maps on stalks are morphisms of algebraic structures.
```

### SHEAVES-063 — ACCEPTED (three identical typographical errors)

**Loci:** lines 3982--3985, 4121--4125, and 4241--4244.

In every sentence, singular subject “The inverse functor” takes the finite passive predicate “is given.” The preposition “in” supplies no verb and yields a fragment. All three occurrences are the same mechanical error and are deduplicated under this ID.

**Adverse reading considered:** none; the cited lemma supplies the inverse and fixes the intended verb uniquely.

**Smallest exact replacement, applied three times:**

```text
OLD: The inverse functor in given
NEW: The inverse functor is given
```

### SHEAVES-064 — ACCEPTED (subject–verb agreement)

**Locus:** lines 4043--4046.

The subject is singular “The analogue,” with the intervening lemma citation inside an `of` phrase. The finite verb must therefore be third-person singular “needs.”

**Adverse reading considered:** none; the referenced lemma does not form a plural subject.

**Smallest exact replacement:**

```text
OLD: The analogue of
     Lemma \ref{lemma-extend-off-basis} need some care.
NEW: The analogue of
     Lemma \ref{lemma-extend-off-basis} needs some care.
```

### SHEAVES-065 — ACCEPTED (infinitive after “let us”)

**Locus:** lines 4349--4353.

The construction “Let us” selects a bare infinitive, “prove,” not third-person finite “proves.”

**Adverse reading considered:** none; the mathematical intent and required form are unique.

**Smallest exact replacement:**

```text
OLD: Let us first proves this
NEW: Let us first prove this
```

### SHEAVES-066 — ACCEPTED (sentence fragment)

**Locus:** lines 4434--4437.

“Similar to the above and omitted” coordinates two predicate adjectives/passives without a subject or finite copula. The preceding proof environment does not grammatically supply either. A complete sentence requires “The proof” and “is.”

**Adverse reading considered:** terse “Similar; omitted” is intelligible as proof-note shorthand. The actual source presents it as a prose sentence, where both grammatical anchors are absent.

**Smallest coherent exact replacement:**

```text
OLD: Similar to the above and omitted.
NEW: The proof is similar to the one above and is omitted.
```

### SHEAVES-067 — ACCEPTED (stalk parenthesization/type)

**Locus:** lines 4464--4468.

The intended object is the stalk at `u` of the restricted sheaf, `(j^{-1}\mathcal G)_u`. Without parentheses, `j^{-1}\mathcal G_u` conventionally forms the stalk `\mathcal G_u` first and appears to apply the inverse-image functor to a set. But `j^{-1}` takes a sheaf on `X`, not a stalk set. The two equal expressions in the same display, `(\mathcal G|_U)_u` and `\mathcal G_u`, confirm the intended grouping.

**Adverse reading considered:** expert precedence can recover the intended stalk from the sentence “identification of stalks.” The standard competing parse is ill-typed, so parentheses are warranted.

**Smallest exact replacement:**

```text
OLD: $j^{-1}\mathcal{G}_u$
NEW: $(j^{-1}\mathcal{G})_u$
```

### SHEAVES-068 — ACCEPTED (base-space preposition; six linked occurrences)

**Loci:** lines 4469--4470, 4577--4578, and 4715--4718.

Presheaves and sheaves are defined **on** a topological space; “of” introduces the kind of values, as in “sheaves of abelian groups on `U`.” Thus “presheaves of `U`” and “sheaves of `U`” wrongly make the space look like the value type. The error occurs twice at each of the three cited loci, including the two abelian variants, for six total occurrences under one ID.

**Adverse reading considered:** the categories in the surrounding formulas reveal that `U` is the base. That makes the intended preposition recoverable but does not license “of.”

**Smallest exact replacement, at all six occurrences:**

```text
OLD: presheaves of $U$
NEW: presheaves on $U$

OLD: sheaves of $U$
NEW: sheaves on $U$
```

The same substitutions apply when “abelian” precedes “presheaves” or “sheaves.”

### SHEAVES-069 — ACCEPTED (missing definite article)

**Locus:** lines 4477--4479.

The relative phrase “of all `W` ...” identifies a particular collection, so singular count noun “collection” requires the definite article: “the collection.”

**Adverse reading considered:** mathematical prose can use bare plurals (“over open subsets”), but not the bare singular count noun used here.

**Smallest exact replacement:**

```text
OLD: is over collection of all $W \subset X$ open
NEW: is over the collection of all $W \subset X$ open
```

### SHEAVES-070 — ACCEPTED (substantive presheaf/sheaf functor mismatch)

**Locus:** lines 4486--4487.

Part (4) asserts `j_pj_*=\mathrm{id}` on presheaves, while part (5) asserts `j^{-1}j_*=\mathrm{id}` on sheaves. The proof writes only
`j^{-1}j_*\mathcal F(V)=...`, which is a sheaf calculation and cannot establish the statement involving presheaf inverse image `j_p`. The presheaf result is true by part (1): for `V\subset U`,
`j_pj_*\mathcal F(V)=j_*\mathcal F(V)=\mathcal F(V)`. The sheaf result uses the parallel calculation with `j^{-1}`.

**Adverse reading considered:** for an open immersion the two inverse-image constructions have identical section values after sheafification, so one computation suggests both. They remain different functors on different categories, and the proof must name the presheaf functor to type part (4).

**Smallest coherent exact replacement:**

```text
OLD: Parts (4) and (5) follow by computing
     $j^{-1}j_*\mathcal{F}(V) = j_*\mathcal{F}(V) = \mathcal{F}(V)$.
NEW: Part (4) follows by computing
     $j_pj_*\mathcal{F}(V) = j_*\mathcal{F}(V) = \mathcal{F}(V)$,
     and part (5) follows from the same computation with $j^{-1}$.
```

### SHEAVES-071 — ACCEPTED (nonparallel sheaf-kind list)

**Locus:** lines 4501--4505.

In item (2), “a sheaf of sets on `X`, abelian groups or algebraic structures on `X`” places the base modifier inside the first coordinated value kind and repeats it only after the last. On a literal parse, “abelian groups” is coordinated directly with the entire noun phrase “a sheaf of sets on `X`,” rather than with “sets.” Moving the single base modifier after all three value kinds restores parallel typing. Item (1) already has `on X` after the full list and needs no substantive change beyond optional serial punctuation.

**Adverse reading considered:** ordinary ellipsis lets a reader supply “sheaf of” before the latter cases. The misplaced first `on X` still breaks the coordination and creates a real attachment ambiguity.

**Smallest exact replacement:**

```text
OLD: Let $\mathcal{G}$ be a sheaf of sets on $X$, abelian groups or
     algebraic structures on $X$.
NEW: Let $\mathcal{G}$ be a sheaf of sets, abelian groups, or
     algebraic structures on $X$.
```

### SHEAVES-072 — REJECTED (register preference, not an error)

**Locus:** lines 4518--4520.

“Ok, so” is grammatical conversational English and correctly connects the omitted definition to the next topic. The authority elsewhere deliberately uses an informal expository voice (“Think about it!”, “Now, doesn't it seem ...?”, and direct addresses to the reader). Replacing it with “Thus” would change register, not grammar, type, or mathematical content.

**Adverse evidence recorded:** “Ok, so” may be undesirable in a more formal house style, and “Thus” would be more compact. No formal-style rule is stated in this file or intake, so the preference does not establish an erratum. **No replacement warranted.**

### SHEAVES-073 — ACCEPTED (stalk parenthesization/type; five occurrences)

**Loci:** lines 4566--4570, 4705--4708, 4749--4752, 4796--4799, and 4905--4908.

Each statement describes the stalk of the extension sheaf `j_!\mathcal F`, whose typed expression is `(j_!\mathcal F)_x`. Bare `j_!\mathcal F_x` conventionally binds the stalk subscript to `\mathcal F` first, appearing to apply `j_!` to a stalk object. But `j_!` takes a sheaf on `U`, while `\mathcal F_x` is a set, group, algebraic object, or module and is undefined when the case assumes `x\notin U`. All five formulas therefore need the same grouping correction.

**Adverse reading considered:** prose and operator precedence may let an expert infer the stalk of the pushforward/extension. The alternative visible parse is untypeable, so this is not merely cosmetic.

**Smallest exact replacement, applied five times:**

```text
OLD: $j_{!}\mathcal{F}_x$
NEW: $(j_{!}\mathcal{F})_x$
```

### SHEAVES-074 — ACCEPTED (presheaf/sheaf object-kind conflation)

**Locus:** lines 4594--4595.

Statement (4) is about the presheaf `j_{p!}\mathcal F`, while statement (5) is about the sheaf `j_!\mathcal F`. Referring to the object in both calculations as “the sheaf” is false in the presheaf case; `j_{p!}\mathcal F` need not be a sheaf and is precisely sheafified to define `j_!\mathcal F` at lines 4542--4544.

**Adverse reading considered:** both have the same section formula on opens contained in `U`, so the proof idea is correct. The generic noun must cover both object kinds.

**Smallest exact replacement:**

```text
OLD: value of the sheaf on any open of $U$.
NEW: value of the relevant (pre)sheaf on any open of $U$.
```

### SHEAVES-075 — ACCEPTED (typographical adjective)

**Locus:** lines 4648--4651.

The past participle “given” modifies “type,” referring to the type fixed by `(\mathcal C,F)`. Bare verb “give” cannot occupy that attributive position.

**Adverse reading considered:** none; one letter sequence uniquely restores the intended adjective.

**Smallest exact replacement:**

```text
OLD: (of the give type)
NEW: (of the given type)
```

### SHEAVES-076 — ACCEPTED (semantic labels incorrectly typeset as variables)

**Locus:** lines 4673--4676.

In TeX math mode, bare `rings` and `abelian` in subscripts are sequences/products of italic variable letters, not textual labels distinguishing two extension functors. The prose explicitly contrasts the categories of rings and abelian groups, so the subscripts are semantic words and must be set upright as text/roman material.

**Adverse reading considered:** readers can visually infer the labels despite italic variable spacing. That does not make the expressions semantically well-formed mathematical subscripts.

**Smallest exact replacement:**

```text
OLD: $j_{!, rings}\mathcal{O} \not = j_{!, abelian}\mathcal{O}$
NEW: $j_{!, \mathrm{rings}}\mathcal{O} \not = j_{!, \mathrm{abelian}}\mathcal{O}$
```

### SHEAVES-077 — ACCEPTED (number in established object-kind phrase)

**Locus:** lines 4731--4734.

Each section is one algebraic structure, but the sheaf’s varying objects are conventionally described as “(pre)sheaves of algebraic structures.” The file uses that plural phrase immediately at lines 4681--4682 and throughout the definitions and lemma statements. Singular “of algebraic structure” is not the established count construction.

**Adverse reading considered:** the separately defined phrase “a type of algebraic structure” correctly uses singular, but here the head is `(pre)sheaves of`, not “type of.”

**Smallest exact replacement:**

```text
OLD: (pre)sheaves of algebraic structure
NEW: (pre)sheaves of algebraic structures
```

### SHEAVES-078 — ACCEPTED (substantive module-ring mismatch)

**Locus:** lines 4773--4806, erroneous phrase at line 4794.

The ring sheaf `\mathcal O` is on `X`. On the open subspace `U`, the acting ring is its restriction `\mathcal O|_U`, as the open subspace notation at lines 4772--4774, both Hom categories at lines 4781--4792, the defining module case at lines 4661--4666, and part (4) at line 4806 all state. Therefore a sheaf on `U` cannot literally be a sheaf of `\mathcal O`-modules unless an unstated convention silently restricts the ring. The typed hypothesis is `\mathcal O|_U`-module.

**Adverse reading considered:** authors sometimes suppress restriction bars when the base open is clear. This file does not do so in the surrounding statements and repeatedly writes `\mathcal O|_U`; the lone omission conflicts with the lemma’s own categories.

**Smallest exact replacement:**

```text
OLD: Let $\mathcal{F}$ be a sheaf of $\mathcal{O}$-modules on $U$.
NEW: Let $\mathcal{F}$ be a sheaf of $\mathcal{O}|_U$-modules on $U$.
```

### SHEAVES-079 — ACCEPTED (wrong part of speech)

**Locus:** lines 4835--4838.

“Faithfulness” is a noun, and the nominal property corresponding to “fully faithful” is “full faithfulness.” Adverb “fully” cannot directly modify that noun. The lemma’s preceding predicate “is fully faithful” is correct because there it modifies the adjective “faithful.”

**Adverse reading considered:** none; the adjectival and nominal constructions determine the two forms.

**Smallest exact replacement:**

```text
OLD: Fully faithfulness
NEW: Full faithfulness
```

### SHEAVES-080 — ACCEPTED (two subject–verb commas)

**Loci:** lines 4599--4601 and 4605--4606.

In the first sentence the full subject is `j_!\mathcal F as defined above` and its verb is “is”; in the second the full subject is “The reason for choosing the empty set in the definition of the extension by the empty set” and its verb is again “is.” Neither subject can be separated from its predicate by a comma. The intervening modifiers are restrictive/integral and do not form parentheticals requiring paired commas.

**Adverse reading considered:** both subjects are long enough to invite a spoken pause. Length does not license the single grammatical comma.

**Smallest exact replacements:**

```text
OLD: $j_!\mathcal{F}$ as defined above, is not a sheaf
NEW: $j_!\mathcal{F}$ as defined above is not a sheaf

OLD: extension by the empty set, is that it is the initial object
NEW: extension by the empty set is that it is the initial object
```

## No-mutation and no-contact boundary

This receipt is append-only evidence. No byte of `sheaves.tex`, the intake, either bound note, any translation, any R3 artifact, or any other project/control file was edited. No overlay admission was made, no Git operation was run, and no upstream contact, issue, or pull request was initiated. The only filesystem mutation for this bounded review is creation of this requested private receipt.
