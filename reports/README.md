# EGA findings channel

`findings.jsonl` is the sole return channel for suspected EGA source errors
found during Stacks comparison. It is append-only and may be empty.

Each nonblank line is one JSON object with exactly these required fields:

`stable_id`, `ega_locus`, `claim`, `suspected_error`, `authority_locator`,
`evidence`, `proposed_disposition`, `reporter`, and `utc`.

A row is a referral, not a correction. The EGA edition task checks direct
authority and alone decides whether to alter the diplomatic French,
corrected-source, or standalone English layers. Its response is later linked
through `ega/issues.csv` and a new append-only decision row.
