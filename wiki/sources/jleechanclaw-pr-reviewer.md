---
title: "jleechanclaw-pr-reviewer"
type: source
tags: [jleechanclaw, pr-review, github, openclaw]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/pr_reviewer.py
---

## Summary
PR review context builder that assembles complete context for LLM-powered PR reviews. Gathers PR diff, commits, CI status via gh CLI, CLAUDE.md rules from repo and global config, OpenClaw memories, and prior review patterns from action_log.jsonl. No filtering or pre-screening — everything goes into context for the LLM.

## Key Claims
- PR diffs are truncated at 300 lines with a summary note for large PRs
- CLAUDE.md rules are loaded from both repo root and global ~/.claude/CLAUDE.md
- OpenClaw memories come from ~/.openclaw/memory/ as JSONL files (project + feedback)
- Prior review patterns are scanned from ~/.openclaw/state/action_log.jsonl
- Repo path discovery checks ~/projects/, ~/repos/, ~/dev/, and worktree parent directories

## Key Quotes
> "No filtering, no pre-screening — everything goes into context for the LLM to read."

## Connections
- [[jleechanclaw-pr-review-decision]] — consumes ReviewContext for LLM-driven decisions
- [[jleechanclaw-slack-catchup]] — different Slack integration pattern
- [[jleechanclaw-human-channel-bridge]] — different Slack integration pattern

## Contradictions
- None identified