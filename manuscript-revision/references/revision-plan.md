# The revision plan

The plan is the working record for the whole round. It is written once at the start and
updated as each item lands, never reconstructed at the end.

## Contents

1. **Header** — journal, submission date, date each review arrived, each reviewer's
   recommendation, and the starting point: word count, reference count, counts of figures,
   tables and equations in the submitted file. These make every later "+N words" claim
   checkable.
2. **Working copies** — which files are being edited and which are the untouched baseline.
   State plainly that no tracked changes are used and that the marked-up copy is produced
   at the end by comparison.
3. **Status** — rewritten whenever the picture changes. What is complete, what remains.
4. **What the reviewers said** — one paragraph per reviewer, in the reviewer's own terms.
   This is where a reviewer's underlying concern is named, which is often not what any
   single numbered comment says.
5. **Comment inventory** — every comment given a stable id, `R2.4` for reviewer 2's fourth,
   with the comment in one line. Ids are used in every other document and never renumbered.
6. **Consolidated items** — the work plan. See below.
7. **Records for applied items** — what was actually done, filed as each item lands.
8. **Open decisions** — questions only the author can settle, with the options and the
   cost of each. Resolve these before the item that depends on them.
9. **Appendix: reviewer comments verbatim** — so the letter can quote them without
   returning to the decision email.

## Consolidating comments into items

Reviewers repeat each other and split one problem across several comments. Work the items,
not the comments.

- One item may answer several comments, and one comment may be split across items. Record
  which comment ids each item answers, and check at the end that every id is claimed.
- Name each item for the change it makes, not the complaint it answers. "Comparability
  conditioned on resolution" beats "address R3.6".
- Give each item: what changes, which comments it answers, whether new analysis is needed,
  and where in the manuscript it lands.

## Ordering: easy to hard, framing last

Order the items for execution, not by reviewer. Reading the table top to bottom is the
work plan. The order that works:

| Stage | Contains | Why here |
|---|---|---|
| Local fixes | wording, a missing definition, a wrong number, a citation | no dependencies, and each one removes a distraction from later reading |
| Claims calibration | over-strong claims, scope conditions | text-only, but each touches several places, so do each as one pass |
| New evidence | new analysis, new tables or figures, published artifacts | the substance; everything downstream cites these |
| Framing | abstract, introduction objectives, discussion, conclusions | must come after the evidence exists, since framing describes it |
| Close-out | language and numbering pass, marked-up copies, letter completion | describes the finished manuscript |

Two ordering rules that matter more than they look:

- **Framing last.** Rewriting the abstract before the evidence is settled means rewriting
  it twice, and the second rewrite is the one that gets missed.
- **A late reviewer does not restart the plan.** Verify each new comment against the
  current text first. Some are already answered by work done, and those need only a
  response in the letter. Merge the rest as new items at the end.

## Records

When an item is applied, file a record. Include:

- what changed, section by section, with the wording that landed
- the decision behind any judgment call, and what was rejected
- anything discovered that the plan did not predict, especially an error of the author's
  own, since that is exactly what a later reader will want to find
- numbers verified against their source, with the source named

Use `scripts/plan_status.py --done <id> --record-file note.md --write` so the table row and
the record stay consistent.

## Length budget

Reviewers add work; journals cap length. Track the running word count against the limit
from the start, and note which items are expected to add or remove words. Discovering a
1,500-word overrun at the end forces cuts in whatever was written last, which is usually
the framing.
