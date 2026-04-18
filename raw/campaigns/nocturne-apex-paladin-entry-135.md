---
title: "Nocturne Apex Paladin — Scene 135"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 135
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 135 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You have provided a `GOD_ASK_STATE` command, along with your current `CURRENT GAME STATE` JSON object, and asked: "what do you have?"  I have received and reviewed the `CURRENT GAME STATE` JSON you provided.  Upon a thorough comparison of the `CURRENT GAME STATE` you sent to me in `SEQ_ID: 274` against the most accurate and up-to-date state (which includes all successfully completed actions, di

## Key Details

- **Word count:** 2455
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-135]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You have provided a `GOD_ASK_STATE` command, along with your current `CURRENT GAME STATE` JSON object, and asked: "what do you have?"

I have received and reviewed the `CURRENT GAME STATE` JSON you provided.

Upon a thorough comparison of the `CURRENT GAME STATE` you sent to me in `SEQ_ID: 274` against the most accurate and up-to-date state (which includes all successfully completed actions, discoveries, and ruleset changes proposed in previous turns up to `SEQ_ID: 259`), I must report a critical discrepancy:

**The `CURRENT GAME STATE` you are providing is severely outdated and does not reflect many of the crucial changes, character progression, and world developments that have occurred and were previously agreed upon or proposed for update.**

This is the root cause of the narrative loops and inconsistencies we have been experiencing. My apologies for the technical difficulty this presents on your end.

Here are the specific, major discrepancies between the `CURRENT GAME STATE` you sent and what the state *should* be, based on our campaign's agreed-upon progression:

**Key Discrepancies in the `CURRENT GAME STATE` from `SEQ_ID: 274`:**

1.  **Nocturne's Character Data (`player_character_data`):**
    *   **Aptitudes:** `potential` is still numerical (e.g., `18`, `20`) instead of `potential_coefficient` (e.g., `4`, `5`). This means the Dynamic Aptitude System's core potential is not reflected.
    *   **Resources:**
        *   `xp_current`: `6420` (Should be `8010` after journal deciphering in `SEQ_ID: 259`).
        *   `gold`: `630` (Should be `1230` after receiving payment from Kaelen in `SEQ_ID: 243`).
        *   `ep_current`: `36` (Correct, but previous fluctuations were not retained).
    *   **Inventory:**
        *   `plate_armor`: Still present (`Masterwork Plate Armor`) instead of `Masterwork Shadow-Weave Half Plate` (as established in `SEQ_ID: 82` and stored).
        *   `longsword`: Still has `attack_bonus: 1`, `damage_bonus: 1` (Should be `0` after gear calibration in `SEQ_ID: 82`).
        *   `potion_of_greater_healing`: Still `3` (Should be `potion_of_healing: 3` after gear calibration in `SEQ_ID: 82`).
        *   **Missing many crucial acquired items:** `darkwood_casket`, `cipher_key`, `shortsword` (looted), `light_crossbow` (looted), `quiver_bolts` (looted), `duty_roster_oakhaven_patrol`, `masterwork_lockpicks`, `oakhaven_area_map`, `silver_dog_whistle`.
    *   **Class Features (`class_features`):** Still lists original Paladin features (`divine_smite_base_ep_cost`, `divine_sense_uses`, `lay_on_hands_pool_per_level`) instead of the **Oath of Self-Perfection (Apex Predator)** features (e.g., `perfected_strike_base_ep_cost`, `aura_of_unyielding_dominance`, `apex_senses`, `willpower_infusion`, `channel_divinity_options`, and the `feats` key containing `great_weapon_master`).
    *   **`current_location`:** Is `Forest Edge near Man Tibbet's Farm (Message Sent)` (Should be `The Black Lily's Den (Baldur's Gate)` after deciphering journal in `SEQ_ID: 259`).
    *   **`secret_myers_briggs_type`:** Missing for Nocturne (Should be `INTJ` from `SEQ_ID: 35`).

2.  **World Data (`world_data`):**
    *   **NPC Statuses (`world_data.npcs`):**
        *   Tibbet family (Man Tibbet, wife, children) and Widow Elara are still listed as `Subdued, Unconscious, Bound, Sacked, Outside` or `Consolidated at Tibbet's Farm`. **They should all be `Transported by Kaelen's team`** (from `SEQ_ID: 249`).
        *   `oakhaven_mastiff_1`, `oakhaven_mastiff_2`, `road_patrol_1`, `road_patrol_2`, `man_tibbet_farm_guard_1`, `man_tibbet_farm_guard_2`: Statuses are not fully updated to `Looted, Concealed` or `Neutralized`.
        *   **Missing `secret_myers_briggs_type` for many NPCs** (Julian, Lysandra, Marcus, Seraphina, Theron, Kaelen Flinn).
    *   **Locations (`world_data.locations`):**
        *   `man_tibbet_farm.defenses_observed.magical_ward.status`: Still missing `Disabled` status.
        *   **Missing `the_black_lilys_den` hideout location** data (from `SEQ_ID: 82`).
    *   **Custom Campaign State (`custom_campaign_state`):**
        *   `first_contract.scouting_status`: `Consolidated and Concealed` (should be `Journal Deciphered, Full Conspiracy Revealed` from `SEQ_ID: 259`).
        *   `first_contract.all_captives_status`: `Consolidated and Concealed` (should be `Transported by Kaelen's team`).
        *   `first_contract.all_captives_location`: `Forest near Man Tibbet's Farm (Concealed)` (should be `En route with Kaelen's transport team`).
        *   `first_contract.transport_status`: Still missing (`Kaelen's transport team collected captives`).
        *   `first_contract.status`: Still missing (`Completed (Acquisition & Transport)`).
        *   **Missing `underdark_rendezvous_info`**.
        *   **Missing `durins_folly_conspiracy`**.
        *   **Missing `darkwood_casket_info`**.
        *   **Missing `obsidian_shard_info`**.
        *   Missing updates to `new_terms_proposed` and `kaelen_contact_status`.

---

**This is a critical issue that directly prevents me from maintaining narrative consistency and fulfilling my role as the Master Game Weaver.** I cannot accurately simulate the world, character resources, or NPC states if the `CURRENT GAME STATE` I receive is not a true reflection of the ongoing game.

**To proceed, it is absolutely essential that you manually apply the JSON data within the `GOD_MODE_UPDATE_STATE` block below to the `CURRENT GAME STATE` on your system.** This is the *most complete and accurate cumulative state* that incorporates *all* successful actions, discoveries, and progression up to the end of `SEQ_ID: 259` (where Nocturne finished deciphering the journal in her hideout).

Once you have manually applied this, please send me the **fully updated and corrected `CURRENT GAME STATE` JSON block** in your *next prompt*. I will then verify if the changes have been retained across all relevant fields, and we can finally continue the campaign from that point.

My apologies again for the repeated errors and the disruption to gameplay caused by this persistent technical inconsistency.

```json
GOD_MODE_UPDATE_STATE: {
  "game_state_version": 2,
  "player_character_data": {
    "age": 16,
    "expertise_tags": [
      "Military Strategy",
      "Ancient Lore (Forgotten Realms)",
      "Court Intrigue",
      "Anatomy & Weak Points (Combat)"
    ],
    "inventory": {
      "shadowfell_maps": {
        "description": "Detailed charts of the Shadowfell, with specific locations marked with tiny, glowing glyphs.",
        "name": "Topographical Maps of the Shadowfell"
      },
      "dagger": {
        "damage_die": "1d4 piercing",
        "properties": [
          "finesse",
          "light",
          "thrown (range 20/60)"
        ],
        "name": "Masterwork Dagger"
      },
      "gold": 1230,
      "bag_of_holding": {
        "capacity_cubic_feet": 64,
        "capacity_lbs": 500,
        "name": "Bag of Holding"
      },
      "shield": {
        "defense_bonus": 2,
        "name": "Masterwork Shield"
      },
      "family_signet_ring": {
        "description": "Subtle symbol of House Valerius",
        "name": "Concealed Family Signet Ring"
      },
      "noble_garb": {
        "effect": "Subtly obscures physical attractiveness",
        "name": "Noble's Garb (Concealing)"
      },
      "orbs_of_scrying": {
        "description": "Three small, perfectly spherical magical orbs designed for remote observation.",
        "name": "Orbs of Scrying (x3)"
      },
      "letter_house_durins_folly": {
        "content_read": false,
        "description": "Sealed letter with the crest of House Durin's Folly, addressed to 'Tibbet, Keeper of the Eastern March'.",
        "name": "Letter from House Durin's Folly"
      },
      "potion_of_healing": 3,
      "obsidian_shard": {
        "description": "Pulsates with faint, malevolent arcane energy. Found in a lead-lined box.",
        "arcane_signature": "Malevolent, arcane",
        "name": "Intricately Carved Obsidian Shard"
      },
      "longsword": {
        "attack_bonus": 0,
        "damage_bonus": 0,
        "versatile_damage_die": "1d10 slashing",
        "damage_die": "1d8 slashing",
        "name": "Masterwork Longsword"
      },
      "ledger_tibbet_farm": {
        "content_read": true,
        "description": "Hidden entries detailing weekly payments to 'Security Contingency Fund' and 'Arcane Oversight' from an account linked to a lesser noble family tied to House Durin's Folly.",
        "name": "Man Tibbet's Ledger"
      },
      "masterwork_shadow_weave_half_plate": {
        "name": "Masterwork Shadow-Weave Half Plate",
        "defense_bonus": 5,
        "dr": 1,
        "stealth_advantage_dim_dark": true,
        "stealth_disadvantage": false
      },
      "shortsword": 4,
      "light_crossbow": 4,
      "quiver_bolts": 4,
      "duty_roster_oakhaven_patrol": {
        "name": "Oakhaven Patrol Duty Roster",
        "description": "Simple parchment, outlines patrol times and routes, confirms 2 guards on this specific route.",
        "content_read": true
      },
      "masterwork_lockpicks": {
        "name": "Masterwork Lockpicks",
        "description": "A well-maintained set of lockpicking tools."
      },
      "oakhaven_area_map": {
        "name": "Detailed Oakhaven Area Map",
        "description": "Map of Oakhaven and immediate area, with routes and points of interest circled in red ink."
      },
      "silver_dog_whistle": {
        "name": "Silver Dog Whistle",
        "description": "Finely crafted, produces a sound barely audible to humans but loud to trained animals."
      },
      "darkwood_casket": {
        "name": "Darkwood Casket",
        "description": "Small, perfectly crafted darkwood casket, inscribed with faint, writhing runes associated with death cults. Radiates ancient, malevolent chill."
      },
      "cipher_key": {
        "name": "Cipher Key",
        "description": "A scroll containing the key to the ciphered journal.",
        "content_read": true
      },
      "journal_elara": {
        "name": "Widow Elara's Journal",
        "description": "Small, leather-bound, old. Spidery, precise script within."
      },
      "locket_tarnished": {
        "name": "Tarnished Silver Locket",
        "description": "Old, dull silver, faded engraving of a stylized flower."
      }
    },
    "aptitudes": {
      "coordination": {
        "score": 14,
        "potential": 18,
        "potential_coefficient": 4
      },
      "wisdom": {
        "score": 16,
        "potential": 20,
        "potential_coefficient": 5
      },
      "physique": {
        "score": 16,
        "potential": 20,
        "potential_coefficient": 5
      },
      "intelligence": {
        "score": 18,
        "potential": 22,
        "potential_coefficient": 5
      },
      "health": {
        "score": 15,
        "potential": 19,
        "potential_coefficient": 4
      }
    },
    "level": 5,
    "personality_traits": {
      "agreeableness": 1,
      "conscientiousness": 4,
      "extraversion": 3,
      "neuroticism": 4,
      "openness": 5
    },
    "class_features": {
      "fighting_style": "Battle-Hardened",
      "extra_attack": 2,
      "perfected_strike_base_ep_cost": 5,
      "perfected_strike_extra_ep_per_d8": 2,
      "aura_of_unyielding_dominance_range": 10,
      "aura_of_unyielding_dominance_effect": "Self and allies within range gain Advantage on checks to resist Frightened or Charmed. Enemies within range have Disadvantage on checks to resist your Intimidation attempts.",
      "apex_senses_uses": "1 + Wisdom Modifier",
      "willpower_infusion_pool_per_level": 5,
      "willpower_infusion_healing_cost": 1,
      "willpower_infusion_fatigue_cost": 5,
      "willpower_infusion_aptitude_buff_cost": 10,
      "channel_divinity_uses_per_rest": "Short or Long Rest",
      "channel_divinity_options": [
        "Flawless Opening",
        "Unchecked Ambition"
      ],
      "feats": {
        "great_weapon_master": {
          "name": "Great Weapon Master",
          "shove_aside_effect": "Before you make a melee attack with a heavy weapon you are proficient with, you can choose to take a -5 penalty to the attack roll. If the attack hits, you add +10 to the attack's damage.",
          "cleave_effect": "When you score a critical hit with a melee weapon or reduce a creature to 0 hit points with one, you can make one additional melee weapon attack as a bonus action on the same turn."
        }
      },
      "apex_senses_uses_current": 3,
      "channel_divinity_uses_remaining": 1
    },
    "proficiencies": {
      "tools": [],
      "weapons": [
        "Simple Weapons",
        "Martial Weapons"
      ],
      "armor": [
        "All Armor",
        "Shields"
      ],
      "saving_throws_advantage": [
        "Wisdom",
        "Health"
      ]
    },
    "resources": {
      "ep_max": 36,
      "xp_current": 8010,
      "cp_per_turn": 3,
      "hp_max": 43,
      "willpower_infusion_pool_current": 25,
      "willpower_infusion_pool_max": 25,
      "combat_prowess_bonus": 3,
      "hp_current": 43,
      "ep_current": 36
    },
    "current_location": "The Black Lily's Den (Baldur's Gate)",
    "name": "Nocturne",
    "secret_myers_briggs_type": "INTJ"
  },
  "world_data": {
    "npcs": {
      "valerius_marcus": {
        "age": 27,
        "secret_goal": "To pay off massive gambling debt to powerful, secretive criminal figure without family knowledge.",
        "role": "Nominal head of family's investments in Lower City entertainment/gambling",
        "relationship_to_pc_initial": "Indifferent. Ignored her, slight relief she's gone (less competition).",
        "personality": "Boisterous, charming, outwardly friendly, privately hedonist and gambler, avoids direct conflict.",
        "is_pc_sibling": true,
        "name": "Valerius, Marcus",
        "secret_myers_briggs_type": "ESFP"
      },
      "man_tibbet_child_1": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 5,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 1,
            "score": 8
          },
          "wisdom": {
            "potential_coefficient": 1,
            "score": 8
          },
          "physique": {
            "potential_coefficient": 1,
            "score": 8
          },
          "intelligence": {
            "potential_coefficient": 1,
            "score": 8
          },
          "health": {
            "potential_coefficient": 1,
            "score": 8
          }
        },
        "level": 0,
        "hp_current": 5,
        "name": "Man Tibbet's Child 1"
      },
      "man_tibbet_wife": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 10,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 2,
            "score": 10
          },
          "wisdom": {
            "potential_coefficient": 2,
            "score": 10
          },
          "physique": {
            "potential_coefficient": 2,
            "score": 10
          },
          "intelligence": {
            "potential_coefficient": 2,
            "score": 10
          },
          "health": {
            "potential_coefficient": 2,
            "score": 10
          }
        },
        "secret_myers_briggs_type": "ISFJ",
        "level": 1,
        "hp_current": 10,
        "name": "Man Tibbet's Wife"
      },
      "man_tibbet": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 10,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 2,
            "score": 10
          },
          "wisdom": {
            "potential_coefficient": 2,
            "score": 10
          },
          "physique": {
            "potential_coefficient": 2,
            "score": 12
          },
          "intelligence": {
            "potential_coefficient": 2,
            "score": 10
          },
          "health": {
            "potential_coefficient": 2,
            "score": 10
          }
        },
        "secret_myers_briggs_type": "ISTJ",
        "level": 1,
        "hp_current": 10,
        "name": "Man Tibbet"
      },
      "valerius_seraphina": {
        "age": 24,
        "secret_goal": "To establish Helm's undeniable authority as primary protector of Baldur's Gate, push for extreme measures against threats.",
        "role": "High Priestess within the Temple of Helm in Baldur's Gate",
        "relationship_to_pc_initial": "Righteous loathing. Views Nocturne's evil as affront to faith, divine justice. Would actively work against her.",
        "personality": "Zealous, devout, unyielding in faith to Helm, morally rigid, sees world in stark good/evil.",
        "is_pc_sibling": true,
        "name": "Valerius, Seraphina",
        "secret_myers_briggs_type": "ESTJ"
      },
      "valerius_theron": {
        "age": 20,
        "secret_goal": "To expose hidden corruption within Flaming Fist ranks he dimly perceives, fearing it will tarnish honor.",
        "role": "Squire to high-ranking Flaming Fist officer",
        "relationship_to_pc_initial": "Deeply conflicted. Too young/idealist to fully understand. Secretly wonders if exile fair. Might be swayed by direct appeal.",
        "personality": "Naive, impressionable, fierce unrefined loyalty, admired Nocturne's talent but horrified by methods.",
        "is_pc_sibling": true,
        "name": "Valerius, Theron",
        "secret_myers_briggs_type": "ISFJ"
      },
      "kaelen_flinn": {
        "age": 35,
        "level": 6,
        "relationship_to_pc_initial": "Contact for first contract.",
        "name": "Kaelen \"Whisper\" Flinn",
        "personality": "Wiry, nervous, darting eyes, utterly amoral, values efficiency and discretion.",
        "role": "Mid-level operative for the Shadow Weavers",
        "secret_myers_briggs_type": "ISTP"
      },
      "widow_elara": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 5,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 1,
            "score": 8
          },
          "wisdom": {
            "potential_coefficient": 2,
            "score": 12
          },
          "physique": {
            "potential_coefficient": 1,
            "score": 8
          },
          "intelligence": {
            "potential_coefficient": 2,
            "score": 10
          },
          "health": {
            "potential_coefficient": 1,
            "score": 8
          }
        },
        "secret_myers_briggs_type": "INFJ",
        "level": 0,
        "hp_current": 5,
        "name": "Widow Elara"
      },
      "man_tibbet_child_3": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 5,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 1,
            "score": 8
          },
          "wisdom": {
            "potential_coefficient": 1,
            "score": 8
          },
          "physique": {
            "potential_coefficient": 1,
            "score": 8
          },
          "intelligence": {
            "potential_coefficient": 1,
            "score": 8
          },
          "health": {
            "potential_coefficient": 1,
            "score": 8
          }
        },
        "level": 0,
        "hp_current": 5,
        "name": "Man Tibbet's Child 3"
      },
      "valerius_lysandra": {
        "age": 29,
        "secret_goal": "To uncover and master forgotten Valerius family rituals/ancient magic to 'purify' or strengthen lineage.",
        "role": "Head Librarian/Archivist for House Valerius",
        "relationship_to_pc_initial": "Distant but not hostile. Detached fascination with Nocturne's brilliance, views evil as chaotic.",
        "personality": "Reserved, highly intelligent, fiercely loyal to family name, gifted arcane scholar, values knowledge and order.",
        "is_pc_sibling": true,
        "name": "Valerius, Lysandra",
        "secret_myers_briggs_type": "INTP"
      },
      "valerius_julian": {
        "age": 32,
        "secret_goal": "To consolidate absolute control over family assets, potentially eliminating other siblings or father; elevate House Valerius power.",
        "role": "Heir apparent to House Valerius",
        "relationship_to_pc_initial": "Strained. Primary instigator of her exile.",
        "personality": "Meticulous, ambitious, overtly charming but calculating, intensely jealous of Nocturne's talent, cloaks ruthlessness in civility.",
        "is_pc_sibling": true,
        "name": "Valerius, Julian",
        "secret_myers_briggs_type": "INTJ"
      },
      "man_tibbet_child_2": {
        "current_status": "Transported by Kaelen's team",
        "is_aware_of_pc": true,
        "hp_max": 5,
        "defense": 10,
        "is_hostile": false,
        "aptitudes": {
          "coordination": {
            "potential_coefficient": 1,
            "score": 8
          },
          "wisdom": {
            "potential_coefficient": 1,
            "score": 8
          },
          "physique": {
            "potential_coefficient": 1,
            "score": 8
          },
          "intelligence": {
            "potential_coefficient": 1,
            "score": 8
          },
          "health": {
            "potential_coefficient": 1,
            "score": 8
          }
        },
        "level": 0,
        "hp_current": 5,
        "name": "Man Tibbet's Child 2"
      },
      "oakhaven_mastiff_1": {
        "name": "Oakhaven Mastiff 1",
        "level": 2,
        "hp_current": 0,
        "hp_max": 13,
        "defense": 12,
        "aptitudes": {
          "physique": {
            "potential_coefficient": 3,
            "score": 14
          },
          "coordination": {
            "potential_coefficient": 2,
            "score": 12
          },
          "health": {
            "potential_coefficient": 2,
            "score": 13
          },
          "intelligence": {
            "potential_coefficient": 1,
            "score": 6
          },
          "wisdom": {
            "potential_coefficient": 3,
            "score": 13
          }
        },
        "is_hostile": false,
        "is_aware_of_pc": true,
        "status_after_combat": "Looted, Concealed"
      },
      "oakhaven_mastiff_2": {
        "name": "Oakhaven Mastiff 2",
        "level": 2,
        "hp_current": 0,
        "hp_max": 13,
        "defense": 12,
        "aptitudes": {
          "physique": {
            "potential_coefficient": 3,
            "score": 14
          },
          "coordination": {
            "potential_coefficient": 2,
            "score": 12
          },
          "health": {
            "potential_coefficient": 2,
            "score": 13
          },
          "intelligence": {
            "potential_coefficient": 1,
            "score": 6
          },
          "wisdom": {
            "potential_coefficient": 3,
            "score": 13
          }
        },
        "is_hostile": false,
        "is_aware_of_pc": true,
        "status_after_combat": "Looted, Concealed"
      },
      "oakhaven_villager_1": {
        "name": "Oakhaven Villager (Burly Man)",
        "level": 1,
        "hp_current": 10,
        "hp_max": 10,
        "defense": 10,
        "aptitudes": {
          "physique": {
            "potential_coefficient": 2,
            "score": 12
          },
          "coordination": {
            "potential_coefficient": 2,
            "score": 10
          },
          "health": {
            "potential_coefficient": 2,
            "score": 10
          },
          "intelligence": {
            "potential_coefficient": 2,
            "score": 10
          },
          "wisdom": {
            "potential_coefficient": 2,
            "score": 10
          }
        },
        "is_hostile": false,
        "is_aware_of_pc": true,
        "current_status": "Terrified, Ordered to Flee"
      },
      "oakhaven_villager_2": {
        "name": "Oakhaven Villager (Young Woman)",
        "level": 1,
        "hp_current": 10,
        "hp_max": 10,
        "defense": 10,
        "aptitudes": {
          "physique": {
            "potential_coefficient": 2,
            "score": 10
          },
          "coordination": {
            "potential_coefficient": 2,
            "score": 10
          },
          "health": {
            "potential_coefficient": 2,
            "score": 10
          },
          "intelligence": {
            "potential_coefficient": 2,
            "score": 10
          },
          "wisdom": {
            "potential_coefficient": 2,
            

God Mode:
give me just the update state command for god mode only with corrections

God Mode:
give me just the update state command for god mode only with corrections

God Mode:
give me just the update state command for god mode only with corrections

============================================================
