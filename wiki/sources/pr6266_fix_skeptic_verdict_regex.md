---
title: "PR #6266 — Fix: Remove Anchor in Skeptic Verdict Regex for Bold Formatting"
type: source
tags: [CI, skeptic, regex, green-gate]
date: 2026-04-14
source_file: ../raw/pr6266_fix_skeptic_verdict_regex_2026-04-14.md
---

## Summary
Fix: remove anchor in skeptic verdict regex to capture bold formatting. The regex was too strict and failed to match CR verdicts with bold markdown.

## Files Changed
- `.github/scripts/skeptic-evaluate.sh` — +1/-2

## Technical Detail
The skeptic verdict regex used `^` anchor at start, but CR comments use bold formatting (`**VERDICT**`) which may have leading whitespace or markdown formatting. The fix removes the anchor to allow matching.

## Connections
- [[SkepticGate]] — verdict detection in skeptic gate
- [[GreenGateWorkflow]] — skeptic-evaluate.sh script used by green-gate
