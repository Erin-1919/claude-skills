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
  Response: <the direct answer, what changed and where, the revised text quoted>
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

Answer the concern behind the comment, directly, in the first sentence. Reviewers read
dozens of responses. Each one should read as an answer, not an explanation of effort.

1. **Find the underlying intent first.** A comment that says "the contribution is unclear"
   asks for a sharper argument, not for more evidence. A comment on the Discussion that
   lists engineering detail asks for scientific meaning. Answer that request, and check
   which section the comment actually targets before proposing anything.
2. **Lead with the answer.** The first sentence states what the revision now does about
   the concern. Section names, quotes and supporting detail come after it.
3. **Keep only what carries the answer.** Cut word counts, page counts of individual
   edits, "no new experiments were added", dataset citations, cost totals, and any number
   that does not change what the reviewer concludes. A ratio beats two absolute figures.
4. **Paragraphs only.** No bullet points, numbered lists or tables inside a response. When
   evidence maps onto several contributions, write one paragraph per contribution and tie
   the metrics to it.
5. **Quote the revised text.** Quote exactly, including citation markers inside the
   span, so `verify_letter.py` can confirm it.

Courtesy follows the editor. Where the editor asks for no courtesy formulas, open with the
answer. A reviewer with no remaining objections gets one sentence of thanks and nothing
else: restating what was retained invites another reading.

**Do not write defensively.** No paragraph explaining why something stayed as it was
unless the reviewer asked for it to change. No pre-emptive disclaimers. A declined comment
gets a plain "no", the reason, and what was done instead, in two or three sentences.

**Do not introduce what the reviewer did not raise.** A new comparison with another
system, including the authors' own, invites a new round of comments. Cite related work in
the manuscript; leave comparisons out of the letter unless requested.

Where a comment was already answered by work done for another comment, say so in one
sentence and point to that response.

**When numbering has shifted, say the old number.** If a table or figure was renumbered
during the round, give it as "Table 6 (previously Table 5)" at its first mention in each
reviewer's thread. The reviewer is reading against the version they reviewed. Their own
comment numbering never changes.

**Use the academic-writing skill for the prose.** The letter is read by the same people who
read the paper.

## The summaries, written last

The editor page and the per-reviewer summaries are written after every other response,
against the finished manuscript.

- **The editor page** is in the body colour; only reviewer responses take the response
  colour. One opening paragraph says what the revision does and states that the
  manuscript is within the journal's length limit, without word counts. A short numbered
  list summarises the changes, one line each with the section it landed in. Close with one
  line handing over to the detailed responses. Say what was changed, not what reviewers
  asked for, and name only the file that actually carries tracked changes (typically the
  anonymised one).
- **A per-reviewer summary** covers what the revision does *for that reviewer's
  comments*, in two or three sentences.

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
- After the author's own pass over the whole manuscript, re-sync before anything else. That
  pass reworded or cut text the letter quotes, and `verify_letter.py` is how you find which
  responses now describe a manuscript that no longer says that. It reports a missing quote;
  it cannot tell you the item was deleted, which is why the plan records are walked at the
  same time.
