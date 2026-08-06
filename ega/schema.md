# Scaffold schema

## Stable identity

Source IDs use `ega.<volume>.<source-number>[.<subitem>]`. They identify the
mathematical source unit, not a mutable line or PDF coordinate. Page, TeX,
hash, and language locators attach as versioned evidence.

The `volume` field is the logical EGA volume determined from the stable label
or source-file role. `printed_page` is an independent witness locator and may
name another volume when a later erratum supplies text for an earlier volume.
It must never reclassify the semantic unit.

Topic IDs use `ega-topic-<slug>`. Local Stacks labels may be recorded as
evidence, but this branch never writes or claims an official Stacks tag.

Decision, issue, and feedback IDs use zero-padded `D`, `I`, and `F` prefixes.
Rows are append-only. A correction names the earlier row in `supersedes`; it
does not rewrite history.

## Authority states

- `english_discovery`: complete English text supports search and candidates.
- `french_admitted`: the diplomatic French unit has a sealed authority receipt.
- `source_corrected`: a separate justified correction exists.
- `source_disputed`: the source claim or reading remains fail-closed.

English discovery may create candidates at any point. Only `french_admitted`
or an exact published authority can support a canonical source claim.

## Review states

- `unreviewed`: search topic or source unit only.
- `candidate`: plausible Stacks correspondence with recorded evidence.
- `reviewed_existing`: equivalent, stronger, weaker, or split treatment found.
- `reviewed_gap`: bounded gap established by mathematical review.
- `integrated_local`: independent Stacks-convention exposition exists locally.
- `built`: every affected chapter passes its bounded build gate.
- `remote_checkpoint`: exact branch bytes are pushed and remotely verified.
- `upstream_feedback`: upstream comment is recorded and dispositioned.
- `upstream_accepted`: upstream merged or explicitly accepted the material.

Build success never promotes mathematical review state by itself.

`tmap.csv` records bounded reviewed correspondences. Its granularity and
coverage columns are part of the claim: a `source_subsection_to_stacks_section`
row with `topical_overlap_only` establishes only a topic-level bridge. It does
not establish theorem equivalence or complete coverage of the source
subsection. Existing official tags in that table are read back from the fixed
upstream `tags/tags`; the scaffold assigns no tags.

## Feedback integration

`fb.csv` records the immutable URL, source, date, affected stable ID, and
disposition of each upstream comment. Any resulting change receives a new
decision row. Rejected or deferred feedback remains visible. This lets the
scaffold absorb maintainer guidance without rekeying the corpus graph.

## Promotion gate

A source unit can modify a Stacks chapter only when it has:

1. stable source identity and exact authority evidence;
2. an explicit correspondence state (existing, stronger, weaker, split, gap,
   historical, false, or unsupported);
3. a reviewed mathematical rationale and dependencies;
4. append-only issue and correction closure;
5. bounded build and rendered-page checks for affected output.
