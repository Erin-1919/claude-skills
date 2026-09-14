# Template: "Wiki Knowledge Base" section for a project's CLAUDE.md

Replace `{{RAW_DIR}}` with the raw-sources directory and `{{PROJECT_FOCUS}}` with a one-line statement of what the wiki is for. Keep project-specific rules at the end.

---

## Wiki Knowledge Base

This project maintains an LLM-generated wiki in `wiki/`. The wiki is a persistent, compounding knowledge base, not a RAG system. Knowledge is compiled once and kept current, not re-derived on every query.

### Structure

- `wiki/index.md`: master catalog of all pages by category
- `wiki/log.md`: chronological record of all operations
- `wiki/overview.md`: evolving high-level synthesis
- `wiki/sources/`: one page per ingested source (paper, spec, article)
- `wiki/concepts/`: one page per key concept
- `wiki/entities/`: one page per concrete system, tool, standard, or dataset
- `wiki/synthesis/`: cross-cutting analyses and comparisons
- `wiki/project/`: this project's evolving design documents ({{PROJECT_FOCUS}})

Raw sources live in `{{RAW_DIR}}/` and are immutable. The wiki reads from them but never modifies them.

### Page Conventions

- All pages have YAML frontmatter with at minimum: title, type, tags.
- Source pages additionally have: authors, year, venue, doi (if known), date_ingested.
- Use Obsidian-style `[[wikilinks]]` for all cross-references.
- Use kebab-case filenames.
- Source pages follow the template: Summary / Key Insights / Relevance to Project / Key Quotes / See Also.

### Workflows

**Ingest**:
1. Read the source from `{{RAW_DIR}}/`
2. Create a source page in `wiki/sources/`
3. Identify all concept, entity, synthesis, and project pages that need creation or updates
4. Flag anything surprising or contradictory for user input
5. Update `wiki/index.md` and append to `wiki/log.md`

**Query**: Read `wiki/index.md` first to find relevant pages. Synthesize answers with wikilink citations. Offer to file valuable answers as synthesis pages.

**Lint**: Scan for orphan pages, missing pages, stale claims, weak cross-references, and concepts mentioned but lacking their own page. Report findings before fixing.

### Rules

- Never modify files in `{{RAW_DIR}}/`
- Always update `index.md` and `log.md` after any wiki change
- Use absolute dates in log entries (e.g., 2026-07-04, not "today")
- When new information contradicts existing pages, flag it rather than silently overwriting
- Cross-reference generously: every page should link to related pages
- Design decisions go in `wiki/project/`, with the reasoning and the sources that motivated them
