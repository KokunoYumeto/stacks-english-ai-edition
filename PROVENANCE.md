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
The current fixed-point build is bound to source
`7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`.

## Branch preservation

The unified repository retains the pre-unification integration heads as
clearly named historical branches in addition to the integrated default
branch. Their presence is provenance, not a claim that they remain competing
editions. The live Verdier release candidate advances the integrated cutoff to
22 overlays and 559 stable IDs at `60f1d97e`. Later R22 and R23 admissions
affect only `more-algebra.tex` and remain queued, in registry order, outside
this release.
