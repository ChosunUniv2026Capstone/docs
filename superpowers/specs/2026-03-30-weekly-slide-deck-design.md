---
title: Weekly slide deck increment workflow
date: 2026-03-30
status: proposed
owner: Codex
---

# Weekly slide deck increment workflow

## Context

The project needs a repeatable way to keep weekly presentation decks up to date inside the `docs` repository, using the existing `w2.pptx` and `w3.pptx` decks as the starting point. The workflow should preserve PowerPoint files in Git, increment the deck week by week, add new content when the project advances, and remove obsolete material when it no longer belongs in the weekly story.

The preferred operating model is:

- keep all slide assets and outputs in `docs`
- use `CodexKit` as the entry point for setup and execution
- update the next deck by incrementally editing the latest published deck
- generate a draft manifest automatically before the user reviews or reruns the update
- start with manual execution only, without scheduled automation

## Goals

- Track `.pptx` source and output files in Git.
- Standardize weekly deck storage, input documents, and output artifacts.
- Make the weekly command simple enough to run with one manual entry point.
- Use the latest published deck as the editing base for the next week.
- Auto-generate a draft manifest for the next week from project documents and prior deck context.
- Keep the process compatible with Codex slide-editing workflows and future skill/plugin packaging.

## Non-goals

- Fully autonomous scheduled deck generation.
- Rebuilding each weekly deck from scratch.
- Treating Git tags as the primary source of weekly change intent.
- Building a large custom presentation engine on day one.

## Considered approaches

### Approach A: upstream Slides skill only

Use an external Slides skill directly and keep only deck files in `docs`.

Pros:

- lowest initial setup cost
- quickest path to manual experimentation

Cons:

- weak reproducibility across machines
- no project-specific weekly workflow contract
- no stable place for manifest drafting rules

### Approach B: `CodexKit`-managed local slide workflow

Add a project-specific slide workflow to `CodexKit`, keep decks and manifests in `docs`, and expose one manual command for weekly updates.

Pros:

- reproducible team workflow
- keeps `docs` as source of truth
- simple user surface with project-specific defaults
- compatible with upstream Slides skill or a future local implementation

Cons:

- requires some initial structure and glue code
- still depends on environment setup for the slide-editing layer

### Approach C: fully custom repo-native deck generator

Implement direct deck editing and validation logic entirely inside the repository.

Pros:

- maximum control
- minimal external workflow dependency after setup

Cons:

- highest implementation and maintenance cost
- unnecessary complexity for the first version

## Recommendation

Choose Approach B.

It fits the current workspace layout, respects the `docs` repository as source of truth, and gives the team a stable, documented interface without overbuilding a new presentation system. This also keeps the door open to use an upstream Slides skill where available, while preserving the option to swap in more local logic later if needed.

## Proposed storage layout

Create a new deck area inside `docs`:

```text
docs/
  08-slide-decks/
    weekly-progress/
      guidelines.md
      assets/
      source/
        w2.pptx
        w3.pptx
      working/
      published/
        w2.pptx
        w3.pptx
      manifests/
        w4.md
      notes/
        w4.md
```

Directory purposes:

- `source/`: imported historical decks kept for provenance
- `working/`: temporary or in-progress copies generated during an update run
- `published/`: canonical weekly deck outputs tracked in Git
- `manifests/`: one manifest per target week, including draft and reviewed intent
- `notes/`: plain-language summary of what changed in each weekly update
- `assets/`: logos, figures, screenshots, and reusable visual references
- `guidelines.md`: stable editing rules for the weekly deck line

## Weekly numbering model

Weekly decks use simple sequential labels such as `w2`, `w3`, `w4`.

The workflow determines the next target week by inspecting the latest published deck. If the latest published file is `w3.pptx`, the next target becomes `w4`.

This numbering is intentionally independent from calendar week numbers. The deck line is a project artifact sequence, not a date-based reporting contract.

## Execution flow

Primary manual entry point:

```bash
bash CodexKit/install/update_weekly_slides.sh --deck weekly-progress
```

Expected behavior:

1. Locate the deck root under `docs/08-slide-decks/<deck>/`.
2. Identify the latest published deck.
3. Compute the next week label from the latest deck name.
4. Generate a draft manifest for the next week if none exists yet.
5. Exit with guidance if the manifest was just created and still needs review.
6. On rerun, copy the latest published deck into `working/`.
7. Perform incremental slide edits for the next week.
8. Save the result into `published/<next-week>.pptx`.
9. Write a change summary to `notes/<next-week>.md`.

## Manifest model

The manifest is the editable bridge between project documentation and slide updates.

Example shape:

```md
# w4 manifest

status: draft
base_deck: published/w3.pptx
target_deck: published/w4.pptx

## Source documents
- 07-status/implementation-roadmap.md
- 07-status/risks-and-issues.md
- 05-work-items/epic-full-lms-delivery-plan.md
- 06-meetings/digested/2026-03-30-kickoff-summary.md

## Keep
- project overview
- system scope slide

## Add candidates
- newly confirmed prototype scope
- latest implementation progress
- new risk or blocker summary

## Remove candidates
- outdated roadmap milestones
- resolved blockers no longer worth showing

## Editing notes
- preserve branding from base deck
- prefer text as text and simple visuals as native slide objects
- add only changes that are supported by source documents
```

## Draft manifest generation

Draft manifest generation should be automatic.

When the next manifest does not exist, the command should create it by combining:

- the previous manifest, if present
- the latest published deck identity
- recent changes in `docs`
- current status documents
- recent digested meeting summaries
- relevant work item and requirement documents

The draft generator should produce:

- inferred `base_deck` and `target_deck`
- a suggested source-document list
- suggested add/keep/remove candidate bullets
- editing notes carried forward from prior guidance

This makes the first pass low-friction while still preserving a human review checkpoint.

## Update rules

The weekly update process should follow these editing rules:

- always start from the latest published deck
- preserve the existing branding, layout language, and aspect ratio unless the manifest explicitly changes them
- add only material supported by documents in `docs`
- remove slides or sections that are obsolete for the current weekly narrative
- prefer incremental edits to slide replacement when a slide still has structural value
- keep text editable as text where practical
- keep simple charts and layout primitives PowerPoint-native where practical

## `CodexKit` responsibilities

`CodexKit` should own the reusable workflow surface:

- the manual command entry point
- manifest template or generator logic
- environment checks for the slide-editing layer
- documentation for installing and using the deck workflow
- a project-local skill or wrapper that standardizes how Codex performs deck edits

The initial implementation can wrap an upstream Slides-oriented workflow rather than reimplementing presentation editing logic immediately.

## `docs` responsibilities

The `docs` repository should own the project-specific source of truth:

- imported historical PPTX files
- published weekly PPTX outputs
- per-week manifests
- per-week change notes
- deck-specific editing guidelines
- reusable slide assets

## Git strategy

Track `.pptx` files directly in Git alongside manifests and notes.

Recommended use of Git metadata:

- commits remain the main change history
- manifests and notes explain why the deck changed
- optional tags such as `slides-w4` can mark milestone outputs

Git tags are intentionally secondary. They help label published snapshots but should not replace manifests as the change-intent record.

## Validation strategy

Initial validation should cover:

- manifest generation succeeds for a new week
- next-week detection works from the latest published deck
- weekly output is written to the expected location
- notes are generated alongside the deck
- deck edits preserve the expected source branding and structure

If the slide-editing layer supports it, later validation should also include:

- render-to-image review
- overflow detection
- overlap detection
- missing or substituted font checks

## Risks

- the upstream Slides workflow may not already be installed in every local Codex environment
- binary `.pptx` diffs are limited, so notes and manifests must remain disciplined
- draft manifest inference can over-suggest changes if recent documents are noisy
- purely automatic content pruning is risky without explicit human review

## Rollout plan

### Phase 1

- add deck storage structure under `docs`
- import `w2.pptx` and `w3.pptx`
- add `guidelines.md`
- add manual update command scaffold in `CodexKit`
- add draft manifest generation

### Phase 2

- connect the command to the actual slide-editing workflow
- generate notes automatically
- add basic validation checks

### Phase 3

- improve source-document selection heuristics
- add optional milestone tagging
- add stronger review outputs such as slide render previews

## Open implementation decisions

- whether `w2.pptx` and `w3.pptx` should live in both `source/` and `published/`, or only in `published/` after import
- whether the actual editing step should call an upstream Slides skill directly, a local wrapper skill, or a hybrid shell-plus-skill path
- what exact heuristics should define “recent changes” in `docs` when drafting the next manifest

## Decision summary

Proceed with a `CodexKit`-managed local weekly deck workflow that:

- keeps PPTX files in `docs`
- increments the deck with `wN -> wN+1`
- auto-generates the next manifest draft
- uses manual execution only for now
- treats manifests as the primary explanation of deck changes
