# DESCENT source and authority defects

The translation follows the pinned source byte-for-byte for protected TeX and
mathematics, while rendering the intended mathematical meaning of the following
plain-prose defects.

1. Authority manifest SHA-256: the supplied value
   `49483B3BCB36427A607A8227F4EA67730FCD1EECCB8E992CA61915ACE3B31D`
   is malformed (62 hexadecimal characters). The named source matches the
   supplied 353760-byte and 9456-line inventory. Its valid SHA-256 is
   `49483B3BCB36427A607A8227F4EA67730FCDDF1EECCB8E992CA61915ACE3B31D`.
2. Canonical line 162 says “the unique descent on … datum”; the intended noun
   phrase is “the unique descent datum on …”. The French draft renders that
   intended phrase without changing any TeX token.
3. Canonical line 3970 says “Since we've assume (2)”; the intended tense is
   “Since we've assumed (2)”. The French draft renders the intended statement.
4. Canonical line 4011 says “Thus we see property (1) lemma holds for the family
   $g_i$”; the phrase is missing “of the” before “lemma”. The French draft
   renders the intended assertion without altering its mathematical tokens.
5. Canonical lines 4061--4063 say “Assume the equivalent assumption of Lemma
   ... hold”; subject--verb agreement requires “holds”. The French draft
   renders the evident intended hypothesis without altering any reference or
   mathematical token.
6. Canonical line 4231 says “a collection of morphism” where the indexed
   family requires the plural “morphisms”. The French draft uses the intended
   plural without changing the indexed objects.
7. Canonical lines 4324--4325 say “an $R$-algebra maps”; the construction
   requires the plural noun phrase “$R$-algebra maps”. The French draft renders
   this as a plural family of homomorphisms and preserves both maps exactly.
8. Canonical lines 5337--5343 quantify over six topologies
   `fpqc, fppf, syntomic, smooth, \etale, Zariski`, but the corresponding
   list of base-change morphisms has only five entries: flat; flat and locally
   of finite presentation; syntomic; \'etale; open immersion. The smooth case
   is omitted between syntomic and \'etale. The likely bounded correction is
   to insert `resp.\ smooth,` before `resp.\ \'etale`. The French translation
   preserves the pinned omission pending canonical adjudication.
9. Canonical line 5775, inside the proof for morphisms locally of finite
   presentation, says “Being locally of finite type is Zariski local on the
   base”, while the cited characterization and the property being proved are
   both locally of finite presentation. The intended phrase is “Being locally
   of finite presentation”. The French translation renders that intended
   phrase without changing the reference or mathematical tokens.
10. Canonical line 6475 places a generic point in
    `$X \times_S X$`, although the lemma has only introduced
    `$f : X \to Y$`, the diagonal at line 6471 has target
    `$X \times_Y X$`, and the projection at line 6477 again has source
    `$X \times_Y X$`. Both occurrences of the undefined base `$S$` at line
    6475 should therefore be `$Y$`. The French translation preserves the
    pinned mathematical tokens pending canonical adjudication.
11. Canonical line 6554 says `$X_i \to S$` is separated, but the hypothesis
    is that `$\mathcal L_i$` is ample on `$X_i/S_i$`, the cited result applies
    to `$X_i \to S_i$`, and descent in the next line requires the base-changed
    morphisms `$X_i \to S_i$` to be separated. The subscript `$i$` is missing
    from `$S$`. The French translation preserves the pinned mathematical token
    pending canonical adjudication.
12. Canonical lines 6571--6574 call `$\psi_d$` a natural map “of
    `$\mathcal O_X$`” before saying that its pullbacks are maps of
    `$\mathcal O_{X_i}$`-modules. The first phrase is grammatically and
    mathematically missing “-modules”; it should read “of
    `$\mathcal O_X$`-modules”. The French translation supplies the intended
    reader-facing noun without altering the pinned mathematical token.
13. Canonical lines 6658--6664 quantify over six topologies
    `fpqc, fppf, syntomic, smooth, \etale, Zariski`, but enumerate only five
    corresponding kinds of precomposition morphisms: flat; flat and locally
    of finite presentation; syntomic; \'etale; open immersion. As in the
    independently recorded omission at lines 5337--5343, the smooth case is
    missing between syntomic and \'etale. The likely bounded correction is to
    insert `resp.\ smooth,`. The French translation preserves the pinned
    omission pending canonical adjudication.
14. Canonical line 6790 begins “Then property” where the grammar and lemma
    structure require “The property”. The French translation renders the
    intended article without changing any mathematical token.
15. Canonical line 6876 defines `$f_i : X_i \to X$` as “the compositions”,
    but the only relevant composites are `$X_i \to X \to Y$`, and the proof
    immediately reasons about their universal openness as morphisms to `$Y$`.
    Thus the codomain in the displayed inline declaration should be `$Y$`.
    The French translation preserves the pinned `$X$` pending canonical
    adjudication.
16. Canonical line 7081 writes `$f(x_i) \leadsto y_i$`, although
    `$x_i \in X_i$`, `$f_i : X_i \to Y_i$` is the base change, and `$f$`
    has domain `$X$`. The specialization should begin with `$f_i(x_i)$`;
    line 7082 then correctly compares its images using `$h_i$` and `$g_i$`.
    The French translation preserves the pinned mathematical token pending
    canonical adjudication.
17. Canonical line 7105 has the same domain error in the source-locality
    half: after defining `$f_i : X_i \to Y$` as `$f \circ h_i$`, it writes
    `$f(x_i) \leadsto y$` for `$x_i \in X_i$`. This should be
    `$f_i(x_i) \leadsto y$`; the next sentence explicitly uses
    `$f(h_i(x_i))`. The French translation preserves the pinned token pending
    canonical adjudication.
18. Canonical line 7132 says “let `$a, b$` the obvious map”. It is missing
    both the verb “be” and plural agreement: “let `$a, b$` be the obvious
    maps”. The French translation renders the evident intended plural phrase
    without changing either morphism token.
19. Canonical line 7292 says “(a) equivalent to (g)”. The predicate is missing
    its copula and should read “(a) is equivalent to (g)”. The French
    translation supplies the evident copula without changing any formal token.
20. Canonical line 7481 claims that
    `$\{X \to X \times_Z Y, X' \to X \times_Y Z\}$` is an étale covering.
    The second codomain is ill-typed: there is no map `$Z \to Y$`, while the
    diagram at lines 7463--7472 identifies both open-and-closed pieces inside
    `$X \times_Z Y$`. The second fibre product should therefore also be
    `$X \times_Z Y$`. The French translation preserves the pinned
    mathematical token pending canonical adjudication.
21. Canonical line 7511 says “locally finite type”. The standard English
    property and the cited lemma both require “locally of finite type”. The
    French translation uses the established term « localement de type fini ».
22. Canonical line 7609 writes `$f'_{U'} : U' \to Y'$`, whereas line 7606 and
    the proof require the restriction `$f'|_{U'} : U' \to Y'$`. The French
    translation preserves the pinned mathematical token pending canonical
    adjudication.
23. Canonical line 7622 writes `$g'|_U' : U' \to X$`; the intended restriction
    notation is `$g'|_{U'} : U' \to X$`. The French translation preserves the
    pinned mathematical token pending canonical adjudication.
24. Canonical line 7632 says “denote `$T_{i,j,d}$` the automorphism”; the
    construction is missing “by”. The French translation uses the idiomatic
    « notons » without changing the automorphism symbol.
25. Canonical line 7652 says that one of `$x_1, \ldots, x_n$` is
    transcendental, although the chosen point at line 7650 is
    `$\xi=(\xi_1,\ldots,\xi_n)$` and the proof immediately renumbers
    `$\xi_n$`. The coordinates should be `$\xi_1, \ldots, \xi_n$`. The French
    translation preserves the pinned symbols pending canonical adjudication.
26. Canonical line 7712 says “`$g$` is smooth `$y'$`”; it is missing “at”. The
    French translation supplies the intended relation « lisse en `$y'$ ».
27. Canonical lines 7718--7720 use the wrong point twice in the étale-source
    reduction. They say `$x \in W(f)$` iff the image of `$x$` in
    `$X\times_Y Y'$` belongs to the pulled-back open, but `$x$` need not have a
    chosen lift there. The argument and the stated equivalence require
    `$x' \in W(f')$` and the image of `$x'$`. The French translation preserves
    the pinned mathematical tokens pending canonical adjudication.
28. Canonical line 7779 repeats the grammatical omission at line 7632:
    “denote `$T_{i,j,d}$` the automorphism” is missing “by”. The French
    translation again uses « notons » without changing the symbol.
29. Canonical line 7814 uses an undefined `$W$` in
    `$T_p^{-1}(W)\cap\mathbf A_x^n=W\cap\mathbf A_x^n$`. The open used
    throughout this proof is `$W(f_n)$`; no abbreviation `$W$` is introduced.
    Both occurrences should therefore be `$W(f_n)$`. The French translation
    preserves the pinned display pending canonical adjudication.
30. Canonical line 7896 says “Let `$Q$` be the associated property”, although
    the preceding lemma defines that property as `$\mathcal{Q}$` at lines
    7856--7865 and item (2) of the same statement again calls it
    `$\mathcal{Q}$` at line 7904. The bare `$Q$` should therefore be
    `$\mathcal{Q}$`. The French translation preserves the pinned mathematical
    token pending canonical adjudication.
31. Canonical line 8051 writes `$\text{trdeg}_{\kappa(v)} \kappa(u) = \text{trdeg}_{\kappa(v')} \kappa(u)$`.
    The right-hand expression is ill-typed in the displayed square: the
    comparison induced by the finite separable extensions at lines 8048--8049
    requires `$\text{trdeg}_{\kappa(v')} \kappa(u')$`. The prime is missing
    from the final `$u$`. The French translation preserves the pinned display
    pending canonical adjudication.
32. Canonical line 8141 says “This because” where the sentence requires
    “This is because”. The French translation renders the evident intended
    connection as « En effet » without altering either fibre-product identity.
33. Canonical line 8362 calls `$(Y_j, \varphi_{jj'})$` a descent datum
    relative to `$\{V_j \to S'\}$`, although line 8355 defines the family as
    `$\mathcal{V} = \{V_j \to S\}_{j \in J}$`. The base in line 8362
    should be `$S$`, not `$S'$`. The French translation preserves the pinned
    mathematical token pending canonical adjudication.
34. Canonical line 8370 says that the pulled-back, `$i$`-indexed system
    `(g_i^*Y_{\alpha(i)}, (g_i \times g_{i'})^*
    \varphi_{\alpha(i)\alpha(i')})` is a descent datum relative to
    `$\mathcal{V}$`. Since it lives over the family `$\mathcal{U}$`, the
    final symbol must be `$\mathcal{U}$`; item (2) consequently defines the
    change-of-base functor from descent data relative to `$\mathcal{V}$` to
    those relative to `$\mathcal{U}$`. The French translation preserves the
    pinned symbol pending canonical adjudication.
35. Canonical line 8423 says “denote `$(X \times_S U, can)$` this descent
    datum”. The construction is missing “by”. The French translation uses the
    idiomatic « nous notons cette donnée de descente » without changing the
    displayed object.
36. Canonical line 8453 repeats the same omission in “We denote this descent
    datum `$(X_i \times_S U, can)$`”. The French translation again uses the
    idiomatic « nous notons » without changing the indexed object.
37. Canonical line 8472 titles the section “Fully faithfulness”. The standard
    noun phrase is “Full faithfulness”. The French title uses « Pleine
    fidélité ».
38. Canonical lines 8708 and 8727 say that the first morphism in
    `$X \to X \times_S X' \to X'$` “has a section”. In fact that graph
    morphism is itself a section of the first projection (equivalently, it has
    a retraction). The French translation states the correct categorical
    direction without altering the factorization.
39. Canonical lines 8718--8719 assume that `$\{X \to S\}$` is an fpqc
    covering, but the parenthetical example says “if `$f$` is surjective,
    flat and quasi-compact”. Those properties of `$f : X \to X'$` do not imply
    that `$X \to S$` is fpqc; the parenthetical should refer to `$X \to S$`.
    The French translation preserves the pinned `$f$` pending canonical
    adjudication.
40. Canonical lines 8765--8766 define the map on the `$i$`th component using
    `$g_{\alpha(i)}$`. The family of morphisms is indexed by `$i \in I$`,
    whereas `$\alpha(i) \in J$`; the component map must be `$g_i$`. The French
    translation preserves the pinned token pending canonical adjudication.
41. Canonical line 8830 says “The functor is faithful and fully faithful”.
    The first adjective is redundant; the intended statement is simply “The
    functor is fully faithful”. The French translation remains diplomatic and
    retains both assertions.
42. Canonical lines 8955--8956 say “is a glueing data”. The singular article
    requires “is a glueing datum” (or the plural construction “form glueing
    data”). The French translation uses the singular « une donnée de
    recollement ».
43. Canonical line 8976 says “a fpqc-covering”. Since the initialism begins
    with a vowel sound, standard English requires “an fpqc-covering”. The
    French sentence avoids the article defect.
44. Canonical line 8986 says “it is sometime the case”. The adverb required by
    the sentence is “sometimes”. The French translation renders the intended
    frequency idiomatically.
45. Canonical line 9060 uses the noun “pullback” as a verb in “if we pullback
    the descent datum”. Standard usage requires “pull back”. The French
    translation uses « effectuer le changement de base ».
46. Canonical line 9125 says that the local isomorphisms are compatible with
    restriction to smaller affine opens in `$X$`. The schemes `$X_V$` are
    indexed by affine opens `$V \subset S$`, and the preceding compatibility
    is for `$V'' \subset V' \subset V$` in `$S$`; the final symbol should be
    `$S$`, not `$X$`. The French translation preserves the pinned `$X$`
    pending canonical adjudication.
47. Canonical line 9395 says “For each `$i$` denote `$F_i$` the sheaf
    `$h_{X_i}$`”. The construction is missing “by” after “denote”. The French
    translation uses the idiomatic « notons `$F_i$` le faisceau `$h_{X_i}$` »
    without changing any indexed object.

Authorial warnings and deliberately omitted proofs (including the notes at
canonical lines 377, 3087, 3774, 3961, 4301, and 8158) are content, not defects;
they remain present and are translated normally.
