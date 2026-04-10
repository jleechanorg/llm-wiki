---
title: "CommentReply"
type: entity
tags: [command, github, pr-workflow]
sources: ["comment-reply-workflow"]
last_updated: 2026-04-07
---

## Description
Claude Code slash command for posting intelligent responses to PR comments. Part of the `/commentreply` system that provides systematic PR comment processing with GitHub API threading.

## Related Commands
- [[CommentFetch]] — fetches PR comments before processing

## Technical Details
- Uses secure tempfile approach (`gh --input`) to prevent shell injection
- Creates proper threaded replies with `in_reply_to_id`
- Validates coverage to prevent systematic bugs
- Single Git call for commit hash reused across all responses
