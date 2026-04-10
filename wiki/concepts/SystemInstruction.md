---
title: "System Instruction"
type: concept
tags: [ai, prompt-engineering, llm]
sources: [world-content-loader]
last_updated: 2026-04-08
---

A system instruction is the foundational prompt that guides an AI model's behavior throughout a session. In WorldArchitect.AI, system instructions combine world content, banned names, and consistency rules to ensure AI-generated narratives maintain campaign integrity.

## Components
- World canon content (e.g., World of Assiah)
- Critical naming restrictions from banned_names.md
- World consistency rules (character, timeline, power scaling, culture, geography, names)

## Usage
The [[WorldContentLoader]] module generates system instructions by:
1. Loading world content via `read_file_cached`
2. Optionally loading banned names
3. Combining with structured rules sections
4. Returning formatted string for AI API calls
