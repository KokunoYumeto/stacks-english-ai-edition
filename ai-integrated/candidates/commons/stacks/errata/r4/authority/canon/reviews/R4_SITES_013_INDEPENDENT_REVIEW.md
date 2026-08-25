# R4 independent review — SITES-013

Date: 2026-08-22  
Disposition: **ACCEPTED**

## Frozen inputs independently verified

- Authority: `upstream/src/stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14/sites.tex`
  - 424,197 bytes
  - SHA-256 `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
- Intake: `canon/control/ERRATA_R4_SUPPLEMENT_SITES_013_20260822.json`
  - 2,548 bytes
  - SHA-256 `D5C4663F9183AE4EC46FF008E582C88220A842A622D1983D182E3C89638A24A9`
- Reviewed authority locus: `sites.tex:2155-2224`, with the claimed defect at lines 2218-2221.

Both recomputed identities exactly match the frozen intake. This review used the authority bytes and intake above, not a conversation summary.

## Claim reviewed

At lines 2217-2221, the proof constructs unique sections
`t_i in F(U_i)` mapping to `s_i in G(U_i)` and must show that the
pullbacks of `t_i` and `t_j` to every `U_{ijk}` agree. The printed
reason ends by saying that agreement is known for `t_i` and `t_j`.
That is the very conclusion being proved. The intake proposes replacing
that final pair by `s_i` and `s_j`.

## Independent proof

Write the given presheaf map as
`eta : F -> G`. Lines 2184-2187 define `B` so that, for every object
`V in B`, the component

`eta_V : F(V) -> G(V)`

is bijective. After the two refinements at lines 2203-2214, both
`U_i` and every `U_{ijk}` lie in `B`. Consequently:

1. Bijectivity of `eta_{U_i}` gives the unique lift
   `t_i in F(U_i)` with `eta_{U_i}(t_i) = s_i`, as stated at lines
   2215-2217.
2. Let `p_i : U_{ijk} -> U_i` and `p_j : U_{ijk} -> U_j` be the
   relevant projections/refinement maps. Naturality of the presheaf
   map gives

   `eta_{U_{ijk}}(p_i^* t_i) = p_i^* eta_{U_i}(t_i) = p_i^* s_i`

   and likewise

   `eta_{U_{ijk}}(p_j^* t_j) = p_j^* s_j`.
3. The agreement furnished at lines 2199-2201, and preserved after
   pulling back to the refinements introduced at lines 2203-2214, is

   `p_i^* s_i = p_j^* s_j` in `G(U_{ijk})`.
4. Hence the two elements `p_i^* t_i` and `p_j^* t_j` have the same
   image under `eta_{U_{ijk}}`. Because `U_{ijk} in B`, this component
   is bijective and therefore injective. Thus

   `p_i^* t_i = p_j^* t_j` in `F(U_{ijk})`.

This is exactly the compatibility required to invoke
`lemma-sections-sheafification` at lines 2222-2223.

## Adverse-reading check

- The phrase “we have the agreement for `t_i` and `t_j`” cannot point
  to an earlier established fact: the `t_i` are introduced only at
  line 2217, and their compatibility is the assertion begun at line
  2218.
- The repeated-refinement sentence at lines 2212-2214 establishes that
  the objects `U_{ijk}` belong to `B`; it does not independently prove
  compatibility of the newly constructed lifts.
- Replacing the final names by `s_i` and `s_j` does not require an
  additional mathematical hypothesis. Naturality is part of being a
  map of presheaves, and membership of `U_{ijk}` in `B` supplies the
  injectivity used above.
- A more explicit rewrite could mention equal images and injectivity,
  but it would be editorially larger. The proposed replacement is the
  smallest correction that changes the circular premise into the
  actual known premise.

## Disposition and exact repair

**ACCEPTED.** In `sites.tex:2221`, replace only the final occurrence

`for $t_i$ and $t_j$`

with

`for $s_i$ and $s_j$`.

The resulting sentence is logically valid by naturality and the
injectivity of `F(U_{ijk}) -> G(U_{ijk})`. No authority, translation,
candidate payload, or other control file was edited by this review.
