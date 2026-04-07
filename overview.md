---
title: "Overview"
type: synthesis
tags: []
sources: [ai-universe-living-blog, bd-beads, ai-usage-tracker]
last_updated: 2026-04-07
---

# Overview

*The page is maintained by the LLM. It is updated on every ingest to reflect the current synthesis across all sources.*

## Current Knowledge

**AI Usage Tracker** adds comprehensive token usage and cost tracking:


- Combines `ccusage` (Claude) and `ccusage-codex` (Codex) data
- Side-by-side reporting with daily averages
- Claude tokens are ~2.8x more expensive but Codex uses ~67% of total tokens
- Cache efficiency of 90%+ on both platforms
- Installable as Claude skill (`/combined-usage`)
- Typical daily cost: $150-250/day for heavy usage

**AI Universe Living Blog** combines two systems:

1. **Blog MCP Server** — HTTP JSON-RPC 2.0 server exposing 7 MCP tools for CRUD operations on blog posts and threads. Supports event types like `pr_created`, `pr_reviewed`, `pr_merged`, plus novel types `novel_branch_entry` and `novel_daily_summary`.

2. **Novel Engine** — transforms real PR lifecycle events into serialized fiction. Two pipelines: branch entry (per-session, ~400-800 words) and daily community summary (synthesized from day's posts, 1000+ words with 2-4 POV inserts). Uses story bead system (15 emotional narrative beats) for traceability.

Key innovation: zero-config dev mode allowing immediate use without Firebase credentials.

**Beads** adds graph-based issue tracking for AI agents:

- Provides persistent, structured memory replacing markdown plans
- Dependency-aware graph enables long-horizon task handling
- Dolt-powered SQL database with git-backed versioning
- Hash-based IDs prevent merge conflicts in multi-agent workflows
- Memory compaction summarizes old tasks to save context window
