---
title: "mvp_site utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/utils.py
---

## Summary
General-purpose utility functions for mvp_site. Provides normalize_status_code() for HTTP status code coercion and add_safe() for defensive numeric addition across ints, floats, and numeric strings.

## Key Claims
- normalize_status_code() coerces value to valid HTTP status (100-599), defaults to 200
- add_safe() performs defensive addition with caller-provided default on invalid inputs

## Connections
- [[Serialization]] — utility functions
