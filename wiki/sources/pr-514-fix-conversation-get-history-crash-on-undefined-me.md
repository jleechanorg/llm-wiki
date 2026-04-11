---
title: "PR #514: fix: conversation.get-history crash on undefined messages + dev improvements"
type: source
tags: []
date: 2025-11-02
source_file: raw/prs-/pr-514.md
sources: []
last_updated: 2025-11-02
---

## Summary
This PR fixes a critical production bug and adds development improvements:

1. **🐛 Critical Fix**: Prevents crash when conversation.get-history receives undefined messages array
2. **🚀 Dev Feature**: Auto-restart now default for local development server
3. **🔧 CI Hardening**: Added npm install retry logic for flaky CI
4. **✅ Test Fixes**: Resolved 2 pre-existing test failures in message persistence suite

---

## Metadata
- **PR**: #514
- **Merged**: 2025-11-02
- **Author**: jleechan2015
- **Stats**: +114/-25 in 7 files
- **Labels**: none

## Connections
