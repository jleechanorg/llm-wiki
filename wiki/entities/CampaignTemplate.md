---
title: "Campaign Template (Sovereign Solo Campaign Generator)"
type: entity
tags: [project, master-prompt, prompt-engineering, campaign-bible, dnd-5e, solo-campaign]
sources: [2026-08-04-campaign-template-prompt-v3]
last_updated: 2026-08-04
---

# Campaign Template (project)

The user's reusable master prompt for generating solo D&D 5e Campaign Bibles, currently at **prompt v3** (with a surviving **prompt v2** fragment titled the [[SovereignSoloCampaignGenerator]]). It casts the AI as an expert Narrative Designer / Game Master and demands a fully detailed nine-section bible ([[CampaignBibleNineSectionStructure]]) for a single powerful protagonist, with parameterized Tone and Setting Concept slots.

## Role in the corpus

This template is the upstream generator of the wiki's campaign-bible sources — the [[VisenyaTargaryen]] v5/v6 bibles, the [[VisenyaBelaerys]] v8 gazetteer continuation, and the Ains Overlord module all instantiate its sections. Recurring wiki concepts trace directly to its slots: [[Auctoritas]] is literally named in Section 3 as an example "Main Character" mechanic; [[CoreCompulsionMechanic]], [[MasksPublicFaceTrueNature]], and [[VipersNestFamilyStructure]] are its Section 2 and Section 5 requirements.

## Version history

- **prompt v2** — "Master Prompt: The 'Sovereign Solo' Campaign Generator", framed as "God-Mode" solo campaigns (fragment only).
- **prompt v3** — current; adds the explicit nine-section breakdown with per-section field requirements and the "do not summarize" instruction.