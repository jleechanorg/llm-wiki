---
title: "Hermes liveness verification protocol + 5-gate merge-readiness checklist"
type: source
tags: [hermes, launchd, merge, verification, protocol]
date: 2026-06-19
source_file: feedback_2026-06-19_hermes_liveness_and_merge_readiness.md
---

## Summary
Two reusable verification protocols emerged from one session on 2026-06-19. The **6-check Hermes liveness** battery (curl /health + pgrep single-instance + launchctl state + gateway.log real responses + canary ack + gateway.err.log empty) runs in ~2s and proves the gateway is functional via behavioral evidence — even when canonical auth-profiles.json path is missing. The **5-gate merge-readiness** checklist (git status clean + PR exists + 7-green+mergeable+Skeptic PASS + literal `MERGE APPROVED` in thread + staging canary passed) catches the silent-data-loss and scope-creep anti-patterns that cause most merge failures.

## Key Claims
- Behavioral evidence (real LLM responses + canary ack) overrides path-based assumptions: `~/.hermes_prod/agents/main/agent/auth-profiles.json` missing at the canonical path does NOT mean Hermes is broken.
- Single-instance is mandatory: `pgrep -f "hermes gateway" | wc -l` MUST equal `1`. `>1` = lock storm = WS pong starvation = HTTP 200 with no real work (root cause of the 2026-04-05 outage).
- Stable PID across hours is a strong health signal — PID 28443 unchanged across 4+ hours on 2026-06-19.
- A branch is not mergeable to `origin/main` until all 5 gates pass; uncommitted M/?? files get silently dropped on merge (silent data loss).
- Scope creep between branch name and commits is a separate failure mode — `fix/mcp-daemon-keepalive` had commits touching 5e detector docs + untracked launchd-drift-audit + skills/worldarchitect + browserclaw spec; should be split into 3-4 PRs.

## Key Quotes
> "Liveness ≠ Functional (CRITICAL): HTTP /health returns {ok:true,status:live} even when the agent cannot authenticate. A gateway is only truly functional if (1) liveness passes AND (2) auth-profiles.json exists..." — CLAUDE.md

> "Never run gh pr merge, gh api .../pulls/N/merge, or push directly to a default branch (main/master) without an explicit MERGE APPROVED from the user in the current conversation thread. The literal phrase 'MERGE APPROVED' is the only valid trigger." — CLAUDE.md merge-safety rule

## Connections
- [[HermesGateway]] — the operational surface being verified; PID 28443 stable across the session
- [[fix-mcp-daemon-keepalive]] — the branch that triggered the merge-readiness check (5/5 gates failed)
- [[LivenessVsFunctionality]] — broader pattern; this protocol extends the CLAUDE.md caveat with behavioral override
- [[MergeApprovedPattern]] — the literal `MERGE APPROVED` requirement that closes the merge-safety loop
- [[SingleInstanceDiscipline]] — the mandatory `pgrep == 1` check (CLAUDE.md gateway restart section)
- [[WorktreeIsolation]] — context: the staging canary gate and PR discipline this protocol enforces
- [[PhantomRevert]] — adjacent risk class: branches whose own diff looks clean but revert main work; the `git diff origin/main..HEAD` part of gate #2 catches this
- [[SlackSubclassMisroute5x]] — adjacent: the canary ack in check #5 catches sub-class 5 misroutes (5a/5b/5c/5d/5e) when they break the bot's ability to respond