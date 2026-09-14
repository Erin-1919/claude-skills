# The response letter

The letter is what the editor reads first and what the reviewer checks against the
manuscript. It is built through the round, not written at the end.

## Structure

```
Response to Editor
  <written last: what the revision does, a summary of the changes, one line handing over>
Response to Reviewer 1 Comments
  <the reviewer's overall assessment, verbatim>
  Response: <written last: what the revision does for THIS reviewer's comments>
  Comment R1.1: <verbatim>
  Response: <thanks, rationale, what changed, the revised text quoted>
  ...
```

`scripts/scaffold_letter.py` builds this from a markdown file of the comments, with a
placeholder for every response, before any of them is answered.

## Formatting

Match the journal's own sample letter where there is one. Otherwise: the comment in the
document's body style, the response in a distinct colour so the editor can see at a glance
what is new, and the words `Response:` in bold at the start of each.

Set the font, size and colour once in `revision.json` under `letter_style`, and let the
scripts apply it. A response typed by hand into Word will not match, and mismatched runs
are obvious in a printed letter.

## Writing an individual response

Every response opens with thanks. Not a formula repeated verbatim twelve times, but an
opening that acknowledges what the comment actually did, since reviewers can tell the
difference between "Thank you for this comment" and "Thank you for reading the breaks off
the colour bars and setting them out figure by figure."

Then, in order:

1. **The rationale.** Why the change was made, or on what grounds the comment was
   answered differently than requested. This is the part that persuades.
2. **What changed and where.** Name the section and paragraph.
3. **The revised text, quoted.** So the reviewer can verify without opening the
   manuscript. Quote exactly, including citation markers that fall inside the quoted span,
   or `verify_letter.py` will report the quote as missing, and rightly.

Where a comment is declined, say so plainly, give the reason, and say what was done
instead. A reviewer accepts a reasoned "no" far more readily than a silent one.

Where a comment was already answered by work done for another comment, say that and point
to the other response rather than repeating it.

**Use the academic-writing skill for the prose.** The letter is read by the same people who
read the paper.

## The summaries, written last

The editor page and the per-reviewer summaries are written after every other response,
against the finished manuscript.

- **The editor page** says what the revision does, then summarises the changes, each with
  the section it landed in, then hands over to the detailed responses. Say what was
  changed, not what the reviewers asked for: the editor has their comments already.
- **A per-reviewer summary** covers what the revision does *for that reviewer's comments*.
  Four summaries that say the same thing tell the editor nobody read the reviews
  individually.

## Disclosing an error of your own

If checking a reviewer's point uncovers an error they did not find, disclose it, in the
response where it surfaced and in the editor summary. Say what was wrong, what it is now,
and how it was verified. An error found and reported by the authors reads as diligence; the
same error found later reads as something else.

## Keeping the letter and the answers file in step

The author edits responses in Word, because that is where they read them. Those edits are
the author's voice and must survive.

- After any editing session, run `sync_letter.py --write` to mirror the letter back into
  `answers.py`.
- Never regenerate a response that has been edited. `fill_responses.py` only touches
  placeholders, which makes this safe by construction.
- Run `verify_letter.py` after any round of manuscript edits, not only at the end. Quotes
  go stale silently when a sentence is reworded, a figure moves, or a citation is inserted
  into a quoted passage.
