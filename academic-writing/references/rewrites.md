# Worked rewrites

Before/after pairs behind the prose rules in SKILL.md. Each heading matches a rule
there. Read this when a rule is clear but you need a pattern to match against.

Most of these came out of reviewer feedback on the author's own manuscripts.

## Say it the simplest direct way, and do not stack subordinate clauses

| Before | After |
|---|---|
| a schema whose row is a cell and whose key is the identifier | a schema with the row as a cell and the key as the cell's hierarchical identifier |
| a clause chain about what a check certifies | three short statements |
| ..., and we will test whether X | a separate sentence |

## State claims directly; avoid nominalized or inverted constructions

The cleft is the same fault as the abstract subject, and it slips through most often.
Any sentence built on "is what", "is that", or a fronted "What ..." gets rewritten as
plain subject-verb-object.

| Before | After |
|---|---|
| The guarantees that make a DGGS valuable are the transitivity of... | A DGGS is valuable because containment is transitive... |
| Reported uncertainty is what makes a result defensible | A reported uncertainty makes a result defensible |
| The difference between the two cases is how... | The two cases differ in how... |
| X errors are failures to apply Y | X errors occur when the model fails to apply Y |

## Negate with the verb, not with a noun phrase

| Before | After |
|---|---|
| No standard makes a grid cell the feature of interest | the standards do not make a grid cell the feature of interest |
| carries no relation to geographic distance | generated coordinates do not correspond to geographic distance |
| with no uncertainty or observation count attached | attaches neither an uncertainty nor an observation count |

Leave ordinary uses alone: "none exceeds 67% accuracy", "without coordinate
conversion", "without being rebuilt". The rule governs the construction, not the word.

## Where a contrast must stay, recast it so the connective disappears

| Before | After |
|---|---|
| computed rather than estimated | computed directly from the cell geometry |
| not exhaustive | restricted to the three datasets |
| rather than relying on manual inspection | without manual inspection |
| not a general claim | for the two study areas examined here |

## Each sentence must connect to the one before it and the one after it

Three repairs, in order of preference.

**Carry a noun forward** and make it the new subject:

> ... requires both the data and the operations defined on those cells. **Those
> operations** also bound the analytical scope of LLM agents.

**Point back with a demonstrative that names what it points at**:

> Performance is the open engineering question ... **Answering it** delivers a shared
> index that ...

**State the relation with a connective that carries meaning** — never "In addition" or
"Also", which signal one more item in a list and are the weakest available link when
the real relation is cause, consequence, or contrast.

Diagnostic: read only the first four words of each sentence in order. If that sequence
alone does not trace the argument, the links are missing.

## Every sentence must do a job, and a concession has to be stated as one

The usual cause of a stray-looking sentence is an unstated concession: a fact was
included to acknowledge a counter-case, but the acknowledgement was left implicit.

> Performance is the open engineering question, **since** the equal-area grid in the
> OGC testbed proved too slow for production use.

Let the next sentence answer it. Diagnostic: delete the sentence and read the
paragraph. If the argument does not notice, the sentence is either filler or in the
wrong place.

## Do not join two different kinds of fact with "and"

Before, pairing a scope limitation with a performance measurement:

> Each such design was built for a single application, **and** the equal-area grid in
> the OGC testbed was too slow for production use.

After, same facts, one fewer seam, and the second sentence now has a job:

> Each such design serves a single application, and their storage cost and speed remain
> unmeasured. Performance is the open engineering question, since the equal-area grid
> in the OGC testbed proved too slow for production use.

## Every abstract noun phrase must be checkable

| Before | After |
|---|---|
| The data model above the grid | the data model that gives cell values their types, units, and relationships |
| Comparative performance, storage volume, and equal-area indexing remain open | the storage cost and speed of these designs are unmeasured |
| Service standards have followed the same path | cut, because no reader could resolve which path |

## Write what the source measured, not what the field believes

"H3 and S2 are the most widely adopted in industry" is a market-share claim, while the
cited paper says "the best software ecosystems". The sentence became "have the most
mature software ecosystems".

Before writing any superlative or adoption claim, find the sentence in the source that
supports it. If the source says something narrower, the narrower version is the claim.

## Replace evaluative comparatives with the property the source names

| Before | After |
|---|---|
| Storage has moved furthest in practice | storage is the most developed layer |
| the harder ones to build on | without comparable tooling for loading, transforming, and analysing data |
| the most advanced implementation | the named state the source reports |
