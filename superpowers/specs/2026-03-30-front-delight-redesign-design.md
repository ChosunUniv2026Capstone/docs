---
title: Front delight redesign workflow
date: 2026-03-30
status: proposed
owner: Codex
---

# Front delight redesign workflow

## Context

The current `Front` app is functionally useful, but it is still shaped like an MVP scaffold:

- almost all UI logic lives in `Front/src/App.tsx`
- visual hierarchy depends on generic panels and cards
- role-specific workflows are mixed into one component tree
- the project has no durable front-end design contract for future Codex runs

The redesign target is not "make it prettier" in isolation. The target is to keep the current working behaviors while changing the way the team designs and implements front-end work so the product becomes visually intentional and stays that way.

The external reference for this redesign is OpenAI's article [Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4). The parts that matter most here are:

- start with explicit design principles and constraints
- define design tokens and typography roles early
- use a narrative structure only where a narrative surface exists
- keep app UI restrained, utility-first, and low-chrome
- avoid dashboard-card mosaics and decorative clutter
- verify desktop and mobile behavior deliberately

## Goals

- Preserve the current working feature set:
  - student / professor / admin login
  - role-aware dashboards
  - profile and device management
  - notices
  - course detail page
  - student eligibility check
  - admin classroom / AP visibility
- Replace the current monolithic UI with smaller role-oriented surfaces.
- Establish a reusable visual language that future Codex runs can follow without reinventing taste.
- Add a repeatable front-end redesign workflow that combines docs guidance, a reusable prompt, and visual verification.
- Keep the initial redesign inside the current stack: React 19, Vite, TypeScript, plain CSS.

## Non-goals

- Expanding LMS scope beyond the currently implemented MVP flows.
- Changing backend contracts during the first redesign pass.
- Introducing a UI framework, component library, or new runtime dependency.
- Replacing domain terminology with marketing-heavy copy.

## Current codebase constraints

- `Front/src/App.tsx` currently owns app state, role branching, and most rendering.
- `Front/src/index.css` is a single global style file.
- `Front/src/api.ts` is already a useful domain boundary and should remain the API contract surface.
- Project rules require the front-end to consume backend decisions rather than re-implement business logic.
- There is no test runner dependency in the repo today, so behavior protection should begin with pure TypeScript seams plus Node's built-in test runner before visual restructuring.

## Design direction

### 1. App surfaces use restraint, not marketing chrome

The OpenAI article distinguishes visually led landing pages from operational product UI. This project is mostly product UI, so the redesign should default to:

- calm surfaces
- strong type hierarchy
- one accent color
- minimal borders and shadows
- cards only when the card itself is the interaction
- utility copy over aspirational copy

This means the post-login experience should look more like an academic operations workspace than a generic dashboard.

### 2. Narrative is reserved for the login / entry surface

The article's narrative structure still applies, but only to the authentication surface, where the product needs orientation and identity. The login page can carry atmosphere, role framing, and one clear call to action. The authenticated app should not reuse that marketing structure; it should pivot immediately into task-oriented utility.

### 3. Fewer panels, clearer regions

The target shell is:

- primary workspace
- navigation
- secondary context / inspector

That maps well to the current product:

- student: course list / notices / attendance status as primary work
- professor: course operations and notice composition as primary work
- admin: operational inventory with detailed side context

### 4. Explicit design tokens

The redesign should introduce a token layer for:

- background
- surface
- surface-strong
- text
- text-muted
- accent
- success / warning / danger
- display / heading / body / meta typography roles
- spacing and radius scales

These tokens should be documented in `docs` and mirrored in CSS so that future visual work is constrained by a design system, not ad hoc color picking.

### 5. Human-readable status communication

The UI should keep raw reason codes available, but it should stop presenting them as the only primary output. For eligibility states, the UI should present:

- plain-language status headline
- concise explanation
- raw backend reason code
- optional technical evidence drawer

This preserves debugging value while making the product legible to actual users.

## Process options for future front-end work

### Option A: prompt only

Create one repo-local prompt file and require agents to start front-end work from it.

Pros:

- fastest to introduce
- low maintenance
- easy to use with standard `executor` agents

Cons:

- easier to ignore over time
- weak source-of-truth separation
- does not by itself force documentation updates

### Option B: docs convention + repo prompt + verifier workflow

Add:

- a design convention in `docs`
- a reusable prompt in `Front/.codex/prompts/`
- a required visual verification loop for front-end changes

Pros:

- durable and still lightweight
- design language becomes auditable in `docs`
- prompt gives execution-ready instructions
- verifier step keeps taste from drifting

Cons:

- requires a little more setup than prompt-only

### Option C: custom skill first

Create a dedicated repo-local front-end design skill before redesign implementation.

Pros:

- strongest workflow enforcement
- can encode required steps, checks, and artifact expectations

Cons:

- more overhead now
- higher maintenance burden while the visual language is still evolving

## Recommendation

Choose Option B for the first pass.

It is the best balance between durability and speed:

- `docs` becomes the canonical design source
- the repo prompt becomes the execution surface for future front-end work
- the redesign itself is still delivered with normal Codex agents
- a later skill can be added once the workflow has stabilized in real use

## Proposed artifact set

### In `docs`

- `docs/03-conventions/conv-frontend-experience-design.md`
  - visual principles
  - token names and intended semantics
  - app-vs-auth surface rules
  - copy rules
  - desktop/mobile verification checklist

### In `Front`

- `Front/.codex/prompts/frontend-delight-redesign.md`
  - implementation kickoff prompt
  - references the convention doc
  - tells the agent to avoid card mosaics and generic dashboard styling
  - requires visual QA before completion

### In `Front`

- split `App.tsx` into app shell + feature surfaces
- introduce presentational seams that can be tested without browser-only tooling
- replace the single large stylesheet with tokens + layout + feature styles

## Proposed information architecture

### Login

- full-height welcome surface
- one product statement
- one supporting sentence
- one credential form
- one small role guide / seed account hint

### Authenticated app shell

- left or top navigation with clear role-aware destinations
- primary content region for the current workflow
- contextual right rail or lower inspector when details help decision-making
- compact account and system status strip

### Student

- default landing: active courses and recent notices
- profile: identity, device registration, registered devices
- course page: notices first, attendance / exam eligibility second

### Professor

- default landing: owned courses and recent notices
- course page: notice authoring + notice history

### Admin

- default landing: users, classrooms, AP/network inventory
- inspector treatment for classroom-network details instead of large JSON-heavy cards everywhere

## Visual language proposal

- overall mood: academic operations workspace
- personality: calm, precise, credible
- color direction: warm neutral surfaces with one cool academic accent
- chrome: low
- emphasis: typography, spacing, and sectional rhythm instead of stacked cards
- motion: small number of meaningful transitions only, such as shell reveal, active-panel shift, and disclosure expansion

## Verification strategy

### Automated

- `npm run lint`
- `npm run build`
- pure TypeScript unit tests for role/view/presenter helpers using Node's built-in test runner

### Manual / visual

- login on desktop
- login on mobile width
- student flow: dashboard, profile, device add/remove, course page, eligibility result
- professor flow: dashboard, course page, notice creation
- admin flow: dashboard, classroom detail visibility
- screenshot review to check clutter, spacing rhythm, and hierarchy

## Sequencing recommendation

1. Protect behavior with pure helper tests.
2. Add the docs convention and repo prompt.
3. Introduce the shell and token system.
4. Move role surfaces into focused feature components.
5. Redesign visuals with the new constraints.
6. Run visual QA and trim anything that still looks like scaffold UI.

## Decision

Proceed with a front-end redesign that treats the design system and execution workflow as first-class deliverables, not just byproducts of the UI rewrite.
