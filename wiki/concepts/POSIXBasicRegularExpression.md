---
title: "POSIX Basic Regular Expression (BRE)"
type: concept
tags: [regex, posix, bash, sed]
sources: []
last_updated: 2026-04-08
---

The POSIX Basic Regular Expression syntax used by sed and grep by default. In BRE, special characters like `+` and `?` are literal unless escaped with backslash.

## Common Patterns
- `[0-9]` — matches a single digit
- `[0-9]*` — matches zero or more digits (PROBLEM: matches empty string)
- `[0-9][0-9]*` — matches one or more digits (CORRECT)
- `\+` — escaped plus matches literal + character

## Bug Example
The pattern `s/ (#[0-9]*)$//` in sed uses BRE where `*` matches zero or more. This causes `(#)` to incorrectly match and strip, resulting in empty strings. The fix requires `[0-9][0-9]*` to ensure at least one digit is present.

## Related
- [[squash-merge-detection-tests]] — tests that validate BRE behavior
