---
title: "Entity Validation"
type: concept
tags: [validation, ai-safety, hallucination-prevention]
sources: [summary-test-unknown-entity-fix]
last_updated: 2026-04-08
---

Entity validation is a technique to prevent AI hallucinations by checking that key entities mentioned in the prompt actually appear in the generated output. The validator compares expected entities against the narrative and flags missing entities for retry.


## Implementation
- Expect entity list provided with prompt
- Validator checks each entity against generated narrative
- Missing entities trigger retry with updated prompt

## Edge Cases
- **Placeholder filtering**: 'Unknown' and similar placeholders filtered to avoid false failures
- **Case insensitivity**: Filtering works for 'Unknown', 'unknown', etc.
