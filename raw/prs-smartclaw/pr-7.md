# PR #7: docs: add OpenClaw 3-stage dev pipeline

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-04-02
**Author:** jleechan2015
**Stats:** +393/-0 in 2 files

## Summary
(none)

## Raw Body
Adds `docs/openclaw-dev-pipeline.md` — a fully automated 3-stage development pipeline:

**Stage 1 — Feature worktrees + integration tests**
- `~/.openclaw-worktrees/feat-*/` — one worktree per feature
- Python test suite runs without a full gateway
- PR → CodeRabbit review → skeptic-cron merges

**Stage 2 — Staging Docker gateway**
- `~/.openclaw-staging/` as a git worktree on `staging` branch
- Docker container runs the full gateway
- On merge to staging: Docker restarts, integration tests run, PR to main opens
- Sibling doc: `openclaw-docker-staging-setup.md` (already PR #6)

**Stage 3 — Production `~/.openclaw/`**
- `~/.openclaw/` as a worktree on `main`
- Native Node.js gateway via launchd
- On merge to main: launchd restarts gateway

**Core principle:** No human edits `~/.openclaw/` directly. All changes flow through the pipeline.

**Key scripts proposed:**
- `staging-promote.sh` — restart Docker, run tests, open PR to main
- Git hooks in worktrees for auto-restart on push

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Documentation-only change plus a new `.gitignore` entry to prevent committing a local staging gateway token; no runtime or production code paths are modified.
> 
> **Overview**
> Adds `docs/openclaw-dev-pipeline.md`, documenting a 3-stage workflow (feature worktrees → Docker-based staging gateway → launchd-managed production) including suggested hooks/automation, health checks, and promotion steps.
> 
> Updates `.gitignore` to exclude `.gateway-token`, a local file used to store the staging gateway auth token referenced by the new doc.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 9991872a5cc1976fef67ac47e4c812ea4d1912ac. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **Documentation**
  * Added comprehe
