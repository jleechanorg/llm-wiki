---
title: "ZFC Leveling Systemic Audit — 30 PRs, 10% Merge Rate, Root Cause Hierarchy"
type: source
tags: [zfc, level-up, agent-drift, harness, postmortem, skill-consolidation]
date: 2026-04-25
source_file: raw/2026-04-25-zfc-systemic-audit.md
---

## Summary

A comprehensive audit of the ZFC Leveling initiative (Apr 22–25, 2026) found that ~30 PRs were opened in 4 days with only 3 (10%) actually merged. The average open PR had 22 commits, with 6 PRs hitting GitHub's 30-commit cap. Root causes were ranked: (1) no machine enforcement of file-responsibility boundaries, (2) 2,585 lines of scattered context too large for agent working memory, (3) LLM training data priors favoring "fix where you see it." The audit led to consolidating 5 fragmented ZFC skills (860 lines) into a single 139-line authoritative skill.

## Key Claims

- ~30 ZFC PRs opened in 4 days (Apr 22–25) with only 3 merged — a 10% success rate
- 6 PRs hit GitHub's 30-commit cap — each commit is a "fix the fix" cycle indicating agents spinning
- 5 recurring anti-patterns identified: (1) "fix where you see it" prior, (2) API contract ignorance, (3) "while I'm here" scope creep, (4) supersede without close, (5) evidence theater
- Root cause hierarchy: no machine enforcement > document too large > LLM training priors
- The actually useful enforcement content across all 5 skills + roadmap fits in ~80 lines
- Consolidation reduced 860 lines of skill + 100KB roadmap references to a single 139-line skill

## Key Quotes

> "3 merged out of ~30 PRs is a 10% success rate. The average open PR has 22 commits — each commit is a 'fix the fix' cycle. This is not efficient progress; it's agents spinning."

> "Agents default to training-data priors ('fix where the bug manifests') when the architecture contract is too large to hold in working memory and no proactive file-boundary check exists in the instruction/skill layer."

> "The ZFC architecture requires the opposite pattern: 'don't add it to the function that builds the response — add it upstream in the designated owner, then pass the precomputed result through.' This is a non-obvious indirection that goes against training data gravity."

> "The harness was designed for the merge/evidence layer (7-green, evidence standards, skeptic gates) but not for the design-contract layer. There's no 'architecture compliance gate' that fires per-file before the agent writes code."

## Connections

- [[ZeroFrameworkCognition]] — The ZFC boundary violations are instances of agents reverting to pre-ZFC "fix where you see it" patterns instead of respecting the "Model Computes, Backend Formats" principle
- [[AgentDrift]] — This audit quantifies the drift pattern with hard metrics (30 PRs, 10% merge rate, 22 avg commits)
- [[Harness5LayerModel]] — Root cause #1 (no machine enforcement) is a gap at L1 (Constraint layer); the skill consolidation addresses L2 (Context layer)
- [[Level-Up Systemic Fix]] — The specific file-responsibility boundaries (rewards_engine.py owns canonicalization, world_logic.py only wraps) that agents keep violating
- [[ScopeDrift]] — Pattern #3 ("while I'm here" scope creep) turned 5-file PRs into 27-file PRs
