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
   `24861b306a34991c0da3d803f92d67e206c805da` was transferred byte-for-byte
   under `ai-integrated/`. The protected public history records that transfer
   as the linear import `c06400fc323abb62990f37563cc31e9ae93fbf8e`; the
   external cutoff remains provenance and is not asserted as a `main` ancestor.
4. Each admitted errata batch R1–R19 was independently materialized against
   the pinned upstream source and composed in registry order. The cumulative
   `derived.tex` projection is committed at source `1f204fb27ff418fd0e75cb35ac8dab5256037f15`,
   a direct linear successor of the registry import; the protected publication
   suffix contains no merge commits.
5. The independent `injectives.tex` correction was carried into the unified
   source.

The mathematical source therefore stays at the repository root while the
complete evidence and registry system remains browsable under
[`ai-integrated/`](ai-integrated/README.md).

## Branch preservation

The unified repository retains the pre-unification integration heads as
clearly named historical branches in addition to the integrated default
branch. Their presence is provenance, not a claim that they remain competing
editions. R20 and later registry work remains outside this R19 fixed point.
