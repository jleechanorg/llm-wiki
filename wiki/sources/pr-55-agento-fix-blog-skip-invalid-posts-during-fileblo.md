---
title: "PR #55: [agento] fix(blog): skip invalid posts during FileBlogStorage.load()"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-/pr-55.md
sources: []
last_updated: 2026-03-30
---

## Summary
`FileBlogStorage.load()` directly passed persisted JSON objects into `MemoryBlogStorage.createPost()` without validating them. If a `blog-data.json` file contained a post with an invalid `status` field (any string not matching `'draft' | 'published'`), Zod validation in `MemoryBlogStorage.createPost()` would throw — causing the server to crash on startup with no recovery path.

## Metadata
- **PR**: #55
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +170/-3 in 4 files
- **Labels**: none

## Connections
