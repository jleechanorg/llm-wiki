# PR #1: Add RPGClaw MVP Design Doc

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-17
**Author:** jleechan2015
**Stats:** +6074/-2 in 22 files

## Summary
- Add initial design doc for WorldAI Claw MVP - lightweight RPG mobile app
- Based on design from worldarchitect.ai PR 9ed14f0
- Includes architecture, 50k context logic, API contracts, and implementation plan

## Test Plan
- [ ] Review design for completeness
- [ ] Validate architecture decisions
- [ ] Check implementation phases are properly ordered

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Mostly documentation and tooling/scaffolding changes; minimal runtime risk since no application code paths are modified.
> 
> **Overview**
> Introduces an **MVP design specification** in `roadmap/worldai_claw_mvp.md`, detailing the intended architec

## Raw Body
## Summary
- Add initial design doc for WorldAI Claw MVP - lightweight RPG mobile app
- Based on design from worldarchitect.ai PR 9ed14f0
- Includes architecture, 50k context logic, API contracts, and implementation plan

## Design Overview
- **Frontend**: React Native (iOS + Android)
- **Backend**: Node.js web service (Fastify)
- **Inference**: OpenClaw only (no multi-provider abstraction)
- **Transport**: SSE streaming
- **Context**: 50k max, 10k system prompt cap

## Test plan
- [ ] Review design for completeness
- [ ] Validate architecture decisions
- [ ] Check implementation phases are properly ordered

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Mostly documentation and tooling/scaffolding changes; minimal runtime risk since no application code paths are modified.
> 
> **Overview**
> Introduces an **MVP design specification** in `roadmap/worldai_claw_mvp.md`, detailing the intended architecture (RN mobile + Fastify backend), SSE streaming contract, token-budget/compaction rules, and phased implementation plan.
> 
> Adds initial **repo scaffolding**: new root/workspace `package.json`, backend TypeScript package config (`packages/backend/package.json`, `tsconfig.json`), and expands `README.md` with architecture/project structure and dev commands.
> 
> Includes developer productivity scripts for Git workflows and Claude tooling (`create_worktree.sh`, `integrate.sh`, `schedule_branch_work.sh`, and a large `scripts/claude_mcp.sh` installer).
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 33661cff61595704f242103ff18d0200771344bc. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->
