# Deterministic replay

Run `python regenerate_r33.py`, then `python verify_r33.py --write-review`, then `python verify_r33.py`.

The verifier replays all seven exact preimages in descending byte order, proves payload identity, checks the five alias pairs and two new rows, verifies manifest closure, and checks the pre-admission registry for stable-ID collisions.
