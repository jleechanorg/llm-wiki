---
title: "Evidence Pipeline"
type: concept
tags: [evidence, pipeline, skeptic, verification, worldai]
last_updated: 2026-04-14
---

## Summary

The Evidence Pipeline is a multi-stage verification system that collects, validates, and archives evidence artifacts (screenshots, recordings, structured data) produced during test and development workflows. It feeds into the Skeptic Gate for automated quality verification.

## Pipeline Stages

```
raw_evidence → collection → validation → archival → presentation
```

### 1. Collection
Artifacts captured via:
- Browser automation (screenshots, DOM snapshots)
- Terminal recording (asciinema cast files)
- Structured JSON (API responses, metrics)

### 2. Validation
Each artifact validated against schema:
- File integrity (hash verification)
- Size constraints (no empty artifacts, max size)
- Format correctness (valid JSON, readable images)

### 3. Archival
Artifacts stored with immutable references:
```python
evidence_path = f"/evidence/{run_id}/{artifact_type}/{timestamp}"
# Symlinked as "latest" for convenience
```

### 4. Presentation
Evidence bundles created for PRs:
```json
{
  "run_id": "...",
  "artifacts": [...],
  "verdict": "pass|fail",
  "gate_version": "..."
}
```

## Skeptic Gate Integration

The Evidence Pipeline feeds directly into [[SkepticGate]] for automated PR quality gates.

## Connections
- [[VideoEvidenceGate]] — Video-specific evidence gate
- [[EvidenceBundles]] — Bundle format specification
- [[TwoStageEvidencePipeline]] — The two-stage variant
