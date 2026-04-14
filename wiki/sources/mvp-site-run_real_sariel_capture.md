---
title: "run_real_sariel_capture.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Captures actual LLM responses by calling the main project environment. Uses subprocess to run tests in the proper environment where Flask is available.

## Key Claims
- Runs capture in main project at `/home/jleechan/projects/worldarchitect.ai/mvp_site` where dependencies exist
- Creates Flask app and test client with `TESTING_AUTH_BYPASS=true`
- Creates campaign and runs 3 interactions (continue, ask for forgiveness with Cassian, choose option 2)
- Records "Cassian Problem" - tests if Cassian is properly referenced in narrative after explicit player reference
- Saves results to `sariel_real_responses.json` and creates detailed summary in `sariel_real_responses_summary.md`

## Connections
- [[show_sariel_test_summary]] — shows what the capture validates
- [[capture]] — uses capture infrastructure