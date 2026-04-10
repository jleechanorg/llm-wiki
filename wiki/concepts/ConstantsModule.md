---
title: "Constants Module"
type: concept
tags: [python, design-pattern, configuration]
sources: ["test-constants-module-values-structure"]
last_updated: 2026-04-08
---

## Overview
A design pattern in Python where related constant values are centralized in a single module rather than scattered throughout the codebase. This approach provides a single source of truth for configuration values, making them easier to maintain, update, and test.

## Benefits
- **Single Source of Truth**: All related constants in one location
- **Easy Maintenance**: Changes only needed in one place
- **Type Safety**: Can add validation to ensure constant types
- **Testing**: Easy to mock or override in tests
- **Documentation**: Constants serve as implicit documentation

## Example from mvp_site
The mvp_site/constants.py module contains:
- Actor constants (ACTOR_USER, ACTOR_GEMINI)
- Interaction modes (MODE_CHARACTER, MODE_GOD)
- Dictionary keys (KEY_*)
- Export formats (FORMAT_*)
- Prompt configuration (FILENAME_*, PROMPT_TYPE_*, PROMPTS_DIR)

## Related Concepts
- [[Python Testing]] — validates constants work as expected
- [[Configuration Management]] — broader concept of managing application settings
