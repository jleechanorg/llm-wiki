---
title: "Comment Threading"
type: concept
tags: [github, api, pr, threading]
sources: ["comment-reply-workflow"]
last_updated: 2026-04-07
---

## Description
GitHub API concept for creating proper reply relationships between PR comments. Uses `in_reply_to_id` parameter to create threaded replies that maintain conversation context and prevent comment visibility issues.

## Why It Matters
Without proper threading, replies appear as top-level comments rather than responses to specific comments, making it easy to miss comments in long PR discussions.

## Related Concepts
- [[PRCommentProcessing]] — workflow that uses threading
- [[ShellInjectionPrevention]] — security concept for the comment system
