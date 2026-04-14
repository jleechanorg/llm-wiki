---
title: "mvp_site capture_llm_responses"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/capture_llm_responses.py
---

## Summary
Script to capture actual LLM responses from Sariel campaign replay for documentation. Runs single test campaigns and saves complete narrative responses with timing data.

## Key Claims
- Uses IntegrationTestSetup pattern with Flask test client
- Loads Sariel campaign prompts and replays first 5 interactions
- Records duration, character count, word count for each response
- Special handling for "Cassian Problem" entity tracking validation
- Outputs to sariel_llm_responses_captured.json and summary markdown

## Connections
- [[LLMIntegration]] — captures actual LLM responses
- [[EntityTracking]] — validates entity mentions in responses
