---
title: "Run Real Sariel Capture"
type: source
tags: [testing, capture, llm-responses, sariel]
sources: [mvp-site-run-real-sariel-capture]
last_updated: 2025-01-15
---

## Summary

Captures actual LLM responses via subprocess in the main project for the Sariel campaign. Records real AI responses for replay testing and analysis.

## Key Claims

- **Subprocess execution**: Runs main project script via subprocess
- **Campaign capture**: Records LLM responses for Sariel campaign
- **Replay preparation**: Creates capture files for replay testing
- **Real mode only**: Requires real API access (Firestore, Gemini)

## Process

1. Invokes main project script as subprocess
2. Runs Sariel campaign scenarios
3. Captures all LLM responses to file
4. Prepares capture for replay testing

## Connections

- [[mvp-site-run-sariel-replays]] - Replay runner
- [[mvp-site-real-provider]] - Real service provider
- [[mvp-site-sariel-campaign]] - Sariel campaign source
