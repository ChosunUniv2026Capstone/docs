# CodexKit Main Guardrails And Bootstrap Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent direct local commits/pushes to `main` by default and make `CodexKit` bootstrap reliably clone sibling repos on fresh machines with clear failure modes.

**Architecture:** Add shared Git hooks under `CodexKit/.githooks`, wire every cloned repo to those hooks during bootstrap, and harden bootstrap preflight checks around `gh`/SSH authentication and clone verification. Keep the live docs convention, bootstrap docs, and workspace seed synchronized so fresh workspaces inherit the same branch-protection rules.

**Tech Stack:** Bash, Git hooks, Git config (`core.hooksPath`), Python validator scripts, Markdown docs

---

## File Structure

### New files

- Create: `CodexKit/.githooks/pre-commit`
- Create: `CodexKit/.githooks/pre-push`
- Create: `CodexKit/install/configure_git_hooks.sh`

### Modified files

- Modify: `CodexKit/install/bootstrap_workspace.sh`
- Modify: `CodexKit/install/doctor.sh`
- Modify: `CodexKit/install/install_user_skills.sh` only if path assumptions need alignment with hook setup
- Modify: `CodexKit/README.md`
- Modify: `CodexKit/skills/git-governance/SKILL.md`
- Modify: `CodexKit/skills/git-governance/references/git-conventions.md`
- Modify: `CodexKit/docs/git-conventions.md`
- Modify: `CodexKit/docs/quickstart-usage.md`
- Modify: `CodexKit/repo-templates/Backend/AGENTS.md`
- Modify: `CodexKit/repo-templates/Front/AGENTS.md`
- Modify: `CodexKit/repo-templates/PresenceService/AGENTS.md`
- Modify: `CodexKit/repo-templates/DB/AGENTS.md`
- Modify: `CodexKit/repo-templates/docs/AGENTS.md` if it mentions direct `main` commits as an allowed path
- Modify: `docs/03-conventions/conv-git-branch-and-pr.md`
- Modify: `CodexKit/workspace-seed/docs/03-conventions/conv-git-branch-and-pr.md`

### Test and verification surfaces

- Test: fresh temp workspace bootstrap via `bash install/bootstrap_workspace.sh --workspace <tmp>`
- Test: local hook enforcement in `docs`, `Front`, `Backend`, `PresenceService`, `DB`
- Test: `doctor.sh` reports hook installation status

### Responsibility map

- `CodexKit/.githooks/*`: actual local enforcement layer
- `CodexKit/install/configure_git_hooks.sh`: idempotent installer that points repos at shared hooks
- `CodexKit/install/bootstrap_workspace.sh`: orchestration entrypoint for cloning, seeding, templates, hooks, doctor
- `CodexKit/install/doctor.sh`: verification/reporting for bootstrap and guardrails
- `docs/03-conventions/conv-git-branch-and-pr.md`: live truth source for branch policy
- `CodexKit/*docs*` and `workspace-seed/docs/*`: bootstrap copy of the same truth

---

### Task 1: Add Shared Main-Branch Guard Hooks

**Files:**
- Create: `CodexKit/.githooks/pre-commit`
- Create: `CodexKit/.githooks/pre-push`
- Test: temporary repo configured with `core.hooksPath`

- [ ] **Step 1: Write the failing hook behavior spec as shell assertions**

Create a scratch verification script in the terminal first:

```bash
tmp_repo="$(mktemp -d)"
git init "$tmp_repo"
git -C "$tmp_repo" checkout -b main
git -C "$tmp_repo" config core.hooksPath "/absolute/path/to/CodexKit/.githooks"
touch "$tmp_repo/README.md"
git -C "$tmp_repo" add README.md
git -C "$tmp_repo" commit -m "docs(test): main commit probe"
```

Expected result after hook implementation:

```text
Direct commits to main are blocked
```

- [ ] **Step 2: Create `pre-commit` with an explicit main-branch block**

Write exactly:

```bash
#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$branch" = "main" ]; then
  echo "Direct commits to main are blocked. Create a feature branch first." >&2
  echo "Suggested: git checkout -b feat/<slug>" >&2
  exit 1
fi
```

- [ ] **Step 3: Create `pre-push` with an explicit main push block**

Write exactly:

```bash
#!/usr/bin/env bash
set -euo pipefail

current_branch="$(git rev-parse --abbrev-ref HEAD)"

if [ "$current_branch" = "main" ]; then
  echo "Direct pushes from main are blocked. Open a PR from a feature branch." >&2
  exit 1
fi

while read -r _local_ref _local_sha remote_ref _remote_sha; do
  if [ "$remote_ref" = "refs/heads/main" ]; then
    echo "Push to refs/heads/main is blocked. Push a feature branch instead." >&2
    exit 1
  fi
done
```

- [ ] **Step 4: Make the hook files executable**

Run:

```bash
chmod +x CodexKit/.githooks/pre-commit CodexKit/.githooks/pre-push
```

Expected: no output

- [ ] **Step 5: Re-run the temp repo probe to verify `pre-commit` now fails**

Run:

```bash
tmp_repo="$(mktemp -d)"
git init "$tmp_repo"
git -C "$tmp_repo" checkout -b main
git -C "$tmp_repo" config core.hooksPath "/Users/kimhyeonseok/CodeStorage/smart-class/CodexKit/.githooks"
touch "$tmp_repo/README.md"
git -C "$tmp_repo" add README.md
git -C "$tmp_repo" commit -m "docs(test): main commit probe"
```

Expected:

```text
Direct commits to main are blocked. Create a feature branch first.
```

- [ ] **Step 6: Commit**

```bash
git add CodexKit/.githooks/pre-commit CodexKit/.githooks/pre-push
git commit -m "chore(codexkit): add local main branch git hooks"
```

---

### Task 2: Install Hooks Automatically During Bootstrap

**Files:**
- Create: `CodexKit/install/configure_git_hooks.sh`
- Modify: `CodexKit/install/bootstrap_workspace.sh`
- Modify: `CodexKit/install/doctor.sh`

- [ ] **Step 1: Write the failing bootstrap expectation**

Run this before implementation in a temp workspace:

```bash
tmp_ws="$(mktemp -d)"
mkdir -p "$tmp_ws/CodexKit"
rsync -a --exclude '.git' /Users/kimhyeonseok/CodeStorage/smart-class/CodexKit/ "$tmp_ws/CodexKit/"
bash "$tmp_ws/CodexKit/install/bootstrap_workspace.sh" --workspace "$tmp_ws" --skip-doctor || true
git -C "$tmp_ws/Backend" config --get core.hooksPath
```

Expected before implementation:

```text
(empty)
```

- [ ] **Step 2: Create `configure_git_hooks.sh` as an idempotent installer**

Write exactly:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 /path/to/workspace"
  exit 1
fi

WORKSPACE="$(cd "$1" && pwd)"
HOOKS_DIR="${WORKSPACE}/CodexKit/.githooks"
REPOS=(docs Front Backend PresenceService DB)

if [ ! -d "${HOOKS_DIR}" ]; then
  echo "Hooks directory not found: ${HOOKS_DIR}" >&2
  exit 1
fi

for repo in "${REPOS[@]}"; do
  repo_path="${WORKSPACE}/${repo}"
  if [ -d "${repo_path}/.git" ]; then
    git -C "${repo_path}" config core.hooksPath "${HOOKS_DIR}"
    echo "Configured hooks for ${repo}"
  fi
done
```

- [ ] **Step 3: Call `configure_git_hooks.sh` from bootstrap after cloning and before doctor**

Insert this block in `CodexKit/install/bootstrap_workspace.sh` after template bootstrap:

```bash
echo "Configuring shared git hooks"
bash "${SCRIPT_DIR}/configure_git_hooks.sh" "${WORKSPACE}"
```

- [ ] **Step 4: Extend doctor to verify hook path**

Add this verification loop to `CodexKit/install/doctor.sh`:

```bash
for repo in docs Front Backend PresenceService DB; do
  hooks_path="$(git -C "${WORKSPACE}/${repo}" config --get core.hooksPath || true)"
  expected="${WORKSPACE}/CodexKit/.githooks"
  if [ "${hooks_path}" = "${expected}" ]; then
    pass "hooks configured in ${repo}"
  else
    fail "hooks missing in ${repo}"
  fi
done
```

- [ ] **Step 5: Re-run bootstrap in a temp workspace and verify hook config**

Run:

```bash
tmp_ws="$(mktemp -d)"
mkdir -p "$tmp_ws/CodexKit"
rsync -a --exclude '.git' /Users/kimhyeonseok/CodeStorage/smart-class/CodexKit/ "$tmp_ws/CodexKit/"
bash "$tmp_ws/CodexKit/install/bootstrap_workspace.sh" --workspace "$tmp_ws"
git -C "$tmp_ws/Backend" config --get core.hooksPath
```

Expected:

```text
/tmp/.../CodexKit/.githooks
```

- [ ] **Step 6: Verify a bootstrap-created repo blocks `main` commits**

Run:

```bash
tmp_ws="$(mktemp -d)"
mkdir -p "$tmp_ws/CodexKit"
rsync -a --exclude '.git' /Users/kimhyeonseok/CodeStorage/smart-class/CodexKit/ "$tmp_ws/CodexKit/"
bash "$tmp_ws/CodexKit/install/bootstrap_workspace.sh" --workspace "$tmp_ws"
touch "$tmp_ws/Backend/probe.txt"
git -C "$tmp_ws/Backend" add probe.txt
git -C "$tmp_ws/Backend" commit -m "test(backend): main hook probe"
```

Expected:

```text
Direct commits to main are blocked
```

- [ ] **Step 7: Commit**

```bash
git add CodexKit/install/configure_git_hooks.sh CodexKit/install/bootstrap_workspace.sh CodexKit/install/doctor.sh
git commit -m "feat(codexkit): install shared git hooks during bootstrap"
```

---

### Task 3: Harden Bootstrap Repo Fetch Preconditions

**Files:**
- Modify: `CodexKit/install/bootstrap_workspace.sh`
- Modify: `CodexKit/install/doctor.sh`
- Modify: `CodexKit/README.md`

- [ ] **Step 1: Add an explicit clone preflight function**

Insert into `bootstrap_workspace.sh`:

```bash
require_clone_access() {
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    return 0
  fi

  if ssh -T git@github.com >/dev/null 2>&1 || [ $? -eq 1 ]; then
    return 0
  fi

  echo "No GitHub clone path is ready." >&2
  echo "Configure either 'gh auth login' or GitHub SSH access first." >&2
  exit 1
}
```

- [ ] **Step 2: Call the preflight before cloning repos**

Add:

```bash
require_clone_access
```

right before the clone loop.

- [ ] **Step 3: Verify each clone result explicitly**

Append to `clone_repo()`:

```bash
if [ ! -d "${path}/.git" ]; then
  echo "Clone failed for ${repo}" >&2
  exit 1
fi
```

- [ ] **Step 4: Teach doctor to distinguish `gh` vs SSH readiness**

Add:

```bash
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  pass "bootstrap clone path: gh auth"
elif ssh -T git@github.com >/dev/null 2>&1 || [ $? -eq 1 ]; then
  pass "bootstrap clone path: ssh"
else
  fail "bootstrap clone path unavailable"
fi
```

- [ ] **Step 5: Update README with an explicit auth prerequisite**

Add this exact snippet under “새 장치 시작”:

```bash
# Option A: GitHub CLI auth
gh auth login

# Option B: SSH auth
ssh -T git@github.com
```

- [ ] **Step 6: Verify failure mode is actionable**

Run:

```bash
env -i PATH="$PATH" HOME="$HOME" bash CodexKit/install/bootstrap_workspace.sh --workspace "$(mktemp -d)"
```

Expected: bootstrap exits early with an auth/setup error instead of hanging inside clone attempts.

- [ ] **Step 7: Commit**

```bash
git add CodexKit/install/bootstrap_workspace.sh CodexKit/install/doctor.sh CodexKit/README.md
git commit -m "feat(codexkit): harden bootstrap clone preflight"
```

---

### Task 4: Align Docs, Templates, And Skill Guidance With The Main Guardrail

**Files:**
- Modify: `docs/03-conventions/conv-git-branch-and-pr.md`
- Modify: `CodexKit/docs/git-conventions.md`
- Modify: `CodexKit/docs/quickstart-usage.md`
- Modify: `CodexKit/skills/git-governance/SKILL.md`
- Modify: `CodexKit/repo-templates/Backend/AGENTS.md`
- Modify: `CodexKit/repo-templates/Front/AGENTS.md`
- Modify: `CodexKit/repo-templates/PresenceService/AGENTS.md`
- Modify: `CodexKit/repo-templates/DB/AGENTS.md`
- Modify: `CodexKit/repo-templates/docs/AGENTS.md`
- Modify: `CodexKit/workspace-seed/docs/03-conventions/conv-git-branch-and-pr.md`

- [ ] **Step 1: Add explicit wording that local commits on `main` are blocked**

Add this bullet under the branch or merge rules in both live docs and CodexKit docs:

```md
- 로컬 작업은 반드시 feature branch 에서 시작한다. `main` 에서의 직접 commit/push 는 로컬 hook 으로 차단된다.
```

- [ ] **Step 2: Update repo template AGENTS to reflect the same rule**

Add this bullet to each repo template Git section:

```md
- `main` 에서 직접 commit 하지 않는다. bootstrap 이 설치한 shared hook 이 이를 차단한다.
```

- [ ] **Step 3: Update `git-governance` usage steps**

Add this line in `CodexKit/skills/git-governance/SKILL.md` under “작업 시작”:

```md
- `main` 에서 바로 commit 하려 하면 local hook 이 실패한다. branch 를 먼저 만든다.
```

- [ ] **Step 4: Sync the workspace seed docs**

Run:

```bash
rsync -a --delete --exclude '.git' --exclude '.obsidian' docs/ CodexKit/workspace-seed/docs/
```

Expected: no output

- [ ] **Step 5: Commit**

```bash
git add docs/03-conventions/conv-git-branch-and-pr.md CodexKit/docs/git-conventions.md CodexKit/docs/quickstart-usage.md CodexKit/skills/git-governance/SKILL.md CodexKit/repo-templates CodexKit/workspace-seed/docs/03-conventions/conv-git-branch-and-pr.md
git commit -m "docs(git): document local main-branch guardrails"
```

---

### Task 5: Add A Focused Guardrail Smoke Test Pass

**Files:**
- Modify: `CodexKit/install/doctor.sh`
- Modify: `CodexKit/README.md`

- [ ] **Step 1: Add an explicit hook smoke test command to README**

Insert:

```bash
git checkout -b feat/hook-smoke
git commit --allow-empty -m "test(repo): hook smoke"
```

and mention that the same command from `main` should fail.

- [ ] **Step 2: Add a non-destructive doctor note for hook validation**

Append to `doctor.sh` output:

```bash
echo "Next recommended manual check: create a feature branch and confirm commits work there, then confirm main rejects commits."
```

- [ ] **Step 3: Validate the branch checker explicitly**

Run:

```bash
python3 CodexKit/skills/git-governance/scripts/validate_branch_name.py feat/course-materials
python3 CodexKit/skills/git-governance/scripts/validate_branch_name.py feat/frontend/course-materials || true
```

Expected:

```text
OK
Invalid branch name
```

- [ ] **Step 4: Commit**

```bash
git add CodexKit/install/doctor.sh CodexKit/README.md
git commit -m "test(codexkit): add guardrail smoke guidance"
```

---

## Self-Review

### Spec coverage

- Main-branch local commit/push guard covered by Task 1 and Task 2.
- Bootstrap-time application of both skill guidance and local enforcement covered by Task 2 and Task 4.
- “Repo 받아오는게 실제로 가능하도록” hardening covered by Task 3.
- Fresh-machine/bootstrap verification covered by Task 2, Task 3, and Task 5.

### Placeholder scan

- No `TODO`, `TBD`, or “appropriate handling” placeholders remain.
- Every task includes exact file paths, code snippets, and concrete commands.

### Type/signature consistency

- Hook path is consistently `CodexKit/.githooks`.
- Branch format is consistently `<type>/<slug>`.
- Bootstrap installer path is consistently `CodexKit/install/configure_git_hooks.sh`.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-01-codexkit-main-guardrails-and-bootstrap.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
