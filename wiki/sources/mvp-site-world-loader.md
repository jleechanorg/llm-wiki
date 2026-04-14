---
title: "mvp_site world_loader"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/world_loader.py
---

## Summary
World content loader for WorldArchitect.AI. Loads world files and creates combined instruction content for AI system prompts. Uses file caching for performance.

## Key Claims
- WORLD_DIR = mvp_site/world/ for world content files
- WORLD_ASSIAH_PATH and BANNED_NAMES_PATH for world content
- load_banned_names() loads optional banned names list
- load_world_content_for_system_instruction() combines world content with banned names

## Connections
- [[LLMIntegration]] — world content for AI prompts
