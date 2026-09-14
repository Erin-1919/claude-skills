---
description: Ingest a source into the wiki — read, summarize, update all affected pages
argument-hint: <source-file-path>
---

# Ingest Source into Wiki

Read a source document, create a wiki source page, update all affected concept/entity/synthesis/project pages, and maintain index + log.

## Implementation Steps

### 1. Validate the Source

Read the file at the provided path (typically in `{{RAW_DIR}}/`).

If the file does not exist, report the error and stop.

If the file is a PDF, read it (use the `pages` parameter, in chunks, until the whole document is read). If the file is markdown, read it directly.

### 2. Check for Existing Source Page

Read `wiki/index.md` to check whether a source page already exists for this document.

If a stub exists: this is an enrichment — read the existing stub and replace it with a full page.

If a full page exists: report that this source has already been ingested and stop (unless the user explicitly asks to re-ingest).

### 3. Create the Source Page

Create a source page in `wiki/sources/` following this exact format:

```markdown
---
title: "Author (Year)"
type: source
authors: [Author A., Author B.]
year: YYYY
venue: "Journal or Conference"
doi: "doi-string"
tags: [relevant, tags]
date_ingested: YYYY-MM-DD
---

## Summary
2-4 dense paragraphs: the problem, the approach, the contribution.

## Key Insights
Numbered list of 6-10 bold-titled insights relevant to {{PROJECT_FOCUS}}. Technical details matter: subdivision rules, cell types, coding schemes, formulas, error metrics.

## Relevance to Project
What the implementation should inherit from this source, and what its limitations are.

## Key Quotes
5-7 verbatim quotes with section/page attributions.

## See Also
A single line of [[wikilinks]] to related wiki pages.
```

Use kebab-case filename: `author-year.md` (e.g., `smith-et-al-2024.md`).

Use today's date for `date_ingested`.

### 4. Flag Surprises (Hybrid Mode)

Before updating other wiki pages, check whether the new source:
- **Contradicts** any existing claims in concept, synthesis, or project pages
- **Introduces concepts** not yet covered by any wiki page
- **Changes the answer** to anything in `wiki/project/open-questions.md` or the trade-offs in `wiki/project/design-decisions.md`
- **Affects the conformance analysis** in the project's standing gap/conformance synthesis pages (adapt to this project)
- **Reveals** something unexpected or ambiguous

If any of these apply: report the findings to the user and ask how to proceed before continuing. Show specifically which pages would be affected and what would change.

If nothing surprising: briefly report key takeaways and proceed to step 5.

### 5. Update Affected Wiki Pages

Identify and update all wiki pages affected by this new source:

- **Concept pages** (`wiki/concepts/`): add references to the new source. Update definitions or key numbers if the source adds new understanding.
- **Entity pages** (`wiki/entities/`): update if the source mentions specific grid systems, standards, or tools.
- **Synthesis pages** (`wiki/synthesis/`): update the lineage/positioning page if the source extends it; update gap/conformance analyses if it changes the picture (adapt page names to this project).
- **Project pages** (`wiki/project/`): update `design-decisions.md` and `open-questions.md` if the source informs a decision or answers/raises a question.

For each page updated, add the new `[[source-page]]` wikilink to the appropriate section.

If the source introduces a concept or entity that deserves its own page but doesn't have one yet: create it. Check first whether an existing red link (see the latest lint entry in `wiki/log.md`) already names it.

### 6. Update Index

Read `wiki/index.md`. Add the new source page entry in the Sources section, maintaining chronological order. Add any new concept/entity/synthesis/project pages created in step 5 to their respective sections.

### 7. Update Log

Append a new entry to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | Source Title
- Created: `sources/filename.md`
- Updated: `concepts/affected-page.md`
- Created: `concepts/new-concept.md` (if applicable)
- Updated: `index.md`
- Flags: [anything surfaced in step 4]
```

Use today's absolute date.

### 8. Commit (if git repo)

If the project is a git repository, stage and commit:

```bash
git add wiki/
git commit -m "wiki: ingest Source Title (Year)"
```

If not a git repository, skip this step silently.

### 9. Report Summary

Report to the user:
- Source page created (with path)
- Number of pages updated
- Number of new pages created (if any)
- Any flagged contradictions or surprises (from step 4)
- Suggested follow-up: related sources to look for, questions to investigate

## Important Notes

- **NEVER modify files in `{{RAW_DIR}}/`** — raw sources are immutable
- **ALWAYS update index.md and log.md** — every wiki change must be tracked
- **Use absolute dates** in log entries (e.g., 2026-07-04, not "today")
- **Cross-reference generously** — every new page should link to related pages
- **Flag contradictions** — do not silently overwrite existing claims
- **One source at a time** — ingest sequentially to maintain wiki coherence
