---
title: "Blood Dragon Reputation Die"
type: concept
tags: [got, game-of-thrones, mechanic, visenya-v9, reputation]
sources: [visenya-v9-blood-dragon-apex-stalker]
last_updated: 2026-07-20
---

## Summary

The **Blood Dragon Reputation Die** is the v9 evolution of the v6 Heat System. It tracks how a settlement knows Visenya as the Blood Dragon — *Unrecognized* → *Recognized* → *Feared* → *Legend*. The die only goes up on **evidence** (a kill, a hanging, a public display, an authoritative source), not rumors. Below the die's threshold per town:

| Roll | Level | Effect |
|------|-------|--------|
| 1–5 | **Unrecognized (d6)** | Treated as a minor noble, a curiosity. The Blood Dragon is whispered in the Riverlands, but not here. |
| 6–12 | **Recognized (d8)** | Common folk cross themselves. Innkeepers won't turn her away but will *watch the door*. Nobles send servants to inquire whether she intends harm. |
| 13–18 | **Feared (d10)** | The local lord sends an honor guard. Commoners do not look at her. Bandits in the area are already riding *away* before she dismounts. |
| 19–20 | **Legend (d20 locked)** | A *rhyme* is being whispered in the market. *"The Blood Dragon rides at dusk / she does not parley, she does not trust / she asks one question: where do you hide / and then she goes inside."* The local lord asks politely if she intends to take the town. |

## Evolution from v6's Heat System

The v6 Heat System tracked 0–100 (linear, with thresholds at 30/70/90). It was a *single-number* mechanic — easy for the LLM to drift on. The v9 Reputation Die has these advantages:

1. **Discrete tiers, not a linear number.** The LLM cannot "drift" by 5 — it can only step into the next tier on evidence.
2. **Locally persistent.** A town that has rolled 13+ (Feared) must remain at minimum 8 (Recognized) for the rest of the campaign. Reputation does not decay below local impact.
3. **No alias downgrade at high tiers.** A Reputation Die at 19+ (Legend) cannot be lowered by an alias. The alias may *temporarily* obscure her identity, but the legend is permanent in that locale.
4. **No rumor-driven inflation.** The die jumps only when an NPC *sees* evidence — not on tavern whispers.

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

## V6 Mirror Mechanic

V6 punished non-manipulation with Exhaustion (Entropy Toll). V9 *rewards* rising reputation with Divine Rank. The two are *opposite sides of the same coin* — V6-Visenya's campaign said "act or suffer"; v9 says "be known or stay mortal." V6-Visenya became the **First Song**; current Visenya is *answering* what V6-Visenya started.

## Connections

- [VisenyaV9BloodDragonApexStalker](../sources/visenya-v9-blood-dragon-apex-stalker.md) — Primary campaign
- [HeatSystem](../concepts/HeatSystem.md) — v6 predecessor
- [SanguineThread](../concepts/SanguineThread.md) — Companion mechanic; thread count is the *soft input* to Divine Rank, Reputation Die is the *primary* driver (replaces WoundLedger)
- [StressLineSight](../concepts/StressLineSight.md) — Sister concept; Stress-Line Sight produces outcomes that drive Reputation Die events
- [MagicBarrierSystem](../concepts/MagicBarrierSystem.md) — The barrier the Reputation Die controls
- [FirstSong](../concepts/FirstSong.md) — V6-Visenya; the consequence of the Reputation Die reaching God tier