---
title: "Visenya V9 — The Blood Dragon Apex Stalker (Dunk & Egg, 209 AC)"
type: source
tags: [campaign, visenya, blood-dragon, apex-stalker, gloom-stalker, assassin, dunk-and-egg, maekar, worldarchitect, character-creation, god-campaign, divine-rank]
date: 2026-07-20
source_file: https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit?usp=drivesdk
campaign_slug: visenya-v9-blood-dragon-apex-stalker
scene_total: 0
status: design-doc
spec: https://github.com/jleechanorg/llm-wiki/blob/main/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md
---

## Summary

Visenya v9 is a **Level 6 Apex Stalker (Gloom Stalker / Assassin gestalt)** set during the **Time of Dunk & Egg (209 AC)**, with a **L20+ god-campaign arc (Divine Rank 0 → 16+)** that scales through seven tiers. Visenya is the **youngest daughter of Prince Maekar Targaryen** (the youngest of King Daeron's four fighting sons), awarded the barony of **Rook's Rest** near King's Landing for clearing the Crownlands' bandit problem in a single campaigning season. Her reputation as "**The Blood Dragon**" comes from the smallfolk whisper that follows her name: ruthless, surgical, patient — *she does not parley*.

The class is a deliberate tonal pivot from v1's *Dragon Scholar godling puppeteer* and v4-v6's *Apex Weaver godling diplomat*: **v9's apex is a godling executioner** who operates the perimeter, deciding which sentry's neck gets the blade. Apex lineage applied to **physical geometry** (Stress-Line Sight), not social geometry (Belaerys Information Geometry).

The campaign ships as **one system with multiple emergent endings** — the player chooses the resolution at the table. The L20+ **First Song confrontation** is the climactic system feature, not a scripted plot point.

## The Sanguine Thread (the lineage mechanic)

Replaces the v6 Entropy Toll. Visenya does not keep a book of sins; she **weaves her kills into a tapestry inside herself**. The Book of the Blood Dragon transforms at each tier: Red Ledger (guilt) → Wound Ledger (page-fills = Inspiration) → Book of Names (singing) → Tapestry (patrons) → Mantle of the Sanguine Slayer (Demi-God) → Mantle of the Radiant Slayer (God Ascent) → Thread Eternal (God Reign). The thread count is a *soft input* to Divine Rank; the Reputation Die is the *primary driver*.

The Sanguine Thread is the **V6 mirror mechanic** — V6 punished non-manipulation with Exhaustion; v9 *rewards* rising reputation with Divine Rank. The two are *opposite sides of the same coin*. V6-Visenya became the First Song.

## The Reputation Die → Divine Rank Coupling

The Blood Dragon's Reputation Die is not just social flavor — it is the **primary engine of Visenya's divine ascension**. As her legend grows, magic itself responds:

| Reputation Tier | Divine Rank Bonus | Magic Barrier |
|---|---|---|
| Unrecognized | +0 | 100% sealed |
| Recognized | +0 | 95% |
| Feared | +0 | 80% |
| Legend | +1 | 50% |
| Myth | +2 | 20% |
| God | +4 | 0% (the confrontation) |

## The First Song (V6-Visenya, the interdimensional exile)

The First Song is V6-Visenya — the Blood Dragon who won her campaign, became divine, and 3000 years later has become *sadistic because bored*. She is an **interdimensional exile** who broke her own world by accident: V6-Visenya performed the Doom ritual, became a god, turned everyone in her world into "playthings" — but did not realize the cost was *the souls of every mortal in her world died*, becoming *zombie-souls*. Her world is a stage of puppets with no players.

So she travels. The Doom was a door, not a catastrophe. She crosses to *our* world looking for sentience to play with. She uses **the same god mechanics Visenya has** — identical Stress-Line Sight, Sanguine Thread, Reputation Die, Divine Rank progression. The only difference is *level* (~L40+ equivalent) and *world*. She cannot fully manifest because the **Magic Barrier System** gates her.

The First Song is present in the campaign from the start — as whispers in Yi Ti (L6-10), presence in dreams (L11-15), avatar in the Shadow Lands (L16-19), and full manifestation at L20+. The barrier decays as Visenya ascends; *she cannot stop it*. The First Song's return is *the price of becoming a god in this world*.

## The L20+ God Campaign (Archon Tier)

Inspired by Tyranny of Dragons Archon ranks — not copied:

| Tier | Rank Title | Mechanical Privilege |
|---|---|---|
| Demi-God (Ascent, L20) | The Initiate of the Blood (Archon of the First Circle) | Sovereign Sight; speak a name aloud and have it answer |
| Lesser God (L21-22) | The Warden of the Rosby Road | Domain claim — Rook's Rest + 30 miles |
| Lesser God (L23-24) | The Voice of the Doomed City | Manifest in the Doom's basalt as projection |
| Intermediate God (L25-26) | The Apex That Walks | Manifest fully in <50% sealed locations |
| Intermediate God (L27-28) | The Sovereign of the Sanguine Thread | Stress-Line Sight reads across centuries |
| Greater God (L29-30) | The Twilight of the Dragon's Daughter | Bind the First Song's avatar for 1 hour |
| Supreme God (L31+) | The Blood Dragon Ascendant (Solar-equivalent) | Full Divinity. The confrontation is unavoidable. |

**Two visual aspects at God (Ascent):** Sanguine Sovereign (alluring, terrifying, auto-succeed Charisma vs mortals) or Chitinous Ruin (frightening, DC 18 WIS or Frightened 1 hour).

## Four Emergent Endings (player choice at the table)

The campaign ships with **four documented endings**, but the player can invent more. No ending is canonical.

- **A) The Joining** — Visenya accepts the inheritance; the First Song passes through her.
- **B) The Replacement** — Visenya kills the First Song; the lineage passes by violence.
- **C) The Refusal** — Visenya breaks the Sanguine Thread; she stays mortal. The most human ending.
- **D+) Player-defined** — e.g., Visenya kills the First Song AND refuses the inheritance; or binds the First Song as her servant; or ascends but loses Dunk (ditchbond meter breaks).

## Seven Hard Guardrails

The v9 spec ships with 7 prompt-layer invariants (G1-G7) that map to **11 open WA issues/PRs**:

| ID | Guardrail | Status |
|---|---|---|
| G1 | Anti-scrying | Partial fix ([#8469](https://github.com/jleechanorg/worldarchitect.ai/pull/8469)) |
| G2 | Anti-frictionless cost discipline | Active investigation ([#8387](https://github.com/jleechanorg/worldarchitect.ai/pull/8387)) |
| G3 | NPC dialogue discipline | **Uncovered** ([#8382](https://github.com/jleechanorg/worldarchitect.ai/issues/8382)) |
| G4 | No out-of-lore antagonistic events | Partial fix ([#8443](https://github.com/jleechanorg/worldarchitect.ai/pull/8443)) |
| G5 | Canonical state anchoring | Partial fix ([#8473](https://github.com/jleechanorg/worldarchitect.ai/pull/8473)) |
| G6 | God-mode / Apex capability lock | **Uncovered** |
| G7 | Reputation die audit | **Uncovered** |

## Player Character Snapshot

**Name:** Princess Visenya Targaryen (alias: "Silver")
**Age:** 16
**Lineage:** Youngest daughter of Prince Maekar Targaryen; sister to Daeron, Aerion, and Aegon ("Egg")
**Title:** Lady of Rook's Rest, Baroness of the Rosby-Kingsroad Choke, Knight-Commander of the Black Sept
**Reputation:** "The Blood Dragon" (earned, not assumed)
**Class:** Level 6 Apex Stalker (Ranger 6 / Rogue 6 gestalt) → L20+ Archon tier progression
**Primary Stats:** DEX 18, WIS 16, INT 14, CHA 12, CON 13, STR 10
**Initiative:** +7 (DEX +4 + WIS +3 Gloom Stalker)
**Signature Mechanics:** Stress-Line Sight, Sanguine Thread (lineage), Apex Predator's Patience, Blood Dragon Reputation Die
**Panoply:** *Silencer* (+2 Longbow), *First-Severance* (+2 Rapier), the Book of the Blood Dragon, the Black Cloak
**Retinue:** Black Sept (50), Ser Tommard Heddle, Mya Rivers, the Pyromancer Galen, Old Nan, Ser Duncan the Tall

## Provenance

- **Brainstorm session Slack:** [C0AH3RY3DK6/p1784584425.185909](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1784584425.185909) (2026-07-20)
- **Source spec:** `docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md`
- **Source Google Doc:** https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit
- **Brainstorm session file:** `/tmp/visenya-v9-campaign-bible.md` (local; 55 KB)

## Connections

- [ApexWeaver](../concepts/ApexWeaver.md) — v5/v6 predecessor; v9 pivots from social geometry to physical geometry
- [VisenyaBelaerys](../entities/VisenyaBelaerys.md) — Cross-version entity; V6-Visenya is the First Song
- [SanguineThread](../concepts/SanguineThread.md) — v9 lineage mechanic (replaces WoundLedger)
- [BloodDragonReputationDie](../concepts/BloodDragonReputationDie.md) — v9 reputation mechanic
- [MagicBarrierSystem](../concepts/MagicBarrierSystem.md) — The First Song's prison
- [FirstSong](../concepts/FirstSong.md) — V6-Visenya as system feature
- [RooksRest](../entities/RooksRest.md) — Visenya's barony
- [StressLineSight](../concepts/StressLineSight.md) — Apex passive; the physical geometry mirror of v6's social geometry