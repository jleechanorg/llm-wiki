---
title: "heal-runners SIGKILL → GitHub session conflict loop"
type: source
tags: [feedback, self-hosted-oss, docker, github-actions, runners, infra]
date: 2026-06-18
source_file: ../../raw/feedback_2026-06-18_heal_runners_sigkill_session_conflict.md
---

## Summary
On 2026-06-18, heal-runners.sh:204 used `docker rm -f` to recycle Mac self-hosted runners — SIGKILL bypassed the myoung34/github-runner entrypoint's SIGTERM handler that calls actions/runner/remove. Orphaned GitHub sessions caused recycled containers to loop forever on `Runner connect error: Error: Conflict. Retrying until reconnected.` Fix: PR #7666 changed the recycle path to `docker stop --time=30 && docker rm` so the entrypoint cleans up its session before exit.

## Key Claims
- `docker rm -f` in heal-runners.sh caused a deterministic GitHub session conflict loop in 3 of 6 recycled runners (mac-1, -2, -4) on the 2026-06-18 15:27Z cycle; survivors (mac-3, -5, -6) only escaped by luck.
- `RUNNER_SELF_HEAL_REQUIRE_GH_BUSY_CHECK` at heal-runners.sh:150-156 explains why only some runners were recycled (busy=true → skip).
- The orphan-session problem is server-side; cannot be cleared via `gh api DELETE`; only via (a) GitHub's session timeout OR (b) `actions/runner/remove` from inside the runner process — exactly what SIGTERM triggers.
- Pattern applies to any containerized GitHub Actions runner (myoung34/github-runner, actions/runner) and any agent holding a long-poll WebSocket (buildkite-agent, drone-agent, circleci runner).
- Existing memory [[runner-supervisor-loop-and-rc-sourcing]] already documents the runtime-mirror pattern (`~/.local/share/worldarchitect-runners/` is the live copy, `self-hosted-oss/` is the source). This memory documents the *causal* fix at the recycle site.

## Key Quotes
> "Survivors only escaped by luck — their old sessions happened to clear before the new container tried to start its session. Pure timing luck."

> "Containerized runners (or any agent holding a long-poll WebSocket to an upstream control plane) MUST be SIGTERM'd, never SIGKILL'd, on recycle."

## Connections
- [[runner-supervisor-loop-and-rc-sourcing]] — companion memory covering the supervisor loop + runtime-mirror sync pattern. The new fix rides on the sync rule.
- [[heal-runners]] — concept page for the self-healing supervisor script.
- [[myoung34-github-runner]] — entity page for the OSS Docker image whose SIGTERM handler this fix relies on.
- [[GitHub Actions self-hosted runners]] — concept page for the org-level runner pool on jleechanorg.
- [[launchd]] — concept page for the macOS job supervisor wrapping heal-runners.sh.
- [[Docker container lifecycle]] — concept page where SIGTERM vs SIGKILL trade-offs are documented.
- [[jleechanorg/worldarchitect.ai PR #7666]] — entity page for the fix PR.
- [[bead rev-dsny5]] — closed learning bead referencing this episode.
