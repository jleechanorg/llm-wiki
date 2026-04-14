---
title: "mvp_site capture_actual_llm_responses"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/capture_actual_llm_responses.py
---

## Summary
Script to capture actual LLM responses from Sariel campaign using the working integration test pattern. Creates test campaigns via Flask API and records complete narrative responses for documentation and analysis.

## Key Claims
- Uses IntegrationTestSetup and setup_integration_test_environment for test infrastructure
- Creates Flask test client and bypasses auth via X-Test-Bypass-Auth headers
- Loads sariel_campaign_prompts.json and replays first 5 interactions
- Captures full response including character count, word count, expected entities
- Special "Cassian Problem" detection for entity tracking validation
- Saves responses to sariel_actual_llm_responses.json and summary markdown

## Connections
- [[LLMIntegration]] — captures actual API responses for documentation
- [[EntityTracking]] — validates entity mention in responses (Cassian Problem)
