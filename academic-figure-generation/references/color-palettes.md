# Recommended Figure Color Palettes

> Preferred colors for plots (green–blue family). Use these by default unless a figure must
> follow an existing scheme, such as a project UI. Adopted 2026-07-18.

All colors are a cohesive **green ↔ blue** family so multi-panel figures read as one system.

## Categorical / qualitative (distinct series, bars, groups)

Use for a small number of unordered categories. Prefer well-separated hues; keep adjacent
categories different enough in lightness to survive grayscale printing.

- **Primary 4** — `#3D9F3C` (green) · `#9ED17B` (light green) · `#367DB0` (blue) · `#9DC7DD` (light blue)
- **Green set** — `#519D78` · `#21AD5D` · `#53BD7D` · `#8BCF8B` · `#AADCA9` · `#A1E7B8`
- **Blue set** — `#04579B` · `#3492B2` · `#5385BD` · `#58B8D1` · `#6CBAD8` · `#72C2FF` · `#9BC7DF`
- **Dark anchors** (emphasis / primary series) — green `#0E600F`, blue `#04579B` or `#191A94`

## Sequential — green (light → dark)

For ordered magnitude / heatmaps / choropleths.
- Ramp A: `#F7FEF0` → `#E9F7E5` → `#CEEFCC` → `#BFE8C1` → `#BCF4C5` → `#92C2A6`
- Ramp B: `#F3FBF2` → `#DDF3DE` → `#C4E9CA` → `#AADCA9` → `#8BCF8B` → `#519D78`

## Sequential — blue (light → dark)

- Ramp A: `#DBF1FA` → `#D8E5F7` → `#BAD2E1` → `#96C2D4` → `#6CBAD8`
- Ramp B: `#D6F6FF` → `#ACEEFE` → `#6FC8CA` → `#58B8D1` → `#3492B2` → `#04579B`

## Two-hue / diverging (green ↔ blue, 12-step)

For diverging scales or a wide ordered range spanning two hues:
`#F7FEF0`, `#E9F7E5`, `#CEEFCC`, `#BFE8C1`, `#BCF4C5`, `#92C2A6`, `#D6F6FF`, `#ACEEFE`,
`#6FC8CA`, `#58B8D1`, `#3492B2`, `#04579B`

## Reference example sets (from the source figures)

- Green categorical bars: `#99BCAC` · `#90B56D` · `#97C87D` · `#B9DF99`
- Green/blue paired scatter — greens `#0E600F` `#21AD5D` `#53BD7D` `#A1E7B8`; blues `#191A94` `#7087E4` `#72C2FF` `#BFE9FE`
- Blue sequential bars (dose/response style): `#6CBAD8` `#96C2D4` `#BAD2E1` `#D8E5F7` `#DBF1FA`

---

# Additional palettes (full hue range)

The green–blue family above is the default "house" look. Use these when a figure needs more
than a few categories, a diverging scale, or a warmer/broader range. Prefer a recognized,
colorblind-aware set (Okabe-Ito, ColorBrewer) when categories must be told apart precisely.

## Diverging (two-ended scales: low ↔ mid ↔ high)

- **RdYlBu** (ColorBrewer) — `#D73027` `#FC8D59` `#FEE090` `#E0F3F8` `#91BFDB` `#4575B4`
- **Red–cream–blue** — `#7A0101` `#BE1420` `#FBF0D9` `#012F48` `#669ABA`
- **Spectral-like** — `#A30543` `#F36F43` `#FBDA83` `#E9F4A3` `#80CBA4` `#4965B0`

## Qualitative / categorical (many distinct groups)

- **Okabe-Ito** (8, colorblind-safe — the safest default for categories) — `#E69F00` `#F0E442` `#009E73` `#56B4E9` `#D55E00` `#CC79A7` (+ black `#000000`, grey `#999999`)
- **tab10 subset** — `#1F77B4` `#2CA02C` `#D62728` `#E377C2` `#BCBD22` `#17BECF`
- **Set3** (12, pastel) — `#8DD3C7` `#FFFFB3` `#BEBADA` `#FB8072` `#80B1D3` `#FDB462` `#B3DE69` `#FCCDE5` `#D9D9D9` `#BC80BD` `#CCEBC5` `#FFED6F`
- **Cool pastel** (8) — `#A1A9D0` `#F0988C` `#B883D3` `#9E9E9E` `#CFEAF1` `#C4A5DE` `#F6CAE5` `#96CCCB`
- **Bright warm** (8) — `#F57C6E` `#F2B56E` `#FBE79E` `#84C3B7` `#88D7DA` `#71B8ED` `#B8AEEA` `#F2A8DA`

## Sequential — multi-hue (ordered, wide range)

- **Sunset (teal → red)** (7) — `#274753` `#297270` `#299D8F` `#8AB07C` `#E7C66B` `#F3A361` `#E66D50`
- **Plasma-like (indigo → gold)** (6) — `#16058B` `#6200AA` `#9E169D` `#CC4A74` `#EB7852` `#FCB431`

## Muted / earthy (small categorical set)

- (5) — `#FBF1C2` `#566970` `#E67A7F` `#9D3151` `#87BAA7`

## Usage guidance

- **Two-group comparison** (e.g. our v1–v4 vs ablation arms): use one dark and one light blue,
  or a green vs blue contrast — reserve the darkest tone for the primary/headline series.
- **≤4 categories**: use the Primary 4; beyond that, draw from the green + blue sets but check
  separation.
- **Ordered data**: use a sequential ramp (green or blue), not categorical colors.
- **Light ramps are for sequential use, not categorical** — the pale steps are too close in
  value to tell apart as separate categories.
- **Contrast/accessibility**: verify adjacent categorical colors are distinguishable in
  grayscale and for common color-vision deficiencies before finalizing.
