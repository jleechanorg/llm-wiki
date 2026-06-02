# level_up_available Schema Ban

**Ingested**: 2026-06-02  
**Source**: Claude memory feedback_2026-06-02_level_up_available_schema_banned.md  
**Bead**: rev-1pmyg (closed)  
**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/7221  

## Summary

`level_up_available` must never appear in the LLM narrative response schema (`provider_utils.py NARRATIVE_RESPONSE_SCHEMA`). It is a backend-derived field set by `rewards_engine.ensure_rewards_box()`. Adding it to the schema makes the LLM echo it, and the backend trusting that echo is a circular dependency.

**ZFC-correct alternative**: `level_up_signal.target_level > level_up_signal.current_level` (model computes these). Secondary backend check: `rewards_box.new_level > player_character_data.level`.

## History

- Removed: commit `cf0f21da43` (2026-05-04)  
- Re-added accidentally: PR #7221 initial revision  
- Re-removed: commit `20372341` (2026-06-02)  
