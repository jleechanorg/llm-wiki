---
title: "Campaign Bible Prompt Template v4"
type: entity
tags: [template, meta-prompt, campaign-bible, dnd-5e, narrative-design, project]
sources: [2026-08-04-campaign-bible-prompt-template-v4]
last_updated: 2026-08-04
---

# Campaign Bible Prompt Template v4

A versioned meta-prompt (v4) that casts an LLM as Narrative Designer / Systems Architect / Game Master and generates publication-ready solo D&D 5e Campaign Bibles for a single powerful protagonist. Parameterized by Tone, Setting Concept, and Style.

## Structure

- **Part 1** — three reusable sub-templates: [[StandardCharacterArchitecture]] (six-tier character profile), [[FactionStructuralProfile]] (five-part faction dossier ending in an exploit Hook), [[TacticalMasterworkRelicFramework]] (5e magic-item spec with mandatory behavioral drawback)
- **Part 2** — the Campaign Bible sections proper, opening with Campaign Intro (Title / Concept / Hook); the ingested source truncates partway through this section
- **Execution Rule** — never summarize or truncate; halt at a section boundary and ask to continue when output limits loom ([[MetaPromptCampaignGeneration]])

## Relationship to the campaign corpus

Interpretation: the 2026-08-04 campaign bibles — [[NocturneSosuke]] Velvet Cage v5/v7, [[NocturneRavencrest]] Deceiver's Crown, [[NocturneOldRepublic]] House of the Dragon — share this template's signature outputs (MBTI-typed NPCs, trauma-rooted fears, faction exploit hooks, relics with behavioral urges), making this the probable upstream generator for that family. The source itself does not name those campaigns.

Source: [[2026-08-04-campaign-bible-prompt-template-v4]]
