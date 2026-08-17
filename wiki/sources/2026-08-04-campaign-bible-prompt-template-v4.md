---
title: "Campaign Bible Prompt Template v4 — meta-prompt architecture behind the solo D&D 5e campaign bibles"
type: source
tags: [campaign, meta-prompt, prompt-engineering, campaign-bible, dnd-5e, solo-campaign, template, narrative-design, character-architecture, faction-design, relic-design]
sources: [2026-08-04-campaign-bible-prompt-template-v4]
last_updated: 2026-08-04
---

# Campaign Bible Prompt Template v4

**Source**: Document "Campaign template / Prompt v4" — not a campaign itself, but the **generator meta-prompt** used to produce hyper-detailed, publication-ready Campaign Bibles for a single powerful protagonist in solo D&D 5e play. This is the upstream artifact behind the campaign-bible family ingested on 2026-08-04 (interpretation: the [[NocturneSosuke]] Velvet Cage line, [[NocturneRavencrest]] Deceiver's Crown, and the [[NocturneOldRepublic]] House of the Dragon bible all exhibit this template's fingerprints — MBTI typing, six-tier character profiles, faction exploit hooks — though the source does not state this explicitly).

**Note**: The source text is truncated mid-way through Part 2, Section 1 ("The Hook" cuts off at "from the sta"). Only Part 1 (sub-templates) and the opening of Part 2 are captured here.

## Role framing and parameters

The LLM is cast as an expert **Narrative Designer, Systems Architect, and Game Master**. The template takes three fill-in parameters:

- **Tone** — e.g. Lawful Evil Political, Grimdark High Fantasy, Cyberpunk Corporate Warfare, Wuxia Cultivation
- **Setting Concept** — a brief premise
- **Style directives** — rich sensory language, "Main Character" energy, variable mechanics; explicitly bans generic summaries in favor of textures, architectural styles, atmospheric detail, and "fluid mathematical systems"

**Execution Rule**: no summarizing, abbreviating, or truncating. If the output limit threatens formatting, the model must halt at a section boundary and ask permission to continue — a deliberate anti-truncation protocol for long-form generation (see [[MetaPromptCampaignGeneration]]).

## Part 1: Systemic Sub-Templates

Three reusable structural profiles that any later section must invoke:

### Sub-Template A — Standard Character Architecture ([[StandardCharacterArchitecture]])
A six-tier profile applied to EVERY generated character (protagonist, retinue, parents, siblings, faction leaders):
1. **Core Identity** — name, archetype, social standing, alignment, **MBTI type**
2. **Psychology** — core motivation, greatest fear rooted in specific formative trauma, 3–5 temperament traits
3. **Behavior and Speech** — stress ticks, explicit speech patterns (tone/cadence/vocabulary/pacing), public reputation
4. **Complete Backstory** — a singular Defining Moment (action → choice → perceived failure), chronological history, and Deep Secrets unknown to anyone
5. **Persona vs. Repressed Interior** — the manipulative outward mask vs. private self-critique when alone
6. **Unconscious Beliefs** — 2–4 absolute subconscious statements (e.g. "I am the cause of all suffering," "Power is the only objective truth")

### Sub-Template B — Faction Structural Profile ([[FactionStructuralProfile]])
Five-part organization dossier: nomenclature + sensory heraldry; infrastructure/domain (HQ, asset bracket, resource engine); a full Sub-Template A profile of the leader; internal operational culture (unwritten codes, power struggles, fate of traitors); and **The Hook** — the structural vulnerability, scandal, or leader trauma the protagonist can exploit to dismantle or control the faction. The template hard-codes factions as *targets of protagonist leverage*, matching the manipulation-first play style documented in the campaign-preferences profile.

### Sub-Template C — Tactical Masterwork / Relic Framework ([[TacticalMasterworkRelicFramework]])
Four-part magic-item spec: true name/titles/base type; exact aesthetic and material description; mythic origin lore; and **System Metrics (5e integration)** — a passive narrative property, an active tactical feature with action-economy cost, variable uses/recharge dice, and scaling DC math, plus a mandatory **Narrative Side Effect / Behavioral Urge** drawback on the attuner.

## Part 2: Campaign Bible Sections (captured portion)

**Section 1: Campaign Intro** — thematic title; The Concept (world twist, sociological themes, protagonist's ultimate goal); The Hook (why the campaign is fun, leaning heavily on power fantasy and the "systemic tools, authority, or unhinged capabilities" granted from the start). The document truncates here; later sections are not present in this source.

## Significance

This template explains the strong structural convergence across the 2026-08-04 campaign-bible ingests: every major NPC arriving with MBTI + trauma-rooted fear + exploit hook is a template output contract, not an emergent authorial choice. It is the reusable production machinery for the [[CampaignBible]] genre in this wiki.
