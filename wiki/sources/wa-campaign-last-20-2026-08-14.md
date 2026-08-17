---
title: "WA Campaign Discovery — Last 20 + 50+ Pool (2026-08-14, scope-corrected)"
type: source
tags: [campaign, worldarchitect, firestore, source]
date: 2026-08-14
source_file: /tmp/avatar_scene_gen/01_campaigns.jsonl (20 rows)
campaign_count_top20: 20
campaign_count_50plus_strict_last20: 1
qualifying_campaign: Overlord shy lich (JQeI1Aq5, 364 entries)
subject_user: jleechan@gmail.com (uid vnLp2G3m21PJL6kxcuAqmWSOtm73)
scope_note: "Strict last-20 → filter ≥50 entries → 1 campaign qualifies. Earlier wider-pool picks discarded."
scene_candidates_source: /tmp/avatar_scene_gen/02_scene_candidates.md
last20_over50_artifact: /tmp/avatar_scene_gen/last20_over50.json
---

# Step 1 — Scene Candidates (5 scenes, Overlord-only)

**Date:** 2026-08-14
**Subject user:** jleechan@gmail.com (uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`)
**Scope (corrected):** Of jleechan's last 20 campaigns (sorted by `last_played` desc), only **1** (`Overlord shy lich`, id8 `JQeI1Aq5`, 364 entries) passes the ≥50-entry threshold. Under the strict rule *"last 20 by `last_played` desc → filter to ≥50 entries → pick 5 scenes"*, **all 5 scenes come from this single campaign**. The earlier wider-pool picks (Overlord Carne + Valeria + SWTOR Tenebria + Visenya v9 + Supergirl) were discarded in Step 5 RE-DO and the corresponding wiki folders + 5 entity pages removed.

> Earlier `/tmp/avatar_scene_gen/02_scene_candidates.md` v1 documented the wider-pool picks (262 campaigns with 50+ entries) and was overwritten with the Overlord-only table below.

**Avatar URL reality (unchanged):** Each WA campaign stores **one campaign-level avatar** in `game_states.current_state.<avatar field>` pointing to a Google Cloud Storage URL. NPC portraits are *not* stored as separate URLs in any field we walked (root doc, `player_character_data`, `npc_data`, or nested state). The parent agent used these campaign-level avatars as the visible character in scenes — or, if multi-avatar depictions are required, generate per-character portraits from the existing avatar as a base.

---

## Scene Candidates — All 5 from Overlord shy lich

| # | Slug | Entry range | Scene summary | Why memorable | Named NPCs | Drive avatars (sha8 + filename) |
|---|---|---|---|---|---|---|
| 1 | `treasury_audit_opening` | `[7, 9]` | Soft pale-blue arcane light spills across the polished mahogany of the Nazarick Council Chamber. Demiurge presents leather-bound ledgers detailing 14,000 mouths to feed and zero local currency, then Ains selects the Carne Village agricultural-sanctuary plan. Sebas Tian escorts the masked Ains out into the New World's pine-scented air. | The campaign's opening moral crisis — a god-queen forced into economy-of-wheat decisions that will define her entire reign. | Ains, Demiurge, Sebas Tian, Albedo (referenced), Aura (referenced), Shalltear (referenced) | `ca197e7b` — `Ains shy lich` (Ains) <br>`(fallback)` — `campaign-level avatar.png` (Demiurge / Sebas stand-in) |
| 2 | `royal_audience_re_estize` | `[79, 93]` | The mahogany doors of the Re-Estize Throne Room groan open. Ains curtsies before King Ramposa III and presents the Sovereign's Covenant. Gazef Stronoff steps forward in silver armor to testify that the "minor envoy" defeated Captain Nigun's Sunlight Scripture without killing a soul. Marquis Raeven watches suspiciously from the balcony. | The diplomatic heist — a god-tier lich validated by the kingdom's champion, the Social HP ticking from 9/10 to 6/10 as the King wavers. | Ains, Sebas Tian, King Ramposa III, Gazef Stronoff, Marquis Raeven, Captain Nigun | `ca197e7b` — `Ains shy lich` (Ains) <br>`(fallback)` — `campaign-level avatar.png` (Gazef / Ramposa / Sebas stand-ins) |
| 3 | `world_item_raid_iron_mine` | `[157, 167]` | Morning mist clings to the jagged maws of the Iron-Mine Ruins. Ains (Layer-2 Sorcerer Queen mask) moves through the fog with Sebas Tian and the silver-clad Vanguard knights. The pavilion erupts in a blinding white pulse as the **Crown of Wisdom** resists; Ains orders the "Mirror Wall" defense and casts **Dominate Person** on High Priest Kalle to compel him to surrender the World Item. The mist swallows the evidence of the sovereign intrusion. | The first time Ains drops the Saintly Envoy mask and operates openly as a Level-12 arcane anchor — the moment the Slane Theocracy learns the "envoy" is hunting them. | Ains, Sebas Tian, High Priest Kalle, Silver Vanguard (10 knights), Albedo (referenced) | `ca197e7b` — `Ains shy lich` (Ains) <br>`(fallback)` — `campaign-level avatar.png` (Sebas / Kalle stand-ins) |
| 4 | `imperial_audit_e_rantel` | `[317, 327]` | Morning light glints off E-Rantel's southern gate as Ains's procession arrives. In the central square the Imperial Auditor (Fluder Paradyne's inner circle) raises the **Orb of Imperial Discernment** against her. The Mask holds (DC 26), the Orb verifies Level 12, and the Auditor goes hollow. Ains turns her back and enters the Merchant Guild to force a total grain monopoly, then steps onto the gilded balcony to pacify Chenier's mob with a "Saintly" miracle. | The single moment Ains publicly announces her Level-12 presence to a hostile empire — turning the Auditor's own weapon into a surrender document. | Ains, Sebas Tian, Imperial Auditor, Baron Chenier, Fluder Paradyne (referenced), Zesshi Zetsumei (referenced) | `ca197e7b` — `Ains shy lich` (Ains) <br>`(fallback)` — `campaign-level avatar.png` (Sebas / Auditor / Chenier stand-ins) |
| 5 | `three_finger_ridge_dragons` | `[353, 355]` | Midday wind whistles through the sharp crags of Three-Finger Ridge. Ains (Layer-1 mask) climbs with the half-elf ranger Rianon, the human Grom, and the demi-human mage Elos of the "Azure Crows." On Day 160 the party reaches the **Cloud-Sea Terrace**; Ains spots surgically-deleted "Absolute Stillness" markers — a high-tier YGGDRASIL "Silent Step" signature. A Young Silver Dragon (Lvl 9) named **Silvershard** spirals up from the mist and lands with a thunderous impact. | The first face-to-face with a Council-State dragon lord while masked as a Level-6 adventurer — Ains reading YGGDRASIL tech-signature trails on a Wild-Magic peak. | Ains (masked), Albedo (masked as adventurer companion), Rianon (half-elf ranger Lvl 6), Grom, Elos, Silvershard (Young Silver Dragon Lvl 9) | `ca197e7b` — `Ains shy lich` (Ains — used despite mask as canonical avatar) <br>`(fallback)` — `campaign-level avatar.png` (Albedo / Rianon / Silvershard stand-ins) |

---

## Diversity Checklist (5 visual buckets covered)

| Bucket | Scene # | Slug | ✓ |
|---|---|---|---|
| Indoor | 1 | `treasury_audit_opening` | ✓ Council Chamber, mahogany table, floating arcane crystals |
| Political | 2 | `royal_audience_re_estize` | ✓ Throne Room, Sovereign's Covenant, Social HP challenge |
| Dramatic battle | 3 | `world_item_raid_iron_mine` | ✓ Iron-Mine Ruins, Mirror Wall + Dominate Person combat |
| Outdoor | 4 | `imperial_audit_e_rantel` | ✓ Open central square + southern gate of E-Rantel |
| Environmental-puzzle | 5 | `three_finger_ridge_dragons` | ✓ Cloud-Sea Terrace, Silent-Step tracking, dragon encounter |

All 5 visual buckets covered. No overlap between scenes (entry ranges are disjoint and span entries 7 → 355).

---

## Notes for the parent agent

- **Strict last-20 → only 1 campaign → all 5 scenes from Overlord shy lich.** The previous pick list (`/tmp/avatar_scene_gen/02_scene_candidates.md` v1) drew from 5 different campaigns out of a 262-campaign 50+ pool. Under the corrected strict rule — *last 20 by `last_played` desc → filter to ≥50 entries → pick 5 scenes* — **only `Overlord shy lich` (id8=`JQeI1Aq5`, 364 entries)** qualifies. The 4 other campaigns (Valeria, SWTOR Tenebria, Visenya v9, Supergirl) are not in the last-20 window and are excluded. **All 5 new scenes are Overlord-shy-lich and the earlier multi-campaign picks are removed.**
- **Per-NPC portrait situation (unchanged from v1).** Firestore still exposes **only the campaign-level `avatar.png`**: `https://storage.googleapis.com/worldarchitecture-ai-frontend-static/campaign_avatars/vnLp2G3m21PJL6kxcuAqmWSOtm73/0lZBWUBP4Na3u4XjArOd/avatar.png`. There are **no per-NPC portraits** stored for `Sebas Tian`, `Demiurge`, `Albedo`, `Gazef Stronoff`, `King Ramposa III`, `Marquis Raeven`, `Captain Nigun`, `High Priest Kalle`, `Imperial Auditor`, `Baron Chenier`, `Rianon`, `Grom`, `Elos`, or `Silvershard`. Drive dedupe manifest confirms: **the only character-name match is `ca197e7b_ains_shy_lich` (Ains).**
- **Avatar coverage tally:** **5 direct Drive character-name matches** (all 5 scenes use `ca197e7b_ains_shy_lich` for Ains) vs **5 falls-back-to-campaign-avatar** (one per scene for non-Ains NPCs). **No adjacent-archetype Drive avatars were found that match Overlord characters** (Sebas / Demiurge / Albedo / Gazef — none present in `drive_avatars_deduped.jsonl`). The 7 avatars used in earlier Step 4 are non-Overlord (Sariel variants, Alexiel variants, Arion variants, Nocturne variants, Visenya, Valeria) so they cannot be repurposed for Overlord characters.
- **Entry-range spacing** — Scene 1 ~10, Scene 2 ~80, Scene 3 ~160, Scene 4 ~320, Scene 5 end-of-campaign (~320-355, adjusted inward because the campaign ends at 363 and the last thematic scene is the dragon encounter).
- **Story-text dumps** for each candidate campaign are saved at `/tmp/avatar_scene_gen/raw_<id8>.jsonl` for the parent agent to verify or re-scope the scene windows.
- **Step 4 outputs** — 10 Grok + Gemini rewrites are saved verbatim at `/tmp/avatar_scene_gen/scenes/<slug>/{grok,gemini}.md` (5 folders × 2 variants). These were copied verbatim into the wiki by Step 5 RE-DO.
- **`npc_data` is rich** (named NPCs with relationships, classes, sometimes MBTI/alignment labels) but does NOT carry portrait URLs. If portrait generation is desired, the named NPCs above are the source list.