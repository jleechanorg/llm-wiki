---
title: "Integrate.sh"
type: entity
tags: [script, integration, bash, git]
sources: []
last_updated: 2026-04-08
---

Bash script that handles integration workflows including squash-merge detection. Contains `detect_squash_merged_commits()` function that parses git commit messages for PR references in the format `(#123)`.

## Known Issues Fixed
- Regex bug: Pattern `[0-9]*` matches zero digits, causing false positives on `(#)`
- Empty string handling: Missing guard caused false positives when stripping produces empty results
- grep behavior: Missing --fixed-strings flag caused regex interpretation issues

## Script resolution: local override vs. maintained global fallback

When a repo has no `./integrate.sh`, `/integrate` falls back to the maintained
global copy at
`~/.claude/plugins/marketplaces/claude-commands-marketplace/scripts/integrate.sh`
rather than treating the missing local file as a hard failure. That script is
kept ahead of the top-level marketplace copy (`.../integrate.sh`) — verify by
content/hash, not mtime, since the two can share a filesystem mtime. See
[feedback-2026-08-28-integrate-global-script-fallback](../sources/feedback-2026-08-28-integrate-global-script-fallback.md).

## Connections
- [squash-merge-detection-tests](../sources/squash-merge-detection-tests.md) — tests validates bug fixes
- [feedback-2026-08-28-integrate-global-script-fallback](../sources/feedback-2026-08-28-integrate-global-script-fallback.md) — global-script fallback + `--new-branch` recovery pattern
- [[IntegrateHardStopPattern]] — hard-stop / `--new-branch` recovery discipline this fallback case follows
