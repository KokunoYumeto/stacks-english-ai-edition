# Stacks errata R3 proof dossier

Authority commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`.

Authority files:

- `sets.tex`, 46,628 bytes, SHA-256
  `9BCC55E7F11CF36B0665AE549D5BA76BE6A0EDD00F7FCA36A567E367099603F9`;
- `topology.tex`, 237,731 bytes, SHA-256
  `C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872`;
- `categories.tex`, 350,957 bytes, SHA-256
  `62F7611AF4C3FEEBD041DB4728B42C7112004CFBB9FA5ECB643C6F5D90DB3F25`.

The French ledger was treated only as a locator. Every locus below was reopened
against these exact bytes and checked against its local declarations and
dependent proof. The six latest topology items also received the independent
bounded review recorded in `R3_TOPOLOGY_018_023_INDEPENDENT_REVIEW.md`.
Canonical translations remain byte-faithful to the frozen source; corrections
belong only in the English AI Edition overlay.

## Sets

### `MC-STK-ERR-0029` — `SETS-001`

Lines 986--988 define only `\mathcal{S}_\tau`. The supremum at line 993 ranges
over undeclared bare `S_\tau`; no competing bare symbol exists. This is a
mechanically certain identifier loss.

Smallest correction: `T \in S_\tau` -> `T \in \mathcal{S}_\tau`.

### `MC-STK-ERR-0030` — `SETS-002`

Lines 1073--1076 define `\beta(\mathcal U)` for the covering under discussion.
The base-change step at line 1088 instead uses a free `\beta`. The first replay
review exposed a linked defect in clause (3): as printed, that clause accepts a
cover in `Cov_{\kappa,\gamma}`, whereas the definition of `\beta(\mathcal U)`
only places `\mathcal U` in `Cov_{\kappa,f(\beta(\mathcal U))}`. Applying the
printed clause at `\gamma=f(\beta(\mathcal U))` would land at
`f(f(\beta(\mathcal U))+1)`, for which no bound below `f(\beta_2)` was proved.
Clause (2) immediately above already uses the coherent recursive-stage input
`Cov_{\kappa,f(\gamma)}`. Changing clause (3) to the same input makes it apply
at `\gamma=\beta(\mathcal U)`. Since `\beta_2` is a limit ordinal and
`\beta(\mathcal U)<\beta_2`, one has `\beta(\mathcal U)+1<\beta_2`, hence
`f(\beta(\mathcal U)+1)\leq f(\beta_2)=\alpha`.

Linked smallest correction: in recursive clause (3), replace
`Cov_{\kappa,\gamma}` by `Cov_{\kappa,f(\gamma)}`; at the application, replace
the free `f(\beta+1)` by `f(\beta(\mathcal U)+1)`.

### `MC-STK-ERR-0031` — `SETS-003`

The proof fixes `\alpha=f(\beta_2)` at lines 1058--1059 and then proves the
site axioms for `Cov_{\kappa,\alpha}`. Lines 1093 and 1096 wrongly assume the
two input coverings lie in the generally larger `Cov_{\kappa,f(\alpha)}`.
Moreover, cofinality of `\beta_2` bounds the image of
`i\mapsto\beta(\mathcal W_i)` below some `\beta<\beta_2`; it supplies no bound
below `\beta_1`. The recursive composition clause requires the outer cover
`\mathcal U` at the same `f(\beta)` stage as every `\mathcal W_i`. Because
`\beta(\mathcal U)<\beta_2`, increasing the bound to at least
`\beta(\mathcal U)` retains `\beta<\beta_2` and, by monotonicity, retains all
the inner-cover memberships. With this common `\beta<\beta_2`, monotonicity gives
`f(\beta+1)\leq f(\beta_2)=\alpha`, exactly the final inclusion used at line
1104.

Linked smallest corrections: replace both occurrences of
`Cov_{\kappa,f(\alpha)}` by `Cov_{\kappa,\alpha}`, and replace
`\beta<\beta_1` by `\beta<\beta_2`; then explicitly increase `\beta`, if
necessary, so that `\mathcal U\in Cov_{\kappa,f(\beta)}` as well.

### `MC-STK-ERR-0032` — `SETS-004`

Lines 843--846 define `W_{a,i}` and prove its size bound. The coproduct at line
848 alone transposes the indices to undeclared `W_{i,a}`.

Smallest correction: `W_{i,a}` -> `W_{a,i}`.

## Topology

### `MC-STK-ERR-0033` — `TOPOLOGY-001`

The graph at lines 1230--1232 declares vertex set `V`; no edge set `E` is
declared. Distance is a relation on vertices, so the diameter endpoints at line
1235 must lie in `V`. If an endpoint of a diameter were a cut vertex, a vertex
in a component away from the other endpoint would produce a longer path, so
the graph argument remains valid.

Smallest correction: `j,j'\in E` -> `j,j'\in V`.

### `MC-STK-ERR-0034` — `TOPOLOGY-002`

`A` is a set whose elements are closed subsets. The formula at lines
1276--1277 orders undeclared indices `\alpha,\alpha'` through undeclared
`Z_\alpha`; the next sentence directly chooses an element `Z\in A`.

Smallest explicit correction: replace the displayed order clause by
`Z\leq Z' \Leftrightarrow Z\subset Z'` for `Z,Z'\in A`.

### `MC-STK-ERR-0035` — `TOPOLOGY-003`

The diagram is indexed by the category `\mathcal I`, not by a set `I`.
The proof at lines 2405--2408 constructs a map into `\Ob(\mathcal I)` and sets
`J` equal to its image.

Smallest correction: `J\subset I` -> `J\subset\Ob(\mathcal I)`.

### `MC-STK-ERR-0036` — `TOPOLOGY-004`

The compact closed set needed at lines 1882--1885 is the complement of the
open union `U\cup V`. Under the ungrouped reading `(X\setminus U)\cup V`, the
set need not be closed and contains `C\subset V`, contradicting the asserted
empty intersection with `S=B\amalg C`.

Smallest linked correction: in both occurrences, write
`X\setminus(U\cup V)`.

### `MC-STK-ERR-0037` — `TOPOLOGY-005`

The intended descending closed chain is
`X\setminus U_{i_1} \supset X\setminus(U_{i_1}\cup U_{i_2})\supset\cdots`.
The printed `(X\setminus U_{i_1})\cup U_{i_2}` is neither forced closed nor a
subset of the preceding term.

Smallest correction: group the union inside the complement.

### `MC-STK-ERR-0038` — `TOPOLOGY-006`

The set-builder defining `U_K` at line 3124 closes with `})`, although only the
brace is opened. This is a mechanically certain unmatched delimiter.

Smallest correction: delete the final `)`.

### `MC-STK-ERR-0039` — `TOPOLOGY-007`

The hypothesis enumerates `V_1,\ldots,V_m`; the conclusion at line 2649 omits
the union index and grouping. Set distributivity gives the exact finite union.

Smallest correction: `E=\bigcup_{j=1}^m(E\cap V_j)`.

### `MC-STK-ERR-0040` — `TOPOLOGY-008`

Lines 3775--3785 choose a chain `Z_i\subset Y` and use its generic points in
the sober target `Y`. Calling these subsets closed in `X`, the domain of `f`,
is type-inconsistent.

Smallest correction: “irreducible closed subsets of `X`” -> “of `Y`”.

### `MC-STK-ERR-0041` — `TOPOLOGY-009`

For `Y\subset Y'` with generic points `\xi,\xi'`, one has
`\overline{\{\xi\}}=Y`, `\overline{\{\xi'\}}=Y'`, hence
`\xi'\leadsto\xi`. Definition 3843--3856 makes the dimension function decrease
under specialization. Therefore codimension is
`\delta(\xi')-\delta(\xi)`, in agreement with the preceding lemma at
3871--3872. Lines 3880, 3887, and 3888 reverse both direction and sign.

Linked corrections: use `\delta(\xi')-\delta(\xi)` at 3880 and 3888, and
`\xi_{i+1}\leadsto\xi_i` at 3887.

### `MC-STK-ERR-0042` — `TOPOLOGY-010`

After the explicit Noetherian reduction, irreducible components are closed and
there are finitely many. Their finite union through `x` is therefore closed.
It contains an open neighbourhood of `x` (remove the finite union of components
not containing `x`), but it need not itself be open.

Smallest correction: “not necessarily closed” -> “not necessarily open”.

### `MC-STK-ERR-0043` — `TOPOLOGY-011`

Density of `E` gives only `\operatorname{Int}(T)=\varnothing` for
`T=X\setminus E`; it does not in general make `T` nowhere dense. The next two
sentences are the argument that upgrades empty interior to nowhere density in
the finite locally closed case: each `T_i` is open dense in its closure `Z_i`,
so a nonempty interior of `Z_i` would contain a nonempty open subset of `T`.
The printed line assumes the conclusion before proving it.

Smallest correction at line 4106: “`T` is nowhere dense” -> “`T` has empty
interior”.

### `MC-STK-ERR-0044` — `TOPOLOGY-012`

The projections have domain `X\times Y`, so `p(X)` and `q(Y)` are not even
typed. Lines 4577--4579 prove `p(Z)` and `q(Z)` irreducible, and lines
4587--4590 explicitly use their closures.

Smallest linked corrections: `p(X)` -> `p(Z)` and `q(Y)` -> `q(Z)`.

### `MC-STK-ERR-0045` — `TOPOLOGY-013`

Line 4684 defines `f:X\to\prod_U W`. The symbol `Y` is introduced only at line
4693 as the image `f(X)`. The image-closed lemma at 4687 applies to the already
defined map into the product.

Smallest correction: at line 4686 replace codomain `Y` by `\prod_U W`.

### `MC-STK-ERR-0046` — `TOPOLOGY-014`

Lines 4793--4800 define the constructible-topology spaces `Z'_i` and prove
those spaces quasi-compact Hausdorff. The inverse-limit compactness lemma must
therefore be applied to `\lim Z'_i`, not to the unprimed spectral-topology
spaces. The next line compares `Z'_i\to Z_i`, confirming the distinction.

Smallest correction: `Z'=\lim Z_i` -> `Z'=\lim Z'_i`.

### `MC-STK-ERR-0047` — `TOPOLOGY-015`

The sets `E_i` are constructible, hence closed in the constructible topology.
The cited lemma proves that this constructible topology is compact Hausdorff.
Although the spectral topology on `Z` is also quasi-compact, the `E_i` need not
be closed there, so it cannot support the cited finite-intersection argument.

Smallest correction: “spectral topology” -> “constructible topology”.

### `MC-STK-ERR-0048` — `TOPOLOGY-016`

The lemma statement already gives `W\setminus E=\lim(U_i\setminus E)`.
The ungrouped proof line naturally reads `(\lim U_i)\setminus E`, which is a
tautological restatement of `W=\lim U_i` and does not identify the inverse
system being used. The universal-property sentence forces the grouped reading.

Smallest correction: `\lim U_i\setminus E` -> `\lim(U_i\setminus E)`.

### `MC-STK-ERR-0049` — `TOPOLOGY-017`

The construction defines `X^*=X\amalg\{\infty\}` and the canonical map
`X\to X^*`. Saying this identifies `X` with an open subspace of itself is
tautological and omits the codomain assertion.

Smallest correction: final `X` -> `X^*` at line 5167.

### `MC-STK-ERR-0050` — `TOPOLOGY-018`

The proof needs `E` to be the complement of the open set
`U\cap f^{-1}(V)`: this makes `E` closed, excludes `p`, and makes “if not, then
`x\in U\cap f^{-1}(V)`” exact. Under the natural left-associated reading of
the printed expression, these properties fail; the independent review supplied
a two-point discrete transposition example where the printed construction is
empty. The intended grouping is unique.

Smallest correction: `X\setminus U\cap f^{-1}(V)` ->
`X\setminus(U\cap f^{-1}(V))`.

### `MC-STK-ERR-0051` — `TOPOLOGY-019`

`X'=\beta(Y)` is the ambient Stone--Cech cover. Lines 5416--5430 construct a
minimal closed `E\subset X'` and prove `E` extremally disconnected. The
uniqueness paragraph then maps the ambient `X'` and invokes false “minimality
of `X'`”. The ambient cover need not be minimal; the independent review
exhibited proper closed subsets still mapping onto a nontrivial compact `X`.
The uniqueness proof is valid when run with the proved minimal cover `E`.

Linked correction: use `g:E\to X''`; replace both `g(X')` by `g(E)`; rename the
proper closed test subset to `T\subset E`; use `g(T)\ne X''` by minimality of
`E`.

### `MC-STK-ERR-0052` — `TOPOLOGY-020`

The fourth enumerated item is literally `add more here.`. Items (1)--(3) are
meaningful and valid; the placeholder asserts nothing and cannot be translated
or proved. Removing it invents no mathematical content. `Proof. Omitted.` is
left untouched because omission of a proof is not itself a false statement.

Smallest correction: delete the line `\item add more here.`.

### `MC-STK-ERR-0053` — `TOPOLOGY-021`

Standard refinement makes the finer parts subdivide the coarser parts. The
following source example says the `X_I` partition refines connected components;
indeed each nonempty `X_I` lies in an irreducible component and hence in one
connected component, so connected components are unions of `X_I`. The printed
pronouns state the opposite orientation. Later source usage has the standard
orientation as well.

Smallest unambiguous correction: “A partition `P` refines a partition `Q` if
every part of `Q` is a union of parts of `P`.” The misspelled internal label is
not bundled into this semantic unit.

### `MC-STK-ERR-0054` — `TOPOLOGY-022`

The source fixes right-coset representatives `G=\bigcup Hg_i`. For
`g=hg_i`, one has `g^{-1}Hg=g_i^{-1}Hg_i`; hence the finite core is
`\bigcap g_i^{-1}Hg_i`. The printed orientation need not be normal: the
independent `S_4`/point-stabilizer counterexample is recorded in the bounded
review. Changing to left cosets would also repair the proof, but preserving the
explicitly printed right-coset convention uniquely fixes the conjugates.

Smallest convention-preserving correction:
`\bigcap g_iHg_i^{-1}` -> `\bigcap g_i^{-1}Hg_i`.

### `MC-STK-ERR-0055` — `TOPOLOGY-023`

The values `G_i` and all transition morphisms must be topological groups.
For a diagram only in `Top`, a continuous transition map need not be a group
homomorphism, so precomposition would not define the displayed transition maps
on `Mor_{TopGroup}(G_i,H)`. The following sentence already names the intended
category.

Smallest typed correction: `\mathcal I\to\textit{Top}` ->
`\mathcal I\to\textit{TopGroup}`.

## Categories

### `MC-STK-ERR-0056` — `CATEGORIES-001`

With `g:W\to V` and `f:V\to U`, the only typed composite lifted directly is
`f\circ g:W\to U`. The diagram and the later equality
`\gamma\circ\chi=\phi\circ\psi` confirm this order.

Smallest correction: `g\circ f` -> `f\circ g`.

### `MC-STK-ERR-0057` — `CATEGORIES-002`

Lemma 6424--6450 defines the comparison as `\alpha_{g,f}` and names the
pseudo-functor datum in that order. Line 7048 alone reverses it.

Smallest correction: `\alpha_{f,g}` -> `\alpha_{g,f}`.

### `MC-STK-ERR-0058` — `CATEGORIES-003`

The inertia category is defined and stated as `\mathcal I_\mathcal S`. Line
7427 alone drops the calligraphic form, producing a different undeclared
symbol.

Smallest correction: `I_\mathcal S` -> `\mathcal I_\mathcal S`.

### `MC-STK-ERR-0059` — `CATEGORIES-004`

The proof has `b:\mathcal X\to\mathcal X''` and
`c:\mathcal X''\to\mathcal X\times_\mathcal Y\mathcal Y`. It announces and
constructs a 2-isomorphism `d\to c\circ b`. The printed conclusion
`d\to b\circ c` is not typed.

Smallest correction: `b\circ c` -> `c\circ b`.

### `MC-STK-ERR-0060` — `CATEGORIES-005`

Line 9148 contains adjacent composition operators `\circ\circ`, a
mechanically invalid duplicated token. The preceding factorization fixes the
single operator.

Smallest correction: delete one `\circ`.

### `MC-STK-ERR-0061` — `CATEGORIES-006`

The tensor product is a bifunctor whose domain is the categorical product
`\mathcal C\times\mathcal C`. The same chapter states this correctly at lines
8920 and 9172. `\mathcal C\otimes\mathcal C` is not a defined domain category.

Smallest correction: replace the domain separator `\otimes` by `\times`.

### `MC-STK-ERR-0062` — `CATEGORIES-007`

Section 8817--8822 defines products of fibred categories over `\mathcal C`.
Thus the product of the representables `\mathcal C/U` and `\mathcal C/V` is
represented by `U\times V`, namely `\mathcal C/(U\times V)`. The printed
`\mathcal C/U\times V` treats the object `V` as a category and is untyped.

Linked correction: replace the malformed right-hand representable and its two
diagram occurrences by `\mathcal C/(U\times V)`.

## Admission boundary

All 34 units have a forced local correction and may enter an R3 candidate.
The corrections to TOPOLOGY-018, -020, and -022 are admitted only with the
adverse evidence and scope choices recorded above: grouping recovers the unique
proof construction; scaffold deletion invents no theorem; and the coset repair
preserves the printed right-coset convention. Candidate payload construction,
builds, visual QA, schema closure, and independent replay remain separate gates.
