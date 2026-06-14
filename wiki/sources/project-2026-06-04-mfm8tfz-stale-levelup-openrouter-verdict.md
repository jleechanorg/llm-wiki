---
title: "MfM8TFz Stuck LevelUpAgent — Stale Flag Root Cause + PR #7262 VERIFIED"
type: source
tags: ["levelup", "stuck-agent", "worldarchitect-ai", "pr-7262", "openrouter", "gemini-3"]
date: 2026-06-04
source_file: project_2026-06-04_mfm8tfz_stale_levelup_openrouter_verdict.md
---

## Summary
Twin-clone repro gave HIGH-confidence verdict: stale top-level `level_up_pending=True` with no actionable transition. PROVIDER CORRECTION: production is GEMINI 3, not OpenRouter (local-env fidelity bug). PR #7262 arbiter twin replay FORCED to Gemini 3 = VERDICT PASS.

## Key Claims
- State: level 8 Sylphina, XP 36870–41820 / 48000 (NOT eligible for L9), level_up_pending=True, _agent_selection_tracker.count 13→14→15
- PROVIDER CORRECTION: production is GEMINI 3, not OpenRouter. The repro logs' OpenRouter line was LOCAL-ENV FIDELITY BUG (twin campaign under test account saw stored-but-disabled OpenRouter key)
- Bucket A refuted (Gemini PROHIBITED_CONTENT not the cause — wrong provider, wrong signature)
- Bucket B refuted (#7251 level-20 cap doesn't apply at L8)
- Bucket C refuted (#7261 XP canonicalization: replay looped identically)
- Root cause: stale flag with `is_level_up_active()=False` — router locks MODAL_LOCK on raw flag, never reaches stale-clear guard
- Evidence: `/tmp/worldarchitect.ai/repro-MfM8TFz/` bundle, branch `fix/stale-top-level-levelup-pending` @ `4d83bc0e20`

## Key Quotes
> Provider-independent root cause held: the gate is upstream of the LLM call. NEVER trust repro PROVIDER_SELECTION_FINAL as production provider — verify the live account/campaign Firestore doc

## Connections
- [[LevelUpStuck]] — concept
- [[PR7262]] — fix PR
