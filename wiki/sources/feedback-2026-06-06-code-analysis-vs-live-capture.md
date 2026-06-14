---
title: "Code analysis vs live capture for root cause"
type: source
tags: [code-analysis, live-capture, root-cause, god-mode, level-12, worldarchitect-ai]
date: 2026-06-06
source_file: raw/feedback_2026-06-06_code_analysis_vs_live_capture.md
---

## Summary
Code-path analysis for the god-mode level-12 regression (PR #7268, bead rev-1fa0i) produced a plausible but WRONG root cause: SchemaRejectionError raised on forbidden rewards_box keys at narrative_response_schema.py:2753-2769 → re-raised → caught at world_logic.py:7223-7231 as 422 before god-mode authorized merge. Actual root cause (bead rev-o98fl, live s9 preview capture): model behaved correctly — emitted state_updates.player_character_data.level=12 with NO forbidden rewards_box keys. Backend merge DID apply level 12. Then validate_and_correct_state() ran WITHOUT agent_mode context and clamped level back to XP-implied 10 (XP=70500). The 422 path was never triggered.

## Key Claims
- For any root cause where hypothesis depends on 'the model must have emitted X' — do NOT finalize without actual raw LLM response payload showing X
- Mark analysis as PENDING-LIVE-CAPTURE until confirmed. Code-path reasoning is hypothesis, not proof
- Fix verified in PR #7268 commits 4f9df6d71d (God Mode validate_and_correct_state bypass) + 821534dee0 (harness hash)
- SchemaRejectionError path (rev-mwno1) remains a valid separate issue but was not the cause of this specific symptom

## Connections
- [[project_2026-06-08_mppfHseT_finish_commit_real_bugs]]
- [[RootCauseFirst]]
- [[LiveCaptureDiscipline]]
