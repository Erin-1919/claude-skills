---
description: Ask a question against the wiki knowledge base — synthesize an answer with citations
argument-hint: <question>
---

# Query the Wiki

Search the wiki for relevant pages, synthesize an answer with citations, and optionally file the answer as a new wiki page.

## Implementation Steps

### 1. Read the Index

Read `wiki/index.md` to identify which pages are likely relevant to the question.

Scan page titles and descriptions for relevance. Select 3-10 candidate pages to read.

### 2. Read Relevant Pages

Read the candidate pages identified in step 1. If a page references other pages that seem relevant, follow those links too.

Also read `wiki/overview.md` for general project context if the question is broad.

### 3. Synthesize an Answer

Compose an answer that:
- **Directly addresses the question** with a clear, substantive response
- **Cites wiki pages** using `[[wikilinks]]` — every factual claim should trace back to a source
- **Distinguishes** what is established in the literature from what is this project's own design
- **Notes contradictions** if different sources disagree
- **Identifies gaps** if the wiki doesn't fully cover the question

The answer format depends on the question:
- **Factual questions** ("What is X?"): concise answer with citations
- **Comparison questions** ("How does X compare to Y?"): markdown table with source references
- **Analysis questions** ("Why does X matter?"): structured argument with evidence from wiki pages
- **Design questions** ("What should we do about X?"): present options with trade-offs, cite relevant prior work, and connect to `wiki/project/design-decisions.md`

### 4. Offer to File the Answer

If the answer produces something worth keeping — a comparison, analysis, connection, or synthesis that would be valuable to reference later — offer to file it as a new page:

> "This answer could be useful as a wiki page. Want me to file it as a synthesis page?"

If the user agrees:
1. Create the page in `wiki/synthesis/` (or the appropriate category; design conclusions go in `wiki/project/`)
2. Add YAML frontmatter with title, type, tags
3. Add `[[wikilinks]]` throughout
4. Update `wiki/index.md`
5. Append to `wiki/log.md`:
   ```markdown
   ## [YYYY-MM-DD] query | Question summary
   - Created: `synthesis/new-page.md`
   - Updated: `index.md`
   ```
6. If the project is a git repository, commit:
   ```bash
   git add wiki/
   git commit -m "wiki: add synthesis page from query — page title"
   ```

If the user declines or doesn't respond: just present the answer. No wiki changes needed.

### 5. Suggest Follow-ups

After answering, suggest 1-3 follow-up questions or investigations that could deepen the wiki's coverage of this topic. These might be:
- Related questions the wiki could answer
- Gaps that would benefit from ingesting a new source
- Connections between pages that aren't yet cross-referenced
- An entry in `wiki/project/open-questions.md` this answer moves forward

## Important Notes

- **Read index.md first** — this is the primary navigation tool
- **Cite sources** — every claim should link to a wiki page
- **Don't fabricate** — if the wiki doesn't cover something, say so and suggest where to find it
- **Respect the wiki's scope** — answer from what's in the wiki, not from general knowledge, unless the user asks you to go beyond it
- **File valuable answers** — the goal is that explorations compound in the knowledge base
