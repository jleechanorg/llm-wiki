---
title: "BLOCKED requires a failed probe, not an inferred constraint — 2026-07-25"
type: source
tags: [agent-behavior, anti-pattern, verification, blocked-state, bigquery, caching]
date: 2026-07-25
source_file: raw/feedback_2026-07-25_probe_the_blocker_before_declaring_blocked.md
---

## Summary

An agent marked a P0 bead (`rev-2gxkp`, "God Mode gets ZERO Gemini cache hits")
as BLOCKED-ON-HUMAN, citing "needs compute this session cannot obtain." The bead's
acceptance criterion was a read of BigQuery rows that production had already
written — four cheap commands, zero LLM spend. The compute blocker was genuinely
real for a **sibling** task on the same bead (a long-campaign replay needing a
local server + real LLM turns) and was inherited by the measurement task without
ever being probed for it. When finally run, the measurement **inverted the bead's
premise**: God Mode was caching on 64% of turns, not zero.

## Key Claims

- BLOCKED is a **terminal** state. A false BLOCKED costs more than a false
  "let me try", because nobody re-examines a handed-back item.
- A blocker inherited from a sibling task, a prior attempt, or a dead delegate is
  a **hypothesis until probed** — its scope must be tested, not assumed.
- Distinguish **needs-AUTHORITY** (rotate a credential at a console, approve a
  force-push, change user-owned config) from **needs-EFFORT**. Only authority is
  genuinely blocked for an agent.
- The measurement that was declared blocked showed `GodModeAgent` with
  `cached_tokens > 0` on 50 of 78 turns (64%, avg 105,929 cached), with consecutive
  turns 15→19 in one campaign all at ~188,365 cached against ~340,000 prompt tokens.
- Consequence of the near-miss: a P0 would have stayed open on a refuted premise,
  and a PR was on track to merge citing that premise.

## Key Quotes

> "authorize execution of the acceptance measurement, which needs compute this
> session cannot obtain" — the BLOCKED reason that was wrong

> "If you cannot name the command that proved it blocked, you have not proved it
> blocked." — the resulting rule

## Probe Checklist

| Claimed blocker | Cheapest falsifying probe |
|---|---|
| needs compute / quota | is there a path reading **already-existing** data? (`bq`, `gh api`, logs, on-disk artifacts) |
| needs a service | is the credential present, and does a one-line call return 200? |
| needs the human | is it authority, or merely effort? |

## Connections

- [[EvidenceStandards]] — same family as "verify before reporting"; this is its
  terminal-state variant
- [[IroncladExitCriteria]] — covers the *inverse* error: grinding against a
  blocker that is genuinely real
- [[GeminiImplicitCaching]] — the domain where the refuted premise lived; prefix
  caching is a cliff, not a slope
- [[BigQueryForensics]] — `worldarchitecture-ai.llm_forensics.llm_payloads` was
  the already-written data source that made the "blocker" false
- [[WorldArchitectAI]] — project context
