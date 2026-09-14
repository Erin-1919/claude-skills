# New evidence: experiments, analyses and artifacts

For a computational paper this is the largest and riskiest stage of a round. Reviewers ask
for runs; some are worth doing, some are not comparable at all, and the ones worth doing
usually share a prerequisite that nobody scheduled. Everything downstream cites the numbers
this stage produces, so it happens before the framing is written and after the local fixes
are out of the way.

## Triage before building anything

Reviewers do not distinguish "run this" from "prove this". You must. Put every requested
experiment in one table in the plan, and decide each one:

| Requested experiment | Asked by | Feasible? | Decision |
|---|---|---|---|
| [what they asked for] | R2.1, R3.2 | yes, moderate — [what it costs, what it needs] | **run it** |
| [what they asked for] | R1.2 | no — [why it is not comparable] | **rebut, plus [what stands in for it]** |

Three verdicts, not two:

- **Run it** when it is cheap relative to what it settles, and above all when it converts
  an assertion the paper already makes into evidence.
- **Rebut** when the comparison is not architecturally meaningful, or when no fair
  competitor exists. Say which, in the letter, and point at the controlled comparison you
  already have. A reasoned refusal, backed by an existing result re-interpreted, is a
  stronger answer than a weak new experiment.
- **Answer from data already on disk.** The commonest outcome, and the one most often
  missed. Logs, per-query timings, token counts and stored state frequently contain the
  requested number already. Check the artifacts before scheduling a run: an item expected
  to need new runs can often be closed by reading what the last run recorded.

Name the shared prerequisite. Several items usually depend on one piece of engineering —
a model-override knob, a flag, an extra recorded field. Build it once, first, and both
items follow. Schedule it as its own line, not inside one of the items.

## Decisions that change what gets built

Which model, which configuration, how many benchmark suites: these are the author's, and
they block the item. Raise them as numbered decisions with the options and the cost of
each, and record the resolution with its reasoning, **including the option rejected and
why**. That reasoning is the rebuttal prose. Where a comment is answered by declining an
experiment, the letter says what the decision record says.

## Exploration is a finding

Choosing the models, endpoints or configurations for a new experiment produces evidence of
its own: which candidates failed, and how. Keep an exploration log in the plan. Failed
candidates that fail for a structural reason — an interface a model does not support, an
output mode that is not honoured — are a result worth reporting in the paper, not
housekeeping.

## Provenance of every reported number

- A number in the manuscript must match an artifact on disk that a script produced.
- **Never change an executed input and keep the old output.** Correcting a typo in a query
  that was actually run means either re-running that query or leaving the artifact alone
  and noting the discrepancy. Silently editing the input is how a table becomes internally
  consistent and wrong.
- State, in the paper, whether reported figures come from a single execution. If they do,
  say so and give the resolution of the measurement, rather than implying a repeat.
- Verify a number a reviewer questions against the data that produced it, never against
  another table in the same manuscript.

## Runs that are executed and then withdrawn

Repeat runs are sometimes done and then not reported — because they would mix measurement
vintages with the published tables, because a hosted model changed under them, or because
reporting them would re-open settled conclusions. This is legitimate, and it has a
protocol:

1. Archive the withdrawn results in their own directory with a README stating when they
   were run, why they are not reported, and that no published number derives from them.
2. Exclude that directory from the repository's tracked results.
3. Say nothing about them in the letter. The letter reports what the manuscript reports.
4. Record the decision and its reasoning in the plan, so a later round does not
   re-discover the same runs and wonder why they were ignored.

## Code changed during a revision

Answering a reviewer often means changing the system: recording a field that was not
recorded, fixing a label, adding an override.

- Keep those commits **separate from the manuscript edits**, and say in the commit message
  which plan item they belong to.
- State in the plan whether each change affects any reported number. If it does, the
  affected runs are re-run and the tables updated; if it does not, say so explicitly, since
  that is the question a later reader will ask.
- A rename or a relabelling must propagate to every artifact that carries it: data files,
  prompts, benchmark inputs, tests, and any reproduction guide.

## Artifacts outside the manuscript

A round frequently touches files that live beyond the paper: a reproduction guide, a data
deposit, a repository README. Anything that names a table number, a figure number or a
metric is invalidated by the manuscript changes and must be updated in the same round. List
those files in the plan when the round starts, so the close-out sweep has something to
check against.
