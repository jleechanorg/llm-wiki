---
title: "Avatar Scene Generation Batch — Overlord-only (2026-08-14, scope-corrected)"
type: query
tags: [campaign, worldarchitect, scene-rewrite, avatar-scene-gen-2026-08-14, overlord-shy-lich]
date: 2026-08-14
parent_query: avatar-scene-gen-2026-08-14
related:
  - "[[wa-campaign-last-20-2026-08-14]]"
  - "[[wa-avatar-drive-dedupe-2026-08-14]]"
pipeline_date: 2026-08-14
scenes_total: 5
llms_total: 2
outputs_total: 10
qualifying_campaigns: 1
qualifying_campaign: Overlord shy lich (JQeI1Aq5, 364 entries)
scope_note: "Strict last-20 (by last_played desc) → filter ≥50 entries → 1 campaign qualifies. All 5 scenes from that single campaign. Earlier wider-pool picks (Overlord Carne / Valeria Razor's Edge / SWTOR Tenebria / Visenya Red Keep / Supergirl ICC) discarded."
grok:
  model: grok-4.3
  endpoint: xai
gemini:
  model: gemini-2.5-flash
  endpoint: vertex-ai
  auth_note: "GEMINI_API_KEY reported leaked by Google; fell back to Vertex AI on worldarchitecture-ai project with gcloud auth print-access-token bearer. Helper at /tmp/avatar_scene_gen/gemini_call.py."
drive_folder_id: 1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc-
drive_unique_avatars: 132
---

# Avatar Scene Generation Batch — Overlord-only (2026-08-14, scope-corrected)

Five campaign scenes, two LLMs each = 10 outputs. This batch is **strict-last-20 scope**: only `Overlord shy lich` (id8 `JQeI1Aq5`, 364 entries) passes the ≥50-entry threshold among the user's last-20 campaigns. All 5 scenes therefore come from that single campaign — earlier multi-campaign picks (Valeria / SWTOR Tenebria / Visenya / Supergirl) are **discarded**, and their wiki folders + 5 entity pages were removed in Step 5 RE-DO.

## Scope correction

1. **Discovery** — jleechan's last-20 campaigns from WA Firestore (`vnLp2G3m21PJL6kxcuAqmWSOtm73`), filter to ≥50 entries. Only **1** (`Overlord shy lich`) qualifies. The earlier wider-pool picks were taken from a 262-campaign 50+ pool and are now removed. See [[wa-campaign-last-20-2026-08-14]].
2. **Avatar sourcing** — unchanged. 132 unique avatars deduplicated from the personal Google Drive folder `1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc-` (141 raw → 132 after SHA-256 dedupe; 3 collisions). See [[wa-avatar-drive-dedupe-2026-08-14]].
3. **Cross-reference** — character → Drive filename joins in `03_xref_characters.json`. Only `ca197e7b_ains_shy_lich` matches an Overlord character (Ains).
4. **Generation** — two parallel LLM workers (Grok subagent + Gemini subagent) rewrote each scene. Grok used xai's `grok-4.3`. Gemini used `gemini-2.5-flash` over Vertex AI because the configured `GEMINI_API_KEY` was reported leaked and `gws`/`gemini` CLI auth paths failed.
5. **Step 5 (this page set)** — verbatim wiki ingest of all 10 outputs (5 Overlord scenes × 2 LLMs); only 1 entity page needed (`ca197e7b-ains-shy-lich`) since all 5 scenes use Ains as the character-of-record.

## Scene Index

| # | Scene slug | Campaign (id8) | Entry range | Avatars referenced | Words (Grok / Gemini) |
|---|---|---|---|---|---|
| 1 | [[treasury_audit_opening]] | Overlord shy lich (`JQeI1Aq5`) | 7–9 | `ca197e7b_ains_shy_lich` | ~414 / ~466 |
| 2 | [[royal_audience_re_estize]] | Overlord shy lich (`JQeI1Aq5`) | 79–93 | `ca197e7b_ains_shy_lich` | ~536 / ~446 |
| 3 | [[world_item_raid_iron_mine]] | Overlord shy lich (`JQeI1Aq5`) | 157–167 | `ca197e7b_ains_shy_lich` | ~499 / ~512 |
| 4 | [[imperial_audit_e_rantel]] | Overlord shy lich (`JQeI1Aq5`) | 317–327 | `ca197e7b_ains_shy_lich` | ~486 / ~516 |
| 5 | [[three_finger_ridge_dragons]] | Overlord shy lich (`JQeI1Aq5`) | 353–355 | `ca197e7b_ains_shy_lich` | ~450 / ~576 |

All 5 scenes share the **Overlord × D&D 5e isekai** IP, the `JQeI1Aq5` campaign, and the `ca197e7b_ains_shy_lich` Drive avatar. Entry ranges are disjoint (7 → 355) and span the early, mid, and late portions of the 364-entry campaign.

## Diversity

| Scene | Setting | Tone |
|---|---|---|
| treasury_audit_opening | Indoor (Nazarick Council Chamber) | Political economy opening — god-queen forced into wheat-decisions |
| royal_audience_re_estize | Indoor (Re-Estize Throne Room) | Diplomatic heist — Social HP 9/10 → 6/10 |
| world_item_raid_iron_mine | Outdoor (Iron-Mine Ruins, morning mist) | First time Ains drops the Saintly Envoy mask openly |
| imperial_audit_e_rantel | Outdoor (E-Rantel central square + southern gate) | Public L12 announcement to a hostile empire |
| three_finger_ridge_dragons | Outdoor (Three-Finger Ridge / Cloud-Sea Terrace) | First face-to-face with a Council-State dragon lord |

Indoor: 1, 2. Outdoor: 3, 4, 5. All five carry strong environmental description. Five disjoint scene beats from a single 364-entry campaign.

## Model & Endpoint Notes

- **Grok** — `grok-4.3` via xai API. Output is prose-first, slightly more internal-monologue (e.g. Ains' "ledger page" metaphor in scene 1).
- **Gemini** — `gemini-2.5-flash` via Vertex AI on `worldarchitecture-ai` project, location `us-central1`, using `gcloud auth print-access-token` as bearer. The configured `GEMINI_API_KEY` was reported leaked by Google (`403 PERMISSION_DENIED`); the configured `gemini-3.6-flash-high` model returned `404 ModelNotFoundError`. Gemini rewrites are slightly more verbose on the "you," second-person framing.

Both LLM outputs are preserved **verbatim** in their per-scene folders. No editing, no normalization, no merged-diff version.

## Related Pages

- Source: [[wa-campaign-last-20-2026-08-14]] — scope-corrected discovery (1 of last-20 campaigns ≥ 50 entries)
- Source: [[wa-avatar-drive-dedupe-2026-08-14]] — 141 → 132 unique avatars from Drive folder `1dM4qeRcKTJmRZVq1bB8wTgPhdZNgazc-`
- 1 Drive-avatar entity used: [[ca197e7b-ains-shy-lich]]
- Drive rclone reference: [[reference-gdrive-upload-via-rclone-own-client]] (not modified by this batch)