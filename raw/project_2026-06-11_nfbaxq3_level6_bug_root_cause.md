---
name: nfbaxq3-level6-bug-root-cause
description: "Repro and root-cause for NFBaxQ3mIUe17UlAAGlE \"level 5 instead of 6\" bug — LLM prompt/schema defect, NOT backend override; PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2a383e2c-90a3-49e7-ba3a-2d3b68ec68b5
---

# NFBaxQ3mIUe17UlAAGlE Level 6 Bug — Root Cause

**Date:** 2026-06-11
**Campaign:** `NFBaxQ3mIUe17UlAAGlE` (owner uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`, "astarion post bg3", Astarion Lvl 5 Gloomstalker/Assassin/Whispers multiclass)
**URL:** `https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app/game/NFBaxQ3mIUe17UlAAGlE`
**Cloud Run revision:** `mvp-site-app-dev-03100-65q` (commit `ff979f9f9d`)

## User's hypothesis (REFUTED)
> "some backend logic is overriding god mode request to be level 6"

**Refuted.** The flow was NOT a god-mode turn. It was a normal CHARACTER-mode level-up where the player typed "level up to 6 right here" → modal → finish. The "god" label in user logs is a conversation-mode persona used AFTER the bug to debug, not a god-mode override.

## Actual root cause
**LLM prompt/schema defect, not backend override.** The LLM consistently emits:
- `rewards_box.new_level: 6` (correct)
- `rewards_box.resolved_target_level: 6` (correct)
- `level_up_signal: {current_level: 5, target_level: 6}` (correct)
- `state_updates.player_character_data.features.append: [Mantle of Whispers, Countercharm, Favored Enemy: Undead, Natural Explorer: Underdark]` (L6 features, correct)
- `state_updates.player_character_data.health: {hp: 56, hp_max: 56}` (L6 HP, correct)
- **`state_updates.player_character_data.level: 5`** ❌ (left at pre-L5 value)

Backend correctly persists what the LLM wrote. The LLM only fails to update `player_character_data.level` in the same `state_updates` block where it writes the L6 features and HP. Cloud Logging surfaces this as `SESSION_HEADER_LEVEL_MISMATCH: LLM-emitted session header displays level 6, but persisted level is 5`.

**Per ZFC, the fix is in the LLM prompt, NOT a backend clamp.** Adding a server-side "if rewards_box.new_level > current_level, override player_character_data.level" would mask the model defect and is forbidden without explicit human approval (per repo CLAUDE.md).

## Does PR #7434 fix it? — NO
PR #7434 (`fix/level-up-daily-cron-combined`) is a 3-PR stack (PR-A god-mode rewards_box persistence, PR-B modal turn revert, PR-C codex quota skip). The diff has **zero** literal `level = 6` / `"level": 6` / `override_level` writes in production code. PR-A only repairs the god-mode rewards_box writeback path; it does not change how `player_character_data.level` is mutated. The bug is in a different code path entirely.

## Smoking-gun entry IDs (cite in any follow-up)
- `3eFGBzXr0wpaQsNotSrb` — player typed `"level up to 6 right here"` in character mode
- `Mo319u4trhbNJUTVQCTK` — gemini opened L6 modal (rewards_box.new_level=6)
- `Omwtl3lOH5g0FmY25s96` — user selected "Level Up to Level 6"
- `Ee4kTAZuVRr8noj41qKE` — gemini modal mid-state (new_level=6)
- `kp0B7r7WgO0Rk4WW0KeC` — user "Apply Recommended Options and Return to Game"
- `o01IS7QHm3geEkzF7CF9` — gemini final state_update: L6 features written but `level: 5` ❌

## Repro recipe
```bash
# 1. User uid
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="mvp-site-app-dev" AND jsonPayload.campaign_id="NFBaxQ3mIUe17UlAAGlE"' \
  --project=worldarchitecture-ai --limit=5 --format=json \
  | jq -r '.[].jsonPayload.message' | grep -m1 user_id

# 2. Download entries
mcp__worldai__admin_download_campaign_entries \
  target_user_id=vnLp2G3m21PJL6kxcuAqmWSOtm73 \
  campaign_id=NFBaxQ3mIUe17UlAAGlE \
  from_timestamp=2026-06-10T22:00:00Z to_timestamp=2026-06-11T02:00:00Z \
  limit=20 format=jsonl reason="repro level-6 bug" ticket_id="..."

# 3. Compare rewards_box.new_level vs state_updates.player_character_data.level
```

## Suggested follow-up (out of scope for this PR)
1. Update the level-up agent's system prompt to **require** `state_updates.player_character_data.level` whenever `rewards_box.new_level` or `level_up_signal.target_level` is written. Cite entry `o01IS7QHm3geEkzF7CF9` as RED evidence.
2. Add a schema invariant (model side, not backend) that rejects responses where `new_level > current_level` but `player_character_data.level` is missing or `≤ current_level`.
3. Convert `SESSION_HEADER_LEVEL_MISMATCH` from a silent warning into a "rejection-and-retry" signal back to the model.

## Evidence bundle
`/tmp/worldarchitect.ai/level6-repro/entries.jsonl` (sha256 `fca3854ac5...`), 20-entry JSONL download with full LLM traces.

**Why:** The "god mode override" hypothesis caused the user to suspect PR #7434. The PR diff audit (Subagent 3) + LLM trace (Subagent 2) + code audit (Subagent 4) all converge: PR #7434 doesn't touch `level` writes, the LLM is the one failing to write `level: 6` to PCD, and per ZFC the fix belongs in the prompt not in backend enforcement.
**How to apply:** When this bug class resurfaces (LLM emits `rewards_box.new_level=N` but persists old `level`), do not propose a backend clamp. Update the level-up agent prompt and add a model-side schema rejection. PR #7434 (PR-A/PR-B/PR-C stack) is for a different bug class entirely.
**See also:** [[stale-level-up-complete-cleared-2to3]] (sibling 2→3 fix landed earlier same session).
