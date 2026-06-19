---
name: hermes-liveness-verification-merge-readiness-checklist
description: "Two reusable verification protocols — 6-check Hermes liveness (behavior over path) and 5-gate merge-readiness before any \"should we merge\" question"
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-9l6p
  originSessionId: 4c98f23b-a506-44ef-b4c9-671dedd6e981
---

# Hermes Liveness Verification + Merge-Readiness Gate

## When
2026-06-19, during `/learn` invocation after user asked "do we need to merge `fix/mcp-daemon-keepalive` to origin main?"

## Context
Two patterns emerged in one session:
1. **Hermes liveness verification** — ran the same 6-check battery twice, ~4 hours apart, same PID 28443 stable, both canary acks in 5.5s/7.4s.
2. **Merge-readiness gate** — user asked the merge question, branch had 5 hard blockers (uncommitted M+??, no PR, scope creep, no canary, no MERGE APPROVED).

## Lesson 1: Hermes liveness check (behavior > path)

When asked "is Hermes working?", run 6 checks **in parallel**. **Trust behavioral evidence over path-based assumptions** — auth-profiles.json path check failed in this build but the LLM was clearly responding.

| # | Check | Pass signal |
|---|---|---|
| 1 | `curl -fsS -m 8 http://127.0.0.1:8643/health` | `{"status":"ok","platform":"hermes-agent"}` |
| 2 | `pgrep -f "hermes gateway" \| wc -l` | exactly `1` (NOT >1 — lock storm precursor) |
| 3 | `launchctl print gui/$UID/ai.hermes.prod \| grep -E "state\|last exit\|pid"` | `state=running` + non-null PID |
| 4 | `tail -n 30 ~/.hermes_prod/logs/gateway.log` | recent inbound→response pairs with `api_calls > 0` |
| 5 | Synthetic canary ack in C0AKALZ4CKW (12-char `ack-<hex>`) | reply within <30s |
| 6 | `tail -n 30 ~/.hermes_prod/logs/gateway.err.log` | empty (no `session file locked`, no `lane wait exceeded`) |

**False positive to avoid**: `~/.hermes_prod/agents/main/agent/auth-profiles.json` missing does NOT mean Hermes is broken. In the 2026-06-18 build, auth-profiles lives elsewhere (likely env-var or different path), and the LLM still responds. Confirm via behavioral evidence (checks #4 + #5) before declaring broken — but if EITHER #4 OR #5 shows failure, treat as broken.

**Single-instance is mandatory** — `>1` gateway process = lock storm = WS pong starvation = HTTP 200 but no real work. Run `pgrep -f "hermes gateway" | wc -l` BEFORE declaring operational.

**Stable PID across 4h** (28443 unchanged) is a strong health signal — no restart storm, no memory leak forcing recycle.

## Lesson 2: Merge-readiness checklist (5 gates)

When user asks "do we need to merge `<branch>` to origin main?", run these 5 gates BEFORE answering. Every gate must pass; any fail → answer is NO with the specific blocker cited.

| # | Check | Pass signal |
|---|---|---|
| 1 | `git status --short` | EMPTY (no uncommitted M/?? files) |
| 2 | `git log --oneline origin/main..HEAD` | commits exist with focused scope matching branch name |
| 3 | `gh pr list --head <branch> --state all` | exactly ONE PR open (or already merged) |
| 4 | `gh pr view <N> --json reviewDecision,mergeable` | `reviewDecision=APPROVED` AND `mergeable=true` AND Skeptic PASS for head SHA |
| 5 | Conversation grep for literal `MERGE APPROVED` | present in current thread (CLAUDE.md merge-safety rule) |

**Also required**: `scripts/staging-canary.sh` must have passed — per CLAUDE.md "Worktree Isolation", direct merges bypass the staging canary gate. Without canary pass, merge is unsafe even if all 5 gates above pass.

**Anti-patterns** (caught in this session):
- **Uncommitted changes get dropped on merge** — silent data loss. The 2026-06-19 session caught `fix/mcp-daemon-keepalive` with 11 `M` files (including `workspace/SOUL.md` — live policy!) and 7 `??` files (new untracked scripts).
- **Scope creep** — branch named `fix/mcp-daemon-keepalive` but commits touched 5e detector docs + untracked files included launchd-drift-audit + skills/worldarchitect + browserclaw spec. Should split into 3-4 PRs.
- **Merging without a PR** — `git push origin main` directly bypasses 7-green, CodeRabbit, Skeptic, and reviewer accountability. Forbidden by CLAUDE.md "Merge safety" rule.
- **Untracked `?? ` + deleted `D ` files** — easy to miss in `git status` if you only look at `M`. Always run `git status --short` (full porcelain) not just `git diff`.

## Why this matters

The 2026-06-19 session demonstrated both:
- **Hermes verification**: 6-check ran twice in 4h, both times PID 28443 stable, canary acks 5.5s/7.4s, real LLM responses streaming. No false alarms on auth-profiles path (assumed broken, proved working via check #4).
- **Merge question**: `fix/mcp-daemon-keepalive` had uncommitted M/?? changes, no PR, scope creep across mcp-daemon + 5e-detector + launchd-drift-audit + skills/worldarchitect/. NOT safe to merge — answering "yes" without these gates would have lost ~18 file changes including live `workspace/SOUL.md`.

## Cross-refs
- CLAUDE.md "Gateway restart — single-instance mandatory" section
- CLAUDE.md "Liveness ≠ Functional (CRITICAL)" — but in this build, behavioral truth wins for THIS specific auth-profiles path
- CLAUDE.md "Worktree Isolation — Edit Your Copy, Not ~/.hermes/ Directly"
- CLAUDE.md "Merge safety — explicit MERGE APPROVED required"
- memory `feedback_2026-06-18_skill_branch_target_repo_clarification.md` (scope-creep pattern — wrong remote)

## Reusable pattern

```bash
# 6-check Hermes liveness (run in parallel, ~2s total)
curl -fsS -m 8 http://127.0.0.1:8643/health
pgrep -f "hermes gateway" | wc -l
launchctl print gui/$(id -u)/ai.hermes.prod | grep -E "state|last exit|pid"
tail -n 30 ~/.hermes_prod/logs/gateway.{log,err.log}
# optional: synthetic canary ack in C0AKALZ4CKW (requires Slack post)

# 5-check merge readiness (run in parallel, ~3s total)
git status --short
git log --oneline origin/main..HEAD
gh pr list --head $(git branch --show-current) --state all
gh pr view <N> --json reviewDecision,mergeable,headRefOid
# verify literal "MERGE APPROVED" in conversation before merging
```

## Verification

2026-06-19 03:30Z — both protocols ran cleanly. PID 28443 stable for 4+ hours across two liveness checks. Merge-readiness correctly flagged 5/5 gates failing on `fix/mcp-daemon-keepalive`.