---
title: "GeminiProvider"
type: entity
tags: [llm-provider, google, api]
sources: [gemini-native-tools-tests, gemini-code-execution-evidence-extraction-tests, gemini-request-size-logging-tests, gemini-token-ratio-real-calibration-2026-05-05]
last_updated: 2026-05-05
---

## Description
Google's Gemini LLM provider module in mvp_site.llm_providers.gemini_provider. Provides generate_json_mode_content function for JSON-mode generation with request size logging.

## Connections
- [[GenerateJsonModeContent]] — main function in this provider
- [[GeminiCodeExecution]] — code execution feature module
- [[GeminiCacheManager]] — context caching support
- [[CalibrationBiasVerification]] — real `countTokens` calibration envelope for local token-estimator constants
