---
title: "mvp_site settings_validation"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/settings_validation.py
---

## Summary
Settings validation helpers extracted from world_logic.py. Centralizes user settings validation for API layer, MCP tools, and other entry points. All validation functions return (validated_value, error_message) tuples.

## Key Claims
- validate_openclaw_gateway_url() validates gateway URL
- validate_openclaw_gateway_token() validates gateway token
- _is_tsnet_hostname() detects Tailscale .ts.net hostnames
- _is_disallowed_gateway_hostname() blocks localhost gateway URLs
- Returns (value, None) on success, (None, error) on failure

## Connections
- [[Validation]] — settings validation
