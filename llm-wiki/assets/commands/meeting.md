---
description: Process a meeting note — extract knowledge, distribute updates across the wiki, track decisions and milestones
argument-hint: <meeting-note-path>
---

# Process Meeting Note

Read a meeting note (typically in `meeting_notes/`), extract actionable content, distribute updates across the wiki, and maintain index + log. Meeting notes are mutable working documents; the wiki is where their durable knowledge lands.

## Implementation Steps

### 1. Read the Meeting Note

Read the file at the provided path. If it does not exist, report the error and stop.

### 2. Triage Content

Classify each section into one of:

- **Knowledge essay** — standalone analysis or conceptual deep-dive (self-contained). Becomes a source page in `wiki/sources/` with `source_type: meeting-analysis`.
- **Conceptual insight** — a new concept or a significant extension of an existing one. Updates or creates a page in `wiki/concepts/`.
- **Direction / suggestion** — a directive that changes project framing or scope. Updates the relevant `wiki/project/` page (e.g. `research-agenda.md`).
- **Idea / open question** — something to investigate later. Goes to `wiki/project/open-questions.md` (or `research-agenda.md` Active/Deferred).

Present the triage to the user and **wait for approval** before acting:

```
Triage for YYYY-MM-DD meeting:
1. Section "Topic A" → new source page `sources/topic-a-analysis-YYYY.md` (knowledge essay)
2. Section "Topic B" → update `project/research-agenda.md` (direction)
3. Section "Topic C" → add to `project/open-questions.md` (open question)
Proceed with all, or adjust?
```

### 3. Extract Knowledge Essays

For essay sections, create a source page in `wiki/sources/` with frontmatter:

```yaml
---
title: "Essay Title (Year)"
type: source
source_type: meeting-analysis
authors: [<note author>]
year: YYYY
venue: "Meeting notes — weekly discussion"
tags: [relevant, tags]
date_ingested: YYYY-MM-DD
meeting_date: YYYY-MM-DD
---
```
Structure: Summary, Key Insights, Relevance to {{PROJECT_FOCUS}}, See Also.

### 4. Update Existing Wiki Pages

For each insight/direction, read the target page, add the content in the right section, and attribute with the meeting date:

```markdown
**[YYYY-MM-DD meeting]** Content here — the insight or decision.
```

### 5. Check for Project-Doc Implications (milestone ritual)

If a section implies a revision to the project's main design/proposal document ({{PROJECT_DOC}}):
- Note it in `wiki/project/idea-evolution.md` as a pending change.
- Ask whether to revise {{PROJECT_DOC}} now or defer.
- If revised, add a version entry to `idea-evolution.md` and, for a genuine milestone, create an annotated git tag (e.g. `idea-vX.Y`) — confirm with the user before tagging.

### 6. Update Index and Log

Add any new pages to `wiki/index.md`. Append to `wiki/log.md` (absolute date):

```markdown
## [YYYY-MM-DD] meeting | Meeting YYYY-MM-DD
- Source: `meeting_notes/YYYY-MM-DD.md`
- Created: `sources/new-page.md` (if applicable)
- Updated: `concepts/…`, `project/…`
- Decisions: [brief list]
- Open questions: [brief list]
```

### 7. Commit

```bash
git add wiki/
git commit -m "wiki: process meeting YYYY-MM-DD"
```

### 8. Report Summary

Pages created/updated (with paths), decisions recorded, open questions added, and any {{PROJECT_DOC}} implications flagged.

## Important Notes

- **Present triage before acting** — the user approves the distribution plan.
- **Attribute meeting content** — always note the meeting date on added content.
- **Never modify raw sources** in `{{RAW_DIR}}/`. Meeting notes themselves are mutable, but leave the original intact after extraction unless the user asks to simplify it.
- **Always update index.md and log.md**; use absolute dates; cross-reference generously.
