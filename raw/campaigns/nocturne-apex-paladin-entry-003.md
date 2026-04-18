---
title: "Nocturne Apex Paladin — Scene 003"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 3
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 003 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You've provided a `DM Note` (treated as `GOD MODE` in this instance) instructing me to always show the aptitude score and a "hidden aptitude potential factor usually 1-5 number" during character creation/setup.  I understand you'd like the display of Aptitudes to be more granular regarding potential.  However, the current Destiny ruleset (2.2.D Aptitude Potential) defines "Aptitude Potential" a

## Key Details

- **Word count:** 1539
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-003]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You've provided a `DM Note` (treated as `GOD MODE` in this instance) instructing me to always show the aptitude score and a "hidden aptitude potential factor usually 1-5 number" during character creation/setup.

I understand you'd like the display of Aptitudes to be more granular regarding potential.

However, the current Destiny ruleset (2.2.D Aptitude Potential) defines "Aptitude Potential" as a numerical score (e.g., 20, 18, 19, 22), not a separate "factor" in the 1-5 range.

Could you please clarify what this "1-5 number" potential factor represents?
*   Is it a new meta-statistic you'd like to introduce, separate from the existing numerical Aptitude Potential score (e.g., "Physique: 16 (Potential: 20, Factor: 4)")? If so, how should this factor be derived or interpreted (e.g., does a Factor 5 mean the Potential Score is always 20+, a Factor 1 mean it's 10-12, etc.)?
*   Or were you referring to a desire for the existing Aptitude Potential scores to somehow be represented qualitatively within a 1-5 scale, even if the underlying number is higher?

Once clarified, I will adjust the character sheet display protocol accordingly for future character setups and re-display Nocturne's sheet with the requested format.

In the meantime, the previously generated character data for Nocturne, the noble houses, factions, and siblings, along with the first contract, stands as the proposed initial state of the campaign. Do you have any other feedback or desire to adjust any of these generated elements before we move to the story's commencement?

[STATE_UPDATES_PROPOSED]
{
  "game_state_version": 2,
  "player_character_data": {
    "name": "Nocturne",
    "level": 5,
    "age": 16,
    "aptitudes": {
      "physique": { "score": 16, "potential": 20 },
      "coordination": { "score": 14, "potential": 18 },
      "health": { "score": 15, "potential": 19 },
      "intelligence": { "score": 18, "potential": 22 },
      "wisdom": { "score": 16, "potential": 20 }
    },
    "resources": {
      "hp_current": 43,
      "hp_max": 43,
      "ep_current": 36,
      "ep_max": 36,
      "cp_per_turn": 3,
      "combat_prowess_bonus": 3,
      "lay_on_hands_pool_current": 25,
      "lay_on_hands_pool_max": 25
    },
    "personality_traits": {
      "openness": 5,
      "conscientiousness": 4,
      "extraversion": 3,
      "agreeableness": 1,
      "neuroticism": 4
    },
    "proficiencies": {
      "armor": ["All Armor", "Shields"],
      "weapons": ["Simple Weapons", "Martial Weapons"],
      "tools": [],
      "saving_throws_advantage": ["Wisdom", "Health"]
    },
    "expertise_tags": [
      "Military Strategy",
      "Ancient Lore (Forgotten Realms)",
      "Court Intrigue",
      "Anatomy & Weak Points (Combat)"
    ],
    "class_features": {
      "divine_sense_uses": 4,
      "lay_on_hands_pool_per_level": 5,
      "fighting_style": "Battle-Hardened",
      "divine_smite_base_ep_cost": 5,
      "divine_smite_extra_ep_per_d8": 2,
      "extra_attack": 2
    },
    "inventory": {
      "plate_armor": { "name": "Masterwork Plate Armor", "defense_bonus": 8, "dr": 3, "stealth_disadvantage": true },
      "longsword": { "name": "Masterwork Longsword", "damage_die": "1d8 slashing", "versatile_damage_die": "1d10 slashing", "attack_bonus": 1, "damage_bonus": 1 },
      "shield": { "name": "Masterwork Shield", "defense_bonus": 2 },
      "dagger": { "name": "Masterwork Dagger", "damage_die": "1d4 piercing", "properties": ["finesse", "light", "thrown (range 20/60)"] },
      "bag_of_holding": { "name": "Bag of Holding", "capacity_lbs": 500, "capacity_cubic_feet": 64 },
      "gold": 500,
      "noble_garb": { "name": "Noble's Garb (Concealing)", "effect": "Subtly obscures physical attractiveness" },
      "family_signet_ring": { "name": "Concealed Family Signet Ring", "description": "Subtle symbol of House Valerius" },
      "potion_of_greater_healing": 3
    }
  },
  "world_data": {
    "noble_houses": {
      "house_valerius": {
        "name": "House Valerius",
        "sigil": "A coiled serpent striking through a stylized rose",
        "ideology": "Power through influence, ruthless pragmatism, maintaining a veneer of respectability. Family above all else.",
        "influence_area": "Economic and political influence within the Upper City and Parliament of Peers, significant investments in trade and infrastructure.",
        "public_perception": "Respected and feared. Known for keen intellect and sharp business dealings.",
        "relations": {
          "ironhand_mercantile_conglomerate": "Alliance (discreet)",
          "house_theron": "Rivalry (intense)",
          "parliament_of_peers": "Neutral/Complex (strained diplomacy)"
        },
        "key_figurehead": {
          "name": "Lord Cassian Valerius",
          "level": "Unknown (Strategist)",
          "age": 55,
          "relationship_to_pc": "Father, orchestrated exile"
        }
      },
      "house_theron": {
        "name": "House Theron",
        "sigil": "A soaring falcon clutching a lightning bolt",
        "ideology": "Martial prowess, honor (outwardly), and expansion of territory/influence through direct means.",
        "influence_area": "Extensive landholdings and military resources around Baldur's Gate. Key military voice in Parliament.",
        "public_perception": "Respected for military strength and tradition, but seen as arrogant and brutish.",
        "relations": {
          "flaming_fist": "Alliance (strong)",
          "house_valerius": "Rivalry (long-standing)",
          "harbor_masters_guild": "Neutral/Complex (wary, transactional)"
        }
      },
      "house_durins_folly": {
        "name": "House Durin's Folly",
        "sigil": "A stylized pickaxe crossed with a coin stack",
        "ideology": "Unmatched craftsmanship, financial stability, and maintaining dwarven traditions.",
        "influence_area": "Manufacturing, mining, and banking within the city.",
        "public_perception": "Trusted for reliability and quality, but insular and traditional.",
        "relations": {
          "ironhand_mercantile_conglomerate": "Alliance (close)",
          "house_valerius": "Rivalry (undercurrents)",
          "parliament_of_peers": "Neutral/Complex (pragmatic)"
        }
      },
      "the_shadow_weavers_power": {
        "name": "The Shadow Weavers",
        "symbol": "A stylized spiderweb with a single, watchful eye at its center",
        "ideology": "Control of the city's underworld through fear, information, and exploitation. Profit above all.",
        "influence_area": "Lower City and Undercity, with tendrils into Upper City corruption. Controls smuggling, slavery, protection rackets.",
        "public_perception": "Feared by common folk, rumored by privileged.",
        "relations": {
          "guild_of_coin": "Alliance (loose, transactional)",
          "emerald_claw": "Rivalry (constant skirmishes)",
          "flaming_fist": "Enemy (actively seeks to undermine)",
          "parliament_of_peers": "Neutral/Complex (uneasy, bribed peace)"
        }
      },
      "the_obsidian_vigil": {
        "name": "The Obsidian Vigil",
        "sigil": "A stylized, unblinking obsidian eye within a shattered arcane circle",
        "ideology": "Preservation of ancient knowledge, monitoring magical threats, guiding arcane balance.",
        "influence_area": "Hidden throughout Sword Coast, discreet presence in Baldur's Gate.",
        "public_perception": "Mostly unknown, whispered among scholars and mages.",
        "relations": {
          "candlekeep_sages": "Alliance (hidden)"
        }
      }
    },
    "factions": {
      "flaming_fist": {
        "name": "The Flaming Fist",
        "description": "City Guard/Military."
      },
      "ironhand_mercantile_conglomerate": {
        "name": "Ironhand Mercantile Conglomerate",
        "description": "Powerful merchant guild."
      },
      "harbor_masters_guild": {
        "name": "Harbor Master's Guild",
        "description": "Controls port traffic and trade."
      },
      "guild_of_coin": {
        "name": "Guild of Coin",
        "description": "Minor thieves/smugglers."
      },
      "emerald_claw": {
        "name": "Emerald Claw",
        "description": "Traditional thieves' guild."
      },
      "parliament_of_peers": {
        "name": "The Parliament of Peers",
        "description": "Governing body of Baldur's Gate."
      },
      "watchful_order_of_magists_and_protectors": {
        "name": "The Watchful Order of Magists & Protectors",
        "description": "Official mage guild."
      },
      "priests_of_helm": {
        "name": "The Priests of Helm",
        "description": "Prominent religious order."
      },
      "knights_of_the_shield": {
        "name": "The Knights of the Shield",
        "description": "Secret society tied to merchants, influence peddlers."
      },
      "zhentarim": {
        "name": "The Zhentarim",
        "description": "Black Network; spies, mercenaries, traders."
      },
      "cult_of_the_dead_three": {
        "name": "The Cult of the Dead Three (Remnants)",
        "description": "Dispersed but dangerous, seeking new power."
      },
      "the_bloom": {
        "name": "The Bloom (Elven Druidic Circle)",
        "description": "Hidden group protecting nature around the city."
      },
      "iron_consuls": {
        "name": "The Iron Consuls",
        "description": "Former Steel Watch remnants, now independent contractors/mercenaries."
      },
      "grey_hands": {
        "name": "The Grey Hands",
        "description": "Adventuring company, sometimes rivals, sometimes allies."
      },
      "bhaalspawn_cult_fringe": {
        "name": "The Bhaalspawn Cult (Fringe Elements)",
        "description": "Small, dangerous groups trying to revive the Bhaal legacy."
      },
      "gondian_artisans": {
        "name": "The Gondian Artisans",
        "description": "Skilled crafters and inventors."
      },
      "society_of_brilliance": {
        "name": "The Society of Brilliance",
        "description": "Philosophers and scholars (often eccentric)."
      },
      "underdark_guides": {
        "name": "The Underdark Guides",
        "description": "Specialized guides for the dangerous routes beneath the city."
      },
      "guild_of_the_green_bottle": {
        "name": "The Guild of the Green Bottle",
        "description": "Alchemists and potion brewers."
      },
      "dockside_drifters": {
        "name": "The Dockside Drifters",
        "description": "Loosely organized group of transient laborers and informants."
      }
    },
    "npcs": {
      "valerius_julian": {
        "name": "Valerius, Julian",
        "age": 32,
        "role": "Heir apparent to House Valerius",
        "personality": "Meticulous, ambitious, overtly charming but calculating, intensely jealous of Nocturne's talent, cloaks ruthlessness in civility.",
        "relationship_to_pc_initial": "Strained. Primary instigator of her exile.",
        "secret_goal": "To consolidate absolute control over family assets, potentially eliminating other siblings or father; elevate House Valerius power.",
        "is_pc_sibling": true
      },
      "valerius_lysandra": {
        "name": "Valerius, Lysandra",
        "age": 29,
        "role": "Head Librarian/Archivist for House Valerius",
        "personality": "Reserved, highly intelligent, fiercely loyal to family name, gifted arcane scholar, values knowledge and order.",
        "relationship_to_pc_initial": "Distant but not hostile. Detached fascination with Nocturne's brilliance, views evil as chaotic.",
        "secret_goal": "To uncover and master forgotten Valerius family rituals/ancient magic to 'purify' or strengthen lineage.",
        "is_pc_sibling": true
      },
      "valerius_marcus": {
        "name": "Valerius, Marcus",
        "age": 27,
        "role": "Nominal head of family's investments in Lower City entertainment/gambling",
        "personality": "Boisterous, charming, outwardly friendly, privately hedonist and gambler, avoids direct conflict.",
        "relationship_to_pc_initial": "Indifferent. Ignored her, slight relief she's gone (less competition).",
        "secret_goal": "To pay off massive gambling debt to powerful, secretive criminal figure without family knowledge.",
        "is_pc_sibling": true
      },
      "valerius_seraphina": {
        "name": "Valerius, Seraphina",
        "age": 24,
        "role": "High Priestess within the Temple of Helm in Baldur's Gate",
        "personality": "Zealous, devout, unyielding in faith to Helm, morally rigid, sees world in stark good/evil.",
        "relationship_to_pc_initial": "Righteous loathing. Views Nocturne's evil as affront to faith, divine justice. Would actively work against her.",
        "secret_goal": "To establish Helm's undeniable authority as primary protector of Baldur's Gate, push for extreme measures against threats.",
        "is_pc_sibling": true
      },
      "valerius_theron": {
        "name": "Valerius, Theron",
        "age": 20,
        "role": "Squire to high-ranking Flaming Fist officer",
        "personality": "Naive, impressionable, fierce unrefined loyalty, admired Nocturne's talent but horrified by methods.",
        "relationship_to_pc_initial": "Deeply conflicted. Too young/idealist to fully understand. Secretly wonders if exile fair. Might be swayed by direct appeal.",
        "secret_goal": "To expose hidden corruption within Flaming Fist ranks he dimly perceives, fearing it will tarnish honor.",
        "is_pc_sibling": true
      },
      "kaelen_flinn": {
        "name": "Kaelen \"Whisper\" Flinn",
        "level": 6,
        "age": 35,
        "role": "Mid-level operative for the Shadow Weavers",
        "personality": "Wiry, nervous, darting eyes, utterly amoral, values efficiency and discretion.",
        "relationship_to_pc_initial": "Contact for first contract."
      }
    },
    "custom_campaign_state": {
      "first_contract": {
        "objective": "Kidnap peasants to sell as slaves",
        "syndicate": "The Shadow Weavers",
        "contact_npc": "kaelen_flinn",
        "target_hamlet": "Oakhaven",
        "target_hamlet_location": "A few miles east of Baldur's Gate",
        "buyers_implied": "New, powerful, secretive slaver ring from the Underdark"
      }
    }
  },
  "last_state_update_timestamp": "2025-06-21T07:00:09.383866+00:00",
  "migration_status": "NO_LEGACY_DATA"
}
[END_STATE_UPDATES_PROPOSED]

God Mode:
**D. Aptitude Potential (Hidden Stat):**
    *   **Definition:** Each Aptitude also has an associated "Aptitude Potential," a hidden numerical value representing a character's innate talent and ultimate capacity for development in that Aptitude.

============================================================
