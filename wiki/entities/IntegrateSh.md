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

## Connections
- [[squash-merge-detection-tests]] — tests validates bug fixes
