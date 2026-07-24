---
title: "End-State Layer Principle"
type: concept
tags: [verification, infrastructure, harness, agent-behavior]
date: 2026-06-28
last_updated: 2026-06-28
---

## End-State Layer Principle

When a tool reports "success" or "healthy" (e.g. `Listening for Jobs`, `Up X minutes`, `=== done: healthy ===`), that's the **implementation layer** saying the tool did its part. It does NOT prove the **end-state layer** is correct.

### Cross-check matrix

| Tool layer | End-state layer (must verify) |
|------------|------------------------------|
| Runner.Listener logs `Listening for Jobs` | `gh api .../runners` shows `status:"online"` |
| Container `Up X minutes` | Health check endpoint returns 200 |
| `git push` reports success | PR appears in `gh pr list --head <branch>` |
| `npm test` exit 0 | CI workflow run `conclusion:"success"` |
| `docker compose up -d` exits 0 | `docker ps` shows container with `Up` |

### Why this matters

The runner-fleet hardening PRs (#7851, #8024, #8026, #8027) merged cleanly with Green Gate passing, but `/advice` reviewer caught that the agent claimed "runners healthy" without verifying the actual end-state. Probes revealed:
- Bind-mount source on Lima VM did match the deployed path (lucky this time)
- Hook md5 inside running container matched the deployed file
- GITHUB_REPOSITORY was being set by runner before hook fires
- BUT: check_github_session_state filtered only `org-runner-mac-*`, missing the same session-conflict class on 16 Linux runners
- AND: silent skip on `gh api` failure returned 0, creating meta-divergence

### Rule

Before claiming "X is working" or "system is healthy", verify at the end-state layer. If you can only cite the implementation-layer tool's output, say so explicitly: "Runner.Listener is listening, but I have not verified GitHub-side registration."

### Anti-pattern: silent skip on health-check API failure

A check function that returns 0 silently when the underlying API (e.g. `gh api`) fails is exactly the silent-divergence failure class it's supposed to catch. Returning 0 on auth failure creates a meta-divergence: can't see divergence because the divergence detector is offline.

Correct pattern: capture stderr, log the failure, add to failure_reasons, return 1.

### Generalization of existing rules

This principle is a generalization of:
- "Multi-gate Runtime Activation Claim Rule" — already in ~/.claude/CLAUDE.md
- "Cache-specific activation gate" — already in ~/.claude/CLAUDE.md
- "Verify before reporting" — exists as a skill

Applied to any tool-status-vs-reality check across any infrastructure domain.

### Related

- [[LimaVM]] — primary place where the runner fleet's tool-status-vs-end-state divergence happens
- [[RunnerSessionConflict]] — the specific failure class caught by Probe 4 (GitHub-side vs container-side divergence)
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — broader category including busy=true corruption
- [[ClaimedWorkingVsActuallyWorking]] — sibling memory with the 5-probe checklist
