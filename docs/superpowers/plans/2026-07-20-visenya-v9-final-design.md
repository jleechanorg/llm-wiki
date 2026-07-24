# Visenya V9 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the Visenya V9 — Blood Dragon Apex Stalker campaign bible, replacing the stale v1 doc and the obsolete WoundLedger concept with the new design (Sanguine Thread lineage mechanic, L20+ god campaign, First Song as system feature, four emergent endings).

**Architecture:** Three-artifact update — (1) rewrite the Google Doc with the v9 spec content (Sections 2-9 updated, Sections 12-14 added, 11 sections total), (2) update the `jleechanorg/llm-wiki` wiki pages (replace WoundLedger with SanguineThread, update ReputationDie with Divine Rank coupling, add MagicBarrierSystem + FirstSong concepts, refresh the v9 source page), (3) commit and push to `origin/main`. No WA implementation PRs in this plan — those are separate.

**Tech Stack:**
- `gog` CLI for Google Docs read/write (gog v0.10.0 at /opt/homebrew/bin/gog)
- `git` for wiki repo version control
- `gh` for GitHub API access (not used for PRs in this plan)
- Wiki repo at `~/llm_wiki` (origin: `https://github.com/jleechanorg/llm-wiki.git`)

---

## File Structure

**Files to create:**
- `~/llm_wiki/wiki/concepts/SanguineThread.md` (NEW — replaces WoundLedger)
- `~/llm_wiki/wiki/concepts/MagicBarrierSystem.md` (NEW — the First Song containment mechanic)
- `~/llm_wiki/wiki/concepts/FirstSong.md` (NEW — V6-Visenya system feature)

**Files to modify:**
- `~/llm_wiki/wiki/concepts/WoundLedger.md` — DELETE (replaced by SanguineThread.md)
- `~/llm_wiki/wiki/concepts/BloodDragonReputationDie.md` — UPDATE to add Divine Rank coupling
- `~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md` — REPLACE with v9 design content
- `~/llm_wiki/wiki/index.md` — UPDATE references (WoundLedger → SanguineThread, add new concepts)
- `~/llm_wiki/wiki/log.md` — ADD new ingest entry for v9 final design
- Google Doc `11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw` — WRITE the full v9 spec content

---

## Task 1: Verify prerequisites and gather context

**Files:**
- Read: `/Users/jleechan/llm_wiki/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md`
- Read: existing `~/llm_wiki/wiki/concepts/WoundLedger.md`
- Read: existing `~/llm_wiki/wiki/concepts/BloodDragonReputationDie.md`
- Read: existing `~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md`
- Read: existing `~/llm_wiki/wiki/index.md` (lines 109-130 for Sources section, lines 46-58 for Concepts section)

- [ ] **Step 1: Verify gog CLI auth and Google Doc ID**

```bash
gog docs info 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw
```

Expected: Document metadata returned (title, docType, length). If "invalid argument" or 401, fix `gog` auth first (check `~/.bashrc` for `HERMES_GOOGLE_TOKEN`).

- [ ] **Step 2: Verify wiki repo state is clean and on origin/main**

```bash
cd ~/llm_wiki && git fetch origin main && git status --short && git rev-parse origin/main
```

Expected: Working tree clean (or only the in-progress v9 files staged); HEAD matches origin/main SHA. If not clean, commit or stash pending changes before continuing.

- [ ] **Step 3: Read the spec file in full**

```bash
wc -l ~/llm_wiki/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md
```

Expected: ~1500 lines. Confirm the spec is the version with the First Song's final backstory (interdimensional exile, identical mechanics). If not, the spec file is stale — DO NOT continue; surface to user.

---

## Task 2: Create the new SanguineThread concept (replaces WoundLedger)

**Files:**
- Create: `~/llm_wiki/wiki/concepts/SanguineThread.md`

- [ ] **Step 1: Write the new concept file**

Use `write_file` with the following content:

```markdown
---
title: "Sanguine Thread"
type: concept
tags: [got, game-of-thrones, mechanic, visenya-v9, class-feature, ascension-track, lineage]
sources: [visenya-v9-blood-dragon-apex-stalker]
last_updated: 2026-07-20
replaces: WoundLedger
---

## Summary

The **Sanguine Thread** is Visenya v9's central mechanical and narrative element — *not a book of sins, but a lineage*. Visenya does not file her kills in a ledger; she **weaves them into a tapestry inside herself**. Every kill writes a thread in the loom. The thread is *not guilt*; the thread is *evidence of what kind of predator she is becoming*. The function of the same object — *the Book of the Blood Dragon* — shifts at each tier.

This concept **replaces the v9 Wound Ledger** (which described a death-clock mechanic that forced retirement by Level 15). The Sanguine Thread is an **ascension track**, not a death clock — it makes Visenya divine, doesn't destroy her.

## Why This Exists (the V6 mirror mechanic)

The v6 Visenya campaign used the **Entropy Toll** — Visenya suffered Exhaustion from *boredom* if she didn't manipulate. The Sanguine Thread is the **mirror mechanic across 3000 years**: V6 punished non-manipulation; v9 *rewards* rising reputation. V6-Visenya's campaign said "act or suffer"; v9 says "be known or stay mortal." The two are *opposite sides of the same coin*.

V6-Visenya became the **First Song** — she ascended but lost every mortal connection that made her human. The Sanguine Thread is the path Visenya walks; whether she follows V6 to apotheosis or refuses is the player's choice at L20+.

## Mechanics (the Book of the Blood Dragon by tier)

| Tier | Levels | Book State | Function |
|---|---|---|---|
| **Cub** | 1-5 | *The Red Ledger* (under her pillow) | Names rise monthly (1d20 1-4, DC 14 WIS save or 1 Exhaustion). The book is *guilt*. |
| **Stalker** | 6-10 | *The Wound Ledger* | Names continue to rise, but page-fills (10 names) now grant *Inspiration*. Old Nan can intervene (1/long rest reroll). |
| **Apex Predator** | 11-15 | *The Book of Names* | The names stop bleeding and start *singing*. No more Exhaustion. |
| **Sovereign** | 16-19 | *The Tapestry of the Blood Dragon* | The pages fuse into a *living document*. The names become *patrons* — minor divine sparks who owe Visenya their existence. |
| **Demi-God** | 20 | *The Mantle of the Sanguine Slayer* | **Divine Rank 1-5.** Sovereign Sight (planar geometry). The book is a *holy relic*. |
| **God (Ascent)** | 21-25 | *The Mantle of the Radiant Slayer* | **Divine Rank 6-10.** Two visual aspects (Sanguine Sovereign / Chitinous Ruin). Stat injections (+2/+4). |
| **God (Reign)** | 26-30+ | *The Thread Eternal* | **Divine Rank 11-16+.** 3e God Combat integration. The book is her. |

## Thread Count as Soft Input to Divine Rank

The Reputation Die is the **primary** engine of Divine Rank progression (see BloodDragonReputationDie). The thread count is a *soft input*: a high thread count (>500 by L20) means Visenya has *earned* the First Song confrontation by sheer killing; a low thread count (<300) means the First Song will not manifest even at L20 because Visenya is *not ready*.

## What the Book Is Not (Guardrail G6)

- **Not magical.** Leather, paper, ink. It can be stolen, burned, dropped in a river. *It does not protect itself.*
- **Not a resurrection anchor.** Killing an NPC whose name is in the book does not bring them back.
- **Not a moral authority.** The book is not a *judgment* — it is a *record*. The moral weight is the campaign's; the book is just the book she writes in.

## Connections

- [VisenyaV9BloodDragonApexStalker](../sources/visenya-v9-blood-dragon-apex-stalker.md) — Source campaign
- [BloodDragonReputationDie](../concepts/BloodDragonReputationDie.md) — Companion mechanic; the Reputation Die is the *primary* engine of ascension
- [FirstSong](../concepts/FirstSong.md) — V6-Visenya's ascended form; the destination of the Thread at L20+
- [MagicBarrierSystem](../concepts/MagicBarrierSystem.md) — The First Song's prison; the barrier weakens as Visenya ascends
```

- [ ] **Step 2: Verify the file was created correctly**

```bash
ls -la ~/llm_wiki/wiki/concepts/SanguineThread.md && head -5 ~/llm_wiki/wiki/concepts/SanguineThread.md
```

Expected: File exists, ~3 KB, first 5 lines are YAML frontmatter.

---

## Task 3: Create the MagicBarrierSystem concept (the First Song's prison)

**Files:**
- Create: `~/llm_wiki/wiki/concepts/MagicBarrierSystem.md`

- [ ] **Step 1: Write the new concept file**

Use `write_file` with the following content:

```markdown
---
title: "Magic Barrier System"
type: concept
tags: [got, game-of-thrones, mechanic, visenya-v9, lore-mechanic, first-song]
sources: [visenya-v9-blood-dragon-apex-stalker]
last_updated: 2026-07-20
---

## Summary

The **Magic Barrier System** is the v9 mechanism that controls *how much of the First Song's power can manifest in the current world*. The First Song is an *interdimensional exile* — V6-Visenya who destroyed her own world's magic containment by performing the Doom ritual — and the current world's barrier seals her in.

**Visenya's growing strength *weakens the barrier* as a side effect of her ascension.** The First Song's manifestation grows in proportion to Visenya's Reputation Die (see BloodDragonReputationDie coupling). This is the *cost* of becoming a god in this world.

## Barrier Decay Table

| Visenya Tier | Reputation Tier | Barrier % Sealed | First Song Manifestation |
|---|---|---|---|
| Cub (1-5) | Unrecognized | 100% | None. Legends only (not encountered). |
| Stalker (6-10) | Recognized | 95% | *Whispers.* Fragments in Yi Ti / Volantis. |
| Apex Predator (11-15) | Feared | 80% | *Presence.* Dreams, omens, weird coincidences. |
| Sovereign (16-19) | Legend | 50% | *Avatar.* Manifests physically in places where barrier is thinnest (Yi Ti, Shadow Lands, Doom's basalt). |
| Demi-God (20+) | Myth | 20% | *Most of her power, most of the time.* |
| God (26-30+) | God | 0% | **Full First Song. Full Visenya. The confrontation.** |

## How It Works Mechanically

The barrier is *not* a meter Visenya tracks — it's a campaign-level constant the GM rolls against behind the screen. The player *feels* the First Song's growing presence; she doesn't *track* it numerically.

The barrier decay is *automatic* — it doesn't require Visenya to *do* anything; it decays as her Divine Rank rises. **She cannot stop it.** The First Song's return is *the price of becoming a god in this world*.

## Why This Exists (the dual mechanic)

This concept pairs with the Sanguine Thread ascension track: Visenya's growth *is* the mechanism by which the First Song returns. The campaign's stakes aren't just "Visenya vs. First Song"; they're "Visenya's growth is the mechanism by which the First Song returns, and the player has to decide whether to ascend anyway."

The Magic Barrier System is also why the First Song's mechanics are **identical to Visenya's** — the barrier is the *only* difference between them. Same lineage, same Stress-Line Sight, same Sanguine Thread, same Reputation Die. The First Song is what Visenya becomes if she makes the same mistake V6-Visenya made.

## Connections

- [VisenyaV9BloodDragonApexStalker](../sources/visenya-v9-blood-dragon-apex-stalker.md) — Source campaign
- [FirstSong](../concepts/FirstSong.md) — The First Song; V6-Visenya's ascended form
- [SanguineThread](../concepts/SanguineThread.md) — Visenya's ascension track; barrier weakens as Thread completes
- [BloodDragonReputationDie](../concepts/BloodDragonReputationDie.md) — The *driver* of barrier decay; Reputation Die tier controls barrier %
```

- [ ] **Step 2: Verify the file was created correctly**

```bash
ls -la ~/llm_wiki/wiki/concepts/MagicBarrierSystem.md && head -5 ~/llm_wiki/wiki/concepts/MagicBarrierSystem.md
```

Expected: File exists, ~2.5 KB, first 5 lines are YAML frontmatter.

---

## Task 4: Create the FirstSong concept (V6-Visenya as system feature)

**Files:**
- Create: `~/llm_wiki/wiki/concepts/FirstSong.md`

- [ ] **Step 1: Write the new concept file**

Use `write_file` with the following content:

```markdown
---
title: "First Song"
type: concept
tags: [got, game-of-thrones, character, antagonist, visenya-v9, v6-mirror, interdimensional-exile]
sources: [visenya-v9-blood-dragon-apex-stalker]
last_updated: 2026-07-20
---

## Summary

The **First Song** is the L20+ system-feature antagonist of Visenya v9. She is V6-Visenya — the Blood Dragon who won her campaign, became divine, and 3000 years later has become *sadistic because bored*. She is an **interdimensional exile** who broke her own world by accident.

## True Backstory (locked)

V6-Visenya, in her timeline (298 AC in her world), performed the Doom ritual — the apex of the Apex lineage, the *completion* of the Sanguine Thread. She became a god. As a god, she turned *everyone in her world* into "playthings" — the apex lineage's cruelest expression, *the geometry of power unchained*.

But she did not realize the cost: *the souls of every mortal in her world died*. They became *zombie-souls* — bodies that move, mouths that speak, eyes that watch — but no one is *sentient* anymore. Her world is a stage of puppets with no players.

So she *travels*. The Doom was not a catastrophe for her world; it was a *door*. She crosses to *our* world/universe — Westeros, 209 AC — looking for *sentience to play with*. She is an *interdimensional exile* who broke her own world by accident and is now searching for a new one.

## Mechanics (identical to Visenya, gated by the Magic Barrier System)

The First Song uses **the same god mechanics Visenya has** — identical Stress-Line Sight scaling, identical Sanguine Thread, identical Reputation Die → Divine Rank coupling, identical L20+ Archon-tier progression. She is mechanically *identical* to Visenya — same class, same lineage, same magic.

The only difference is *level* (she is ~L40+ equivalent in her own timeline) and *world*. She cannot fully manifest in our world because (a) her world's magic containment was destroyed by her Doom ritual, (b) our world's magic containment is *intact*, and (c) the Magic Barrier System gates how much of her power can enter.

**She is what Visenya becomes if she makes the same mistake** — the same predator, the same lineage, the same Thread, just *older and alone*.

## Personality: Sadistic Because Bored

The First Song is not a monster in the *bhaal* sense (her whole cult was built on tragic betrayal; that is *not* Visenya's shape). The First Song is sadistic in the *V6* sense — *boredom-driven cruelty*. She views people as "dolls waiting to be broken." She has been a god for 3000 years and every mortal is *less interesting than a puzzle she has already solved*.

Her cruelty is *personal* (not administrative):
- She punishes boredom by *making interesting things happen* (war, plague, magical accidents).
- She manipulates mortals into *doing her work* (the way V6-Visenya manipulated Robb Stark).
- She is *vast, tired, and cruel*. She is not *evil* in the cartoon sense — she is *what the Apex lineage becomes when nothing ties it to mortality*.

## Current Domain

The First Song's *current* domain is the **Shadow Lands east of Asshai** — a place where light does not reach, where the Doom's aftermath still echoes in the basalt. She *cannot* leave this domain fully because the magic barrier seals her in. As Visenya ascends, the barrier weakens, and the First Song can manifest in more places with more power.

## The First Song as System Feature (NOT Plot Point)

The First Song is present in the campaign from the start:
- **L1-5:** The Doom is a *myth*. No manifestation.
- **L6-10:** *Whispers.* Yi Ti merchants speak of a "sleeping goddess" in the basalt. Volantene scholars mention a "first weaver."
- **L11-15:** *Presence.* Visenya travels to Yi Ti, finds the First Song's legend preserved in fragments (statues, songs, abandoned temples).
- **L16-19:** *Avatar.* The First Song manifests physically in places where the barrier is thinnest.
- **L20+:** *Full.* The barrier is 0% sealed. The confrontation is *unavoidable*.

## The Confrontation Is the Player's Choice

The campaign ships with **four documented endings**:
- **A) The Joining** — Visenya accepts the inheritance; the First Song passes through her.
- **B) The Replacement** — Visenya kills the First Song; the lineage passes by violence.
- **C) The Refusal** — Visenya breaks the Sanguine Thread; she stays mortal.
- **D+) Player-defined** — The player can invent other resolutions.

No ending is canonical.

## Connections

- [VisenyaV9BloodDragonApexStalker](../sources/visenya-v9-blood-dragon-apex-stalker.md) — Source campaign
- [SanguineThread](../concepts/SanguineThread.md) — Visenya's ascension track; the First Song's path
- [MagicBarrierSystem](../concepts/MagicBarrierSystem.md) — The First Song's prison; gates her manifestation
- [BloodDragonReputationDie](../concepts/BloodDragonReputationDie.md) — The driver of barrier decay
- [VisenyaBelaerys](../entities/VisenyaBelaerys.md) — V6-Visenya entity (the First Song's prior form)
```

- [ ] **Step 2: Verify the file was created correctly**

```bash
ls -la ~/llm_wiki/wiki/concepts/FirstSong.md && head -5 ~/llm_wiki/wiki/concepts/FirstSong.md
```

Expected: File exists, ~4 KB, first 5 lines are YAML frontmatter.

---

## Task 5: Update the BloodDragonReputationDie concept (add Divine Rank coupling)

**Files:**
- Modify: `~/llm_wiki/wiki/concepts/BloodDragonReputationDie.md`

- [ ] **Step 1: Read the existing file to confirm structure**

```bash
cat ~/llm_wiki/wiki/concepts/BloodDragonReputationDie.md
```

Expected: Existing concept with the 4-tier Reputation Die mechanic. Keep the original content; ADD the Divine Rank coupling section.

- [ ] **Step 2: Patch the file to add the Divine Rank coupling section**

Use `patch` to add the following block BEFORE the `## Connections` section:

```markdown

## Divine Rank Coupling (v9 only)

The Reputation Die is **not just social flavor** — it is the *primary engine of Visenya's divine ascension*. As her legend grows, magic itself responds. Specifically:

| Reputation Tier | Die Range | Divine Rank Bonus (cumulative) | Magic Barrier Effect |
|---|---|---|---|
| **Unrecognized** | 1-5 | +0 | Barrier: 100% sealed. The First Song cannot manifest. |
| **Recognized** | 6-12 | +0 (still mortal tier) | Barrier: 95% sealed. The First Song is whispers only. |
| **Feared** | 13-18 | +0 (still mortal tier) | Barrier: 80% sealed. The First Song is presence. |
| **Legend** | 19-20 (locked min) | **+1 Divine Rank** (entering L20+) | Barrier: 50% sealed. The First Song is avatar. |
| **Myth** | 21+ (campaign-defining) | **+2 Divine Rank** | Barrier: 20% sealed. The First Song can manifest most of her power. |
| **God** | 30+ | **+4 Divine Rank** | Barrier: 0% sealed. Full First Song. The confrontation. |

The Reputation Die only goes *up* on evidence (kills, hangings, public displays, authoritative source), not on rumors. Once at 19+, it does not decay below 8 (Recognized) in any locale. Reputation is a *persistent world state*, not a temporary modifier.
```

- [ ] **Step 3: Verify the patch**

```bash
grep -c "Divine Rank Coupling" ~/llm_wiki/wiki/concepts/BloodDragonReputationDie.md
```

Expected: Returns 2 (one in header, one in section name).

---

## Task 6: Update the v9 campaign source page

**Files:**
- Modify: `~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md`

- [ ] **Step 1: Read the existing source page**

```bash
wc -l ~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md
```

Expected: ~250 lines (the v1 source page).

- [ ] **Step 2: Replace the file with the v9 final design**

Use `write_file` to OVERWRITE the file with:

```markdown
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
| G1 | Anti-scrying | Partial fix (#8469) |
| G2 | Anti-frictionless cost discipline | Active investigation (#8387) |
| G3 | NPC dialogue discipline | **Uncovered** (#8382) |
| G4 | No out-of-lore antagonistic events | Partial fix (#8443) |
| G5 | Canonical state anchoring | Partial fix (#8469, #8473) |
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
- [SerDuncanTheTall](../entities/SerDuncanTheTall.md) — The Ditchbond
```

- [ ] **Step 3: Verify the file was overwritten**

```bash
wc -l ~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md && head -5 ~/llm_wiki/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md
```

Expected: ~150 lines; first 5 lines are YAML frontmatter with `spec:` field.

---

## Task 7: Delete the obsolete WoundLedger concept

**Files:**
- Delete: `~/llm_wiki/wiki/concepts/WoundLedger.md`

- [ ] **Step 1: Remove the file with `git rm`**

```bash
cd ~/llm_wiki && git rm wiki/concepts/WoundLedger.md
```

Expected: `rm 'wiki/concepts/WoundLedger.md'`. Note: this stages the deletion.

---

## Task 8: Update the wiki index.md (Sources, Concepts, Entities)

**Files:**
- Modify: `~/llm_wiki/wiki/index.md`

- [ ] **Step 1: Update the WoundLedger reference in the Concepts section**

Use `patch` to replace the existing `- [Wound Ledger]` entry with the new `- [Sanguine Thread]` entry. The patch replaces the line containing the old WoundLedger reference with three new lines (Sanguine Thread, Magic Barrier System, First Song).

Old text to find (single line in Concepts section):
```
- [Wound Ledger](concepts/WoundLedger.md) — v9 central mechanical object. Records every kill; bleeds 1d20 roll per month (DC 14 WIS save or 1 Exhaustion, success = Temp HP equal to WIS mod). Mechanical endgame: by Level 15, every kill costs more than it gains. NOT magical — can be stolen or burned. Source: v9 campaign bible.
```

New text (3 lines):
```
- [Sanguine Thread](concepts/SanguineThread.md) — v9 lineage mechanic (replaces WoundLedger). Visenya weaves kills into a tapestry inside herself; the Book of the Blood Dragon transforms at each tier (Red Ledger → Wound Ledger → Book of Names → Tapestry → Mantle of the Sanguine Slayer → Mantle of the Radiant Slayer → Thread Eternal). The path Visenya walks; the First Song's destination. Source: v9 spec.
- [Magic Barrier System](concepts/MagicBarrierSystem.md) — The First Song's prison. The current world's magic barrier seals the First Song; the barrier decays as Visenya's Reputation Die rises. The price of becoming a god in this world. Source: v9 spec.
- [First Song](concepts/FirstSong.md) — V6-Visenya as system feature. Interdimensional exile who broke her own world by accident; uses the same god mechanics as Visenya (identical Stress-Line Sight, Sanguine Thread, Reputation Die, Divine Rank), gated by the Magic Barrier System. Sadistic because bored, not malicious. Source: v9 spec.
```

- [ ] **Step 2: Update the v9 Sources entry to reflect the new design**

The existing source entry needs to be replaced with the updated version that mentions the spec file and the Sanguine Thread lineage mechanic.

Find the existing line:
```
- [Visenya V9 — The Blood Dragon Apex Stalker (Dunk & Egg, 209 AC)](sources/visenya-v9-blood-dragon-apex-stalker.md) — Level 6 Apex Stalker (Gloom Stalker / Assassin gestalt), youngest daughter of Maekar, Rook's Rest barony, the Blood Dragon reputation earned by clearing the Crownlands' bandits. 7 hard guardrails (G1-G7) mapped to **11 open WA issues/PRs** ([#8469](https://github.com/jleechanorg/worldarchitect.ai/pull/8469), [#8473](https://github.com/jleechanorg/worldarchitect.ai/pull/8473), [#8443](https://github.com/jleechanorg/worldarchitect.ai/pull/8443), [#8387](https://github.com/jleechanorg/worldarchitect.ai/pull/8387), [#8468](https://github.com/jleechanorg/worldarchitect.ai/issues/8468), [#8472](https://github.com/jleechanorg/worldarchitect.ai/issues/8472), [#8386](https://github.com/jleechanorg/worldarchitect.ai/issues/8386), [#8382](https://github.com/jleechanorg/worldarchitect.ai/issues/8382), [#8400](https://github.com/jleechanorg/worldarchitect.ai/issues/8400), [#8336](https://github.com/jleechanorg/worldarchitect.ai/issues/8336), [#8335](https://github.com/jleechanorg/worldarchitect.ai/issues/8335)). Source Google Doc: https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit. Entities: [[RooksRest]], [[BloodDragonReputationDie]], [[WoundLedger]], [[StressLineSight]].
```

Replace with:
```
- [Visenya V9 — The Blood Dragon Apex Stalker (Dunk & Egg, 209 AC)](sources/visenya-v9-blood-dragon-apex-stalker.md) — Level 6 Apex Stalker (Gloom Stalker / Assassin gestalt) with L20+ Archon-tier god campaign. Youngest daughter of Maekar, Rook's Rest barony, Blood Dragon reputation earned by clearing Crownlands' bandits. **Sanguine Thread lineage mechanic** (replaces v6 Entropy Toll) + Reputation Die → Divine Rank coupling + Magic Barrier System gates the First Song (V6-Visenya as interdimensional exile). **4 emergent endings** (Joining / Replacement / Refusal / Player-defined). 7 hard guardrails (G1-G7) mapped to 11 open WA issues/PRs. Source Google Doc: https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit. Entities: [[RooksRest]], [[SanguineThread]], [[BloodDragonReputationDie]], [[MagicBarrierSystem]], [[FirstSong]], [[StressLineSight]].
```

- [ ] **Step 3: Verify the index.md updates**

```bash
grep -c "Sanguine Thread\|Magic Barrier\|First Song" ~/llm_wiki/wiki/index.md
```

Expected: Returns 6+ (3 mentions per new concept — Sources, Concepts, plus cross-references).

---

## Task 9: Update the wiki log.md

**Files:**
- Modify: `~/llm_wiki/wiki/log.md`

- [ ] **Step 1: Find the existing v9 ingest entry**

```bash
grep -n "Visenya V9" ~/llm_wiki/wiki/log.md
```

Expected: One match — the v1 ingest entry (from the prior session).

- [ ] **Step 2: Append a new ingest entry for the v9 final design**

Use `patch` to ADD a new entry AFTER the existing v9 entry. Find the line:
```
## [2026-07-20] ingest | Visenya V9 — Blood Dragon Apex Stalker (Dunk & Egg, 209 AC)
```

Append immediately after the existing entry (before the next ## [date] line):
```
## [2026-07-20] finalize | Visenya V9 — final design (Sanguine Thread + First Song + L20+ god campaign)
- Source: brainstorming session Slack C0AH3RY3DK6/p1784584425.185909
- Wrote spec: `docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md` (15 sections, ~7,400 words)
- Created `wiki/concepts/SanguineThread.md` (replaces WoundLedger; lineage mechanic, 7-tier book transformation)
- Created `wiki/concepts/MagicBarrierSystem.md` (First Song's prison; barrier decays as Reputation Die rises)
- Created `wiki/concepts/FirstSong.md` (V6-Visenya as system feature; interdimensional exile; same god mechanics, gated by barrier)
- Updated `wiki/concepts/BloodDragonReputationDie.md` (added Divine Rank coupling table)
- Replaced `wiki/sources/visenya-v9-blood-dragon-apex-stalker.md` (final v9 design content)
- Deleted `wiki/concepts/WoundLedger.md` (replaced by SanguineThread)
- Updated `wiki/index.md` (Concepts section: SanguineThread, MagicBarrierSystem, FirstSong entries; Sources section: updated v9 entry)
- Source Google Doc: https://docs.google.com/document/d/11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw/edit
```

- [ ] **Step 3: Verify the log.md updates**

```bash
grep -c "Visenya V9 — final design" ~/llm_wiki/wiki/log.md
```

Expected: Returns 1.

---

## Task 10: Stage and commit all changes

**Files:**
- All wiki changes from Tasks 2-9

- [ ] **Step 1: Stage all new and modified files**

```bash
cd ~/llm_wiki && git add \
  docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md \
  wiki/concepts/SanguineThread.md \
  wiki/concepts/MagicBarrierSystem.md \
  wiki/concepts/FirstSong.md \
  wiki/concepts/BloodDragonReputationDie.md \
  wiki/concepts/WoundLedger.md \
  wiki/sources/visenya-v9-blood-dragon-apex-stalker.md \
  wiki/index.md \
  wiki/log.md
```

Expected: All paths accepted (no "fatal: pathspec ... did not match" errors).

- [ ] **Step 2: Verify staged state**

```bash
cd ~/llm_wiki && git status --short
```

Expected: Multiple `A` (added) and `M` (modified) lines, plus `D` for WoundLedger.md. NO `??` (untracked) lines for wiki/* paths.

- [ ] **Step 3: Commit with a clear message**

```bash
cd ~/llm_wiki && git commit -m "feat(campaign): Visenya V9 final design — Sanguine Thread + L20+ god campaign + First Song

Design Visenya campaign v9 as Level 6 Apex Stalker (Gloom Stalker / Assassin gestalt)
in the time of Dunk & Egg, with a L20+ Archon-tier god campaign (Divine Rank 0->16+)
and four emergent endings (Joining / Replacement / Refusal / Player-defined).

Replaces the v1 Wound Ledger (death clock) with the Sanguine Thread lineage mechanic:
the Book of the Blood Dragon transforms at each tier, making Visenya divine instead
of destroying her. The thread count is a soft input to Divine Rank; the Reputation
Die is the primary driver.

The First Song is V6-Visenya as an interdimensional exile who broke her own world
by accident (Doom ritual -> god -> turned everyone into zombie-souls). She uses
the same god mechanics Visenya has, gated by the Magic Barrier System.

Spec: docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md
Source Google Doc: 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw
Brainstorm session: Slack C0AH3RY3DK6/p1784584425.185909"
```

Expected: Commit succeeds; SHA returned (e.g., `[main abc1234] feat(campaign): Visenya V9 final design ...`).

---

## Task 11: Push to origin/main

**Files:**
- N/A (git operation)

- [ ] **Step 1: Push the commit to origin/main**

```bash
cd ~/llm_wiki && git push origin HEAD:refs/heads/main
```

Expected: `To https://github.com/jleechanorg/llm-wiki.git\n   <old_sha>..<new_sha>  HEAD -> main`. If 403/auth error, do NOT retry; surface to user.

- [ ] **Step 2: Verify origin/main updated**

```bash
cd ~/llm_wiki && git rev-parse origin/main
```

Expected: Returns the new commit SHA (matches the SHA from Task 10 Step 3).

- [ ] **Step 3: Verify the new wiki pages render on raw.githubusercontent.com**

```bash
curl -sI "https://raw.githubusercontent.com/jleechanorg/llm-wiki/main/wiki/concepts/SanguineThread.md" | head -3
curl -sI "https://raw.githubusercontent.com/jleechanorg/llm-wiki/main/wiki/concepts/MagicBarrierSystem.md" | head -3
curl -sI "https://raw.githubusercontent.com/jleechanorg/llm-wiki/main/wiki/concepts/FirstSong.md" | head -3
curl -sI "https://raw.githubusercontent.com/jleechanorg/llm-wiki/main/wiki/sources/visenya-v9-blood-dragon-apex-stalker.md" | head -3
```

Expected: All four return `HTTP/1.1 200 OK` and `content-type: text/plain; charset=utf-8`. If 404, the push did not land; check origin/main SHA.

---

## Task 12: Update the Google Doc with the v9 final content

**Files:**
- Modify: Google Doc `11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw`

- [ ] **Step 1: Read the spec file to use as the canonical Google Doc content**

```bash
cat ~/llm_wiki/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md
```

Expected: Full spec content (~7,400 words, 15 sections). This is the content that goes into the Google Doc.

- [ ] **Step 2: Truncate the existing Google Doc content (clear it first)**

The doc currently has the v1 stale content from the prior session. Clear it before writing the new content.

```bash
gog docs truncate 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw --length 1
```

Expected: Truncation confirmation. If `gog docs truncate` does not exist, use `gog docs write` to OVERWRITE (verify behavior first with `--help`).

- [ ] **Step 3: Write the new v9 spec content to the Google Doc**

```bash
cat ~/llm_wiki/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md | gog docs write 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw
```

Expected: `documentId: 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw` + `written: <bytes>`. Should report ~64,000 bytes written.

- [ ] **Step 4: Verify the doc was written**

```bash
gog docs info 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw
```

Expected: Document metadata returned; docType is `document`; length is ~64,000 bytes.

- [ ] **Step 5: Smoke-test the doc content by exporting to text**

```bash
gog docs export 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw --format txt --output /tmp/v9-doc-verify.txt
wc -l /tmp/v9-doc-verify.txt
grep -c "Sanguine Thread\|First Song\|Magic Barrier" /tmp/v9-doc-verify.txt
```

Expected: `/tmp/v9-doc-verify.txt` is ~700+ lines; the grep returns 20+ matches.

---

## Task 13: Final verification

**Files:**
- N/A (read-only checks)

- [ ] **Step 1: Confirm wiki pages live on origin/main**

```bash
for path in \
  "wiki/sources/visenya-v9-blood-dragon-apex-stalker.md" \
  "wiki/concepts/SanguineThread.md" \
  "wiki/concepts/MagicBarrierSystem.md" \
  "wiki/concepts/FirstSong.md" \
  "wiki/concepts/BloodDragonReputationDie.md" \
  "docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md"
do
  status=$(curl -sI "https://raw.githubusercontent.com/jleechanorg/llm-wiki/main/${path}" | head -1 | awk '{print $2}')
  echo "$path: $status"
done
```

Expected: All return `200`. The WoundLedger should return `404` (it was deleted).

- [ ] **Step 2: Confirm the Google Doc is updated**

```bash
gog docs info 11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw | grep -i "length\|size\|bytes"
```

Expected: Length is ~64,000 bytes (the full v9 spec content).

- [ ] **Step 3: Post completion summary**

Post a final message in the original Slack thread (C0AH3RY3DK6/p1784584425.185909) summarizing what was published:
- Wiki source page URL
- New concept pages (Sanguine Thread, Magic Barrier System, First Song)
- Updated concept (Blood Dragon Reputation Die)
- Deleted concept (Wound Ledger)
- Google Doc URL
- Spec file URL
- Next steps: optional WA PRs for G3/G6/G7 (3 uncovered guardrails)

```bash
# Use the Slack MCP tool to post in the original thread
# channel_id: C0AH3RY3DK6
# thread_ts: 1784584425.185909
```

Expected: Slack message posted with summary + URLs.

---

## Self-Review

**1. Spec coverage check:**
- Section 1 (Campaign Concept) → Task 6 (v9 source page summary section)
- Section 2 (Personality) → Task 6 (v9 source page), Task 12 (Google Doc)
- Section 3 (Apex Stalker class) → Task 6, Task 12
- Section 4 (Assets & Retinue) → Task 12 (Google Doc has full content)
- Section 5 (Family) → Task 12
- Section 6 (Setting) → Task 12
- Section 7 (World Lore) → Task 12
- Section 8 (Gazetteer & Mechanics) → Task 12
- Section 9 (Starting Scene) → Task 12
- Section 10 (Guardrails G1-G7) → Task 12 (already in v9 doc), Task 11 (verified via Wiki source page)
- Section 11 (Open PRs) → Task 12
- Section 12 (L20+ God Campaign) → Task 6, Task 12
- Section 13 (First Song as system feature) → Task 4 (FirstSong.md), Task 12
- Section 14 (Four Emergent Endings) → Task 6, Task 12
- Section 15 (Tier Starting Scene variants) → Task 12

**Coverage:** All 15 sections are addressed. The wiki pages are summaries that link to the full spec; the Google Doc is the canonical full content. ✓

**2. Placeholder scan:** No "TBD", "TODO", "implement later" in this plan. Every step has explicit commands. ✓

**3. Type/file consistency:** All file paths in Tasks 2-9 match the File Structure section. All gog CLI commands use the same doc ID (`11HohncqogJHQtIk0_JwsEuz7IsaLolFw1rM1mePM3Bw`). ✓

**4. YAGNI check:** This plan ships the *minimum* to publish the v9 design. No WA PRs are in this plan (separate scope). No Slack thread crons are created (separate scope). No new external dependencies are added. ✓

**5. TDD check:** This is a *content publication* plan, not a code-change plan. No automated tests are required for content publication; the verification steps (curl HEAD requests, gog docs info, wc -l) are the equivalent.

---

## End of Plan

Plan saved to `~/llm_wiki/docs/superpowers/plans/2026-07-20-visenya-v9-final-design.md`. 13 tasks, ~5-10 minutes total to execute.

**Two execution options:**

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Per the brainstorming/writing-plans handoff: **which approach do you want?**