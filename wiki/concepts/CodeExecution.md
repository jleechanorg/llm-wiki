---
title: "Code Execution"
type: concept
tags: [dice, strategy, gemini, api]
sources: ["dice-strategy-selection"]
last_updated: 2026-04-08
---

Dice rolling strategy where Gemini executes Python code within a single API call to generate structured JSON dice results. The code runs `random.seed(server_seed)` before dice functions for provable fairness.
