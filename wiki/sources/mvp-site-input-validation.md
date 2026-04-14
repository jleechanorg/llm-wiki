---
title: "mvp_site input_validation"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/input_validation.py
---

## Summary
Input validation utilities for campaign IDs, user IDs, strings, request sizes, array sizes, and export formats. Provides sanitization functions to prevent injection attacks.

## Key Claims
- validate_campaign_id() validates campaign ID strings
- validate_user_id() validates user ID strings
- sanitize_string() sanitizes string input with max_length enforcement
- sanitize_user_input() sanitizes user-provided input
- validate_request_size() checks if request fits within limits
- validate_array_size() validates array/list sizes
- validate_export_format() validates export format strings

## Connections
- [[Validation]] — input validation for API requests
- [[Serialization]] — request size validation