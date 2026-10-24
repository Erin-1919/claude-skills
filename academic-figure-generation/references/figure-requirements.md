# Figure Requirements (house standard)

Apply all of these before finalizing any figure. The user's instructions for a specific paper or venue override them.

## 1. Typography

- Large fonts, well above library defaults: panel labels 14–15, axis labels 13, tick and value labels 11–12, legend 12. Map pages for screenshots: body text 20 px or more.
- Never shrink fonts to make a layout fit; change the layout instead.
- One sans-serif family (Arial) across all figures of a paper.

## 2. Only necessary text

- No figure title in the image; the caption carries it.
- No interpretive sentences, grey notes, significance stars, or statistics boxes on the plot.
- No "·" separators or decorative punctuation in labels; minimal wording.
- Labels use the paper's terms exactly as the text uses them (model names, region names, condition names). Internal jargon from code or experiment logs never reaches a label.

## 3. Panels

- Lowercase panel labels "(a)", "(b)", top-left, bold; a single-panel figure has none. In-text citations match the case: "Figure 4a".
- Stack panels vertically by default; go side by side when stacking would stretch bars wide. Aim for balanced panels.
- Shared legend placed once, outside the data region.

## 4. Output and naming

- PNG at 300 dpi by default. Add PDF only when the venue requires vector or the user asks.
- File names follow caption order: `figure1.png` … `figureN.png`. When figures are renumbered, rename the files and scripts in the same step and update every in-text citation.
- Delete figure files and scripts that the paper no longer uses.

## 5. Captions and citation

- Caption: one brief sentence, about 25 words at most, naming only the main elements shown, with panel letters where there are panels. Leave details (grid levels, years, data sources, abbreviation expansions, symbology) to the text and legend; abbreviations defined in the text are used as is. Never trim the country from a place name ("British Columbia, Canada"). Write a plain sentence with "with" or "showing", never a colon list. No findings, no numbers absent from the text.
  - Map: "Study area in northeastern British Columbia, Canada, with the three nested study regions and the BCER facilities." (17 words)
  - Plot: "Prompt tokens per question wake (a), per event wake (b), and per run (c) for study regions of one, two, and four level-5 cells."
- Every figure and table, including supplementary ones, is cited in the text. Grep for each "Figure N" and "Table N" before delivering.
- Place names include the country ("British Columbia, Canada").

## 6. Reproducibility

- Every plotted figure comes from a script, never a hand-edited image. One authoritative script per figure.
- Value guards: assert each number the text reports from the figure (ratios, ranges, counts), with tolerance matching the reported rounding. A guard checks the claim; never loosen one just to pass.
- External data render from a pinned local copy. Bulky derived data (GeoJSON, rasters) go in a gitignored folder that a script regenerates.

## 7. When not to plot

- Text-only content, a short list of values, or a two-point comparison belongs in prose or a table.
- Numbers already in a table are not plotted again unless the plot shows a relation the table hides.
