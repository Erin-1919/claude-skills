---
description: Health-check the wiki — find orphans, stale claims, missing pages, weak cross-references
---

# Lint the Wiki

Perform a comprehensive health-check of the wiki. Identify structural and content issues, report findings, and fix with user approval.

## Implementation Steps

### 1. Read the Full Index

Read `wiki/index.md` to get the complete page catalog.

### 2. Build a Link Map

Read every wiki page listed in the index. For each page, extract:
- All outbound `[[wikilinks]]` (pages this page links to)
- All YAML frontmatter fields
- Page type and tags

Build a map of: which pages link to which, and which pages are linked to by others. The mechanical part can be done with a shell one-liner:

```bash
cd wiki && grep -rhoE '\[\[[^]|]+' --include='*.md' . | sed 's/\[\[//' | sort -u > /tmp/links.txt
find . -name '*.md' -printf '%f\n' | sed 's/\.md$//' | sort -u > /tmp/pages.txt
echo '--- unresolved links:'; comm -23 /tmp/links.txt /tmp/pages.txt
echo '--- orphan pages:'; comm -13 /tmp/links.txt /tmp/pages.txt
```

### 3. Run Structural Checks

Check for the following issues and collect all findings:

**Orphan pages** — pages in the index that have zero inbound links from other pages. Every page should be reachable from at least one other page.

**Missing pages (red links)** — `[[wikilinks]]` that point to pages that don't exist. Compare against the known intentional red links recorded in the latest lint/bootstrap entry of `wiki/log.md`; report new ones separately. Each needs either a new page created or the link redirected to an existing page.

**Unreferenced source pages** — source pages that aren't cited by any concept, entity, synthesis, or project page. Sources should be woven into the wiki, not isolated.

**Frontmatter issues** — pages missing required fields (title, type, tags). Source pages additionally need: authors, year, venue, doi, date_ingested.

**Empty sections** — pages with section headers but no content beneath them.

**Link synonym drift** — two different link targets naming the same concept (two link targets naming one concept). Normalize to one canonical page.

### 4. Run Content Checks

**Stale claims** — read synthesis and project pages. Flag any claims that reference specific sources but where newer ingested sources may have updated the picture. Cross-check the log to see what was ingested recently. Pay special attention to synthesis pages that depend on external standards (external specs/standards referenced by the wiki may have been superseded) and the status fields in `project/design-decisions.md`.

**Missing concepts** — scan all pages for recurring terms or ideas that are referenced but don't have their own concept page. Look for terms that appear in 3+ pages without a dedicated page.

**Weak cross-references** — pages that discuss related topics but don't link to each other.

**Contradictions** — claims in one page that conflict with claims in another page. Flag with specific page references and quotes.

**Answered open questions** — entries in `project/open-questions.md` that newer content has actually answered; they should be resolved and moved into the relevant pages.

### 5. Check Index Completeness

Scan the `wiki/` directory for any `.md` files not listed in `wiki/index.md`. These are pages that exist but aren't indexed.

```bash
find wiki -name "*.md" -not -name "index.md" -not -name "log.md" | sort
```

Compare against index entries. Report any discrepancies.

### 6. Report Findings

Present findings organized by severity:

```markdown
## Wiki Health Report

### Critical (broken links, missing pages, contradictions)
- [ ] `[[missing-page]]` referenced by concepts/foo.md:15 — page does not exist
- [ ] ...

### Important (orphans, stale content, weak links)
- [ ] `entities/bar.md` has zero inbound links (orphan)
- [ ] ...

### Minor (frontmatter, style)
- [ ] `concepts/foo.md` missing tags in frontmatter
- [ ] ...

### Suggestions (new pages, new sources)
- The term "X" appears in 4 pages but has no concept page
- Consider ingesting [specific paper] to strengthen coverage of [topic]
- ...

**Summary:** X critical, Y important, Z minor issues found.
```

### 7. Fix with Approval

After presenting the report, ask:

> "Want me to fix any of these? I can handle them all, or you can pick specific ones."

If the user approves fixes:

1. Fix issues in priority order (critical first)
2. For each fix:
   - Make the change
   - Briefly report what was done
3. Update `wiki/index.md` if pages were added
4. Append to `wiki/log.md`:
   ```markdown
   ## [YYYY-MM-DD] lint | Wiki health check
   - Fixed: [list of fixes]
   - Created: [any new pages]
   - Remaining: [issues not fixed, including intentional red links]
   ```
5. If the project is a git repository, commit:
   ```bash
   git add wiki/
   git commit -m "wiki: lint — fix N issues"
   ```

If the user declines: leave the wiki unchanged. The report itself is the value.

## Important Notes

- **Read every page** — lint requires a full scan, not sampling
- **Report before fixing** — never auto-fix without presenting findings first
- **Prioritize by impact** — broken links and contradictions matter more than missing tags
- **Suggest new sources** — if a gap could be filled by ingesting a known paper, say so
- **Track lint history** — the log entry helps future lints know what was checked and when
