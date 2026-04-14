---
title: "mvp_site debug_hybrid_system"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/debug_hybrid_system.py
---

## Summary
Hybrid debug content system for backward compatibility with old campaigns that have embedded debug tags vs new campaigns with structured debug_info fields. Provides bracket-aware JSON extraction and JSON string unescaping.

## Key Claims
- _extract_nested_object() uses bracket-aware parsing to extract nested JSON (handles nested braces correctly)
- _unescape_json_string() handles JSON escape sequences including unicode escapes

## Connections
- [[LLMIntegration]] — debug content handling for narrative responses
