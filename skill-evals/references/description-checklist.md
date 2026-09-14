# Skill Description Checklist

The description is the only part of a skill in context on *every* model call. It decides
whether the skill fires at all, and roughly half of all skill failures are trigger
failures. Audit it first.

## The three questions

A description answers **why**, **how**, and **when** — for the model, not for a human.

- **Why** — what the skill gets the model that it doesn't have.
- **How** — what it does with it.
- **When** — the concrete conditions that make it apply.

## Directives, not essays

Passive information invites the model to decide. A directive doesn't.

```
BAD   The interactions API is recommended for multi-turn agents because it handles
      session state on the server side and reduces token usage.

GOOD  Use when building chat or multi-turn agent code against Gemini. Replaces
      generate_content with the interactions API and the current model ids.
```

Write what to do, not what is true.

## Name the negatives

An over-triggering skill is a real cost: it burns tokens on every load and pollutes
context. Bound the trigger explicitly.

```
BAD   Use for web development tasks.
GOOD  Use when writing React components or Tailwind styles. Not for Angular, Vue, or
      backend work.
```

If you can't name what it's *not* for, the trigger is too broad.

## Length

Two sentences, target under ~500 characters. You pay for this on every single model
call whether or not the skill ever fires. Detail belongs in the body; deep detail
belongs in reference files.

## Audit checklist

- [ ] Starts with "Use when" (or an equivalent explicit trigger condition)
- [ ] Third person, no "I can help you"
- [ ] Names concrete artifacts / tools / file types, not abstract domains
- [ ] States at least one thing it is NOT for, when over-triggering is plausible
- [ ] Directive voice — tells the model what to do
- [ ] Under ~500 characters
- [ ] Does not summarize the skill's step-by-step workflow (the model will follow the
      summary instead of reading the body)
- [ ] Covered by at least 5 positive and 5 negative eval cases

## Body checklist

- [ ] Under ~500 lines; deep material split into `references/*.md`
- [ ] Goals and constraints, not a rigid step list — if the steps never vary, write a script
- [ ] No no-ops ("write clean code", "be thorough", "follow best practices")
- [ ] Reference files split by branch (one per cloud, one per language), so the model
      loads only the branch it needs
