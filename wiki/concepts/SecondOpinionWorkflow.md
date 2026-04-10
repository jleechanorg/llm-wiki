---
title: "Second Opinion Workflow"
type: concept
tags: ["validation", "testing", "workflow", "multi-model"]
sources: ["llm_wiki-raw-secondo_campaign_analysis_iteration_005.md-9798155f"]
last_updated: 2026-04-07
---

A quality assurance workflow that runs the same prompt through multiple AI models and compares outputs for coherence, correctness, and consistency. Used to identify model-specific issues and validate prompt fixes across different LLM backends.

## How It Works

1. **Same prompt** submitted to 4+ different models
2. **Outputs compared** for discrepancies in:
   - Timestamp progression
   - Gold/numeric calculations
   - Level progression
   - State consistency
3. **Analysis report** generated documenting findings

## Use Cases

- Validating game system prompts (D&D campaigns)
- Checking mathematical consistency across models
- Ensuring tutorial messaging clarity
- Identifying model-specific hallucination patterns

## Related Concepts

- [[Campaign Coherence]] — the property being validated
- [[StructuredResponse]] — common output format requirement
- [[JSONParsingFallback]] — handling model output variability