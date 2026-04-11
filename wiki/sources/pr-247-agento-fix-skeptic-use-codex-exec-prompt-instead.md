---
title: "PR #247: [agento] fix(skeptic): use codex exec [prompt] instead of broken --print flag"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-247.md
sources: []
last_updated: 2026-03-28
---

## Summary
The skeptic agent shells out to `codex --print --no-input` via `llm-eval.ts` for headless LLM evaluation. `codex --print` does not exist — Codex CLI uses `exec` as its primary subcommand, and prompts are passed as positional arguments. This means skeptic has always failed to use Codex and silently fell back to Claude (when `ANTHROPIC_API_KEY` was set).

Additionally, the `skeptic-run` composite action had an early-exit gate that skipped the entire skeptic run when `ANTHROPIC_API_KEY` was not set

## Metadata
- **PR**: #247
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +262/-19 in 7 files
- **Labels**: none

## Connections
