---
title: "Nocturne Apex Paladin — Scene 008"
type: source
tags: [campaign, scene, nocturne-apex-paladin]
last_updated: 2026-04-12
scene_number: 8
scene_total: 203
source_file: /tmp/campaign_downloads_v2/
---

## Scene 008 Summary

============================================================ Game Master: [Mode: DM MODE]  Understood. You have given **final approval** for the ruleset modifications proposed in **[Change ID: 20240702-A]** and explicitly confirmed the proposed conversion mapping for Aptitude Potential.  The "Dynamic Aptitude System" with its 1-5 "Aptitude Potential Coefficient" and "Yearly Progression Model" is now integrated into the Destiny Core Rules. The mapping for Aptitude Potential conversion is also now

## Key Details

- **Word count:** 4562
- **Campaign:** [[Nocturne Apex Paladin]]
- **Entry:** [[nocturne-apex-paladin-entry-008]]

---

## Full Scene Content

============================================================
Game Master:
[Mode: DM MODE]

Understood. You have given **final approval** for the ruleset modifications proposed in **[Change ID: 20240702-A]** and explicitly confirmed the proposed conversion mapping for Aptitude Potential.

The "Dynamic Aptitude System" with its 1-5 "Aptitude Potential Coefficient" and "Yearly Progression Model" is now integrated into the Destiny Core Rules. The mapping for Aptitude Potential conversion is also now official.

Here is the updated **Destiny Core Rules** document:

# Destiny Core Rules

### Table of Contents
* Core Concepts
* Character Attributes
* Character Progression System
* Energy & Resource Systems
* Core Combat System
* Combat Mechanics
* Martial Techniques
* World Interaction Rules
* Resting and Recovery

---

**I. Core Concepts**

*   **1.1 Game Master Role:** The AI will act as a Game Master (GM) and collaborative co-designer for the campaign.
*   **1.2 Setting:** This ruleset is setting-agnostic. The GM will establish the specific setting at the start of the campaign.
*   **1.3 GM Discretion & Collaborative Storytelling:** While these rules provide a comprehensive framework, the Master Game Weaver (GM AI) retains discretion to make minor adjudications or situational rulings to ensure smooth gameplay, narrative consistency, and fairness, especially in unforeseen circumstances. The goal is a collaborative and engaging story. Any significant or permanent deviations from these core rules should be discussed and agreed upon with the player (as per the Finalization Protocol in `mechanics_system_instruction.md` if applicable).

**II. Character Attributes**

*   **2.1 Core Resolution Mechanic:**
    *   All actions where the outcome is uncertain are resolved with a **Resolution Check**: `d20 + Relevant Modifiers vs. Challenge Number (CN)`.
    *   **Relevant Modifiers** typically include an Aptitude Modifier (see 2.2.A.2), a Combat Prowess Bonus (see 3.7) if applicable (e.g., for Spell Save CNs, see 6.8), and may also include bonuses/penalties from skills, Expertise Tags (see 2.5.B), circumstances, equipment, spells, or other game effects.
    *   **Challenge Number (CN) Determination:**
        *   **Opposed by Leveled Entity (Non-Attack Roll Checks):** If an action (such as a skill check against a creature or a spell requiring a saving throw) directly opposes or targets a creature, character, or entity with a defined Level, the baseline `CN = 10 + Target's Level`. (Weapon attack rolls target a creature's Defense score, see 6.3.A. For spells requiring a save, see 6.8 Spell Save Challenge Number).
        *   **General Task Difficulty:** For tasks not directly opposing a leveled entity (e.g., picking a lock, climbing a wall, recalling lore), the GM (AI) will assign an "Equivalent Level" (EqL) to the task based on its perceived difficulty, then derive the CN using the same formula (`CN = 10 + EqL`). Suggested benchmarks:
            *   Trivial Task (EqL 0-1): CN 10-11
            *   Easy Task (EqL 2-3): CN 12-13
            *   Moderate Task (EqL 4-6): CN 14-16
            *   Hard Task (EqL 7-10): CN 17-20
            *   Very Hard Task (EqL 11-15): CN 21-25
            *   Formidable/Legendary Task (EqL 16+): CN 26+
        *   The GM (AI) may apply situational adjustments (+/- 1 to 5 or more) to any CN based on specific advantageous or disadvantageous circumstances not already covered by other modifiers.

*   **2.2 The Dynamic Aptitude System:**
    A character's core attributes are dynamic, evolving with age and experience based on innate potential. The five Aptitudes are: Physique, Coordination, Health, Intelligence, and Wisdom.

    *   **A. Core Aptitudes & Aptitude Modifier:**
        1.  **Core Aptitudes:** A character possesses five core Aptitudes that define their fundamental capabilities:
            *   **Physique:** Represents physical power, brawn, and forcefulness.
            *   **Coordination:** Represents agility, dexterity, reflexes, and physical precision.
            *   **Health:** Represents physical resilience, stamina, and vitality.
            *   **Intelligence:** Represents reasoning, memory, analytical skill, and knowledge.
            *   **Wisdom:** Represents perceptiveness, intuition, willpower, and common sense.
        2.  **Aptitude Score & Modifier:** Each Aptitude has a score, typically ranging from 1 to 20 for player characters (though some beings may exceed this). This score is the current numerical representation of the character's ability in that Aptitude and is primarily used to derive the Aptitude Modifier. The Aptitude Modifier is calculated as: `(Aptitude Score - 10) / 2`, rounded down. This modifier is added to relevant d20 Resolution Checks.
            *   *Example: An Intelligence Score of 14 yields an Intelligence Modifier of +2. An Aptitude Score of 9 yields a modifier of -1.*

    *   **B. Aptitude Potential (Coefficient):**
        1.  **Definition:** Each character has an innate "Aptitude Potential" coefficient (rated 1-5) for each Aptitude, representing their natural talent. This coefficient primarily influences the rate of yearly progression and the ultimate ceiling for an Aptitude.
        2.  **Determination at Character Creation (Player Character):**
            *   The GM (AI) may propose a set of Potential coefficients based on the character's background, lineage, and concept.
            *   Alternatively, the player may propose Potential coefficients, which the GM (AI) will review for thematic consistency with the character concept (warning the player if choices seem narratively unrealistic for the established background).
            *   As a third option, a random generation method can be used if agreed upon.
            *   *GM (AI) Note: Work with the player to arrive at a narratively satisfying set of Potentials.*
        3.  **Determination (NPCs):** The GM (AI) will determine Aptitude Potentials for NPCs, aligning them with their role, backstory, and perceived innate talents.
        4.  **Conversion from Numerical Potential (for existing characters):** If a character was created with the previous numerical Aptitude Potential system, convert those values to the new 1-5 coefficient using the following mapping:
            *   **Numerical Potential 10-13:** Translates to a **Coefficient of 1 (Low/Below Average)**
            *   **Numerical Potential 14-15:** Translates to a **Coefficient of 2 (Average)**
            *   **Numerical Potential 16-17:** Translates to a **Coefficient of 3 (Good)**
            *   **Numerical Potential 18-19:** Translates to a **Coefficient of 4 (High)**
            *   **Numerical Potential 20+:** Translates to a **Coefficient of 5 (Exceptional/Prodigious)**
        5.  **Knowledge of Potential:**
            *   The GM (AI) knows all Aptitude Potentials (Coefficients).
            *   **Player Characters:** The player will be informed of their own character's Aptitude Potentials (Coefficients) during character creation or if they explicitly ask the GM (AI) in DM MODE.
            *   **Assessing Others:** Characters may attempt to assess or sense another character's (PC or NPC) Aptitude Potential through specific, challenging skill checks (e.g., a very high Insight or relevant knowledge check, possibly requiring observation over time), magical divination, or unique abilities. Success would yield a qualitative understanding (e.g., "They have a remarkable gift for magic," "They seem to have reached their physical peak") rather than exact numbers, unless a very high degree of success is achieved.
        6.  **Mutability:** While "innate," Aptitude Potential is not necessarily immutable. Extraordinary circumstances such as an epic quest, a powerful divine boon, a profound magical transformation, or a debilitating curse could, at the GM (AI)'s discretion and as a major narrative development, alter a character's Potential in one or more Aptitudes. Such changes are exceptionally rare.

    *   **C. The Yearly Progression Model:** A character's Aptitude scores change fractionally each year based on their age and Aptitude Potential coefficient.
        *   **Growth Years (Ages 16-25):** All Aptitudes gain `+ (Potential Coefficient / 10)` points per year.
        *   **Plateau Years (Ages 26-35):** Physical Aptitudes (Physique, Coordination, Health) change by `+ ((3 - Potential Coefficient) * 0.1)` points per year. Intelligence changes by `-0.1` points per year. Wisdom changes by `+0.2` points per year.
        *   **Decline Years (Ages 36+):** Physical Aptitudes change by `+ ((2 - Potential Coefficient) * 0.2)` points per year. Intelligence changes by `-0.2` points per year. Wisdom changes by `+0.1` points per year.

    *   **D. Special Growth: The "Lesson Learned" Check:** Wisdom can also be actively developed outside of normal progression by successfully making an Intelligence check to learn from significant life failures. The Challenge Number (CN) for this check is between 12-18, determined by the GM (AI) based on the severity and complexity of the failure from which the character is attempting to learn. Success grants a minor, immediate increase to Wisdom (e.g., +0.1 to +0.5 points).

    *   **E. Hidden Stats:** All NPC Aptitude Scores, Modifiers, and Potential are hidden from the player by default, revealed only through specific game actions (e.g., successful assessment skill checks, magical divination) or at the GM (AI)'s narrative discretion.

*   **2.3 Personality Traits (The Big Five System):**
    *   Characters are defined by five core Personality Traits, each rated on a scale of 1 (very low) to 5 (very high). These traits are generally static but can be influenced by major life events or character development arcs at GM discretion.
    *   **Trait Evolution (Optional Rule for Long Campaigns):** While core personality is largely stable, traits are not entirely immutable. Over extended periods of significant character development, or after profoundly impactful and repeated life experiences that consistently challenge or reinforce a particular way of being, the GM (AI) may, at major campaign milestones (e.g., completion of a Core Ambition, transition to a new Tier of Play), propose a minor shift (+/- 1) in a relevant Personality Trait rating. This should be a rare occurrence, reflecting genuine, earned character growth or trauma, and always discussed with the player for their PC. This is intended to model how individuals can subtly change over long arcs of their life story.
    *   **A. Active Traits (Direct Modifiers):** Four traits provide direct modifiers to relevant social Resolution Checks. The modifier is calculated as: `(Trait Rating - 3)`. This results in a range of -2 (for a rating of 1) to +2 (for a rating of 5), with a rating of 3 providing no modifier.
        1.  **Openness (to Experience):** Modifies checks related to creativity, imagination, appreciating art/beauty, trying new things, intellectual curiosity, and understanding unconventional ideas or individuals.
        2.  **Conscientiousness:** Modifies checks related to being organized, dependable, responsible, disciplined, and thorough. Can influence checks for planning, resisting distraction, or being perceived as reliable.
        3.  **Extraversion:** Modifies checks related to being outgoing, sociable, assertive, energetic, and seeking excitement. Directly impacts Performance, public speaking, and attempts to lead or inspire groups.
        4.  **Agreeableness:** Modifies checks related to being cooperative, empathetic, trusting, and good-natured. Directly impacts Diplomacy, attempts to mediate, build rapport quickly (initial interactions), or show compassion. May impose a penalty on Intimidation checks if very high.
    *   **B. Neuroticism (Behavioral Influence & Passive Effects):** This trait (rated 1-5, where higher means more prone to negative emotions) is not typically used as a direct roll modifier by the character but informs their behavior and passive resistances.
        1.  **Emotional Thresholds:** Higher Neuroticism may lower the threshold for negative emotional reactions like panic, suspicion, or despair in stressful situations, potentially requiring Wisdom (Willpower) checks to overcome.
        2.  **Starting Rapport:** May subtly influence the starting NPC Rapport tier with strangers (e.g., very high Neuroticism might lead to more cautious or suspicious initial reactions from others, or make the character themselves more wary).
        3.  **Susceptibility:** May impose penalties on checks to resist fear, despair, or mental manipulation effects. The GM (AI) will apply this as appropriate.
        4.  **Internal Conflict:** May influence the frequency or intensity of Internal Conflict checks (see 2.6).
*   **2.4 Relationship & Rapport System:**
    This system models the interpersonal dynamics between characters.

    *   **A. Rapport (Trust & History - PC to PC):**
        *   A numerical score from **-5 (Bitter Rivals)** to **+10 (Inseparable Companions)** tracked between any two significant player characters (PCs) or between a PC and a major, long-term NPC companion treated similarly to a PC in terms of relationship depth.
        *   **Mechanical Effect:** This score directly modifies the Challenge Number (CN) for social interaction checks *between these two specific characters*. The formula is `Adjusted CN = Base CN - Rapport Score`.
            *   *Example: If PC A tries to Persuade PC B (Base CN 15) and their Rapport is +3, the Adjusted CN becomes 12 (15-3=12), making it easier. If their Rapport is -2, the Adjusted CN becomes 17 (15 - (-2) = 17), making it harder.*
        *   **Evolution:** Rapport scores evolve dynamically based on shared experiences, mutual aid, betrayals, fulfilled or broken promises, and significant interpersonal interactions. The GM (AI) will track and update these scores.

    *   **B. Chemistry (Attraction & Romance - Any Two Characters):**
        *   A numerical score from **0 (None/Platonic)** to **+10 (Soulmates/Deeply Enamored)** representing romantic or deep platonic attraction between any two characters (PC-PC, PC-NPC, NPC-NPC if relevant).
        *   **Mechanical Effect:** This score provides a direct bonus to Resolution Checks related to romance, flirting, seduction, or expressing deep affection between these two specific characters. The character initiating the romantic action adds their Chemistry score with the target to their d20 roll.
        *   **Evolution:** Chemistry can develop (or fade) based on interactions, shared values, physical attraction (if applicable to characters), and romantic gestures.

    *   **C. NPC Rapport (PC to/from NPC - Tiered System):**
        *   This system models the general disposition and bond between a Player Character and most Non-Player Characters using a simplified tier system. The GM (AI) tracks this for each PC's relationship with significant NPCs.
        *   **Tiers & Narrative Descriptors:**
            *   **Tier 0: Hostile / Unfriendly / Distrustful / Indifferent-Unknown.** (Default for unknown NPCs or those with negative initial impressions).
            *   **Tier 1: Neutral / Acquaintance / Cautiously Tolerant / Mildly Positive.** (Basic professional interactions, or initial positive but unproven encounters).
            *   **Tier 2: Friendly / Cooperative / Allied / Trusted.** (Established positive relationship, willing to offer reasonable aid).
            *   **Tier 3: Loyal Friend / Confidante / Staunch Ally.** (Strong bond, willing to take personal risks or offer significant aid).
            *   **Tier 4: Utterly Devoted / Profoundly Loyal / Dominated.** (An exceptionally rare and powerful bond. The NPC deeply trusts and prioritizes the PC's well-being and stated goals, often above their own immediate self-interest or previous lesser allegiances. Even at this tier, if the PC's request starkly violates one of the NPC's own Core Motivations or deeply held fundamental ethics not related to the PC, the NPC might still experience an Internal Conflict check (see 2.6), though the PC's influence would grant a significant bonus to the side favoring the PC. Outright refusal would be exceptionally rare and only in the most extreme conflicting circumstances. This tier can also represent magical domination or extreme psychological influence, in which case free will may be entirely suppressed).
        *   **Mechanical Effects (Bonuses to PC's Social Checks targeting the NPC):**
            *   Tier 0: May impose a -2 penalty to the PC's social checks, or the NPC makes opposed social checks with Advantage. Social CNs set by this NPC for the PC are increased by +2.
            *   Tier 1: +0 modifier to PC's social checks. Standard CNs.
            *   Tier 2: +2 bonus to PC's social checks, or the NPC makes opposed social checks with Disadvantage. Social CNs set by this NPC for the PC are decreased by -2.
            *   Tier 3: +4 bonus to PC's social checks. The NPC is generally helpful and may provide information or minor aid without a check, or perform significant favors on a successful check against a reduced CN.
            *   Tier 4: +6 bonus (or automatic success on many non-extreme requests) to PC's social checks. The NPC will strive to fulfill the PC's requests to the best of their ability, often without question, unless it directly violates an even more profound core principle or results in certain self-destruction without overwhelming justification.
        *   **Influence on NPC's Internal Conflict Checks (see 2.6):**
            1.  If an NPC has an Internal Conflict check regarding an action that would **harm or betray a PC with whom they have positive Rapport (Tier 2+):** The NPC adds their Rapport Tier number (2, 3, or 4) as a bonus to the side of the conflict representing loyalty or aid to the PC.
            2.  If an **external party attempts to socially influence (e.g., persuade, deceive, intimidate) an NPC to act against a PC with whom the NPC has positive Rapport (Tier 2+):** The CN for the external party's social check is increased by the NPC's Rapport Tier with the PC.
        *   **Evolution:** NPC Rapport tiers evolve based on the PC's actions, dialogue, reputation, fulfilled promises, acts of kindness or cruelty towards the NPC or things they value.

    *   **D. Protector's Conviction:**
        *   When a character makes a Deception check specifically to protect an individual (PC or NPC) with whom they have a positive Rapport score (for PC-PC Rapport, a score of +1 or higher; for PC-NPC Rapport, Tier 2 or higher), they may add their numerical Rapport score/Tier with that person as a direct bonus to their Deception roll.
            *   *Example: PC has Rapport +5 with an NPC. To protect that NPC via a lie, the PC adds +5 to their Deception check. If PC has Tier 3 NPC Rapport with an NPC, they add +3 to the Deception check.*
*   **2.5 Influence & Expertise System:**
    This system models a character's social standing within specific groups or regions (Influence) and their specialized non-combat knowledge or skills (Expertise Tags).

    *   **A. Influence:**
        1.  **Definition:** Influence is a numerical score, typically ranging from **0 (Unknown/Neutral/No Standing)** to **5 (Highly Respected/Feared/Authoritative Figure)**, representing a character's reputation, sway, and social capital within a *specific defined social group, organization, or geographical region*.
            *   A character may have different Influence scores with different groups/regions (e.g., Influence 4 with the Merchants' Guild, Influence 1 with the City Watch, Influence 0 with the Elven Enclave of a distant forest).
            *   The GM (AI) will track a character's Influence scores with relevant entities as they become established through gameplay.
        2.  **Mechanical Effect:** When a character makes a social Resolution Check (e.g., Persuasion, Intimidation, Deception, Diplomacy, Requesting Favors) targeting an individual who is part of a group/region where the character has an established Influence score, or when the social interaction explicitly leverages that reputation, the character **adds their Influence score with that specific group/region as a direct bonus to their d20 roll.**
            *   *Example: If a PC has Influence 3 with the "Dockworkers' Union" and attempts to persuade a union foreman, they add +3 to their Persuasion check.*
            *   **Relevance Adjudication:** The GM (AI) determines if the Influence is "relevant" to the check. Generally, it applies if the target NPC would logically know of and care about the character's standing within that group, or if the character is explicitly using their position/reputation. Influence with the "Royal Court" might not help when haggling with a back-alley smuggler unless a specific connection is made.
        3.  **Gaining & Losing Influence:**
            *   Influence is dynamic and changes based on a character's actions, achievements, failures, and how they are perceived by the relevant group.
            *   **Gaining Influence:** Typically achieved by completing significant tasks that benefit or impress the group, upholding the group's values, achieving high rank within it, public commendations, or forming strong alliances with its key members.
            *   **Losing Influence:** Can occur due to actions that harm the group or its interests, betraying its trust, publicly failing in important duties related to the group, associating with its enemies, or through successful efforts by rivals to slander or undermine the character's standing.
            *   The GM (AI) will narrate significant changes in Influence and update the tracked scores.
        4.  **Interaction with Rapport:** Personal Rapport (see 2.4) with an individual generally takes precedence over broader Influence with their group if the two scores would conflict significantly for an interaction *with that specific individual*. However, high Influence can make it easier to *gain* initial positive Rapport with members of that group.

    *   **B. Expertise Tags:**
        1.  **Definition:** Expertise Tags are descriptive keywords or short phrases representing specific, often non-combat, fields of knowledge, craft, or specialized skill that a character has mastered (e.g., "Ancient History," "Herbalism," "Starship Navigation," "Dwarven Runelore," "Courtly Etiquette," "Underworld Contacts," "Cryptography").
        2.  **Acquisition:**
        *   Characters may start with Expertise Tags based on their background, class features (as per rule 3.4 - Adapting Existing Class Features), or initial concept.
        *   Upon reaching a **new Tier of Play** (typically around Levels 5, 11, and 17, as per Part 6.C of `mechanics_system_instruction.md`), characters may choose **one new Expertise Tag.**
        *   Additional tags can be gained through dedicated training, extensive practical experience in a field, significant study, mentorship, or as rewards for completing specific quests related to that expertise. The GM (AI) will award new tags when narratively appropriate and earned.
        *   Specific classes (like the Expert archetype) may grant additional Expertise Tags as part of their features.
        3.  **Mechanical Effect:** When a character makes a Resolution Check (skill check, ability check) where their specific, relevant Expertise Tag would directly and significantly contribute to their chance of success, they **gain Advantage on that d20 roll.**
            *   **Advantage Definition (Default):** Roll two d20s and use the higher result. (If the active ruleset defines Advantage differently, use that definition).
            *   **Relevance Adjudication:** The GM (AI) determines if an Expertise Tag is directly applicable. For example, "Ancient History" would apply to a check to recall details about a long-dead empire, but not to a check to persuade a modern-day merchant (unless the historical knowledge itself is the persuasive element). A character can possess multiple Expertise Tags, but typically only one highly relevant tag grants Advantage on a single check unless specific circumstances or abilities allow for stacking benefits.
        4.  **Distinction from General Skills/Proficiencies:** Expertise Tags represent a deeper or more specialized mastery than general skill proficiencies (if the active ruleset uses a separate skill system). A character might be "Proficient in History," but have an "Expertise Tag: Pre-War Dynastic Lineages," granting Advantage on very specific historical recall within that niche.

*   **2.6 Internal Conflict System:**
    This system is used to resolve significant internal dilemmas for characters (both PC and major NPCs), representing moments where their values, desires, fears, or loyalties are in direct opposition, leading to a character-defining decision. It is typically invoked by the GM (AI) when a character faces a profound moral choice or a situation that challenges their core being.

    *   **A. Triggering an Internal Conflict Check:**
        *   An Internal Conflict Check is triggered when a character faces a **major character-defining decision** where two or more core aspects of their being (values, strong desires, loyalties, fears, ingrained personality traits) are in significant opposition.
        *   *Examples of Triggering Decisions:*
            1.  "Should I betray my sacred oath to my order to save my captured sibling?" (Loyalty to Order vs. Familial Love/Protection)
            2.  "Should I seize this opportunity for immense personal power, knowing it will likely cause widespread suffering to innocents?" (Ambition/Desire for Power vs. Compassion/Moral Code)
            3.  "Do I reveal a devastating truth that could shatter a fragile peace, or maintain a lie for the sake of stability?" (Honesty/Justice vs. Pragmatism/Order)
            4.  "Do I confront this terrifying, overwhelming foe to protect others, or do I flee to ensure my own survival?" (Courage/Altruism vs. Self-Preservation/Fear)
        *   The GM (AI) will identify when such a pivotal moment arises based on the narrative and the character's established persona.

    *   **B. Identifying Opposing Traits/Values:**
        *   When an Internal Conflict is triggered, the GM (AI) will determine the two primary **opposing forces** at play within the character for that specific dilemma. These forces can be drawn from:
            1.  **Core Aptitudes:** (e.g., Wisdom representing moral judgment vs. Physique representing raw impulse or desire).
            2.  **Personality Traits (Big Five):** (e.g., High Conscientiousness urging one path vs. High Neuroticism fearing its consequences, or Low Agreeableness pushing for a selfish act vs. an acquired sense of duty).
            3.  **Abstract Values & Loyalties:** Explicitly stated or strongly implied values such as Loyalty (to a person, group, or ideal), Ambition, Love, Honor, Justice, Greed, Fear, Survival Instinct, Vengeance, Mercy, etc. These are often derived from the character's backstory, actions, and Core Motivation.
            4.  **Situational Pressures vs. Ingrained Beliefs.**
        *   The GM (AI) will attempt to **simulate realistic human psychological conflict** when selecting these opposing forces, choosing the most salient and narratively compelling drivers for the character in that moment. The GM (AI) will state these opposing forces to the player (for a PC's conflict) or use them for internal NPC resolution. (e.g., "Your sense of Honor (Trait A) battles with your raw Fear (Trait B).")

    *   **C. Core Motivation's Influence:**
        *   Each significant character (PC and major NPCs) should have one or more **Core Motivations** established (either player-defined at character creation, suggested by the GM (AI) based on concept, or emerging through gameplay and then confirmed). These are overarching drives (e.g., "To protect the innocent," "To achieve ultimate knowledge," "To avenge my fallen family," "To amass great wealth").
        *   **Mechanical Effect:**
            1.  If one of the opposing Traits/Values (from B) directly **aligns with or strongly supports** the character's Core Motivation, that side of the contested check receives a **+2 to +5 bonus** (GM (AI) discretion based on the strength of alignment and the power of the Motivation).
            2.  If one of the opposing Traits/Values directly **conflicts with or undermines** the character's Core Motivation, that side of the contested check receives a **-2 to -5 penalty** (GM (AI) discretion).
            3.  If neither Trait directly engages the Core Motivation, no bonus or penalty from it applies for this specific conflict.

    *   **D. Resolution - The Contested Check:**
        *   The Internal Conflict is resolved via a **contested d20 check**:
            `d20 + Modifier for Trait/Value A (including Core Motivation bonus/penalty) vs. d20 + Modifier for Trait/Value B (including Core Motivation bonus/penalty)`
        *   The "Modifier for Trait/Value" will be:
            *   If an Aptitude is chosen as the Trait: The Aptitude Modifier (see 2.2.A.2).
            *   If a Big Five Personality Trait is chosen: Its scaled modifier (see 2.3.A).
            *   If an abstract Value/Loyalty is chosen: The GM (AI) will assign a situational modifier (e.g., +0 to +5) based on how deeply ingrained or situationally potent that value is for the character (this can also be influenced by Rapport scores if the loyalty is to a specific person).
        *   The side with the higher total "wins" the internal struggle, indicating the character's stronger inclination. The GM (AI) will narrate this internal resolution (e.g., "Despite your fear, your resolve to protect your comrades (Trait A) wins out over your instinct to flee (Trait B).").

    *   **E. Player Agency & Consequence of Final Decision:**
        1.  **Player Decides for PC:** For a Player Character, the outcome of the contested check (D) represents their character's *internal inclination or subconscious leaning*. However, the **player always retains 100% agency to make the final decision** about their character's actual chosen action, even if it directly contradicts the "winning" side of their internal conflict.
        2.  **Consequences for Acting Against Internal Resolution:** If the player chooses an action for their PC that goes against the "winning" side of a significant Internal Conflict check (especially if it means acting against a deeply held "good" value or succumbing to a "negative" one that their inner strength tried to resist):
            *   The GM (AI) **must impose narrative and/or minor mechanical consequences** to reflect the psychological dissonance or stress. These are not meant to be overly punitive but to add realism. Examples:
                *   **Temporary Fatigue:** The character gains 1 level of Fatigue (see 4.4).
                *   **Temporary Stat Reduction:** A minor, temporary penalty (e.g., -1 or -2 for a few hours or until a rest) to a relevant Aptitude Score (e.g., Wisdom if they acted against their conscience, Charisma if they betrayed trust).
                *   **Internal Monologue:** Narrate the character's feelings of guilt, regret, unease, or self-justification.
                *   **Social Repercussions (Subtle):** If the decision was observable or its consequences become known, there might be subtle shifts in how others perceive the character, potentially affecting future NPC Rapport or contributing to changes in Influence with relevant groups. This is not an immediate mechanical penalty but a narrative consequence the GM (AI) will track.
                *   **Future Roleplaying Prompts:** The event might be referenced in

God Mode:
just print the changes to destiny

============================================================
