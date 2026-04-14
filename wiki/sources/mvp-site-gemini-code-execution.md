---
title: "mvp_site gemini_code_execution"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/gemini_code_execution.py
---

## Summary
Gemini code_execution evidence helpers providing server-verified detection of Gemini code_execution usage by inspecting SDK response structure. Detects RNG patterns (random.randint, numpy.random.*) in executed code and produces provably fair log summaries.

## Key Claims
- Detects actual random number generation in code via _RNG_PATTERNS and _RNG_FUNCTIONS_BY_MODULE
- _RNG_FACTORIES for random number generators (SystemRandom, numpy.random.default_rng)
- AST-based code analysis for safe code execution detection
- Integrates with dice_provably_fair for seed injection verification

## Connections
- [[DiceMechanics]] — code execution for dice rolls
- [[DiceProvablyFair]] — provably fair RNG detection
- [[LLMIntegration]] — Gemini code execution evidence
