# Weekly Slide Deck Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a first-pass `w4` deck under `docs` by importing the provided `w2/w3` PPTX files, summarizing the current project changes, and generating a publishable weekly-update PowerPoint draft.

**Architecture:** Keep the canonical artifacts in `docs/08-slide-decks/weekly-progress/`, treat `w3` as the latest published deck reference, and build a new `w4` weekly update deck with a task-local PptxGenJS workspace. Use repo documents and recent repository history as the source of weekly change content.

**Tech Stack:** Git, PowerPoint `.pptx`, PptxGenJS, LibreOffice `soffice`, Python XML inspection, workspace-local Codex `slides` skill

---

### Task 1: Prepare deck storage

**Files:**
- Create: `docs/08-slide-decks/weekly-progress/`
- Create: `docs/08-slide-decks/weekly-progress/source/`
- Create: `docs/08-slide-decks/weekly-progress/published/`
- Create: `docs/08-slide-decks/weekly-progress/manifests/`
- Create: `docs/08-slide-decks/weekly-progress/notes/`
- Create: `docs/08-slide-decks/weekly-progress/guidelines.md`

- [ ] **Step 1: Create the directory structure**
- [ ] **Step 2: Copy the provided `w2` and `w3` decks into `source/`**
- [ ] **Step 3: Seed `published/` with the current latest baseline deck**
- [ ] **Step 4: Add a minimal `guidelines.md` for weekly update rules**

### Task 2: Collect weekly change input

**Files:**
- Create: `docs/08-slide-decks/weekly-progress/manifests/w4.md`
- Modify: `docs/08-slide-decks/weekly-progress/notes/w4.md`

- [ ] **Step 1: Inspect recent `docs`, `CodexKit`, `Front`, `Backend`, `PresenceService`, and `DB` history**
- [ ] **Step 2: Extract the major current-state updates worth presenting**
- [ ] **Step 3: Write a first-pass `w4` manifest**
- [ ] **Step 4: Write a short `w4` note describing the intended slide updates**

### Task 3: Author the `w4` deck

**Files:**
- Create: `docs/08-slide-decks/weekly-progress/workspace/w4/`
- Create: `docs/08-slide-decks/weekly-progress/workspace/w4/w4.js`
- Create: `docs/08-slide-decks/weekly-progress/published/w4.pptx`

- [ ] **Step 1: Create a task-local JS workspace with the `slides` skill helpers**
- [ ] **Step 2: Render a concise weekly-update deck that reflects the current project changes**
- [ ] **Step 3: Generate `w4.pptx`**
- [ ] **Step 4: Render slide previews for manual verification**

### Task 4: Verify and report

**Files:**
- Modify: `docs/08-slide-decks/weekly-progress/notes/w4.md`

- [ ] **Step 1: Confirm the output deck exists and is readable**
- [ ] **Step 2: Check the rendered slides for obvious layout breakage**
- [ ] **Step 3: Update `notes/w4.md` with what was actually produced**
- [ ] **Step 4: Report artifact paths and remaining gaps**
