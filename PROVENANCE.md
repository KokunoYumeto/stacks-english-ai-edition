# Provenance and preserved histories

## Canonical upstream

The canonical external source is the official
[Stacks Project repository](https://github.com/stacks/stacks-project). This
unofficial derivative is pinned to upstream commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, tree
`3feeb703b931a6e7259782c10e7d1575adc83e5e`.

The upstream source and this modified source retain the GNU Free Documentation
License 1.2 recorded in [COPYING](COPYING). Nothing in this repository implies
upstream review or endorsement.

## Pre-unification repositories

Two public repositories previously split the work by workflow rather than by
mathematical product:

| Repository | Pre-unification role | Captured refs |
| --- | --- | --- |
| [`KokunoYumeto/stacks-project`](https://github.com/KokunoYumeto/stacks-project) | Full Stacks source plus FAC, Tôhoku, GAGA, FGA, and EGA source branches | `master` plus five `codex/*` integration branches |
| [`KokunoYumeto/unofficial-ai-integrated-stacks-project`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project) | Errata candidates, overlay registry, schemas, and replay evidence | `main` and `codex/stacks-cjk-canon` |

The split is now resolved in favor of one integrated public edition.
The former `stacks-project` fork is retained publicly as a read-only archive;
its six branch heads were verified unchanged after archival. Active integrated
development and publication now use this repository's protected `main` branch.

## Frozen full-history copies

Before unification, complete remote mirrors were fetched, checked with
`git fsck --full`, exported as Git bundles, and verified with
`git bundle verify`. GitHub reported no tags, release assets, Git LFS payloads,
or submodules in either input repository.

| Original repository | Bundle bytes | SHA-256 |
| --- | ---: | --- |
| `KokunoYumeto/stacks-project` | 241,336,664 | `0DFA9F785757BE07D755DB315947A90ECB18DA4152666CAFEAE4ADDDB47FF74D` |
| `KokunoYumeto/unofficial-ai-integrated-stacks-project` | 14,610,301 | `B048584F27D4A9482FC9040D4946024F3584FCF71C66DA245D1B879AF912E9A3` |

The preservation release is
[`pre-unification-snapshots-2026-08-25`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/pre-unification-snapshots-2026-08-25).
The exact validation, preservation, publication, and public-readback identities
are recorded in the machine-readable
[`release receipt`](validation/unification-release-2026-08-25.json).

## Unification method

The histories were combined without flattening either input:

1. The source union at `ad58625f60e6816905ff217d21d91b07b2722fcf`
   supplied the FAC/Tôhoku/GAGA/FGA and notation-normalized Stacks tree.
2. EGA scaffold and export history through
   `91df7f1c96bd4973264c29b0e121253a05d1d361` was merged into that source.
3. The complete registry content through the frozen external cutoff
   `13ca6aaaca454f5930c4885c93f427e30cf21959` was transferred byte-for-byte
   under `ai-integrated/`. The integrated linear history records that transfer
   as import `e3b28d7d7068eb45d3348a57e201c49044826e86`; the external cutoff
   remains provenance and is not asserted as a `main` ancestor.
4. Each admitted errata batch R1–R21 is manifest-bound and composed in registry
   order. R20 extends the cumulative `derived.tex` projection. R21 is replayed
   onto the verified cumulative `simplicial.tex`, preserving earlier
   AI-integrated additions outside its operations. The resulting source is
   committed at `ef467614041d569e56a6c1758b8fe74b51d99f4a`, tree
   `b181820f096c3b78b6608429e477aaa8acd614c4`, as a direct linear successor
   of the registry import.
5. The independent `injectives.tex` correction was carried into the unified
   source.
6. The separately admitted Verdier II.1.2.13 contribution was composed through
   its unique unchanged context in cumulative `derived.tex`, preserving the
   R1–R21 source and claiming no official Stacks tag or upstream endorsement.
7. Registry content through R23 cutoff
   `49fc23ab2f3d94cc98f27bc0f315fb0da6f2c98a`, tree
   `a67a8529b853da8834502456e8ca75afe71aa78c`, was imported into the linear
   integrated history at `806ed1d11943f5a66b17b75f9fddccd61f58b62b`.
   R22 and R23 were then composed in registry order by replaying 106
   manifest-bound operations onto cumulative `more-algebra.tex`. The resulting
   source commit is `3a1100a79abc76315592711c9f2c86ad21b5f6a9`, tree
   `28980ba358cadddecc67d5013c7a9b624fee6305`.

The mathematical source therefore stays at the repository root while the
complete evidence and registry system remains browsable under
[`ai-integrated/`](ai-integrated/README.md).

The verified R21 build is separately bound to tooling/build source
`8e9520aa30e0d538e71e787850bac91f5ddb35f9`, tree
`c63e22c9ec1fef6d5af3820f5f83bd316e51ae62`. It produced 22 readable PDFs
(2,342 pages; 24,385,554 bytes) at fixed-point sweep four, with zero recorded
fatal or listed serious diagnostics. Visual QA passed all 202 review pages and
the affected-page superset. A separate linked-worktree reproduction also passed:
both builds use the same commit, tree, builder, and sweep, and all 22 artifact
identity tuples are exactly equal. The resulting R21 content fixed point is
public at `780f48fafbb46dc1057bf8fdcd339693fb44d6bf`; anonymous readback matched
the recorded public bytes and hashes.

The next separately admitted contribution is the independently written Verdier
II.1.2.13 overlay `stacks-verdier-a04446e-1-2-13-r1`, frozen at registry commit
`60f1d97ecbd376ff7a91298d17e1f162b9996c3a`. It adds one 2,339-byte
manifest-bound insertion to cumulative `derived.tex` through a unique unchanged
803-byte context. Prefix and suffix bytes remain unchanged, and the proposed
local label occurs exactly once. The candidate and source addition claim no
official Stacks tag, affiliation, review, approval, or upstream endorsement.
The historical Verdier fixed-point build is bound to source
`7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`.

The current R22/R23 fixed-point build is bound to source
`1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`. It preserves the Verdier
`derived.tex`, cumulative R21 `simplicial.tex`, and independent `injectives.tex`
identities while advancing `more-algebra.tex` through 93 new correction IDs and
106 operations. Two independent builds produced exactly matching identities
for all 22 PDFs: 2,343 pages, 24,389,773 bytes, and a global fixed point on
sweep four. Visual QA covers all 406 pages of `more-algebra.pdf` and 63
high-resolution correction-locus pages.

## Branch preservation

The unified repository retains the pre-unification integration heads as
clearly named historical branches in addition to the integrated default
branch. Their presence is provenance, not a claim that they remain competing
editions. The published Verdier content release at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0` remains historical evidence for
the 22-overlay / 559-ID cutoff at `60f1d97e`. The current validated composition
advances the repository state to 24 overlays and 652 stable IDs at `49fc23ab`;
R22 and R23 affect only `more-algebra.tex`. R24 remains an active intake lease,
and the French `MORE-ALGEBRA-L-001..029` packet remains unadmitted.
