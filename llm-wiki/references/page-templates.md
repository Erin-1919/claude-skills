# Page Templates and Ingestion-Agent Prompt Requirements

## Frontmatter requirements

All pages:
```yaml
---
title: "Human-Readable Title"
type: source | concept | entity | synthesis | project | meta
tags: [kebab-case, tags]
---
```

Source pages additionally: `authors: [list]`, `year`, `venue`, `doi` (omit if unknown), `date_ingested: YYYY-MM-DD`.

Filenames: kebab-case; sources named `author-year.md` (`smith-et-al-2024.md`), disambiguate colliding author-years (`ulmer-samavati-2020.md` vs `ulmer-et-al-2020.md`).

## Source page template

```markdown
## Summary
2-4 dense paragraphs: the problem, the approach, the contribution.

## Key Insights
6-10 numbered, bold-titled insights, each a substantive paragraph.
Technical details matter: rules, formulas, schemes, algorithms, error metrics.

## Relevance to Project
What the project should inherit from this source, and what its limitations are.

## Key Quotes
5-7 verbatim quotes with section/page attributions.

## See Also
Single line of [[wikilinks]]: sources | concepts | entities.
```

## Concept/entity page shape

Short and focused: a one-paragraph definition, then only the sections the content demands (how sources treat it, key numbers as a table, constraints, open items). Every page links to its sources and its neighboring concepts. A page that would be under ~5 sentences should be merged into a neighbor instead.

## Ingestion-agent prompt checklist

When dispatching one agent per source (bootstrap step 4), each prompt must contain:

1. **Project framing** — one sentence on what the project is, so "Relevance to Project" lands.
2. **Exact file path** to read (PDF via Read `pages` param in chunks, or pre-extracted text file).
3. **Exact output path** for the source page (`wiki/sources/<kebab-name>.md`).
4. **The full page format** (frontmatter fields + section template above).
5. **Shared wikilink vocabulary** — the list of likely link targets, so parallel agents converge on the same names instead of inventing synonyms. Also: license to invent new kebab-case targets for source-specific concepts.
6. **The sibling sources** being ingested in the same batch, so agents cross-link them.
7. **The maintainer digest** to RETURN as the final message:
   - TL;DR (with the source's exact title),
   - concept-page candidates (name, one-line definition, 2-3 sentences),
   - entity-page candidates (same),
   - numbers/statistics worth preserving,
   - flags: anything surprising, contradictory, or ambiguous.
8. For long sources (theses, specs): which sections are priority vs. likely duplication of already-ingested material, and the specific open questions the source might answer.

The digests — not the source pages — are what the maintainer uses to write concept/entity/synthesis pages, so they must be detailed enough to write from without re-reading the sources.

## Log entry format

```markdown
## [YYYY-MM-DD] ingest | Source Title
- Created: `sources/filename.md`
- Updated: `concepts/affected-page.md`, `index.md`
- Flags: [surprises/contradictions, or "none"]
```

Operations: `bootstrap`, `ingest`, `query`, `lint`, `synthesis`.
