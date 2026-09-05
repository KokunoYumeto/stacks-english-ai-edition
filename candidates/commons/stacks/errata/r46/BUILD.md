# Build contract

Run `pipeline_r46.py --materialize` for the source-only stage. Then invoke
`run-builds-with-mutex.ps1` with the frozen upstream source directory and four
new, absent task-local build/evidence directories. The wrapper owns
`Global\InterlanguageTeXSlotV1` for both deterministic candidate/authority
builds and their immediate replay checks.

Source materialization does not admit, compose, or publish the overlay. The
candidate remains append-only evidence until independent replay, page-complete
visual adjudication, manifest closure, fresh-checkout validation, and registrar
admission all pass.
