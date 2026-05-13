---
title: Exam Workflow Requirements
type: requirement
status: active
updated: 2026-05-14
owners:
  - frontend-team
  - backend-team
  - db-owner
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/04-architecture/exam-workflow-api.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - 2026-04-09 local alignment with dd exam workflow
  - 2026-05-14 issue-resolution contract checkpoint for requires_presence=false
---

# Goal

Provide a local end-to-end exam flow for student and professor users inside the course detail page.
The local implementation must stay aligned with the shared course-scoped exam schema and current MVP contract.

# Scope

- A course detail page exposes an `exam` section.
- A professor can create, edit, publish, close, and delete exams for owned courses.
- A student can list available exams, open exam detail, start an attempt, save answers, and submit answers.
- The current local professor UI supports objective questions for the first release.
- The first local student UI uses a dedicated exam-taking page after start.

# Professor Requirements

- Professors can create `draft` exams with:
  - title
  - description
  - exam type
  - start and end time
  - duration in minutes
  - late-entry policy
  - auto-submit policy
  - shuffle flags
  - max attempts
- Exams default to `requires_presence=true` for compatibility, and professor create/update flows must preserve an explicit `requires_presence=false` value when that policy is selected.
- Professors can edit only `draft` exams.
- Professors can delete owned exams from the course exam page.
- Professors can publish a `draft` exam.
- Professors can close a published or open exam.
- Professors can see exam counts and attempt counts per course.
- Professors can review a selected exam's schedule and policy settings inside the course exam page.
- Professors can review per-student latest submission status for enrolled students, including:
  - not started
  - in progress
  - submitted
  - auto submitted
  - graded
- Professor exam detail can show the latest attempt summary per student with:
  - student id
  - student name
  - latest attempt number
  - started time
  - submitted time
  - score
  - answered question count summary
- Professor exam detail can show overview counts for:
  - enrolled students
  - started students
  - submitted students
  - not started students
  - average score for scored latest attempts

# Student Requirements

- Students can see only exams for enrolled courses.
- Students can see `published`, `open`, or `closed` exams in the course exam list.
- Before starting, students should only see exam summary information and start guidance, not the actual question body.
- Students can start an attempt only inside the valid exam window.
- If `late entry` is disabled, a student without an existing attempt cannot start after the official exam start time.
- If `late entry` is enabled, a student can still create the first attempt after the official start time while the exam window remains open.
- If `late entry` is enabled and a student starts late, the actual attempt deadline is still capped by the official exam end time.
- Questions should be revealed only after the student presses the start button and the attempt is created.
- If `shuffle questions` is enabled, the student sees a per-attempt deterministic shuffled question order.
- Objective question choice order remains fixed.
- If `requires_presence=true`, the student start action must confirm that the student has at least one active registered device before the first attempt is created.
- If `requires_presence=false`, the student start action must not block solely because the student has no active registered device.
- The current local exam policy does not require the current class window or classroom network observation for exam start.
- After the start button is pressed, the student UI switches to a dedicated exam-taking page.
- The dedicated exam-taking page hides the normal LMS navigation and keeps the student inside the exam flow.
- The local student exam-taking page shows one question at a time, previous/next controls, a remaining-time indicator, and direct question-number navigation.
- Students can continue an in-progress attempt until the stored submission expiry.
- Students cannot submit while required questions remain unanswered.
- Before submit, the UI alerts the student with unanswered question numbers and moves to the first missing answer.
- If `auto-submit` is enabled, the student exam-taking page automatically finalizes the in-progress attempt when the stored submission expiry is reached.
- Student exam views can show attempt status and submission completion only.

# Shared Rules

- The DB schema follows the shared tables:
  - `exams`
  - `exam_questions`
  - `exam_question_options`
  - `exam_submissions`
  - `exam_submission_answers`
- The first local UI sends and renders objective questions.
- A student can have multiple attempts only up to `max_attempts`.
- Submission expiry is derived from `duration_minutes` and stored in each submission row, capped at the earlier of the configured duration or the official exam end time.
- API routes remain course-scoped for both student and professor flows.
- Exam start reuses the registered-device ownership data from the attendance domain, but does not require the current class-window presence check.
- Deleting an exam removes linked questions, attempts, and answers together in the local DB.

# Out of Scope

- Essay grading workflow
- File upload answers
- Rich anti-cheating features
- Separate grading dashboard

# Acceptance

- The student course detail page restores the exam route.
- The professor course detail page can save, edit, publish, and delete a draft.
- The professor course detail page can review latest submission status for enrolled students.
- The student can start and submit at least one published exam.
- The backend persists attempts and answers in the shared schema table names.
