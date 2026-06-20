---
title: "Pre-generation Directive"
type: concept
tags: [prompt-engineering, ai-generation, validation, testing]
sources: []
last_updated: 2026-04-08
---

A pre-generation directive is a mandatory instruction embedded in AI prompts that requires the model to perform validation checks BEFORE generating output. In the context of character name generation, this means the AI must check proposed names against a list of banned/overused names BEFORE outputting them.

## Key Characteristics
- **Mandatory**: Must use "mandatory" or "critical" language
- **Pre-generation**: Executes before any output generation
- **Check-based**: Contains explicit validation logic

## Related Concepts
- [BannedNamePrevention](BannedNamePrevention.md) — the specific prevention being validated
- [MasterDirective](../entities/MasterDirective.md) — file containing the directive
- [MechanicsSystemInstruction](../entities/MechanicsSystemInstruction.md) — contains Option 2 directive
