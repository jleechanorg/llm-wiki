---
title: "PR #1855: fix: Update CSP to allow CDN resources for Bootstrap and Firebase"
type: source
tags: []
date: 2025-10-11
source_file: raw/prs-worldarchitect-ai/pr-1855.md
sources: []
last_updated: 2025-10-11
---

## Summary
- Allow script-src from cdn.jsdelivr.net, www.gstatic.com, apis.google.com
- Allow style-src from cdn.jsdelivr.net  
- Allow font-src from cdn.jsdelivr.net and data URIs
- Allow connect-src for Firebase authentication endpoints
- Allow img-src for all HTTPS sources and data URIs

## Metadata
- **PR**: #1855
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +6/-1 in 1 files
- **Labels**: none

## Connections
