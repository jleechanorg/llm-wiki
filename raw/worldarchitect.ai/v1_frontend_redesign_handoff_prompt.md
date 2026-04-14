# Prompt: Audit Every V1 Screen and Produce a V2 Redesign Spec (Same Functionality)

You are auditing the WorldAI v1 frontend running locally at `http://localhost:8066` and must produce a V2 redesign plan that preserves all existing functionality.

## Mission
1. Visit every user-facing screen and modal in v1.
2. Explain the current UI/UX in enough detail that an implementation agent can rebuild it in v2 with improved design.
3. Keep all behavior/functionality identical unless explicitly flagged as optional enhancement.
4. Provide implementation-ready output: route map, component map, interaction matrix, API dependencies, and parity checklist.

## Auth Setup (from project skills)
Use `.claude/skills/worldai-auth.md` and `.claude/skills/worldai-browser-login.md` guidance.

### Token + login commands
Run from repo root:
```bash
node .claude/scripts/auth-worldai.mjs status
node .claude/scripts/auth-worldai.mjs login
node .claude/scripts/auth-worldai.mjs token
```

Token location:
- `~/.ai-universe/auth-token-worldarchitecture-ai.json`

### Browser auth flow
1. Open `http://localhost:8066`.
2. Click `Sign in with Google` if shown.
3. Complete Firebase Google OAuth popup.
4. Confirm login success by verifying user email + campaigns list are visible.

If local test-mode bypass is required in dev, use:
- `?test_mode=true&test_user_id=test-user-123&test_user_email=test@example.com`

## Required Screen Coverage
You must inspect each of these routes/states:
1. `/` (auth view when signed out, dashboard when signed in)
2. `/new-campaign`
3. `/game/<campaign_id>` (use a real campaign id from dashboard)
4. `/settings`

Also cover these UI states/modals/components:
1. Theme/settings dropdown in navbar (Light/Dark/Fantasy/Cyberpunk)
2. Dashboard campaign list item interactions:
- open campaign
- edit campaign title modal
- load more campaigns
- search/filter UI if present
3. New campaign flow:
- Dragon Knight vs Custom
- description collapse/expand
- expertise checkboxes
- default world toggle
- submit and navigation to game
4. Game screen controls:
- back to dashboard
- settings button
- spicy mode toggle + tooltip
- download button + `Download Story As...` modal (`txt`, `pdf`, `docx`)
- share button
- interaction textarea + send
- mode radios (`Character`, `Think/Plan`, `God`) + tooltips
- planning block choice buttons (including risk display and switch-to-story behavior)
- quick action buttons that appear in story entries (`Equipment`, `Stats`, `Spells`)
- story pagination (`Load older entries`) behavior when available
- debug indicator visibility behavior
- BYOK indicator visibility behavior
5. Settings page controls:
- provider radio group (`Gemini`, `OpenRouter`, `Cerebras`)
- model dropdowns per provider
- BYOK key inputs for all providers
- show/hide key toggle and clear key actions
- debug mode switch
- faction minigame switch
- save/error/loading feedback alerts
- confirmation modal
- back to home button

## What to Document for Each Screen/State
For each route/state above, write:
1. **Purpose**: why the screen exists.
2. **Layout map**: top/nav/main/side/footer regions and hierarchy.
3. **Components**: controls, labels, help text, default values.
4. **Interactions**: click, submit, toggle, hover tooltip, modal open/close, keyboard behavior.
5. **Data dependencies**: API endpoints and payload fields required.
6. **State transitions**: where user can navigate from/to.
7. **Functional parity requirements**: what must be preserved in v2.
8. **UX pain points**: what should be redesigned visually/structurally without removing behavior.

## Key API/Behavior Dependencies to Preserve
Preserve frontend behavior against these endpoints (non-exhaustive):
- `GET /api/campaigns`
- `GET /api/campaigns/<id>`
- `GET /api/campaigns/<id>/story`
- `POST /api/campaigns`
- `PATCH /api/campaigns/<id>`
- `POST /api/campaigns/<id>/interaction`
- `POST /api/campaigns/<id>/interaction/stream`
- `GET /api/campaigns/<id>/equipment`
- `GET /api/campaigns/<id>/stats`
- `GET /api/campaigns/<id>/spells`
- `GET /api/campaigns/<id>/export`
- `GET/POST /api/settings`

## Deliverables
Produce all of the following:
1. Full route + state inventory.
2. Component inventory mapped to route/state.
3. Functional parity checklist (must-pass list for v2).
4. UX redesign brief (visual hierarchy, typography, spacing, accessibility, responsiveness).
5. Proposed v2 information architecture and navigation model.
6. V2 implementation plan broken into phased tickets.
7. Risks/unknowns and validation plan.

## Output Format (strict)
1. `Route/State Matrix`
2. `Screen-by-Screen UI Spec`
3. `Interaction + API Contract Matrix`
4. `V1 -> V2 Parity Checklist`
5. `Redesign Direction (No Functional Regressions)`
6. `Execution Plan`

Do not skip any route/state listed above.
