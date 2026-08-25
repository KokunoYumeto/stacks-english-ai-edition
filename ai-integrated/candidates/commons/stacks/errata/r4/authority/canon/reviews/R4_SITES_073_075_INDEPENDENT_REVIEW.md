# R4 independent review: SITES-073--075

Review date: 2026-08-22  
Scope: only SITES-073, SITES-074, and SITES-075  
Aggregate: **3 ACCEPTED, 0 REJECTED, 0 DEFERRED**

## Frozen inputs

| Input | Bytes | SHA-256 |
|---|---:|---|
| `ERRATA_R4_SUPPLEMENT_SITES_073_20260822.json` | 2,887 | `0e0050db4b05ae06d0b0fce2d54d6f1be90122f105cfc873998db75de065d4fb` |
| `ERRATA_R4_SUPPLEMENT_SITES_074_075_20260822.json` | 2,732 | `20e63c725fcf83435083be95bd948d82eb71dc570c6b7816737476f140f20d60` |
| frozen `sites.tex` at commit `a04446e57ec1fbc252a871afcec7752fb2807b14` | 424,197 | `07ae4690c2d8eb6873837d3d14a37f07408bb14f9e0be6077ed570c220b1845d` |

Both intake JSON files were read completely. The relevant definitions, results, and exact source contexts were reopened in the frozen authority. The producer's private `R4_SITES_073_COUNTEREXAMPLE_REPLAY.json` was not consulted; the construction and calculation below are independent.

## SITES-073 -- ACCEPTED

Locus: `sites.tex:8196-8223`, especially the claims at lines 8204 and 8222 that \(p_*\) commutes with coequalizers.

### Independent finite construction

Let \(\mathcal C\) have two objects \(0,1\), identities, exactly two distinct nonidentity arrows

\[
 a,b:0\longrightarrow 1,
\]

and no other arrows. Give \(\mathcal C\) the chaotic (indiscrete, coarsest) topology, so only isomorphism coverings are required. Let

\[
 u(U)=\operatorname{Hom}_{\mathcal C}(0,U).
\]

Then \(u(0)=\{\mathrm{id}_0\}\) and \(u(1)=\{a,b\}\).

This \(u\) really is a point of the site. Conditions (1) and (2) of `definition-point` hold for isomorphism coverings. More directly for condition (3), the neighbourhood category of this representable functor has initial object \((0,\mathrm{id}_0)\), so for every presheaf \(F\) its stalk is naturally

\[
 F_p\cong F(0).
\]

Every presheaf is a sheaf for the chaotic topology (`example-indiscrete`), and evaluation at \(0\) on the presheaf category preserves finite limits (indeed all limits and colimits). Thus the stalk functor is left exact and \(u\) defines the required point.

For a set \(E\), the frozen formula gives

\[
 (p_*E)(1)=\operatorname{Map}(u(1),E)=\operatorname{Map}(\{a,b\},E)\cong E^2.
\]

Take \(A=\{*\}\), \(B=\{0,1\}\), and parallel maps \(r,s:A\rightrightarrows B\) with \(r(*)=0\) and \(s(*)=1\). Their coequalizer is the singleton \(q:B\to Q=\{\bullet\}\). At object \(1\), the induced maps are

\[
 A^2=\{(*,*)\}\mathrel{\substack{\xrightarrow{r^2}\\[-2pt]\xrightarrow[s^2]{}}}B^2,
\qquad
 r^2(*,*)=(0,0),\quad s^2(*,*)=(1,1).
\]

Hence their coequalizer has exactly the three classes

\[
 \{(0,0),(1,1)\},\qquad \{(0,1)\},\qquad \{(1,0)\}.
\]

On the other hand, \((p_*Q)(1)=Q^2\) is a singleton. Therefore the canonical comparison at \(1\),

\[
 \operatorname{coeq}(p_*r,p_*s)(1)\longrightarrow
 p_*\bigl(\operatorname{coeq}(r,s)\bigr)(1),
\]

is the map from a three-element set to a one-element set and is not bijective.

### Why sheaf colimits do not change the calculation

In general, `lemma-colimit-sheaves` says that a sheaf colimit is the sheafification of the objectwise presheaf colimit. Here the topology was deliberately chosen so that every presheaf is already a sheaf. Consequently

\[
 \operatorname{Sh}(\mathcal C)=\operatorname{PSh}(\mathcal C),
\]

and colimits are computed objectwise (`section-limits-colimits-PSh`). Thus the three classes at \(1\) are the actual sheaf coequalizer; there is no sheafification collapse.

### Adverse readings and repair

Being a right adjoint explains preservation of limits, not general coequalizers. Some special points can have all \(u(U)\) of cardinality at most one, and every functor preserves split coequalizers, but neither fact rescues the universal, unqualified assertion in the lemma. The counterexample also leaves the separate surjection claim untouched.

The smallest safe source repair is to remove only the false property in its two occurrences:

- line 8204: delete `it commutes with coequalizers,`;
- lines 8221--8222: replace `transforms surjections into surjections and coequalizers into coequalizers` by `transforms surjections into surjections`.

Merely narrowing the statement to split coequalizers would be true for every functor but would add an unmotivated, categorically automatic property. Deletion is the cleaner minimal repair.

## SITES-074 -- ACCEPTED

Locus: `sites.tex:7693-7702`, line 7699.

The statement of `lemma-localize-morphism-compare` supplies one morphism of sites

\[
 f:\mathcal C\longrightarrow\mathcal D
\]

given by one continuous functor \(u\). The proof compares that supplied presentation of \(f\) with the possibly different choice of a morphism of sites used to present the same \(f\) in the proof of `lemma-localize-morphism-topoi`. Thus the phrase “the morphisms of sites given to us in the lemma” has no plural antecedent in the current lemma.

Adverse reading: the surrounding diagram contains several morphisms of topoi, and `lemma-localize-morphism` also constructs an induced \(f'\). But those are not multiple morphisms of sites *given to us* as hypotheses of this lemma; only \(f\) is supplied. They do not justify the plural.

Smallest repair: at line 7699 replace `morphisms` by `morphism`. This is editorial and does not change the mathematics.

## SITES-075 -- ACCEPTED

Locus: `sites.tex:8041-8048`, line 8047.

In “the pair of functors \((p_*,p^{-1})\) ... define a morphism of topoi,” the grammatical head of the subject is the singular noun “pair.” The parenthetical names its two members but does not replace that head with a coordinated plural subject.

Adverse reading: the two functors act together and may be regarded semantically as plural data. That does not override agreement with the explicit singular head “pair.”

Smallest repair: at line 8047 replace `define` by `defines`. This is editorial and does not change the mathematics.

## Classification table

| Candidate | Decision | Nature | Selected repair |
|---|---|---|---|
| SITES-073 | **ACCEPTED** | substantive false functoriality claim | delete both unqualified coequalizer claims |
| SITES-074 | **ACCEPTED** | editorial number agreement | `morphisms` -> `morphism` |
| SITES-075 | **ACCEPTED** | editorial subject--verb agreement | `define` -> `defines` |
