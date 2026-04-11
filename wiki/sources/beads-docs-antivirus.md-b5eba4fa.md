---
title: "Antivirus False Positives"
type: source
tags: [beads, antivirus, false-positive, security, windows]
sources: []
date: 2026-04-07
source_file: beads/docs/antivirus.md
last_updated: 2026-04-07
---

## Summary
Guide for users encountering antivirus false positives when running beads (bd). Covers why Go binaries trigger false positives, known issues with specific vendors (Kaspersky), and solutions including exclusion lists, checksum verification, and false positive reporting.

## Key Claims
- **Industry-wide problem**: Go binaries are commonly flagged by antivirus due to heuristic detection patterns and behavioral analysis
- **Kaspersky specific**: Flags bd.exe v0.23.1 as "PDM:Trojan.Win32.Generic" via Proactive Defense Module
- **Three solution paths**: Add exclusion list, verify file integrity via checksums, report false positive to vendor
- **Mitigation measures**: Beads embeds Windows PE version info and uses code signing to reduce false positive rates
- **No code fix possible**: The issue is inherent to Go binary characteristics, not beads-specific code

## Key Quotes
> "This is a known industry-wide problem affecting many legitimate Go projects." — Go project issues reference

> "Windows PE resource metadata... is one of the most effective measures against AV false positives" — Build configuration docs

## Connections
- [[Beads]] — the affected tool
- [[Go]] — the language whose binaries trigger false positives
- [[Kaspersky]] — specific vendor with known false positive
- [[WindowsDefender]] — another affected vendor

## Contradictions
- None detected — this is documentation for a known issue, not a claim that conflicts with other wiki content
