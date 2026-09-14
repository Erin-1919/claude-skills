---
name: manuscript-revision
description: Revise an academic manuscript in response to peer review and write the point-by-point response letter. Use when the user has received reviewer comments, referee reports, or an editor's decision letter and wants to revise a paper, plan a revision, answer reviewers, write a rebuttal or response-to-reviewers letter, produce a marked-up copy, or work through revision items one by one. Covers consolidating comments into ordered work items, maintaining a revision plan, editing .docx files safely, keeping numbered citations in first-appearance order, and building the response letter as the work lands.
---

# Manuscript revision

A revision round has two deliverables that must stay in step: the revised manuscript and
the response letter. The letter quotes the manuscript, so it can only be finished as the
manuscript is finished, and it goes stale whenever the manuscript changes.

## Standing rules

These hold throughout and override any local convenience.

1. **Propose before editing.** Show before and after text and wait for approval before
   touching a .docx. Every time, however small the change.
2. **Use the academic-writing skill for all new prose**, in the manuscript and in the
   letter. Invoke it rather than writing from general instinct.
3. **Never overwrite the author's hand edits.** They edit responses in Word. Mirror those
   edits back with `sync_letter.py --write`.
4. **Update the plan as each item lands**, not at the end, with `plan_status.py`.
5. **Verify numbers against their source**, not against another part of the manuscript.
6. **One item at a time.** Finish, record, then start the next.

## Setup, once per revision round

```bash
S=<this skill>/scripts
python $S/revision_config.py --init <revision folder>   # then edit revision.json paths
python $S/revision_config.py                            # confirm every path resolves
```

`revision.json` holds the paths, the citation style and the letter's font and colour.
Every script reads it, so nothing is hard-coded to a project.

Copy `assets/REVISION_PRINCIPLES.md` into the revision folder and edit it for the project.
Ask the author to confirm it, since it records their standing preferences.

**Flatten citation fields before any editing**, once:

```bash
python $S/flatten_endnote.py --working --write
```

Reference-manager citations are Word fields. Editing prose around them breaks them, no
reference can be added without returning to the manager, and edits can land inside field
code where they are invisible.

## The workflow

### 1. Read the reviews and build the plan

Read every comment and give each a stable id, `R2.4` for reviewer 2's fourth comment. Ids
are used everywhere afterwards and are never renumbered.

Write the plan from `assets/REVISION_PLAN_TEMPLATE.md`. Consolidate comments into items
ordered easy to hard: local fixes, claims calibration, new evidence, framing, close-out.
Framing comes last because it describes evidence that does not exist yet.

Read `references/revision-plan.md` for the plan's structure, the consolidation rules and
what belongs in a record.

Before scheduling anything, **verify each comment against the current text**. Some are
already answered, some rest on a misreading worth answering differently, and a reviewer
arriving late may be asking for work already done.

Surface anything only the author can decide as an open decision, with the options and the
cost of each. Resolve it before starting the item that depends on it.

### 2. Scaffold the letter

```bash
python $S/scaffold_letter.py comments.md --write
```

Write `comments.md` with a `# Editor` or `# Reviewer N` heading per section, the reviewer's
overall assessment as plain paragraphs, and `## R1.1` per comment. This produces the letter
with every comment verbatim and a placeholder for every response, plus an `answers.py`
stub. Read `references/response-letter.md` for structure and formatting.

### 3. Work the items

For each item, in plan order:

1. Read what the manuscript currently says. Quote it back to the author.
2. Draft the replacement with the **academic-writing skill**. Propose before and after.
3. On approval, apply it with the `docx_util` helpers. Read `references/docx-editing.md`
   first; every trap in it has cost real time.
4. Write the response into `answers.py`, then `python $S/fill_responses.py --write`.
5. Record the item: `python $S/plan_status.py --done C7 --record-file note.md --write`.
6. Re-run the checks below.

When the author says they edited the letter, run `sync_letter.py --write` before anything
else, so their wording is what gets built on.

### 4. Checks, after every item

```bash
python $S/manage_references.py --check     # ordering and coverage
python $S/verify_letter.py                 # every quoted passage exists
python $S/sync_letter.py                   # letter and answers agree
```

If a reference was added or removed:

```bash
python $S/manage_references.py --renumber --write
```

Renumbering changes markers the letter may quote, so run `verify_letter.py` afterwards.

### 5. Re-audit when figures or tables change

A change late in the round can falsify a response written early. After any change to a
figure, a table or a number, re-read the responses that mention it. `verify_letter.py`
catches stale quotes; it cannot catch a claim that is now untrue.

### 6. Close out

1. Language, numbering and markup pass: equation, table and figure numbering against their
   cross-references; abbreviations at first use; leftover markers; consistent ranges and
   spacing.
2. Write the editor page and the per-reviewer summaries, last, against the finished
   manuscript. Each summary says what the revision does for *that reviewer's* comments.
3. Produce the comparison baselines and hand over:

```bash
python $S/flatten_endnote.py --baseline --write
```

Then the author runs Word's Compare, original `*_plaincite.docx` against the working copy.
Compare cannot be scripted; it is the author's step.

## Scripts

| Script | Does |
|---|---|
| `revision_config.py` | finds and validates `revision.json`; `--init` writes a template |
| `docx_util.py` | run-safe reading and editing helpers; import, do not run |
| `letter_io.py` | reads letter blocks, rewrites `answers.py`; import, do not run |
| `flatten_endnote.py` | `--working` flattens citation fields; `--baseline` makes comparison copies |
| `scaffold_letter.py` | builds the letter and `answers.py` from `comments.md` |
| `fill_responses.py` | writes answers into placeholders only |
| `sync_letter.py` | mirrors hand edits from the letter back into `answers.py` |
| `verify_letter.py` | every quoted passage must exist in the manuscript |
| `manage_references.py` | `--check` and `--renumber` for first-appearance ordering |
| `plan_status.py` | marks an item applied and files its record |

Every script prints what it would do and needs `--write` to act. Each backs up to `.bak`
before writing.

## What to hand back to the author

- Anything that needs their judgment, as a question with options and costs, not a guess.
- Any error found in their own work, plainly, with how it was verified.
- The steps only they can do: typing equations in Word, running Compare, placing figures,
  and confirming any value that could not be read from a source they hold.
