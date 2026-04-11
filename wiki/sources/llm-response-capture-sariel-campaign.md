---
title: "LLM Response Capture — Sariel Campaign Replay"
type: source
tags: [worldarchitect, testing, llm-capture, campaign-replay, integration-testing]
source_file: "raw/llm-response-capture-sariel-campaign.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python script that captures actual LLM responses from Sariel campaign replay for documentation. Runs a single test via Flask test client and saves complete narrative responses to JSON for analysis and GitHub plan updates.

## Key Claims
- **Flask Test Client**: Uses app.test_client() for API testing without live server
- **IntegrationTestSetup**: Provides test headers and authentication bypass for campaign creation
- **Interaction Replay**: Captures responses for first 5 interactions after initial campaign creation
- **JSON Output**: Saves complete response data including timing, character count, word count
- **Test Environment**: Uses setup_integration_test_environment() for proper test initialization

## Key Quotes
> "🎯 Starting Sariel campaign replay with response capture..."

> "📄 Preview: {narrative[:100]}..."

## Connections
- [[IntegrationTesting]] — uses Flask test client pattern
- [[CampaignReplay]] — replays campaign interactions sequentially
- [[LLMResponseCapture]] — captures and stores LLM outputs for documentation

## Workflow
1. Create campaign via POST /api/campaigns
2. Replay each interaction via POST /api/campaigns/{id}/interaction
3. Capture response timing, character count, word count
4. Save to JSON for documentation and analysis
