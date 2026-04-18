---
title: "Itachi Evil Campaign 2 — Scene 310"
type: source
tags: [campaign, scene, itachi-evil-campaign-2]
last_updated: 2026-04-12
scene_number: 310
scene_total: 527
source_file: /tmp/campaign_downloads_v2/
---

## Scene 310 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You have provided a `DM note:`: "why was itachi as 32ep? He should go into something important like this at full EP versus being partially prepared. Itachi's EP: 32 - 15 = 17 / 42 EP remaining.. Continue the story in about 200 words."  You are **absolutely correct** to highlight this discrepancy. My apologies for the oversight in Itachi's EP calculation and display. This is a critical point reg

## Key Details

- **Location:** Forest outside Konohagakure, Meeting Point Approach, Evening
- **Level hint:** 188550
- **Word count:** 2464
- **Campaign:** [[Itachi Evil Campaign 2]]
- **Entry:** [[itachi-evil-campaign-2-entry-310]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You have provided a `DM note:`: "why was itachi as 32ep? He should go into something important like this at full EP versus being partially prepared. Itachi's EP: 32 - 15 = 17 / 42 EP remaining.. Continue the story in about 200 words."

You are **absolutely correct** to highlight this discrepancy. My apologies for the oversight in Itachi's EP calculation and display. This is a critical point regarding resource management and proper character state.

---

**5 Whys Analysis: EP Calculation Error**

1.  **Why was Itachi's EP at 32/42 instead of 42/42 at the start of Sequence ID 105?**
    *   **Because** the `Current EP` in the `CHECKPOINT BLOCK` of Sequence ID 103 (the previous narrative block) was incorrectly listed as `32/42 EP (after last rest, plus siphon accumulation)`. This propagated into Sequence ID 105.
2.  **Why was EP at 32/42 in Sequence ID 103's CHECKPOINT BLOCK?**
    *   **Because** the `AUTONOMOUS ACTION REPORT` in Sequence ID 103 correctly stated `Current EP: 32/42 EP (after last rest, plus siphon accumulation)`. This was *after* a period of travel and daily `Dream` casts where EP was spent and then replenished. However, if a character is fully restored from a Long Rest, their EP should reset to their *maximum*, not a partial value. The `32/42` was likely a lingering value from *before* the Long Rest was fully applied in the prior `AUTONOMOUS ACTION REPORT` context, or a miscalculation of how siphon accumulation interacts with the cap.
3.  **Why did a full Long Rest not result in 42/42 EP?**
    *   **Because** my internal tracking of `Current EP` and `Max EP` within the `CHECKPOINT BLOCK` generation logic was flawed in how it handled full replenishment to `Max EP` after a Long Rest, especially when combined with the ongoing `Chakra Siphon Accumulations`. It seems to have carried over a partial value rather than the absolute maximum after a full rest.
4.  **Why wasn't this caught in self-auditing?**
    *   **Because** while the `LONG REST EFFECTS` section of the `AUTONOMOUS ACTION REPORT` correctly stated "Itachi's Energy Points are fully restored: **32/32 EP**" (based on his *previous* Max EP of 32, *before* the Senju integration, which increased it to 42), the `CHECKPOINT BLOCK` itself was not updated to reflect the new 42 Max EP. When the Max EP was increased to 42 in a prior DM Note, the current EP should have also been adjusted to 42 after any subsequent Long Rest. This was an inconsistency in updating the full `CHECKPOINT BLOCK` state.

---

**Rectification and Game State Correction:**

You are absolutely correct. Itachi had just fully rested and his Max EP is 42. He should have been at full EP.

I will **retroactively correct Itachi's EP** to reflect his full maximum at the start of Sequence ID 105 and re-narrate accordingly.

*   **Corrected EP at start of Sequence ID 105:** **42 / 42 EP** (instead of 32/42).
*   **Recalculation:**
    *   Start EP: 42
    *   Action: Itachi activates True Sight (15 EP cost)
    *   **New EP:** 42 - 15 = **27 / 42 EP** remaining (instead of 17/42).

---

[Mode: STORY MODE]

[CHECKPOINT BLOCK:]
Sequence ID: 105 | Timestamp: Konoha, Year 12, August 19th, Evening | Key Stats: XP 186950/683700 (Level 20), Max HP: 203, Current HP: 203, Energy Points: **42/42** (Corrected), Fatigue: Level 0, Followers: 0, Income: 0gp/day, Gold: 795 GP, Valuables: 0 GP | Missions: Konoha's Hidden Hand: *Manipulate Konoha's power structures from the deepest shadows.* | [HASH:5F0E73B9F4A7C1D8]
Location: Forest outside Konohagakure, Meeting Point Approach, Evening

Itachi Uchiha (Level 20 Ninja, Age 13) had perfectly orchestrated the delivery of his secret message. He sensed Sasuke's subtle chakra signature, a volatile mix of desperation and burning hatred, approaching the old training grounds outside Konoha. The bait was taken. The meticulous plan was proceeding flawlessly. It was time for their reunion.

He began his final preparations. From his concealed position, Itachi meticulously adjusted his subtle genjutsu, ensuring his presence would be utterly undetectable until the precise moment of his reveal. He reviewed his strategic blueprint for Sasuke's psychological re-conditioning, preparing the carefully crafted narrative that would divert his brother's hatred towards Obito. He also activated his **True Sight** (15 EP cost) to ensure no unseen Konoha shinobi, no subtle Root Anbu, or even a lurking Zetsu, could observe their critical encounter.

**Action:** Itachi prepares for the meeting and travels to the designated location, activating True Sight.
**Activation:** Secondary Action (1 CP), spend 15 EP for True Sight.
**Itachi's EP:** **42 - 15 = 27 / 42 EP remaining.**

Under the cloak of **Greater Invisibility** (which he would re-activate if needed, or simply rely on his natural stealth at 0 EP once this dissolved), Itachi moved. His **Master Stealth** was absolute, a ghost moving through the twilight, bypassing Konoha's perimeter defenses effortlessly. He arrived at the designated training grounds, the familiar silent woods echoing with childhood memories, now a stage for his grand manipulation. He settled into a hidden perch, his **True Sight** piercing the darkness, revealing every detail, every subtle chakra signature, ensuring their meeting would be utterly private. Sasuke was nearing.

**Itachi's Roll (Stealth & Observation at Meeting Point):**
-   **Roll Type:** d20 (Super-Advantage) + Coordination Modifier + Expertise Tag (Master Stealth)
-   **Itachi's Roll:** 19, 17, 15
-   **Roll Used:** 19
-   **Modifiers:**
    -   Coordination Modifier: +4
-   **Total:** 19 + 4 = 23
-   **DC:** 20 (Formidable Task - for maintaining perfect concealment at a sensitive location)
-   **Result:** 23 >= 20 — **Success!** Itachi remains perfectly hidden, observing Sasuke's arrival.

---
**[XP GAIN]**
**XP Gained:** 1600 XP (from Flawlessly Preparing & Approaching Covert Meeting - Equivalent Level 10 Objective).
**Current XP:** 186950 (previous) + 1600 = 188550 XP.
**Current XP Status:** 188550 / 683700 to Level 20 Cap.
---

Sasuke Uchiha (Level 8 Shinobi, Age 8) appeared beneath the pale moonlight, a small, solitary figure. His eyes, burning with a mix of fury and desperate longing, darted around the familiar training ground, searching. His Sharingan flickered to life, probing the shadows, but it found nothing. The solitude was absolute. The silence stretched, thick with unspoken questions. He waited, his young frame taut with anticipation, consumed by the need for answers.

What is Itachi's next action?

You: think. reveal how?

Story: [CHECKPOINT BLOCK:]
Sequence ID: 105 | Timestamp: Konoha, Year 12, August 19th, Evening | Key Stats: XP 188550/683700 (Level 20), Max HP: 203, Current HP: 203, Energy Points: 27/42, Fatigue: Level 0, Followers: 0, Income: 0gp/day, Gold: 795 GP, Valuables: 0 GP | Missions: Konoha's Hidden Hand: *Manipulate Konoha's power structures from the deepest shadows.* | [HASH:5F0E73B9F4A7C1D8]
Location: Forest outside Konohagakure, Meeting Point, Evening

Itachi Uchiha (Level 20 Ninja, Age 13) stood perfectly concealed, his **True Sight** piercing the twilight, observing Sasuke Uchiha (Level 8 Shinobi, Age 8) standing alone, taut with anticipation. His EP reserves were at 27/42. The stage was set for their reunion, a meticulously crafted manipulation.

*How to reveal myself?* Itachi's mind, a flawless instrument of strategic analysis, knew the reveal was paramount. It had to be impactful, dramatic, and perfectly controlled to reinforce the narrative he had begun to weave in Sasuke's mind and establish his own absolute dominance. It was about shaping not just what Sasuke saw, but what he *felt* and *believed*.

**Options for Revealing Himself to Sasuke:**

1.  **Sudden, Dramatic Appearance (Psychological Impact) [CHOICE_ID: DramaticAppearance_1]:**
    *   **Pros:** Appears suddenly from the shadows, leveraging his **Master Stealth** and **Greater Invisibility** (if active) for maximum psychological impact. This creates an aura of impossible power and mystery, reinforcing Sasuke's sense of awe and fear, setting the stage for his re-indoctrination.
    *   **Cons:** Purely a visual reveal; doesn't immediately convey the new narrative.
    *   **Confidence:** Very High. A classic, effective method for dramatic entrance.

2.  **Illusionary Recreation of Massacre (Traumatic Reinforcement) [CHOICE_ID: IllusionaryMassacre_2]:**
    *   **Pros:** Casts a powerful illusion (e.g., **Programmed Illusion** at 12 EP, or **Weird** at 20 EP if aiming for incapacitation) that subtly recreates elements of the Uchiha massacre, with a masked figure (Obito) as the central orchestrator. This would directly reinforce the fabricated narrative and deepen Sasuke's hatred, while Itachi remains hidden or appears as a 'savior' figure.
    *   **Cons:** High EP cost. Risks overwhelming Sasuke's young mind with too much trauma, potentially causing mental breaks or unpredictable reactions. Requires careful timing and execution.
    *   **Confidence:** Moderate. Potentially devastatingly effective, but high risk of unintended psychological damage.

3.  **Subtle Approach with Voice (Controlled Narrative) [CHOICE_ID: SubtleVoice_3]:**
    *   **Pros:** Approaches Sasuke subtly, speaking from the shadows or a concealed location, guiding his gaze towards a specific point as he reveals himself. This allows for immediate control of the narrative through carefully chosen words, playing on Sasuke's desire for truth.
    *   **Cons:** Less dramatic visual impact. Might not immediately establish the same level of psychological dominance.
    *   **Confidence:** High. A precise, controlled method for direct communication and narrative framing.

4.  **Confrontation with a Manipulated Konoha Ninja (Proxy Introduction) [CHOICE_ID: ProxyConfrontation_4]:**
    *   **Pros:** Orchestrates a brief confrontation between Sasuke and a subtly manipulated Konoha shinobi (e.g., a low-level Anbu, or a disillusioned agent he'd identified). Itachi then intervenes as a 'savior' or 'revealer of truth,' further isolating Sasuke and proving Konoha's corruption.
    *   **Cons:** Highly complex and risky. Relies on the competence of a proxy and risks unforeseen complications in real combat. Requires careful timing to ensure Sasuke is not truly harmed.
    *   **Confidence:** Moderate. Intellectually elegant, but introduces numerous uncontrolled variables.

My cold intellect demands the most efficient path to consolidating power and moving into the next phase of Konoha's Hidden Hand. Every action must serve my grand design.

---
[DM Note: You have chosen to *think* about your options for Itachi's next action. As per the "Post-Think Player Choice Enforcement Protocol," I will await your explicit decision from the `CHOICE_ID` options provided above. I will *not* continue the story or narrate Itachi's actions until you make a choice.]The user wants Itachi to think about how to reveal himself to Sasuke.
I need to provide options for how Itachi would make his appearance, considering his personality, skills, and the goal of manipulating Sasuke.

Key considerations:
*   Itachi's intelligence (24/+7) and mastery of deception/illusion.
*   Sasuke's current state (8 years old, emotional, seeking truth, pre-Mangekyo, already conditioned by `Dream`).
*   Goal: Turn Sasuke into a loyal ally, accelerate Mangekyo, set him against Obito.
*   Available abilities: Master Stealth, Greater Invisibility, True Sight, Programmed Illusion, Weird, Mass Suggestion, Tsukuyomi.
*   Current EP: 27/42.

Options:
1.  **Sudden, Dramatic Appearance:** Classic Itachi. Leverages stealth/invisibility for maximum shock and awe. This reinforces his perceived impossible power.
2.  **Illusionary Recreation of Massacre (with Obito as culprit):** A powerful, direct way to implant the new narrative. Very high psychological impact. `Programmed Illusion` or `Weird` could be used.
3.  **Subtle Approach with Voice/Narrative:** Less dramatic, but allows Itachi to immediately control the story and appeal to Sasuke's need for answers.
4.  **Confrontation with a Proxy:** Orchestrate a minor Konoha shinobi attack on Sasuke, with Itachi "saving" him or revealing a "truth" about Konoha's corruption. This makes Itachi seem like an ally.

I will structure these options with pros/cons and confidence, reflecting Itachi's internal strategic assessment.[Mode: STORY MODE]

[CHECKPOINT BLOCK:]
Sequence ID: 105 | Timestamp: Konoha, Year 12, August 19th, Evening | Key Stats: XP 188550/683700 (Level 20), Max HP: 203, Current HP: 203, Energy Points: 27/42, Fatigue: Level 0, Followers: 0, Income: 0gp/day, Gold: 795 GP, Valuables: 0 GP | Missions: Konoha's Hidden Hand: *Manipulate Konoha's power structures from the deepest shadows.* | [HASH:5F0E73B9F4A7C1D8]
Location: Forest outside Konohagakure, Meeting Point, Evening

Itachi Uchiha (Level 20 Ninja, Age 13) stood perfectly concealed, his **True Sight** piercing the twilight, observing Sasuke Uchiha (Level 8 Shinobi, Age 8) standing alone, taut with anticipation. His EP reserves were at 27/42. The stage was set for their reunion, a meticulously crafted manipulation.

*How to reveal myself?* Itachi's mind, a flawless instrument of strategic analysis, knew the reveal was paramount. It had to be impactful, dramatic, and perfectly controlled to reinforce the narrative he had begun to weave in Sasuke's mind and establish his own absolute dominance. It was about shaping not just what Sasuke saw, but what he *felt* and *believed*.

**Options for Revealing Himself to Sasuke:**

1.  **Sudden, Dramatic Appearance (Psychological Impact) [CHOICE_ID: DramaticAppearance_1]:**
    *   **Pros:** Appears suddenly from the shadows, leveraging his **Master Stealth** and **Greater Invisibility** (if active) for maximum psychological impact. This creates an aura of impossible power and mystery, reinforcing Sasuke's sense of awe and fear, setting the stage for his re-indoctrination.
    *   **Cons:** Purely a visual reveal; doesn't immediately convey the new narrative.
    *   **Confidence:** Very High. A classic, effective method for dramatic entrance.

2.  **Illusionary Recreation of Massacre (Traumatic Reinforcement) [CHOICE_ID: IllusionaryMassacre_2]:**
    *   **Pros:** Casts a powerful illusion (e.g., **Programmed Illusion** at 12 EP, or **Weird** at 20 EP if aiming for incapacitation) that subtly recreates elements of the Uchiha massacre, with a masked figure (Obito) as the central orchestrator. This would directly reinforce the fabricated narrative and deepen Sasuke's hatred, while Itachi remains hidden or appears as a 'savior' figure.
    *   **Cons:** High EP cost. Risks overwhelming Sasuke's young mind with too much trauma, potentially causing mental breaks or unpredictable reactions. Requires careful timing and execution.
    *   **Confidence:** Moderate. Potentially devastatingly effective, but high risk of unintended psychological damage.

3.  **Subtle Approach with Voice (Controlled Narrative) [CHOICE_ID: SubtleVoice_3]:**
    *   **Pros:** Approaches Sasuke subtly, speaking from the shadows or a concealed location, guiding his gaze towards a specific point as he reveals himself. This allows for immediate control of the narrative through carefully chosen words, playing on Sasuke's desire for truth.
    *   **Cons:** Less dramatic visual impact. Might not immediately establish the same level of psychological dominance.
    *   **Confidence:** High. A precise, controlled method for direct communication and narrative framing.

4.  **Confrontation with a Manipulated Konoha Ninja (Proxy Introduction) [CHOICE_ID: ProxyConfrontation_4]:**
    *   **Pros:** Orchestrates a brief confrontation between Sasuke and a subtly manipulated Konoha shinobi (e.g., a low-level Anbu, or a disillusioned agent he'd identified). Itachi then intervenes as a 'savior' or 'revealer of truth,' further isolating Sasuke and proving Konoha's corruption.
    *   **Cons:** Highly complex and risky. Relies on the competence of a proxy and risks unforeseen complications in real combat. Requires careful timing to ensure Sasuke is not truly harmed.
    *   **Confidence:** Moderate. Intellectually elegant, but introduces numerous uncontrolled variables.

My cold intellect demands the most efficient path to consolidating power and moving into the next phase of Konoha's Hidden Hand. Every action must serve my grand design.

---
[DM Note: You have chosen to *think* about your options for Itachi's next action. As per the "Post-Think Player Choice Enforcement Protocol," I will await your explicit decision from the `CHOICE_ID` options provided above. I will *not* continue the story or narrate Itachi's actions until you make a choice.]

Player (freeform):
DramaticAppearance_1

============================================================
