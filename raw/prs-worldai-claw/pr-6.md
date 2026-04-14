# PR #6: feat: MVP TDD roadmap implementation

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-22
**Author:** jleechan2015
**Stats:** +16972/-6952 in 102 files

## Summary
- Full-stack MVP lifecycle implementation with TDD evidence
- AbortController fixes for React StrictMode duplicate fetches
- OpenClaw settings wired frontend → backend (11434 → 18789)
- Mobile: disable direct OpenClaw mode by default for MVP safety
- Strip raw JSON planning_block from GM scene_text before rendering
- SSE header ordering, UUID sessions, abort timeout fixes
- Strict lifecycle evidence bundle persisted under docs/

## Test Plan
- [ ] Full lifecycle e2e test passes
- [ ] Mobile direct-OpenClaw disabled by default
- [ ] Frontend OpenClaw settings propagate to backend
- [ ] No duplicate SSE/fetch calls in React StrictMode

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Primarily documentation/evidence artifacts and local ignore-rule tweaks; no runtime code paths are changed in this diff, but it does add large static test artifacts to the repo.
> 
> *

## Raw Body
## Summary
- Full-stack MVP lifecycle implementation with TDD evidence
- AbortController fixes for React StrictMode duplicate fetches
- OpenClaw settings wired frontend → backend (11434 → 18789)
- Mobile: disable direct OpenClaw mode by default for MVP safety
- Strip raw JSON planning_block from GM scene_text before rendering
- SSE header ordering, UUID sessions, abort timeout fixes
- Strict lifecycle evidence bundle persisted under docs/

## Replaces
- PR #4 (`pr-2-codex-implement-tdd-for-worldai_claw_mvp-roadmap-work`)
- Old branch `pr-4-pr-2-codex-implement-tdd-for-worldai_claw_mvp-roadmap-work-work`

No work lost — all commits from prior branches included.

## Test plan
- [ ] Full lifecycle e2e test passes
- [ ] Mobile direct-OpenClaw disabled by default
- [ ] Frontend OpenClaw settings propagate to backend
- [ ] No duplicate SSE/fetch calls in React StrictMode

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Primarily documentation/evidence artifacts and local ignore-rule tweaks; no runtime code paths are changed in this diff, but it does add large static test artifacts to the repo.
> 
> **Overview**
> Adds a checked-in **strict `testing_ui` lifecycle evidence bundle** under `docs/evidence/…`, including a run README plus captured browser/API/MCP traces, server traces/logs, and LLM HTTP/request-response artifacts for review.
> 
> Updates ops/docs guidance by adding a `video-frame-review` skill doc and tightening `CLAUDE.md` rules to forbid mock LLM/server modes in `testing_ui/` and `testing_mcp/`.
> 
> Refines `.beads/.gitignore` to ignore Dolt state and other runtime/legacy DB artifacts, and trims `.beads/issues.jsonl` to a small set of newly-filed roadmap issues.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 8088eea70e9270fa420b7ebc606b80dd89aecb6c. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bu
