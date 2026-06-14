---
name: canonical-level-up-target-lives-in-result-rewards-box-not-the-stream-done-payload-2026-06-04
description: "When asserting level-up target_level in testing_mcp, fetch persisted rewards_box via post-turn get_campaign_state — the streaming done payload often returns rewards_box {} and omits level_up_signal"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 15c06163-394b-4d82-97e5-d551f8fa1350
---

A no-cap GREEN validation FAILED (`target_level: None`, NO_SIGNAL) purely as a **test-extraction bug**, not a prompt-fix failure. The test read `level_up_signal.target_level` and `resp.get("rewards_box")` from the streaming `done` payload — which returned `{}` / omitted the signal — while the model's real output (`current_level=20, new_level=141, resolved_target_level=141, level_up_available=true, source="model"`) was persisted at **`result.rewards_box`**, a sibling of `game_state` at the campaign-state result top level.

**Fix pattern (works):** after the streaming turn, fetch `post = ctx.get_campaign_state(campaign_id)` and read `post["rewards_box"]`; extract target via `resolved_target_level` then `new_level`. Fall back chain: `level_up_signal.target_level` (if dict) → turn `rewards_box` → **persisted `rewards_box`**. Use `level_up_available` OR'd across turn box and persisted box.

**Why:** canonical level-up evidence = the `rewards_box` availability layer (5 fields: current_level, new_level, resolved_target_level, level_up_available, source). The streaming `done` payload is NOT a reliable carrier of it; `get_campaign_state` is authoritative.

**How to apply:** any testing_mcp assertion on level-up target/availability must read persisted `rewards_box` post-turn, never trust only the inline stream payload or `level_up_signal`. `source:"model"` distinguishes LLM-emitted from backend-synthesized. See [[project_2026-06-04_pr7251_nocap_levelup_stuck_root_cause]].
