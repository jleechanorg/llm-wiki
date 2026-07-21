---
title: "God of Murder V2 (Nocturne — The Sanguine Architecture)"
type: source
tags: [campaign, baldurs-gate, nocturne, god-of-murder, divine-mechanics, v2-spec, god-classes, apex-attention, reputation]
last_updated: 2026-07-21
source_file: "campaign_module_god_of_murder.md"
sources:
  - "world_reference/campaign_module_god_of_murder.md"
  - "world_reference/nocturne-v2-god-mechanics-design.md"
github_pr: "https://github.com/jleechanorg/worldarchitect.ai/pull/8487"
spec_path: "~/roadmap/docs/superpowers/specs/2026-07-21-nocturne-v2-god-mechanics-design.md"
---

## Summary

The Sanguine Architecture (God of Murder V2) is a Baldur's Gate 3 post-game campaign where a female Dark Urge — gestalt Gloomstalker Ranger + Assassin Rogue — drained the Netherbrain and the Crown of Karsus of their primordial energy, marched into the Undercity Temple of Bhaal, and consumed her own father's divine spark. She is now the incubating Goddess of Murder, ruling a terrified Baldur's Gate through the absolute, bloodless architecture of Submissive Death and Tragic Betrayal. The campaign is the slow ascent from a nascent Quasi-Deity anchored in a single city to a Greater Goddess waging plane-spanning deicide against the Faerûnian pantheon.

**V2 (2026-07-21)** introduces a **mechanically load-bearing divine stat scaffold** (DR/DAC/DAIR/DPP) — fixing V1's narrative-heavy "calculations which don't mean much" weakness by making the math the campaign itself.

## V2 Key Claims

### 7-tier ascension ladder (NEW in V2)

| Tier | Levels | Stat system | Ascension trigger |
|---|---|---|---|
| Mortal | L1-20 | Standard 5e | n/a |
| **Demi-god** | L21-25 | Standard 5e + divine flavor | L21 achieved |
| **Lesser god** ⭐ | L26-30 | **God stats kick in here** | First god-kill |
| Minor god | L31-35 | God stats | Reach Minor threshold |
| Intermediate god | L36-40 | God stats | Reach Intermediate threshold |
| Greater god | L41-45 | God stats | Reach Greater threshold |
| Transcendent | L46+ | Apex | Reach Transcendent |

**Ascension IS at L26 (Lesser god), NOT L21.** L21-25 is the "almost-a-god" interstitial — character mechanically stays at 5e stats.

### Mortal → Divine multiplier (NEW in V2)

```
DR   = HP × 5.4    (V1 Aizen: HP 138 → DR 750)
DAC  = AC + 4       (V1 Aizen: AC 21 → DAC 25)
DAIR = Attack + 18  (V1 Aizen: +13 → +31)
DPP  = base 825 + Reputation modifier
```

**Stronger mortals = stronger gods. Multiplier stays.** L1-19 gear choices compound forward.

### 6 god-classes with stat biases (NEW in V2)

| Class | DR | DAC | DAIR | DPP | Examples |
|---|---|---|---|---|---|
| War god | High | Low | High | Mid | Tempus, Bane |
| Trickster god | Low | Low | Very High | High | Mask, Cyric |
| Domain god | High | Mid | Mid | Mid | Chauntea, Silvanus |
| Magic god | High | Low | Mid | High | Mystra, Shar |
| Death god | Very High | Mid | Mid | Mid | Kelemvor, Myrkul |
| **Skilled god** ⭐ | Mid | Mid | **Very High** | Mid | **Nocturne (Murder)** |

**Nocturne = Skilled god** — top-tier DAIR, middling DR/DPP. She's good at killing specifically, not war-tanking.

### Hidden Reputation + Apex Attention bands (NEW in V2)

Reputation (0-100+): Unknown → Whispered → Open → Established → Revered → Pantheon-tier
Apex Attention (0-100+): Unseen → Whispered → Noticed → Marked → Hunted → Apotheosis imminent

**Player never sees the numbers.** LLM tracks, player reads the bands + LLM-generated consequences.

### Context-aware per-dawn menu (NEW in V2)

| Dawn type | Menu shape |
|---|---|
| Routine dawn | 2-3 light options |
| Triggered dawn | 4-6 full options (god-hunt, etc.) |
| Quiet dawn | No menu, narrative + stat updates only |

**Player picks → math runs deterministically → roll resolves variance within math-determined bracket.**

### Auto-win combat ladder (NEW in V2)

| Target | Result |
|---|---|
| Commoner / random NPC | Auto-win (no roll) |
| Named mortal | Auto-win (divine Save DC) |
| Chosen mortal | Divine combat (d20+DAIR vs DAC) |
| Avatar of lesser/major god | Full divine combat |
| Greater god / Apex | Full divine combat (may require action chain) |

**Combat math only matters for divine beings and Chosen NPCs.** Mortal-tier combat resolves as auto-win.

### 4-roll cap per scene (NEW in V2)

V1 had max-1-roll-per-scene. V2 allows up to 4 rolls per scene (cultist loyalty × 1, assassination attempt × 1, deception × 1, target's final death save × 1). Beyond that, the math decides.

### Deicide-cost = Apex Attention growth only (NEW in V2)

V1 had no deicide-cost (clean kill). V2 adds ONE cost: each god-kill advances Apex Attention +1 band. The mechanic is hidden (narrative surfacing only — see PR #8467).

## V2 Sample Stat Block at L26 Ascension

```
═══════════════════════════════════════════
NOCTURNE — DAWN OF L26 (Lesser God Ascension)
═══════════════════════════════════════════
Mortal form (L20, capped):
  HP 142 · AC 22 · Save DC 22 · Attack +14
  Gear: +5 Greatsword, +5 Plate, +5 Amulet
  Class: Gestalt Gloomstalker 12 / Assassin 8
  Sneak Attack pool: 10d6

DIVINE PROJECTION — LESSER GOD (L26):
  DR 766 (HP 142 × 5.4)
  DAC 26 (AC 22 + 4)
  DAIR +32 (Attack 14 + 18)
  DPP/day 825

Hidden state (narrative surfacing only):
  Reputation: "Whispered" — small cults in BG shadows
  Apex Attention: "Unseen" — gods do not know you exist

God-class: Skilled god (top-tier DAIR, mid DR/DPP)
═══════════════════════════════════════════
```

## V2 Deltas from V1 (Summary)

| V1 had | V2 changes to |
|---|---|
| Flat Divine Rank 1→20 | 7-tier ladder |
| Single Mortal → Divine | Mortal L20 → Demi-god L21-25 → Lesser god L26+ |
| No god-classes | 6 god-classes |
| No Reputation / Apex mechanics | Hidden bands (narrative surfacing only) |
| Fixed menu every dawn | Context-aware (routine / triggered / quiet) |
| Implicit combat | Auto-win ladder + 4-roll cap |
| No deicide cost | Apex Attention +1 band per kill |

## Key V1 Claims (carried forward)

- **Submissive Death Doctrine**: True perfection requires the prey to be mentally broken before the physical strike lands. Victims drop to their knees, presenting their necks.
- **Tragic Betrayal Portfolio**: Energy released by a death is proportional to the emotional weight of the bond severed. Killing loved ones releases exponential cosmic power.
- **5-Pillar Dread Court**: Ascended Astarion (High Chancellor), Dark Justiciar Shadowheart (Grand Inquisitor), Warlord Minthara (Supreme Commander), Gale of Waterdeep (Bound Vizier), Lae'zel of Kli'ir (Apostate Marshal).
- **Sanguine Sovereign / Chitinous Ruin Aspects**: Two visual aspects of the Radiant Slayer mantle.
- **3-Generation Power Lineage**: G0 Dark Urge (origin) / G1 Bhaalist elders (recontextualizer) / G2 future self or successor (inheritor's NEW choice — is the architecture good?).

## Connections

- [[AizenBg3Campaign]] — universal god-mechanics pattern (Aizen = Transcendent reference)
- [[AizenGodhoodContinuedCampaign]] — V1 reference doc that V2 inherits from
- [[DivineAscensionCeremony]] — multi-layer deception protocol for hiding divinity
- [[VisenyaV6BloodDragonApexStalker]] — sibling god-tier campaign; similar 7-tier mechanics + Sanguine Thread lineage
- [[NocturneApexPaladinCampaign]] — sibling Nocturne campaign (L20 mortal politics, no god-tier)

## Contradictions

- None identified in this source. V2 supersedes V1's narrative-heavy approach; V1 mechanical scaffold (Section 8) is preserved verbatim as the V1 foundation, V2 (Section 9) is the new overlay.

## Source Provenance

- **Source conversation:** Gemini share link — `https://share.gemini.google/Td7fA4pzuvMs` (Flash, 2026-07-20)
- **V2 design iteration:** Slack thread C0AH3RY3DK6/p1784585087 (2026-07-21, 24+ iterative rounds)
- **V2 canonical spec:** `~/roadmap/docs/superpowers/specs/2026-07-21-nocturne-v2-god-mechanics-design.md` (270 lines)
- **V2 PR:** https://github.com/jleechanorg/worldarchitect.ai/pull/8487

---

## File Stats

- **V2 world_reference source:** `world_reference/campaign_module_god_of_murder.md` (322 → ~410 lines after Section 9 overlay, +239 lines)
- **V2 canonical spec:** `world_reference/nocturne-v2-god-mechanics-design.md` (270 lines, NEW)
- **V2 wiki source:** This file (current page)