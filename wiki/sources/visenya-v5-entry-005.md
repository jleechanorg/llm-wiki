---
title: "Visenya V5 — Scene 005"
type: source
tags: [campaign, scene, visenya-v5]
last_updated: 2026-04-12
scene_number: 5
scene_total: 258
source_file: /tmp/campaign_downloads_v2/
---

## Scene 005 Summary

============================================================ [Timestamp: 298 AC, 3rd Moon, Day 14, 14:30:00 Location: Maegor's Holdfast Gardens, King's Landing Status: Lvl 1 Apex Weaver | HP: 8/8 | XP: 150/300 | Gold: 10gp]  Game Master: ━━━ Equipment summary ━━━ ▸ Armor:   • Indigo Velvet Gown (AC 13) ▸ Miscellaneous:   • Lemon cake (half-eaten)  God Mode: try to fix my st ats. in game state and use the right type  • Your “System: Sorry, an error occurred fetching stats.” is the frontend fallba

## Key Details

- **Location:** Maegor's Holdfast Gardens, King's Landing
- **Level hint:** 1
- **Word count:** 166
- **Campaign:** [[Visenya V5]]
- **Entry:** [[visenya-v5-entry-005]]

---

## Full Scene Content

============================================================
[Timestamp: 298 AC, 3rd Moon, Day 14, 14:30:00
Location: Maegor's Holdfast Gardens, King's Landing
Status: Lvl 1 Apex Weaver | HP: 8/8 | XP: 150/300 | Gold: 10gp]

Game Master:
━━━ Equipment summary ━━━
▸ Armor:
  • Indigo Velvet Gown (AC 13)
▸ Miscellaneous:
  • Lemon cake (half-eaten)

God Mode:
try to fix my st ats. in game state and use the right type

• Your “System: Sorry, an error occurred fetching stats.” is the frontend fallback when GET /api/
  campaigns/ARrfJ39LhNEi5rcGq1c7/stats returns non-200 (it’s returning 500). The Cloud Run error
  is:

  - 🔥🔴 Get stats error: unhashable type: 'list'
  - Traceback points to mvp_site/stats_display.py:798 inside build_stats_summary (val_normalized
    in {"expertise", 2}), i.e. it’s trying to treat a list as a hashable value.
  - This is triggered by your Firestore shape: player_character_data.skills is {"proficiencies":
    [...]} (a dict whose value is a list), but the stats builder’s “skills dict” path assumes a
    mapping like {skill_name: true/"expertise"/2} and iterates skills_data.items(); when it hits
    ("proficiencies", [..]), it blows up.

============================================================
