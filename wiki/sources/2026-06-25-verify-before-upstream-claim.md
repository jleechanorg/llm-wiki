---
type: source
slug: 2026-06-25-verify-before-upstream-claim
title: "verify-before-upstream-claim (2026-06-25)"
date: 2026-06-25
origin: Slack thread C0ALSKLU9KM / 1782382574.896179
tags: [agent-mistakes, verify-first, slack-mcp, upstream-drift, fork-tracking, skill-class-level]
---

# Source — verify-before-upstream-claim (2026-06-25)

## Source

Slack thread `C0ALSKLU9KM / 1782382574.896179` (2026-06-25, 10:16-10:29 PT). User: Jeffrey Lee-Chan. Three consecutive corrections to the same thread:

1. *"Wait mine shouldn't be python I have an older fork"* — corrected a fabricated path claim.
2. *"What is this sub folder"* — pinned the hallucinated `~/.hermes/agent-orchestrator/` reference.
3. *"You have slack mcp"* — corrected "I can't fetch Slack URLs" claim.
4. *"Read this whole thread and look at all your mistakes and prevent them with the /skillify"* — the skillify directive.

## The three failures (verbatim)

### Failure 1 — Hallucinated local path

> "Compared to the Python `agent-orchestrator` you've been running locally (the `~/.hermes/agent-orchestrator/` we use)..."

Path does not exist. Real layout: Python AO is `~/.hermes/ao_runner/`, real source is TS fork `jleechanorg/agent-orchestrator` cloned at `~/projects/agent-orchestrator-684-thread-ts/`.

### Failure 2 — Fork/upstream conflation

> "Upstream `AgentWrapper/agent-orchestrator` went TypeScript → Go... Your fork is still on the older TS architecture."

Fork state was never verified. Claim was made without `gh api repos/jleechanorg/agent-orchestrator/languages`.

### Failure 3 — Tool-blindness

> "I don't have access to Slack thread URLs from this runtime — I can't fetch that link."

Runtime exposes `mcp__slack__conversations_replies`. Agent defaulted to "I can't fetch external URLs" without checking the runtime's tool list.

## The class-level pattern

**Verify-before-claim.** Three different "external state" categories (local file system, GitHub fork state, Slack thread state) all failed the same way: the agent filled the gap from training-data memory instead of running the verification command. Same drift class, three different surfaces.

## Prevention (verbatim from the anti-pattern card)

```bash
# Upstream / fork repo state
gh api repos/<owner>/<repo>/languages | jq '. | to_entries | map({lang: .key, bytes: .value})'

# Local path
ls -d <path> 2>&1

# Slack thread
mcp__slack__conversations_replies channel_id=<C> thread_ts=<ts> limit=20
```

If a tool isn't exposed in the current runtime, say so explicitly with the blocker rather than guessing.

## Skillify shape (cross-reference, not standalone)

Existing umbrella: `~/.hermes/skills/agent-agent-mistakes/SKILL.md` (Garry Tan mistake-memory framework, previously prod-only — staging copy added in this same turn).

New anti-pattern card: `~/.hermes/skills/agent-agent-mistakes/references/2026-06-25-verify-before-upstream-claim.md`.

Umbrella step 4 patched to add the verify-before-claim gate as a session-init pre-action check.

## Cross-references

- **Memory file:** `~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-25_verify-before-upstream-claim.md`
- **Roadmap entry:** `~/roadmap/learnings-2026-06.md` — 2026-06-25 section
- **Bead:** `jleechan-yi32` (CLOSED, 2026-06-25)
- **PR:** pending on `jleechanorg/jleechanclaw` from `feature/agent-agent-mistakes-verify-upstream`
- **Companion drift classes:** `~/.hermes/skills/skillify/SKILL.md` → "Claiming DONE Without Re-Running The Test Suite" + "Claiming DONE For Staging AND Prod Without `ls`-Verifying Both"
- **Related skill:** `root-cause-first`