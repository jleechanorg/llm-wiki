# PR #6309 — fix(green-gate): fix \s to [ \t] for mawk/BSD grep portability

**Author**: jleechan2015
**Merged**: 2026-04-15
**Labels**: agento, CI, bugfix
**Files changed**: 1

## Summary
Fix GNU-specific `\s` regex in `grep -v '^\s*#'` to POSIX-compliant `[ \t]` for mawk/BSD compatibility across macOS/Homebrew environments.

## Changes

### `.github/workflows/green-gate.yml`
- Replace `grep -v '^\s*#'` with `grep -v $'^[ \t]*#'` in design_doc_gate grep patterns (lines 130, 145)
- ANSI-C quoting `$'^[ \t]*#'` expands `\t` to tab character for POSIX compatibility

## Technical Details
- GNU grep: `\s` matches whitespace (POSIX [[:space:]])
- BSD/mawk grep: `\s` is not recognized, requires explicit `[ \t]`
- The fix uses `$'^[ \t]*#'` which is ANSI-C quoting supported by bash

## Evidence
```
$ xxd <<< $'^[ \t]*#'
00000000: 5e5b 2009 5d2a 230a                      ^[ .]*#.
```
Hex `09` confirms tab character.

## Connections
- Related to [[GreenGateWorkflow]] — affects green-gate CI workflow
- [[AWKCompatibility]] — mawk/BSD grep portability fix
- [[POSIXRegex]] — POSIX-compliant regex pattern
