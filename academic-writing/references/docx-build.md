# Building the Word manuscript from Markdown

Rules for any build script that turns Markdown sections into a journal's Word template (python-docx). Each rule fixes a fault the author had to repair by hand after a rebuild. A fix made in Word is lost at the next rebuild, so every formatting rule lives in the build script and every content change in the Markdown.

## Equations

- **Write displayed equations as native Word equations (OMML), never as formatted text runs.** Text runs look right but cannot be edited in Word's equation editor. Use [../scripts/docx_equations.py](../scripts/docx_equations.py): copy it beside the build script, then `add_equation(paragraph, tex)` for each `$$ ... $$` block. It covers subscripts and superscripts, `\mathrm`, Greek letters, common operators, braces, and `cases`; extend its tables for other symbols. Inline `$...$` math can stay as formatted runs.
- **One equation per line, each with its own number.** Do not pack several definitions into one row with commas or `\qquad` under one number. Give each its own `$$ ... \tag{n} $$` block. Put tuple expansions and small definitions in the "where" text below, for example "where each action $\alpha_i = (\kappa_i, T_i, p_i)$ has ...". Renumber every "Equation n" cross-reference after splitting, and turn a reference to a former group into a range ("Equations 5 to 7").
- **Number with tab stops.** The equation paragraph style holds a centre tab and a right tab: tab, equation, tab, "(n)".
- **The "where ..." text after an equation continues the paragraph.** It starts at the left margin with no first-line indent. Give the paragraph after a displayed equation the unindented body style.

## Figures and tables

- **A figure paragraph is flush left with no first-line indent.** Insert the image in the unindented body style at the full text width, never in the indented "new paragraph" style.
- **Separate table groups with a thin rule.** A group row after the first (for example "Wildfire" after the methane steps) gets a top border of about half the weight of the header rules. The first group sits under the header rule and needs none.
- **Table text follows the same terminology as the prose.** Captions, header cells, and body cells change together with the text (see Terminology in SKILL.md).

## Rebuild routine

- Rebuild after every change to the Markdown, including the author's own edits, so the Word file never lags the source.
- A rebuild fails while the file is open in Word. Ask the author to close it, or build to a temporary copy to check the result first.
- Verify a layout change in a render: export to PDF through Word and look at the page, because python-docx shows only the XML.
