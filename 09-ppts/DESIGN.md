---
version: alpha
name: Smart Class Presentation System
description: "A restrained blue, Apple-inspired presentation design system for Smart Class decks. The system is optimized only for 16:9 PowerPoint slides, uses Pretendard as the sole typeface, applies the official Smart Class logo asset, and keeps slide titles, subtitles, chapter labels, and footers in stable positions across the deck. It favors dense but calm information design: every slide should feel intentional, readable, and well-filled without visual clutter."

assets:
  logo:
    path: "assets/brand/smartclass-logo.png"
    usage: "Use this Smart Class logo only. Do not use, trace, approximate, or reference the Apple logo."
    placement: "Use as a small identity mark in the top-left or footer-left depending on the slide type."

slide:
  aspectRatio: "16:9"
  size: "20in x 11.25in"
  orientation: "landscape"
  rule: "Generate only 16:9 slides. Do not create 4:3, square, poster, web-page, or mobile layouts."

colors:
  primary: "#0066CC"
  primary-focus: "#0071E3"
  primary-on-dark: "#2997FF"
  navy-950: "#07172B"
  navy-900: "#0B1F3A"
  navy-800: "#102A4C"
  navy-700: "#173B69"
  ink: "#1D1D1F"
  body: "#273142"
  body-muted: "#65758B"
  body-on-dark: "#FFFFFF"
  body-muted-on-dark: "#C7D2E2"
  canvas: "#FFFFFF"
  canvas-soft: "#F5F7FA"
  canvas-blue: "#EEF5FF"
  surface: "#FAFBFD"
  surface-raised: "#FFFFFF"
  hairline: "#DDE5EF"
  divider-soft: "#EAF0F7"
  success: "#1F8A5B"
  warning: "#C88719"
  danger: "#D64545"
  on-primary: "#FFFFFF"

typography:
  fontFamily: "Pretendard"
  rule: "Use Pretendard only. Do not use any other font, fallback stack, mixed typeface, or system-default typeface in generated slides."
  sizeRule: "Use integer point sizes only. Do not use fractional font sizes such as 11.5pt, 9.5pt, or 8.8pt."
  scaleRule: "Use a type scale approximately 15% larger than the previous Smart Class deck scale while preserving hierarchy and preventing text overflow."
  audienceMinimumRule: "Any text the audience is expected to read during the presentation must be at least 14pt in the final PPTX. This includes subtitles, body text, labels, table cells, diagram labels, sequence messages, ERD fields, and meaningful captions."
  auxiliaryTextRule: "Use 9pt only for text the audience does not need to read closely, such as quiet footer metadata, slide numbers, tiny logo lockups, or optional URL captions beside QR codes."
  contrastRule: "Audience-facing text must have strong contrast against its actual rendered background in Microsoft PowerPoint, not only in the generator preview. Normal body/title text should target WCAG contrast 7:1 or stronger when feasible and must never fall below 4.5:1. Large display text must never rely on black text over navy/dark backgrounds or pale blue text over low-contrast blue surfaces. Verify dark slides in rendered PowerPoint/PDF output."
  cover-title:
    fontFamily: "Pretendard"
    fontSize: 58pt
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: 0
  cover-subtitle:
    fontFamily: "Pretendard"
    fontSize: 21pt
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0
  chapter-number:
    fontFamily: "Pretendard"
    fontSize: 21pt
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 0
  chapter-title:
    fontFamily: "Pretendard"
    fontSize: 44pt
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: 0
  chapter-subtitle:
    fontFamily: "Pretendard"
    fontSize: 17pt
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0
  slide-title:
    fontFamily: "Pretendard"
    fontSize: 29pt
    fontWeight: 700
    lineHeight: 1.16
    letterSpacing: 0
  slide-subtitle:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0
  section-label:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 700
    lineHeight: 1.0
    letterSpacing: 0
  body:
    fontFamily: "Pretendard"
    fontSize: 16pt
    fontWeight: 400
    lineHeight: 1.42
    letterSpacing: 0
  body-strong:
    fontFamily: "Pretendard"
    fontSize: 16pt
    fontWeight: 700
    lineHeight: 1.36
    letterSpacing: 0
  body-small:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: 0
  table-header:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 700
    lineHeight: 1.18
    letterSpacing: 0
  table-cell:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 400
    lineHeight: 1.24
    letterSpacing: 0
  agenda-title:
    fontFamily: "Pretendard"
    fontSize: 20pt
    fontWeight: 700
    lineHeight: 1.18
    letterSpacing: 0
  agenda-description:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 400
    lineHeight: 1.24
    letterSpacing: 0
  diagram-label:
    fontFamily: "Pretendard"
    fontSize: 14pt
    fontWeight: 500
    lineHeight: 1.18
    letterSpacing: 0
  caption:
    fontFamily: "Pretendard"
    fontSize: 9pt
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0
  footer:
    fontFamily: "Pretendard"
    fontSize: 9pt
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: 0

grid:
  marginLeft: 0.83in
  marginRight: 0.83in
  marginTop: 0.40in
  marginBottom: 0.40in
  titleX: 0.83in
  titleY: 1.02in
  titleW: 15.63in
  titleH: 0.56in
  subtitleX: 0.83in
  subtitleY: 1.56in
  subtitleW: 15.63in
  subtitleH: 0.35in
  headerRuleX: 0.83in
  headerRuleY: 2.08in
  headerRuleW: 18.33in
  headerRuleH: 0.01in
  headerRuleClearance: "Keep at least 0.16in of vertical clearance between the subtitle text box bottom and the header divider line. The standard subtitle frame ends at 1.91in, so the divider at 2.08in must never touch or overlap subtitle descenders."
  logoX: 0.83in
  logoY: 0.25in
  logoH: 0.35in
  footerY: 10.69in
  contentTop: 2.29in
  contentBottom: 10.42in
  contentW: 18.33in
  columnGap: 0.23in
  rowGap: 0.19in

layoutRules:
  stableHierarchy: "Keep chapter names, slide titles, subtitles, logo, and footer elements in consistent positions across all normal slides."
  titleDiscipline: "Every content slide uses the same title anchor unless it is a cover, chapter divider, Q&A, or closing slide."
  subtitleDiscipline: "Use subtitles for explanatory context, not decorative taglines. Keep them under the title in a fixed position. The title, subtitle, and header divider must be separate objects with fixed frames; do not place title and subtitle inside an auto-height group that can collide with the divider."
  headerDividerSafety: "Place the standard header divider at grid.headerRuleY only. The line must sit below the subtitle safe area, not through it. If a subtitle needs two lines, shorten the subtitle or move the entire content area down; never let the divider overlap the subtitle."
  backgroundShapePolicy: "Do not add a full-slide white rectangle on normal content slides when the slide canvas is already white. Use background shapes only when they create a visible band, dark chapter background, screenshot frame, diagram surface, or other meaningful visual layer."
  textSafeArea: "Text must never touch, cross, or visually collide with a shape boundary. Every text object inside a card, chip, table cell, or framed panel must keep generous internal padding and a visible safety gap from the border."
  contrastSafety: "A slide fails QA if text color is too close to the background, even when the layout, font size, and alignment are otherwise correct. Dark backgrounds require white or near-white text; blue accent text may be used only when contrast remains clearly readable."
  noMidWordBreaks: "Do not allow words to break in the middle. Rewrite, shorten, resize, widen the text box, or insert manual line breaks only between semantic phrases. Never split Korean, English, numbers, API names, file names, or technical terms across lines."
  generousTextBoxes: "Create text boxes wider than the expected text, not just exactly equal to the visual label width. Korean names, short labels, role names, and section tags must have enough width to remain on one line unless an intentional manual line break is specified."
  levelAlignment: "Content at the same semantic level must share the same baseline, top edge, and visual grouping. Names align with names, roles align with roles, captions align with captions, and card labels align with other card labels."
  sameLineGrouping: "When two items belong together, such as a person's name and role, keep them in the same visual group with a stable baseline. Do not let one item wrap downward while the paired item stays on the first line."
  bottomDensity: "Do not leave the lower third of content slides empty. Fill it only with audience-useful proof objects, callouts, legends, caveats, status, implications, or concise takeaways. Do not fill space with production notes, source-process labels, 'original preserved' notes, or other meta commentary that the presenter would not say aloud."
  densityLimit: "Increase density through structure, not clutter. Prefer real tables, aligned diagrams, compact evidence rows, and useful summary strips over random floating text."
  cardRestraint: "Avoid card-based layouts unless cards are genuinely needed to separate otherwise ambiguous content groups. Do not use cards as the default page structure, as decorative containers, or to fill empty space. If alignment, spacing, a real table, or a direct diagram can separate the content clearly, use those instead of cards."
  nativeTablePolicy: "When a slide requires a table, use a real PowerPoint table or a native table component. Do not build fake tables by manually placing many separate rectangles, text boxes, and lines to imitate table rows and columns."
  whitespace: "Use whitespace to separate hierarchy, but avoid empty presentation pages unless the slide is a chapter divider or closing slide."
  alignment: "All objects must align to the grid. Avoid approximate centering and accidental offsets."
  textFitting: "If text risks overflowing or colliding with a boundary, reduce the copy first, then reduce font size slightly, then increase the container width or height. Do not accept clipped text, border collisions, or cramped cards."
  labelSizing: "Short Korean labels must be given enough width for a single-line rendering. Never place labels such as names, roles, section tags, or summary-strip labels in narrow boxes that force syllable-by-syllable wrapping."
  numberBoxSafety: "Numbers inside square or rounded index boxes must never touch or clip against the left, right, top, or bottom edge. Give numeric labels extra internal padding and place them in a slightly inset text box. Do not align large numbers directly to the container edge."
  editableDiagramPolicy: "All diagrams, charts, tables, flows, architecture maps, sequence diagrams, ERDs, and status boards should be built from editable PowerPoint shapes and text by default. Do not paste diagram screenshots unless the user explicitly requests an image-based reference."

components:
  logo-mark:
    asset: "{assets.logo.path}"
    height: 0.24in
    placement: "{grid.logoX}, {grid.logoY}"
  standard-header:
    title: "{typography.slide-title}"
    subtitle: "{typography.slide-subtitle}"
    titlePosition: "{grid.titleX}, {grid.titleY}"
    subtitlePosition: "{grid.subtitleX}, {grid.subtitleY}"
    dividerPosition: "{grid.headerRuleX}, {grid.headerRuleY}"
    rule: "Use on most content slides. Title, subtitle, and divider are fixed separate objects; the divider stays below the subtitle with at least grid.headerRuleClearance."
  footer:
    typography: "{typography.footer}"
    color: "{colors.body-muted}"
    placement: "Bottom-left deck label and bottom-right slide number."
    rule: "Keep footer quiet but present on all slides except intentional full-bleed cover or closing pages."
  chapter-divider:
    backgroundColor: "{colors.navy-900}"
    textColor: "{colors.body-on-dark}"
    accentColor: "{colors.primary-on-dark}"
    rule: "Use large chapter number and chapter title in fixed positions. Do not add dense body content."
  content-card:
    backgroundColor: "{colors.surface-raised}"
    borderColor: "{colors.hairline}"
    rounded: 8px
    padding: "0.18in minimum; 0.22in preferred for paragraph cards"
    shadow: "none"
    rule: "Use only when the card boundary is necessary for comprehension. Card text must sit comfortably inside the card. Do not place text close to the border."
  emphasis-card:
    backgroundColor: "{colors.canvas-blue}"
    borderColor: "{colors.primary}"
    rounded: 8px
    padding: 0.18in
    shadow: "none"
  summary-strip:
    backgroundColor: "{colors.canvas-soft}"
    borderColor: "{colors.divider-soft}"
    height: "0.48in to 0.75in"
    placement: "Use near the bottom of content slides when the main visual leaves empty space."
    rule: "Summarize the slide in 2-4 compact points or metrics."
  status-chip:
    backgroundColor: "{colors.canvas-blue}"
    textColor: "{colors.navy-800}"
    rounded: 9999px
    typography: "{typography.caption}"
    padding: "0.05in 0.12in"
  index-number-box:
    backgroundColor: "{colors.canvas-blue}"
    textColor: "{colors.primary}"
    activeBackgroundColor: "{colors.navy-900}"
    activeTextColor: "{colors.body-on-dark}"
    rounded: 8px
    minPadding: "0.10in left/right and 0.08in top/bottom"
    rule: "The number text must be inset from all edges. If the number appears visually clipped, widen the box or shift the text inward before exporting."
  table:
    headerFill: "{colors.canvas-blue}"
    headerText: "{colors.navy-900}"
    cellText: "{colors.body}"
    borderColor: "{colors.hairline}"
    borderWidth: 0.6pt
    rowStripe: "{colors.surface}"
    rule: "Use a real PowerPoint table or native table object with thin lines, compact rows, and selective blue emphasis. The first row must be treated as the table header whenever it contains column labels or contents labels, and every header cell must have a visible pale-blue background fill. Avoid heavy borders and do not fake table structure with grouped rectangles."
  agenda-table:
    tableType: "native PowerPoint table"
    titleTypography: "{typography.agenda-title}"
    descriptionTypography: "{typography.agenda-description}"
    columns: "Two columns only: a narrow number tab on the left and a wide title/description tab on the right."
    headerPolicy: "Do not add a header row such as Number, Contents, or Description to the agenda table."
    backgroundPolicy: "All agenda table cell backgrounds must be transparent. Do not use header fills, row stripes, number-tab fills, or white table-surface fills behind agenda items."
    borderPolicy: "Use only a thin bottom border for each agenda row. Do not draw top, left, right, vertical, outer-table, inner-column, or full-cell borders. Explicitly disable inherited PowerPoint table-style borders so no black outer border or divider appears."
    columnWidth: "The number column should be only wide enough to hold a two-digit section number comfortably, approximately 0.85in to 1.10in on the 20in-wide slide. Give the remaining table width to the title/description column."
    numberTab: "Use a compact left cell for the section number. Align number text to the right and center it vertically."
    textTab: "Use one wide right cell per agenda item. Place the bold 20pt title above the 14pt description inside the same cell. Align title and description text to the left and center the cell content vertically."
    rule: "Build the table-of-contents slide as a real table, not as cards. Each agenda row has one number tab and one title/description tab. Each agenda item's title must be bold 20pt, and each description must be 14pt."
  architecture-diagram:
    nodeFill: "{colors.surface-raised}"
    nodeBorder: "{colors.hairline}"
    activeNodeFill: "{colors.canvas-blue}"
    activeNodeBorder: "{colors.primary}"
    connector: "{colors.body-muted}"
    rule: "Use editable PPT shapes and text. Use at most three semantic colors. Make flow direction obvious."
  sequence-diagram:
    diagramArea: "Left or center visual proof area"
    explanationArea: "Right or bottom summary area"
    rule: "Build lifelines, participants, messages, returns, and alt blocks as editable PPT shapes and text. Do not paste a small unreadable screenshot alone. Pair it with a concise 3-step narrative."
  erd-diagram:
    backgroundColor: "{colors.canvas}"
    entityFill: "{colors.surface-raised}"
    headerFill: "{colors.canvas-blue}"
    keyColor: "{colors.primary}"
    connectorColor: "{colors.body-muted}"
    rule: "Build ERDs from editable entity boxes, rows, key markers, and connector lines. Show only the necessary fields for the current story; avoid full-schema screenshots."
  screenshot-frame:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.hairline}"
    rounded: 6px
    padding: 0.08in
    shadow: "none"
    rule: "Screenshots should be large enough to inspect. Add short labels, not paragraphs."
  portrait-frame:
    backgroundColor: "{colors.surface-raised}"
    borderColor: "{colors.hairline}"
    rounded: 6px
    padding: 0.06in
    imageFit: "contain"
    rule: "Portrait photos must preserve the original image ratio and full crop. Do not use cover-crop, face-crop, circle-crop, or any crop that removes parts of the source portrait."

slidePatterns:
  cover:
    background: "{colors.navy-900}"
    logo: "Use {assets.logo.path}; place small and clean."
    title: "{typography.cover-title}"
    subtitle: "{typography.cover-subtitle}"
    rule: "Strong first impression, minimal metadata, no Apple branding."
  agenda:
    background: "{colors.canvas}"
    rule: "Use numbered rows with thin separators. Keep enough density to show the full story arc."
  chapter:
    background: "{colors.navy-900}"
    rule: "Use fixed chapter number, fixed chapter title, and a short subtitle. Do not add unrelated body objects."
  problem:
    background: "{colors.canvas}"
    rule: "Use one clear claim, 2-3 evidence blocks, and a bottom summary strip if the visual area is sparse."
  goal:
    background: "{colors.canvas}"
    rule: "Use a left claim column and right proof or mockup. Use blue only for the target state."
  requirements:
    background: "{colors.canvas}"
    rule: "Use compact tables with grouped rows. Highlight only the changed or critical requirements."
  architecture:
    background: "{colors.canvas}"
    rule: "Use a clean system map and a bottom strip explaining responsibilities or data flow."
  progress:
    background: "{colors.canvas}"
    rule: "Use screenshots or deliverables as proof. Fill unused lower space with completed/in-progress/next status."
  database:
    background: "{colors.canvas}"
    rule: "Use large ERD crops plus a concise explanation. Do not place tiny full-schema images without callouts."
  sequence:
    background: "{colors.canvas}"
    rule: "Use one readable diagram crop plus a short numbered flow explanation."
  closing:
    background: "{colors.navy-900}"
    rule: "Use logo, a short closing line, and quiet footer metadata. Keep it clean."

chartRules:
  barCharts: "Use navy for baseline values and primary blue for the key value. Avoid rainbow palettes."
  flowCharts: "Use white nodes, blue active nodes, and gray connectors. Keep connector lines thin."
  tables: "Use native table objects with compact row heights. If content is long, split into grouped tables or move detail into notes. Never imitate a table with manually aligned boxes."
  screenshots: "Crop to the useful area. Pair each screenshot with one label and one insight."
  diagrams: "If a diagram is visually dense, enlarge it and move explanatory text to a structured side panel."
  emphasis: "Prefer blue emphasis, bold Pretendard, or a thin left accent bar. Use red only for true risk or error."
  textInShapes: "Use short labels inside shapes. If a label needs more than two lines, move the explanation outside the shape or use a larger panel."
  editableByDefault: "Prefer editable PPT shapes over raster images for every chart and diagram. A diagram slide should remain easy to edit in PowerPoint without re-exporting an image."

dos:
  - "Use Pretendard for every text object."
  - "Use only 16:9 slide dimensions."
  - "Use assets/brand/smartclass-logo.png as the only logo."
  - "Keep titles, subtitles, chapter labels, logos, and footers in stable positions."
  - "Maintain a restrained blue palette with white and blue-gray surfaces."
  - "Fill the lower content area with useful structured information when the main visual leaves empty space."
  - "Make charts, tables, and diagrams readable at presentation distance."
  - "Use dense layouts only when structure and alignment preserve clarity."
  - "Preserve portrait photos with their original crop and aspect ratio."
  - "Keep text away from shape borders with clear internal padding."
  - "Manually break long text only at phrase boundaries."
  - "Make text boxes generously wider than the visible text whenever labels must stay on one line."
  - "Align same-level content on the same row or baseline."
  - "Inset large numbers inside index boxes so no digit is clipped at the edges."
  - "Build diagrams and charts with editable PowerPoint shapes by default."
  - "Use cards only when they are necessary to separate content that would otherwise be hard to understand."
  - "Use native PowerPoint table functionality for tables."

donts:
  - "Do not use Apple logos, Apple product imagery, or Apple brand marks."
  - "Do not use any font other than Pretendard."
  - "Do not generate non-16:9 slides."
  - "Do not move the slide title or subtitle arbitrarily from page to page."
  - "Do not leave the bottom third empty on content-heavy slides."
  - "Do not overuse red text. Red is reserved for risk, error, or critical warnings."
  - "Do not create decorative gradients, floating ornaments, or heavy shadows."
  - "Do not use card grids as the default layout pattern or as a filler device."
  - "Do not create fake tables from many separate rectangles, lines, and text boxes."
  - "Do not paste unreadable full-size technical diagrams without cropping or explanation."
  - "Do not crop portrait photos with cover-fit or circular masks."
  - "Do not let text overlap, touch, or escape shape boundaries."
  - "Do not break words or technical terms in the middle of a line."
  - "Do not make narrow text boxes that force Korean names or labels to stack vertically."
  - "Do not separate same-level items into different visual rows unless the hierarchy intentionally changes."
  - "Do not place numeric labels flush against the left edge of a box."
  - "Do not use screenshots for diagrams, flowcharts, architecture maps, sequence diagrams, ERDs, or tables unless explicitly requested."

promptGuidance:
  language: "English"
  instruction: "All design-system prompts and generated instruction text should remain in English. Slide content may follow the source material language, but this DESIGN.md file and design-control prompts must stay English."
  generationBehavior: "When creating a deck from this system, treat the reference PPT as the content-density and hierarchy baseline, not as a style to copy exactly. Preserve the stable positions and improve clarity with restrained blue visual grammar."
---

# Smart Class Presentation Design System

This file defines the presentation design system for Smart Class decks. It is intentionally inspired by Apple's restraint, clarity, and disciplined hierarchy, but it is not an Apple-branded system. The deck must use the Smart Class logo, Smart Class content, Pretendard typography, and a blue enterprise presentation language. The deck should avoid default card-heavy SaaS layouts; use cards only when they materially improve comprehension.

The system is built for technical project presentations that contain screenshots, tables, diagrams, architecture maps, database models, sequence diagrams, requirements, and progress evidence. It should feel polished and calm, but it should not become sparse. A slide with a small visual in the center and an empty lower half is considered unfinished unless it is a chapter divider or closing slide.

## Core Rules

1. Use Pretendard only.
2. Use `assets/brand/smartclass-logo.png` as the only logo.
3. Generate only 16:9 slides.
4. Keep chapter names, titles, subtitles, logo, and footer locations stable.
5. Fill the lower content area with useful information when the slide would otherwise feel empty.
6. Keep text safely inside shapes with enough padding.
7. Preserve portrait photos with their original crop and aspect ratio.
8. Avoid mid-word line breaks; break only between phrases.
9. Use generous text boxes for names, labels, role tags, and summary-strip headings.
10. Keep same-level items aligned together on a stable baseline.
11. Keep numbers inside index boxes inset from the box edges.
12. Build all diagrams and charts as editable PowerPoint shapes by default.
13. Keep this design-system prompt in English.

## Visual Personality

The design should feel reliable, modern, and restrained. Blue is the trust signal, white is the reading surface, and blue-gray is the supporting structure. The deck should avoid loud decoration, heavy shadows, saturated multi-color palettes, and arbitrary icon noise.

Slides should be dense enough to communicate the current project state. Density should come from ordered information: real tables, status strips, callout rows, grouped evidence, readable diagrams, and concise labels. Do not solve empty space by adding decorative shapes, unnecessary cards, or presenter-irrelevant notes.

## Typography Principles

Pretendard is the entire typographic system. Use weight and size, not font changes, to show hierarchy. The normal hierarchy is:

- Cover title: 58pt / 700
- Chapter title: 44pt / 700
- Slide title: 29pt / 700
- Subtitle: 14pt / 400
- Body: 16pt / 400
- Strong body: 16pt / 700
- Small body: 14pt / 400
- Table header: 14pt / 700
- Table cell: 14pt / 400
- Caption/footer: 9pt / 400

All font sizes must be whole-number point values. Audience-facing content must not go below 14pt. If a slide feels cramped after this scale, revise the copy and layout first; do not fall back to fractional sizes or tiny table text.

Do not use negative letter-spacing. Korean and mixed Korean-English technical content reads more reliably with neutral tracking.

Do not permit mid-word line breaks. When a Korean, English, numeric, API, file, or technical term cannot fit, rewrite the sentence into shorter phrase groups, use manual line breaks between phrases, or resize the container. Never rely on automatic wrapping that splits a word or term.

Short labels and names must be treated as non-breaking visual units. A name like `김현석`, a role like `팀장`, or a label like `핵심 문장` must stay on one line by default. If it does not fit, widen the text box or reduce the font size before accepting a line break.

Large numeric labels require their own safety area. In agenda rows, section markers, step indicators, and page index boxes, never place the number flush to the container edge. Use a wider box, inset the text, and visually inspect the left edge of every digit before final export.

## Layout Principles

Normal content slides should share a consistent header system. The title should sit at the same top-left anchor, the subtitle should sit directly beneath it, and the logo/footer should not wander. This makes the deck feel coherent even when slide contents vary between tables, screenshots, diagrams, and status boards.

The body area begins below the header and should usually extend close to the footer. If a diagram, screenshot, or table does not naturally fill the body area, add a bottom summary strip, compact evidence row, risk/status row, legend, or 2-4 key takeaways only when those elements help the audience understand the slide. This keeps the slide informative without making it crowded.

Text inside cards, chips, tables, and diagram nodes must have a visible safety gap from all borders. If the text touches the boundary, the slide fails visual QA even if the words are technically readable.

Cards are not the default layout unit. Use them only when a visible boundary is necessary to distinguish people, modules, repeated evidence items, or comparable groups. Cards that repeat at the same level must align their internal elements. In a team grid, all portraits share the same frame size, all names share the same baseline, all role tags share the same baseline, and all interest captions share the same baseline. Do not let one card wrap differently from its peers.

## Diagram And Data Style

Technical diagrams should be clear before they are decorative. Use thin connectors, restrained blue highlights, and white or very light blue-gray node surfaces. Use at most three semantic colors in a diagram.

Tables should be real PowerPoint tables or native table components. Use thin borders, compact rows, and a pale blue header. When the top row contains column names, section names, or other contents labels, it is a header row and must use the table header fill, even if the table is visually simple. Do not leave header rows on a plain white background. Do not use heavy gridlines. Highlight only the most important row, column, or status. Do not simulate tables with many separate shapes.

Diagrams and charts should be editable PowerPoint objects by default. For Smart Class decks, network topology diagrams, architecture maps, sequence diagrams, ERDs, and status boards must be rebuilt with shapes, text boxes, and lines rather than pasted as screenshots. Priority tables and other tabular content must use real table objects, not manually assembled table-like rows.

Screenshots should be cropped and framed. A screenshot should not float alone; pair it with a short label, status chip, or insight panel.

Portrait photos are different from screenshots. Preserve the original portrait image as supplied, using contain-fit inside a clean rectangular frame. Do not crop faces, shoulders, hair, or document-photo margins for visual symmetry.

Sequence diagrams and database diagrams are allowed to be dense, but they must be readable. If the original diagram is too large, crop the meaningful region and explain the flow in a side or bottom panel.

## Brand Rules

The Smart Class logo asset is mandatory when a logo is needed. Do not create an Apple-like logo, do not use Apple marks, and do not replace the Smart Class logo with generic Wi-Fi icons. Icons may support content, but they are not a substitute for the brand logo.

If the logo does not fit a dark background, place it on a clean white or light-blue logo field, or use it only on light slides. Do not recolor the logo unless a verified alternate logo asset exists.

## Completion Standard

A finished deck should pass three checks:

- Thumbnail check: slide types are visually distinct, but titles and brand anchors are consistent.
- Readability check: titles, tables, diagrams, and screenshots are readable in presentation mode.
- Density check: content slides do not leave the lower third empty unless the slide is intentionally a chapter divider or closing page.
- Relevance check: every bottom strip, callout, label, and note is useful to the evaluator or audience, not just to the deck-generation process.
- Boundary check: no text overlaps or touches shape borders.
- Portrait check: all person photos preserve the original image crop and aspect ratio.
- Wrapping check: no word or technical term breaks in the middle.
- Text-box check: short labels and names have enough width to stay on one line.
- Alignment check: same-level repeated content is aligned across cards, rows, and panels.
- Number-box check: no numeric label is clipped or flush against an index box edge.
- Editability check: charts and diagrams are editable PPT shapes, not raster screenshots, unless explicitly requested otherwise.
- Table check: every table is a real PowerPoint/native table object, not a group of manually arranged shapes that only looks like a table.
