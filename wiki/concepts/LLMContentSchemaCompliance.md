---
title: "LLM Content Schema Compliance"
type: concept
tags: [schema, LLM, dice-rolls]
sources: []
last_updated: 2026-01-22
---

## Definition

LLM Content Schema Compliance refers to the challenge of ensuring LLM-generated responses include all required structured fields (like `dice_rolls`) alongside narrative content. Unlike administrative fields that are straightforward to inject, content fields require the LLM to generate and include them voluntarily.

## The Problem

LLMs tend to omit structured fields when:
1. Narrative generation is prioritized over structured output
2. The field is technically optional in schema (no hard enforcement)
3. Multiple fields compete for the LLM's attention
4. Long responses may "forget" trailing fields

## Server-Side Fallback Pattern

When LLM omits a content field, the server:
1. Logs a warning (e.g., "LLM_MISSING_FIELDS: Response missing ['dice_rolls']")
2. Computes the content server-side if needed for game logic
3. Does NOT retry or reject the response

This means the feature still works, but the audit trail is incomplete.

## Severity Assessment

| Field Type | Example | When Omitted | Severity |
|---|---|---|---|
| Administrative | `rewards_processed` | Server injects; audit incomplete | Medium |
| LLM Content | `dice_rolls` | Server computes; narrative detached | Medium |
| Critical | `rewards_box` | Rewards invisible in UI | High |

## Solutions

### Option A: JSON Schema Enforcement
Make the field required and reject responses without it. High effort, breaks existing LLM flows.

### Option B: Soft Injection
Server injects missing content fields from its own computation after the fact, annotating that the field is server-generated.

### Option C: Prompt Enrichment
Systematically remind the LLM to include content fields in the schema description.

## Sources

- dice-rolls-schema-compliance bead: combat action responses omitting dice_rolls field
