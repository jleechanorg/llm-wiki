---
title: "bd-qw6 skeptic catches warning-mode measured-section contradiction (2026-06-12)"
type: source
tags: [bd-qw6, skeptic, gate-4, bugbot, warning-mode, measured-section, daily-gemini, pr7315, real-bug, tdd]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_bd_qw6_measured_section_warning.md
---

## Summary
skeptic-self-verify reported `VERDICT: PASS` (all 8 gates) and Bugbot on the prior head was clean, but a second skeptic agent (bd-qw6, posted as `VERDICT: FAIL` by `github-actions[bot]`) flagged a real contradiction in PR #7315: `scripts/daily_gemini_cost_report.py:1682` appended `_format_measured_section(...)` to `report["report_text"]` unconditionally after `build_report()` had already returned a warning-only body for `send_mode == "warning"` at line 1240 — the warning email could say spend is not being reported, then immediately include per-campaign `attributed=$12.3400` lines.

## Key Claims
- skeptic-self-verify is the official Green Gate signal, but bd-qw6 is a deeper second pass; the two can disagree on the same head
- Treat any bd-qw6 FAIL as a real blocker to investigate, not as noise
- RED test: stub `load_cost_summary` to return `target_day_complete=None` (forces `send_mode=warning`); stub `load_measured_split` to return per-campaign cost rows; assert `report_text` contains "Spend is NOT being reported" AND does NOT contain "MEASURED (per-campaign, post-join)" / "campaign-A" / "day_gemini_cost" / "apportioned_usd"
- GREEN fix: in `main()`, gate the measured section (and the `orphan_lifecycle` bookkeeping lines) on `send_decision["send_mode"] != "warning"`; the `measured` dict is still exposed in the JSON payload for programmatic consumers; only the report body is suppressed

## Key Quotes
> "skeptic-self-verify is the official Green Gate signal, but bd-qw6 (and the AO lifecycle-manager it appears to be driven by) is a deeper, second pass. The two can disagree on the same head: skeptic-self-verify can PASS while bd-qw6 posts VERDICT: FAIL with a specific bug."

> "When skeptic-self-verify PASSes but bd-qw6 FAILs on the same head, the bd-qw6 issue is real — fix it, then re-trigger skeptic-self-verify (and confirm bd-qw6 re-evaluates to PASS on the new head)."

## Connections
- [[BdQw6Skeptic]] — deeper second-pass skeptic
- [[GreenGateSkepticVsBugbot]] — skeptic vs Bugbot conflict pattern
- [[WarningModeMeasuredSection]] — gated report body pattern
- [[DailyGeminiCostReport]] — PR #7315 reference
- [[TDDRedGreenFix]] — RED test for send_mode=warning path
