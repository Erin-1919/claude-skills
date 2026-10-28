# Worked example: GridMind booth video (ACM SIGSPATIAL 2026 demo D-3577)

A silent 5:28 loop for a conference booth: animated intro, two live-app replays with agent chats, a bridge between them, a closing card. Source: `E:\UCalgary_postdoc\dggs_spatial_reasoning\acmgis\video\` (`DESIGN.md` is the storyboard and decision record, `NARRATION.md` the presenter's script, `intro/` the scenes, `record/` the recorders, `post/assemble.mjs` the assembly). Read it for patterns; do not copy its content.

## Structure

| Part | Length | Content |
|---|---|---|
| Intro: title | 6 s | Title, authors, affiliation, logos, paper ID |
| Intro: problem | 11 s | Heading "LLMs can violate Tobler's First Law of Geography"; a two-well example: the question, the LLM's wrong answer, the ground truth |
| Intro: method | 22 s | rHEALPix globes from the paper figure, a coloured cube net and a turning sphere of the six base cells, zoom into one cell, then a 3×3 grid showing the cell-ID hierarchy, containment, adjacency |
| Intro: evidence | 8 s | Score ranges counting up for the method and the baseline, prompt-token bars |
| Intro: architecture | 16 s | The paper's architecture diagram built layer by layer, messages pulsing along each channel |
| Intro: hand-off | 6 s | Two case-study cards; one dims, the other gets its colour ring, the camera moves into it |
| Demo 1 | about 130 s | Full-screen walkthrough with channel-tagged captions, panel tour, three chats |
| Bridge | 6 s | Same cards, the other one chosen, same transition |
| Demo 2 | about 115 s | As demo 1 |
| Close | 10 s | Summary line, links, logos |

## Decisions the user made, with why

- Off-screen headless render, never screen capture: smooth, reproducible, 4K, the machine stays free.
- One round per scenario: full screen once, then the full layout once; no repeated shots or captions.
- Captions in academic register; the method is "grounding", the baseline "coordinate inference" (calling both grounding credits the baseline).
- The problem's framing (Tobler's law) is the slide heading, not a note under the example.
- Abstract identifiers (face letters N to S) are shown as a picture (cube net and sphere in matching colours), never as bare letters.
- A grid-agent chat in demo 2 was dropped because its popup was taller than the map; demo 1 already shows a grid-agent chat.
- Both case-study transitions use the same highlight; inconsistency between parallel parts was a review failure.

## Process lessons

- The user caught a covered popup and an inconsistent transition that self-review missed: run the full review checklist, including side-by-side comparison of parallel parts, before every hand-off.
- Monolithic renders (20 min) made small fixes expensive; segments brought one fix to about 5 minutes. Segment from the start.
- Contact sheets of stills (seconds) caught most layout bugs before any full render: the empty grid square behind the globes, a hard clip edge, tiny canvas labels, a zoom that spilled over the text column.
- The narration drifted from the cut twice; regenerate its section times from the timing table after every change in length.
