# Independent bounded review: TOPOLOGY-018--023

Reviewer task: `/root/r2_independent_replay` with two bounded adverse-review
children. Review was read-only; no Git operation or file edit was performed.

Authority: Stacks commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, `topology.tex`, 237,731 bytes,
SHA-256
`C6BAC8DCF8AD96DC47416BF34CB45BA4A10B894E40D67D3E1FA68D8EF0D9F872`.

## Outcomes

- **TOPOLOGY-018:** the proof uniquely requires
  `E = X \setminus (U \cap f^{-1}(V))`. Under the natural left-associated
  reading of the printed expression, the result can fail: on a two-point
  discrete space with the transposition map, the printed construction can give
  the empty set. Admit the unique proof-forced grouping correction.
- **TOPOLOGY-019:** `X' = beta(Y)` is only an ambient Stone--Cech cover. The
  proof later constructs the minimal extremally disconnected `E`, but the
  uniqueness paragraph silently reverts to `X'` and invokes nonexistent
  minimality of that ambient cover. Rebind the uniqueness proof to `E` (or
  explicitly replace `X'` by `E`) before admission.
- **TOPOLOGY-020:** `add more here.` is literal unfinished scaffold. Items
  (1)--(3) are valid; the smallest non-inventive correction is deletion of the
  empty fourth item. `Proof. Omitted.` is not itself false and is not changed.
- **TOPOLOGY-021:** the printed definition reverses refinement. Each nonempty
  `X_I` is contained in an irreducible component and therefore in a connected
  component; connected components are unions of the `X_I`, not conversely.
  Later source usage gives the same orientation. Admit an explicit named-
  partition definition.
- **TOPOLOGY-022:** with the printed right-coset representatives
  `G = union H g_i`, writing `g = h g_i` gives
  `g^{-1} H g = g_i^{-1} H g_i`. The printed intersection need not be normal.
  In `S_4`, take `H = Stab(1)` and right-coset representatives whose
  nonidentity members send `1` to `3`; the printed intersection is
  `Stab(1) intersect Stab(3) = {e,(2 4)}`, not normal in `S_4`. Preserve the
  stated right-coset convention and replace the intersection by
  `intersection g_i^{-1} H g_i`.
- **TOPOLOGY-023:** a diagram in `Top` may contain continuous arrows that are
  not group homomorphisms, so precomposition does not define the displayed
  transition maps on `Mor_TopGroup(G_i,H)`. `TopGroup` is the unique typed
  codomain.

All six may proceed to the R3 payload with the bounded corrections above. The
review does not certify the other R3 units or the eventual payload/build.
