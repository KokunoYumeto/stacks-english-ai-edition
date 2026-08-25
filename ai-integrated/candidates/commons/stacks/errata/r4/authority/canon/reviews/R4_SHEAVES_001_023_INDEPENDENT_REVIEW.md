# R4 independent review: `sheaves.tex`, SHEAVES-001--SHEAVES-023

Date of review: 2026-08-22 (Europe/Berlin)

## Authority and scope

This review concerns only the following frozen English authority:

- repository identity: `stacks/stacks-project`
- commit identity supplied by the frozen authority/intakes: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- file: `sheaves.tex`
- exact local path: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sheaves.tex`
- recomputed byte count: `184841`
- recomputed SHA-256: `AC4F9EDC7DB85E66329806EC9EA42816187A469772844BAEA663E1C9A9F00B38`

The byte count and digest agree with all four intake records. No Git operation was used. Review was confined to the cited loci and the definitions, examples, and lemmas in this same authority file needed to type-check or prove the claims.

## Frozen intake identities

All identities below were recomputed from the exact local files, not copied as unverified metadata.

| Intake | Bytes | SHA-256 | IDs |
|---|---:|---|---|
| `ERRATA_R4_SUPPLEMENT_SHEAVES_20260822.json` | 2914 | `E576BE04353FF5557C8590A1280B3D87FF4714F4A8FEE4D7E91E5A0C3FBCA5B0` | 001--002 |
| `ERRATA_R4_SUPPLEMENT_SHEAVES_003_007_20260822.json` | 4137 | `E6A7DA4D6B37B04B0D14599133ABE0B31D7945338250EE4D6DA76BFCA48BF8F2` | 003--007 |
| `ERRATA_R4_SUPPLEMENT_SHEAVES_008_014_20260822.json` | 5447 | `DF88F9BAE47BC119A628D0A105144B9DA3BCC23062050216A9B107A8874B2C2E` | 008--014 |
| `ERRATA_R4_SUPPLEMENT_SHEAVES_015_023_20260822.json` | 6156 | `70FAA1CD6109166FD25B4A8C4D35E8A60A2D44E32AD2ECE7FC60457DC98D3160` | 015--023 |

## Disposition summary

“Accepted” means that the frozen source contains an objective mathematical, typing, grammatical, or typographical defect at the cited locus. “Rejected” means that the proposed change would be optional stylistic expansion or would erase defensible intentional notation. “Deferred” is reserved for a claim not decidable from this file; none is deferred.

| Disposition | Count | IDs |
|---|---:|---|
| Accepted | 18 | 002--014, 016--020 |
| Rejected | 5 | 001, 015, 021--023 |
| Deferred | 0 | none |

The two occurrences in SHEAVES-020 are one repeated-error finding, not two hypotheses. The missing article and agreement error in the single clause of SHEAVES-018 are treated together. SHEAVES-009 and SHEAVES-010 remain separate because one concerns object/transition data and the other morphism/component data.

## Per-hypothesis review

### SHEAVES-001 — REJECTED (intentional, type-resolved notation)

**Locus:** lines 92--94.

Definition `definition-presheaf`, lines 77--83, introduces restriction maps generically as `\rho^U_V`. In the naturality square the left vertical arrow has type
`\mathcal F(U) \to \mathcal F(V)` and the right vertical arrow has type
`\mathcal G(U) \to \mathcal G(V)`. Their domains and codomains uniquely identify the restriction belonging to each presheaf. The repeated label therefore does not assert equality of two maps (which usually do not even have the same source and target); it is conventional overloading of the generic restriction notation.

**Adverse evidence considered:** subscripts such as `\rho^{\mathcal F,U}_V` and `\rho^{\mathcal G,U}_V` could make the square more explicit. That is an optional readability change, not a forced correction. **No replacement warranted.**

### SHEAVES-002 — ACCEPTED (typing/prose defect)

**Locus:** lines 192--195.

The displayed group datum explicitly types `- : A \to A` but types `0\in A`. Thus negation is a map and zero is an element. In “the zero and the negation maps,” the shared plural head “maps” grammatically classifies both coordinated items as maps, contradicting the displayed type of `0`.

**Adverse evidence considered:** an element can be encoded by a map from a singleton, as lines 206--216 later do for a zero section. No such encoding is made in line 192; the source instead explicitly writes `0\in A`. The implicit-encoding defence therefore does not cure this sentence.

**Smallest exact replacement:**

```text
OLD: then the zero and the negation maps are
NEW: then the zero element and the negation map are
```

### SHEAVES-003 — ACCEPTED (grammar)

**Locus:** lines 1542--1546.

“Function” is a singular count noun. After “the presheaf of” it needs a determiner if singular, while the intended object contains all continuous functions and therefore takes the ordinary plural. Example `example-basic-continuous-maps`, lines 553--561, confirms that the presheaf assigns a set of continuous maps/functions, not one distinguished function.

**Adverse evidence considered:** “function” can be a noun adjunct in compounds such as “function sheaf,” but it is not a noun adjunct after the preposition “of.”

**Smallest exact replacement:**

```text
OLD: presheaf of continuous function
NEW: presheaf of continuous functions
```

### SHEAVES-004 — ACCEPTED (subject–verb agreement)

**Locus:** lines 1747--1753.

The grammatical subject is the singular citation “Lemma `\ref{lemma-diagram-fibre-product}`”; the finite verb must consequently be third-person singular “shows.” The intervening citation does not change the subject’s number.

**Adverse evidence considered:** none; “show” cannot agree with the singular subject here.

**Smallest exact replacement:**

```text
OLD: Lemma \ref{lemma-diagram-fibre-product} show that
NEW: Lemma \ref{lemma-diagram-fibre-product} shows that
```

### SHEAVES-005 — ACCEPTED (missing article)

**Locus:** lines 1765--1769.

In “is morphism of presheaves,” “morphism” is a singular count noun used predicatively and requires a determiner. The displayed `\psi` denotes one morphism, so “a” is the required article.

**Adverse evidence considered:** mathematical headings can use telegraphic noun phrases, but this is running prose after “is,” where the bare singular is not grammatical.

**Smallest exact replacement:**

```text
OLD: is morphism of presheaves
NEW: is a morphism of presheaves
```

### SHEAVES-006 — ACCEPTED (article and mathematical-prose clarification)

**Locus:** lines 1847--1854.

There is a canonical ring-presheaf map `\mathcal O \to \mathcal O^\#`. If `\mathcal G` is an `\mathcal O^\#`-module, its `\mathcal O`-action is the composite
`\mathcal O\times\mathcal G \to \mathcal O^\#\times\mathcal G \to \mathcal G`. This is exactly the restriction construction described for a ring-presheaf map in lines 432--452. Hence the factorization’s target is `\mathcal G` *viewed as* an `\mathcal O`-module by restriction of scalars. The source’s “to a `\mathcal O`-module” both uses the wrong article before the vowel sound “O” and names the result imprecisely instead of the scalar restriction.

**Adverse evidence considered:** the surrounding types make the intended module structure recoverable, so the universal property itself is not wrong. A wording correction is nevertheless warranted and does not alter that property.

**Smallest exact replacement that fixes both defects:**

```text
OLD: (into the restriction of $\mathcal{G}$ to a $\mathcal{O}$-module)
NEW: (where $\mathcal{G}$ is viewed as an $\mathcal{O}$-module by restriction of scalars)
```

### SHEAVES-007 — ACCEPTED (missing preposition)

**Locus:** lines 1949--1953.

The established construction is “a sheaf **of** `\mathcal O`-modules” (compare lines 864--876 and 1884--1887). Without “of,” the noun phrase has no grammatical relation between “sheaf” and “modules.”

**Adverse evidence considered:** “module sheaf” would be a possible compound, but that is not the word order used here.

**Smallest exact replacement:**

```text
OLD: a sheaf $\mathcal{O}$-modules
NEW: a sheaf of $\mathcal{O}$-modules
```

### SHEAVES-008 — ACCEPTED (agreement and number)

**Locus:** lines 320--327.

For each fixed inclusion `V\subset U`, line 321 supplies one map `\rho^U_V`, and line 326 identifies it with one image `F(\alpha^U_V)`. The plural subject “restriction mappings” cannot agree with singular “is”; moreover, the indexed symbol and singular right-hand side show that the intended subject is one mapping for the chosen pair.

**Adverse evidence considered:** a collective assertion about all restriction mappings could use “are the images,” but that would also require pluralizing the right-hand formulation. The local sentence instead fixes `U,V` and one `\alpha^U_V`.

**Smallest exact replacement:**

```text
OLD: the restriction mappings $\rho^U_V$ is the image
NEW: the restriction mapping $\rho^U_V$ is the image
```

### SHEAVES-009 — ACCEPTED (substantive definition gap)

**Locus:** lines 339--350.

The composition axiom does not imply identity preservation. A concrete counterexample lies in `\mathcal C=\mathit{Sets}`: choose a two-element set `A` and the nonidentity idempotent `e:A\to A` that is constant at one element. Assign `\mathcal F(U)=A` to every open `U` and assign `\rho^U_V=e` to every inclusion, including equal inclusions. Every required composition holds because `e\circ e=e`, but `\rho^U_U=e\ne\mathrm{id}_A`. Thus the displayed data satisfy lines 344--350 as written and are not a contravariant functor/presheaf.

Definition `definition-presheaf` for sets explicitly includes `\rho^U_U=\mathrm{id}` at lines 77--83. Faithfulness in the preceding discussion cannot repair the general definition, which no longer assumes a faithful functor.

**Adverse evidence considered:** “presheaf” is often defined beforehand as a contravariant functor, in which case identities are built in. Here, however, the numbered item purports to give the data and axioms directly (“is given by a rule ... such that”), so the unstated functor axiom cannot be imported without making the definition circular.

**Smallest exact replacement:**

```text
OLD: in $\mathcal{C}$ such that whenever $W \subset V \subset U$
NEW: in $\mathcal{C}$ such that $\rho_U^U = \text{id}_{\mathcal{F}(U)}$ for every open $U \subset X$, and whenever $W \subset V \subset U$
```

### SHEAVES-010 — ACCEPTED (substantive morphism-data and wording defect)

**Locus:** lines 351--354.

A natural transformation between presheaves requires a component `\varphi_U` for every open `U`, with the restriction squares commuting. The source provides one unindexed morphism at a free, unquantified `U`. On a space with two distinct opens, specifying a component at only one open plainly does not determine the component at the other; even after choosing both independently, compatibility is an additional condition. Therefore the stated datum is insufficient as written.

This differs from lines 84--87: there a “rule” explicitly assigns a map to **each** open `U`, even though the component label is typographically unindexed. Also, the established English construction is “presheaves with values in `\mathcal C`,” not singular “with value.”

**Adverse evidence considered:** suppressing the subscript on components is common after a family has been quantified. It cannot supply the missing family quantifier in this sentence.

**Smallest coherent exact replacement:**

```text
OLD: \item A {\it morphism $\varphi : \mathcal{F} \to \mathcal{G}$
     of presheaves with value in $\mathcal{C}$} is given by a
     morphism $\varphi : \mathcal{F}(U) \to \mathcal{G}(U)$
     in $\mathcal{C}$ compatible with restriction morphisms.
NEW: \item A {\it morphism $\varphi : \mathcal{F} \to \mathcal{G}$
     of presheaves with values in $\mathcal{C}$} is given by
     morphisms $\varphi_U : \mathcal{F}(U) \to \mathcal{G}(U)$
     in $\mathcal{C}$, one for every open $U \subset X$, compatible with
     restriction morphisms.
```

### SHEAVES-011 — ACCEPTED (duplicated word)

**Locus:** lines 402--410.

“Defines the structure of an ... module structure” gives “structure” the same syntactic role twice. Deleting the second occurrence leaves the standard and mathematically identical phrase “the structure of an `\mathcal O(U)`-module on the abelian group.”

**Adverse evidence considered:** the sentence remains understandable, but recoverability does not make the lexical duplication grammatical.

**Smallest exact replacement:**

```text
OLD: defines the structure of an $\mathcal{O}(U)$-module
     structure on the abelian group $\mathcal{F}(U)$.
NEW: defines the structure of an $\mathcal{O}(U)$-module
     on the abelian group $\mathcal{F}(U)$.
```

### SHEAVES-012 — ACCEPTED (missing grammatical relation)

**Locus:** lines 596--604.

“Open set” is a singular count-noun phrase. In “For `U\subset X` open set” it has neither a determiner nor a copula/appositive marker. Postpositive mathematical shorthand such as “for `U` open” does not license adding the bare count noun “set.”

**Adverse evidence considered:** compressed postpositive “open” occurs elsewhere in the file and is conventional. The objective defect here is the unattached bare singular “open set,” not merely the position of “open.”

**Smallest exact replacement:**

```text
OLD: For $U \subset X$ open set
NEW: For every open $U \subset X$
```

### SHEAVES-013 — ACCEPTED (number)

**Locus:** lines 871--876.

`\Hom_\mathcal O(\mathcal F,\mathcal G)` contains all morphisms of the indicated kind. After “the set of,” the count noun denoting its variable members must be plural: “morphisms.”

**Adverse evidence considered:** “morphism” can modify another noun in a compound, but here it is the object of the preposition “of,” not a noun adjunct.

**Smallest exact replacement:**

```text
OLD: the set of morphism of sheaves
NEW: the set of morphisms of sheaves
```

### SHEAVES-014 — ACCEPTED (substantive object misclassification)

**Locus:** lines 1106--1127.

The lemma assumes only a presheaf with values in `\mathcal C`. Definition `definition-underlying-presheaf-sets`, lines 359--365, names `U\mapsto F(\mathcal F(U))` its “underlying presheaf of sets,” and the lemma itself uses that exact term at lines 1112--1113. There is no sheafification or sheaf hypothesis before line 1127.

The distinction is real, not terminological. Take `\mathcal C=\mathit{Sets}`, `F=\mathrm{id}`, and the constant presheaf of Definition `definition-constant-presheaf` with a two-element value. It meets the lemma’s categorical hypotheses, but its value on the empty open is two-element; by Remark `remark-confusion`, lines 527--542, a sheaf’s value there must be a singleton. Hence an allowed underlying presheaf need not be a sheaf, providing a direct counterexample to the noun at line 1127.

**Adverse evidence considered:** the maps into the stalk are still well-defined and the intended object is recoverable. That makes the error local wording, but it does not make “sheaf” true.

**Smallest exact replacement:**

```text
OLD: the corresponding maps for the underlying sheaf of sets.
NEW: the corresponding maps for the underlying presheaf of sets.
```

### SHEAVES-015 — REJECTED (conventional categorical shorthand)

**Locus:** lines 2058--2064.

Strictly, a representing object for the displayed Hom functor is determined up to a unique isomorphism compatible with the representing bijection, not as a literally unique object. This follows from Yoneda: if `P` and `P'` both represent the functor, the two representing natural isomorphisms give a unique isomorphism `P\cong P'`. Unequal but isomorphic copies show why literal equality would be too strong.

That strict observation does not force a source correction here. In ordinary categorical prose, “determines ... uniquely” is standard shorthand for this representability uniqueness. The file itself spells out the longer form when it matters—“adjoint functors are unique up to unique isomorphism” at lines 2217--2220—and the subsequent lemma constructs a representative rather than relying on equality of objects. No downstream assertion confuses equality with canonical isomorphism.

**Adverse evidence recorded:** expanding the phrase to “uniquely up to unique isomorphism” would be formally more explicit, but it is an optional clarification, not an erratum. **No replacement warranted.**

### SHEAVES-016 — ACCEPTED (missing quantifier/type binder)

**Locus:** lines 2100--2105.

In the construction immediately before this paragraph, `U` denotes an open subset of `X` (lines 2073--2090). At line 2101, however, `\mathcal G(U)` is defined only when `U` is open in `Y`. The new paragraph silently switches the universe of `U` without binding it. Once `U\subset Y` is declared open, `f(f^{-1}U)\subset U` proves that `U` occurs in the neighbourhood system and yields the stated canonical component. Thus the mathematics is correct but the component’s parameter is formally missing.

**Adverse evidence considered:** readers can infer the type of `U` from `\mathcal G(U)` and the next sentence. Inference recovers the intent but does not quantify the free symbol, especially after the preceding use of `U\subset X`.

**Smallest exact replacement:**

```text
OLD: A small useful remark is that there exists
     a canonical map $\mathcal{G}(U) \to f_p\mathcal{G}(f^{-1}(U))$,
NEW: A small useful remark is that for every open $U \subset Y$ there exists
     a canonical map $\mathcal{G}(U) \to f_p\mathcal{G}(f^{-1}(U))$,
```

### SHEAVES-017 — ACCEPTED (missing copula)

**Locus:** lines 2116--2120.

In the directive “let `U\subset X` open,” “open” is the predicate adjective describing `U`; after “let” that predicate requires the infinitive copula “be.” This is distinct from a parenthetical range such as “for `U` open,” where an elliptical postpositive modifier is conventional.

**Adverse evidence considered:** the intended condition is obvious and compressed open-set ranges occur in the file. The finite construction “let ... open” is nevertheless missing its required copula.

**Smallest exact replacement:**

```text
OLD: Namely, let $U \subset X$ open.
NEW: Namely, let $U \subset X$ be open.
```

### SHEAVES-018 — ACCEPTED (missing article plus linked agreement error)

**Locus:** lines 2264--2273.

“Family” is a singular count noun and therefore cannot occur as bare singular in “if and only if corresponding family.” Because the adjective “corresponding” selects the family just extracted from `a`, the definite article “the” is appropriate. The same noun phrase is the subject of “satisfy,” so its singular head additionally requires “satisfies.” These are one co-located grammatical finding, not two queue items.

**Adverse evidence considered:** the members `a_V` are plural, but in the written construction they occur inside the prepositional phrase “of maps”; agreement is controlled by the head “family.” An alternative would be “the corresponding maps `a_V` satisfy,” but that is not a smaller repair of the existing syntax.

**Smallest exact replacement:**

```text
OLD: if and only if corresponding family of maps $a_V$
     satisfy the condition
NEW: if and only if the corresponding family of maps $a_V$
     satisfies the condition
```

### SHEAVES-019 — ACCEPTED (typographical error)

**Locus:** lines 2298--2305.

The map `\mathcal F(f^{-1}V)\to\mathcal F(U)` is a presheaf restriction map because `U\subset f^{-1}V`, as the next line explicitly proves. “Restruction” is not the applicable English word and is a one-letter transposition/substitution error.

**Adverse evidence considered:** none; the type and the explanation uniquely force “restriction.”

**Smallest exact replacement:**

```text
OLD: restruction map
NEW: restriction map
```

### SHEAVES-020 — ACCEPTED (article; two deduplicated occurrences)

**Loci:** lines 2320 and 2380.

The indefinite article is selected by pronunciation. The symbol `g` is read “gee,” beginning with a consonant sound, so the phrase is “a `g`-map,” just as line 2319 correctly has “an `f`-map” because “eff” begins with a vowel sound. The identical error occurs once in the definition and once in the later lemma; both are covered by this one ID.

**Adverse evidence considered:** the visual glyph is irrelevant to article choice; English articles follow the spoken form.

**Smallest exact replacement, applied at both cited occurrences:**

```text
OLD: an $g$-map
NEW: a $g$-map
```

### SHEAVES-021 — REJECTED (plural is semantically justified)

**Locus:** lines 2321--2332.

Definition `definition-f-map`, lines 2228--2240, makes an `f`-map a collection of components indexed by every open subset. Accordingly, the displayed triangle at lines 2324--2332 is a schematic diagram with one instance for each open `W\subset Z`. “The diagrams” refers to this indexed family, not to the number of `xymatrix` environments printed on the page.

**Adverse evidence considered:** singular “the diagram” could refer to the displayed template, but it would be an equally possible stylistic viewpoint and is not more mathematically correct. **No replacement warranted.**

### SHEAVES-022 — REJECTED (awkward but correctly typed quotient language)

**Locus:** lines 2353--2360.

The stalk construction at lines 914--929 is explicitly a quotient of pairs `(U,s)` and calls the resulting class the “image of `s` in `\mathcal F_x`.” Thus “the image of a representative `(V,s)`” can denote the equivalence class of that representative in `\mathcal G_{f(x)}`. That class, not the raw pair, is in the domain of `\varphi_x`, and it is mapped to the class represented by `(f^{-1}V,\varphi_V(s))`. The following sentence’s well-definedness check is exactly what is required for independence of representatives.

**Adverse evidence recorded:** “the element represented by `(V,s)` is mapped to ...” would be smoother and would avoid the repeated passive. The existing sentence nevertheless distinguishes representative from quotient image and has a coherent, correct type; awkwardness alone does not establish an erratum. **No replacement warranted.**

### SHEAVES-023 — REJECTED (the quantifier is present in conventional range notation)

**Locus:** lines 2361--2371.

The sentence says “all diagrams” and then gives the parenthetical range `(for f(x) \in V \subset Y open)`. In the file’s established postpositive shorthand, this means all open subsets `V\subset Y` containing `f(x)`; compare “for all `V'\subset V\subset Y` open” at line 2240. Since `f(x)\in V`, each such `V` is precisely an open neighbourhood of `f(x)`. There is no missing mathematical quantifier or missing diagram family.

**Adverse evidence recorded:** “for every open `V\subset Y` containing `f(x)`” is more idiomatic full prose and less visually compressed. It is an optional copyedit, not a forced correction. **No replacement warranted.**

## Mutation and contact boundary

This review is evidentiary only. No byte of the frozen `sheaves.tex` authority, any translation, any intake JSON, or any other project artifact was changed. No overlay admission was made, no Git operation was run, and no upstream Stacks contact, issue, or pull request was initiated. The only filesystem mutation made for this review is the creation of this review file at its requested private-control path.
