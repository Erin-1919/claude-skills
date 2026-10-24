"""Shared style for a paper's figures: fonts, palette, export, and panel labels.

Copy into the paper's figures folder and import from each figN_<slug>.py script:

    import figstyle as fs
    fs.apply()
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ...
    fs.save(fig, "figure4")
"""

from pathlib import Path

import matplotlib as mpl

HERE = Path(__file__).resolve().parent

# Green-blue house palette (references/color-palettes.md): dark anchors for headline series.
GREEN_DARK, GREEN, GREEN_LIGHT = "#0E600F", "#3D9F3C", "#9ED17B"
BLUE_DARK, BLUE, BLUE_LIGHT = "#04579B", "#367DB0", "#58B8D1"
GREY, GREY_LIGHT = "#7F7F7F", "#D9D9D9"   # computed reference series, with hatching


def apply() -> None:
    mpl.rcParams.update({
        "font.family": "Arial", "font.size": 12,
        "axes.labelsize": 13, "xtick.labelsize": 12, "ytick.labelsize": 12,
        "legend.fontsize": 12, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
        "hatch.linewidth": 0.8, "pdf.fonttype": 42, "savefig.dpi": 300, "savefig.bbox": "tight",
    })


def save(fig, name: str, formats: tuple[str, ...] = ("png",)) -> None:
    """Write figures/<name>.png (add "pdf" to formats when the venue wants vector)."""
    for ext in formats:
        fig.savefig(HERE / f"{name}.{ext}")
    print(f"wrote {name}: {', '.join(formats)}")


def panel_label(ax, text: str) -> None:
    """Lowercase bold panel label, e.g. panel_label(ax, "(a)")."""
    ax.text(-0.07, 1.04, text, transform=ax.transAxes, fontsize=15, fontweight="bold", va="bottom")


def guard(name: str, value: float, lo: float, hi: float) -> None:
    """Assert a number the text reports from this figure; fails loudly when results and text drift apart."""
    assert lo <= value <= hi, f"{name} = {value:.4g} outside the reported range [{lo}, {hi}]"
