# Integration status

Status date: **2026-08-26**

Pinned official upstream: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This dashboard summarizes the live integrated tree. Detailed evidence remains
in each corpus dossier and in the machine-readable registry.

## Source integrations

| Workstream | Current state | Bounded claim |
| --- | --- | --- |
| FAC | Integrated | The full 661-target review is dispositioned. The dossier records 37 new theorem or lemma statements, seven source corrections, 27 corrected Stacks defects, successful validators, builds, and targeted visual inspection. |
| Tôhoku | Integrated through r71 | The sealed successor records 1,066 decisions, 679 decided units, 33 resolved source issues, and zero remaining gap-class dispositions. This does not convert the dossier's explicit nonclaims into a claim of upstream acceptance or an official release. |
| GAGA | Integrated through r3 | All 126 source units are classified; all 79 substantive units have reviewed decisions. The 23-page English chapter and deterministic mapping replay pass. The three previously dangling cross-reference targets are closed. |
| FGA | Integrated and normalized | The combined source contains the normalized FGA chapter and its post-merge dossier. The closure covers 1,253 units, 1,612 term links, and 579 append-only decisions; the recorded fixed-point Moduli build is 83 pages. |
| EGA | Active | Direct-French semantic review reaches EGA I 6.1.13. The active graph contains 1,059 edges across 355 generated units; the next semantic cursor is EGA I 6.2.1. |

## Errata state

- Registered and composed: **R1–R21**.
- Registered batches: **21**.
- Stable correction IDs represented: **547**. The highest identifier is
  `MC-STK-ERR-0914`; the sequence contains intentional gaps, so this is not a
  claim of 914 corrections.
- Exact v2 operations represented: **591**. R20–R21 add 43 operations; the
  baseline-aware R18–R21 replay contains 120 operations in total.
- Frozen external registry cutoff:
  `13ca6aaaca454f5930c4885c93f427e30cf21959`. The integrated linear history
  uses registry import `e3b28d7d7068eb45d3348a57e201c49044826e86`
  and composition source `ef467614041d569e56a6c1758b8fe74b51d99f4a`.
  The external cutoff remains explicit provenance rather than a false ancestor
  claim; admissions after this exact cutoff are outside the current fixed point.
- R20 is composed into `derived.tex`. R21 is operation-replayed onto the
  verified cumulative `simplicial.tex`, preserving earlier AI-integrated
  additions outside its manifest-bound operations.
- The independent `injectives.tex` parenthesis correction is included in the
  live source and retained in Git history.

The authoritative registry is
[`ai-integrated/registry/overlays.json`](ai-integrated/registry/overlays.json).
Candidate manifests, source maps, adjudication, replay evidence, and rejected
proposals remain under
[`ai-integrated/candidates/commons/stacks/errata/`](ai-integrated/candidates/commons/stacks/errata/).

## Validation state

The repository integrity gate checks the pinned authority, protected linear
ancestry, all 21 registry entries and 547 stable IDs, all 591 exact v2
operations, exact manifest/source-map/payload/review joins, the baseline-aware
120-operation R18–R21 replay, both composed source identities, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R21 unified-tree gate built all 22 required chapters (2,342 pages
and 24,385,554 PDF bytes) to a global PDF fixed point on sweep four. It is bound
to tooling/build source `8e9520aa30e0d538e71e787850bac91f5ddb35f9`,
tree `c63e22c9ec1fef6d5af3820f5f83bd316e51ae62`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all
202 review pages and the affected-page superset. The exact artifact inventory is
in the [current fixed-point build receipt](validation/unified-fixed-point-2026-08-25-r19.json).

The [independent linked-worktree rebuild gate](validation/reproducibility-r21.json) is
**PASS**. Both builds use the same commit, tree, builder, and fixed-point sweep;
all 22 `{stem, pages, bytes, sha256}` artifact tuples are exactly equal. The R21
content fixed point is public at `780f48fafbb46dc1057bf8fdcd339693fb44d6bf`;
anonymous byte readback is **PASS** for the sources, registry, receipts,
documentation, tooling, and R20/R21 manifests. Stable receipt filenames are
retained for automation compatibility; their JSON scope and source identities
are authoritative.
