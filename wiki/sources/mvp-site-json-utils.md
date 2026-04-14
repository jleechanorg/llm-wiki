---
title: "mvp_site json_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/json_utils.py
---

## Summary
JSON parsing utilities for handling malformed or embedded JSON in LLM responses. Finds matching braces for JSON blocks and extracts best parseable JSON.

## Key Claims
- find_matching_brace() finds matching closing brace for JSON block start
- extract_best_json() attempts multiple JSON extraction strategies to find best parseable JSON

## Connections
- [[Serialization]] — JSON parsing utilities
- [[LLMIntegration]] — helps parse LLM responses