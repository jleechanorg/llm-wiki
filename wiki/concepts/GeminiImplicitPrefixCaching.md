---
title: "Gemini Implicit Prefix Caching"
type: concept
tags: [gemini, prompt-engineering, caching, performance, worldarchitect-ai]
sources: [feedback-2026-09-13-ready-gate-and-heavydialog-prompt-invariants, feedback-2026-08-18-gemini-cache-si-identity-vs-byte0-lcp]
last_updated: 2026-09-13
---

# Gemini Implicit Prefix Caching

Gemini models implement server-side implicit KV-caching based on the longest common prefix of tokens. In WorldArchitect.AI, this mechanism is leveraged across gameplay agents by maintaining a shared, byte-identical prompt prefix.

## Architecture

- **Shared Prefix**: `NarrativeFamilyAgent.SHARED_PREFIX` contains 10 core contracts loaded identically across all 5 narrative family agents (`StoryModeAgent`, `HeavyDialogAgent`, `LoreAgent`, etc.).
- **Suffix Isolation**: Agent-specific directives (e.g. `HeavyDialogAgent` dialogue word count guidance, `LoreAgent` world-building constraints) must be appended via `SUFFIX_PROMPT_ORDER` *after* the shared prefix contracts.
- **Precedence Control**: When an agent needs to modify guidance established earlier (e.g. `HeavyDialogAgent` expanding the 180-word narrative ceiling to 600 words), its dedicated prompt must appear strictly after `PROMPT_TYPE_NARRATIVE` in `SUFFIX_PROMPT_ORDER`. This overrides earlier rules without perturbing the shared prefix.

## Invariants

1. Never modify shared prefix contracts to solve single-agent requirements.
2. Never inject dynamic per-session or per-turn state into prefix contracts.
3. Validate byte-identity across agents when modifying prefix prompt definitions.

## Related
- [[HeavyDialogAgent]]
- [[CampaignBibleDuplication]]
- [[LatencyOptimization]]
