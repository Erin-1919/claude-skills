# Citations

Companion to [../SKILL.md](../SKILL.md). Read before attaching, verifying, or renumbering citations, or formatting a reference list.

## Placement

- **Place in-text citations at the end of sentences**, not mid-sentence. Write "Previous research has shown that X (Author et al., Year)" rather than "Author et al. (Year) showed that X leads to Y".
- **Exception for Related Work**: narrative citations with the author as subject ("Li and Ning (2023) proposed...") are acceptable when summarizing a specific study's contribution, not for general claims. Under a hard page limit this exception narrows further, so see the Related Work section in [section-patterns.md](section-patterns.md).
- When listing multiple supporting references, group them at the end: "(Author1 et al., Year; Author2 and Author3, Year)".
- Use citation-dense sentences in the Introduction to establish context without over-explaining each source.
- **Cite general framing and definitional claims.** Statements about standardization efforts, the state of a field, or what a technology is should carry a citation rather than stand bare.
- **Cite the author's own relevant prior work wherever appropriate** (for this author, Mingke Li / Mingke Erin Li). In a double-blind manuscript, cite it in the third person like any other source.

## Verification

- **Verify a citation actually supports the claim it is attached to.** Do not cite a source, or a paper section, that only appears relevant. Confirm the source makes the specific point before attaching it, and do not claim "Section X traces this lineage" unless that section really cites those works.
- **In grouped citations, attach each specific finding only to the papers that report it.** A finding measured by one paper (for example, accuracy declining as reasoning steps increase) must not be attributed to co-cited papers that show something weaker or different. Split the sentence so each claim ends with its own supporting sources, and check the sources themselves, not memory of them.
- **Re-check attribution after every trim, because compression is what breaks citations.** Cutting a paragraph to fit a limit is the operation that merges two sources into one bracket and attaches a finding to a paper that does not report it. In one case a conformance audit and a research-agenda paper were grouped as `[5,6]` for a data-model claim only the second makes. Trimming also orphans references and inverts first-appearance numbering. Treat any length cut as a trigger to re-run the grouped-citation, orphan, and numbering checks together, and compute the numbering from the text rather than adjusting it by hand.
- **Verify negative claims about prior work at method depth before writing them.** A statement that other work "does not do X" can be narrowed once their method is read (a system may run its own correction loop, just not the one you claim is unique). Scope the gap statement to what the method actually shows.
- **Verify every reference before inserting it.** Confirm the DOI, author list, and year against the publisher. Never fabricate a DOI, author, or page range. If an author list cannot be fully verified (for example, a paper with 20+ authors), verify it fully or drop the citation rather than invent names. When a work was published online-first in one year and in an issue the next, cite the issue year.
- **Check for orphan citations during revision.** Every in-text citation must have a matching reference-list entry, and every entry must be cited at least once. Re-run this check whenever a section is rewritten.
- **Cite the published record, not the preprint, once one exists.** When an arXiv paper has since appeared in archival proceedings or a journal, cite that record with volume and pages, and re-check the published title and author order against the publisher, because both can differ from the preprint. Titles gain subtitles like "(vision paper)", and author order can change between versions.

## Numbering during drafting

While drafting a multi-section document, number citations from [1] within each section and end the section with a numbered list of what it cites. Renumber across the whole document only at assembly, computing the numbering from the text.

## Venue mechanics: IJGIS / Taylor & Francis Reference Style V (Harvard B)

Verified against `tf_v.pdf` and typeset IJGIS reference lists (2026-08-04).

Reference list:

- "Surname, I." with initials closed up.
- Comma before "and" in two- and three-author lists ("Cohn, A.G., and Blackwell, R.E., 2024.").
- 4+ authors become "Surname, I., et al., Year."
- Sentence-case article titles; italic journal names in title case.
- "volume (issue), pages" with an en dash and no "vol."/"pp.".
- Roman "In:" for proceedings.
- NO DOIs on journal or conference entries. Datasets and online resources instead use "Available from: https://doi.org/... [Accessed D Month YYYY]".
- arXiv-only work as "*arXiv preprint arXiv:NNNN.NNNNN*" in the journal slot.
- Software as "*Name* (version X) [software]. Distributor. Available from: URL [Accessed date]."

In text:

- No comma between name and year: "(Stevens 1988)".
- "et al." for three or more authors.
- Multiple citations in one parenthesis separated by commas in chronological order: "(Shi et al. 2022, Li et al. 2024)", not semicolons.
