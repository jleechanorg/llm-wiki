---
name: fable-5-1-missing-from-model-picker-is-an-upstream-claude-code-bug
description: "/model picker never lists a modelPicker.options entry unless it's the session's active model; confirmed via 8 real upstream GitHub issues, not a local settings.json error"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-fable-model-picker-upstream (see roadmap entry; no fix possible in this repo)
  originSessionId: a252645b-d06d-4174-b5d5-398b580cad49
  modified: 2026-09-06T21:59:09.027Z
---

## Context

User asked why "Fable 5.1" (claude-fable-5-1) didn't show in the interactive
`/model` picker in Claude Code v2.1.259, even after another agent had already
added it to `modelPicker.options` in `~/.claude/settings.json`. Investigated
across two turns: local repro (settings/binary/tmux) then web verification.

## Technical detail

- `~/.claude/settings.json` had a syntactically correct entry:
  `modelPicker.options: [{model: "claude-fable-5-1", label: "Fable 5.1"}]`.
- `claude-fable-5-1` is a real, fully-registered catalog model (confirmed via
  binary `strings` search on the compiled CLI: Bedrock ids
  `us.anthropic.claude-fable-5-1` / `anthropic.claude-fable-5-1`, Vertex region
  `VERTEX_REGION_CLAUDE_FABLE_5_1`, pricing tier `tier_10_50_cache_read_0_25`).
- Reproduced in a brand-new `tmux` session (ruling out session-cache staleness):
  `/model` still only listed Default/Opus/Sonnet/Haiku.
- No competing config found: no `managed-settings.json`, no `policy-limits.json`
  on this machine, no `settings.local.json` overriding the key.
- **Root mechanism found by direct testing**: `claude --model claude-fable-5-1`
  at launch works immediately (banner shows "Fable 5.1 with high effort",
  session runs fine). Inside THAT session, `/model` then lists Fable fully
  (checked, real description). Plain `claude` (no `--model` flag) never offers
  it. So the picker's visible list = fixed GA lineup + whatever model the
  session was actually launched with — `modelPicker.options` does not inject
  rows for non-active models in this build.

## Upstream verification (fetched live via `gh api`, not just search-summary text)

All 8 issues confirmed to exist with matching titles:
- **anthropics/claude-code#66827** (closed) — root cause: server-pushed
  `~/.claude/policy-limits.json` had `allow_cobalt_plinth: false`; manually
  editing to `true` was silently reverted by the server on next restart —
  proves it's server-controlled, not client-fixable. Two other users
  (`paolomainardi`, `jimmystridh`) confirmed in comments; one from an
  org with `managed-settings.json` explicitly listing `claude-fable-5` in
  `availableModels` — still didn't fix it. (Note: this specific file didn't
  exist on this machine, so not an identical local artifact — same failure
  class though.)
- **#73423** (closed) — exact match: picker shows "Fable (disabled)"
  while `claude --model claude-fable-5` works and the banner confirms
  entitlement. Reporter's diagnosis: stale/cached gating flag left over
  from a June 12 suspension not invalidated after a July 1 re-enable.
- **#73333** (closed) — same pattern; notably "My teammates do not have
  this problem and can choose fable" — proves it's account/session-flag
  specific, not a universal client bug or local misconfig.
- **#82797** (closed) — Team Premium seat, entitled per plan, picker still
  showed "Requires usage credits"; worked fine in Claude Desktop same account.
- All four were closed by the inactivity bot — never actually fixed upstream.

## Rule / pattern

When a Claude Code `/model` picker entry from `modelPicker.options` doesn't
appear, do NOT assume the settings.json syntax is wrong. First test
`claude --model <id>` directly — if that works, the model is truly entitled
and the picker's absence is a display-only bug (picker lists GA lineup + the
launch-time active model only, in v2.1.259). Verify via `gh api
repos/anthropics/claude-code/issues/<n>` (not WebSearch summaries alone,
which can restate hallucinated detail) before telling a user "this is a
known bug" — confirm titles/bodies/comments actually exist and match.

## Fix vs. workaround

This is third-party code (Anthropic's Claude Code CLI) — no fix possible
from this repo or account. Workaround only:
- **Best**: `claude --model fable` (or `claude-fable-5-1`) per session —
  zero side effects, confirmed working.
- **Avoid**: editing the top-level `"model"` key in `~/.claude/settings.json`
  to force Fable as the global default — this silently changes the default
  for every future session across all worktrees. See
  [[feedback_2026-09-03_silent_model_downgrade_after_quota_reset]] for why
  silent model-default changes are specifically flagged as risky for this
  user.

## Verification

- `gh api repos/anthropics/claude-code/issues/<66827|73423|73333|82797|...>`
  returned real title/state/created_at/body/comments for all 8 cited issues.
- Local repro: fresh tmux session, `strings` search on compiled CLI binary,
  `claude --model claude-fable-5-1 -p "..."` exit 0.
- Findings archived at `/tmp/jc-fable-picker-investigation/findings.md`
  (scratch dir, not committed to any repo).
