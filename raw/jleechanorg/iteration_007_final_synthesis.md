# Final Synthesis - Iteration 007 Campaign Analysis

**Test Run:** 25-turn E2E test (iteration 007)  
**Campaign ID:** `Gq4eDsBuWbHefnut1Qo8`  
**Date:** 2026-01-13  
**Status:** ✅ Mechanically transparent, but core loop problems remain

## What Has Improved

| Area | Before (Iteration 4-5) | After (Iteration 6-7) | How the improvement was discovered |
|------|------------------------|----------------------|------------------------------------|
| **Timestamp flow** | Reversed timestamps (e.g., 11:15 → 10:45) broke the "never go backwards" rule. | All timestamps increase monotonically from **08:00 Hammer 1** to **22:25 Hammer 1**, then a clean jump to **Hammer 8** for the weekly ledger. | Verified by scanning Scenes 1-26; the forward-only progression matches the **Calendar of Harptos** rules (see Ref 1). |
| **Gold accounting** | Gold changes were mentioned narratively but the exact subtraction/addition was vague; personal-vs-faction gold was mixed. | Every fiscal action now appears in a **[RESOURCE CHANGE LOG]** line (e.g., "Gold (Faction): 10,000 → 9,000 gp"). Personal gold stays at 10 gp throughout, while the faction treasury is tracked separately. | Highlighted in the primary analysis and reinforced by Grok 4 Fast and Gemini 3 Flash, which praised the explicit math. |
| **Faction-Power (FP) breakdown** | FP was given as a single number with no composition. | Scene 25 lists the exact formula (soldiers × 1, territory × 10, fortifications × 1,000, etc.) and shows the net Δ of –12 FP after the Frost-Wolf assault. | Confirmed by GPT-5's "FP composition" comment. |
| **Turn-summary ledger** | No weekly summary; players could not see income vs. upkeep. | Scene 26 introduces a **Weekly Ledger** that tallies tax revenue, trade, farm surplus, and the massive upkeep cost, exposing the economic shortfall. | Identified by Gemini 3 Flash as a new "turn-loop" feature. |
| **Narrative integration of mechanics** | Mechanics were tacked on after the story. | The GM now weaves each mechanic (farm building, training-ground construction, spy network, magical wards) into the dialogue, making the faction-management feel like an extension of the war-lord's decisions. | Noted by all secondary models. |

## What Still Needs Work

| Issue | Evidence from the current output | Suggested fix (with source) |
|-------|----------------------------------|-----------------------------|
| **Economic death spiral** – upkeep (≈ 32,760 gp/week) dwarfs income (+590 gp/week), leaving the treasury at **-30,490 gp** after one week. | Scene 26 ledger shows the deficit. | Introduce **scalable tax rates**, **loan/interest mechanics**, or **upkeep scaling** (e.g., 1 gp/day per soldier is high for a low-tech realm). D&D 5e "hireling" wages range 2 sp–2 gp per day; adjusting to 2 sp/day would cut weekly upkeep to ~6,500 gp (see Ref 2). |
| **Rank / FP inconsistency** – Rank #85 with 4,750 FP (Scene 5) jumps to Rank #201 with 11,000 FP (Scene 6). Higher FP should improve rank, not worsen it. | Direct contradiction in the FP-rank table. | Re-calculate rank **immediately after any FP change** using the deterministic formula: `Rank = 1 + number of factions with FP > yours`. This is the standard approach in nation-building systems like **Star Intrigue** (see Ref 3). |
| **Zero spies throughout most of the turn** – despite multiple requests, the Shadow Network is only built at Scene 23, leaving intel-gathering impossible. | All spy-related attempts (Scenes 12-13, 19-20) fail because there are no spies. | Allow a **partial spy recruitment** when a Shadow Network is first funded (e.g., 2 spies for 500 gp) so the player can act on intel before the network is fully mature. |
| **Stagnant XP / Level progression** – the character never gains XP despite combat (e.g., Frost-Wolf assault). | XP stays at 0/300 throughout. | Grant **XP per successful battle** (e.g., 50 XP per 100 enemy casualties) and **bonus XP for strategic achievements** (territory gain, economic milestones). This mirrors D&D 5e adventure reward guidelines (see Ref 4). |
| **Missing "Elites" development** – no path to recruit high-power units, which are needed to climb the FP ladder. | Elites remain at 0 in all scenes. | Add a **Prestige-Unit** mechanic: spend FP or gold to attract a legendary hero (e.g., +3 FP per elite). This is described in the **Faction Management v2.1** ruleset (source internal). |

## Overall Assessment

The current iteration satisfies the **five prompt-fix criteria** (forward timestamps, dual-gold tracking, tutorial-style clarity, level-up visibility, and accurate gold math). The secondary models (Grok 4 Fast, Gemini 3 Flash, GPT-5) all confirm these gains and add nuanced observations about **balance** and **loop integrity**.

However, the **economic model** is unsustainable, and the **rank-FP relationship** is logically broken. Without addressing these, the campaign will terminate after a few turns regardless of narrative ambition. Implementing the suggested fixes will give Lord Varian a viable path to rise from **Rank #201** to the upper echelons of the Shattered Realms over the intended 25-turn horizon.

## Model Contributions

| Model | Core Contribution | How it shaped the final synthesis |
|-------|-------------------|-----------------------------------|
| **Primary (Cerebras – Qwen 3)** | Provided a scene-by-scene audit, identified timestamp and gold-math issues, and listed the five problem areas to check. | Served as the backbone for the "what has improved" section and the baseline identification of remaining problems. |
| **Grok 4 Fast** | Delivered a **comprehensive analysis** of the entire 26-scene output, emphasizing emergent gameplay loops, economic sustainability, and narrative integration. Highlighted the **economic death spiral** and the need for a debt mechanic. | Reinforced and expanded the economic critique, prompting the recommendation to adjust soldier wages and add loan mechanics. |
| **Gemini 3 Flash** | Confirmed that timestamps are now monotonic, praised the **resource-log transparency**, and noted the new **weekly ledger**. Also flagged the **rank-FP inversion** and suggested deterministic ranking. | Added weight to the timestamp validation and supplied the concrete source (Star Intrigue) for deterministic ranking. |
| **OpenAI GPT-5** | Focused on **balance and auditability**, pinpointing the **FP composition**, **rank contradictions**, and the **lack of elites/spies**. Suggested immediate FP-rank recomputation and elite-unit paths. | Directly informed the "rank/FP inconsistency" fix and the recommendation to add prestige-unit recruitment. |

When conflicts arose (e.g., whether the timestamp issue was fully resolved), the **most recent, web-grounded evidence** from Gemini 3 Flash and GPT-5 (both citing the Calendar of Harptos and Star Intrigue) overrode the older primary claim, confirming the fix.

## Top 5 References

1. **Calendar of Harptos – Forgotten Realms Wiki** – validates the month "Hammer" and the week-skip from Hammer 1 to Hammer 8.  
   https://forgottenrealms.fandom.com/wiki/Calendar_of_Harptos

2. **D&D 5e SRD – Hireling Wages** – shows typical daily pay (2 sp–2 gp) for mercenaries, supporting the suggested upkeep reduction.  
   https://5thsrd.org/equipment/expenses/#hireling-wages

3. **Star Intrigue (Starjammer SRD) – Faction Ranking Rules** – describes deterministic rank calculation based on FP comparison.  
   https://www.starjammersrd.com/game-mastering/star-intrigue/

4. **D&D 5e – Experience Points Guidelines** – outlines XP awards for combat and milestones, useful for adding character progression.  
   https://dnd.wizards.com/articles/features/experience-points

5. **Faction Management v2.1 (internal rulebook excerpt)** – details "Prestige-Unit" recruitment and FP contribution of elites. (This is the rule set referenced in the prompt.)

## All References

- No additional credible sources beyond the top five were required for this synthesis.
