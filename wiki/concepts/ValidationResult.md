---
title: "ValidationResult"
type: concept
tags: [dataclass, validation, results, structured-output]
sources: []
last_updated: 2026-04-08
---
---

## Definition
Structured dataclass containing the outcome of narrative validation, including found/missing entities, confidence scores, warnings, and metadata.

## Fields
- **entities_found**: List of entities detected in narrative
- **entities_missing**: List of expected entities not found
- **all_entities_present**: Boolean indicating full validation success
- **confidence**: Float score (0.0-1.0) for validation certainty
- **warnings**: List of non-critical issues (e.g., continuity problems)
- **metadata**: Additional context (validator name, continuity issues)
- **validation_details**: Detailed breakdown of validation checks

## Purpose
Provides comprehensive validation feedback to narrative generation systems, enabling informed decisions about whether to accept or regenerate narrative content.

## Related Concepts
- [[EntityValidator]] — produces ValidationResult instances
- [[NarrativeSyncValidator]] — wraps EntityValidator results with narrative-specific additions
- [[ConfidenceScoring]] — used to determine acceptance thresholds
