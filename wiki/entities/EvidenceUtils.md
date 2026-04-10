---
title: "EvidenceUtils"
type: entity
tags: [module, testing]
sources: []
last_updated: 2026-04-08
---

EvidenceUtils is a Python module within testing_mcp that handles evidence bundle generation for tests. It provides functions for capturing test provenance and generating structured evidence documentation.

## Key Functions
- **create_evidence_bundle**: Creates evidence bundle directory with test results
- **capture_provenance**: Captures git HEAD and branch information
- **validate_provenance**: Validates provenance data
- **has_critical_warnings**: Checks for critical warnings in test results

## Related Tests
- [[Evidence Utils Steps-to-Scenarios Conversion Tests]] — validates conversion logic
