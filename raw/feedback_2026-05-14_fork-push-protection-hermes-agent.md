---
name: fork-push-protection-clean-branch-hermes-agent
description: hermes-agent fork (jleechanclaw) has old openclaw commits with embedded secrets; push to upstream requires clean branch from hermes/main
type: feedback
bead: orch-havc
date: 2026-05-14
---

## Context

`jleechanorg/hermes-agent` has two remotes in local worktrees:
- `origin` = `https://github.com/jleechanorg/jleechanclaw.git` (fork with full history)
- `hermes` = `https://github.com/jleechanorg/hermes-agent.git` (canonical upstream)

The fork (`jleechanclaw`) retains old pre-migration commits (openclaw era) that contain embedded API keys:
- Discord Bot Tokens in `launchd/ai.openclaw.gateway.plist`
- xAI API keys, Slack tokens, Groq API keys in `openclaw.json`

GitHub Push Protection blocks any push to `hermes` that includes these commits.

## Problem

Session branches like `session/ha-14` (based on the fork's `main`) are ~50 commits ahead of `hermes/main` due to divergent history (squash merge / rebase). Pushing these branches to `hermes` remote triggers Push Protection on the old commits.

## Solution

1. Create a clean branch from `hermes/main`:
   ```bash
   git checkout -b fix/<topic> hermes/main
   ```
2. Cherry-pick only the specific fix commit(s):
   ```bash
   git cherry-pick <sha>
   ```
3. Resolve any `.gitignore` conflict (upstream is NousResearch-style, fork is openclaw-style — different content)
4. Push the clean branch to `hermes`:
   ```bash
   git push hermes fix/<topic>
   ```
5. Open PR from `jleechanorg/hermes-agent:fix/<topic>` → `main`

## Verification

PR #13 created successfully: https://github.com/jleechanorg/hermes-agent/pull/13

## Reusable Pattern

**Rule:** In hermes-agent worktrees, ALWAYS use a `fix/*` or `feat/*` branch based on `hermes/main` when opening PRs against `jleechanorg/hermes-agent`. Never push `session/ha-*` branches directly to the `hermes` remote.

**jeffrey-oracle**: not affected (ops/workflow discipline)
