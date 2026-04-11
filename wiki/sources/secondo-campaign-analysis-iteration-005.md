---
title: "Second Opinion: Campaign Coherence Analysis Iteration 005"
type: source
tags: [worldarchitect, campaign, coherence, second-opinion, faction]
date: 2026-01-12
source_file: raw/secondo_campaign_analysis_iteration_005.md
---

## Summary
Multi-model second opinion analysis (Cerebras Qwen 3, Grok 4 Fast, Perplexity Sonar Pro, GPT-5) of WorldArchitect.AI faction campaign coherence across 20-turn E2E test. All models confirm major improvements from iteration 004 fixes: timestamp reversals eliminated, dual gold tracking working, level progression incremental, tutorial messaging improved. Remaining gaps: missing arithmetic narration for gold changes, full-log timestamp verification needed, explicit tutorial completion banner needed.

## Key Claims
- **Timestamp progression**: Forward-only confirmed in sample (09:55 → 10:55), eliminates 08:05 → 08:45 reversal from iter 004. Need full-log monotonicity check.
- **Gold calculations**: Dual gold (personal 10gp vs faction gold) is now separate and consistent. +124gp gain in Scene 15 unexplained — needs explicit pre-narrative math. Prior 110gp vs 10gp and 758gp vs 748gp errors appear fixed.
- **Level progression**: Incremental only (Lvl 2, XP 300/900) — no 1→3 jumps. Fix confirmed effective.
- **Tutorial messaging**: "TUTORIAL PHASE COMPLETE — Campaign continues" banner recommended but not confirmed in sample.
- **25/25 turns passed** — system achieves full run without crashes.

## Model Perspectives
| Model | Key Insight |
|-------|------------|
| Cerebras Qwen 3 | 90% coherence uplift confirmed; recommends "Delta Log" in status blocks |
| Grok 4 Fast | Strongest timestamp fix confirmation; recommends auto-math validator |
| Perplexity Sonar Pro | Gold still needs per-scene breakdowns; skirmish costs upfront |
| GPT-5 | Structured "Equations block" before narrative recommended; standardized dice notation |

## Recommendations Across All Models
1. Add pre-narrative "Equations block" for all resource changes (gold, soldiers, territory, citizens)
2. Standardize dice notation: "1d20 (20) + INT (+1) = 21 vs DC 12 — Critical Success"
3. Make unit costs explicit: "Block = 10 soldiers; Equip new block = 100gp"
4. Add automated validator: timestamp monotonicity, XP thresholds, equation balance, scene consistency
5. Insert tutorial banner once: "TUTORIAL PHASE COMPLETE — Campaign continues."

## Connections
- [[WorldArchitect.AI]] — parent project for faction campaign
- [[CampaignCoherence]] — core concern: long-sequence consistency
- [[LLMFirstStateManagement]] — LLM-first approach to state consistency
- [[SecondOpinionWorkflow]] — multi-model review methodology
- [[TimestampProgression]]]] — Harptos calendar timestamp monotonicity
- [[GoldLedgerTracking]] — faction gold tracking with arithmetic audit trail
