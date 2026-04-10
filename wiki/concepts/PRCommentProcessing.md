---
title: "PR Comment Processing"
type: concept
tags: [workflow, github, pr, automation]
sources: ["comment-reply-workflow"]
last_updated: 2026-04-07
---

## Description
Systematic workflow for processing PR comments to prevent the common bug where comments are silently missed while claiming 100% coverage. Uses a 3-step process: fetch, analyze/fix, and post responses.

## Process Steps
1. **Fetch** — Use [[CommentFetch]] to gather all PR comments with metadata
2. **Analyze & Fix** — Claude reads comments, implements fixes, generates technical responses
3. **Post** — Use [[CommentReply]] to post responses via GitHub API with proper [[CommentThreading]]

## Anti-Bug Mechanisms
- Explicit coverage validation re-fetches comments after processing
- Threaded reply verification checks for proper `in_reply_to_id`
- Error tracking reports exactly which comments failed
- Atomic operations ensure clear error reporting on failure

## Related Concepts
- [[CommentThreading]] — GitHub API threading concept
- [[ShellInjectionPrevention]] — security feature in the workflow
