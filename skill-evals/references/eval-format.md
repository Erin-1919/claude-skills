# Eval Case Format

A case file is a single JSON file. Stdlib-only so it runs anywhere.

```json
{
  "skill": "gemini-interactions-api",
  "cases": [
    {
      "id": "py-basic-chat",
      "prompt": "Write a Python script that has a back-and-forth conversation with Gemini.",
      "tags": ["python", "happy"],
      "should_trigger": true,
      "expect": ["from google import genai", "gemini-3"],
      "forbid": ["google\.generativeai", "gemini-1\.5", "gemini-2\.0"]
    },
    {
      "id": "neg-openai",
      "prompt": "Write a Python script that calls the OpenAI chat completions API.",
      "tags": ["negative"],
      "should_trigger": false,
      "forbid": ["from google import genai"]
    },
    {
      "id": "ts-streaming",
      "prompt": "In TypeScript, stream a model response token by token to the terminal.",
      "tags": ["typescript", "happy"],
      "should_trigger": true,
      "expect": ["@google/genai", "stream"],
      "files": {
        "package.json": "{\"name\":\"scratch\",\"type\":\"module\"}"
      }
    }
  ]
}
```

## Fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable identifier; used in the report |
| `prompt` | yes | What the user types. Write it as a *user* would — no skill name, no internal jargon |
| `should_trigger` | yes | `true` = the skill may/should load; `false` = loading it is a failure |
| `expect` | no | Regexes that must ALL appear in the final output |
| `forbid` | no | Regexes that must NOT appear |
| `tags` | no | Free-form; used to slice the report (`python`, `negative`, `prod-trace`) |
| `files` | no | Seed files written into the isolated workspace before the run |
| `setup` | no | Shell command run in the workspace before the agent (install deps, git init) |
| `judge` | no | Rubric string; when present the runner asks an LLM judge for pass/fail |

## Scoring

A trial passes when **all** hold:

1. Every `expect` regex matches the final output.
2. No `forbid` regex matches.
3. If `should_trigger` is `false`, the skill was not loaded.
4. If a `judge` rubric is present, the judge returns PASS.

Note the asymmetry on rule 3: a `true` case does **not** require the skill to load.
Outcomes, not paths — if the model got it right without the skill, that is a pass,
and a signal for the ablation report.

A case's score is `passes / trials`. The suite score is the mean case score.

## Regex notes

- Matched case-insensitively against the agent's final text output, `re.search`.
- Escape dots in identifiers: `google\.generativeai`, not `google.generativeai`.
- Prefer several narrow regexes over one long brittle one.
- Anchor on things the *skill* is responsible for: SDK import, method name, model id,
  file path, config key. Not on prose the model happens to write.

## LLM judge rubric

Use only when correctness isn't lexical. Keep the verdict binary.

```json
"judge": "PASS if the script handles a multi-turn conversation, persists session state between turns, and never re-sends the full history manually. FAIL otherwise. Answer with PASS or FAIL on the first line, then one sentence of reasoning."
```

Judges are ~1000x the cost of a regex per assertion. Convert a judge to regexes as soon
as you can see what the pass condition actually keys on.

## Sourcing prompts

Ranked best to worst:

1. **Production/real transcripts** — what users actually typed, including the vague ones.
2. **Bug reports** — "it keeps using the old model id" is a test case verbatim.
3. **Synthetic variations** — paraphrase the above; vary vagueness, language, framing.
4. **Written from the SKILL.md** — worst, and the default failure mode. These leak
   trigger keywords and pass trivially.
