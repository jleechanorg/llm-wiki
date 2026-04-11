---
title: "PR #242: [agento] fix(launchd): remove KeepAlive from lifecycle-all plist to prevent thrashing"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-242.md
sources: []
last_updated: 2026-03-28
---

## Summary
- **Root cause**: KeepAlive { SuccessfulExit: false } on ai.agento.lifecycle-all caused launchd to immediately restart the oneshot start-all.sh wrapper after every successful exit, exhausting launchd ThrashInterval protection and deregistering the service
- **Fix**: Removed KeepAlive from the plist template. Workers self-manage via pid/lock files — launchd supervision of the oneshot wrapper is unnecessary and causes thrashing
- **Also**: Reduced ThrottleInterval from 60 to 30 per spec

## Metadata
- **PR**: #242
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +717/-22 in 12 files
- **Labels**: none

## Connections
