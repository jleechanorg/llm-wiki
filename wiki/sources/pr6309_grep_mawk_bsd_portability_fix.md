---
title: "PR #6309 — Fix grep \\s to [ \\t] for mawk/BSD Portability"
type: source
tags: [CI, grep, POSIX, BSD, macOS, green-gate]
date: 2026-04-15
source_file: ../raw/pr6309_grep_aws_mawk_bsd_fix_2026-04-15.md
---

## Summary
Fix GNU-specific `\s` regex in `grep -v '^\s*#'` to POSIX-compliant `[ \t]` for mawk/BSD compatibility across macOS/Homebrew environments. The fix uses ANSI-C quoting `$'^[ \t]*#'` which bash expands to a tab character.

## Technical Details
- **GNU grep**: `\s` matches whitespace (equivalent to POSIX `[:space:]`)
- **BSD/mawk grep**: `\s` is not recognized, requires explicit `[ \t]` or `[[:space:]]`
- **Fix**: `$'^[ \t]*#'` — ANSI-C quoting supported by bash, expands `\t` to literal tab

## Evidence
```
$ xxd <<< $'^[ \t]*#'
00000000: 5e5b 2009 5d2a 230a                      ^[ .]*#.
```
Hex `09` confirms tab character in the pattern.

## Changed Files
- `.github/workflows/green-gate.yml` — lines 130, 145: `grep -v '^\s*#'` → `grep -v $'^[ \t]*#'`

## Connections
- [[GreenGateWorkflow]] — affects green-gate CI workflow patterns
- [[POSIXRegex]] — POSIX-compliant regular expression
- [[AWKCompatibility]] — mawk/BSD grep portability
- [[DesignDocGate]] — the gate that used these grep patterns (later removed by PR #6325)
