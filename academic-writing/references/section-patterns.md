# Section Patterns and Document Conventions

Companion to [../SKILL.md](../SKILL.md). The hard rules, the storyline rules, and the precision rules there apply throughout. This file covers what changes from section to section, plus the conventions that govern the document as a whole.

Each section entry gives the section's purpose, its structure, its length, and the faults the author has corrected in review. The guidance combines published writing guides (listed under **Sources** at the end) with the author's own review comments. Where the two differ, the author's rule wins. Sentence templates for each section are in [phrase-bank.md](phrase-bank.md).

## The shape of the whole paper

- **Hourglass.** The Introduction narrows from the field to the gap and the objectives. Methods and Results stay at the narrow waist. The Discussion widens from the answer to each research question to the literature and the field (Cals and Kotz 2013). The first paragraph of each Discussion subsection answers a research question in the terms the Introduction posed it.
- **Context, content, conclusion at every scale.** The paper as a whole, each section, and each paragraph open with context, deliver content, and close with the conclusion the reader takes away (Mensh and Kording 2017). A paragraph that ends on a detail leaves the reader asking why it was there.
- **Each subject in one place.** Cover each topic once and group related material. Only the central claim recurs across sections. Use the same term for the same concept everywhere, because a synonym makes the reader suspect a distinction (Mensh and Kording 2017).
- **Methods and Results mirror each other.** Every method has a result and every result has a method (Kotz and Cals 2013b). Describe no method whose result the paper does not report.

## Abstract

Purpose: tell the complete story for the reader who reads nothing else.

- **Structure.** Context and gap (one or two sentences) → what this study presents → approach, including the experimental comparison in one sentence → key results with one or two numbers → one implication sentence. The author's four required elements are the gap and purpose, the main contributions, a few key quantitative results, and a closing sentence on the implications.
- **Length**: the venue limit, often 150-250 words (IJGIS: 200), in a single paragraph.
- **No results before context.** The reader must know the question before any number appears (Mensh and Kording 2017).
- **State the implication directly.** The last sentence names the claim in its plainest form ("a DGGS is a foundation for agent-friendly geospatial software"), not a circumlocution ("software designed for these agents").
- No citations and no references to other papers. Every sentence carries essential information. Write the Abstract last.
- **Keywords**: usually five, following the venue's count. Capitalize expanded acronyms as the author prefers ("Discrete Global Grid System", "Large Language Model"), and do not repeat title words where the venue discourages it.

## Introduction

Purpose: convince a reader who does not know the work that the gap matters and that this paper fills it.

- **Three moves** (Swales 1990). First, establish the territory: open with a broad, grounding statement about the field and its importance. Second, establish the niche: state the gap explicitly, as a limitation of current approaches or an open question. Third, occupy the niche: present the approach, the objectives, and the contributions.
- **Narrow paragraph by paragraph.** Each paragraph orients the reader, says what is known, and ends on the key unknown that the next paragraph takes up (Mensh and Kording 2017). The gap statement sets the reader's expectations, so everything it promises must be delivered.
- **Stay general.** Specific findings of prior studies, their numbers and benchmark names, belong in Related Work. In the Introduction, summarize the state of knowledge in one sentence with grouped citations ("Benchmarks report low accuracy of LLMs on spatial reasoning tasks (A, B, C)"). Never repeat a number that Related Work reports.
- **Describe the approach at the level of components, not implementation.** Name the main components and how they relate (the agent types, and that agents communicate along the grid topology). Leave out what computes what, how a message is processed, and which property enables which shortcut. Those belong in the system description or the case studies.
- **Objectives in flowing prose, introduced plainly and in parallel.** "This study has three objectives. The first is to examine ..., the second is to examine ..., and the third is to demonstrate ...". Do not split the objectives into groups ("the first two examine ..., while the third ...") or number them as a list. State research questions the same way, never as an enumerated Q1-Q4 list.
- **Contributions introduce the work, not the results.** State what the paper delivers (a benchmark, a system, an analysis), not the numbers it found. Aim for about three contributions, folding supporting items such as an artifact release into the main ones.
- An analogy from a neighbouring field (for example, peer-to-peer networks for agent communication) earns at most a sentence here, or none. Develop it in the Discussion.
- A paper roadmap is optional. Drop it when the word budget is tight.

## Related Work

Purpose: show what the literature has established, what remains open, and therefore why this paper is needed. It is a synthesis, not an inventory.

- **Organize into two to four thematic threads** that match what the paper contributes, one per subsection or paragraph. Open each thread with its theme, not with a single paper. Fold related but non-central literature into the nearest thread.
- **Synthesize approaches, not papers.** Describe a general approach in one sentence and cite the two or three studies that take it together ("These agents plan and execute workflows of GIS tool calls (A, B, C), pass spatial operations to deterministic GIS algorithms (D), or decompose questions across specialized agents (E, F)"). A long sentence of grouped citations reads better than a sequence of "A did X. B did Y." A group holding a single study means the grouping is too fine, so merge it into a broader approach. Reserve author-as-subject citations for the one or two studies the paper positions itself directly against.
- **Give concrete detail on what the grouped studies do.** Prefer "convert land-use raster products onto a hierarchical grid" to "perform multi-source analysis".
- **Close each thread on the gap where the gap is real.** Name the limitation of prior work plainly and say how this study addresses it ("GridMind keeps these relations as a persistent property of the grid, which every agent reads whenever it acts"). Where prior work is a foundation the study builds on, state what it established and that the study adopts or extends it. Do not dress up a research question as a gap. Do not add a section-closing synthesis or positioning paragraph.
- **Write the gap sentence plainly.** "A substrate that holds the relations between queries is the opportunity this study takes up" is stilted. "GridMind addresses this limitation by ..." is the register.
- **Keep the finding that runs against the paper's own position**, and answer it. A related-work section with no cost in it reads as advocacy.
- **State limits of prior work as consequences of scope, not as shortcomings** ("each was built for a single application").
- **Keep it concise and every citation earned.** Each cited study supports a gap or a design decision. Around 40 references suits a full-length journal article. Where the venue counts references in the word limit, prune them first.
- **Under a hard page limit, cite the finding rather than the author.** "Two decades of research have settled the geometry of global grids [1]" makes the point in a third of the space of an author-by-author account.

## System Design (Architecture, Framework)

Purpose: describe the components that carry the contribution, and why each design choice fits the problem. It is not a manual of the software.

- **Open with an overview figure and one paragraph** naming the components and their relations. Then describe the components in the order in which data or messages flow through them.
- **Give depth in proportion to novelty.** Concentrate on the unusual features that carry the paper's technical content. Do not describe every component at equal depth (Levin and Redell 1983). Cite standard components in one sentence.
- **Give the rationale for each key decision in one sentence**, as a fit to the problem. Alternatives that no one raised belong in the Discussion, if anywhere (see **Defensive framing** in SKILL.md).
- **Omit details that no result depends on.** Parameter defaults, file formats, module names, retry logic, and edge cases go to the code repository or the supplementary material.
- **Use field vocabulary.** Every internal term from the codebase is either replaced by a field term or defined once at first use and used consistently after that (see **Precision** in SKILL.md).
- **Formalize what can be formalized**: data model, operations, and properties, per [formalization.md](formalization.md).
- **Tables carry content.** A table of actions with their arguments is content. A table of checkmarks or of yes/no comparisons is not, so express it in prose or move it to the supplementary material.

## Methods (Experimental Design, Materials and Methods)

Purpose: give what a reader needs to understand, judge, and reproduce the experiments, and nothing else.

- **Subsection-heavy**: use clear subsections (study area, data, experimental conditions, metrics, analysis).
- **Past tense** for what was done; **present tense** for general truths and equations.
- **Describe only methods whose results are reported** (Kotz and Cals 2013a), and only details that affect the results. Experimental design needs detail, but trivial settings that do not change any outcome are cut or moved to the supplementary material.
- **Name each condition by its manipulation** (see **Precision** in SKILL.md), and keep the names identical in Methods, Results, tables, and figures.
- **Define metrics in prose.** For each metric, state what it measures scientifically and why that quantity answers the research question. Introduce only metrics that Results reports.
- Describe the study area with its location (with the country), extent, and geographic context. Present data sources in a summary table when there are several: variable, unit, description, source.
- Specify software, libraries, models, and versions explicitly.
- **Formalize the method.** This is the section where [formalization.md](formalization.md) applies hardest: define the data model and every operation, metric, and property symbolically before or alongside the prose description. A Methods section carrying no formal definitions is a draft, not a submission.
- **Equation conventions**: introduce displayed equations with a sentence ending in a colon. Follow each equation with a "where" paragraph that defines every symbol. Number equations sequentially as (1), (2), and so on.
- Use "was/were" passive voice naturally ("Elevation values were assigned to...") but do not overuse it. Mix with active "We" constructions.

## Results

Purpose: present what was found, objectively and in the past tense, in the order that answers the research questions.

### Organization

- **Organize subsections by experiment, not by conclusion.** Each subsection covers one experiment, which can carry several findings. The heading names the experiment, never a finding. With one experiment per research question, use one subsection per experiment and fold model or configuration comparisons into it.
- **Each paragraph opens with the question or comparison it addresses, presents the data, and ends with the answer** (Mensh and Kording 2017). Primary results come first, secondary results after, and any unexpected finding last, labelled as unexpected (Kotz and Cals 2013b).
- **Put the detailed numbers in tables and the key findings in the text.** The text highlights the findings that carry the claim and does not repeat a table in full (Kotz and Cals 2013b). Under a tight budget (the author's rule of thumb is about 800 words for a two-experiment Results section), report only the most important comparisons and numbers.
- **Report similar results with identical sentence structure and words**, and always in the same order of conditions (Kotz and Cals 2013b). A synonym for a metric or condition makes the reader suspect a different quantity.
- **Present findings directly, without interpretation or mechanism.** Leave the why, broader implications, and practitioner takeaways for the Discussion. A single measured one-sentence interpretation per finding is acceptable. Words such as "remarkably" or "strikingly" are interpretation.
- **Distribute a cross-cutting analysis across the experiments it spans**, inside each experiment's subsection.
- Use precise quantitative language: values with their denominators or ranges, statistics with their tests, and consistent decimals.
- Reference tables and figures inline, by purpose.

### Story-first reporting

Before writing any results text, identify the single key claim the experiment supports, then write around that claim. Do not report every metric available.

- **One claim per experiment or paragraph.** State the claim as the topic sentence, then report only the metrics that directly support it.
- **Every reported metric is a potential reviewer question.** Before including a number, ask what question it invites. If the metric is not needed for the claim, omit it. The full numbers remain available for the supplementary material or the response letter.
- **Explain a performance drop in the same breath as reporting it.** Pair the drop with its identified locus, converting it into a finding.
- **Frame honestly but favorably.** "Performance scales with model capability while the architecture remains the constant" reports the same numbers as "accuracy drops on weaker models" but states the contribution.
- **Tables follow the story.** Keep only the rows that carry the story, typically three to five. Combine related comparisons into one table with configuration columns instead of several tables repeating the reference column.
- **Avoid introducing metrics not defined in the evaluation section.**
- **Keep anecdotes out of results.** Single-case observations belong in the Discussion or the response letter.
- **Never hand the reviewer a quotable self-indictment.** Words like "preliminary", "illustrative", or "a substantive limitation" applied to your own results invite rejection language verbatim. State scope as a design fact inside the finding, and give each caveat once, in the Limitations subsection.
- **Move scope bookkeeping into table captions.** Which metric each row block uses, conditioning rules, and excluded cases belong in the caption of the table they govern, while prose states the finding.

## Case Studies (Applications, Demonstrations)

Purpose: show the system working on a real problem, in service of the paper's claim.

- **One paragraph of setting per case**: location (with the country), data, period, and the agents involved.
- **Narrate the behaviour that demonstrates the claim**, through a few concrete decisions the agents made and why. Do not narrate the full run.
- Report a small set of outcome numbers in a table, using the round of record, and keep design details that belong in the system description out of this section.

## Discussion

Purpose: explain what the findings mean, why they turned out as they did, how they relate to existing work, and what they imply for the field. It is interpretation, never a second Results section.

- **Subsections.** The structure the author uses: one subsection per research question, then a subsection on implications, then limitations and future research. Headings are polished declarative noun phrases that state the role of the contribution ("DGGS as a guardrail of spatial reasoning for LLM agents", "DGGS as a communication structure for multi-agent systems", "Implications for agent-friendly geospatial software").
- **Open each subsection with the general claim, then narrow.** The first sentence answers the research question at a level broader than this study ("the reliability of spatial reasoning by LLM agents depends on whether spatial relations are inferred by the LLM or received as facts computed from a known spatial topology"). The following sentences give the study's specifics.
- **Then explain the mechanism**: why the result came out this way, in terms of how the conditions differ.
- **Then relate to the literature.** Compare with the one or two most relevant studies, state whether the findings align with them or extend them, and give the reason for any difference (Cals and Kotz 2013; Docherty and Smith 1999). Do not list many references, since the main review is in Related Work.
- **Then state the implication** for the field or for practice, which is the sentence the reader should remember.
- **No numbers unless essential.** Do not restate results. Use a number only when the interpretation cannot be made without it, and do not introduce new results or methods.
- **Develop an analogy from a neighbouring field lightly**, in a sentence or two that brings in the idea (for example, flooding in peer-to-peer networks) without shifting the paper's focus.
- **Implications subsection.** State the one key message straightforwardly and professionally, then support it in one logical sequence. When the support is a set of properties, introduce them with a sentence that names how many and enumerate them inline ("First, ... Second, ..."). Where the design generalizes, say so concretely (a new application defines its entities as feature agents and adds its actions).
- **Limitations lead into future research.** Write each limitation softly, as the scope of the current study ("This study represents spatial features as points ..."), not as a shortcoming that invites reviewers to demand new experiments. Each limitation maps one-to-one to a future direction, in the same order, and the future directions are concrete ("First, ... Second, ... Third, ..."). Leave out detailed case examples. Never write a bare "further research is needed" (Cals and Kotz 2013).
- **Length.** About 250 words per subsection in a full-length article, and a short subsection reads best as one paragraph.

## Conclusions

Purpose: give the citable bottom line of the paper.

- **Content, in order**: what the study did, the key findings as an answer to each objective, the contribution and its implication, and specific future work.
- **Length**: one paragraph of about 150-200 words, never more than half a page. Halve a bloated summary rather than trimming at the margin.
- **Synthesize, do not list.** Show how the findings together answer the question, with at most a few numbers.
- **Introduce nothing new**, and do not copy sentences from the Abstract or the Discussion verbatim.
- **Future work follows from the limitations** already stated, in one sentence, and is specific.
- End on the one-line takeaway readers should remember (Cals and Kotz 2013).

## Document-wide conventions

- **Abbreviations**: write out the full term at first occurrence in both the Abstract and the main body, including abbreviations every reader knows (for example, GIS). After that, use the abbreviation consistently. For this author, GIS expands to Geographic Information Science, not Systems.
- **Place names**: every study location carries its country at each mention, in prose and captions ("northeastern British Columbia, Canada", "Butte County, California, USA").
- **Numbers**: spell out one through nine in prose; use numerals for 10+, measurements, and statistical values.
- **Percentages**: use the "%" symbol with the numeral ("10%", "0.1%"), not the word "percent". Keep the word only inside a metric's proper name (for example, "mass-weighted absolute percentage error").
- Use the Oxford comma in lists.
- **Captions**: at most one brief sentence, above tables and below figures. Table captions may add the scope notes described under Results.
- **Cross-references**: "Table 1", "Figure 1" (or "Fig. 1" per journal style), "Algorithm 1", "Equation 1", "Section X", all capitalized. Ranges as "Tables 3-5"; sub-figures as "Figure 7(a-c)"; supplementary as "Table S1" / "Figure S1".
- **Place each table or figure immediately after the paragraph that first cites it**, not at the end of the subsection or section. When one paragraph cites both a table and a figure, place the table first.
- **Number tables and figures in order of first in-text citation.** If restructuring changes the order, renumber and update every cross-reference (text, other captions, and any table or figure build scripts).
- **Each table is a single standalone exhibit with one consistent header.** Never stack two blocks with different columns, denominators, or units under one table number, and split them into separate numbered tables instead. Combining related comparisons via extra configuration columns is fine, because that keeps one consistent structure.
- **Section and subsection headings are declarative noun phrases**, not questions, sentences, or conversational fragments, and never internal abbreviations such as "RQ1". Write "Generality of the mechanism" not "Is any of this general?". A heading names the topic, it does not argue it.
- **Supplementary material stays short**: only the tables a reviewer needs to verify the main claims.

## Sources

- Cals, J.W.L. and Kotz, D., 2013. Effective writing and publishing scientific papers, part VI: discussion. *Journal of Clinical Epidemiology*, 66 (10), 1064. doi:10.1016/j.jclinepi.2013.04.017
- Docherty, M. and Smith, R., 1999. The case for structuring the discussion of scientific papers. *BMJ*, 318 (7193), 1224-1225. doi:10.1136/bmj.318.7193.1224
- Gopen, G.D. and Swan, J.A., 1990. The science of scientific writing. *American Scientist*, 78 (6), 550-558.
- Kotz, D. and Cals, J.W.L., 2013a. Effective writing and publishing scientific papers, part IV: methods. *Journal of Clinical Epidemiology*, 66 (8), 817.
- Kotz, D. and Cals, J.W.L., 2013b. Effective writing and publishing scientific papers, part V: results. *Journal of Clinical Epidemiology*, 66 (9), 945. doi:10.1016/j.jclinepi.2013.04.003
- Levin, R. and Redell, D.D., 1983. How (and how not) to write a good systems paper. *ACM SIGOPS Operating Systems Review*, 17 (3), 35-40.
- Mensh, B. and Kording, K., 2017. Ten simple rules for structuring papers. *PLOS Computational Biology*, 13 (9), e1005619. doi:10.1371/journal.pcbi.1005619
- Swales, J.M., 1990. *Genre analysis: English in academic and research settings*. Cambridge University Press.
- Williams, J.M. and Bizup, J., 2017. *Style: lessons in clarity and grace*. 12th ed. Pearson. (Characters as subjects, actions as verbs; behind the **Sentence Structure** rules in SKILL.md.)
