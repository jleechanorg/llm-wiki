---
title: "mvp_site preventive_guards"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/preventive_guards.py
---

## Summary
Preventive Guards for continuity safeguards and state integrity enforcement. Last line of defense preventing LLM hallucinations from breaking game state. Enforces Social HP cooldown blocking (anti-blitz), world time consistency, location progress tracking, and memory deduplication.

## Key Claims
- Social HP integrity enforcement: cooldown blocking, damage capping (anti-blitz)
- World time consistency: prevents time travel exploits
- Location progress tracking: ensures valid location changes
- Core memory deduplication: prevents duplicate memories
- God mode response extraction: separates god mode from narrative
- MANDATORY: Take raw state_updates from LLM, return augmented state_changes

## Connections
- [[GameState]] — state integrity enforcement
- [[LLMIntegration]] — prevents LLM hallucinations
