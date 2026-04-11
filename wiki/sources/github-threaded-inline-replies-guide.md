---
title: "GitHub Threaded Inline Replies Guide"
type: source
tags: [github, API, PR, copilot, workflow, automation]
date: 2026-04-07
source_file: raw/github-threaded-inline-replies-guide.md
last_updated: 2026-04-07
---

## Summary
Complete guide to creating threaded replies on GitHub PR review comments using the REST API. Addresses the undocumented challenge of using `in_reply_to` parameter with correct flag usage (`-F` for numeric, `-f` for strings).

## Key Claims
- **Endpoint**: `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments`
- **Threading parameter**: `in_reply_to` (NOT `in_reply_to_id`)
- **Flag usage**: `-f` for strings (body), `-F` for numeric (comment ID)
- **GitHub MCP does NOT support threaded replies** — use GitHub CLI directly
- **Common mistakes**: Wrong flag (-f vs -F), wrong parameter name (in_reply_to_id), wrong endpoint (/reviews instead of /comments)

## Key Quotes
> "Threaded replies ARE supported via GitHub REST API" — key discovery

## Connections
- [[WorldArchitect.AI]] — used in PR workflow for the project
- [[AI Universe Living Blog]] — PR lifecycle fiction relates to this workflow

## Contradictions
- None identified
