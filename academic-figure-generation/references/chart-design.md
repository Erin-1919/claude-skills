# Chart Design

Decide the form from the data and the message, then code it. The examples come from real revisions where the first draft was rejected.

## 1. Table or figure

- List the tables first. A figure that shows the same per-condition means as a table adds nothing; reviewers and the author will ask for it to go.
- Good reasons for a figure beside a table: a trend across an ordered factor (cost growing with region size), a spread or distribution (min–max over models, runs, or seeds), a ratio or per-unit view the table does not give, a spatial pattern, a structure.
- Example: a grouped-bar figure of accuracy per model duplicated the results table. It was replaced by one figure of token cost against study-region size, which no table showed.

## 2. Variable type sets the axis

| Variable on x | Axis and mark |
|---|---|
| Nominal (models, methods, conditions) | Categorical axis; bars or dot plot; order by the paper's table order or by value |
| Small set of ordered levels, even if numeric (1, 2, 4 cells; 130, 248, 463 agents; low/medium/high) | **Categorical axis with equal spacing**; grouped bars or points; label every level |
| Truly continuous with many values (time, distance, a parameter sweep) | Continuous axis; line or scatter |

- Never put three or four experimental levels on a continuous (ratio) axis. Uneven spacing implies an interpolation the experiment did not test and leaves gaps that read as missing data. Example: region sizes plotted at x = 130, 248, 463 agents looked like a sparse line plot; as three labelled categories they read immediately.
- Join points with lines only when x is ordered and the trend is the message; never join nominal categories.
- Grouped bars: groups = the x levels, bars within a group = the series compared (for example, conditions). Keep the series order and colors identical across panels.

## 3. Labels in the reader's terms

- Tick labels name each level fully and can carry a second line: "1 level-5 cell\n(130 agents)". The axis label names the quantity: "Study region size".
- Avoid code or log vocabulary ("region set", "rs4", "topo"); use the term the text uses, and if the text uses a weak term, fix the text too.
- Y labels state the quantity and unit or scale: "Prompt tokens per run (log scale)", "Thousand tokens".

## 4. Aggregation and spread

- When several models or replicates share a pattern, plot the mean with a min–max whisker (or CI, stating which in the caption) in one panel. Small multiples per model are for when the models differ in kind.
- Show the spread whenever the text reports a range ("1.29 to 1.41").

## 5. Scales and reference series

- Use a log axis when series differ by more than about 10×, and say so in the label.
- Reference baselines that are computed, not measured (flooding, exhaustive search, a bound), get a neutral grey fill with distinct hatching ("///", "...") so they separate from measured series in color and in grayscale.
- Start bar axes at zero on linear scales.

## 6. Checks before delivering

- Read the rendered PNG. Look for overlapping tick labels, clipped text, a legend over data, whiskers hidden behind bars, and hatching that disappears at print size.
- Grayscale test: series stay distinguishable by lightness or hatching.
- Every number the text quotes from the figure is guarded in the script.
