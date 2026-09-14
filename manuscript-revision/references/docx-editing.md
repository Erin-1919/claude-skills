# Editing a manuscript .docx safely

Every trap here cost real time in a live revision. `scripts/docx_util.py` handles most of
them; this explains what it is protecting against.

## Runs, not strings

A phrase is almost never one run. Word splits runs at spell-check boundaries, formatting
changes, and after any edit, so `p.text.replace(a, b)` cannot be written back.

Use `splice(paragraph, old, new)`, which replaces a span straddling runs and keeps the
formatting of the run where the span starts.

## Paragraph.runs hides text

`Paragraph.runs` skips runs inside `w:hyperlink`. A paragraph with a link reads short, and
an edit silently misses text. Always read through `all_runs` / `ptext`.

## Document order is not paragraphs-then-tables

`doc.paragraphs` followed by `doc.tables` puts every table after all prose. Anything
depending on where things appear, above all first-appearance citation ordering, must walk
the body's children instead. Use `iter_document_order`.

## Equations are invisible to text extraction

OMML equations (`m:oMath`) hold no `w:t`, so a paragraph containing inline maths reads with
gaps: "where  is Avogadro's number". That is not a missing word. Check `has_math` before
concluding anything is wrong, and never "repair" such a gap.

Equations are typed in Word by the author. To add one, insert a marker paragraph such as
`[TYPE EQUATION 6 HERE, THEN DELETE THIS MARKER]`, tell the author where it goes, and
verify later that no marker survives.

## Rewriting a whole paragraph

`set_text` is only safe when every run shares one format. Check `uniform(paragraph)` first.
Author blocks, table footnotes and anything with superscripts usually fail that test.

## Locate by content, never by index

Paragraph indices shift the moment anything is inserted. Find the target by a distinctive
substring, and assert exactly one match. A script that says "paragraph 115" will edit the
wrong paragraph the next time it runs.

## Word holds the file open

Saving over a file open in Word raises `PermissionError` and writes nothing. Ask the author
to close it and re-run. Never write to a different name as a workaround: two versions of
the manuscript is a worse problem than waiting.

## Back up before writing

Copy to `path + '.bak'` before `doc.save`. Every script here does.

## Verify against the source, not the document

When a reviewer questions a number, check it against the data that produced it, not against
another table in the same manuscript. In one round this is how a table of totals was found
to have been transcribed from a superseded run: the manuscript was internally consistent
and wrong.

## Check, do not trust, after writing

After a script reports success, confirm the change is in the file. A filtered command can
hide an error, and a stale timestamp can look like a fresh write. Read the paragraph back.
