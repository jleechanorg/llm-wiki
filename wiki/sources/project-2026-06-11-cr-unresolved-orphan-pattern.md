---
title: "CR unresolved orphan pattern (2026-06-11)"
type: source
tags: [code-rabbit, pr-comments, stale-orphan, addressed-marker, subagent-dispatch]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_cr_unresolved_orphan_pattern.md
---

## Summary
CodeRabbit's PR-level issue summary comment (e.g. "X open comments" with severity counts) can be **stale**: comments may be marked "✅ Addressed" by a follow-up review but not removed from the open count. Acting on the summary count wastes subagent time re-fixing already-fixed code. Verified on PR #7467: summary said "8 open review comments" with 4 Major; reality was 7 of 8 marked `✅ Addressed` in commits f8a6a97/57b25cf/eca8ad5/13b2dac, and 1 remaining was a stale orphan from PR #7242 on a file #7467 doesn't touch.

## Key Claims
- Issue-summary comments are not auto-refreshed when CodeRabbit re-reviews.
- Stale orphan pattern: comments without `✅ Addressed in commit <sha>` marker that are on files the PR didn't modify are CR-reused old review threads.
- Verified on PR #7467: 7 of 8 comments marked `✅ Addressed`, 1 remaining (scripts/test_determine_smoke_mode.sh:20) was a stale orphan from PR #7242. All 5 actual code issues genuinely fixed; 914 tests pass, 7 skipped, 0 failed.
- Operational rule: when user says "handle with subagents" + links to a CR issue comment, run the 5-step verification FIRST. If most comments are marked Addressed, skip subagent dispatch and report the resolution status.

## Key Quotes
> "Comments with that marker are resolved — do NOT act on them" — verification step

> "Acting on the summary count wastes subagent time re-fixing already-fixed code." — why it matters

> "When user says 'handle with subagents' + links to a CR issue comment, run the 5-step verification above FIRST. If most comments are marked Addressed, skip subagent dispatch and report the resolution status to the user." — protocol

## Connections
- [[CodeRabbit]] — review source
- [[CodeRabbitStall]] — companion pattern: rate-limit skips
- [[SkepticGate]] — parallel subagent verification
- [[SubagentDispatch]] — context for the wasted-effort warning
- [[PR7467]] — example PR that demonstrated the pattern
