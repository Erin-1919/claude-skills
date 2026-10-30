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

## Precision: corrections from the author's manuscript reviews

Each pair below is a sentence the author rejected after it had passed the checklist. The faults are in word choice, so no mechanical scan catches them. Run the precision pass in SKILL.md.

| Before | Fault | After |
|---|---|---|
| The grounding results indicate that the spatial accuracy of an LLM agent depends on where its spatial relations are computed. | "grounding results" is shorthand; "spatial accuracy" means positional accuracy of coordinates; an agent has no spatial accuracy; "where" names a location, not a method; the claim is narrowed to this study in an opening sentence | The results of the grounding experiment indicate that the reliability of spatial reasoning by LLM agents depends on whether spatial relations are inferred by the LLM or received as facts computed from a known spatial topology. |
| the LLM derived relations from the cell corners and facility points in its prompt | informal geometry; a domain instance in a general claim | the LLM derived relations from the vertex coordinates of the cell polygons and the coordinates of the points in its prompt |
| DGGS grounding compared with coordinate grounding | the second condition has no grounding | the DGGS-grounded condition compared with the coordinate-inference condition |
| the runtime determines the recipients from cell identifiers | internal codebase term as subject | GridMind determines the recipients from the cell identifiers of the sender |
| The prevailing response couples LLMs with external spatial computation. | figurative verb, vague subject, unresolved object | Recent studies connect LLM agents to external tools that compute spatial relations. |
| The LLM of each agent observes incoming messages | which LLM, which messages, what "observes" does | When a message reaches an agent, the LLM observes it, reasons over it and the agent's memory, acts by selecting the agent's actions, and explains the decision in natural language. |
| world channel | "channel" is reserved for the three DGGS channels | world events |
| In GIScience, autonomous GIS has begun ... | "GIScience" used after GIS was defined as Geographic Information Science | the defined abbreviation, GIS, or a rephrase |
| ... which makes a DGGS a foundation for geospatial software designed for these agents. | circumlocution for a named concept | ... which makes a DGGS a foundation for agent-friendly geospatial software. |
| (Discussion) lets agents act, lets the grid provide | casual "let" constructions | allows, enables ... to, or the actor as subject |
| The year, sector, and code fields instantiate the temporal and thematic dimensions | fancy verb where a plain one exists | The year, sector, and code fields represent the temporal and thematic dimensions |
| 3.1 Data model and system overview | "data model" is reserved in GIScience for vector/raster and object/field models | 3.1 DGGS-indexed data and system overview |
| without a persistent checkpointer; bypass geo-resolution | framework-internal and codebase terms | carries a lightweight conversational state between turns; skip geospatial grounding |
| an LLM-as-judge quality gate ... rather than an independent correctness oracle | software jargon plus a defensive contrast | an LLM-as-judge between response generation and final output that uses the same evidence available to the system |
| 35 queries enumerate over the spatial dimension | opaque abstraction for a countable property | 35 queries return values for several locations or cells |
| the gap reflects the full engineering stack; expose operations as tools; contributes recovery | software jargon; odd verb | the design as a whole; provide operations as agent tools; enables recovery |
| Each question constrains spatial, temporal, and thematic extents | indirect verb | Each question specifies spatial, temporal, and thematic extents |

## Terminology: field terms for recurring concepts

From the terminology audit of the GridMind manuscript (IJGIS, 2026). Each internal term was replaced by the term the literature uses, in the prose, captions, tables, and figures.

| Internal or coined term | Field term | Reason |
|---|---|---|
| "action vocabulary" | "action space" | Standard term for the set of actions available to an LLM or RL agent |
| "wake" (an agent's turn) | "activation" | Agent-based modelling term for when an agent runs; "wake" is code vocabulary |
| "run store" | "event log" | Standard name for an append-only record of messages and state changes |
| "typed state" | "structured state" | "Typed" suggests data types; the property is a fixed set of fields |
| "policy" (standing instructions in the system prompt) | "role system prompt" | In agent research a policy is the decision function, which here is the LLM call |
| "scenario package" | "domain application" | "Package" names a code module |
| "multi-agent system" (hundreds of agents) | "large-scale multi-agent system" at first use | The field keeps "multi-agent system" at large scale and marks the scale with "large-scale" |

Kept after the audit, each defined at first use: "runtime", "harness", "world event", the three channel names, and the condition names.

## Introduction: level of detail

Before (implementation detail in an Introduction):

> Because the cell area at each resolution is known, an observation with a spatial extent, such as a methane plume, can enter the hierarchy at the resolution whose cells match that extent. ... The runtime computes these relations with DGGS operators, so every agent receives them as facts.

After: the Introduction names grid agents and feature agents and states that agents communicate along the DGGS topology. The entry-resolution point moved to the Discussion as one sentence, and the operator detail moved to the system description.

Before (numbers repeated from Related Work):

> On a benchmark of spatial cognition, the leading model answered fewer than one quarter of the questions correctly (Yang et al. 2025).

After: a general statement with grouped citations ("Benchmarks report low accuracy of LLMs on spatial cognition and map-based reasoning (Yang et al. 2025, Dihan et al. 2025)"), with the numbers kept in Related Work only.

Objectives, before and after:

> Before: This study has three objectives, of which the first two examine (1) how ... and (2) how .... The third objective is to demonstrate (3) the architecture ...
>
> After: This study has three objectives. The first is to examine how ..., the second is to examine how ..., and the third is to demonstrate ...

## Related Work: synthesis instead of inventory

Before, one study per sentence:

> GeoGPT plans sequences of GIS tool calls (Zhang et al. 2024), and GIS Copilot runs spatial analysis inside QGIS (Akinboyewa et al. 2025). Yang et al. (2025) raised spatial-cognition accuracy to 70.48% by coupling the LLM with deterministic GIS algorithms. GeoAgentic-RAG retrieves spatial data and decomposes queries across specialized agents (Liang et al. 2026) ...

After, approaches with grouped citations:

> These agents plan and execute workflows of GIS tool calls (Zhang et al. 2024, Akinboyewa et al. 2025, Li et al. 2025), pass spatial operations to deterministic GIS algorithms (Yang et al. 2025), or decompose geospatial questions across specialized agents and workflow graphs built on neighbourhood, hierarchy, and containment (Liang et al. 2026, Bao et al. 2026).

Gap sentence, before (stilted) and after (plain):

> Before: A substrate that holds the relations between queries and lets agents act on events as they occur is the opportunity this study takes up.
>
> After: GridMind keeps these relations as a persistent property of the grid, which every agent reads whenever it acts.

## Limitations that lead into future research

Before (self-critical, invites requests for new experiments): a list of what the study failed to model, with detailed case examples such as the assignment of a fire engine to a specific burning cell.

After (scope stated softly, mapped one-to-one to future directions):

> This study represents spatial features as points bound to the cells that contain them and coordinates responses at the resolution of grid cells. Environmental context ... informs a subset of agent decisions. The memory of each agent holds its structured state and recent messages within a single run. Future research will extend GridMind in these three respects. First, finer-grained features ... Second, each grid cell will integrate the environmental context of its area ... Third, memory management will extend the structured state toward a spatio-temporal memory ...
