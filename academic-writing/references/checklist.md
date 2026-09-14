# Final Checklist

Run every pass on every draft or revision before delivering. Each item is a mechanical search or count, and the rule it enforces lives in the linked section. If an item fails, go read that section rather than patching the symptom.

## Words and punctuation

1. **Punctuation scan.** Search for `;`, `—`, and `:`. No semicolons, no em dashes, no colons in prose (equations and formal definitions excepted). Confirm parentheses appear only for the four allowed uses, and that fronted scope-setting phrases carry a comma. → SKILL.md, Hard rules
2. **Modal scan.** Search for "would", "could", "may", "might". Every hit is recast. → SKILL.md, Hard rules
3. **Banned-word scan.** Work through the Banned words and phrases table. Then re-scan each edited sentence and its neighbors for same-root collisions the swap introduced. → SKILL.md, Word Choice
4. **Negation scan.** Search for sentences opening "No ", and for "no " and "none" as the object of a verb. Convert each to verb negation unless the phrasing is ordinary spoken English. → SKILL.md, Sentence Structure

## Claims

5. **Abstract-noun scan.** For each abstract noun phrase ("the data model", "the same path", "remain open", "these advantages"), ask whether a reader can say what it points at from the sentence alone. Replace or cut every one that fails. This is the most frequent failure in compressed prose. → SKILL.md, Terminology and Claims
6. **Defensive-writing scan.** Search for "not", "rather than", "instead of", "as opposed to", and "while" at a sentence opening, then count what survives. Keep at most one contrast per major section, and only where the contrast is the claim itself. Recast or delete the rest, and confirm no sentence ends in a corrective fragment. → SKILL.md, Defensive framing
7. **Claim and citation scan.** Every claim carries a number, citation, or mechanism. Grouped citations are attributed per finding, there are no orphan citations, and all reference metadata is verified. → citations.md
8. **Trim-triggered citation re-check.** If any passage was shortened this pass, re-run grouped-citation attribution, orphan detection, and first-appearance numbering together, computing the numbering from the text. → citations.md
9. **Anonymity sweep** (double-blind venues only). No "our prior work" phrasing anywhere, including the abstract, methods provenance, and discussion. → SKILL.md, Anonymity

## Structure

10. **Paragraph scan.** 4-8 sentences each, no short-sentence openers, no subsection-listing lead-ins, transitions varied, no paragraph opening on anaphora. → SKILL.md, Paragraph Structure
11. **Connection scan.** Read only the first four words of each sentence in order, within each paragraph. If that sequence does not trace the argument, the links have to be written in. Confirm also that no sentence joins two different kinds of fact with "and", and that no link rests on "In addition" or "Also" where the real relation is cause, consequence, or contrast. → SKILL.md, Paragraph Structure
12. **Formalization scan.** For each concept, metric, operation, and property introduced in Methods, confirm it has a formal definition where one is possible, that every symbol is defined in a "where" paragraph, that notation is consistent across sections, and that each numbered definition or property is referred to somewhere downstream. → formalization.md
13. **Section scan.** No new results or methods in Discussion or Conclusions. Results report findings without sustained interpretation, and every reported metric earns its place. → section-patterns.md
14. **Exhibit scan.** Headings are declarative noun phrases, captions concise, each table a single consistent exhibit, and tables and figures numbered by first citation and placed after the citing paragraph. → section-patterns.md, Document-wide conventions

## Final pass

15. Run the **academic-humanizer** skill.
