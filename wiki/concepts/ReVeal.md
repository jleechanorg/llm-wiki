---
title: "ReVeal"
type: concept
tags: [reveal, evidence, verification, skeptic]
last_updated: 2026-04-14
---

## Summary

ReVeal is the evidence verification component of the Skeptic Gate system. It takes evidence artifacts (screenshots, recordings, JSON bundles) and produces a pass/fail verdict based on configurable rules.

## How It Works

```
Evidence Bundle → Artifact Extraction → Rule Evaluation → Verdict
```

### Artifact Extraction
Different artifact types require different extraction:
- **Images**: Screenshot comparison against baseline
- **Video**: Frame extraction + OCR + visual diff
- **JSON**: Schema validation + semantic checks
- **Terminal**: Command sequence validation

### Rule Evaluation
Rules are defined in YAML:
```yaml
rules:
  - name: screenshot_has_content
    type: image_quality
    threshold: 0.9  # SSIM score

  - name: terminal_has_commands
    type: command_count
    min_commands: 3

  - name: response_is_valid_json
    type: json_schema
    schema: rewards_box.schema.json
```

## Verdict Output

```json
{
  "verdict": "pass",
  "scores": {"screenshot": 0.95, "terminal": 1.0, "json": 1.0},
  "rule_results": [...]
}
```

## Connections
- [[SkepticGate]] — Parent gate system
- [[EvidencePipeline]] — Evidence collection
- [[VideoEvidenceGate]] — Video-specific verification
