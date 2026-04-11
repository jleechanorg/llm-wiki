---
title: "Comment Reply Workflow"
type: source
tags: [github, pr-comments, automation, workflow, api]
sources: []
source_file: docs/commentreply_workflow.md
last_updated: 2026-04-07
---

## Summary

The `/commentreply` system provides intelligent, systematic processing of PR comments with proper GitHub API threading to prevent missed comment bugs. It uses a 3-step workflow: fetching comments, analyzing/fixing via Claude, and posting responses via GitHub API.

## Key Claims

- **3-Step Workflow**: Comment Fetching (/commentfetch) → Analysis & Fixes (Claude) → Response Posting (Python)
- **Interface Files**: Input via `/tmp/{branch}/comments.json`, output via `/tmp/{branch}/responses.json`
- **Shell Injection Prevention**: Uses secure tempfile + `gh --input` approach instead of shell string interpolation
- **Threaded Replies**: Creates proper threaded replies with `in_reply_to_id` to prevent comment threading bugs
- **Anti-Bug System**: Explicit coverage validation, threaded reply verification, error tracking, atomic operations
- **Performance**: Single git call for commit hash, batch processing, secure temporary files

## Key Interface

### Input (comments.json)
```json
{
  "comments": [{
    "id": "2310770476",
    "user": { "login": "author_name" },
    "body": "Comment text",
    "path": "file/path.py",
    "line": 42
  }]
}
```

### Output (responses.json)
```json
{
  "pr": "1510",
  "commit_hash": "43dca36e",
  "responses": [{
    "comment_id": "2310770476",
    "response": "Technical response with analysis, fix, verification",
    "implemented_fix": true
  }]
}
```

## Security Features

- Shell injection prevention via secure tempfile
- Rate limiting protection for GitHub API
- Input validation for JSON structure
- Coverage validation to prevent missed comments