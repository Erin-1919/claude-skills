# Section Patterns and Document Conventions

Companion to [../SKILL.md](../SKILL.md). The hard rules and prose rules there apply throughout. This file covers what changes from section to section, plus the conventions that govern the document as a whole.

Sentence templates for each section are in [phrase-bank.md](phrase-bank.md).

## Abstract

- **Structure**: Context (1-2 sentences) → Gap/Problem → Objective → Methods (brief) → Key Results → Implication/Conclusion.
- **Length**: 150-250 words, single paragraph.
- **Style**: dense, self-contained. No citations and no references to other papers. Every sentence carries essential information.
- Write the Abstract last.

## Introduction

- **Funnel structure**: broad context → narrowing to the specific problem → knowledge gap → objectives. Open with a broad, grounding statement about the field, then progressively narrow.
- Dedicate 2-3 paragraphs to literature review, grouping by theme and not chronologically.
- State the knowledge gap explicitly.
- End with explicit objectives in flowing prose, never a numbered list. State research questions in flowing prose too, not as an enumerated Q1-Q4 list ("we examine whether ..., which ..., how ..., and where ...").
- **Contributions introduce the work, not the results.** State what the paper does and delivers (a benchmark, a system, an analysis), not the numbers it found. Specific results belong in the Abstract and Results. Aim for about three contributions, folding supporting items such as an artifact release or a sub-method into the main ones.
- Optionally follow objectives with a paper roadmap.
- Use citation-dense sentences here to establish context without over-explaining each source.

## Related Work

- **Cluster-first, thematic organization.** Group prior work into a few coherent threads, one per subsection or paragraph, and open each with the thread rather than a single paper. Match the subsection structure to what the paper actually contributes, and fold related-but-not-central literature into a nearby subsection rather than giving it its own.
- **Use narrative citations for specific studies.** Make the author or named system the grammatical subject ("Author (year) applied X to Y"). Do not open a sentence with filler such as "Subsequent work in this journal ...", "A related line uses ...", or "The closest line of work is ...".
- **Give concrete detail on what each cited study did.** Prefer "converting land-use raster products onto a hierarchical grid" over "performed multi-source analysis".
- **State the gap once, at the end of the section.** Do not criticize each thread at the end of every paragraph or scatter gap fragments ("none does X", "Y remains understudied") across paragraphs. Consolidate them into a brief closing paired with what this paper provides.
- **Close crisply.** A two-sentence gap-then-contribution close beats an enumerated positioning paragraph. Drop a standalone "Positioning" subsection when its content is only the gap, and fold that gap into the last subsection's closing.
- **Keep it concise.** Trimming redundant critique is worth it even when the section falls below its word target.
- **Under a hard page limit, cite the finding rather than the author.** The narrative-citation guidance above assumes room. When a review has to fit one page, "Sahr, White and Kimerling [1] decomposed the design space and surveyed sixteen systems" spends its words on who did the work and reads as an inventory. "Two decades of research have settled the geometry of global grids [1]" makes the point in a third of the space and describes a field instead of a bibliography. Reserve author-as-subject for the one or two studies the contribution is positioned directly against.
- **Keep the finding that runs against the paper's own position.** A related-work section with no cost in it reads as advocacy. Where the literature reports something unfavourable, state it and answer it: an equal-area prototype found "too slow for significant production usage" is a concrete engineering problem the work can respond to, and a reviewer holding that document will trust everything else more for having seen it. Suppressing it is both a credibility risk and a lost argument.
- **State limits as consequences of scope, not as shortcomings.** A draft that says what each contribution failed to do reads as an audit of other people's work. Say what each achieved, explain the limit as a consequence of what it was built for ("each was built for a single application"), and close on the opportunity. Same facts, and the posture is what changes.

## Methods (Materials and Methods / Methodology)

- **Subsection-heavy**: use clear subsections (Study Area, Data Collection, Analysis Methods, and so on).
- **Past tense** for what was done; **present tense** for general truths and equations.
- Describe the study area with geographic coordinates, area size, and ecological or geographic context.
- Present data sources in a **summary table** (Table 1 pattern): variable name, abbreviation, unit, description, source.
- Specify software, libraries, and versions explicitly.
- **Formalize the method.** This is the section where [formalization.md](formalization.md) applies hardest: define the data model and every operation, metric, and property symbolically before or alongside the prose description. A Methods section carrying no formal definitions is a draft, not a submission.
- **Equation conventions**: introduce displayed equations with a sentence ending in a colon. Follow each equation with a "where" paragraph that defines every symbol. Number equations sequentially as (1), (2), and so on.
- Use "was/were" passive voice naturally ("Elevation values were assigned to...") but do not overuse it. Mix with active "We" constructions.

## Results

### Organization

- **Organize subsections by experiment, not by conclusion.** Each subsection covers one experiment or analysis (a cross-model comparison, an ablation study), and a single experiment can carry several findings. The heading names the experiment, never a finding. A short lead-in mapping the subsections to the experiments helps the reader.
- Open each subsection by naming the experiment, then lead with its most important finding.
- **Present findings directly, without interpretation or mechanism.** Report what happened and the numbers. Leave the "why", broader implications, proposed fixes, and practitioner takeaways for the Discussion. A single measured one-sentence interpretation per finding is acceptable, but sustained explanation is not.
- **Distribute a cross-cutting analysis across the experiments it spans.** If one analysis (for example, a failure taxonomy) reports on several experiments, discuss the relevant part inside each experiment's subsection rather than in a separate catch-all subsection.
- Use precise quantitative language: percentages, R-squared values, RMSE, p-values, counts with denominators.
- Reference tables and figures inline, by purpose.

### Story-first reporting

Before writing any results or experiment text, identify the single key claim ("story") the experiment supports, then write around that claim. Do NOT report every metric available.

- **One claim per experiment or paragraph.** State the claim as the topic sentence, then report ONLY the metrics that directly support it. A validator-swap experiment whose finding is stability needs only the stability metrics, not replan rate, latency, cost, or per-field breakdowns.
- **Every reported metric is a potential reviewer question.** Before including a number, ask what question it invites. A 63.7% replan rate invites "is the system thrashing?". If the metric is not needed for the claim, omit it. The full numbers remain available for the response letter or supplementary material.
- **Explain a performance drop in the same breath as reporting it.** An unexplained degradation generates more questions than the explanation itself. Pair the drop with its identified locus (for example, "task success declines ... as intent F1 for IPCC codes declines in parallel"), converting the drop into a finding.
- **Frame honestly but favorably.** "Performance scales with model capability while the architecture remains the constant" reports the same numbers as "accuracy drops on weaker models" but converts the observation into the contribution being claimed.
- **Tables follow the story.** Keep only the rows that carry the story, typically 3-5. Combine related comparisons into one table with configuration columns instead of several tables repeating the reference column. A baseline configuration should appear in at most two tables across the paper. See the single-exhibit rule below for what may be combined.
- **Avoid introducing metrics not defined in the metrics or evaluation section.** Each new metric in a results table needs a definition, which costs space and invites scrutiny. Prefer reusing already-defined metrics.
- **Keep anecdotes out of results.** Single-case observations (one query caught, one interesting failure) belong in the Discussion or the response letter, not results paragraphs, where they invite generalization questions.
- **Never hand the reviewer a quotable self-indictment.** Words like "preliminary", "illustrative", "suggestive", or "a substantive limitation" applied to your own results invite rejection language verbatim. State the scope as a design fact inside the finding ("in a single re-prompting run, few sets become consistent") and reserve boundary discussion for the Limitations subsection, where each caveat appears exactly once, never in Results and again in Limitations.
- **Move scope bookkeeping into table captions.** Which metric each row block uses, conditioning rules, and excluded-case notes belong in the caption of the table they govern ("One wrong set consisting entirely of abstentions passes vacuously and is excluded."), while prose states the finding. A caption may carry these scope notes and still be concise.

## Discussion

- **Organize by theme in dedicated subsections** rather than strictly mirroring objectives. Typical subsections: performance analysis, role of key components, comparison with alternatives, design decisions and their implications, and limitations with future work.
- **One idea per subsection, stated exactly once.** If the same point appears in two subsections, consolidate them. Prefer fewer, well-organized subsections over many overlapping ones, and remove any sentence that repeats a point already made.
- Open each subsection with its main finding or claim, then interpret it.
- **Do not restate numerical results from the Results section** unless essential to a key interpretation. Discussion is interpretation, not a second Results section. Minimize references to earlier tables and figures.
- **Do not introduce new results or methods.** Move beyond explaining results: interpret findings in a broader context, discuss real-world implications, and relate them to existing literature.
- Acknowledge limitations openly in a dedicated subsection. Present each limitation as a factual observation, not hedged. **Keep the few limitations that matter** and fold necessary integrity disclosures (design asymmetries, budget artifacts, confounds) in compactly, not as a sprawling per-item list.
- End with a forward-looking statement about future research directions.

## Conclusions

- **Concise summary**: 1-2 paragraphs, not more than half a page. Halve a bloated summary rather than trimming at the margin.
- Restate what was done and the key results without introducing new information or repeating a point verbatim from the Discussion.

## Document-wide conventions

- **Abbreviations**: write out the full term at first occurrence in both the Abstract and the main body, including abbreviations every reader knows (for example, GIS). After that, use the abbreviation consistently. For this author, GIS expands to Geographic Information Science, not Systems.
- **Numbers**: spell out one through nine in prose; use numerals for 10+, measurements, and statistical values.
- **Percentages**: use the "%" symbol with the numeral ("10%", "0.1%"), not the word "percent". Keep the word only inside a metric's proper name (for example, "mass-weighted absolute percentage error").
- Use the Oxford comma in lists.
- **Captions**: concise and descriptive, above tables and below figures, without unnecessary detail. Never verbose.
- **Cross-references**: "Table 1", "Figure 1" (or "Fig. 1" per journal style), "Algorithm 1", "Equation 1", "Section X", all capitalized. Ranges as "Tables 3-5"; sub-figures as "Figure 7(a-c)"; supplementary as "Table S1" / "Figure S1".
- **Place each table or figure immediately after the paragraph that first cites it**, not at the end of the subsection or section. When one paragraph cites both a table and a figure, place the table first.
- **Number tables and figures in order of first in-text citation.** If restructuring changes the order, renumber and update every cross-reference (text, other captions, and any table or figure build scripts).
- **Each table is a single standalone exhibit with one consistent header.** Never stack two blocks with different columns, denominators, or units under one table number, and split them into separate numbered tables instead. Combining related comparisons via extra configuration columns is fine, because that keeps one consistent structure.
- **Section and subsection headings are declarative noun phrases**, not questions, sentences, or conversational fragments. Write "Generality of the mechanism" not "Is any of this general?". A heading names the topic, it does not argue it.
