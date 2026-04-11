---
title: "PR #487: [agento] [P1] fix bug-hunt: agents fail silently → proper error reporting + /tmp output"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-487.md
sources: []
last_updated: 2026-04-04
---

## Summary
bug-hunt-daily.sh reported "0 bugs found" as a clean sweep after all 5 bug-hunt agents failed completely (Codex had CA certificate errors, others produced 0-byte output files). Root causes: `|| true` on all agent invocations swallowed failures, empty output files were counted as 0 bugs (not failures), outputs went to ~/.openclaw/bug_reports/ (polluting the live repo), and Codex was invoked with a broken flag.

## Metadata
- **PR**: #487
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +113/-46 in 1 files
- **Labels**: none

## Connections
