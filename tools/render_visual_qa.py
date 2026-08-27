#!/usr/bin/env python3
"""Render a fixed-point chapter PDF for deterministic visual QA."""

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def render_pages(
    pdf: Path,
    destination: Path,
    dpi: int,
    first: int | None = None,
    last: int | None = None,
) -> None:
    command = ["pdftoppm", "-r", str(dpi), "-png"]
    if first is not None:
        command.extend(["-f", str(first)])
    if last is not None:
        command.extend(["-l", str(last)])
    command.extend([str(pdf), str(destination / "page")])
    subprocess.run(command, check=True)


def image_identity(path: Path) -> dict[str, object]:
    return {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--render-root", type=Path, required=True)
    parser.add_argument("--full-page-dpi", type=int, default=96)
    parser.add_argument("--high-resolution-dpi", type=int, default=180)
    parser.add_argument("--high-resolution-pages", type=int, nargs="*", default=[])
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    render_root = args.render_root.resolve()
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    if render_root.exists():
        raise FileExistsError(f"refusing to overwrite render root: {render_root}")
    if args.full_page_dpi < 1 or args.high_resolution_dpi < 1:
        raise ValueError("render DPI must be positive")

    reader = PdfReader(str(pdf))
    if reader.is_encrypted:
        raise ValueError("refusing to render an encrypted PDF")
    page_count = len(reader.pages)
    high_resolution_pages = sorted(set(args.high_resolution_pages))
    if any(page < 1 or page > page_count for page in high_resolution_pages):
        raise ValueError("high-resolution page lies outside the PDF")

    page_root = render_root / "full-pages"
    contact_root = render_root / "contact-sheets"
    high_resolution_root = render_root / "high-resolution"
    for path in (page_root, contact_root, high_resolution_root):
        path.mkdir(parents=True, exist_ok=False)

    render_pages(pdf, page_root, args.full_page_dpi)
    rendered = sorted(page_root.glob("page-*.png"))
    if len(rendered) != page_count:
        raise RuntimeError(f"expected {page_count} page renders, found {len(rendered)}")

    page_rows: list[dict[str, object]] = []
    render_hashes: list[str] = []
    render_dimensions: set[tuple[int, int]] = set()
    minimum_ink_pixels: int | None = None
    pages_without_ink = 0
    for page_number, path in enumerate(rendered, 1):
        with Image.open(path) as image:
            grayscale = image.convert("L")
            dimensions = image.size
            ink_pixels = sum(1 for value in grayscale.getdata() if value < 245)
        if ink_pixels == 0:
            pages_without_ink += 1
        minimum_ink_pixels = (
            ink_pixels
            if minimum_ink_pixels is None
            else min(minimum_ink_pixels, ink_pixels)
        )
        identity = image_identity(path)
        identity.update(
            {
                "page": page_number,
                "dimensions_pixels": list(dimensions),
                "ink_pixels_below_245": ink_pixels,
            }
        )
        page_rows.append(identity)
        render_hashes.append(str(identity["sha256"]))
        render_dimensions.add(dimensions)

    font = ImageFont.load_default()
    tile_width = 300
    label_height = 24
    gap = 8
    contact_rows: list[dict[str, object]] = []
    for sheet_index in range(math.ceil(page_count / 16)):
        selected = rendered[sheet_index * 16 : (sheet_index + 1) * 16]
        with Image.open(selected[0]) as sample:
            tile_height = round(sample.height * tile_width / sample.width)
        sheet = Image.new(
            "RGB",
            (4 * tile_width + 5 * gap, 4 * (tile_height + label_height) + 5 * gap),
            "white",
        )
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
            draw.text(
                (x + 4, y + 4),
                f"{pdf.name} page {page_number}",
                fill="black",
                font=font,
            )
        output = contact_root / f"{pdf.stem}_{sheet_index + 1:02d}.png"
        sheet.save(output, format="PNG", optimize=True)
        row = image_identity(output)
        row["sheet"] = sheet_index + 1
        row["pages"] = [
            sheet_index * 16 + 1,
            sheet_index * 16 + len(selected),
        ]
        contact_rows.append(row)

    high_resolution_rows: list[dict[str, object]] = []
    for page_number in high_resolution_pages:
        scratch = high_resolution_root / f"scratch-{page_number}"
        scratch.mkdir()
        render_pages(
            pdf,
            scratch,
            args.high_resolution_dpi,
            page_number,
            page_number,
        )
        outputs = list(scratch.glob("page-*.png"))
        if len(outputs) != 1:
            raise RuntimeError(
                f"unexpected high-resolution output count for page {page_number}"
            )
        output = high_resolution_root / f"{pdf.stem}_p{page_number}.png"
        outputs[0].replace(output)
        scratch.rmdir()
        row = image_identity(output)
        row["page"] = page_number
        high_resolution_rows.append(row)

    page_boxes = sorted(
        {
            tuple(float(value) for value in page.mediabox)
            for page in reader.pages
        }
    )
    manifest = {
        "schema": "unofficial-ai-integrated-stacks-private-render-manifest/v1",
        "status": "PASS",
        "created_utc": utc_now(),
        "published": False,
        "pdf": {
            "path": str(pdf),
            "bytes": pdf.stat().st_size,
            "sha256": sha256(pdf),
            "pages": page_count,
            "encrypted": False,
            "page_boxes_points": [list(box) for box in page_boxes],
        },
        "full_page_render": {
            "dpi": args.full_page_dpi,
            "count": len(page_rows),
            "dimension_sets": [list(item) for item in sorted(render_dimensions)],
            "pages_without_ink": pages_without_ink,
            "minimum_ink_pixels_below_245": minimum_ink_pixels,
            "duplicate_render_hashes": len(render_hashes) - len(set(render_hashes)),
            "pages": page_rows,
        },
        "contact_sheets": {
            "layout": "ordered 4-by-4",
            "count": len(contact_rows),
            "sheets": contact_rows,
        },
        "high_resolution_render": {
            "dpi": args.high_resolution_dpi,
            "count": len(high_resolution_rows),
            "pages": high_resolution_rows,
        },
    }
    manifest_path = render_root / "render-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "pages": page_count,
                "contact_sheets": len(contact_rows),
                "high_resolution_pages": len(high_resolution_rows),
                "manifest": str(manifest_path),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
