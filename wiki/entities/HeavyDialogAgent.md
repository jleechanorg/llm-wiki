---
title: "HeavyDialogAgent"
type: entity
tags: [agent, worldarchitect-ai, dialog, gameplay, narrative-family]
sources: [feedback-2026-09-13-ready-gate-and-heavydialog-prompt-invariants]
last_updated: 2026-09-13
---

# HeavyDialogAgent

`HeavyDialogAgent` is one of the five core narrative family agents in `mvp_site/agents.py` within WorldArchitect.AI. It specializes in turns with complex NPC dialogue, intrigue, negotiations, and social encounters.

## Architecture

- **Subclass of**: `NarrativeFamilyAgent`
- **Prefix**: Reuses `NarrativeFamilyAgent.SHARED_PREFIX` (10 shared contracts) ensuring prefix KV cache reuse via [[GeminiImplicitPrefixCaching]].
- **Suffix**: Loads `PROMPT_TYPE_HEAVY_DIALOG` (`mvp_site/prompts/heavy_dialog_system_instruction.md`) at the end of `SUFFIX_PROMPT_ORDER`, after `PROMPT_TYPE_NARRATIVE`.
- **Word Ceiling**: 600 words (expanded from earlier 300 words in [[PR9861]]).
- **Agency Constraints**: Prohibited from authoring player character interiority or forcing unnatural verbosity.

## Related
- [[PR9861]]
- [[GeminiImplicitPrefixCaching]]
