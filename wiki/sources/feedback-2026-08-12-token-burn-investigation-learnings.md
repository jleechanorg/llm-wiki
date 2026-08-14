---
title: "Token-Burn Investigation Anti-Patterns (2026-08-12)"
type: source
tags: [claude-code, billing, anti-pattern, validation, ccusage, minimax, max-plan, advice, watchdog, daemon]
date: 2026-08-12
source_file: raw/feedback_2026-08-12_token_burn_investigation_learnings.md
---

## Summary

Three wrong conclusions during a single token-burn investigation — (1) treating ccusage's theoretical cost column as actual billing, (2) assuming MiniMax = free because ccusage showed $0, (3) citing a file:line without grep -n verification. The third error was caught by `/advice` Reviewer A before it shipped. Meta-rule: dispatch `/advice` as a hard gate after two user pushbacks on the same investigation. **The dominant token source was the cmux-resume-watchdog with LLM fallback (94.8 MB / 6,505 JSONLs in 7 days)** — fix applied at `cmux_resume_watchdog.py:526`.

## Key Claims

- ccusage's `costUSD` column uses LiteLLM pricing, NOT the Anthropic billing API. Anthropic's docs state it "may differ from your actual bill."
- `~/.claude.json` `oauthAccount.hasExtraUsageEnabled: false` is the truth test for "is this user being billed per-token over Max?"
- "X tool shows Y model at $0" ≠ "Y model is free." Cost = 0 is a missing-data signal until proven otherwise.
- `~/.claude/.credentials.json` `subscriptionType` and `rateLimitTier` fields being null triggers Anthropic bug #32286 (CLI silently enters API billing mode even on Max).
- **DOMINANT TOKEN SOURCE:** cmux-resume-watchdog running `--daemon --interval 600` invoked `classify_with_llm()` per tick, spawning `codex exec` or `claude -p` as subprocess. Generated **6,505 JSONL files in 7 days (94.8 MB)**, dwarfing all user-driven sessions.
- **FIX APPLIED 2026-08-14:** `~/.claude/skills/cmux-resume-watchdog/scripts/cmux_resume_watchdog.py:526` — `llm_predict = None` always. Fastembed-only classification; ambiguous surfaces default to "clear" (no resume) instead of LLM subprocess.
- `/sidekick` teammate sending "available" without STATE.md Progress Log advance = idle, not done.

## Key Quotes

> "The investigator will next conclude that the right lever is `claudem` (MiniMax-M3) for all heavy investigation — but the actual third wrong conclusion waiting to happen is the assumption that `claudem` calls don't count against anything. MiniMax charges per-token too." — `/advice` Reviewer A (sonnet subagent), 2026-08-12

## Connections

- [[RouteClassifierClaudemVsMax]] — companion memory with verified routing facts
- [[CcusageTheoreticalCost]] — concept: ccusage cost column semantics
- [[MaxOAuthSubscription]] — concept: Claude Max flat-fee billing structure
- [[MiniMaxMeteredNotFree]] — concept: MiniMax API is pay-as-you-go
- [[AdviceGateAfterPushback]] — concept: when to dispatch `/advice`
- [[AnthropicBug32286]] — concept: silent API billing when credentials null
- [[CmuxResumeWatchdogLlmRemoval]] — concept: dominant token source identified and fixed
- [[WorkAttributionPattern]] — concept: JSONL → worktree → PR → commits mapping