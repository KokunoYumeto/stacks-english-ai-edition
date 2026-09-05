# R46 finalization order

1. Run `python finalize_r46.py mechanical`.
2. Run `python finalize_r46.py prepare`.
3. Run `python independent-final-review-r46.py`.
4. Run `python finalize_r46.py seal`.
5. Run `python check-manifest.py` and a deterministic replay of the sealed tree.

Registry admission, public readback, and generated-source composition are
separate append-only stages.

