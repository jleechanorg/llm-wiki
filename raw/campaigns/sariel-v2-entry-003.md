---
title: "Sariel V2 — Scene 003"
type: source
tags: [campaign, scene, sariel-v2]
last_updated: 2026-04-12
scene_number: 3
scene_total: 252
source_file: /tmp/campaign_downloads_v2/
---

## Scene 003 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. I have processed your directives and will now establish the definitive canon for our campaign, integrating all your choices.  ### **Unified Canon Decisions:**  *   **Timeline:** The campaign begins on **Kythorn, Day 2, Year 11 of the New Peace**, which is the day after the Battle of the Sacrifice Fields and Alexiel's death. This is now the official starting point. *   **Sariel's Starting Level:

## Key Details

- **Location:** Deep Archives, Zenith Spire, Aeterna.
- **Word count:** 1704
- **Campaign:** [[Sariel V2]]
- **Entry:** [[sariel-v2-entry-003]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. I have processed your directives and will now establish the definitive canon for our campaign, integrating all your choices.

### **Unified Canon Decisions:**

*   **Timeline:** The campaign begins on **Kythorn, Day 2, Year 11 of the New Peace**, which is the day after the Battle of the Sacrifice Fields and Alexiel's death. This is now the official starting point.
*   **Sariel's Starting Level:** Sariel begins the campaign at Level 1.
*   **Rowan's Surname:** Your companion's name is officially **Rowan Thorne**.
*   **Commander Kyra Vian's Status:** Commander Kyra Vian **is dead**, having fallen heroically during the final battle against Lucifer's forces.

### **Major Retcon: Character Ages & Implications**

Per your directive, the character ages have been significantly adjusted. This has important narrative implications:

*   **Sariel is now 15:** This makes her trauma even more profound. She is not a young woman, but a child who has been tortured and witnessed her mother's death. Her isolation and the court's scorn are directed at someone even more vulnerable, amplifying her tragedy and making her intellectual brilliance even more remarkable.
*   **The Twins are now 18:** Cassian and Valerius are now young men on the cusp of true adulthood. Their grief and anger are not those of older, established figures, but of young lords grappling with a world-shattering loss at a formative age. This makes Cassian's rage more volatile and Valerius's retreat into cold logic more poignant.
*   **Companion Age Adjustment:** To maintain the "childhood friend" dynamic, I have adjusted the ages of Cressida and Rowan to be closer to Sariel's. Cressida is now 16, and Rowan is also 16. This makes their loyalty and friendship more grounded in a shared youth.

### **CANONICAL STATE CORRECTION**

The following `STATE_UPDATES_PROPOSED` block reflects all of these canonical changes. This information now supersedes the initial state proposed in `SEQ_ID: 1`.

[STATE_UPDATES_PROPOSED]
{
  "game_state_version": 1,
  "player_character_data": {
    "name": "Sariel Arcanus",
    "age": 15,
    "archetype": "The Grieving Scholar / The Bearer of a Terrible Secret",
    "alignment": "True Neutral",
    "mbti": "INTP",
    "level": 1,
    "xp_current": 0,
    "xp_to_next": 300,
    "hp_max": 6,
    "hp_current": 6,
    "stats": {
      "STR": 9,
      "DEX": 12,
      "CON": 10,
      "INT": 18,
      "WIS": 16,
      "CHA": 13
    },
    "skills": [
      "Arcana",
      "History",
      "Investigation",
      "Insight"
    ],
    "inventory": {
      "gold": 10,
      "items": {
        "mourning_robes": {
          "name": "Simple Mourning Robes"
        },
        "dataslate": {
          "name": "Personal Data-slate"
        }
      }
    },
    "backstory_summary": "Daughter of the legendary Alexiel and Prince Artorius. At age 15, she was kidnapped by the warlord Mordan. Under duress from torture, she revealed the secret of her mother's absolute moral vow to protect children. She then witnessed Mordan use this information to trap her mother, forcing Alexiel to sacrifice her own life to stop a demonic ritual and save Sariel. She is now consumed by guilt, believing her weakness directly caused her mother's death."
  },
  "npc_data": {
    "Alexiel Arcanus (Deceased)": {
      "name": "Alexiel Arcanus",
      "age_at_death": 30,
      "role": "Magister of the Watch, Lady of House Arcanus, the 'Mortal Queen'.",
      "archetype": "The God in Hiding / The Sacrificed Mother",
      "mbti": "INTJ",
      "alignment": "Lawful Neutral",
      "public_legacy": "The legendary war hero who ended the Host Wars. Seen as a martyr who made the ultimate sacrifice at the Battle of the Sacrifice Fields to stop a profane ritual and save hundreds of innocent children, including her own daughter.",
      "secret_truth": "A hidden demigod of immense power who chose to live as a mortal. Her greatest secret was a Nullification Field she could project. Her death was the result of a trap specifically designed by the warlord Mordan to exploit her single, absolute moral code: the protection of children."
    },
    "Cassian Arcanus": {
      "name": "Prince Cassian Arcanus",
      "age": 18,
      "role": "Heir to House Arcanus, Twin Prince.",
      "archetype": "The Avenging Son",
      "mbti": "ESTJ",
      "alignment": "Lawful Neutral",
      "status": "Consumed by grief and rage over his mother's death. He directs his fury at the remnants of Mordan's forces and the Shattered Host, but secretly holds Sariel responsible for being the bait in the trap."
    },
    "Valerius Arcanus": {
      "name": "Prince Valerius Arcanus",
      "age": 18,
      "role": "Twin Prince.",
      "archetype": "The Cold Analyst",
      "mbti": "ISTP",
      "alignment": "True Neutral",
      "status": "Has retreated into cold, analytical silence. He processes his mother's death as a strategic failure and is dissecting every report from the battle, trying to understand how the legendary Magister could have been outmaneuvered. His silence is more damning to Sariel than Cassian's rage."
    },
    "Titus val Raziel": {
      "name": "High Commander Titus val Raziel",
      "role": "Leader of the Triumvirate, High Commander of the Imperial Legions.",
      "archetype": "The Grieving Guardian",
      "mbti": "ESTP",
      "alignment": "Lawful Good",
      "status": "Devastated by the death of Alexiel, whom he had come to see as a sister. He is now the sole protector of her children and legacy, trying to hold the shaken Imperium together."
    },
    "Cressida Valeriana": {
      "name": "Lady Cressida Valeriana",
      "age": 16,
      "role": "Sariel's lady-in-waiting and closest friend.",
      "archetype": "The Loyal Politician",
      "mbti": "ENFJ",
      "status": "Fiercely protective of Sariel, acting as her shield against the whispers of the court."
    },
    "Gideon Vance": {
      "name": "Ser Gideon Vance",
      "age": 25,
      "role": "Sworn shield to Sariel, member of the Starfall Guard.",
      "archetype": "The Stoic Protector",
      "mbti": "ISTJ",
      "status": "Haunted by his failure to protect Sariel from being kidnapped. His loyalty is now absolute."
    },
    "Rowan Thorne": {
      "name": "Rowan Thorne",
      "age": 16,
      "role": "Sariel's childhood friend and fellow scholar.",
      "archetype": "The Moral Compass",
      "mbti": "INFP",
      "status": "Worried for Sariel's emotional state, he tries to offer academic distraction and simple friendship in the face of overwhelming grief."
    }
  },
  "world_data": {
    "political_situation": "The Imperium is in mourning. The 'Mortal Queen', Alexiel Arcanus, is dead. The court is a viper's nest of factions seeking to exploit the vacuum. High Commander Titus struggles to maintain order. The hero's death has cemented her legend, but the political reality is one of instability and fear.",
    "current_location": "Sariel's Chambers, House Arcanus Wing, Zenith Spire, Aeterna."
  },
  "world_time": {
    "year": 11,
    "era": "New Peace",
    "month": "Kythorn",
    "day": 2,
    "hour": 9,
    "minute": 0,
    "second": 0
  },
  "custom_campaign_state": {
    "premise": "The day after her legendary mother sacrificed herself to save her, Sariel Arcanus must navigate a web of grief, guilt, and political intrigue, all while bearing the secret that she was the one who broke under torture and revealed the weakness that led to her mother's death.",
    "active_missions": [],
    "core_memories": [
      "Alexiel, a secret magic-user, defected from Lucifer's Host.",
      "Alexiel married Prince Artorius, son of the Lord Regent Raziel.",
      "Alexiel and Raziel orchestrated the Starfall Gambit, ending the war with Lucifer.",
      "Alexiel ascended to demigod status but chose to live as the 'Mortal Queen', hiding her power.",
      "At age 15, Sariel was kidnapped by the warlord Mordan.",
      "Under duress, Sariel revealed her mother's unbreakable moral code about protecting children.",
      "Mordan used this knowledge to set a trap at the Battle of the Sacrifice Fields, using hundreds of captive children as leverage.",
      "Alexiel, faced with an impossible choice, sacrificed her own life by overloading her Nullification Field to stop the ritual and save Sariel and the other children."
    ]
  },
  "migration_status": "FRESH_INSTALL"
}
[END_STATE_UPDATES_PROPOSED]

All conflicts are resolved. We will now resume the story.

***

[Mode: STORY MODE]
Timestamp: Year of the New Peace, 11. Month of Kythorn, Day 2. 10:35 AM.
Location: Deep Archives, Zenith Spire, Aeterna.
Key Game Stats: Level 2 (XP: 1000/2700), Gold: 10gp, HP: 10/10

Kantos’s explanation settled into the silence of the vault, a final, chilling piece of the puzzle. The Imperium's disdain for Nulls, their dismissal of them as genetically flawed and powerless, was the perfect soil for your mother's lifelong deception to take root. She had hidden in plain sight, her terrifying power masked by the court's own arrogance and prejudice.

You finally understood the full scope of her genius. The journals had given you the 'how'—the horrifying science of her creation. But they could not give you the 'what'. They could not show you the look in her eyes during that final battle, the truth of the "Joyful Predator" unleashed. Only one person could.

Your mind, now sharp and clear, cut through the fog of grief and confusion. Your objective was no longer abstract; it was a person. Sergeant Kaelan. The Starfall Patient.

You looked at the old Magister, your Starlit Eyes burning with a new, unshakeable resolve. The time for academic discovery was over. It was time to find the witness.

"Magister," you stated, your voice devoid of its earlier hesitation, now holding the quiet, firm authority of a princess of the realm. "You have guarded these secrets for decades. You have done your duty. Now, I must do mine."

You met his gaze, leaving no room for argument. "Take me to the Quiet Ward. Take me to Sergeant Kaelan. I will see the truth for myself."

Kantos paled, his ancient hands trembling. He opened his mouth to protest, to warn you of the dangers, of Raziel's explicit orders, of the horrors that lay in the sanitarium's deepest levels. But he saw the look on your face—the same relentless, unyielding determination he had once seen in your mother's eyes. He knew, with a profound and weary certainty, that he could no more stop you than he could stop a rising tide.

He gave a slow, defeated nod, the weight of his decision settling upon him like a shroud. "As you wish, Princess," he rasped. "But we will need help. The Quiet Ward is not a library. It is a fortress. And you will need your shield."

---
**--- PLANNING BLOCK ---**
What would you like to do?
1.  **[Summon Gideon]:** Agree with Kantos. Send a message to summon Ser Gideon Vance, your sworn shield.
2.  **[Summon Cressida]:** Send for Lady Cressida, believing her political cunning will be needed to navigate the sanitarium's bureaucracy.
3.  **[Summon Rowan]:** Send for Rowan, hoping his kindness and healing knowledge might be of use in such a dark place.
4.  **[Assemble the Team]:** Decide to bring all three of your companions, believing you will need all their skills for what lies ahead.
5.  **[Other]:** You can also describe a different action you'd like to take.

God Mode:
Ask Kantos about mothers power. How can I acquire it? Does nullifcation need to be done on babies or could Ido it and posses magic and null power

============================================================
