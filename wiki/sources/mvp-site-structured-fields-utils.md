---
title: "mvp_site structured_fields_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/structured_fields_utils.py
---

## Summary
Utility helpers for extracting structured Gemini response fields. Provides _get_structured_attr() for safe attribute access with default values and _summarize_mapping() for dict summarization.

## Key Claims
- _get_structured_attr() safely extracts structured response attributes with defaults
- treat_falsy_as_default option for falsy-safe extraction
- _summarize_mapping() with sample_limit for dict summarization
- Used by action_resolution_utils for structured field extraction

## Connections
- [[LLMIntegration]] — structured response field extraction
