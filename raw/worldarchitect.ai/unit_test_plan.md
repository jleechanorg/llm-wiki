# Unit Test Plan for Faction Minigame + CampaignUpgradeAgent PR

**Goal:** Increase coverage from 17% to 60%+ by adding unit tests for new code

**Current Status:**
- Coverage: 17% (below 60% threshold)
- PR Size: 310 files changed, 50,476 insertions
- Existing Tests: CampaignUpgradeAgent has tests, FactionManagementAgent has partial tests

---

## Priority 1: Critical New Code (High Impact on Coverage)

### 1. Campaign Tier Prompt Loading (`mvp_site/agents.py:531-549`)
**File:** `mvp_site/tests/test_agents.py`  
**Test Class:** `TestBaseAgentCampaignTierPrompts`

**Tests Needed:**
- ✅ `test_base_agent_loads_divine_prompt_when_tier_divine` - Verify Divine Leverage prompt loads when `campaign_tier == CAMPAIGN_TIER_DIVINE`
- ✅ `test_base_agent_loads_sovereign_prompt_when_tier_sovereign` - Verify Sovereign Protocol prompt loads when `campaign_tier == CAMPAIGN_TIER_SOVEREIGN`
- ✅ `test_base_agent_no_tier_prompt_when_tier_normal` - Verify no tier prompt loads for normal campaigns
- ✅ `test_base_agent_no_tier_prompt_when_game_state_none` - Verify no tier prompt loads when `game_state is None`
- ✅ `test_base_agent_handles_missing_divine_prompt_gracefully` - Verify warning logged when divine prompt file missing
- ✅ `test_base_agent_handles_missing_sovereign_prompt_gracefully` - Verify warning logged when sovereign prompt file missing

**Estimated Coverage Impact:** +2-3% (affects all agents via BaseAgent)

---

### 2. PayloadTooLargeError Handling (`mvp_site/world_logic.py:2256-2261, 2643-2648`)
**File:** `mvp_site/tests/test_world_logic.py`  
**Test Class:** `TestPayloadTooLargeErrorHandling`

**Tests Needed:**
- ✅ `test_create_campaign_handles_payload_too_large_error` - Verify 422 response with user-friendly message when PayloadTooLargeError during campaign creation
- ✅ `test_process_action_handles_payload_too_large_error` - Verify 422 response with user-friendly message when PayloadTooLargeError during story continuation
- ✅ `test_payload_too_large_error_logs_correctly` - Verify error is logged with context
- ✅ `test_payload_too_large_error_status_code_422` - Verify status code is 422 (not 500)

**Estimated Coverage Impact:** +1-2%

---

### 3. User Input Type Validation (`mvp_site/world_logic.py:2501-2502`)
**File:** `mvp_site/tests/test_world_logic.py`  
**Test Class:** `TestUserInputValidation`

**Tests Needed:**
- ✅ `test_process_action_rejects_non_string_user_input` - Verify 400 error when `user_input` is not a string (e.g., list, dict)
- ✅ `test_process_action_accepts_string_user_input` - Verify string input passes validation
- ✅ `test_process_action_handles_none_user_input` - Verify None input returns "User input is required" (existing check)
- ✅ `test_process_action_handles_empty_string_user_input` - Verify empty string is accepted (may be valid)

**Estimated Coverage Impact:** +1%

---

### 4. Scene Generated Fix (`mvp_site/world_logic.py:238`)
**File:** `mvp_site/tests/test_world_logic.py`  
**Test Class:** `TestAnnotateEntry`

**Tests Needed:**
- ✅ `test_annotate_entry_sets_scene_generated_independently` - Verify `scene_generated` is set even when `turn_generated` already exists
- ✅ `test_annotate_entry_sets_both_when_missing` - Verify both `turn_generated` and `scene_generated` are set when missing
- ✅ `test_annotate_entry_preserves_existing_turn_generated` - Verify existing `turn_generated` is not overwritten
- ✅ `test_annotate_entry_handles_legacy_entries` - Verify legacy entries with only `turn_generated` get `scene_generated` added

**Estimated Coverage Impact:** +0.5%

---

## Priority 2: Faction Management Agent (Expand Existing Tests)

### 5. FactionManagementAgent.matches_input() (`mvp_site/agents.py:1754-1811`)
**File:** `mvp_site/tests/test_agents.py`  
**Test Class:** `TestFactionManagementAgentMatchesInput` (NEW)

**Tests Needed:**
- ✅ `test_matches_input_returns_true_for_minigame_patterns` - Verify `FACTION_MINIGAME_PATTERNS` trigger even when disabled
- ✅ `test_matches_input_requires_enabled_for_query_patterns` - Verify `FACTION_QUERY_PATTERNS` require `enabled=True`
- ✅ `test_matches_input_returns_false_when_disabled_and_no_minigame_pattern` - Verify returns False when disabled and no minigame pattern
- ✅ `test_matches_input_case_insensitive` - Verify pattern matching is case-insensitive
- ✅ `test_matches_input_handles_none_game_state` - Verify handles None game_state gracefully

**Estimated Coverage Impact:** +1-2%

---

### 6. FactionManagementAgent.build_system_instructions() (`mvp_site/agents.py:1615-1677`)
**File:** `mvp_site/tests/test_agents.py`  
**Test Class:** `TestFactionManagementAgentBuildInstructions` (NEW)

**Tests Needed:**
- ✅ `test_build_instructions_includes_minigame_prompt_when_enabled` - Verify faction minigame prompt included when `enabled=True`
- ✅ `test_build_instructions_excludes_minigame_prompt_when_disabled` - Verify faction minigame prompt excluded when `enabled=False`
- ✅ `test_build_instructions_includes_required_prompts` - Verify all required prompts are included
- ✅ `test_build_instructions_prompt_order` - Verify prompts are in correct order

**Estimated Coverage Impact:** +1%

---

## Priority 3: Faction Tools and Calculations

### 7. Faction Power Calculation (`mvp_site/faction/combat.py:calculate_faction_power`)
**File:** `mvp_site/tests/test_faction_combat.py` (NEW)

**Tests Needed:**
- ✅ `test_calculate_faction_power_territory_multiplier` - Verify territory FP = territory * 5 (not * 10)
- ✅ `test_calculate_faction_power_soldiers` - Verify soldiers contribute 1x FP each
- ✅ `test_calculate_faction_power_spies` - Verify spies contribute 0.5x FP each
- ✅ `test_calculate_faction_power_elites` - Verify elites contribute 3x FP each
- ✅ `test_calculate_faction_power_total_calculation` - Verify total FP calculation is correct
- ✅ `test_calculate_faction_power_handles_missing_units` - Verify handles missing unit types gracefully
- ✅ `test_calculate_faction_power_handles_zero_values` - Verify handles zero territory/units correctly

**Estimated Coverage Impact:** +2-3%

---

### 8. Faction Ranking Calculation (`mvp_site/faction/rankings.py`)
**File:** `mvp_site/tests/test_faction_rankings.py` (NEW)

**Tests Needed:**
- ✅ `test_calculate_total_fp_territory_multiplier` - Verify docstring matches code (territory * 5)
- ✅ `test_calculate_ranking_returns_correct_rank` - Verify ranking calculation is correct
- ✅ `test_calculate_ranking_handles_edge_cases` - Verify handles edge cases (rank 1, last rank, ties)
- ✅ `test_calculate_ranking_with_ai_factions` - Verify ranking includes AI factions correctly

**Estimated Coverage Impact:** +1-2%

---

### 9. Faction Tools (`mvp_site/faction/tools.py`)
**File:** `mvp_site/tests/test_faction_tools.py` (NEW)

**Tests Needed:**
- ✅ `test_faction_calculate_power_tool_schema` - Verify tool schema is correct
- ✅ `test_faction_calculate_ranking_tool_schema` - Verify tool schema is correct
- ✅ `test_faction_tools_are_in_faction_tools_list` - Verify tools are exported correctly
- ✅ `test_faction_tools_call_correct_functions` - Verify tool calls map to correct functions

**Estimated Coverage Impact:** +1%

---

## Priority 4: Agent Routing Logic

### 10. get_agent_for_input() CampaignUpgradeAgent Routing (`mvp_site/agents.py:1975-1977, 2069-2080, 2121-2127`)
**File:** `mvp_site/tests/test_agents.py`  
**Test Class:** `TestGetAgentForInputCampaignUpgrade` (NEW)

**Tests Needed:**
- ✅ `test_get_agent_campaign_upgrade_state_based` - Verify CampaignUpgradeAgent selected when upgrade available (priority 3)
- ✅ `test_get_agent_campaign_upgrade_semantic_intent` - Verify CampaignUpgradeAgent selected via semantic classifier
- ✅ `test_get_agent_campaign_upgrade_api_explicit_mode` - Verify CampaignUpgradeAgent selected via `mode="campaign_upgrade"`
- ✅ `test_get_agent_campaign_upgrade_priority_over_character_creation` - Verify CampaignUpgradeAgent takes precedence over CharacterCreationAgent

**Estimated Coverage Impact:** +1-2%

---

### 11. get_agent_for_input() FactionManagementAgent Routing (`mvp_site/agents.py:1984-1989, 2057-2067, 2102-2120`)
**File:** `mvp_site/tests/test_agents.py`  
**Test Class:** `TestGetAgentForInputFaction` (NEW)

**Tests Needed:**
- ✅ `test_get_agent_faction_state_based_priority_5` - Verify FactionManagementAgent selected when enabled (priority 5)
- ✅ `test_get_agent_faction_semantic_intent` - Verify FactionManagementAgent selected via semantic classifier
- ✅ `test_get_agent_faction_api_explicit_mode` - Verify FactionManagementAgent selected via `mode="faction"`
- ✅ `test_get_agent_faction_input_pattern_fallback` - Verify FactionManagementAgent selected via input patterns (priority 9)
- ✅ `test_get_agent_faction_priority_after_character_creation` - Verify FactionManagementAgent doesn't interrupt character creation

**Estimated Coverage Impact:** +1-2%

---

## Priority 5: Edge Cases and Error Handling

### 12. Gemini Provider Tool Result Mismatch (`mvp_site/llm_providers/gemini_provider.py:568-573`)
**File:** `mvp_site/tests/test_gemini_provider.py`  
**Test Class:** `TestGeminiNativeToolLoop` (NEW)

**Tests Needed:**
- ✅ `test_tool_result_mismatch_logs_warning` - Verify warning logged when `len(tool_results) != len(tool_requests)`
- ✅ `test_tool_result_mismatch_builds_from_results_only` - Verify function responses built from tool_results only when mismatch

**Estimated Coverage Impact:** +0.5%

---

## Implementation Strategy

### Phase 1: Quick Wins (Priority 1)
**Estimated Time:** 2-3 hours  
**Coverage Gain:** +5-7%

1. Campaign tier prompt loading tests (6 tests)
2. PayloadTooLargeError handling tests (4 tests)
3. User input validation tests (4 tests)
4. Scene generated fix tests (4 tests)

**Total:** ~18 tests

---

### Phase 2: Agent Tests (Priority 2, 4)
**Estimated Time:** 3-4 hours  
**Coverage Gain:** +4-6%

1. FactionManagementAgent.matches_input() tests (5 tests)
2. FactionManagementAgent.build_system_instructions() tests (4 tests)
3. CampaignUpgradeAgent routing tests (4 tests)
4. FactionManagementAgent routing tests (5 tests)

**Total:** ~18 tests

---

### Phase 3: Faction Core Logic (Priority 3)
**Estimated Time:** 4-5 hours  
**Coverage Gain:** +4-6%

1. Faction power calculation tests (7 tests)
2. Faction ranking calculation tests (4 tests)
3. Faction tools tests (4 tests)

**Total:** ~15 tests

---

### Phase 4: Edge Cases (Priority 5)
**Estimated Time:** 1-2 hours  
**Coverage Gain:** +0.5%

1. Gemini provider tool mismatch tests (2 tests)

**Total:** ~2 tests

---

## Total Estimated Impact

**Total Tests:** ~53 tests  
**Total Time:** 10-14 hours  
**Estimated Coverage Gain:** +13.5-19.5%  
**New Coverage:** ~30-36% (from 17%)

**Note:** This may not reach 60% immediately, but will significantly improve coverage and establish patterns for future tests.

---

## Test File Structure

```
mvp_site/tests/
├── test_agents.py (expand existing)
│   ├── TestBaseAgentCampaignTierPrompts (NEW)
│   ├── TestFactionManagementAgentMatchesInput (NEW)
│   ├── TestFactionManagementAgentBuildInstructions (NEW)
│   ├── TestGetAgentForInputCampaignUpgrade (NEW)
│   └── TestGetAgentForInputFaction (NEW)
├── test_world_logic.py (expand existing)
│   ├── TestPayloadTooLargeErrorHandling (NEW)
│   ├── TestUserInputValidation (NEW)
│   └── TestAnnotateEntry (expand existing)
├── test_faction_combat.py (NEW)
│   └── TestFactionPowerCalculation
├── test_faction_rankings.py (NEW)
│   └── TestFactionRankingCalculation
├── test_faction_tools.py (NEW)
│   └── TestFactionTools
└── test_gemini_provider.py (expand existing)
    └── TestGeminiNativeToolLoop (NEW)
```

---

## Success Criteria

- ✅ All Priority 1 tests implemented
- ✅ Coverage increases from 17% to 30%+
- ✅ All new code paths have at least basic test coverage
- ✅ Tests follow existing patterns in `test_agents.py`
- ✅ Tests use proper mocking (no external dependencies)
- ✅ Tests run in < 5 seconds total

---

## Next Steps

1. Start with Phase 1 (Quick Wins) - highest ROI
2. Run coverage after Phase 1 to measure impact
3. Adjust plan based on actual coverage gains
4. Continue with Phase 2-4 as needed
