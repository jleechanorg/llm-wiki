---
title: "Semantic Classifier Analysis - Faction Tool Invocation Gap"
type: source
tags: [faction-minigame, semantic-classifier, tool-invocation, gemini-api, investigation]
sources: [worldarchitect.ai-docs-faction_investigation_findings.md-ae81a08e, worldarchitect.ai-docs-faction_iteration_021_final_results.md-b0d2e8fd]
date: 2026-01-15
source_file: Semantic Classifier Analysis - Faction Tool Invocation Gap
last_updated: 2026-04-07
---

## Summary
Analysis of the 28% tool invocation rate vs iteration_011's 56% baseline despite matching configuration. The semantic classifier may be routing faction queries to wrong agent, with test inputs that SHOULD trigger tools not consistently doing so.

## Key Claims
- **Issue:** Tool invocation at 28% vs 56% baseline despite matching configuration
- **Hypothesis:** Semantic classifier routing faction queries to wrong agent
- **Inconsistent Matching:** Even inputs matching faction phrases don't always trigger tools
- **Problem Examples:** Turn 2 ("How many troops...") matches but no tools, Turn 6 ("build farms") matches but no tools
- **Working Examples:** Turn 7 ("recruit more men") and Turn 10 ("gather intelligence") correctly trigger tools

## Key Quotes
> "The semantic classifier may be: Not matching consistently, Similarity threshold too high (0.65), Fallback not working, Agent selected but tools not passed to API"

## Matching Analysis

**Test inputs that SHOULD match but DON'T consistently:**
| Turn | Input | Should Match | Actually Matches? |
|------|-------|---------------|-------------------|
| 2 | "How many troops do I have?" | "how many troops do i have?" | ✅ Yes, but NO tools |
| 6 | "build some farms" | "build farms" | ✅ Yes, but NO tools |
| 11 | "gather information about Iron Legion" | "faction intel" | ✅ Yes, but NO tools |

**Current MODE_FACTION phrases:**
```python
constants.MODE_FACTION: [
    "manage my faction", "faction management", "strategic faction system",
    "activate faction minigame", "show faction status", "check faction power",
    "what's my faction ranking?", "build farms", "recruit soldiers",
    "faction operations", "faction intel", "faction battle",
    "faction territory", "how many troops do i have?", "faction suggestions"
]
```

## Investigation Steps

1. **Check Similarity Scores** — What scores are test inputs getting? Above/below 0.65 threshold?
2. **Verify Fallback Logic** — Is Priority 7 fallback reaching `FactionManagementAgent.matches_game_state()`?
3. **Check Agent Selection Logs** — Are logs in server file instead of test output?
4. **Verify Tool Availability** — When agent selected, are tools passed to API via `agent.get_tools()`?

## Recommendations

**Short-term:**
- Add more faction phrases to semantic classifier
- Lower similarity threshold from 0.65 to 0.55-0.60
- Verify fallback logic is working

**Long-term:**
- Bypass semantic classifier when `faction_minigame.enabled=True`
- Force FactionManagementAgent when minigame enabled (Priority 1 check)
- Improve phrase matching with more diverse phrases

## Files to Review
- `mvp_site/intent_classifier.py` — Semantic classifier logic
- `mvp_site/agents.py` — Agent selection (Priority 7 fallback)
- Test inputs: `testing_mcp/faction/test_faction_20_turns_e2e.py` TURN_ACTIONS

## Connections
- [[Faction Tool Invocation - Next Steps Summary]] — Related investigation
- [[Next Steps After 40% Tool Invocation Achievement]] — Prior analysis
- [[LLM Game State Accuracy Analysis - Iteration 021]] — Related tool integration issues

## Contradictions
- None identified — this analysis is consistent with prior investigation findings