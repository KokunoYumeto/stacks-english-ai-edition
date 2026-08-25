# R4 topology queue: independent review of TOPOLOGY-024 through TOPOLOGY-040

## Frozen scope and independently recomputed identities

- Intake: `canon/control/ERRATA_R4_INTAKE_FRENCH_20260822.json`
  - byte count: **7,392**
  - SHA-256: **DDB2CA1AEBCF130DF35DA62B34864ABBC3DD03CFC312F4FC86C6468101AD9173**
- Authority: `upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/topology.tex`
  - byte count: **237,731**
  - SHA-256: **C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872**
  - frozen upstream commit supplied by the intake: **a04446e57ec1fbc252a871afcec7752fb2807b14**

The byte counts and hashes above were recomputed from the two exact local files, not copied as assumed facts from the intake. Review was confined to the 17 frozen hypotheses, their exact loci, the required surrounding arguments, and exact same-file label references. No Git operation, upstream contact, authority edit, translation edit, intake edit, or candidate mutation was performed.

## Disposition summary

| ID | Disposition | Classification |
|---|---|---|
| TOPOLOGY-024 | **ACCEPT** | DCC supplies a minimal, not necessarily least/smallest, member |
| TOPOLOGY-025 | **ACCEPT** | missing union operator |
| TOPOLOGY-026 | **ACCEPT** | missing union operator |
| TOPOLOGY-027 | **ACCEPT** | missing intersection operator |
| TOPOLOGY-028 | **ACCEPT** | DCC supplies a minimal, not necessarily least/smallest, member |
| TOPOLOGY-029 | **ACCEPT** | point-dependent basis choice is incorrectly indexed only by the cover index |
| TOPOLOGY-030 | **ACCEPT** | ill-typed complement/preimage identity swaps source and target |
| TOPOLOGY-031 | **ACCEPT** | the new index is free; its existence was proved but it is not bound at use |
| TOPOLOGY-032 | **ACCEPT** | refinement can remove more than one bad tuple |
| TOPOLOGY-033 | **ACCEPT** | graph-as-product formula is ill-typed when `j = k`; both occurrences need projection preimages |
| TOPOLOGY-034 | **ACCEPT** | “third” incorrectly suggests distinctness that the theorem neither assumes nor proves |
| TOPOLOGY-035 | **ACCEPT** | literal unfinished equivalence item, with no corresponding proof |
| TOPOLOGY-036 | **ACCEPT** | free variable `g` omits the quantifier needed for the following inclusion |
| TOPOLOGY-037 | **REJECT as defect** | density is already invoked by “By (c)”; rewrite is optional clarity only |
| TOPOLOGY-038 | **REJECT as defect** | the cited hypothesis already supplies a nonempty witness; repeating “nonempty” is optional clarity |
| TOPOLOGY-039 | **ACCEPT** | exhibited point-closure family need not be directed; finite unions repair the proof |
| TOPOLOGY-040 | **REJECT as defect** | intended scope is fixed by the asserted properties and proof context; parentheses are optional style |

Totals: **14 accepted, 3 rejected as canon defects, 0 deferred**.

“Accept” means the frozen authority contains a real local defect, including a formally free variable or a misleading semantic overclaim. “Reject as defect” does not forbid an editorial rewrite; it means the authority's mathematical inference is already recoverable from its explicit hypotheses and context, so the proposed change is not required for correctness.

## Item-by-item proof and adverse review

### TOPOLOGY-024 — ACCEPT

**Locus and authority.** Lines 1273–1289 form the contradiction proof that a Noetherian space has finitely many irreducible components. Lines 1278–1279 say:

```tex
By the descending chain condition we may find a
smallest element of $A$, say $Z$.
```

**Derivation.** For inclusion order, a *smallest* (least) member `Z` would satisfy `Z \subset Z'` for every `Z' \in A`. DCC gives only a *minimal* member: there is no `Z' \in A` with `Z' \subsetneq Z`. The inference “DCC implies least” is false even for finite posets: the two-member family `{{a}, {b}}` of closed subsets of the discrete space `{a,b}` satisfies DCC but has no least member under inclusion.

The proof needs only minimality. From `Z = Z' \cup Z''` with both `Z'` and `Z''` proper closed subsets of `Z`, minimality gives `Z',Z'' \notin A`; therefore each has finitely many irreducible components, yielding the contradiction. No comparison with every member of `A` is used.

**Smallest exact replacement.** Replace only:

```tex
smallest element of $A$
```

by:

```tex
minimal element of $A$
```

**Dependent-use check.** The same-file references to Lemma `lemma-Noetherian` are at lines 1376, 1379, 1951, 2922, 3698, 3908, 3934, and 5642. They consume its stated conclusions, not the stronger word “smallest”; the replacement leaves all conclusions and uses unchanged.

### TOPOLOGY-025 — ACCEPT

**Locus and authority.** In the proof of part (3) of Lemma `lemma-Noetherian`, line 1297 reads:

```tex
Because $X = Z \cup Z_1 \cup \ldots Z_n$ (see Lemma \ref{lemma-irreducible}),
```

**Derivation.** The previously named irreducible components are `Z,Z_1,\ldots,Z_n`, and line 1298 takes the complement of `Z_1\cup\cdots\cup Z_n`. Thus line 1297 must be the finite union of all these components. Juxtaposition `\ldots Z_n` supplies no set operation and does not denote that union.

**Smallest exact replacement.** Replace:

```tex
Z \cup Z_1 \cup \ldots Z_n
```

by:

```tex
Z \cup Z_1 \cup \ldots \cup Z_n
```

**Dependent-use check.** This is internal notation in the proof of `lemma-Noetherian`. The same-file consumers listed under TOPOLOGY-024 use the unchanged lemma statement.

### TOPOLOGY-026 — ACCEPT

**Locus and authority.** Lines 1345–1348 distribute an intersection over a finite union:

```tex
F_m = G_m \cap X' = G_m \cap (X_1 \cup \ldots \cup X_n) =
(G_m \cap X_1) \cup \ldots (G_m \cap X_n)
```

**Derivation.** Set distributivity gives

`G_m \cap (X_1\cup\cdots\cup X_n)=(G_m\cap X_1)\cup\cdots\cup(G_m\cap X_n)`.

The last displayed term is merely juxtaposed after `\ldots`; the final `\cup` is missing. Stabilization of every `G_m\cap X_i` then implies stabilization of their correctly written finite union.

**Smallest exact replacement.** Replace:

```tex
(G_m \cap X_1) \cup \ldots (G_m \cap X_n)
```

by:

```tex
(G_m \cap X_1) \cup \ldots \cup (G_m \cap X_n)
```

**Dependent-use check.** As for TOPOLOGY-025, this repairs only an internal display in `lemma-Noetherian`; all same-file consumers use the unchanged conclusion.

### TOPOLOGY-027 — ACCEPT

**Locus and authority.** Lines 2165–2168 assert the containment satisfied by the refined opens, but lines 2167–2168 read:

```tex
V_{j_0, k} \cap V_{j_1} \ldots \cap V_{j_p} \subset
W_{\alpha(j_0) \ldots \alpha(j_p), k}.
```

**Derivation.** The set on the left is the `(p+1)`-fold intersection. This is also forced by lines 2161–2163, where `V_{j_0,k}=V_{j_0}\cap W_{i_0\ldots i_p,k}`, and by the target property at lines 2114–2116. An intersection operator is absent between `V_{j_1}` and the continuation ellipsis.

**Smallest exact replacement.** Replace:

```tex
V_{j_1} \ldots \cap V_{j_p}
```

by:

```tex
V_{j_1} \cap \ldots \cap V_{j_p}
```

**Dependent-use check.** `lemma-refine-covering` has no same-file `\ref` occurrence beyond its label. The repair agrees with, and does not alter, the lemma statement at lines 2112–2116.

### TOPOLOGY-028 — ACCEPT

**Locus and authority.** Lines 2916–2919 say that the nonempty family `\mathcal S` of closed subsets on which constructibility fails has a “smallest” member by Noetherianity.

**Derivation.** This is the same order-theoretic error as TOPOLOGY-024. DCC on closed subsets guarantees a minimal member of `\mathcal S`, not a least one. Lines 2923–2925, 2931–2932, and 2937–2940 use only the fact that proper closed subsets of `Y` are not in `\mathcal S`. Thus minimality is exactly sufficient.

**Smallest exact replacement.** Replace:

```tex
then it has a smallest element $Y$
```

by:

```tex
then it has a minimal element $Y$
```

**Dependent-use check.** Same-file references to `lemma-characterize-constructible-Noetherian` occur at lines 2972, 2997, and 3815. They use the unchanged equivalence, so the terminology repair has no downstream cost.

### TOPOLOGY-029 — ACCEPT

**Locus and authority.** Lines 345–349 choose `i_x`, then write a basis member as `B_{i_x}`, set `J={i_x\mid x\in U}`, and use one `V_j` for each resulting cover index.

**Counterexample to the written construction.** Let `X=\mathbb R`, let `\mathcal B` be the basis of bounded open intervals with rational endpoints, and take the one-member cover `I={0}`, `U_0=\mathbb R`. Necessarily `i_x=0` for every `x`. Pointwise there is a basis interval around each `x`, but no single bounded basis member `B_0` contains every real number. The written `J={0}` and `V_0=B_0` therefore do not cover `U`. The choice of basis member depends on `x`, even when `i_x` is the same for many points.

**Smallest coherent old-to-new replacement.** Replace lines 345–349:

```tex
If $ x \in U = \bigcup_{i\in I} U_i $, there is an $ i_x \in I $ such that
$ x \in U_{i_x} $. Thus we have a $ B_{i_x} \in \mathcal{B}$
verifying $ x \in B_{i_x} \subset U_{i_x}$. Set
$J = \{i_x | x \in U\}$ and for $j = i_x \in J$ set $V_j = B_{i_x}$.
This gives the desired open covering of $U$ by $\{V_j\}_{j \in J}$.
```

with:

```tex
For every $x \in U = \bigcup_{i \in I} U_i$, choose $i_x \in I$ and
$B_x \in \mathcal{B}$ such that $x \in B_x \subset U_{i_x}$.
Set $J = U$ and, for $j = x \in J$, set $V_j = B_x$.
This gives the desired open covering of $U$ by $\{V_j\}_{j \in J}$.
```

Every new member is in the basis and is contained in a member `U_{i_x}`, which is precisely the refinement definition at lines 87–92.

**Dependent-use check.** `lemma-refine-covering-basis` has no same-file `\ref` occurrence beyond its label. The replacement proves exactly the existing statement.

### TOPOLOGY-030 — ACCEPT

**Locus and authority.** For `f:X\to Y`, lines 514–515 use

```tex
f^{-1}(X\setminus E) = Y \setminus f^{-1}(E) ... E \subset X.
```

**Type check.** The argument of `f^{-1}` must be a subset of the codomain `Y`, while `f^{-1}(E)` is a subset of the domain `X`. The displayed identity reverses both spaces. The correct complement law is

`f^{-1}(Y\setminus E)=X\setminus f^{-1}(E)` for `E\subset Y`.

This is exactly the law needed to pass between the open and closed characterizations of the quotient topology.

**Smallest exact replacement.** Replace lines 514–515 by:

```tex
Finally, (2) and (3) equivalence follows from $f^{-1}(Y \setminus E) = X
\setminus f^{-1}(E)$ for all subsets $E \subset Y$.
```

**Dependent-use check.** `lemma-quotient` has no same-file `\ref` occurrence beyond its label. The topology and all three equivalent conditions remain unchanged.

### TOPOLOGY-031 — ACCEPT

**Locus and authority.** Lines 1831–1834 define `S=\bigcap_{\alpha\in A}Z_\alpha` using all clopen subsets containing `x` and note that every finite intersection is another member. After choosing `\alpha'` and `\alpha''`, lines 1851–1852 say:

```tex
Then $Z_\alpha = Z_{\alpha'} \cap Z_{\alpha''}$ is contained
in $U \cup V$ and disjoint from $U \cap V$.
```

**Derivation.** The note at line 1834 proves that there exists an index `\alpha\in A` representing this intersection, because the intersection is again clopen and contains `x`. But the displayed `\alpha` at line 1851 is a new free index; neither an existential quantifier nor a choice binds it. Once that index is chosen, the rest of the decomposition argument is valid.

**Smallest coherent replacement.** Replace the quoted sentence by:

```tex
Choose $\alpha \in A$ such that
$Z_\alpha = Z_{\alpha'} \cap Z_{\alpha''}$. Then $Z_\alpha$ is contained
in $U \cup V$ and disjoint from $U \cap V$.
```

**Dependent-use check.** `lemma-connected-component-intersection` is used at lines 1914 and 4566. Both uses consume only its unchanged characterization of connected components; binding `\alpha` completes the existing proof without changing that characterization.

### TOPOLOGY-032 — ACCEPT

**Locus and authority.** Lines 2174–2176 claim that the replacement makes `N` decrease by exactly one and hence can be repeated `N` times.

**General count.** A new bad tuple maps, via the refinement map `\beta:J'\to J` of lines 2187–2188, to an old bad tuple. For an old bad tuple whose first entry is the selected `j_0`, all new entries from `K` are good because their opens lie in a specified `W_{i_0\ldots i_p,k}`; at most the residual entry still gives a bad tuple. The selected tuple gives none because the residual open is disjoint from `V_{j_1}\cap\cdots\cap V_{j_p}`. Thus `N` decreases by **at least** one. Other old bad tuples sharing first entry `j_0` may disappear too.

**Counterexample to “by one”.** Take `p=1`, the finite discrete compact Hausdorff space `X={a,b}`, `I={0,1}`, and `U_0=U_1=X`. Let the cover for `(0,1)` be `W_{01,1}={a}`, `W_{01,2}={b}`; take `W_{00,1}=W_{11,1}=X` for the repeated-index cases. Let `J={r,s,t}`, `\alpha(r)=0`, `\alpha(s)=\alpha(t)=1`, and `V_r=V_s=V_t=X`. The two pairs `(r,s)` and `(r,t)` are bad, so `N=2`. Refining with the selected pair `(r,s)` leaves residual `V'_r=\varnothing` and adds `{a}` and `{b}`. Every new pair over either `s` or `t` is now empty, `{a}`, or `{b}`, hence good. Therefore `N` drops from `2` to `0`, not from `2` to `1`.

**Smallest coherent replacement.** Replace lines 2174–2176 by:

```tex
A simple check shows that $N$ has decreased by at least one under this
replacement. Repeating this procedure at most the original $N$ times,
we arrive at the situation where $N = 0$.
```

Equivalently, “`N` strictly decreases; repeating, we reach `N=0`” is sufficient.

**Dependent-use check.** `lemma-refine-covering` has no same-file `\ref` occurrence beyond its label. The corrected termination bound proves the same statement.

### TOPOLOGY-033 — ACCEPT

**Loci and authority.** Lines 2487–2496 and 2515–2523 represent the compatibility condition for a morphism `\varphi:j\to k` as

```tex
\Gamma_\varphi \times \prod\nolimits_{l \not = j, k} X_l
\subset \prod X_i.
```

The second proof repeats this expression as the definition of `Z_\varphi`.

**Type failure.** A category may have an endomorphism, so `j=k` is allowed. Even for `\varphi=\mathrm{id}_j`, `\Gamma_\varphi` lies in `X_j\times X_j`, whereas `\prod_iX_i` has only one `X_j` coordinate. Multiplying the graph by the factors with `l\ne j,k` therefore does not produce a subset of `\prod_iX_i`. The expression is ill-typed; it is not merely a missing convention.

Let

`p_{j,k}:\prod_iX_i\to X_j\times X_k`, `(x_i)\mapsto(x_j,x_k)`.

Then the compatibility locus is exactly `p_{j,k}^{-1}(\Gamma_\varphi)`. For `j=k`, this says `(x_j,x_j)\in\Gamma_\varphi`, equivalently `\varphi(x_j)=x_j`, which is the correct endomorphism constraint. For the identity endomorphism its inverse image is all of the product, as it should be. Since `p_{j,k}` is continuous and the graph is closed, the corrected locus is closed.

**Smallest coherent replacements.** In lines 2491–2496, replace the displayed product construction (and introduce the map) by:

```tex
Let $p_{j,k} : \prod X_i \to X_j \times X_k$ be the continuous map
$(x_i) \mapsto (x_j, x_k)$. It is clear that $\lim X_i$ is the
intersection of the closed subsets
$$
p_{j,k}^{-1}(\Gamma_\varphi) \subset \prod X_i.
$$
```

In lines 2518–2523, replace the definition display and extend its following sentence by:

```tex
$$
Z_\varphi = p_{j,k}^{-1}(\Gamma_\varphi)
$$
inside the quasi-compact space $\prod X_i$, where
$p_{j,k} : \prod X_i \to X_j \times X_k$ is the map
$(x_i) \mapsto (x_j, x_k)$, $\varphi : j \to k$ is a morphism of
$\mathcal{I}$, and $\Gamma_\varphi \subset X_j \times X_k$ is the graph
of the corresponding morphism $X_j \to X_k$.
```

Both occurrences must change; repairing only the first leaves `Z_\varphi` ill-typed.

**Dependent-use check.** `lemma-inverse-limit-quasi-compact` is invoked at lines 2515, 4148, 4193, and 4802; `lemma-nonempty-limit` is invoked at line 4831. The finite-intersection construction at lines 2526–2545 already equalizes coincident source/target coordinates, including the `j_t=k_t` case, so it proves nonemptiness of the corrected projection-preimage loci. The theorem statements and all downstream uses remain valid.

### TOPOLOGY-034 — ACCEPT

**Locus and authority.** Lines 4499–4501 say there exists “a third point specializing to both `x` and `y`” or disjoint neighbourhoods.

**Counterexamples to distinctness.** The lemma does not assume `x\ne y`, and its proof at lines 4520–4521 chooses any common generalization without proving it differs from either point. In a one-point spectral space with `x=y`, the common point is `x`, while no pair of disjoint neighbourhoods can both contain `x`; there is no distinct “third” point. Even with `x\ne y`, in the two-point Sierpiński spectral space where `x` is a generalization of `y`, the only common generalization can be `x` itself and the two points do not have disjoint neighbourhoods. Thus the ordinary distinctness implication of “third point” is unsupported.

**Smallest exact replacement.** Replace:

```tex
a third point specializing to both $x$ and $y$
```

by:

```tex
a point specializing to both $x$ and $y$
```

**Dependent-use check.** `lemma-two-points` has no same-file `\ref` occurrence beyond its label. The replacement makes the statement match exactly what lines 4504–4521 prove.

### TOPOLOGY-035 — ACCEPT

**Locus and authority.** The equivalence list at lines 4526–4538 ends with:

```tex
\item the constructible topology equals the given topology on $X$, and
\item add more here.
```

**Adverse check.** Lines 4542–4557 prove the equivalences among items (1)–(8) and contain no ninth condition or implication involving item (9). “add more here.” is neither a mathematical proposition nor a proved equivalent condition. It is a literal editorial placeholder.

**Smallest coherent replacement.** Delete the placeholder and terminate item (8):

```tex
\item the constructible topology equals the given topology on $X$.
```

That is, remove line 4537 and replace the terminal `, and` on line 4536 by `.`.

**Dependent-use check.** `lemma-characterize-profinite-spectral` has no same-file `\ref` occurrence beyond its label. The proof already closes after condition (8), so no proof text must be removed.

### TOPOLOGY-036 — ACCEPT

**Locus and authority.** After constructing `U_t`, lines 5813–5815 say:

```tex
$U_t = U_{w_1} \cap \ldots \cap U_{w_n}$ is an open neighbourhood
of $e$ such that $f(gw) = t$ for all $w \in W$.
Since $T$ is finite we see that $\bigcap_{t \in T} U_t \subset H$
```

**Derivation.** The construction proves the two-variable statement. If `g\in U_t` and `w\in W`, choose `i` with `w\in U'_{w_i}`; then `g\in U_{w_i}` and `U_{w_i}U'_{w_i}\subset W`, so `gw\in W` and `f(gw)=t`. Consequently, for `g\in\bigcap_tU_t` and arbitrary `g'\in G`, put `t=f(g')` and `W=f^{-1}(t)`; then `f(gg')=t=f(g')`, hence `g\in H`. Without `g\in U_t`, the displayed sentence has a free `g` and does not state the universal fact needed for the inclusion.

**Smallest exact replacement.** Replace:

```tex
such that $f(gw) = t$ for all $w \in W$.
```

by:

```tex
such that $f(gw) = t$ for all $g \in U_t$ and $w \in W$.
```

**Dependent-use check.** The only same-file reference to `lemma-profinite-group` is line 5847, which defines “profinite group” via its unchanged equivalent conditions. The quantifier repair supplies exactly the step used locally to prove `\bigcap_tU_t\subset H`.

### TOPOLOGY-037 — REJECT AS DEFECT (optional clarity only)

**Locus and authority.** Assumption (c), lines 1120–1121, says explicitly that the set

`D={y\in Y\mid f^{-1}(y)\text{ is irreducible}}`

is dense. Lines 1129–1133 establish that `O=f(U_1)\cap f(U_2)` is nonempty open and then say, “By (c) there is a point `y` ... of this intersection such that the fibre ... is irreducible.”

**Formal reconstruction.** Since `D` is dense and `O` is nonempty open, `D\cap O\ne\varnothing`. Choose `y\in D\cap O`. Membership in `O` makes both `X_y\cap U_i` nonempty, and membership in `D` makes `X_y` irreducible, producing the contradiction. The phrase “By (c)” invokes the condition whose content is density; no additional hypothesis is missing.

Changing the sentence to “By density in (c), choose `y\in f(U_1)\cap f(U_2)` with irreducible fibre” would be clearer, and “corresponds to a point of this intersection” is awkward English, but it would only spell out the already valid inference.

**Dependent-use check.** The only same-file reference is line 1155, which applies the lemma after verifying its hypotheses. The proof and that use are valid without a source correction.

### TOPOLOGY-038 — REJECT AS DEFECT (optional clarity only)

**Locus and authority.** The lemma statement at lines 2902–2903 explicitly says that `E\cap Z` “contains a nonempty open of `Z`” or is not dense. Lines 2929–2930 invoke “assumption (2)” and introduce an open `V` in case (a); line 2931 uses `Y\setminus V` as a proper closed subset.

**Formal reconstruction.** In case (a), choose `V` to be the witness supplied by condition (2). That witness is nonempty by the quantified condition, whether or not the adjective is repeated in line 2930. Therefore `Y\setminus V\subsetneq Y`, and minimality applies. The proof does not derive nonemptiness from the weakened phrase at line 2930; it retains it from the cited hypothesis used to choose `V`.

Inserting “nonempty” before “open `V`” would improve local explicitness but does not repair a mathematical gap.

**Dependent-use check.** Same-file uses of `lemma-characterize-constructible-Noetherian` occur at lines 2972, 2997, and 3815. They rely on the statement's already explicit “nonempty open” alternative. No consumer depends on the abbreviated restatement in its proof.

### TOPOLOGY-039 — ACCEPT

**Locus and authority.** The statement at lines 3594–3601 requires a directed union of closed subsets. The forward proof at lines 3605–3607 exhibits only

```tex
T = \bigcup_{y\in T} \overline{\{y\}}.
```

**Counterexample to directedness of the exhibited family.** In a two-point discrete space with `T=X`, the point closures are `{a}` and `{b}`. Neither contains the other, and the family consisting only of these two closures has no member containing their union. Hence that particular family is not directed by inclusion, although `T` is specialization-stable.

**Repair and proof.** For every finite subset `S\subset T`, set

`F_S=\bigcup_{y\in S}\overline{\{y\}}`.

Each `F_S` is closed (finite union) and lies in `T` by specialization stability. The family is directed because `F_S\cup F_{S'}=F_{S\cup S'}`, and its union is `T`: every `y\in T` lies in `F_{\{y\}}`, while every `F_S` lies in `T`. Including `S=\varnothing` also handles `T=\varnothing` with a nonempty directed index family if that convention is required. The converse proof needs no change; even an arbitrary union of closed subsets is specialization-stable.

**Smallest coherent replacement.** Replace lines 3605–3607 through “which is an union ...” by:

```tex
Suppose that $T$ is stable under specialization. For every finite subset
$S \subset T$ set
$$
F_S = \bigcup_{y \in S} \overline{\{y\}}.
$$
Then $F_S$ is closed and contained in $T$, the family $(F_S)$ is directed
by inclusion since $F_S \cup F_{S'} = F_{S \cup S'}$, and
$T = \bigcup_{S \subset T\text{ finite}} F_S$.
```

Continue with the existing converse beginning “Reciprocally, suppose that ...”.

**Dependent-use check.** `lemma-stable-specialization` has no same-file `\ref` occurrence beyond its label. The repaired proof establishes the statement as written.

### TOPOLOGY-040 — REJECT AS DEFECT (optional parenthesization)

**Locus and authority.** Lines 4015 and 4017 contain, respectively,

```tex
U \setminus U \cap \overline{B}
U \setminus U \cap \overline{A}
```

**Contextual parse and proof.** The next words say the first set is open in `X` and contained in `\overline A`. Those asserted properties force the intended operand of `\setminus` to be `U\cap\overline B`:

`U\setminus(U\cap\overline B)=U\setminus\overline B`.

Because `U\subset\overline A\cup\overline B`, this open set lies in `\overline A` and is empty since `A` is nowhere dense. Thus `U\subset\overline B`; as `U` is open and `B` is nowhere dense, `U=\varnothing`. The symmetric sentence gives the analogous conclusion. The prose therefore disambiguates the notation and the proof is valid.

Parenthesizing as `U \setminus (U \cap \overline B)` and `U \setminus (U \cap \overline A)` would make the display easier to parse, but it changes no proposition or inference. This is a style improvement, not a required canon correction.

**Dependent-use check.** The only same-file reference to `lemma-nowhere-dense` is at line 4109, where its unchanged finite-union conclusion is used. That use is valid.

## Cross-item dependency and completion gate

- The accepted edits for TOPOLOGY-024 through -032 and -036 and -039 repair proofs or notation without changing lemma statements.
- TOPOLOGY-033 must be corrected in both the quasi-compact-limit proof and the copied `Z_\varphi` definition; its corrected formulation preserves all later inverse-limit uses, including diagrams with endomorphisms.
- TOPOLOGY-034 removes an unsupported distinctness suggestion and makes the statement coincide with its proof.
- TOPOLOGY-035 removes only the unproved placeholder; conditions (1)–(8) and their proof remain intact.
- The rejected items -037, -038, and -040 are optional clarity edits. Treating them as mandatory mathematical errata would overstate the frozen authority's defects.
- No hypothesis requires deferral: every item is decided from the frozen authority and its same-file dependencies.

This review is a disposition record only. It does not alter the frozen authority, any translation, the intake, or an R3/R4 candidate.
