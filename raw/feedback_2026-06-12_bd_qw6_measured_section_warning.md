---
name: feedback-2026-06-12-bd-qw6-measured-section-warning
description: bd-qw6 skeptic catches warning-mode email contradictions in daily Gemini cost report (PR #7315)
metadata:
  type: feedback
---

# bd-qw6 skeptic (separate from skeptic-self-verify) catches real bugs that Gate-4 Bugbot can miss

**Date**: 2026-06-12
**Context**: PR #7315 (`fix/daily-gemini-wait-for-export`)
**Affected file**: `scripts/daily_gemini_cost_report.py:1682`

## Symptom

skeptic-self-verify reported `VERDICT: PASS` (all 8 gates), and Bugbot on the prior head `64267c123` was also clean. **However** a second skeptic agent (bd-qw6, posted as `VERDICT: FAIL` by `github-actions[bot]`) flagged:

> `scripts/daily_gemini_cost_report.py:1682` appends `_format_measured_section(...)` to `report["report_text"]` unconditionally after `build_report()` has already returned a warning-only body for `send_mode == "warning"` at `scripts/daily_gemini_cost_report.py:1240`. That means the warning email can say spend is not being reported, then later include `day_gemini_cost`, `apportioned_usd`, and campaign attributed dollar lines.

This was a real contradiction: a warning email opened with "Spend is NOT being reported" and then immediately listed per-campaign `attributed=$12.3400` lines.

## TDD red→green fix

- **RED** test (new in `scripts/tests/test_daily_gemini_wait_state.py`):
  - `test_main_warning_mode_omits_measured_appendix`
  - Stubs `load_cost_summary` to return `target_day_complete=None` (forces `send_mode=warning` regardless of `attempt_count` per `_resolve_send_mode`)
  - Stubs `load_measured_split` to return `available=True, day_gemini_cost=12.34, campaign_rows=[{campaign_id=campaign-A, attributed_cost_usd=12.34}]`
  - Asserts `report_text` contains "Spend is NOT being reported" AND does NOT contain "MEASURED (per-campaign, post-join)" / "campaign-A" / "day_gemini_cost" / "apportioned_usd"
- **GREEN**: in `main()`, gate the measured section (and the `orphan_lifecycle` bookkeeping lines) on `send_decision["send_mode"] != "warning"`. The `measured` dict is still exposed in the JSON payload for programmatic consumers; only the report body is suppressed.

```python
if send_decision["send_mode"] == "warning":
    report["report_text"] = _build_warning_body(
        target_day, cost_now, send_decision["attempt_count"],
        send_decision["max_wait_days"],
        send_decision.get("first_seen_date"),
        send_decision.get("last_seen_date"),
    )
else:
    report["report_text"] += (
        "\n- orphan_lifecycle_start_iso: ..."
        "\n- orphan_lifecycle_end_iso: ..."
    )
```

## Why it matters

skeptic-self-verify is the official Green Gate signal, but bd-qw6 (and the AO lifecycle-manager it appears to be driven by) is a deeper, second pass. The two can disagree on the **same head**: skeptic-self-verify can PASS while bd-qw6 posts VERDICT: FAIL with a specific bug. Treat any bd-qw6 FAIL as a real blocker to investigate, not as noise.

When skeptic-self-verify PASSes but bd-qw6 FAILs on the same head, the bd-qw6 issue is real — fix it, then re-trigger skeptic-self-verify (and confirm bd-qw6 re-evaluates to PASS on the new head).

## Related

- [[project-2026-06-12-pr7315-bugbot-conditional-append]] — see also
- [[feedback-2026-06-12-skeptic-self-verify-bugbot-conflict]] — companion lesson
