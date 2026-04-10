---
title: "Name Filtering"
type: concept
tags: [content-quality, llm-generation, worldbuilding, quality-control]
sources: ["banned-names"]
last_updated: 2026-04-08
---

## Definition
Name filtering is a quality control mechanism that prevents overused or clichéd names from appearing in AI-generated content. The filter maintains a blocklist of names that have become synonymous with generic fantasy tropes.

## Use Cases
- **WorldBuilding**: Ensuring generated NPCs, locations, and organizations have original names
- **Content Differentiation**: Preventing output that feels derivative or AI-generic
- **User Experience**: Providing more immersive, distinctive world content

## Implementation
The filtering is enforced at the prompt level — generated prompts explicitly instruct the LLM to avoid banned names. The system applies to ALL content generation contexts with no exceptions, even when users request specific names.

## Related Concepts
- [[PromptBuildingUtilities]] — constructs prompts with name restrictions
- [[ContentQualityControl]] — broader quality assurance for generated content
