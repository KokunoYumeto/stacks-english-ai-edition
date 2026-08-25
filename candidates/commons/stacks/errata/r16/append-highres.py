from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "builds" / "homology.pdf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-root", type=Path, required=True)
    parser.add_argument("pages", type=int, nargs="+")
    args = parser.parse_args()

    render_root = args.render_root.resolve()
    manifest_path = render_root / "render-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["pdfs"]["homology"]["pdf_sha256"] != sha256(PDF):
        raise AssertionError("render manifest is bound to a different PDF")
    highres_root = render_root / "highres"
    rows = {row["page"]: row for row in manifest["high_resolution"]["renders"]}
    for page in sorted(set(args.pages)):
        output = highres_root / f"homology_p{page}.png"
        if output.exists() or page in rows:
            raise FileExistsError(f"refusing to overwrite page {page}")
        scratch = highres_root / f"append-{page}"
        scratch.mkdir()
        subprocess.run(
            ["pdftoppm", "-r", "180", "-f", str(page), "-l", str(page), "-png", str(PDF), str(scratch / "page")],
            check=True,
        )
        generated = list(scratch.glob("page-*.png"))
        if len(generated) != 1:
            raise AssertionError(f"unexpected render count for page {page}")
        generated[0].replace(output)
        scratch.rmdir()
        rows[page] = {"page": page, "file": output.name, "bytes": output.stat().st_size, "sha256": sha256(output)}
    manifest["high_resolution"]["renders"] = [rows[key] for key in sorted(rows)]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"appended": sorted(set(args.pages)), "manifest_sha256": sha256(manifest_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
