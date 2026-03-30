# Weekly Progress Deck Guidelines

- Keep the deck in 16:9 widescreen format.
- Preserve the blue-and-white tone from `w3.pptx`.
- Use `Pretendard Variable` as the primary font when available.
- Prefer concise status wording over dense paragraphs.
- Treat `docs` as the source of truth for roadmap, risks, and scope.
- Highlight concrete repository-level changes before future plans.
- Remove outdated roadmap claims when the current repository state no longer matches them.
- Keep one slide focused on risks and open questions.
- Keep one slide focused on next actions.
- Collect update content from `git diff` across `docs`, `CodexKit`, `Front`, `Backend`, `PresenceService`, and `DB`.
- If weekly tags exist, use `previous tag -> HEAD` as the update range.
- If no weekly tags exist yet, use `empty repo -> HEAD` as the initial baseline.
- Place new information inside the closest existing section before adding a brand-new slide.
- Add a new slide under an existing section only when the change does not fit cleanly on the original slides.
- Do not add a new table-of-contents item unless a genuinely new presentation section is needed.
- Derive slide content from both commit messages and the corresponding diffed files.
- Summarize implemented features by feature page, not only by repository name.
