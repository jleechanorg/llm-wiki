---
title: "PR #5582: Revert "Revert "Allow configurable OpenClaw gateway port in Settings and use it at runtime"""
type: source
tags: []
date: 2026-02-20
source_file: raw/prs-worldarchitect-ai/pr-5582.md
sources: []
last_updated: 2026-02-20
---

## Summary
Adds **OpenClaw** as a new selectable LLM provider with configurable localhost gateway port (default `18789`). Routes inference through local OpenClaw gateway while preserving existing GCP deployment path.

- **What**: New OpenClaw provider for LLM inference via local gateway
- **Why**: Enable local development with OpenClaw while maintaining production Gemini path
- **Risk**: Medium - touches core LLM dispatch and streaming paths

## Metadata
- **PR**: #5582
- **Merged**: 2026-02-20
- **Author**: jleechan2015
- **Stats**: +6109/-747 in 54 files
- **Labels**: none

## Connections
