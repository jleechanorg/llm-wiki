---
title: "Visenya V9 — The Blood Dragon Apex Stalker (Dunk & Egg, 209 AC)"
type: source
tags: [campaign, visenya, blood-dragon, apex-stalker, gloom-stalker, assassin, dunk-and-egg, maekar, worldarchitect, character-creation]
date: 2026-07-20
source_file: https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit?usp=drivesdk
campaign_slug: visenya-v9-blood-dragon-apex-stalker
scene_total: 0
status: design-doc
---

## Summary

Visenya v9 is a **Level 6 Apex Stalker (Gloom Stalker / Assassin gestalt)** set during the **Time of Dunk & Egg (209 AC)**. Visenya is the **youngest daughter of Prince Maekar Targaryen** (the youngest of King Daeron's four fighting sons), awarded the barony of **Rook's Rest** near King's Landing for clearing the Crownlands' bandit problem in a single campaigning season. Her reputation as "**The Blood Dragon**" comes from the smallfolk whisper that follows her name: ruthless, surgical, patient — *she does not parley*. The class is a deliberate tonal pivot from v1's *Dragon Scholar godling puppeteer* and v4–v6's *Apex Weaver godling diplomat*: **v9's apex is a godling executioner** who operates the perimeter, deciding which sentry's neck gets the blade.

## Why v9 Exists (Brainstorm Provenance)

Across 8 prior Visenya iterations the user has chased three recurring desires:

1. **Hidden Apex blood** that mathematically outclasses everyone in the room — not louder, faster, smarter. Just *unfair* by design.
2. **A mask / mortal anchor** that anchors her humanity — Ser Duncan in Dunk & Egg; Daenerys/Ser Davos/Rhaenys in the others.
3. **A scaling tension** (Heat, Ascension Meter, Entropy Toll, Sovereign Power) — *something* that tracks "how much longer can this stay subtle?"

v9 unifies these into one campaign bible and adds **seven hard guardrails** (Section 10 of the source doc) mapping the user's recurring frustrations to specific WA prompt-layer invariants. The guardrails reference **11 open issues/PRs in `jleechanorg/worldarchitect.ai`** that already touch the same surface area — v9 makes them addressable as a single spec rather than 11 separate fires.

## Key Design Decisions

### Pivot 1: Don't replay "claim a dragon at level 6"

v1 (Dragon Scholar) and v6 (Apex Weaver) both earned their dragons at level 6. v9's apex **does not claim a dragon**. She *is* the dragon. Apex lineage, applied not to social geometry (godling puppeteer) but to **physical geometry** (which way the bolt will come, where the shadow falls, where the stress line cracks) — *the Blood Dragon is the dragon, in human form*.

### Pivot 2: Assassin/Gloomstalker, not Bard/Mastermind

The v6 *Apex Weaver* was a Bard/Mastermind gestalt — power through social manipulation. v9 is **Ranger (Gloom Stalker) / Rogue (Assassin) gestalt** — power through *physical geometry*. The "Information Geometry" of the Belaerys blood becomes **Stress-Line Sight**: she perceives the structural weaknesses in a guard rotation, the exact moment a shadow falls, the precise angle at which light refracts off an arbalest bolt. **Same mathematical perception, different application.**

### Pivot 3: The CHA-substitution flips

- v1 Dragon Scholar: CHA-based checks use INT or WIS (*charisma through intellect*)
- v9 Apex Stalker: CHA-based checks use DEX or WIS (*you do not charm, you arrive uninvited at the exact moment you were not looking*)

This is the *physical geometry* mirror of v1's *social geometry* trick.

### Pivot 4: The Wound Ledger (replaces v6's Entropy Toll)

v6's *Entropy Toll* made her suffer Exhaustion from *boredom* if she didn't manipulate. v9's *Wound Ledger* is the **virtue-into-vice inversion**: every kill *is* a sin, recorded in a literal red-leather book. At month roll 1–4 (on 1d20) the ledger *bleeds* — DC 14 WIS save or 1 Exhaustion; success = Temp HP equal to WIS mod. The ledger is **mechanical AND narrative**: a sin AND a tax, paid back as Temporary HP when the ledger is "balanced." Apex lineage turned *inward* — *the dragon files her own dead*.

### Pivot 5: The Reputation Die (replaces v6's Heat System)

The Blood Dragon's name is a weapon. A rolling **d8 → d20 Reputation Die** tracks how towns know her (Unrecognized → Recognized → Feared → Legend). It only goes up on *evidence* (kill, hanging, public display), not rumors. The rumor becomes a **rhyme** at d20: *"The Blood Dragon rides at dusk / she does not parley, she does not trust / she asks one question: where do you hide / and then she goes inside."*

### Pivot 6: Dunk as the Ditchbond (the dramatic engine)

Ser Duncan the Tall is the *only* retainer she respects. He is her **ditchbond** — the mortal anchor that keeps her from becoming a worse version of herself. A **campaign-specific bond meter** (0–10) tracks his growing trust in her *without* her ever saying what she is. The meter rises on her showing vulnerability (rare, painful for her). The dramatic engine is *his slow realization* — and her *deliberately giving him enough rope to hang his suspicions on, then pulling it back*, because she needs his honor more than she needs his ignorance.

## The Seven Guardrails (Section 10 of source doc)

| ID | Guardrail | Maps to | Status (2026-07-20) |
|---|---|---|---|
| **G1** | Strict scrying detection block — no NPC learns Visenya's Apex lineage via magic | [Issue #8468](https://github.com/jleechanorg/worldarchitect.ai/issues/8468), [PR #8469](https://github.com/jleechanorg/worldarchitect.ai/pull/8469) | Partial fix in flight |
| **G2** | Anti-frictionless campaign / cost discipline | [PR #8387](https://github.com/jleechanorg/worldarchitect.ai/pull/8387), issues #8384, #8386, #8395, #8397, #8400 | Active investigation |
| **G3** | NPC dialogue discipline (no silent monologues) | [Issue #8382](https://github.com/jleechanorg/worldarchitect.ai/issues/8382) | **Uncovered** — no merged fix |
| **G4** | No out-of-lore antagonistic events | [PRs #8439](https://github.com/jleechanorg/worldarchitect.ai/pull/8439), [#8441](https://github.com/jleechanorg/worldarchitect.ai/pull/8441), [#8443](https://github.com/jleechanorg/worldarchitect.ai/pull/8443), [#8452](https://github.com/jleechanorg/worldarchitect.ai/pull/8452) | Partial fix in flight |
| **G5** | Canonical state anchoring (no canonical-dead-NPC revival, no identity contradiction) | [PRs #8469](https://github.com/jleechanorg/worldarchitect.ai/pull/8469), [#8473](https://github.com/jleechanorg/worldarchitect.ai/pull/8473) | Partial fix in flight |
| **G6** | God-mode / Apex-injection discipline (Stress-Line Sight ≠ Precognition) | [PR #8265](https://github.com/jleechanorg/worldarchitect.ai/pull/8265), [#8132](https://github.com/jleechanorg/worldarchitect.ai/pull/8132) | **Uncovered** — no open PR |
| **G7** | Reputation die audit (no lore drift on her reputation) | Existing Heat System concept | **Uncovered** — no open PR |

The 7 guardrails are the **v9 specification for the WA prompt layer**. Future prompt-fix PRs that touch the seven areas MUST reference this section. **3 of 7 (G1, G4, G5) have partial prompt-layer fixes already in flight.** G3, G6, G7 are uncovered.

## Player Character Snapshot

**Name:** Princess Visenya Targaryen (alias: "Silver")
**Age:** 16
**Lineage:** Youngest daughter of Prince Maekar Targaryen; sister to Daeron, Aerion, and Aegon ("Egg")
**Title:** Lady of Rook's Rest, Baroness of the Rosby-Kingsroad Choke, Knight-Commander of the Black Sept
**Reputation:** "The Blood Dragon" (earned, not assumed — a rhyme, not a rumor)
**Class:** Level 6 Apex Stalker (Ranger 6 / Rogue 6 gestalt)
**Primary Stats:** DEX 18, WIS 16, INT 14, CHA 12, CON 13, STR 10
**Initiative:** +7 (DEX +4 + WIS +3 Gloom Stalker)
**Passive Perception:** 18
**Signature Mechanics:** Stress-Line Sight, Wound Ledger, Apex Predator's Patience, Blood Dragon's Reputation
**Panoply:** *Silencer* (+2 Longbow, Adamantine), *First-Severance* (+2 Rapier, Cold-Iron/Valyrian hybrid), the Wound Ledger, the Black Cloak
**Retinue (the Black Sept, 50):** Ser Tommard Heddle, Mya Rivers, the Pyromancer Galen, Old Nan, Ser Duncan the Tall (the Ditchbond)

## Starting Scene

The Whispering Glade, Kingswood, 05:00:00. Visenya has been still for nine hours on a low branch of a stag-headed oak. The bandit captain is late. She is not worried; she is patient. The wound ledger has a blank page waiting.

## Open Questions for the GM

- Where do you want Aerion's first antagonist beat to land? (He's tried to kill her twice; both attempts ended with his men in the Ledger.)
- Does the user's preference lean toward Choice B (the Diplomatic Knife) for the bandit-cell resolution, or the morally heavier Choice A (the Ledger)? Both are equally "Visenya" but produce very different campaign tones.
- Should Old Nan be allowed to die in v9? She's the only retainer who ever told Visenya "no." Her death would force a real narrative cost; her survival preserves the only check on the Blood Dragon.

## Provenance

- **Brainstorm source:** [Jeff's Slack message](https://jleechanai.slack.com/archives/C0AH3RY3DK6/p1784584425.185909) (2026-07-20) — "Look at the Google Docs and /wiki-search my Visenya campaigns and brainstorm a way to make them more interesting or better for what I like and use Google cli and then design a Visenya v9 campaign and let's set it during the time of dunk and egg and make Visenya known as the blood dragon title and a level 6 assassin gloomstalker custom class", followed by mid-turn steering: "Make me the youngest daughter of the youngest son like Aegon 16 year old sister but I am awarded a barony near Kings landing for killing all the bandits and making roads safe but due to my ruthlessness I am called the blood dragon and make a wiki page in llm wiki repo ad link it here once you're down", followed by "Just make me a Targaryen but extremely beautiful and regal and a tier above and make strict guard rails against magical scrying detection and audits and random antagonistic events that don't fit lore and see if we made any PRs yet to fix this stuff"
- **Source campaign bible (Google Doc):** https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit?usp=drivesdk
- **Brainstorm session notes:** `/tmp/visenya-v9-campaign-bible.md` (local; 55 KB)
- **Wiki version:** This page
- **Predecessor versions:**
  - [v1 Dunk & Egg wiki campaign](../sources/visenya-v1-dunk-and-egg-campaign.md) — Dragon Scholar, INT/WIS scholar
  - [Visenya Belaerys entity](../entities/VisenyaBelaerys.md) — covers v2–v6
  - [Apex Weaver concept](../concepts/ApexWeaver.md) — v5/v6 Bard/Mastermind gestalt
  - [Dragon Scholar concept](../concepts/DragonScholar.md) — v1 class
  - [Heat System concept](../concepts/HeatSystem.md) — v6 reputation mechanic (predecessor of v9's Reputation Die)
  - [Shadow Knights concept](../concepts/ShadowKnights.md) — v6 godling subjugation
  - [Obsession Paradox concept](../concepts/ObsessionParadox.md) — v6 NPC mechanic

## Connections

- [ApexWeaver](../concepts/ApexWeaver.md) — v5/v6 predecessor; v9 pivots from social geometry to physical geometry
- [VisenyaBelaerys](../entities/VisenyaBelaerys.md) — Cross-version entity
- [SerDuncanTheTall](../entities/SerDuncanTheTall.md) — The Ditchbond (v9 dramatic engine)
- [HouseTargaryen](../entities/HouseTargaryen.md) — Maekar's line, 209 AC
- [RooksRest](../entities/RooksRest.md) — The barony (NEW entity, created with v9)
- [BloodDragon](../concepts/BloodDragon.md) — Reputation mechanic (NEW concept, evolved from Heat System)
- [WoundLedger](../concepts/WoundLedger.md) — Class mechanic (NEW concept)
- [StressLineSight](../concepts/StressLineSight.md) — Apex Stalker passive (NEW concept)