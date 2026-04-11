---
title: "PR #1283: feat: Increase Gemini 2.5 Flash payload limit to 10MB"
type: source
tags: []
date: 2025-08-12
source_file: raw/prs-worldarchitect-ai/pr-1283.md
sources: []
last_updated: 2025-08-12
---

## Summary
Fixes the PayloadTooLargeError that occurs when complex game states exceed the payload limit, and provides generous headroom for future growth.

- **Issue**: Game state payload of 105,843 bytes exceeded the 100KB limit
- **Solution**: Increased MAX_PAYLOAD_SIZE to 10MB in gemini_request.py
- **Impact**: Supports very complex D&D campaigns with extensive histories

## Metadata
- **PR**: #1283
- **Merged**: 2025-08-12
- **Author**: jleechan2015
- **Stats**: +3/-1 in 1 files
- **Labels**: none

## Connections
