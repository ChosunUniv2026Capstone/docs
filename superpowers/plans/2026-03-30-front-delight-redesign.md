# Front Delight Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current MVP-looking frontend with a more deliberate, calmer, role-aware workspace while preserving the current login, profile, course, notice, eligibility, and admin behaviors.

**Architecture:** Keep `Front/src/api.ts` as the backend contract surface, extract the current monolithic `App.tsx` into a small app model plus role-focused feature views, and introduce a documented design-token system that separates the expressive login surface from the utility-first authenticated workspace. Add a repo-local prompt and a docs convention so future Codex runs keep the same taste and verification loop.

**Tech Stack:** React 19, TypeScript, Vite, plain CSS, Node built-in `node:test`, existing Codex browser/screenshot verification tools

---

## Planned File Structure

- `docs/03-conventions/conv-frontend-experience-design.md`
  - canonical front-end visual rules and verification checklist
- `Front/.codex/prompts/frontend-delight-redesign.md`
  - reusable implementation prompt for future front-end redesign work
- `Front/src/app/model.ts`
  - role/view/course-tab state helpers
- `Front/src/app/AppShell.tsx`
  - authenticated workspace shell
- `Front/src/features/auth/LoginScreen.tsx`
  - login-only visual entry surface
- `Front/src/features/navigation/navigation.ts`
  - role-aware navigation definitions
- `Front/src/features/dashboard/DashboardView.tsx`
  - student/professor/admin dashboard composition
- `Front/src/features/profile/ProfileView.tsx`
  - account and device management surface
- `Front/src/features/course/CourseView.tsx`
  - course detail shell with notices / eligibility split
- `Front/src/features/eligibility/presenter.ts`
  - reason-code to UI copy mapping
- `Front/src/styles/tokens.css`
  - design tokens
- `Front/src/styles/base.css`
  - reset, typography, layout primitives
- `Front/src/styles/surfaces.css`
  - panel, nav, list, badge, form, and disclosure styling
- `Front/test/app-model.test.ts`
  - pure state model tests
- `Front/test/navigation.test.ts`
  - role-aware navigation tests
- `Front/test/eligibility-presenter.test.ts`
  - status copy tests
- `Front/tsconfig.test.json`
  - compile target for `node:test`

### Task 1: Freeze the redesign contract before touching UI

**Files:**
- Create: `docs/03-conventions/conv-frontend-experience-design.md`
- Create: `Front/.codex/prompts/frontend-delight-redesign.md`
- Modify: `Front/AGENTS.md`

- [ ] **Step 1: Write the design convention document**

```md
---
title: 프론트엔드 경험 디자인 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - frontend-team
applies_to:
  - frontend
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
source:
  - https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4
---

# 핵심 규칙

- 로그인 화면만 서사적 연출을 허용한다.
- 로그인 이후 앱 화면은 utility copy 와 작업 중심 구조를 기본값으로 한다.
- 카드 모자이크를 만들지 않는다.
- 카드가 없어도 의미가 유지되면 카드가 아니다.
- 색상은 하나의 주요 accent 와 명확한 중립 계층만 사용한다.
- 학생 / 교수 / 관리자 화면은 같은 컴포넌트에 억지로 겹치지 말고 역할별 surface 로 분리한다.
- eligibility 결과는 사람용 설명, reason code, evidence 순으로 보여준다.
- 데스크톱과 모바일 스크린샷 검증 없이 완료를 주장하지 않는다.
```

- [ ] **Step 2: Write the reusable redesign prompt**

```md
Read `../docs/03-conventions/conv-frontend-experience-design.md` first.

You are redesigning `Front` without changing current product behavior.

Rules:
- Keep existing API contracts and role boundaries.
- Treat login as the only expressive narrative surface.
- Treat the authenticated app as a calm operational workspace.
- Avoid dashboard-card mosaics, thick borders on every region, and decorative gradients behind routine product UI.
- Use explicit CSS tokens and meaningful spacing hierarchy.
- Prefer utility copy over marketing copy on product surfaces.
- Preserve desktop/mobile usability.
- Run lint, build, and screenshot-based verification before completion.
```

- [ ] **Step 3: Update `Front/AGENTS.md` so future work reads the new convention**

```md
## 구현 전 반드시 확인할 문서
- `../docs/03-conventions/conv-frontend-experience-design.md`
```

- [ ] **Step 4: Validate the docs are internally consistent**

Run: `pattern='T''ODO|TB''D|implement later|fill in details'; rg -n "$pattern" /Users/kimhyeonseok/CodeStorage/smart-class/docs/03-conventions/conv-frontend-experience-design.md /Users/kimhyeonseok/CodeStorage/smart-class/Front/.codex/prompts/frontend-delight-redesign.md /Users/kimhyeonseok/CodeStorage/smart-class/Front/AGENTS.md`

Expected: no matches

- [ ] **Step 5: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/docs add 03-conventions/conv-frontend-experience-design.md
git -C /Users/kimhyeonseok/CodeStorage/smart-class/docs commit -m "docs(docs): record the frontend experience rules

The redesign needs a stable visual contract in the source-of-truth docs
before implementation starts, otherwise later UI work will drift.

Constraint: Frontend behavior must stay aligned with existing requirements
Rejected: Keep design direction only in chat context | not durable enough
Confidence: high
Scope-risk: narrow
Directive: Update this convention before large visual shifts, not after them
Tested: Placeholder scan of the convention draft
Not-tested: Browser rendering"

git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add AGENTS.md .codex/prompts/frontend-delight-redesign.md
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): make the redesign prompt discoverable

Future frontend work needs a repo-local execution surface that points
agents at the new design rules before they touch code.

Constraint: Front repo and docs repo are committed separately
Rejected: Put the prompt in the workspace root | root is not a git repo here
Confidence: high
Scope-risk: narrow
Directive: Keep prompt guidance consistent with the docs convention
Tested: Placeholder scan of new prompt and AGENTS reference
Not-tested: Browser rendering"
```

### Task 2: Extract pure app-state seams and protect current behavior

**Files:**
- Create: `Front/src/app/model.ts`
- Create: `Front/test/app-model.test.ts`
- Create: `Front/tsconfig.test.json`
- Modify: `Front/package.json`
- Modify: `Front/src/App.tsx`

- [ ] **Step 1: Write the failing pure-state tests**

```ts
import test from 'node:test'
import assert from 'node:assert/strict'
import {
  getDefaultView,
  getVisibleCourseTabs,
  canManageDevices,
  isEligibilityVisible,
  type AppRole,
} from '../src/app/model'

test('student gets dashboard as the default view', () => {
  assert.equal(getDefaultView('student'), 'dashboard')
})

test('only students see the eligibility tab', () => {
  assert.deepEqual(getVisibleCourseTabs('student'), ['notices', 'eligibility'])
  assert.deepEqual(getVisibleCourseTabs('professor'), ['notices'])
  assert.deepEqual(getVisibleCourseTabs('admin'), ['notices'])
})

test('device management is student-only', () => {
  const roles: AppRole[] = ['student', 'professor', 'admin']
  assert.deepEqual(roles.map((role) => canManageDevices(role)), [true, false, false])
})

test('eligibility panel visibility is student-only', () => {
  assert.equal(isEligibilityVisible('student'), true)
  assert.equal(isEligibilityVisible('professor'), false)
  assert.equal(isEligibilityVisible('admin'), false)
})
```

- [ ] **Step 2: Run the test command to confirm the seam does not exist yet**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npx tsc -p tsconfig.test.json && node --test .tmp-tests/test/app-model.test.js`

Expected: FAIL with a module-not-found or compile error for `src/app/model`

- [ ] **Step 3: Add the test compile target and script**

```json
{
  "scripts": {
    "test:unit": "tsc -p tsconfig.test.json && node --test .tmp-tests/test/**/*.test.js"
  }
}
```

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": ".tmp-tests",
    "module": "nodenext",
    "target": "es2022",
    "lib": ["es2022", "dom"],
    "types": ["node"],
    "noEmit": false
  },
  "include": ["src/**/*.ts", "test/**/*.ts"]
}
```

- [ ] **Step 4: Implement the pure state model**

```ts
export type AppRole = 'student' | 'professor' | 'admin'
export type AppView = 'dashboard' | 'profile' | 'course'
export type CourseTab = 'notices' | 'eligibility'

export function getDefaultView(_role: AppRole): AppView {
  return 'dashboard'
}

export function getVisibleCourseTabs(role: AppRole): CourseTab[] {
  return role === 'student' ? ['notices', 'eligibility'] : ['notices']
}

export function canManageDevices(role: AppRole) {
  return role === 'student'
}

export function isEligibilityVisible(role: AppRole) {
  return role === 'student'
}
```

- [ ] **Step 5: Replace inline role checks in `App.tsx` with `model.ts` helpers**

```ts
const role = currentUser?.role ?? null
const visibleCourseTabs = role ? getVisibleCourseTabs(role) : []
const deviceManagementEnabled = role ? canManageDevices(role) : false
const eligibilityVisible = role ? isEligibilityVisible(role) : false
```

- [ ] **Step 6: Run the unit tests**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run test:unit`

Expected: PASS for `app-model.test.ts`

- [ ] **Step 7: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add package.json tsconfig.test.json src/app/model.ts test/app-model.test.ts src/App.tsx
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): isolate role state before redesign

The current UI mixes role visibility rules directly into rendering,
which makes a visual rewrite risky. Extracting the state model gives us
a small seam we can test before reshaping the shell.

Constraint: No new test dependency for the first pass
Rejected: Redesign first and test later | behavior regressions would be too easy to miss
Confidence: high
Scope-risk: narrow
Directive: Keep business eligibility decisions in backend-owned data; this model only decides visibility
Tested: npm run test:unit
Not-tested: Browser layout"
```

### Task 3: Add role-aware navigation and human-readable presenters

**Files:**
- Create: `Front/src/features/navigation/navigation.ts`
- Create: `Front/src/features/eligibility/presenter.ts`
- Create: `Front/test/navigation.test.ts`
- Create: `Front/test/eligibility-presenter.test.ts`
- Modify: `Front/src/App.tsx`

- [ ] **Step 1: Write the failing navigation and presenter tests**

```ts
import test from 'node:test'
import assert from 'node:assert/strict'
import { getPrimaryNavigation } from '../src/features/navigation/navigation'

test('student nav exposes dashboard, profile, and course workspace', () => {
  assert.deepEqual(
    getPrimaryNavigation('student').map((item) => item.id),
    ['dashboard', 'profile', 'course'],
  )
})

test('admin nav omits profile-only student actions', () => {
  assert.deepEqual(
    getPrimaryNavigation('admin').map((item) => item.id),
    ['dashboard', 'profile'],
  )
})
```

```ts
import test from 'node:test'
import assert from 'node:assert/strict'
import { presentEligibility } from '../src/features/eligibility/presenter'

test('blocked device state becomes user-facing copy plus raw reason code', () => {
  assert.deepEqual(presentEligibility('DEVICE_NOT_REGISTERED'), {
    tone: 'warning',
    title: '등록된 단말이 필요합니다.',
    body: '프로필에서 단말을 등록한 뒤 다시 확인하세요.',
  })
})
```

- [ ] **Step 2: Run tests to verify they fail first**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run test:unit`

Expected: FAIL with missing module errors for `navigation` and `presenter`

- [ ] **Step 3: Implement the role navigation definitions**

```ts
import type { AppRole, AppView } from '../../app/model'

export type NavigationItem = {
  id: AppView
  label: string
}

export function getPrimaryNavigation(role: AppRole): NavigationItem[] {
  if (role === 'admin') {
    return [
      { id: 'dashboard', label: '운영 현황' },
      { id: 'profile', label: '계정' },
    ]
  }

  return [
    { id: 'dashboard', label: '워크스페이스' },
    { id: 'profile', label: '프로필' },
    { id: 'course', label: '강의' },
  ]
}
```

- [ ] **Step 4: Implement the eligibility presenter**

```ts
type PresentedEligibility = {
  tone: 'success' | 'warning' | 'danger'
  title: string
  body: string
}

const MAP: Record<string, PresentedEligibility> = {
  OK: {
    tone: 'success',
    title: '출석 또는 시험 접근이 가능합니다.',
    body: '현재 단말과 강의실 조건이 확인되었습니다.',
  },
  DEVICE_NOT_REGISTERED: {
    tone: 'warning',
    title: '등록된 단말이 필요합니다.',
    body: '프로필에서 단말을 등록한 뒤 다시 확인하세요.',
  },
  NETWORK_NOT_ELIGIBLE: {
    tone: 'danger',
    title: '현재 네트워크에서는 확인할 수 없습니다.',
    body: '수업 강의실 네트워크 연결 상태를 점검하세요.',
  },
}

export function presentEligibility(reasonCode: string): PresentedEligibility {
  return (
    MAP[reasonCode] ?? {
      tone: 'warning',
      title: '추가 확인이 필요합니다.',
      body: '아래 reason code 와 evidence 를 확인하세요.',
    }
  )
}
```

- [ ] **Step 5: Wire the new definitions into `App.tsx`**

```ts
const navigationItems = role ? getPrimaryNavigation(role) : []
const eligibilityPresentation = eligibility
  ? presentEligibility(eligibility.reason_code)
  : null
```

- [ ] **Step 6: Run the unit tests**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run test:unit`

Expected: PASS for `app-model`, `navigation`, and `eligibility-presenter`

- [ ] **Step 7: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add src/features/navigation/navigation.ts src/features/eligibility/presenter.ts test/navigation.test.ts test/eligibility-presenter.test.ts src/App.tsx
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): make navigation and status copy explicit

The redesign needs stable information architecture and readable status
messaging before visual shell work starts. These presenters keep those
decisions out of JSX sprawl.

Constraint: Must preserve backend reason codes for debugging
Rejected: Show raw reason codes as the primary UI copy | too technical for real users
Confidence: high
Scope-risk: narrow
Directive: Add new reason codes in presenter.ts instead of sprinkling copy through components
Tested: npm run test:unit
Not-tested: Browser layout"
```

### Task 4: Replace the monolithic shell with a calmer workspace frame

**Files:**
- Create: `Front/src/app/AppShell.tsx`
- Create: `Front/src/features/auth/LoginScreen.tsx`
- Create: `Front/src/styles/tokens.css`
- Create: `Front/src/styles/base.css`
- Create: `Front/src/styles/surfaces.css`
- Modify: `Front/src/main.tsx`
- Modify: `Front/src/App.tsx`
- Modify: `Front/src/index.css`

- [ ] **Step 1: Create the token layer**

```css
:root {
  --bg: #f3efe8;
  --surface: rgba(255, 252, 247, 0.86);
  --surface-strong: #fffaf2;
  --text: #172033;
  --text-muted: #5f6b7d;
  --accent: #0d6b61;
  --accent-strong: #0b4f49;
  --line-soft: rgba(23, 32, 51, 0.08);
  --line-strong: rgba(23, 32, 51, 0.16);
  --success: #1c6b42;
  --warning: #9a5a12;
  --danger: #b33a28;
  --radius-xl: 28px;
  --radius-lg: 20px;
  --radius-md: 14px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
}
```

- [ ] **Step 2: Create the login surface as the only narrative screen**

```tsx
type LoginScreenProps = {
  loginId: string
  password: string
  error: string | null
  onLoginIdChange: (value: string) => void
  onPasswordChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function LoginScreen(props: LoginScreenProps) {
  return (
    <main className="login-screen">
      <section className="login-hero">
        <p className="kicker">Smart Class</p>
        <h1>수업 운영과 출석 확인을 하나의 워크스페이스로 정리합니다.</h1>
        <p>학생, 교수, 관리자 모두 같은 진입점을 사용하되 역할별 화면은 분리합니다.</p>
      </section>
      <section className="login-panel">
        <form onSubmit={props.onSubmit}>{/* existing fields reused here */}</form>
      </section>
    </main>
  )
}
```

- [ ] **Step 3: Create the authenticated app shell**

```tsx
type AppShellProps = {
  title: string
  subtitle: string
  health: 'checking' | 'online' | 'offline'
  navigationItems: { id: string; label: string }[]
  activeView: string
  accountName: string
  accountSummary: string
  onNavigate: (view: 'dashboard' | 'profile' | 'course') => void
  onLogout: () => void
  children: React.ReactNode
}

export function AppShell(props: AppShellProps) {
  return (
    <main className="workspace-shell">
      <aside className="workspace-nav">{/* nav buttons */}</aside>
      <section className="workspace-main">
        <header className="workspace-header">{/* title, health, account */}</header>
        <div className="workspace-body">{props.children}</div>
      </section>
    </main>
  )
}
```

- [ ] **Step 4: Replace the old topbar / auth JSX in `App.tsx` with the new components**

```tsx
if (!currentUser) {
  return (
    <LoginScreen
      loginId={loginId}
      password={password}
      error={error}
      onLoginIdChange={setLoginId}
      onPasswordChange={setPassword}
      onSubmit={handleLogin}
    />
  )
}

return (
  <AppShell
    title={view === 'course' && selectedCourse ? selectedCourse.title : 'Learning Workspace'}
    subtitle={roleSummary}
    health={health}
    navigationItems={navigationItems}
    activeView={view}
    accountName={currentUser.name}
    accountSummary={roleSummary}
    onNavigate={setView}
    onLogout={handleLogout}
  >
    {/* dashboard/profile/course render output */}
  </AppShell>
)
```

- [ ] **Step 5: Build the app to catch shell integration errors**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run build`

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add src/app/AppShell.tsx src/features/auth/LoginScreen.tsx src/styles/tokens.css src/styles/base.css src/styles/surfaces.css src/main.tsx src/App.tsx src/index.css
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): give the app a restrained workspace shell

The redesign needs a structural break from the current panel stack.
Separating the login surface from the authenticated workspace lets us
use narrative only where it helps and restraint where users operate.

Constraint: No UI library or runtime dependency change
Rejected: Keep one global page frame and restyle in place | structure would still fight the new hierarchy
Confidence: medium
Scope-risk: moderate
Directive: Do not reintroduce hero-style composition inside authenticated product screens
Tested: npm run build
Not-tested: Mobile browser screenshots"
```

### Task 5: Move each role flow into focused surfaces and reduce generic cards

**Files:**
- Create: `Front/src/features/dashboard/DashboardView.tsx`
- Create: `Front/src/features/profile/ProfileView.tsx`
- Create: `Front/src/features/course/CourseView.tsx`
- Modify: `Front/src/App.tsx`
- Modify: `Front/src/styles/surfaces.css`

- [ ] **Step 1: Create the dashboard surface with role-based sections**

```tsx
type DashboardViewProps = {
  role: 'student' | 'professor' | 'admin'
  courses: Course[]
  notices: Notice[]
  adminUsers: UserSummary[]
  adminClassrooms: Classroom[]
  adminNetworks: ClassroomNetwork[]
  onOpenCourse: (course: Course) => void
}

export function DashboardView(props: DashboardViewProps) {
  if (props.role === 'admin') {
    return <AdminOperationsPanel /* ... */ />
  }

  return <CourseAndNoticeWorkspace /* ... */ />
}
```

- [ ] **Step 2: Create the profile surface with account, device form, and device list**

```tsx
export function ProfileView(props: ProfileViewProps) {
  return (
    <section className="workspace-columns">
      <AccountPanel /* ... */ />
      <DeviceRegistrationPanel /* ... */ />
      <DeviceInventoryPanel /* ... */ />
    </section>
  )
}
```

- [ ] **Step 3: Create the course surface with main content plus inspector rail**

```tsx
export function CourseView(props: CourseViewProps) {
  return (
    <section className="course-workspace">
      <article className="course-primary">{/* notices or eligibility */}</article>
      <aside className="course-secondary">{/* tabs, metadata, classroom */}</aside>
    </section>
  )
}
```

- [ ] **Step 4: Replace repeated `device-card` rendering with more specific surface classes**

```css
.workspace-list {
  display: grid;
  gap: var(--space-3);
}

.list-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--space-4);
  padding: var(--space-4);
  border-top: 1px solid var(--line-soft);
}
```

- [ ] **Step 5: Build and lint**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run lint && npm run build`

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add src/features/dashboard/DashboardView.tsx src/features/profile/ProfileView.tsx src/features/course/CourseView.tsx src/App.tsx src/styles/surfaces.css
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): split role flows into focused workspace surfaces

The app no longer benefits from one giant component once the visual
language becomes role-aware. Focused surfaces let each role use clear
regions instead of repeating generic cards.

Constraint: Must preserve current role capabilities
Rejected: Keep role branches inline in App.tsx | too brittle for ongoing redesign work
Confidence: medium
Scope-risk: moderate
Directive: New role UI belongs in feature surfaces, not back in App.tsx
Tested: npm run lint; npm run build
Not-tested: Cross-role manual browser flow"
```

### Task 6: Run browser verification and trim visual clutter

**Files:**
- Modify: `Front/src/styles/surfaces.css`
- Modify: `Front/src/features/auth/LoginScreen.tsx`
- Modify: `Front/src/features/dashboard/DashboardView.tsx`
- Modify: `Front/src/features/profile/ProfileView.tsx`
- Modify: `Front/src/features/course/CourseView.tsx`

- [ ] **Step 1: Start the app for visual review**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run dev -- --host 0.0.0.0 --port 3000`

Expected: local app available at `http://127.0.0.1:3000`

- [ ] **Step 2: Verify the login surface on desktop and mobile**

Checklist:

- headline fits in roughly 2-3 lines on desktop
- supporting copy is one short sentence
- form remains readable on narrow mobile width
- decorative treatment does not overpower the form

- [ ] **Step 3: Verify the authenticated app surface for each role**

Checklist:

- no dashboard-card mosaic
- one primary workspace region is obvious
- accent color is used sparingly
- JSON evidence is behind a lower-priority disclosure treatment
- admin inventory reads as operations UI, not marketing UI

- [ ] **Step 4: Remove any styling that still looks decorative without doing narrative work**

```css
/* Delete shadow-heavy or gradient-heavy rules that do not improve hierarchy */
.legacy-card-shadow {
  box-shadow: none;
}
```

- [ ] **Step 5: Run final verification**

Run: `cd /Users/kimhyeonseok/CodeStorage/smart-class/Front && npm run test:unit && npm run lint && npm run build`

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front add src/styles/surfaces.css src/features/auth/LoginScreen.tsx src/features/dashboard/DashboardView.tsx src/features/profile/ProfileView.tsx src/features/course/CourseView.tsx
git -C /Users/kimhyeonseok/CodeStorage/smart-class/Front commit -m "feat(frontend): finish the redesign with visual verification

The last pass is where scaffold habits usually come back through
unnecessary chrome. A deliberate visual trim keeps the product closer to
the documented design rules.

Constraint: Must finish with the existing runtime and feature set
Rejected: Stop after structural refactor only | the UI would still look unfinished
Confidence: medium
Scope-risk: moderate
Directive: If a border, shadow, radius, or panel can be removed without hurting comprehension, remove it
Tested: npm run test:unit; npm run lint; npm run build; desktop/mobile browser verification
Not-tested: Real production traffic"
```

## Self-review

### Spec coverage

- Preserve current behavior: covered by Tasks 2-6.
- Change the design method, not just the CSS: covered by Task 1.
- Apply GPT-5.4 front-end article ideas: reflected in Task 1 rules, Task 4 shell split, and Task 6 visual trimming.
- Keep the current stack: reflected in all tasks by staying on React + TypeScript + CSS with no new runtime dependency.

### Placeholder scan

Search plan for common placeholders before execution:

Run: `pattern='TB''D|T''ODO|implement later|fill in details|appropriate error handling|Write tests for the above|Similar to Task'; rg -n "$pattern" /Users/kimhyeonseok/CodeStorage/smart-class/docs/superpowers/plans/2026-03-30-front-delight-redesign.md`

Expected: no matches

### Type consistency

- `AppRole`, `AppView`, and `CourseTab` are defined in `src/app/model.ts`.
- `navigation.ts` consumes `AppRole` and `AppView`.
- `presenter.ts` is string-in, UI-copy-out, and does not invent backend fields.
- `App.tsx` remains the composition root only until later cleanup removes old inline rendering.
