"""Render poster previews from a PDF (needs PyMuPDF).

Full poster:      python preview.py poster.pdf --dpi 20
Print-scale crop: python preview.py poster.pdf --dpi 100 --crop X Y W H   (inches from top-left)
"""
import argparse
from pathlib import Path

import fitz

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--dpi", type=int, default=20)
ap.add_argument("--crop", type=float, nargs=4, metavar=("X", "Y", "W", "H"))
ap.add_argument("--out")
a = ap.parse_args()

page = fitz.open(a.pdf)[0]
clip = None
if a.crop:
    x, y, w, h = (v * 72 for v in a.crop)
    clip = fitz.Rect(x, y, x + w, y + h)
pix = page.get_pixmap(dpi=a.dpi, clip=clip)
suffix = "_crop" if a.crop else "_preview"
out = a.out or str(Path(a.pdf).with_name(Path(a.pdf).stem + suffix + ".png"))
pix.save(out)
print(f"{out} ({pix.width}x{pix.height} px; page {page.rect.width / 72:.2f}x{page.rect.height / 72:.2f} in)")
