# R4 independent review: `SITES-014` through `SITES-024`

Review date: 2026-08-22  
Scope: the eleven named ledger candidates only. The review used only the frozen `sites.tex` authority and the selected ledger rows. No translation, authority, ledger, build, or Git state was changed.

## Frozen input identities

- Authority: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex`
  - byte count: `424197`
  - SHA-256: `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
  - result: exact match to the frozen authority identity supplied for this review
- Candidate ledger: `<LOCAL_WORKSPACE>/03_projects\language_management\romance\03_working_translations\stacks_fr_20260821\00_control\SOURCE_DEFECT_LEDGER.csv`
  - byte count: `64191`
  - CSV data-row count (header excluded): `155`
  - SHA-256: `B5DA691E4FC026C375A069CF92BF7D9168894EE190C96FFBEDDBF13A1708868E`
  - result: exact match to the frozen ledger identity supplied for this review
  - selected row IDs, in ledger order: `SITES-014`, `SITES-015`, `SITES-016`, `SITES-017`, `SITES-018`, `SITES-019`, `SITES-020`, `SITES-021`, `SITES-022`, `SITES-023`, `SITES-024`

Concurrency note: the ledger identity above is the verified input snapshot from which the eleven rows were read. A read-only check after this review file was written found that the live shared ledger path had been changed concurrently to `65495` bytes, `159` data rows, SHA-256 `96C203A7AF6C2908EC9687E112330A7CD25219566E4F6164C20F42B0BB8C8A91` (filesystem last-write time `2026-08-22T04:12:05.1525439Z`). All fields of the eleven selected rows were unchanged on that second read; the four additional rows were outside this review's scope and were not inspected. This reviewer did not write the ledger.

## Governing source conventions

The type checks below use the conventions stated in `sites.tex:3769-3803`. For an arrow \(a:i\to j\) in the cofiltered category \(\mathcal I\), the source defines

\[
f_a:\mathcal C_i\to\mathcal C_j,
\qquad
u_a:\mathcal C_j\to\mathcal C_i,
\]

and states that if \(c=a\circ b\), then \(f_a\circ f_b=f_c\) and \(u_b\circ u_a=u_c\). The canonical functor \(u_i:\mathcal C_i\to\mathcal C\) is introduced at `sites.tex:3803`. Thus, when \(a:j\to i\) and \(b:k\to j\), one has

\[
u_a:\mathcal C_i\to\mathcal C_j,
\quad
u_b:\mathcal C_j\to\mathcal C_k,
\quad
a\circ b:k\to i.
\]

These declarations settle the variance and composition questions in `SITES-015` through `SITES-017`, `SITES-020`, and `SITES-021` without recourse to any external source.

## Complete verdict table

| ID | Exact locus | Verdict | Class | Smallest correction |
|---|---:|---|---|---|
| `SITES-014` | 3884 | **ACCEPTED** | prose typo | Delete the prose article `a` immediately before the math variable `$a : j \to i$`. |
| `SITES-015` | 3885 | **ACCEPTED** | object-type error | Replace `\Ob(\mathcal{C})` by `\Ob(\mathcal{C}_j)`. |
| `SITES-016` | 3891, 3893-3896 | **ACCEPTED** | bound-index/variance errors | At 3891 and 3893 replace the displayed arrow name `b` by `a`; make explicit at 3896 that the restriction arrows use `u_b(\alpha_j)` for `b:k\to j`. |
| `SITES-017` | 3905-3906 | **ACCEPTED** | ill-typed composition | Replace both `b \circ a` occurrences by `a \circ b`. |
| `SITES-018` | 3940, 3947 | **ACCEPTED** | TeX/identity notation | Replace both `\varphi_{id}` occurrences by `\varphi_{\text{id}}`. |
| `SITES-019` | 3957 | **ACCEPTED** | subject-verb agreement | Replace `commutes` by `commute`. |
| `SITES-020` | 3987 | **ACCEPTED** | sheaf-domain error | Replace `\mathcal{F}_i` by `\mathcal{F}_j`. |
| `SITES-021` | 4022 | **ACCEPTED** | ill-typed composition | Replace `b:k\to i` by `b:k\to j`. |
| `SITES-022` | 4028, 4035, 4040 | **ACCEPTED** | undefined index symbol | Replace each `i \in I` by `i \in \Ob(\mathcal I)`. |
| `SITES-023` | 4035, 4040 | **ACCEPTED** | undefined sheaf / omitted functor | Replace both `f_i^{-1}\mathcal F_i` occurrences by `f_i^{-1}f_{i,*}\mathcal F`. |
| `SITES-024` | 4388-4390 | **ACCEPTED** | sentence fragment | Join the two lines grammatically: change the period after the lemma reference to a comma and `For` to `for`. |

## Typed and textual findings

### `SITES-014` — ACCEPTED

Source evidence: `sites.tex:3884` reads “we can pick a `$a : j \to i$`”.

Adverse evidence against the frozen text: the first `a` is the English indefinite article and the second is the mathematical variable. Keeping both produces an accidental duplicate token; no notation convention can make “pick a a” grammatical.

Smallest correction: delete only the prose `a`, producing “we can pick `$a : j \to i$`”.

### `SITES-015` — ACCEPTED

Source evidence: `sites.tex:3885` declares \(V_j\in\Ob(\mathcal C)\), while also requiring \(V=u_j(V_j)\). The defining colimit at `sites.tex:3888` applies \(u_b\) to the same \(V_j\), for \(b:k\to j\).

Adverse evidence against the frozen text: \(u_j\) has domain \(\mathcal C_j\), not \(\mathcal C\). Also, for \(b:k\to j\), \(u_b:\mathcal C_j\to\mathcal C_k\); hence \(u_b(V_j)\) is typed only when \(V_j\in\Ob(\mathcal C_j)\). The subscript \(j\) and the later correctly typed quantification \(V_j\in\Ob(\mathcal C_j)\) at `sites.tex:3933` corroborate this reading.

Smallest correction: at `sites.tex:3885`, change `\Ob(\mathcal{C})` to `\Ob(\mathcal{C}_j)`.

### `SITES-016` — ACCEPTED

Source evidence:

- `sites.tex:3884-3888` first chooses \(a:j\to i\), then defines the value by a colimit whose dummy arrow is \(b:k\to j\).
- `sites.tex:3891` instead says independence is from the choice of \(b:j\to i\).
- `sites.tex:3893-3896` again chooses \(b:j\to i\), then applies \(u_b\) to a morphism \(\alpha_j:V_j\to V'_j\) of \(\mathcal C_j\).

Adverse evidence against the frozen text: the representative-level arrow chosen at 3884 is \(a\), so the independence assertion must concern \(a\), not the colimit dummy \(b\). More decisively, an arrow \(b:j\to i\) induces \(u_b:\mathcal C_i\to\mathcal C_j\), which cannot be applied to \(\alpha_j\in\operatorname{Arrows}(\mathcal C_j)\). The restrictions in the colimit are instead obtained for \(b:k\to j\), when \(u_b:\mathcal C_j\to\mathcal C_k\).

Smallest correction: replace `b` by `a` in the two choices at 3891 and 3893, and read/make explicit the final restriction family as \(u_b(\alpha_j)\) for \(b:k\to j\). No change to the actual \(u_b(\alpha_j)\) term is needed.

### `SITES-017` — ACCEPTED

Source evidence: `sites.tex:3901` fixes \(a:j\to i\), while the two colimits at `sites.tex:3905-3906` run over \(b:k\to j\) but use \(f_{b\circ a}^{-1}\).

Adverse evidence against the frozen text: with these domains and codomains, \(a\circ b:k\to i\) exists; \(b\circ a\) is not composable in general. The governing Situation explicitly uses \(c=a\circ b\) (`sites.tex:3780`), and the correctly typed defining formula at `sites.tex:3888` already has \(f_{a\circ b}^{-1}\).

Smallest correction: replace both instances of `f_{b \circ a}^{-1}` by `f_{a \circ b}^{-1}`.

### `SITES-018` — ACCEPTED

Source evidence: the system is indexed by `\text{id}` at `sites.tex:3935`, `3936`, `3938`, and `3939`, but the resulting identity-indexed map is written `\varphi_{id}` at 3940 and 3947.

Adverse evidence against the frozen text: in TeX math mode, bare multi-letter `id` is rendered as adjacent italic math letters, whereas the identity morphism used to define this exact component is consistently `\text{id}`. Moreover, `sites.tex:3937` names the family \(\varphi_a\), so its identity component should carry the same identity symbol as the indices from which it is derived.

Counter-consideration: the intended identity component remains inferable, so this is typographical rather than a change to the mathematical argument. That does not remove the source-notation defect.

Smallest correction: change both `\varphi_{id}` tokens to `\varphi_{\text{id}}`.

### `SITES-019` — ACCEPTED

Source evidence: `sites.tex:3957-3958` says “the functors \(f_a^{-1}\) commutes with finite limits”.

Adverse evidence against the frozen text: the grammatical head of the subject is plural, “functors”, and therefore requires the plural verb “commute”.

Smallest correction: `commutes` to `commute`.

### `SITES-020` — ACCEPTED

Source evidence: the lemma statement at `sites.tex:3980` has

\[
\mathop{\rm colim}_{a:j\to i}\mathcal F_j(u_a(X_i)),
\]

but the proof begins at `sites.tex:3987` with the same expression using \(\mathcal F_i(u_a(X_i))\).

Adverse evidence against the frozen text: for \(a:j\to i\), \(u_a:\mathcal C_i\to\mathcal C_j\), so \(u_a(X_i)\in\Ob(\mathcal C_j)\). The sheaf \(\mathcal F_i\) lives on \(\mathcal C_i\) and cannot be evaluated on that object; \(\mathcal F_j\) lives on the correct site. After that substitution, the next equality is typed because \(u_bu_a=u_{a\circ b}\), exactly as stated at `sites.tex:3795-3796`.

Smallest correction: change `\mathcal{F}_i` to `\mathcal{F}_j` at 3987.

### `SITES-021` — ACCEPTED

Source evidence: `sites.tex:4022` takes \(a:j\to i\) and \(b:k\to i\), then declares \(c=a\circ b\); `sites.tex:4024` uses the corresponding cocycle formula.

Adverse evidence against the frozen text: \(a\circ b\) is defined only when the codomain of \(b\) is the domain \(j\) of \(a\). This is also precisely the arrow pattern used in the hypothesis of the invoked colimit lemma at `sites.tex:3971-3976`.

Smallest correction: change only the codomain in the second arrow, from `b : k \to i` to `b : k \to j`.

### `SITES-022` — ACCEPTED

Source evidence: the Situation defines the index category \(\mathcal I\) at `sites.tex:3773`; the surrounding construction quantifies its objects as \(i\in\Ob(\mathcal I)\) at 3774, 3970, and 3978. Nevertheless, the colimits at 4028, 4035, and 4040 use \(i\in I\). There is no local definition of plain \(I\) in this Situation or these lemmas.

Adverse evidence against the frozen text: plain \(I\) and calligraphic \(\mathcal I\) are distinct TeX symbols. Because the displayed colimits require the objects and transition arrows of the already declared category \(\mathcal I\), an undeclared set \(I\) does not supply the stated diagram.

Counter-consideration: a reader may guess that \(I\) informally denotes \(\Ob(\mathcal I)\). The source itself does not state that abbreviation and repeatedly uses the explicit object notation, so the guess does not make the frozen formula formally self-contained.

Smallest correction: in all three colimit subscripts, replace `i \in I` by `i \in \Ob(\mathcal I)`.

### `SITES-023` — ACCEPTED

Source evidence: `sites.tex:3999-4008` assumes only a sheaf \(\mathcal F\) on \(\mathcal C\) and states

\[
\mathcal F=\mathop{\rm colim} f_i^{-1}f_{i,*}\mathcal F.
\]

The proof then writes \(f_i^{-1}\mathcal F_i\) at 4035 and 4040, although no \(\mathcal F_i\) is introduced in this lemma. At 4041 it evaluates \(f_{j,*}\mathcal F\), confirming the intended level sheaf.

Adverse evidence against the frozen text: the undefined \(\mathcal F_i\) makes the two displays formally unbound, and omitting \(f_{i,*}\) changes the diagram from the one in the lemma statement. To invoke Lemma `lemma-colimit`, the intended specialization is \(\mathcal F_i=f_{i,*}\mathcal F\); it must either be declared or expanded in the formula.

Smallest correction: expand both occurrences to `f_i^{-1}f_{i, *}\mathcal{F}`. This repairs the formulas without adding a separate definition.

### `SITES-024` — ACCEPTED

Source evidence: the lemma statement at `sites.tex:4388-4390` reads, as two sentences, “In the situation of Lemma … . For any presheaf … we have …”.

Adverse evidence against the frozen text: “In the situation of Lemma …” is a dependent prepositional phrase, not an independent English clause; the period strands it from the assertion it modifies.

Counter-consideration: the same standalone pattern occurs at `sites.tex:2580-2582` and `2595-2597`, and the mathematical scope is still understandable. Those parallels show a repeated house/source habit, but they do not supply a finite verb or turn the phrase at 4388 into a complete sentence. This verdict is therefore grammatical only and makes no claim of mathematical ambiguity.

Smallest correction: write “In the situation of Lemma `\ref{lemma-exact-cocontinuous}`, for any presheaf …” by changing the period to a comma and lowercasing `For`.

## Aggregate

- **ACCEPTED:** 11
- **REJECTED:** 0
- **DEFERRED:** 0
- **Total reviewed:** 11

The seven mathematical/type or binding defects are `SITES-015`, `SITES-016`, `SITES-017`, `SITES-020`, `SITES-021`, `SITES-022`, and `SITES-023`. `SITES-018` is a TeX identity-notation defect. `SITES-014`, `SITES-019`, and `SITES-024` are prose/grammar defects. Every verdict is resolved from the frozen `sites.tex`; none requires external authority.
