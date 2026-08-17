---
title: "Meta-prompt campaign generation — LLM-as-Game-Master production pipeline"
type: concept
tags: [prompt-engineering, meta-prompt, campaign-bible, llm, narrative-design, anti-truncation]
sources: [2026-08-04-campaign-bible-prompt-template-v4]
last_updated: 2026-08-04
---

# Meta-Prompt Campaign Generation

The practice — exemplified by [[CampaignBibleTemplateV4]] — of using a parameterized meta-prompt to have an LLM mass-produce internally consistent, publication-ready campaign bibles, rather than authoring each bible by hand.

## Key techniques in the v4 template

- **Role stacking** — the model is simultaneously Narrative Designer, Systems Architect, and Game Master, forcing prose, mechanics, and playability to be handled in one pass
- **Parameter slots** — Tone, Setting Concept, and Style are the only per-campaign inputs; all structure is fixed
- **Reusable sub-templates as contracts** — [[StandardCharacterArchitecture]], [[FactionStructuralProfile]], and [[TacticalMasterworkRelicFramework]] must be invoked verbatim wherever a character, faction, or item appears, guaranteeing uniform depth across outputs
- **Anti-truncation protocol** — an explicit execution rule: never summarize or abbreviate; if the output limit threatens formatting, halt at the end of a section and ask the user for permission to continue. This turns long-form generation into a resumable, section-by-section pipeline instead of accepting silent truncation
- **Style enforcement by prohibition** — generic summaries are banned; the prompt demands textures, architecture, atmosphere, and "fluid mathematical systems" (variable DCs, recharge dice) over static numbers

## Observed downstream effect

Interpretation: the structural sameness across the 2026-08-04 campaign-bible ingests (MBTI-typed NPCs, trauma-rooted fears, faction exploit hooks, relics with behavioral urges) is the template contract executing repeatedly across different settings (Baldur's Gate 3, Warcraft III, SWTOR), not convergent authorship.

Source: [[2026-08-04-campaign-bible-prompt-template-v4]]
