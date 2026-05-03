# Smart Class PPT Generation Guide

This guide defines non-visual production rules for Smart Class presentation decks. Use this file together with `DESIGN.md`: `DESIGN.md` controls the visual system, while this guide controls source usage, slide logic, chart construction, diagram construction, evidence handling, and quality checks.

## 1. Source Of Truth

Use the `docs` repository as the source of truth. Do not treat an existing PPT as the primary source of factual content.

Priority order:

1. Current reports under `docs/08-reports`.
2. Current requirements, architecture, ADRs, status, and risk documents.
3. Meeting digests and raw notes only when current truth documents do not cover the topic.
4. Existing PPT files only as references for story order, historical framing, or examples of what was previously shown.

When the existing PPT and docs disagree, prefer docs. If the disagreement affects a major claim, state the uncertainty in working notes before generating the slide.

Source usage must remain mostly invisible to the audience. Use docs to decide what is true, but do not place labels such as `from docs`, `docs source`, `current truth`, `original preserved`, `reference maintained`, or `enhanced from existing PPT` inside the slide body. Those are production notes, not presentation content. Only show a source on the slide when the audience needs it to evaluate an external citation, a quoted number, a legal/policy claim, or a public reference.

## 2. Slide Intent Before Layout

Every slide must have a clear intent before layout work begins.

For each slide, define:

- Main claim: the one sentence the audience should remember.
- Evidence object: table, chart, diagram, screenshot, status board, or process flow.
- Supporting notes: labels, caveats, next-step implications, or audience-facing evidence notes.
- Required editability: what should remain editable in PowerPoint.

Do not create a slide only because a section needs visual variety. Each slide should explain, compare, prove, or transition.

Before writing visible slide text, ask: “Would the presenter naturally say this to an evaluator or audience?” If the answer is no, remove it from the slide. Keep production rationale, source mapping, comparison against the old PPT, and self-evaluation notes outside the deck.

## 3. Use Existing PPTs Correctly

Existing PPTs are references, not truth sources.

Use them for:

- Section order.
- Approximate slide count.
- Audience expectation.
- Previously used terminology.
- Identifying diagram types that need to be rebuilt.

Do not use them for:

- Copying outdated facts.
- Reusing rasterized diagrams as final diagrams.
- Preserving unclear layout decisions.
- Treating screenshots of diagrams as authoritative models.

## 4. Editable Objects By Default

All charts, tables, architecture diagrams, network topology diagrams, ERDs, sequence diagrams, flowcharts, status boards, and priority matrices must be built as editable PowerPoint objects by default.

Use raster images only for:

- Product or UI screenshots.
- Official logos or brand assets.
- Photographs.
- Reference images explicitly requested by the user.

Never paste a diagram screenshot as the final diagram if it can reasonably be rebuilt with shapes, text, and connectors. Use real table objects for tabular parts of a diagram.

For tables, use real PowerPoint table functionality or a native table object. Do not construct table-looking objects from many separate rectangles and text boxes.

## 5. Diagram Rules

Diagrams must explain relationships, not just list objects.

Every diagram should answer:

- What are the nodes?
- What connects to what?
- What flows across the connection?
- In which direction does it flow?
- What decision or state changes because of that flow?

Every connection line should have a purpose. Add labels such as `API request`, `station snapshot`, `eligibility check`, `registered device lookup`, `audit log write`, or `status update` when the connection meaning is not obvious.

If a diagram is too risky or time-consuming to draw manually with correct geometry, use a reliable Mermaid rendering workflow instead of creating a weak pseudo-diagram. Install or use an available Mermaid CLI/rendering tool when needed, render the diagram cleanly, and verify that the output is legible at slide size. Prefer editable PPT shapes when feasible, but a correct, readable Mermaid-rendered diagram is better than an incorrect hand-built diagram. If Mermaid is used, keep the source `.mmd` or equivalent working file with the deck workspace so the diagram can be regenerated.

## 6. Network Topology Diagrams

Network topology diagrams must show both physical/network connections and data interpretation.

Include, when relevant:

- Student device to OpenWrt AP: Wi-Fi association.
- PresenceService to OpenWrt AP: SSH or device-specific station-list query when the cache is missing or stale.
- OpenWrt AP to PresenceService: station list with MAC, signal, and last-seen evidence.
- Future collector or adapter plans must be labeled as future work, not as the current production data path.
- PresenceService to Redis: snapshot cache.
- Backend to PresenceService: eligibility check.
- Backend to DB: registered devices, classroom networks, attendance sessions.
- Backend to Front: attendance status, reason code, feedback.

Do not show APs, classrooms, and devices as isolated boxes. The topology must explain how network evidence becomes attendance evidence.

## 7. System Architecture Diagrams

System architecture diagrams must preserve module order and dependency direction.

Show:

- Entry point.
- Frontend.
- Reverse proxy or gateway.
- Backend API.
- PresenceService.
- Database.
- Redis or cache.
- Object storage, if relevant.
- External or physical devices.

Use arrows to show request direction and data dependencies. Avoid rearranging modules only for visual symmetry if that changes the meaning of the architecture.

## 8. Sequence Diagrams

Sequence diagrams must follow sequence-diagram conventions.

Required elements:

- Participants as vertical lifelines.
- Request arrows.
- Response arrows.
- Activation or processing regions when useful.
- `alt`, `opt`, or failure blocks when the flow has branches.
- Message labels that match API or domain language from docs.
- Time must flow clearly from top to bottom.
- Each message must connect exactly two participants.
- Arrows must show direction; response messages should use a visually distinct return style.
- Branches such as cache hit/cache miss must be shown as `alt`/`else` blocks, not as ordinary rows.

Do not convert a sequence diagram into a generic table, swimlane table, card list, or timeline. A slide that only looks like a table with participant names is not a sequence diagram. If a proper editable sequence diagram cannot be built quickly, render a Mermaid `sequenceDiagram` and use that instead.

## 9. ERD Rules

ERDs must show relationships, not just entity boxes.

Each ERD should include:

- Entity name.
- Primary key marker.
- Foreign key marker.
- Essential fields only.
- Relationship lines.
- Cardinality markers or labels where important.
- A short note explaining why these entities matter for the slide claim.

Do not include the full database schema unless the slide is explicitly an appendix. For main-body slides, show only the subset needed for the story.

## 10. Tables And Priority Matrices

If the source is a table, keep it as a table or matrix. Do not convert it into unrelated cards unless the user explicitly asks for a more editorial interpretation.

Tables must be actual table objects. Do not fake a table by aligning multiple independent shapes, even if the result looks like a table in the screenshot.

Good tables should have:

- Clear columns.
- Stable row heights.
- A header row.
- Compact but readable text.
- Highlighting for only the most important cells.
- No decorative color noise.

Priority tables should preserve ranking. Use numeric rank, feature name, purpose, status, and dependency where useful.

## 11. Charts And Graphs

Only create charts from real data found in docs or user-provided sources. Do not invent numbers to make a chart look complete.

Before making a chart:

- Identify the metric.
- Identify the unit.
- Identify the time period or scope.
- Identify the source document.
- Decide the intended comparison.

Chart selection:

- Bar chart: compare categories.
- Stacked bar: show composition.
- Line chart: show change over time.
- Scatter plot: show relationship between two numeric variables.
- Waterfall: show contribution from starting value to ending value.
- Heatmap: show matrix intensity.
- Small multiples: compare the same metric across groups.

If exact numeric data is unavailable, use a qualitative matrix or status board instead of a fake chart.

## 12. Status Boards

Status boards should separate progress, evidence, and risk.

Recommended fields:

- Area.
- Completed.
- In progress.
- Remaining.
- Evidence.
- Risk or blocker.

Avoid long bullet lists. Use structured lanes, status chips, or compact tables.

## 13. Screenshots

Screenshots are evidence objects, not decoration.

For every screenshot slide:

- Crop to the meaningful area.
- Make at least one screenshot large enough to inspect.
- Add a short label that explains what the viewer should notice.
- Pair screenshots with status or implication notes.

Do not place many tiny screenshots on one slide unless the purpose is a gallery or appendix.

## 14. Content Density

Dense slides are allowed when the structure is clear.

Good density:

- Grouped information.
- Tables with clear columns.
- Diagrams with labeled connections.
- Summary strips.
- Status chips.
- Callouts tied to evidence.
- Bottom strips that summarize the slide's actual implication, decision, risk, or next action.

Bad density:

- Unstructured bullet lists.
- Tiny unreadable screenshots.
- Multiple unrelated proof objects.
- Large pasted diagrams with no explanation.
- Decorative cards that do not add meaning.
- Bottom strips filled with process notes, source labels, old-vs-new commentary, or generic filler.
- Notes such as `original preserved`, `docs-based`, `enhanced`, `reference maintained`, or `this slide was updated`.

## 15. Claims And Evidence

Each factual claim should be supported by visible evidence or traceable source context.

Examples:

- Claim: “Attendance is judged through registered device and classroom network evidence.”
  Evidence: flow diagram showing Backend, PresenceService, registered devices, classroom networks, and eligibility result.
- Claim: “The current implementation covers login, dashboard, device management, attendance, and exam MVP.”
  Evidence: status board or screenshots with labeled completed areas.

Do not let a slide make claims that are stronger than the underlying docs.

Traceability is a production requirement, not always a visible slide requirement. Keep detailed source mapping in working notes or appendix material unless the audience needs the source to judge the claim. The main deck should contain the claim, evidence, implication, and caveat that the presenter actually needs.

## 16. Terminology

Use consistent project terminology.

Preferred terms:

- Smart Class.
- LMS.
- Front.
- Backend.
- PresenceService.
- OpenWrt.
- Redis.
- PostgreSQL.
- registered device.
- classroom network.
- eligibility check.
- attendance session.
- reason code.
- audit log.

Do not casually rename the same concept across slides.

## 17. Korean And English Text

Slide content may be Korean, English, or mixed depending on the source material and audience. Technical identifiers should remain stable.

Rules:

- Keep API paths in English.
- Keep service names as written in docs.
- Do not translate `PresenceService`, `OpenWrt`, `Redis`, or `Backend` inconsistently.
- Avoid mid-word line breaks.
- Use short Korean labels when possible.

## 18. Speaker-Oriented Structure

Slides should help the presenter speak.

The PPT is for evaluators and listeners, not for the deck-generation process. Visible text should be content the audience needs to understand the project, the system, the evidence, the risk, or the next decision. Do not include self-referential generation notes, internal scoring comments, source-routing explanations, or statements about how the slide was modified from an earlier deck.

Each slide should support one of these functions:

- Introduce.
- Explain.
- Compare.
- Prove.
- Show progress.
- Identify risk.
- Transition.

Avoid slides that require the presenter to explain why the visual exists.

Avoid slides that are technically accurate but audience-useless. If a bottom area is empty, fill it only with a useful implication, risk, legend, decision rule, or proof detail. Leaving a clean lower area is better than adding irrelevant filler.

## 19. Team Introduction Slides

Team introduction slides should make the people immediately recognizable and avoid over-labeling.

Rules:

- Keep member photos large enough to read as portraits in presentation mode.
- Preserve the original portrait crop and aspect ratio.
- Show a role badge only for the team leader, unless the user explicitly asks to label every member's role.
- For non-leader members, show the member name and the most relevant contribution or interest area without a separate role chip.
- Do not add a generic collaboration-standard or production-process box unless it contains audience-essential information.
- If a team slide needs more density, use contribution areas, implementation ownership, or evidence of responsibility instead of decorative filler.

## 20. Verification Checklist

Before delivering a PPT:

- Confirm slide count.
- Confirm 16:9 page size.
- Confirm Smart Class logo usage.
- Confirm `DESIGN.md` visual rules are followed.
- Confirm this guide’s source and diagram rules are followed.
- Confirm diagrams are editable shapes unless explicitly image-based.
- Confirm no major text clipping or numeric clipping exists.
- Confirm tables are real PowerPoint/native table objects, not table-like assemblies of shapes.
- Confirm ERDs have relationship lines.
- Confirm sequence diagrams have lifelines and directional messages.
- Confirm sequence diagrams are not generic tables or card lists; use Mermaid rendering if necessary.
- Confirm screenshots are readable.
- Confirm no visible slide text says `from docs`, `original preserved`, `enhanced`, `reference maintained`, or similar production commentary.
- Confirm every lower-third filler, summary strip, and note is useful for the evaluator or audience.
- Convert to PDF and verify page count.
- Render slide previews and inspect thumbnail rhythm.

## 21. Evaluation Criteria

Use these criteria when scoring a generated PPT. A deck should not be considered complete if any criterion is below 90.

- Audience usefulness: every slide contains only what an evaluator or listener needs to understand the presentation.
- Content preservation: existing required content is not silently removed, but it may be corrected or strengthened from current sources.
- Source fidelity: facts follow the source-of-truth documents, while source-routing notes stay out of the main slide body.
- Diagram correctness: topology, architecture, sequence diagrams, ERDs, tables, and charts preserve the actual relationships.
- Sequence-diagram quality: sequence slides use real sequence conventions or Mermaid-rendered sequence diagrams.
- Table correctness: tables are native tables, not shape collages.
- Evidence clarity: screenshots, diagrams, and tables are large enough to inspect.
- Useful density: lower slide areas are filled only with meaningful evidence, implications, legends, or risks.
- Design-system compliance: `DESIGN.md` is followed.
- Readability and delivery: the presenter can speak from the slide without explaining production context.

## 22. When Unsure

If source content is unclear, do not guess. Use the most conservative representation:

- Use “planned”, “in progress”, or “to verify” labels.
- Prefer qualitative status over invented numbers.
- Prefer a small, accurate diagram over a large, speculative one.
- Add a quiet caveat instead of overclaiming.

The goal is a presentation that is clear, editable, evidence-based, faithful to the source-of-truth documents, and useful to the evaluator or audience.
