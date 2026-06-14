---
name: code-analysis-vs-live-capture-root-cause
description: Code-path analysis without live payload capture can produce plausible but wrong root causes — always anchor to real wire evidence before filing a root cause
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5c0b4513-a902-4aeb-9807-954138687f1a
---

Code-path analysis for the god-mode level-12 regression (PR #7268, bead rev-1fa0i) produced a
plausible but WRONG root cause:

**My analysis said:** `narrative_response_schema.py:2753-2769` SchemaRejectionError raised on
forbidden `rewards_box` keys → re-raised → caught at `world_logic.py:7223-7231` as 422 before
god-mode authorized merge. The model must have emitted `rewards_box.level_up_available`.

**Actual root cause (bead rev-o98fl, live s9 preview capture):** The model behaved correctly —
emitted `state_updates.player_character_data.level=12` with NO forbidden `rewards_box` keys.
The backend merge DID apply level 12. Then `validate_and_correct_state()` ran WITHOUT
`agent_mode` context and clamped level back to XP-implied 10 (XP=70500). The 422 path was
never triggered.

**Why:** I was doing pure code-path tracing without the actual HTTP response body. A plausible
execution path (SchemaRejectionError → 422) does not mean the model actually triggered it.

**How to apply:** For any root cause where the hypothesis depends on "the model must have
emitted X" — do NOT finalize the root cause without the actual raw LLM response payload showing
X. Mark the analysis as PENDING-LIVE-CAPTURE until confirmed. Code-path reasoning is a
hypothesis, not proof.

**Corrective action:** Added correction comment to rev-1fa0i bead. Fix verified in PR #7268
commits 4f9df6d71d (God Mode validate_and_correct_state bypass) + 821534dee0 (harness hash).
The SchemaRejectionError path (rev-mwno1) remains a valid separate issue but was not the cause
of this specific symptom.
