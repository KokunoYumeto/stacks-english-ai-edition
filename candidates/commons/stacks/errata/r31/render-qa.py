from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "candidate.config.json").read_text(encoding="utf-8"))
if len(CONFIG["stems"]) != 1:
    raise AssertionError("R31 rendering requires exactly one configured stem")
STEM = next(iter(CONFIG["stems"]))
PDF = ROOT / "builds" / f"{STEM}.pdf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def render_pages(pdf: Path, destination: Path, dpi: int, first: int | None = None, last: int | None = None) -> None:
    command = ["pdftoppm", "-r", str(dpi), "-png"]
    if first is not None:
        command.extend(["-f", str(first)])
    if last is not None:
        command.extend(["-l", str(last)])
    command.extend([str(pdf), str(destination / "page")])
    subprocess.run(command, check=True)


def configured_high_res_pages() -> list[int]:
    visual = CONFIG.get("visual_qa", {})
    page_map_path = ROOT / visual.get("source_page_map_path", "")
    if not page_map_path.is_file():
        raise AssertionError("derive-visual-pages.py must seal the source-page map before rendering")
    page_map = json.loads(page_map_path.read_text(encoding="utf-8"))
    pages = page_map.get("unique_pages")
    if (
        page_map.get("schema") != "mathematics-commons-stacks-synctex-source-page-map/v1"
        or page_map.get("candidate_id") != CONFIG["candidate_id"]
        or page_map.get("stem") != STEM
        or not isinstance(pages, list)
        or not pages
        or any(not isinstance(page, int) or isinstance(page, bool) for page in pages)
        or pages != sorted(set(pages))
    ):
        raise AssertionError("source-page map lacks a valid unique-page inventory")
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the sealed R31 candidate PDF and its configured high-resolution pages."
    )
    parser.add_argument("--render-root", type=Path, required=True)
    parser.add_argument(
        "--high-res-pages",
        type=int,
        nargs="*",
        help="Must exactly match the sealed SyncTeX source-page map; omit to use that map.",
    )
    args = parser.parse_args()

    high_res_pages = configured_high_res_pages()
    if args.high_res_pages is not None and sorted(set(args.high_res_pages)) != high_res_pages:
        raise AssertionError("--high-res-pages differs from the sealed candidate configuration")
    render_root = args.render_root.resolve()
    if render_root.exists():
        raise FileExistsError(f"refusing to overwrite render root: {render_root}")
    page_root = render_root / STEM
    contact_root = render_root / "contact_sheets"
    highres_root = render_root / "highres"
    for path in (page_root, contact_root, highres_root):
        path.mkdir(parents=True, exist_ok=False)

    page_count = len(PdfReader(str(PDF)).pages)
    full_dpi = int(CONFIG["visual_qa"]["full_page_dpi"])
    high_dpi = int(CONFIG["visual_qa"]["high_resolution_dpi"])
    sheet_capacity = int(CONFIG["visual_qa"]["contact_sheet_page_capacity"])
    if sheet_capacity != 16:
        raise AssertionError("the current 4-by-4 contact-sheet renderer requires capacity 16")
    render_pages(PDF, page_root, full_dpi)
    rendered = sorted(page_root.glob("page-*.png"))
    if len(rendered) != page_count:
        raise AssertionError(f"expected {page_count} renders, found {len(rendered)}")

    font = ImageFont.load_default()
    tile_width = 300
    label_height = 24
    gap = 8
    contact_rows = []
    for sheet_index in range(math.ceil(page_count / 16)):
        selected = rendered[sheet_index * 16:(sheet_index + 1) * 16]
        with Image.open(selected[0]) as sample:
            tile_height = round(sample.height * tile_width / sample.width)
        sheet = Image.new("RGB", (4 * tile_width + 5 * gap, 4 * (tile_height + label_height) + 5 * gap), "white")
        draw = ImageDraw.Draw(sheet)
        for offset, page_path in enumerate(selected):
            page_number = sheet_index * 16 + offset + 1
            row, column = divmod(offset, 4)
            x = gap + column * (tile_width + gap)
            y = gap + row * (tile_height + label_height + gap)
            with Image.open(page_path) as page:
                page = page.convert("RGB")
                page.thumbnail((tile_width, tile_height), Image.Resampling.LANCZOS)
                sheet.paste(page, (x, y + label_height))
            draw.text((x + 4, y + 4), f"{STEM}.pdf page {page_number}", fill="black", font=font)
        output = contact_root / f"{STEM}_{sheet_index + 1:02d}.png"
        sheet.save(output, format="PNG", optimize=True)
        contact_rows.append({"sheet": sheet_index + 1, "file": output.name, "bytes": output.stat().st_size, "sha256": sha256(output)})

    highres_rows = []
    for page_number in high_res_pages:
        if page_number < 1 or page_number > page_count:
            raise ValueError(f"high-resolution page outside PDF: {page_number}")
        scratch = highres_root / f"scratch-{page_number}"
        scratch.mkdir()
        render_pages(PDF, scratch, high_dpi, page_number, page_number)
        outputs = list(scratch.glob("page-*.png"))
        if len(outputs) != 1:
            raise AssertionError(f"unexpected high-resolution output for page {page_number}")
        output = highres_root / f"{STEM}_p{page_number}.png"
        outputs[0].replace(output)
        scratch.rmdir()
        highres_rows.append({"page": page_number, "file": output.name, "bytes": output.stat().st_size, "sha256": sha256(output)})

    render_rows = []
    for page_number, path in enumerate(rendered, 1):
        render_rows.append({"page": page_number, "file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "schema": "mathematics-commons-stacks-private-render-manifest/v1",
        "generated_at_utc": utc_now(),
        "published": False,
        "pdfs": {STEM: {"pdf_sha256": sha256(PDF), "dpi": full_dpi, "renders": render_rows}},
        "contact_sheets": contact_rows,
        "high_resolution": {"dpi": high_dpi, "renders": highres_rows},
    }
    manifest_path = render_root / "render-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"pages": page_count, "contact_sheets": len(contact_rows), "high_resolution": len(highres_rows), "manifest": str(manifest_path)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
