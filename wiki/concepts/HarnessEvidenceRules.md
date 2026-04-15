---
title: "Harness Evidence Rules"
type: concept
tags: [harness, evidence, rules, testing, worldai]
last_updated: 2026-04-14
---

## Summary

Harness Evidence Rules define what constitutes valid evidence for passing automated quality gates. They specify artifact types, quality thresholds, and collection requirements for different harness modes (real-mode, mock-mode).

## Core Rules

**Real-mode evidence requirements** (no mocks):
- Must capture actual API responses
- Screenshots/video for UI changes
- Terminal recordings for CLI tools
- JSON artifacts for data transformations

**Minimal evidence bundle**:
```json
{
  "artifacts": [
    {"type": "terminal_recording", "path": "...", "hash": "sha256:..."},
    {"type": "screenshot", "path": "...", "hash": "sha256:..."}
  ],
  "gate_version": "2.1.0",
  "run_id": "..."
}
```

**Evidence completeness criteria**:
1. All source files are committed/referenceable
2. No placeholder content in evidence
3. Timing/metadata is realistic (not faked)
4. Hash chain links to verifiable source

## Violations

Evidence is rejected if:
- Video duration is 0 seconds or exceeds 60s without justification
- Screenshots are blank or show error states
- Terminal recording shows no commands executed
- Timestamps are in the future or pre-date source changes

## Connections
- [[HarnessEngineering]] — Harness system architecture
- [[EvidenceGateVsCompileCI]] — Evidence gates vs. traditional CI
- [[StreamingEvidenceValidation]] — Validation in streaming context
