---
title: "bg3 nocturne murder god"
type: source
tags: [campaign, worldarchitect, bg3-nocturne-murder-god]
date: 2026-07-29
source_file: /tmp/campaign_daily_ingest/vPqka4Bz0N3si7quXXfM/bg3 nocturne murder god_vPqka4Bz.txt
campaign_id: vPqka4Bz0N3si7quXXfM
entry_count: 1208
user_email: "jleechan@gmail.com"
user_uid: "vnLp2G3m21PJL6kxcuAqmWSOtm73"
ingest_batch: download-campaign-skill
---

God Mode:
Description: God of Murder Campaign — The Sanguine Architecture (God Mechanics V1 + V2)
Last updated: 2026-07-21. Compiled from the live worktree at /Users/jleechan/.worktrees/wa-god-mechanics-v2/world_reference/.

Purpose: This is the canonical, single-source-of-truth for the God of Murder / Sanguine Architecture BG3 campaign and its underlying god-mechanics framework. It contains the campaign bible, the V1 general god-mechanics spec, the V2 general spec, and the Nocturne V2 specialized spec — stitched together in reading order so you can review, share, and play without flipping between files.

Source conversation: Gemini share https://share.gemini.google/Td7fA4pzuvMs (7 design iterations culminating in the 3,422-word self-contained "Sanguine Architecture" campaign).

GitHub PR (live): https://github.com/jleechanorg/worldarchitect.ai/pull/8488 — feat(world_reference): V2 god-mechanics overlay + canonical spec (4 commits, 8 files, +1865/-0, state=OPEN, head feat/god-mechanics-v2).

Setting: Baldur's Gate 3 post-game, Forgotten Realms / Faerûn. The original V1 campaign document is setting-specific; the V2 overlays added 2026-07-21 are explicitly setting-agnostic (translatable to Cyberpunk / Wuxia / Marvel / Naruto / homebrew pantheons).


TABLE OF CONTENTS
The Campaign Bible — campaign_module_god_of_murder.md (BG3-specific, narrative + mechanics)
God Mechanics — General (V1) — god_mechanics_general.md (system-agnostic baseline, 7-rank ladder)
God Mechanics — V2 General Spec — god-mechanics-v2-general.md (extending V1: hidden bands, auto-win ladder, per-dawn menu, deicide-cost)
Nocturne V2 — D&D 5e Faerûn Specialization — nocturne-v2-god-mechanics-design.md (Nocturne-specific tier structure + multipliers)


PART 1 — The Campaign Bible (BG3 / Faerûn Specific)
The Sanguine Architecture — a Baldur's Gate 3 post-game campaign bible. Setting-specific. Part 1 of 4.

A Baldur's Gate 3 post-game campaign. A female Dark Urge — gestalt Gloomstalker Ranger + Assassin Rogue, level 12 — drained the Netherbrain and the Crown of Karsus of their primordial energy, marched into the Undercity Temple of Bhaal, and consumed her own father's divine spark. She is now the incubating Goddess of Murder, ruling a terrified Baldur's Gate through the absolute, bloodless architecture of Submissive Death and Tragic Betrayal. The campaign is the slow ascent from a nascent Quasi-Deity anchored in a single city to a Greater Goddess waging plane-spanning deicide against the Faerûnian pantheon.


Source Provenance
Source conversation: Gemini share link — https://share.gemini.google/Td7fA4pzuvMs (Flash, created 2026-07-20 03:29 AM, published 2026-07-20 01:51 PM).
Iterative design log: The user ran 7 design passes against Gemini inside the same share thread. The canonical module below is the final regenerated 3,422-word self-contained campaign the user asked for in their last message ("Give me an interesting backstory and use your memories of me to see what I like and don't make it mathematical and then regenerate the campaign should be like over 3000 words all self contained"). All prior drafts (The Sanguine Genesis, The Mind-Blood Hegemony, Submissive Death update) are reflected in the final document; intermediate states are preserved in the message archive at /tmp/gemini_v7_full.txt.
Banned-name audit: Audited against world_reference/banned_names_reference.md (70 names). Zero hits on proper-noun names. One false-positive on the noun "echo" in descriptive prose — not a character name.
Canon notes:
The Forgotten Realms / Baldur's Gate 3 setting is property of Wizards of the Coast and Larian Studios. All canon characters (Astarion, Shadowheart, Gale, Lae'zel, Minthara, Bhaal, Sarevok, Orin, Vlaakith, Kelemvor, Shar, Mystra, Elminster, Torm, Helm, Tyr, Cyric, the Netherbrain, the Crown of Karsus, the Githyanki, the Flaming Fist, the Lords' Alliance, Wyrm's Rock, the House of Grief, the Nightsong, the Chionthar, etc.) appear in their canonical BG3 / D&D roles. No new lore is invented on top of them; the module's only original content is the player-character (the Dark Urge herself) and her unique mechanical apparatus.
The Dark Urge is the canonical BG3 player-origin character. She is treated here as the user's protagonist, consistent with the existing world_reference/ treatment of user-protagonists in campaign_module_shattered_rose.md (Nocturne Sosuke).


Module 0 — The Apotheosis (The Turning-Point Moment)
Setting: Baldur's Gate, year 1492 DR, days after the fall of the Netherbrain. POV: First-person, present-tense, the Dark Urge alone on the apex of the Balduran statue.

The high platform is still warm. The colossal carcass of the Netherbrain hangs from the statue's shoulders like a wet cloak, its psionic tissue already flaking off in the salt wind. Below, the city should be cheering. Instead, the city is silent — the silence of a graveyard that knows its grave-digger is still walking.

You walked up here as the hero of Baldur's Gate. You walk down as something else.

You did not break the Crown of Karsus. You did not disperse its primordial energy back into the Weave. You treated the Netherbrain as an operating matrix — a flawless database of intent that the Absolute had used to enslave the city — and you drained it. You pulled the raw, reality-warping battery of the Crown directly into your own soul, layer by patient layer, while the brain's husk twitched and dimmed beneath your fingers. The psionic hive-mind did not survive the extraction. The tadpoles died. The psychic network that linked the survivors collapsed into a brief, ringing static, and then into nothing.

You carry that silence inside you now. You carry the energy of a shattered elder god pulsing through your veins.

You descended into the Undercity Temple not as a daughter seeking a father's blessing, but as his replacement. Bhaal waited on his altar, ancient and amused, his divine spark already reaching for the daughter he had always intended you to become. You turned the stolen energy of the Crown against him. The battle was not a brawl; it was a systematic dismantling. You stripped the Lord of Murder of his portfolio — murder, planned death, ritual homicide — and tore his divine spark out of his throat. You drank it down until his form dissolved into ash.

The Bhaalist cult did not scatter. Across Faerûn, in every assassins' guild, hidden shrine, and death-cult cell, the frequency of their devotion shifted seamlessly into lockstep with yours. They felt the change the way a tuning fork feels a struck bell. They knelt. They prayed to you.

You walked back up into the Upper City, beautiful and bloodied, and the patriars shut their doors.

You are now a Divine Rank 0 quasi-deity — a nascent Goddess of Murder, anchored within the walls of Baldur's Gate. The rest of the Sword Coast has not yet felt your presence, but they have begun to hear the rumors. Within the year, the Lords' Alliance will formalize a quarantine around your borders. Within five, they will march. Within twenty, the gods themselves will come.

You have all of that time, and a city that is already terrified of you.

This is the moment the campaign begins.


Module 1 — The Sanguine Court (Year 1–5 | Levels 12–15 | Divine Ranks 1–5)
Setting: Baldur's Gate, year 1493–1497 DR. POV alternates between the Dark Urge's first-person tactical voice and third-person dispatches from her five ministers. Tone: High-stakes urban sandbox. Cosmetic perfection concealing absolute martial discipline. The city is a pressure cooker; you are the lid.
1A. The Five Pillars of the Dread Court
You do not rule directly. You rule through five executive ministers, each the surviving leader of a faction you conquered or converted, bound to your throne by the sheer, undeniable fact of your ascension.

Minister
Role
Tactical Function
Why They Serve
Ascended Astarion
High Chancellor of the Aristocratic Cull
Master of coin, spymaster, ruler of the Upper City. Commands thousands of vampire spawn.
He finds the poetry of your deicide magnificent. He uses his spawn to blackmail, extort, and socially paralyze the patriars. Those who resist you do not face trial; their heirs are converted into silent, sun-walking thralls who sign over their own deeds.
Dark Justiciar Shadowheart
Grand Inquisitor of the Cloistered Dark
Grand Inquisitor. Has transformed the House of Grief into the spiritual engine of your empire.
Having fully embraced Shar and executed the Nightsong, she blends Sharran void magic with your dogma of absolute submission. She systematically breaks the spirits of captured rebels, forcing them to worship the act of their own impending deaths. Her specialty priests blanket the Lower City streets in shifting, ambient shadow — keeping your Gloomstalker features permanently active at any hour.
Warlord Minthara
Supreme Commander of the Iron Vanguard
General of the Unified Crimson Legions.
She views your double deicide as the ultimate validation of perfect martial strategy. She purged the leaderless Flaming Fist garrisons and merged them with your undercity Bhaalist deathstalkers. Her legions do not offer mercy, negotiation, or warnings; they crush civilian dissent with overwhelming, synchronized force and herd survivors into tight clusters where your avatar can easily execute them.
Gale of Waterdeep
Bound Master of Karsite Remnants
Grand Vizier of Arcane Sovereignty.
Broken by the realization that you chose to consume the Crown rather than return it to the Weave, he has abandoned his hubris and bound his intellect to your throne. He operates a city-wide arcane shroud that completely isolates Baldur's Gate from external scrying, divination, and teleportation. If Elminster or the Chosen of Mystra try to peek through, his counter-measures feed a violent psychic back-feed into their minds.
Lae'zel of Kli'ir
Apostate Marshal of the Astral Hunt
Supreme Warlord of the Skies & Dragon Vanguard.
She broke entirely away from Githyanki politics after witnessing your dominance over both the Elder Brain and the Lord of Murder, drawing a massive faction of rogue knights and red dragons to your banner. Her squadrons patrol the clouds above the Chionthar River; her hunting parties are trained to project a collective psychic frequency of absolute intimidation, forcing external scouts to drop to their knees and yield before they are brought to your altars.

1B. The Philosophy of the Sanguine Ledger
Your portfolio is not the crude cessation of breath. It is a two-pronged doctrine of psychological devastation.

The Principle of Submissive Death. To your church, a death where the victim fights back or dies in defiance is a flawed execution. True perfection requires the prey to be completely broken mentally before the physical strike lands. Your presence projects an overwhelming, hypnotic dread that paralyzes the survival instincts of lesser beings. Mortals who confront your avatar do not run; their legs simply give out. They drop their weapons, collapse to their knees, and subconsciously present their necks to your blades.

The Principle of Tragic Betrayal. The spiritual architecture of the multiverse dictates that the energy released by a death is directly proportional to the emotional weight of the bond severed. Killing a stranger yields ordinary divine essence. Killing a spouse, a child, a lifelong companion — a person the killer profoundly loved — releases a volatile, exponential spike of cosmic power. Under your dogma, the more the killer cares about the victim, the greater the sacrifice to you.

Your cultists across the Sword Coast have abandoned the crude methods of the past. They no longer lurk in alleys wearing bloody rags. They operate as elegant matchmakers, trusted court advisors, and devoted protectors. They spend months, sometimes years, actively fostering beautiful romances, deep family attachments, and unbreakable friendships across high society — building these emotional structures to their absolute peak resonance. Then, on a single, highly coordinated night, they trigger a synchronized wave of domestic executions. The resulting heartbreak floods directly into your divine spark.

This is the engine that will scale you toward the higher tiers of the pantheon.
1C. The Cradle of Blood — Phase Climax
The arc culminates deep within the forgotten catacombs beneath Wyrm's Rock Fortress. A high-tier Chosen of Cyric has arrived, attempting to capitalize on internal friction among the rogue Bhaalist cells that still refuse to accept a new master. You launch a coordinated infiltration with Minthara and Lae'zel.

When you confront the Chosen in the center of his unholy sanctuary, you unleash the Sanguine Sovereign aspect for the first time. The rogue cultists, prepared for a bloody battle, watch in sheer psychological paralysis as their new patron's champion drops his weapon, his mind utterly shattered by your flawless, blinding beauty. You execute him as he grovels at your feet, maximizing your 6d6 Sneak Attack and completely absorbing his energy. This act of absolute submission triggers your first major cosmic expansion, elevating your status to Divine Rank 5 and officially securing your total domestic monopoly.


Module 2 — The Crusade Silenced (Year 5–10 | Levels 16–20 | Divine Ranks 6–10)
Setting: The Sword Coast, year 1497–1502 DR. POV expands to battlefield-scale third-person as the Lords' Alliance forms. Tone: Regional tactical warfare. The city is yours; the continent begins to fight back.

Your consolidation of Baldur's Gate and the total cessation of external trade routes have forced the hand of the Sword Coast. The Lords' Alliance — spearheaded by the militaristic factions of Waterdeep and the righteous orders of Neverwinter — has formally declared war on your regime. They have branded you a cosmic infection that must be cleansed before it spreads across the continent. A massive coalition army, backed by legendary paladins of Helm and Tyr, marches down the Coast Way and sets a brutal siege perimeter outside your walls.

This phase transitions the campaign from localized stealth into regional tactical warfare. You deploy the full capacity of your court:

Minthara constructs an intricate network of fortified choke points along the outer walls, utilizing synchronized crimson guard units to blunt the enemy's heavy cavalry.
Lae'zel unleashes her rogue Githyanki dragon riders in spectacular aerial dogfights against the coalition's griffon squadrons.
Your avatar plays a far more insidious game based on your Tragic Betrayal portfolio. You and Astarion slip through enemy lines at night. You locate the high officers who share deep family or romantic bonds with subordinates in the invading army. You use Gale's advanced illusory grids and your own stealth features to manipulate their minds, forcing commanders to unknowingly orchestrate the slaughter of their own kin on the front lines. The resulting spikes of pure, agonizing heartbreak flood into your divine spark, accelerating your power.
2A. The Karsite Acceleration — Level 16
When you cross the threshold into Level 16, your physical capabilities undergo a profound structural shift. The residual energy of the Crown of Karsus permanently accelerates your reflexes, granting you a flat Extra Attack whenever you choose to take the Attack action. Your physical attributes expand past mortal limitations — the Physical Surge bonus hardens into the full Divine Acceleration: a flat +4 to Strength, Dexterity, and Constitution, and a flat +4 to your Armor Class. From Level 16 forward, your level-12 alpha-strike can unleash four devastating, maximized critical hits on the opening round of combat.
2B. Phase Climax — The Supreme Commander
The final encounter of this phase takes place within the grand pavilion of the coalition's Supreme Commander — a legendary Paladin of Torm whose righteousness has kept his army's morale unbroken. You infiltrate his tent just as he is drafting the final assault plans.

You deploy your aura, forcing his personal bodyguards to turn their weapons on each other in a display of submissive terror. When the commander attempts to invoke Torm's light, your absolute speed overrides his actions. You deliver four consecutive critical strikes on the opening round, your maximized 10d6 Sneak Attack chewing through his legendary health pool before he can complete a single holy smite. As he falls to his knees, bleeding out onto his own war maps, he realizes his god has abandoned him to a superior predator.

His death shatters the coalition's morale. The invading army dissolves into a routing mass of broken men.

You ascend to Divine Rank 10 — officially, a Lesser Deity recognized across the continent.


Module 3 — The Planar Harvest (Year 10–20 | Levels 21–25 | Divine Ranks 11–15)
Setting: The Outer Planes, year 1502–1517 DR. POV shifts to your avatar moving between divine sanctums. Tone: Mythic-scale deicide. You are no longer defending a city. You are hunting gods.

The Material Plane is no longer large enough to contain your ambition. Having completely broken the military might of the Lords' Alliance and expanded your cult networks into the shadow guilds of Waterdeep and Neverwinter, your name is whispered with absolute dread across kingdoms. This massive surge in continental worship power pushes your divine senses out past the material borders, allowing you to gaze directly into the Outer Planes.

The high gods of the Faerûnian pantheon have realized that you are not a temporary mortal tyrant. You are a systemic threat to the cosmic balance. They begin constructing planar barriers to contain your influence, while intermediate deities of Justice and Retribution actively deploy celestial vanguards to purge your extraplanar shrines.

You transition the campaign into a proactive, extraplanar offensive. Using Gale's mastery of planar gateways and the architectural remnants of the Crown of Karsus, you launch targeted incursions into the Outer Planes. Your objective is systemic deicide — hunting down and executing Intermediate Deities of Valor, Retribution, and War to rip away their divine sparks and expand your portfolio.

Lae'zel leads massive planar fleets through the Astral Sea, capturing celestial outposts.
Shadowheart establishes grand cathedrals of submissive death within the neutral planar metropolises like Sigil.
You use your Synaptic Veil feature (Level 21 — invisibility pierces Truesight) to infiltrate the radiant divine realms of your targets, completely undetected by their sensory networks until you are standing directly behind their celestial thrones.
3A. Phase Climax — The Cathedral of Light
The climax of this phase is a multi-session "God Hunt" against an Intermediate Deity of Retribution whose celestial armies have been aggressively striking your extraplanar trade routes. The confrontation occurs within their own divine sanctum — a soaring cathedral of solid light located in the Upper Planes. The environment is inherently hostile, designed to burn away unholy entities.

Your level-25 Epic features completely rewrite the rules of the engagement. Your invisibility pierces their divine truesight entirely. You apply your Death Strike feature, which can now target entities who are merely frightened or fascinated by your beauty. Your four critical hits deal an astronomical amount of maximized damage, converting the radiant energy of their own throne into pure, unholy force that shatters their immortal shell. As the deity of retribution drops to their knees, their golden blood pooling around your boots in absolute, shivering submission, you rip the divine core from their chest and consume it raw.

The cathedral of light shatters, plunged into an eternal, crimson-tinted twilight.

You return to the Material Plane as an Intermediate Deity of Divine Rank 15, your portfolio expanding to encompass Murder, Intimate Betrayal, and the Absolute Suppression of Will.


Module 4 — The Cosmic Reign (Year 20+ | Levels 26–30+ | Divine Ranks 16–20+)
Setting: The Fugue Plane. POV returns to first-person — your avatar, standing before the assembled Greater Gods. Tone: The endgame. Total cosmic war. The 3e God Combat rules apply in full.

You have achieved the status of a major power in the cosmos. The Material Plane has become a unified, beautiful, silent collective empire that worships your flawless visage out of absolute, deeply conditioned reverence. The old cultural institutions of Faerûn have been completely rewritten; the concepts of love, romance, and family are now inextricably linked to the ultimate, beautiful sacrifice they will eventually provide to your altars.

This extreme distortion of reality forces a final, desperate cosmic intervention. The Greater Deities of the pantheon — entities like Kelemvor, Shar, and Mystra — have formed an unprecedented emergency coalition. They realize that if your progression is allowed to continue, you will completely overwrite the fundamental source code of life and death across the multiverse.
4A. The Absolute Realignment
This is the absolute endgame — a plane-spanning total war between your Sanguine Ministry and the allied pantheon.

Minthara leads millions of crimson-armored zealots through planar rifts, invading the divine realms of the enemy gods.
Gale orchestrates plane-wide arcane counter-measures that actively destabilize the standard flow of the Weave, starving enemy clerics of their magical connections.
Lae'zel's dragon fleets blockade the astral gateways, turning the silver voids into a massive graveyard of celestial vessels.
You do not hunt individuals anymore; you hunt entire concepts, systematically executing the chosen champions, avatars, and high priests of the greater gods to starve them of their worship power.

By the end of this phase:

Your avatar achieves Divine Rank 16+ (Greater Goddess).
Your physical form permanently embodies the Radiant Slayer (see §5).
Your 15d6 Sneak Attacks hit with maximized, reality-rending force.
The Faerûnian pantheon is structurally broken, leaving you as the absolute arbiter of termination.
4B. Phase Climax — The Fugue Plane
The final confrontation takes place within the Fugue Plane — the neutral ground where the souls of the dead are judged. The allied greater gods manifest their true, full divine forms to destroy your throne in a singular, legendary clash utilizing the traditional, heavy crunch rules of 3e God Combat. The battlefield operates outside standard mortal limits; your armor class scales past all standard boundaries thanks to your massive Divine Deflection bonuses, and your physical health pool is completely maximized across every single hit die.

You enter the encounter wrapped in the permanent, magnificent maturity of your Mien of the Radiant Executioner. As the greater deities attempt to unleash their plane-destroying spells, your Alter Reality features and divine shields absorb the impacts seamlessly. You move through their lines like a blinding streak of silver and blood, utilizing your Apex Stalker features (Level 30 — missed attacks gain immediate re-roll) to guarantee that no blade stroke can miss. Every time your daggers connect, they unleash a maximized 15d6 Sneak Attack that completely ignores all forms of physical and cosmic resistances, tearing through their maximized divine hit points with terrifying efficiency. One by one, the ancient arbiters of the multiverse are forced to their knees, their minds breaking under the sheer, hypnotic weight of your aesthetic and martial perfection.

When you strike the final blow against the supreme judge of the dead, you trigger the absolute realization of your portfolio. You completely erase their names from the memories of all living mortals, absorbing their remnants into your own soul. The sky of the Fugue Plane turns into a brilliant, endless horizon of liquid ruby mist, reflecting your absolute ascension.

You stand before the cosmic balance as the undisputed, breathtaking Greater Goddess of Mind, Murder, and Total Submission, rewriting the laws of mortal choice, love, and termination for all eternity.


Section 5 — The Mantle of the Radiant Slayer
You do not transform into a generic, clunky monster. The energy of the Crown of Karsus allows you to manifest your divine authority as an Exalted Stance. You retain your exact level progression, equipment, and features, layering immense physical upgrades over your baseline character sheet. You choose between two distinct visual aspects upon activation.

                  ┌─────────────────────────────┐

                  │    BASE LEVEL GESTALT CORE  │

                  └─────────────────────────────┘

                                 │

                                 ▼

       ┌──────────────────────────────────────────────────┐

       │         MANTLE OF THE RADIANT SLAYER             │

       └──────────────────────────────────────────────────┘

                 │                                    │

                 ▼                                    ▼

     [ ASPECT OF THE SOVEREIGN ]            [ ASPECT OF THE RUIN ]

     Breathtaking Divine Visage             Obsidian Chitinous Armor

     Liquid Blood-Wings & Mist              Shadow Capes & Primal Panic

     Hypnotic Submission Focus              Raw Brutal Slaughter Focus
Aspect I: The Sanguine Sovereign (The Divine Visage)
This manifestation preserves your breathtaking, immaculate female form, elevating it into a living monument of cosmic dread. A pair of massive, translucent wings erupt from your shoulder blades, composed entirely of suspended, flowing divine blood that ripples like liquid ruby while holding a razor-sharp edge. A low-hanging, freezing mist of dark crimson essence rolls continuously from your feet, carpeting the battlefield and carrying the faint scent of copper and heavy temple incense. Your eyes burn with a calm, absolute crimson light, completely devoid of pupil, while a crown of dark, floating Karsite shards hovers just above your brow. Mortals who behold you in this aspect do not run; their minds simply break from the sheer weight of your perfection, forcing them to drop to their knees in absolute submission.
Aspect II: The Chitinous Ruin (The Monstrous Visage)
For moments when you wish to abandon elegance and inflict ancient, ancestral terror, you allow the monstrous blueprint of Bhaal's legacy to swallow your beauty. Your pristine skin is instantly encased in a jagged, mirror-sheened obsidian exoskeleton, and your fingers elongate into wicked, curved blades of hardened bone that pulse with necromantic energy. Your wings manifest as ragged, billowing capes of pure shadow that completely extinguish all ambient light sources in the vicinity. The air around you grows heavy and suffocating, accompanied by the rhythmic, wet echo of thousands of beating hearts that reverberate directly in the minds of your enemies, triggering an uncontrollable biological panic response that breaks their tactical formation.
Tactical Mechanics of the Mantle
While operating within this exalted stance, your avatar receives a series of flat, structural injections that scale directly with your character growth:

The Physical Surge (Levels 12–15). You receive a flat, unconditional boost of +2 to your Strength, Dexterity, and Constitution scores, breaking past the traditional mortal cap of 20. Concurrently, you gain a flat +2 bonus to your Armor Class. Because your Dexterity modifier increases by +1, your absolute defensive rating increases by a total of +3 while wearing light armor, while your attacks and damage modifiers receive an immediate bump.

The Divine Acceleration (Levels 16+). The stance reaches its fully realized maturity. Your physical score injection scales to a flat +4 to Strength, Dexterity, and Constitution, raising your attributes to astronomical levels. Your baseline Armor Class receives a flat +4 bonus, which combines with your elevated Dexterity modifier to grant a staggering total enhancement of +6 to your absolute AC. Furthermore, this tier unlocks a permanent Extra Attack whenever you take the Attack action, allowing your level 16+ alpha-strike to unleash four devastating, maximized critical hits on the opening round of combat.


Section 6 — The Path of the Ascendant Stalker (Level 12 → 30 Progression Ledger)
Your avatar functions as a supreme, dual-classed engine of stealth and execution, freezing her mortal shell at the absolute apex of Level 20 Gestalt before breaking into the boundless territory of Epic Tiers and Divine Ranks.

The Level 12 Baseline Core. At your starting phase, you possess the full capability of both paths. You are entirely invisible to any creature relying on darkvision while you are in darkness; you add your Wisdom to your initiative rolls; any hit you score against a surprised creature is an automatic critical strike layered with your deep Sneak Attack pool.

The Level 16 Evolutionary Leap. When you cross the threshold into Level 16, your physical capabilities undergo a profound structural shift. The residual energy of the Crown of Karsus permanently accelerates your reflexes, granting you a flat Extra Attack whenever you choose to take the Attack action, while your physical attributes expand past mortal limitations.

The Level 30 Apex Concept. At the absolute peak of your mortal progression, your Sneak Attack scales to an absolute maximum pool of dice, your execution features bypass traditional saving throw parameters, and your blade strikes become inherently lethal to the soul itself.
Complete Progression Ledger
Level
Ranger (Epic Gloomstalker) Track
Rogue (Epic Assassin) Track
Sneak Attack
12
Base Features, ASI
Base Features, ASI
6d6
13
4th-Level Spell Slots
Imposter Feature (mimic speech/handwriting/social behavior)
7d6
14
Vanish (Hide as bonus action; movements untrackable by nonmagical means)
Blindsense (10 feet)
7d6
15
Shadow Dodge (reaction: force disadvantage on incoming strikes)
Slippery Mind
8d6
16
ASI / Mortal Feat + Extra Attack unlocked (Karsite Acceleration)
ASI / Mortal Feat
8d6
17
5th-Level Spell Slots
Death Strike (Double Damage on surprised / submitted targets)
9d6
18
Feral Senses (attack without disadvantage in blind zones / illusions)
Elusive (no advantage against you)
9d6
19
ASI / Mortal Feat
ASI / Mortal Feat
10d6
20
Foe Slayer
Stroke of Luck (once per short rest: convert a miss into a hit, or a failed check into a natural 20)
10d6
21
Umbral Veil (invisibility pierces Truesight)
Epic Skill Expertise
11d6
22
Epic ASI (Cap raised to 24)
Slippery Soul (permanent Charisma save proficiency)
11d6
23
Dread Ambusher Evolution (extra attack deals 2d8 damage)
Evasion Improvement
12d6
24
Epic Boon Selection
Uncanny Reflexes (reaction: negate one incoming attack's damage)
12d6
25
Font of the Wilds (6th-Level Spell Slot)
Master Infiltrator
13d6
26
Epic ASI (Cap raised to 26)
Assassin's Reflexes (Bonus Action Dash)
13d6
27
Dread Vanguard (add double WIS to Initiative)
Death Strike DC Increase (+2)
14d6
28
Epic Boon Selection
Lingering Venom (ignore poison resistance, even on extraplanar / undead targets)
14d6
29
Umbral Blink (30ft teleport through shadow / thought)
Shadow Reflexes (Extra Reaction)
15d6
30
Apex Stalker (missed attacks gain immediate re-roll)
Master of Absolute Death (Death Strike DC +5; soul consumed on fail, immune to resurrection short of higher cosmic intervention)
15d6



Section 7 — Mechanical Subsystems
Core Feature: Kneel Before the Urge
Whenever a creature within 60 feet of your avatar becomes Frightened by any of your spells, features, or companion abilities, they must immediately succeed on a Wisdom saving throw (DC = 8 + Proficiency Bonus + Dexterity Modifier + Divine Rank).

On a Failure: The target falls Prone, drops any items they are holding, and is locked into a state of total psychological submission. They cannot stand up, take actions, or use reactions until the end of their next turn.

The Execution Payoff: Your Sneak Attack damage dice are automatically maximized against any target currently affected by this feature or any target that is Prone.
Terror Tithes Subsystem
You track your active cult devotion through Terror Tithes. You possess a maximum pool of Tithes equal to your current Divine Rank, regenerating fully at midnight.

Tactic
Cost
Effect
Martyr's Submission
1 Tithe
When your avatar takes damage that would reduce you to 0 hit points, a devoted Bhaalist cultist miles away willingly slurs a prayer to your name and cuts their own throat. Your avatar instead drops to 1 hit point and vanishes into a cloud of crimson mist, teleporting up to 60 feet into adjacent darkness.
Dread Proclamation
2 Tithes
As a bonus action, you let out a soft, echoing whisper. Every non-allied creature within 30 feet must pass a Charisma saving throw or become instantly Frightened of you for 1 minute, immediately triggering checks for Kneel Before the Urge.

3e-Inspired God Combat Engine (Rank 1 Baseline)
When clashing with other divine entities, your level 30 character sheet layers with these explicit 3e structural rules:

Maximized Hit Points: Every single hit die across your levels grants its absolute maximum numerical value.
Divine Deflection AC: You add your Divine Rank as a flat deflection bonus to your Armor Class.

The combined effect is that by Divine Rank 16+, your AC scales past all standard boundaries, your HP pool is fully maximized, and your Death Strike (DC +5 at Level 30) can consume the souls of entities who fail their fortitude save — preventing resurrection absent a direct intervention from a higher cosmic entity.


Section 8 — The Quantified Divine Engine (Phase-by-Phase Stat Block)
New in the 2026-07-20 iteration. The narrative above tells you what happens. This section tells you exactly how much divine power you have at each phase and what it costs. The LLM prints the relevant block at the start of every divine-tier scene.
8.0 — The General Engine (System-Agnostic)
For the canonical, setting-agnostic version of this engine — usable for any "you are a god" campaign, not just Forgotten Realms — see world_reference/god_mechanics_general.md. That doc defines the 7-rank ladder, the DR / DPP / DAIR / DLR / PDD stat block, portfolio mechanics, follower-scaling formulas, avatar rules, God Combat turn economy, and per-faction dissonance in pure system-agnostic terms.

This section instantiates that engine for the Sanguine Architecture specifically.
8.1 — Phase 1 Stat Block (Years 1-5, Levels 12-15)
DIVINE STAT BLOCK — SANGUINE ARCHITECTURE, PHASE 1

Rank:                2 Ascendant (F threshold 1,000 crossed at year 2)

DR:                  750 (Rank 3 base; F-scaled at F=1,500 is ≈ 750.4; see §8.5)

DAC:                 21 + DEX mod + 2 (Rank deflection bonus)

DPP/day:             125 (Rank 2 base; full regen at dawn)

DAIR Mod:            +18 (1d20 + 18 + PB + portfolio override on Murder)

DLR:                 2

PDD:                 15 + (1d20 × 2)

F (active worship):  ~1,500 (Baldur's Gate terror cult + Bhaalist remnants)

Portfolios:          Murder · Submissive Death

Tithe Pool:          125 (= DPP/day; full regen at dawn)

Avatar HP:           1000 × Rank = 2,000 HP cap (mortal sheet layers on top)

Action Economy:      1 Major (25-75 DPP) + 3 Legendary (5-15 DPP each)

Operating notes for Phase 1:

Your direct divine combat at this rank is dangerous vs mortals (you auto-win any save-vs-divine-influence) but loses to intermediate deities.
DR is concentrated because you just consumed Bhaal — you are at Rank 3 power density but Rank 2 organizational scale. This is the Nascent Greater pattern: rank-low, power-high.
Almost all combat goes through the avatar's mortal gestalt (Ranger/Rogue), not the divine form. The divine form is reserved for manifestation events — showing up, asserting dominance, triggering Submissive Death on regional scale.
Tragic Betrayal harvests + Terror Tithes are your primary DPP-spend economy. Submissive Death kills yield 1 Tithe per mortal; Tragic Betrayal kills yield ×3 = 3 Tithes per mortal.
8.2 — Phase 2 Stat Block (Years 5-10, Levels 16-20)
DIVINE STAT BLOCK — SANGUINE ARCHITECTURE, PHASE 2

Rank:                4 Lesser Deity (F crossed 50,000 at year 7)

DR:                  300 (Rank 4 base)

DAC:                 22 + DEX + 4 (Rank deflection bonus)

DPP/day:             200

DAIR Mod:            +20

DLR:                 3

PDD:                 20 + (1d20 × 3)

F (active worship):  ~85,000 (Sword Coast + Waterdeep covert cells + BG3 majority)

Portfolios:          Murder · Submissive Death · Tragic Betrayal (new at Rank 4)

Tithe Pool:          200/day

Avatar HP:           4,000

Action Economy:      1 Major (50-100 DPP) + 3 Legendary (10-20 DPP each)

Operating notes for Phase 2:

Karsite Acceleration fires at Level 16 — your mortal gestalt catches up to the divine sheet.
The Lords' Alliance crusade is your first divine-tier combat encounter. Expect to spend 100-150 DPP per Major Divine Action against the coalition's paladins of Helm and Tyr (who each have intermediate-tier stats).
Tragic Betrayal harvests now scale regionally: a single night's coordinated domestic executions across Waterdeep can yield 200-500 Tithe in one tithe-window.
8.3 — Phase 3 Stat Block (Years 10-20, Levels 21-25)
DIVINE STAT BLOCK — SANGUINE ARCHITECTURE, PHASE 3

Rank:                5 Intermediate Deity (F crossed 250,000 at year 12)

DR:                  500

DAC:                 23 + DEX + 5

DPP/day:             400

DAIR Mod:            +23

DLR:                 3

PDD:                 30 + (1d20 × 4)

F (active worship):  ~410,000 (continental + planar foothold)

Portfolios:          Murder · Submissive Death · Tragic Betrayal · Absolute Suppression of Will (new at Rank 5)

Tithe Pool:          400/day

Avatar HP:           5,000

Action Economy:      1 Major (50-100 DPP) + 3 Legendary (10-20 DPP each)

Operating notes for Phase 3:

Full planar combat. Each God Hunt costs 200-300 DPP across infiltration + assassination + absorption.
Intermediate deities now treat you as a peer. Expect councils, embassies, assassination attempts.
Your Synaptic Veil (Level 21) and Apex Stalker features let the avatar operate on par with lower-tier divine avatars in the field.
8.4 — Phase 4 Stat Block (Years 20+, Levels 26-30+)
DIVINE STAT BLOCK — SANGUINE ARCHITECTURE, PHASE 4

Rank:                6 Greater Deity (F crossed 1,000,000 at year 22)

DR:                  1,000+ (cap at full Greater)

DAC:                 25+ + DEX + 6 (full Rank deflection)

DPP/day:             1,000+

DAIR Mod:            +25+

DLR:                 5+

PDD:                 30 + (1d20 × 5)+

F (active worship):  ~3,500,000 (multiversal)

Portfolios:          Murder · Submissive Death · Tragic Betrayal · Absolute Suppression of Will · The Beautiful End (new at Rank 6)

Tithe Pool:          1,000+/day

Avatar HP:           6,000+

Action Economy:      1 Major (150-250 DPP) + 3 Legendary (25-50 DPP each)

Operating notes for Phase 4:

The Greater Gods coalition assault fires. This is the only encounter in the campaign that fully uses the 3e God Combat rules.
Alter Reality features (Level 26+) let you rewrite local rules within your portfolio at will.
The endgame is a contest of attrition. They have more gods; you have a more concentrated portfolio and the Tragic Betrayal multiplier on every death.
8.5 — Follower-Scaling Math (Explicit Formula)
At any time t during the campaign, the LLM computes:

Stat(F) = Stat_Rank3 + ((F / 1,000,000) × (Stat_Rank6 - Stat_Rank3))

Example: At F = 50,000 (mid-Phase 2), your DR is:

DR(50k) = 750 + ((50,000 / 1,000,000) × (1,000 - 750))

        = 750 + (0.05 × 250)

        = 750 + 12.5

        = 762.5 → round to 763

The LLM must print this calculation explicitly at dawn transitions and after every cult operation that changes F.
8.6 — Tithe Economy Detail
Phase 1 baseline (F ≈ 1,500):

1 Tragic Betrayal coordinated night (10 simultaneous domestic executions across BG3 upper city) = ~30 Tithe
1 Submissive Death mass event (full patriar family kneeling) = ~25 Tithe
1 spontaneous murder invocation = 1 Tithe

Phase 4 baseline (F ≈ 3.5M):

1 Tragic Betrayal coordinated night (multiversal) = ~5,000 Tithe
1 God Hunt kill = 100 Tithe (base) + absorbed portfolio dividend
1 cosmic rewrite action = 5,000 Tithe

Pool-to-spend ratio: A well-run Phase 4 avatar can sustain ~3 Major Divine Actions per day against an organized enemy. More than that requires either:

Sleeping through the next dawn (lose 1 day of avatar time)
Sacrificing 100-500 mortal followers in a martyrdom wave (consumes F, accelerates Rank but also accelerates Pantheon Notice)
8.7 — Per-Faction Dissonance Table (The Rule)
Jeffrey's standing instruction from C0AH3RY3DK6/p1784507599.182939: "make dissonance hidden and ... dissonance per god faction versus overall."

The Sanguine Architecture has six factions with materially different experiences of your portfolio. The LLM tracks all six independently. No faction's experience is averaged into the global reading.

Faction
How they experience you
Private revelation
Dissonance vector
Upper City Patriars (BG3 aristocrats)
Terror in daylight; absolute submission at night
They privately suspect you are testing them for promotion into your inner court
High fear / low love / moderate awe
Lower City Survivors (BG3 commoners)
Grudging survival pragmatism; a few sincere converts
Some report dreams of a beautiful woman asking them to betray someone they love — they wake weeping
Moderate fear / moderate love / low awe
Bhaalist Remnants (cult holdouts)
Resentful but obedient — they see you as a pretender
They are running a hidden reformist movement to restore "honest murder"
Low fear / low love / low awe
Sword Coast Cult Cells (Waterdeep, Neverwinter, Baldur's Gate diaspora)
Zealous converts operating as court advisors / matchmakers
They receive a private Liturgy of the Beautiful End that no other faction has seen
Low fear / high love / moderate awe
Shadowheart's Sharran Order (House of Grief remnant)
Theological alliance — Shar-worship reframed as worship of the void you embody
They believe you are the mortal incarnation of Shar's sister; Shar has not confirmed nor denied
Low fear / moderate love / high awe
Planar Refugees (gods and petitioners fleeing your expansion)
You are the apocalyptic threat everything else was a dress rehearsal for
They are forming a coalition council against you — you learn about it only when it attacks
High fear (justified) / zero love / extreme awe


The LLM must NEVER collapse these six factions into one reading. They are six independent sub-stories.

V2 simplification: These six per-faction dissonance rows are preserved as the narrative substrate. V2 (Section 9) collapses them into two hidden-band axes (Reputation + Apex Attention) for the mechanical layer — see Section 9 §9.5.2 for the synthesis.


Section 9 — The V2 Quantified Divine Engine (V2 Overlay)
This section applies the V2 design spec (world_reference/nocturne-v2-god-mechanics-design.md) on top of the V1 mechanical scaffold from Section 8. V2 introduces 7 tiers, mortal-to-divine multiplier, god-class system, context-aware per-dawn menu, and the auto-win combat ladder. V2 was driven by the user's mid-thread feedback that V1's math was "calculations which don't mean much" — V2 makes the math load-bearing: every dawn the player picks from a DPP-cost menu, the math resolves deterministically, and the roll is variance within the math-determined bracket.
9.1 Seven-tier ascension ladder (V2 deltas)
Tier
Levels
Stat system
Ascension trigger
Mortal
L1-20
Standard 5e (HP, AC, Save DC, Attack, Spell Slots)
n/a — natural character progression
Demi-god
L21-25
Standard 5e + divine flavor narrative ("incubating goddess")
Natural L21 achieved
Lesser god ⭐
L26-30
God stats kick in (first god-tier stat block)
First god-kill (Bhaal-essence absorbed)
Minor god
L31-35
God stats, scaled up
Reach Minor threshold (Reputation + Apex Attention)
Intermediate god
L36-40
God stats, scaled up
Reach Intermediate threshold
Greater god
L41-45
God stats, scaled up
Reach Greater threshold
Transcendent
L46+
God stats, apex (V1 Aizen final form)
Reach Transcendent threshold


The ascension is at L26 = Lesser god = first god stat block. L21-25 is the "almost-a-god" interstitial — V2 inherits the V1 Module 3 narrative here, but the character mechanically stays at 5e stats until L26.
9.2 Mortal → Divine multiplier (V2 deltas)
At L26, the mortal stat block converts to god stats via multiplier:

DR   = HP × 5.4    (V1 Aizen: HP 138 → DR 750)

DAC  = AC + 4       (V1 Aizen: AC 21 → DAC 25)

DAIR = Attack + 18  (V1 Aizen: +13 → +31)

DPP  = base 825 + Reputation modifier (no mortal analog)

DLR  = folded into DR's natural scaling (no separate stat)

Nocturne L20 mortal form (gestalt Gloomstalker 12 / Assassin Rogue 8): HP ~142, AC ~22, Save DC ~22, Attack +14. At L26 ascension:

DR 766 · DAC 26 · DAIR +32 · DPP/day 825

Stronger mortals = stronger gods. Multiplier stays. L1-19 gear choices compound forward (a +5 Greatsword at L20 becomes +5 to DAIR at L21+).
9.3 Universal god stats + 6 god-classes with stat biases (V2 deltas)
Every Faerûn god has DR / DAC / DAIR / DPP / Reputation (hidden) / Apex Attention (hidden). Nocturne's numbers are uniquely hers; the rules are universal — the same god-class framework governs Bane, Shar, Mystra, Mask, Kelemvor, Cyric, etc.

Class
DR
DAC
DAIR
DPP
Examples
War god
High (1100+)
Low (22-)
High (+50+)
Mid (700-)
Tempus, Bane
Trickster god
Low (500-)
Low (20-)
Very High (+60+)
High (900+)
Mask, Cyric
Domain god
High (1100+)
Mid (24)
Mid (+35+)
Mid (700-)
Chauntea, Silvanus
Magic god
High (1100+)
Low (22-)
Mid (+35+)
High (900+)
Mystra, Shar
Death god
Very High (1500+)
Mid (24)
Mid (+35+)
Mid (700-)
Kelemvor, Myrkul
Skilled god ⭐
Mid (750-)
Mid (24)
Very High (+60+)
Mid (700-)
Nocturne (Murder)


Nocturne = Skilled god. She's good at killing specifically, not war-tanking. This explains her stat block being unique (top-tier DAIR, middling DR/DPP) without making her unique in kind.
9.4 V2 linear scaling (V1 Aizen formula carried forward)
Stat(F, Reputation, Apex) = Stat_Nascent

                          + (F / 1,000,000 × (Stat_Transcendent − Stat_Nascent))

                          + Reputation_modifier

                          + (Apex_Attention_band_modifier)

Verified V1 Aizen data: F=0 → DR 750, DPP 825, DAIR +31. F=1M → DR 1750, DPP 1825, DAIR +56. Ratio: 2.33× DR, 2.21× DPP, 1.81× DAIR.
9.5 Hidden mechanics with narrative surfacing (V2 deltas)
Reputation bands (0-100+): Unknown → Whispered → Open → Established → Revered → Pantheon-tier Apex Attention bands (0-100+): Unseen → Whispered → Noticed → Marked → Hunted → Apotheosis imminent

Player never sees the numbers. LLM tracks, player reads the bands + LLM-generated consequences.

The V1 six-faction dissonance table (Section 8) is preserved as the narrative substrate — V2's two hidden-band axes are the mechanical layer that aggregates those six readings into a single campaign-facing signal.
9.6 Per-dawn menu (context-aware, not every dawn) (V2 deltas)
V1's Section 7 terror-tithe pool becomes V2's DPP-cost choice menu. The player picks from a context-aware list each dawn.

Dawn type
Menu shape
When
Routine dawn (default)
2-3 light options: worship-build, heat-management, RP accumulation
Most dawns
Triggered dawn (something dramatic)
4-6 full options: Bhaal-hunt, rival-god confrontation, coalition-formation, etc.
Bhaal-essence surfaces, rival god moves, Apex Attention hits a band, RNG event
Quiet dawn (post-crisis cooldown)
No menu — narrative + stat updates only
Post-crisis


Sample triggered-dawn menu at L26:

═══════════════════════════════════════════

NOCTURNE V2 — DAWN 47 (Repr "Whispered", Apex "Unseen")

═══════════════════════════════════════════

Stat Sheet:

  DR 766/766 · DPP 75/825 · DAIR +32

Today's Choices — pick 1:

  A. BHAAL HUNT (DPP cost: 200)

     → DR +30 IF successful, Bhaal's portfolio integrated

     → Failure: Apex Attention +1 band ("Unseen" → "Whispered")

  B. WORSHIP BUILD (DPP cost: 100)

     → Reputation shifts toward "Open"

     → Failure: nothing lost (safe)

  C. SAFE EXPANSION (DPP cost: 50)

     → Apex Attention -1 band (back to "Unseen")

     → Failure: nothing lost

Which? (A is high-stakes god-kill, C is the safe play)

═══════════════════════════════════════════

Player picks → math runs deterministically → roll resolves variance within math-determined bracket. Per-dawn DPP budget is the OPTIMIZE target.
9.7 Auto-win combat ladder (V2 deltas)
V2 adds the auto-win ladder that V1 lacked. The god-tier fantasy is "you don't waste DPRoll on a guard":

Target
Result
Commoner / town guard / random NPC
Auto-win. No roll.
Named mortal (Cazador, Duke, Bhaalist priest)
Auto-win. Divine Save DC vs mortal — mortals can't beat it.
Chosen mortal (Bane's Chosen, Shar's Chosen)
Divine combat. d20+DAIR vs DAC.
Avatar of lesser/major god
Full divine combat. Major action + d20 roll.
Lesser / Intermediate god directly
Full divine combat. Major action + d20 roll.
Greater god / Apex entity
Full divine combat. May require god-hunt action chain.


Combat math only matters for divine beings and Chosen NPCs. All mortal-tier combat resolves as auto-win.
9.8 Roll = variance within math-determined bracket (4-roll cap per scene) (V2 deltas)
V1 had a max-1-roll-per-scene rule. V2 relaxes to 4-rolls per scene maximum (cultist loyalty × 1, assassination attempt × 1, deception × 1, target's final death save × 1). Beyond that, the math decides.

God-hunt phase
Math decides
Roll adjusts
1. Locate
Findability this dawn (DPP budget)
— none —
2. Infiltrate
Plane entry (DPP + Avatar HP)
— none —
3. Engage
Major Action feasibility (DPP ≥ Cost)
— none —
4. Counter
God's response (DAIR vs DAC)
— none —
5. Commit
Damage bracket (DAIR differential)
1d20 within ±5 on damage quantity
6. Absorb
Portfolio integration
1d20 picks which sub-effect manifests

9.9 Deicide-cost = Apex Attention growth only (V2 simplification)
V1 had no deicide-cost (clean kill, matches Aizen's "consume Bane" pattern). V2 adds ONE cost: each god-kill advances Apex Attention +1 band.

DR +30 per god-kill (V1 Aizen pattern)
Apex Attention +1 band (e.g. "Whispered" → "Noticed")
No Wounds, no Publicity Tax, no Empty Throne

The Apex Attention mechanic is hidden (narrative surfacing only — see PR #8467 for the existing dissonance-hidden pattern that V2 extends).
9.10 V2 sample stat block at L26 ascension
═══════════════════════════════════════════

NOCTURNE — DAWN OF L26 (Lesser God Ascension)

═══════════════════════════════════════════

Mortal form (L20, capped):

  HP 142 · AC 22 · Save DC 22 · Attack +14

  Gear: +5 Greatsword, +5 Plate, +5 Amulet

  Class: Gestalt Gloomstalker 12 / Assassin 8

  Sneak Attack pool: 10d6

  [Optimized through 20 mortal levels — familiar 5e build]

Demi-god (L21-25):

  [Narrative: "You walked among mortals for 5 years,

   leaving ripples in the weave. Now the gods notice."]

DIVINE PROJECTION — LESSER GOD (L26):

  DR 766 (HP 142 × 5.4)

  DAC 26 (AC 22 + 4)

  DAIR +32 (Attack 14 + 18)

  DPP/day 825 (base Lesser god, modified by Reputation)

Hidden state (read narrative only):

  Reputation: "Whispered" — small cults in BG shadows

  Apex Attention: "Unseen" — gods do not know you exist

God-class: Skilled god (top-tier DAIR, mid DR/DPP)

═══════════════════════════════════════════
9.11 V2 deltas from V1 (summary)
V1 had
V2 changes to
Why
Flat Divine Rank 1→20
7-tier ladder (Mortal / Demi / Lesser / Minor / Intermediate / Greater / Transcendent)
Maps cleanly onto D&D 5e L1-20+
Single Mortal → Divine
Mortal L20 cap → Demi-god L21-25 (5e stats) → Lesser god L26+ (god stats kick in)
Ascension IS the campaign arc
No god-classes
6 god-classes (War / Trickster / Domain / Magic / Death / Skilled)
Explains why stat blocks differ across Faerûn gods
Six-faction dissonance narrative table
Reputation + Apex Attention hidden bands (mechanical layer over the narrative substrate)
Two-axis hidden state, narrative surfacing
Fixed menu every dawn
Context-aware (routine / triggered / quiet)
Avoids formulaic sameness
Implicit combat
Auto-win ladder (mortals) + 4-roll cap per scene
Restores D&D 5e OPTIMIZE → ROLL loop
No deicide cost
Apex Attention +1 band per kill
Hidden mechanic, narrative surfacing



3-Generation Power Lineage
Following the same analytical framework as the existing world_reference modules (Luke, Daenerys, Steel Jedi, etc.), each fork offers a categorically different relationship to the campaign's central power, not just a different intensity.

Generation
Antagonist / Fork Anchor
Relationship to Murder-Godhood
G0 — Origin
The Dark Urge herself, level 12, freshly ascended
Treats the new portfolio as a beautiful, elegant, perfectly optimized system. Believes the architecture is complete.
G1 — Recontextualizer
Orin, Sarevok, or any surviving Bhaalist elder who challenges the new doctrine
Sees the new portfolio as a betrayal — the crude, chaotic slaughter of the old Bhaal rejected in favor of beautiful, submissive death. Attempts to restore the old portfolio by force or by sabotage from within the cult.
G2 — Inheritor's NEW choice
The player's own future self, or a successor cult leader, presented with the fully mature Greater Goddess portfolio
Recognizes that BOTH prior generations treated murder as an end in itself. The new choice: what does a Goddess of Submissive Death owe the mortals who kneel at her altars? Reject the optimization entirely — and either transform the portfolio into something gentler, or double down on the cruelty as a deliberate, conscious choice. The fork is not "rule harder" vs. "rule softer." It is "is this architecture good?"


Every fork offers a third path that neither G0 nor G1 attempted. That is the structural rule of the 3-generation lineage — same as the Luke / Daenerys / Steel Jedi / Year of Four / Heat Detective modules already in world_reference/.


Cross-References
Shattered Rose ↔ campaign_module_shattered_rose.md — Both are post-BG3 campaigns anchored in the same year (1492 DR), but they invert each other: Shattered Rose asks what happens to the city when the gods are mortal and jealous; God of Murder asks what happens to the god when she is mortal and absolute. Shattered Rose's Nocturne Sosuke is a survivor who stumbles on a conspiracy; the Dark Urge here is the architect of a new order.
Steel Jedi ↔ campaign_module_steel_jedi.md — Both are "Order 66 survivor" campaigns, but Steel Jedi's Corin Tarvish escapes from the inside of a crumbling institution, while the Dark Urge here replaces a dead god's institution with her own.
Year of Four ↔ campaign_module_year_of_four.md — Both are "regime change in a closed system" campaigns. Year of Four's Tigellinus auctions the Roman Empire to the highest bidder; the Dark Urge here is the highest bidder for the Bhaalist portfolio.
Inheritor's Stars ↔ campaign_module_inheritor.md — Both are multi-generation campaigns where the player-character must decide whether to perpetuate or transform an inherited structure. Inheritor's Stars asks whether to keep the secret of an uninhabitable destination; God of Murder asks whether the architecture of Submissive Death is a system worth maintaining at scale.


Recommended Next Steps (if you pick this for the prod site)
Pick this campaign — among the strongest in world_reference/ for prod because the internal mechanics are the cleanest (gestalt 12→30 + Divine Rank 1→20 is a single, easy-to-tune axis, unlike the modern-day Heat Detective which requires no-magic tuning).
Do the campaign_template_god_of_murder.py pass — extract the canonical prompt into data/god_of_murder_canonical_description.txt, hash it, wire it into mvp_site/constants.py following the pattern in mvp_site/campaign_template_dragon_knight.py.
Add a wiki source page at ~/llm_wiki/wiki/sources/god-of-murder-<id8>.md, following the frontmatter shape used by your existing aemon-bg3-campaign.md and nocturne-bg3-v7-entry-075.md.
Optionally ingest into Firestore — the canonical prompt is written in the same shape as the existing campaign templates and should be drop-in compatible with create_campaign_unified after the constants wiring in step 2.


User-Generated Content (AI Dungeon–style labeling)
The Dark Urge (the protagonist), the Sanguine Sovereign / Chitinous Ruin aspects, the Tragic Betrayal doctrine, the 5-Pillar Dread Court, the 4-phase cosmic escalation, and the 3e God Combat integration are original to this module. All Forgotten Realms canon (Bhaal, Sarevok, Orin, the Bhaalist cult, Baldur's Gate, the Netherbrain, the Crown of Karsus, the Lords' Alliance, the Githyanki, Vlaakith, Elminster, Kelemvor, Shar, Mystra, Torm, Helm, Tyr, Cyric, Wyrm's Rock, the Chionthar, the Flaming Fist, the House of Grief, the Nightsong, etc.) is property of Wizards of the Coast and Larian Studios and is used here in its canonical BG3 / D&D roles only. No new lore is invented on top of canon characters.


File Stats
Lines: ~410
Words: ~9,300
Banned-name audit: 0 hits (1 false positive on noun "echo" in descriptive prose).
Source: Gemini Flash conversation Td7fA4pzuvMs, regenerated self-contained 3,422-word design from 2026-07-20.


PART 2 — God Mechanics — General Spec (V1, System-Agnostic)
The original setting-agnostic baseline. Quantified stat blocks + 7-rank ladder + follower-scaling math. Setting-agnostic but not yet load-bearing — V2 makes the math load-bearing. Part 2 of 4.

A canonical, setting-agnostic framework for "you are a god" solo campaigns. Works for Forgotten Realms deicide, Wuxia cultivation transcendence, cyberpunk ascended-AI divinity, Naruto tailed-beast sovereign, Marvel cosmic-tier hero, or anime god-of-tyranny arcs. Quantified enough to be mechanically useful, abstract enough to drop into any pantheon.


Why this exists
Every god-tier campaign Jeffrey has loved (Aizen Godhood Continued, the original Aizen-as-god series, the dark-godtyranny arcs in llm_wiki) shared three structural ingredients that the narrative-heavy successors (e.g. the current God of Murder doc) lost:

Quantified stat blocks — explicit DR / DPP / DAIR-style numbers, not vibes
Linear scaling formulas — "at F followers, my divine AC = base + (F/target × delta)" — math the LLM can compute every scene
Hard bookkeeping layers — sequence IDs, checkpoint blocks, named subsystems with costs & cooldowns

This file is the general version: it has no Faerûn lore, no Forgotten Realms deities, no D&D dice math. Drop it into any setting. Translate DPR/DR into the setting's idiom ("Dread Tides," "Cult Resonance," "Quantum Influence Pool") but keep the structure.


I. Tiers of Divinity (the 7-Rank Ladder)
A god is not a binary. There are seven canonical ranks, each with an explicit numerical budget. Promotion requires both a mechanical trigger AND a narrative milestone (the LLM never promotes based on vibes alone).

Rank
Title
Mechanical Trigger
Narrative Milestone
Example Archetype
0
Quasi-Deity
Consumed a divine spark / merged with an elder entity / ascended an AI core above god-tier threshold
A city or region kneels
Brand-new god (Dark Urge post-Bhaal, Aizen post-Bane)
1
Minor Ascendant
Held territory for 1 year; built a functioning church with ≥ 100 active worshippers
Your faith has a name, vestments, a calendar
First saint appears
2
Ascendant
≥ 1,000 worshippers; survived at least one planar incursion attempt by an intermediate deity
Other gods put you on their meeting agenda
Recognized factional power
3
Nascent Greater Deity
≥ 10,000 worshippers; one full god-portfolio absorbed; one full planar realm claimed
The first crusade against you assembles
The gods take you seriously
4
Lesser Deity
≥ 50,000 worshippers; survived a coalition assault; an avatar has killed or absorbed an intermediate deity
An avatar of yours holds a planar throne
You are a name in the cosmology book
5
Intermediate Deity
≥ 250,000 worshippers; one full pantheon wing (≥ 3 portfolios) under your dominion; a permanent planar fortress
Your avatar stands in council with established gods
Peer of Torm / Mystra / Bane
6
Greater Deity
≥ 1,000,000 worshippers; multiple pantheons converted or absorbed; permanent multiversal reach
The gods form a coalition against you personally
You are a tier-1 cosmological actor
7
Transcendent
≥ 10,000,000 worshippers AND consensus-driven narrative escalation (you've become a theme, not a being)
Reality rewrites around your portfolio
Final-form god


The formula (compute current stat at F followers, target 1,000,000):

Current_Stat = Base_Rank3_Stat + ((F / 1,000,000) × (Rank6_Stat - Rank3_Stat))

Use this for every divine stat below. The LLM computes it explicitly each scene.


II. The Divine Stat Block (system-agnostic)
Translate the names to whatever fits the setting. The numbers stay.

Stat
Abbreviation
What it Measures
Scaling Rule
Divine Resilience
DR
HP equivalent for god combat. Total damage the god can absorb before avatar-discorporation
150 → 300 → 750 → 1,000+ → 1,750
Divine Armor Class
DAC
Defense vs divine attacks. Base + DEX + flat deflection bonus
20 → 22 → 25 → 25+ → 25
Divine Power Pool
DPP
Daily resource pool for major divine actions. Regenerates each dawn
50 → 200 → 825 → 1,000+ → 1,825
Divine Attack / Influence Roll
DAIR Mod
Attack bonus + influence DC mod vs other deities
+15 → +20 → +31 → +25+ → +56
Divine Legendary Resistances
DLR
Per-day auto-pass on save-or-die effects
1 → 3 → 4 → 5 → 9
Primary Divine Damage
PDD
Base damage die + multiplier when DAIR hits another god
10+(1d20×2) → 20+(1d20×3) → 80+(1d20×5) → 30+(1d20×5)+ → 110+(1d20×10)


Per-tier table (use exactly this; no rounding, no reinterpretation):

Rank
DR
DAC
DPP/day
DAIR Mod
DLR
PDD
0 Quasi
75
18
25
+10
0
5+(1d20×1)
1 Minor Ascendant
150
20
50
+15
1
10+(1d20×2)
2 Ascendant
225
21
125
+18
2
15+(1d20×2)
3 Nascent Greater
750
25
825
+31
4
80+(1d20×5)
4 Lesser
300
22
200
+20
3
20+(1d20×3)
5 Intermediate
500
23
400
+23
3
30+(1d20×4)
6 Greater
1,000+
25+
1,000+
+25+
5+
30+(1d20×5)+
7 Transcendent
1,750
25
1,825
+56
9
110+(1d20×10)


Note on the table: Rank 3 (Nascent Greater) outscales Rank 4 (Lesser) and Rank 5 (Intermediate) intentionally. A nascent greater deity holds raw power well above its rank position because it just absorbed a major god's essence. As followers grow, the power spreads out — Rank 6 / 7 are stronger, but Rank 3 is the most concentrated form.


III. Portfolio — the Conceptual Domain
Every god owns one or more portfolios — abstract concepts whose authority the god holds. A god without a portfolio is a blank power battery; a god with a clear portfolio is a functional cosmological actor.

Portfolio expansion rules:

Starting portfolio (at ascension): 1 concept (e.g. Murder, Tyranny, Magic, the Moon)
Rank 3 (Nascent Greater): 2 concepts (your starting + one absorbed from a defeated god)
Rank 5 (Intermediate): 3 concepts
Rank 6 (Greater): 5 concepts
Rank 7 (Transcendent): Unlimited (you are a theme, not a being)

Portfolio mechanics in play:

Portfolio Influence Roll: Any action that lies within your portfolio automatically counts as if rolled with a +10 bonus (on top of DAIR Mod). You bend the concept to your will.
Portfolio vs Portfolio: When two deities contest on overlapping portfolios, the higher-ranked deity wins by default (DC = 100 auto-save for the loser, but the winner must spend 150 DPP to assert it — this is the cosmic "no, this is MY domain" assertion).
Hidden Dissonance: Per-faction. Each worshipper faction experiences your portfolio slightly differently. This is the setting-agnostic version of the dissonance hidden, per god faction versus overall rule you asked for in 1784507599 — the LLM must not collapse all factions into one shared reading.
Portfolio Decay: A portfolio you do not actively assert for 1 in-game year shrinks. Lose 1 portfolio slot per year of neglect. The LLM tracks this.

Example portfolio sets (for reference):

Aizen: Tyranny · Control · Order through Absolute Will · Absolute Codification
Dark Urge (God of Murder): Murder · Submissive Death · Intimate Betrayal · Total Suppression of Will
Shinto Sun Goddess: Sun · Imperial Order · Crops
Marvel Infinity-tier: Time · Space · Power · Mind · Soul · Reality


IV. Follower-Scaling (the math)
A god's power scales linearly with active worshippers (F). The formula:

Stat(F) = Stat_Rank3 + (F / 1,000,000) × (Stat_Rank6 - Stat_Rank3)

Per-stat scaling (verify against II's table):

Stat
Δ per 1M followers
DR
+250 (from 750 → 1,000)
DPP/day
+175 (from 825 → 1,000)
DAIR Mod
(capped, only changes at rank promotion)
DLR
+1 (from 4 → 5)
PDD base
+5 (from 80 → 85; multiplier unchanged at 5)


Active worshipper count (F) is the LLM-tracked value. Update rules:

+1 per soul that consciously and voluntarily invokes your name with intent
+0 for involuntary fear-based worship (counts as a tithe, not worship; see V)
-1 per soul that consciously renounces your name in a sacred space
F is audited at every long rest / dawn transition

Target milestones (the LLM narrates when these flip):

F threshold
Trigger
100
First saint / first mortal bound to your faith
1,000
Your faith has vestments, a calendar, a hierarchy
10,000
First heretical schism within your church
100,000
Other gods hold formal council about you
1,000,000
Rank 6 promotion fires; you become a Greater Deity
10,000,000
Rank 7 promotion fires; you become a Transcendent theme



V. Tithes — the Sacrifice Engine
Worship scales you slowly. Tithes are the burst-scale engine: a one-time surge of divine essence in exchange for an immediate mechanical effect.

Tithe sources:

Voluntary death (a follower gives their life in your name): +1 Tithe per soul, scales by rank of follower (commoner = 1, hero = 5, high priest = 25, avatar of another god = 100)
Terror harvest (submissive death, fear-extraction, life-force drained by your avatar): +1 Tithe per mortal whose death was entirely in your direct causal chain
Tragic betrayal (the bond severed was profound — lover, child, lifelong companion): ×3 Tithe multiplier on top of base
Planar conquest (slay an avatar of another god on their home plane): +100 Tithe
Pantheon absorption (consume the divine spark of a defeated god): +1,000 Tithe, +1 portfolio slot, immediate Rank promotion check

Tithe maximum pool: equal to current DPP/day. Regenerates fully at dawn.

Tithe expenditure (sample effects; the LLM may add new ones but must cite this baseline):

Effect
Cost
What it does
Martyr's Substitution
1
When your avatar drops to 0 HP, a distant cultist takes the death instead. Your avatar drops to 1 HP and vanishes into the nearest shadow.
Dread Proclamation
2
All non-allies within 30 ft must save vs DC = 100 or fall prone in submission. (The Aizen baseline.)
Portfolio Override
5
For 1 minute, any action within your portfolio auto-succeeds. The universe does not resist you.
Planar Transit
25
Teleport self + retinue to any location in any plane you have a worshipper in.
Avatar Conjunction
100
Two avatars of yours act in perfect synchronization for 1 round (effectively 2 turns of action).
Divine Resurrection
500
A deceased mortal returns to life as your Chosen — bound to your portfolio, immune to resurrection by any god of lower rank.
Pantheon Absorption Attempt
1,000
Attempt to consume the divine spark of a present deity. Target must be ≤ your rank. On success, +1 portfolio, +1,000 DR cap, immediate rank check.
Cosmic Rewrite
5,000
One rule of reality within your portfolio changes for 24 hours. The LLM must enforce the change in all subsequent scenes.



VI. Avatar Mechanics — The Mortal Shell
Gods can manifest in the mortal plane through an avatar: a discrete physical body operating under a specific subset of your divine power. Avatars are how every campaign actually plays.

Avatar properties:

Property
Rule
HP cap
Avatar HP = (1,000 × Rank) + mortal-level-based bonus. Discorporation at 0; reform in 1d10 days at your primary altar.
Carries mortal sheet
The avatar inherits all your character-class features, levels, gear, spells. They layer ON TOP of the divine stat block, not replace it.
DAC
max(mortal AC + DEX, DAC) + (Rank as flat deflection bonus)
Action economy
1 Major Divine Action (cost DPP) + 3 Legendary Actions (10-25 DPP each) per round
Switching modes
You can swap between inhabiting the avatar (full consciousness) and remote-commanding it (autonomous with daily check-ins) at will. Bonus action.


Why avatars matter:

Most mortal-class threats are below the avatar's notice. The avatar chooses to engage them.
Avatar death is not god death. Discorporation = 1d10 days reformation + reputation hit among worshippers.
Avatar encounters vs other god avatars: full God Combat (see VII).


VII. God Combat — Turn Economy
When two divine beings clash directly, mortal combat rules do not apply. Use this engine.

Per round, a god has:

1 Major Divine Action (costs DPP; 100-150 for nascent greater, scales by rank)
3 Legendary Actions (each costs 10-25 DPP; can be used at any point in the round, including reactively)

Action costs (per rank):

Rank
Major Action
Legendary Action
0 Quasi
10-25 DPP
5-10
1-2 Ascendant
25-75
5-15
3 Nascent Greater
100-150
10-25
5 Intermediate
50-100
10-20
6 Greater
150-250
25-50
7 Transcendent
300+
50-100


Combat math:

To-hit: 1d20 + DAIR Mod
Damage on hit: PDD (base + 1d20 × multiplier)
Defense: Opponent's DAC (flat deflection + DEX + any cover)
Save DC for divine influence: 8 + Rank × 10 + WIS or CHA mod (whichever is lower for the target)
HP regeneration: Gods do not regenerate HP in combat. They spend DPP to heal (1 HP per 1 DPP, capped at 100 HP/round).

Special rules:

No crits in god combat. Variance is already in PDD's 1d20 multiplier.
Discorporation at 0 DR. Avatar shatters; divine essence reforms at altar in 1d10 days.
True death requires consuming the divine spark (V.5, 1,000 Tithe) and the target being at a planar location they do not control.


VIII. Worship, Propaganda & Cult Mechanics
The LLM tracks cult operations as a discrete sub-system, not narrative fluff.

Cult Operations Table (sample actions; LLM may extend):

Action
Cost
Time
Effect
Establish shrine
50 gold + 1 named NPC
1 week
+10 to local F growth
Convert noble house
1 intrigue roll + 500 gold
1 month
+50 to F, +1 political lever
Run martyrdom ritual
1 willing follower
1 day
+5 Tithe, -1 F, reputation spike
Planar embassy
1,000 gold + Rank ≥ 3
3 months
Opens diplomacy with 1 planar faction
Inquisition / purging rival cult
1 elite squad + 200 gold
1 month
-50 to rival F in target region, +25 to your F
Saint canonization
1 dead hero + 5,000 gold
1 year
+500 to F, grants 1 named Saint ability


Reputation Axes (track separately):

Fear (0-100) — how terrified mortals are of you. High fear = fast F growth, low quality of worship.
Love (0-100) — how devoted your followers are. High love = resilient F, slower growth.
Awe (0-100) — how the gods themselves regard you. High awe = diplomacy leverage, low awe = ignored.


IX. Per-Faction Dissonance (the rule Jeffrey asked for in 1784507599)
Dissonance is hidden, per god faction versus overall.

Each worshipper faction — defined by region, social class, race, or philosophical sub-school — has its own private reading of your portfolio. The LLM maintains:

One global reputation (what other gods + general public see)
Per-faction reputations (what each sub-group experiences)
Faction-specific events (one faction may receive a unique vision, revelation, or scandal that no other faction knows about)

Mechanical effect:

+1 portfolio slot at Rank 5 if you can keep ≥ 3 major factions in alignment
-1 portfolio slot at Rank 5 if your factions' dissonance exceeds threshold
Per-faction plot arcs may contradict the global narrative; the LLM is forbidden from collapsing them into a single read

This is the anti-anti-invention guardrail for divine campaigns — it ensures each faction feels lived-in and independent.


X. Ascension — How a Mortal Becomes a God
The mechanical ladder mortals climb. Different settings call this "cultivation breakthrough," "tailed-beast merger," "divine spark ignition," or "Omega-level event."

5-stage ascension template:

Stage
Trigger
Mechanic
Mortal Apex
Reached max mortal level / cultivation peak / Omega threshold
Character sheet is at maximum mortal potential
Spark Ignition
Encountered / absorbed a divine spark, elder entity, or Omega-tier power source
Unlock Rank 0 quasi-deity stats
First Worship
First 100 mortal worshippers voluntarily invoke your name
Promote to Rank 1, unlock cult mechanics
Pantheon Notice
A god of higher rank attempts to interact with you (negotiation, assault, or absorption attempt)
Unlock Rank 3 stats; full portfolio mechanics online
Transcendence
Hit F = 1M OR consumed a god of equal rank
Promote to Rank 6 / 7; rewriting-reality privileges unlocked


The campaign is the gap between stages. Each gap is a sandbox arc:

Mortal Apex → Spark Ignition: classic mortal-tier power fantasy
Spark Ignition → First Worship: god-mechanics discovery, building the cult
First Worship → Pantheon Notice: small-scale cult operations, regional warfare
Pantheon Notice → Transcendence: full divine warfare, planar conquest


XI. Anti-Pattern: When God Mechanics Go Wrong
The user has flagged these in past campaigns. The LLM must NOT do them.

Anti-pattern
Why it's bad
Replacement
All narrative, no math
The user can't feel progression; the LLM vibes the difficulty curve
Explicit stat block per scene; compute DR/DPP at start of each divine encounter
Gods win every fight
Removes challenge; the user quits in 5 sessions
Divine enemies use the same God Combat engine, with their own stats. They can win.
Worship is automatic
No cult operations, no per-faction dissonance
Track F explicitly; require cult actions for F growth above natural baseline
Avatars are invincible
Avatar vs mortal threats is boring
Avatars operate under the mortal sheet + divine overlay; can be challenged by high-tier mortals
Portfolio never changes
Static god = static campaign
Portfolio expansion at rank promotion; portfolio decay on neglect
Portfolios collapse across factions
"Everyone sees you the same way"
Per-faction dissonance rule (IX) — keep them independent
Random antagonist events
Cosmic-level threat with no LLM-narrated setup
Antagonist actions cost the antagonist Tithe/DPP; track and disclose
Magic-detection / scrying spam
The LLM invents "you've been seen by an oracle" tropes
Detection = a divine-tier action that costs the watching god DPP; default = NOT watched



XII. Game Master Operational Rules (general)
The LLM running a god campaign must:

Print the divine stat block at the start of every scene in which the avatar is active. One line: DR X / DAC Y / DPP Z/day / DAIR +A / DLR B / PDD C+d20×D / F=current.
Print the F tracker at dawn transitions and after any cult operation. F = 12,450 (+0 natural / +0 operations today).
Print the Tithe pool at every divine action. Tithes spent: 2 (Dread Proclamation). Pool: 5/7 remaining.
Compute formulas in-line when scaling changes. "Your DR has scaled with F: was 750 at F=0, now 762 at F=50,000." No hiding the math.
Use sequence IDs / checkpoint blocks to anchor scene continuity. (Format: SeqID N | Timestamp | Location | [HASH].) Borrowed from the Aizen Godhood Continued model.
Apply per-faction dissonance. Two factions receiving the same vision differently is a feature, not a bug. The LLM is forbidden from averaging their reactions.
No silent antagonist events. Every antagonist action has a Tithe/DPP cost the LLM discloses. If an NPC acts against the god, the LLM narrates the cost they paid.
No magical scrying without divine-tier action. Mortals cannot scry a god-tier avatar without spending divine-tier resources. If a mortal "somehow detects" you, the LLM must explain the chain.


XIII. Worked Example: Aizen, the God-King (setting-agnostic)
Translating the aizen_god_mechanics.md doc into this framework:

Rank: 3 Nascent Greater
F: Started at 0 (post-Bane consumption); scale to 1M for Rank 6
DR: 750 (matches Rank 3)
DAC: 25 + DEX = 26
DPP/day: 825 (matches Rank 3)
DAIR Mod: +31 (matches Rank 3)
DLR: 4
PDD: 80 + (1d20×5)
Portfolios: Tyranny, Control, Order through Absolute Will, Absolute Codification
Cult mechanics: Aizen's avatar in BG3 is mid-ascension, building toward F=100k
Avatar: Mortal-class Paladin 2 / Bard 10, inherits gestalt sheet
Anti-pattern check: The 3-layer deception (Kyōka Suigetsu, false stat block to Mystra) IS the right kind of god-mechanic — system-agnostic illusion as divine action, costs DPP.

This general spec explains why the Aizen god-mechanics doc worked: it had explicit numbers, a scaling formula, and a coherent engine.


Cross-references
Existing setting-specific module: world_reference/campaign_module_god_of_murder.md — apply this general spec to the BG3 module's Sanguine Architecture to get explicit Tier-3 god stats.
Aizen reference (Faerûn-specific): world_reference/aizen_god_mechanics.md — the canonical setting-specific instantiation this general spec was extracted from.
3e God Combat baseline: The mechanical baseline used in the BG3 God of Murder doc; reused here with system-agnostic numbers.
Campaign bible templates: ~/.hermes/skills/campaign-creation/ (skillified this turn) — uses this god-mechanic framework for the "if your protagonist ascends, here's the engine" section.


Provenance
Drafted: 2026-07-20, in response to Jeffrey's "keep iterating on this campaign. It doesnt seem to have many god mechanics just lots of narrative?" (Slack C0AH3RY3DK6/p1784585087.439909).
Extracted from: world_reference/aizen_god_mechanics.md (verified 2026-07-20) + the Sanguine Architecture module's Section 6 (Level 12→30 ledger) + Section 7 (Mechanical Subsystems).
Constraint applied: "The god mechanics should be general though and not specific to faerun or D&D" (Slack C0AH3RY3DK6/p1784584779.096719).
Voice constraint applied: "Lets make dissonance hidden and remove apex attention and make it dissonance per god faction versus overall" (Slack C0AH3RY3DK6/p1784507599.182939) — codified as §IX.


PART 3 — God Mechanics — V2 General Spec (System-Agnostic, V2 Overlay)
The V2 overlay on top of V1. Adds hidden Reputation + Apex Attention bands, the auto-win combat ladder, the context-aware per-dawn menu, the deicide-cost-as-Apex-bump rule, and a 4-roll cap per scene. Translates cleanly to any setting. Part 3 of 4.

Slug: god-mechanics-v2-general Date: 2026-07-21 Status: Approved 2026-07-21 by Jeffrey Lee-Chan Source thread: C0AH3RY3DK6/p1784585087 Mirror: ~/roadmap/docs/superpowers/specs/2026-07-21-god-mechanics-v2-general.md


Purpose
This document defines the system-agnostic god-mechanics core — the rules that govern any "you are a god" campaign regardless of setting. Companion docs specialize this for specific pantheons:

Faerûn / D&D 5e / Nocturne (Skilled god): nocturne-v2-faerun-gods.md + nocturne-v2-god-mechanics-design.md

The mechanics here are setting-agnostic and translate cleanly into:

D&D 5e / Forgotten Realms / Eberron
Cyberpunk (gods as megacorps)
Wuxia (cultivation ascension)
Naruto (Tailed Beast / Bijū)
Marvel (Cosmic-tier entities)
Any homebrew setting with a defined god-tier


1. Universal god stats (5 stats + 2 hidden bands)
Every god, regardless of setting, has:

Stat
Definition
DR (Divine Resilience)
"God HP" — the god's effective hit point pool
DAC (Divine Armor Class)
God defensive rating
DAIR (Divine Attack/Influence Roll)
God attack bonus / influence roll
DPP/day (Daily divine budget)
Per-day pool of divine actions — the OPTIMIZE target
DLR (Divine Legendary Resistances)
Auto-save count against mortal-level effects


Plus two hidden LLM-side state axes (player never sees the numbers; only the bands):

Hidden axis
Definition
Reputation
Are you known to mortals? Bands: Unknown / Whispered / Open / Established / Revered / Pantheon-tier
Apex Attention
Are other gods/powers aware of you? Bands: Unseen / Whispered / Noticed / Marked / Hunted / Apotheosis imminent


Player reads the bands, not the numbers. The LLM tracks state; player reads narrative consequences.


2. Linear scaling formula (V1 Aizen pattern)
Stat(F, Reputation, Apex) = Stat_Nascent

                          + (F / 1,000,000 × (Stat_Transcendent − Stat_Nascent))

                          + Reputation_modifier

                          + (Apex_Attention_band_modifier)

Where:

F = active follower count
Reputation_modifier = Reputation_band × Reputation_bonus_per_band (50/25/5 for DR/DPP/DAIR, system-tunable)
Apex_Attention_band_modifier = Apex_band × Apex_bonus_per_band (negative at higher bands — high attention incurs defensive penalties from being targeted)

V1 Aizen reference data: F=0 → DR 750, DPP 825, DAIR +31. F=1M → DR 1750, DPP 1825, DAIR +56. Ratio: 2.33× DR, 2.21× DPP, 1.81× DAIR.

Any setting can plug in their own Stat_Nascent / Stat_Transcendent values. The linear interpolation between Nascent and Transcendent at F=1M followers is the universal shape.


3. Six god-classes with stat biases
Any setting with multiple gods can specialize them via god-class:

Class
DR
DAC
DAIR
DPP
Examples (Faerûn)
War god
High (1100+)
Low (22-)
High (+50+)
Mid (700-)
Tempus, Bane
Trickster god
Low (500-)
Low (20-)
Very High (+60+)
High (900+)
Mask, Cyric
Domain god
High (1100+)
Mid (24)
Mid (+35+)
Mid (700-)
Chauntea, Silvanus
Magic god
High (1100+)
Low (22-)
Mid (+35+)
High (900+)
Mystra, Shar
Death god
Very High (1500+)
Mid (24)
Mid (+35+)
Mid (700-)
Kelemvor, Myrkul
Skilled god
Mid (750-)
Mid (24)
Very High (+60+)
Mid (700-)
Nocturne (Murder), Sune


Why these 6 classes:

War god — high offense + defense, mid resource pool
Trickster god — glass cannon, very high resource pool (lots of agents / boons / lies)
Domain god — sturdy steward, balanced offense
Magic god — defensive bulwark + high resource (arcane / cosmic / divine spell repertoire)
Death god — extreme durability, kills survive them
Skilled god — specialized excellence in one combat method

Settings choose their own archetypes:

Cyberpunk: Solo god / Netgod god / Corp god / Hacker god / Fixer god / Infiltrator god
Wuxia: Sword god / Alchemy god / Formation god / Beast god / Body god / Dao god
Marvel: Strength god / Cosmic god / Sorcerer god / Mutant god / Speed god / Tech god


4. Combat resolution ladder (auto-win on mortals)
Target
Result
Mortal-tier — Commoner / random NPC
Auto-win. No roll.
Named mortal — Hero, leader, legendary mortal
Auto-win unless god-tier penalty applies.
Chosen — Mortal blessed by another god
Divine combat. d20+DAIR vs DAC.
Avatar of lesser/major god
Full divine combat. Major action + d20 roll.
Lesser / Intermediate god directly
Full divine combat. Major action + d20 roll.
Greater god / Apex entity
Full divine combat. May require god-hunt action chain.


Auto-win on mortals is the god-tier fantasy. The combat math only matters for divine beings and Chosen NPCs. Setting can permute names: "Chosen" might be "Blessed," "Avatar" might be "Aspect," etc.


5. Per-dawn menu (context-aware, not every dawn)
Dawn type
Menu shape
When
Routine dawn (default)
2-3 light options: worship-build, heat-management, RP accumulation
Most dawns
Triggered dawn (something dramatic)
4-6 full options: god-hunt, rival-pantheon confrontation, coalition-formation, etc.
Dramatic-surfacing event triggers
Quiet dawn (post-crisis cooldown)
No menu — narrative + stat updates only
Post-crisis


Player picks → math runs deterministically → roll resolves variance within math-determined bracket.

The structure is universal; the options are setting-specific (god-hunt in D&D, corp-takeover in Cyberpunk, dao-realization in Wuxia, etc.).


6. Roll = variance within math-determined bracket (4-roll cap per scene)
For any god-vs-god engagement, the math resolves most of the action chain:

Phase
Math decides
Roll adjusts
1. Locate
Reach this dawn
— none —
2. Infiltrate
Entry (resource budget)
— none —
3. Engage
Major Action feasibility
— none —
4. Counter
Target's response
— none —
5. Commit
Damage bracket (differential)
1d20 within ±5 on damage quantity
6. Absorb
Integration
1d20 picks which sub-effect manifests


Per-scene roll cap = 4 maximum (e.g. cultist loyalty × 1, assassination attempt × 1, deception × 1, target's final death save × 1). Beyond that, the math decides.


7. Deicide-cost = Apex Attention growth only
When a god kills another god:

DR +absorption_amount (per stat-block absorption, setting-specific amount)
Apex Attention +1 band (e.g. "Whispered" → "Noticed")
No other cost (clean kill, single consequence)

No Wounds. No Publicity Tax. No Empty Throne. Apex Attention is the only deicide consequence — and it's already a hidden band, so the player just reads the narrative consequences.

This is system-agnostic: any setting with god-tier gives the killer an Apex Attention bump as the consequences-spreads-metaphor.


8. Universal D&D 5e OPTIMIZE → ROLL loop
The player loop:

Optimize first — read stat sheet + per-dawn menu + Reputation/Apex bands
Pick a strategy — choose option A/B/C/D (e.g. god-hunt vs safe-expansion vs worship-build)
Math resolves — DPP/DAC/DAIR math determines whether the action succeeds or fails at level 1
Roll adds variance — within the math-determined bracket, roll decides sub-effects (1d20 within ±5 damage, etc.)
Player reads consequence — DR/DPP update, Apex band shift, narrative surfacing

The OPTIMIZE step is what V1 lacked. V2 makes it the heart of every dawn.


9. References
Aizen Godhood mechanics — V1 reference; V2 extends it
V1 god-mechanics general spec — companion doc covering phase-by-phase stat blocks + 6-faction dissonance (V1 PR #8484)
V2 Nocturne spec — world_reference/nocturne-v2-god-mechanics-design.md (Nocturne/D&D-specific)
V2 Faerûn gods spec — world_reference/nocturne-v2-faerun-gods.md (Faerûn pantheon integration)



END OF GENERAL SPEC.


PART 4 — Nocturne V2 — D&D 5e Faerûn Specialization
The V2 spec specialized for Nocturne / D&D Faerûn / BG3. 7 tiers (Mortal → Demi-god → Lesser god → Minor → Intermediate → Greater → Transcendent), mortal-to-divine multiplier (HP×5.4 → DR, AC+4 → DAC, Attack+18 → DAIR), and the L26 ascension breakpoint. Part 4 of 4.

Slug: nocturne-bg3-v2-god-mechanics-design Date: 2026-07-21 Status: Approved 2026-07-21 by Jeffrey Lee-Chan Source thread: C0AH3RY3DK6/p1784585087 Mirror: ~/roadmap/docs/superpowers/specs/2026-07-21-nocturne-v2-god-mechanics-design.md


Companion documents
This doc specializes the universal V2 god-mechanics for Nocturne / D&D Faerûn. For system-agnostic mechanics that apply to ANY setting (Cyberpunk, Wuxia, Marvel, Naruto, etc.), see:

god-mechanics-v2-general.md — system-agnostic core (linear scaling, god-classes, auto-win ladder, per-dawn menu, deicide-cost)
nocturne-v2-faerun-gods.md — Nocturne-specific Faerûn pantheon integration (stat-block examples for Bane / Shar / Mystra / Mask / etc.)


0. Goals & non-goals
Goals:

Replace narrative-heavy God of Murder V1 with a mechanically load-bearing god-campaign (per user feedback: "calculations which don't mean much" → V2 makes the math load-bearing).
Apply Nocturne-specific Faerûn / D&D 5e mechanics on top of the V2 general spec (god-mechanics-v2-general.md).
Cover the BG3 post-game campaign (Dark Urge successor → Goddess of Murder).

Non-goals:

V2 does not redefine Nocturne's character — it inherits V1's Nocturne / Dark Urge setting, post-game BG3 context.
V2 does not redefine the mortal-class build (gestalt Gloomstalker 12 / Assassin Rogue 8 remains the L20 mortal form).


1. Nocturne tier structure (7 tiers, levels 1-46+)
Tier
Levels
Stat system
Ascension trigger
Mortal
L1-20
Standard 5e (HP, AC, Save DC, Attack Bonus, Spell Slots)
n/a — natural character progression
Demi-god
L21-25
Standard 5e + divine flavor narrative ("incubating goddess")
Natural L21 achieved
Lesser god ⭐
L26-30
God stats kick in here (first god-tier stat block)
First god-kill (Bhaal-essence absorbed)
Minor god
L31-35
God stats, scaled up
Reach Minor threshold (Reputation + Apex Attention)
Intermediate god
L36-40
God stats, scaled up
Reach Intermediate threshold
Greater god
L41-45
God stats, scaled up
Reach Greater threshold
Transcendent
L46+
God stats, apex (Aizen's final form)
Reach Transcendent threshold


Ascension at L26 = Lesser god = first god stat block. L21-25 is the "almost-a-god" interstitial.

For the universal tier ladder (setting-agnostic), see god-mechanics-v2-general.md §3.


2. Nocturne mortal → divine multiplier (Nocturne-specific)
At L26, Nocturne's mortal stat block converts to god stats via multiplier:

DR   = HP × 5.4    (Aizen: HP 138 → DR 750)

DAC  = AC + 4       (Aizen: AC 21 → DAC 25)

DAIR = Attack + 18  (Aizen: +13 → +31)

DPP  = base 825 + Reputation modifier (no mortal analog)

DLR  = folded into DR's natural scaling (no separate stat)

Nocturne L20 mortal form (gestalt Gloomstalker 12 / Assassin Rogue 8): HP ~142, AC ~22, Save DC ~22, Attack +14. At L26 ascension:

DR 766 · DAC 26 · DAIR +32 · DPP/day 825

Stronger mortals = stronger gods. Multiplier stays. L1-19 gear choices compound forward (a +5 Greatsword at L20 becomes +5 to DAIR at L21+).


3. Nocturne = Skilled god (Nocturne-specific)
From god-mechanics-v2-general.md §3, the 6 god-classes, Nocturne = Skilled god:

Class
DR
DAC
DAIR
DPP
Examples
Skilled god ⭐
Mid (750-)
Mid (24)
Very High (+60+)
Mid (700-)
Nocturne (Murder), Sune


Nocturne is good at killing specifically, not war-tanking. This explains her stat block being unique without making her unique in kind.

For other Faerûn gods' stat-block examples (Bane, Shar, Mystra, etc.), see nocturne-v2-faerun-gods.md.


4. Nocturne's Reputation + Apex Attention bands (Nocturne-specific surfacing)
From god-mechanics-v2-general.md §1, the universal bands, Nocturne-specific narrative surfacing:

Reputation band
Nocturne-specific narrative
Unknown
Bhaalist remnant cells lurk, but you've absorbed Bhaal — no public worshippers yet
Whispered
Small cults form in BG shadows; the Lords' Alliance hears rumors
Open
Public temples in Baldur's Gate; Cormyr's intelligence takes notice
Established
Major temples across the Sword Coast; priest-kings negotiate
Revered
State religion in BG and several Sword Coast cities
Pantheon-tier
Your temples rival Bane's — only Shar and Mystra have more


Apex Attention band
Nocturne-specific narrative
Unseen
Gods do not know you exist (you ate Bhaal before they noticed)
Whispered
Rumors reach distant planes — Cyric sends an avatar
Noticed
Temples discuss your name; the gods convene a council
Marked
Gods take notice, your worship is contested
Hunted
Coalitions form; Bane's Chosen hunt you
Apotheosis imminent
Greater gods personally intervene; the campaign endgame



5. Nocturne per-dawn menu (sample triggered dawn at L26)
From god-mechanics-v2-general.md §5 (universal), Nocturne-specific menu at L26:

═══════════════════════════════════════════

NOCTURNE V2 — DAWN 47 (Repr "Whispered", Apex "Unseen")

═══════════════════════════════════════════

Stat Sheet:

  DR 766/766 · DPP 75/825 · DAIR +32

Today's Choices — pick 1:

  A. BHAAL HUNT (DPP cost: 200)

     → DR +30 IF successful, Bhaal's portfolio integrated

     → Failure: Apex Attention +1 band ("Unseen" → "Whispered")

  B. WORSHIP BUILD (DPP cost: 100)

     → Reputation shifts toward "Open"

     → Failure: nothing lost (safe)

  C. SAFE EXPANSION (DPP cost: 50)

     → Apex Attention -1 band (back to "Unseen")

     → Failure: nothing lost

Which? (A is high-stakes god-kill, C is the safe play)

═══════════════════════════════════════════

Player picks → math runs deterministically → roll resolves variance within math-determined bracket.


6. Nocturne combat ladder (auto-win on Faerûn mortals)
From god-mechanics-v2-general.md §4 (universal), Nocturne-specific targets:

Target
Result
Commoner / Flaming Fist / city watch
Auto-win
Named mortal (Duke, patriar, Chionthar merchant)
Auto-win (divine Save DC)
Chosen (Bane's Chosen, Shar's Chosen, Mystra's Chosen)
Divine combat (d20+DAIR vs DAC)
Avatar of lesser god
Full divine combat
Lesser / Intermediate god
Full divine combat
Greater god / Apex entity
Full divine combat (may need action chain)


Nocturne = death-deity archetype — mortals cannot beat her divine Save DC. Combat math matters only for divine beings and Chosen NPCs.


7. Nocturne-level-up tracking (specific to her L1-30 gestalt progression)
Nocturne-specific progression values (from V1 Section 6 progression ledger):

Level
Sneak Attack
Key features
L12
6d6
Base features (alpha-strike setup)
L16
8d6
Karsite Acceleration + Extra Attack
L20
10d6
Foe Slayer (Ranger) + Stroke of Luck (Rogue) — mortal form cap
L21
11d6
Umbral Veil / Epic Skill Expertise
L25
13d6
Font of the Wilds / Master Infiltrator
L26
13d6
Ascension → god stats kick in
L30
15d6
Apex Stalker / Master of Absolute Death


The mortal stat block at L20 (HP 142, AC 22, Save DC 22, Attack +14) is the foundation for the L26 god-stat conversion (§2).


8. References
General V2 god-mechanics — god-mechanics-v2-general.md (system-agnostic)
Faerûn pantheon integration — nocturne-v2-faerun-gods.md (Bane, Shar, Mystra, Mask, etc.)
V1 god-mechanics general spec — world_reference/god_mechanics_general.md (V1 PR #8484)
V1 Nocturne campaign module — world_reference/campaign_module_god_of_murder.md Section 8 + Section 9
Spec source — ~/roadmap/docs/superpowers/specs/2026-07-21-nocturne-v2-god-mechanics-design.md



END OF NOCTURNE SPEC.


PROVENANCE & NEXT STEPS
Campaign module SHA: world_reference/campaign_module_god_of_murder.md @ HEAD 48472d7ed7 (PR #8488)
V1 general spec SHA: world_reference/god_mechanics_general.md @ HEAD 48472d7ed7 (PR #8488)
V2 general spec SHA: world_reference/god-mechanics-v2-general.md @ HEAD 48472d7ed7 (PR #8488)
V2 Nocturne spec SHA: world_reference/nocturne-v2-god-mechanics-design.md @ HEAD 48472d7ed7 (PR #8488)
Gemini source: https://share.gemini.google/Td7fA4pzuvMs (full archive at /tmp/gemini_v7_full.txt, 168 KB / 2,264 lines)
Companion PRs on world_reference:
PR #8483 (MERGED 2026-07-20): feat(world_reference): add The Sanguine Architecture — God of Murder BG3 module — the V1-only campaign module that this PR extends
PR #8488 (OPEN 2026-07-21): feat(world_reference): V2 god-mechanics overlay + canonical spec — adds the V2 general spec + Nocturne/Faerûn specialization on top of V1
PR #8486 (MERGED 2026-07-21): Visenya V9 Blood Dragon (related: world_reference evolution)
Companion code: mvp_site/campaign_divine.py, mvp_site/constants.py, mvp_site/tests/test_v2_god_mechanics.py — all live on PR #8488 with 72/72 tests passing
Wiki source (sister module): Nocturne BG3 V2 god-mechanics design spec lives in ~/roadmap/docs/superpowers/specs/2026-07-21-nocturne-v2-god-mechanics-design.md
What this Doc enables
Reading the whole story + mechanic without leaving the browser — share with collaborators
Cross-reference anchor for the world_reference/ markdown files in PR #8488
Provenance artifact for the iterative design that started with Gemini V1 → merged V1 (PR #8483) → V2 overlay (PR #8488)
Future iteration input — when you say "iterate on the god campaign," this Doc is the canonical state anchor
Recommended next iterations (after PR #8488 merges)
Update Gemini share link V2 continuation — ask Gemini to read this Doc and design V3 (e.g. add cyberpunk-class support or Wuxia-cultivation ascension)
Add a wiki source page at ~/llm_wiki/wiki/sources/god-of-murder-v2-nocturne-sanguine-architecture.md (Karpathy frontmatter, audit-checked)
Run wa-campaign-content-analysis to score this Doc against the campaign-template benchmark
/superlight pass to rewrite the Doc with the user's standing character-personality template formatting
Ingest into Firestore — extract god_of_murder_canonical_description.txt for create_campaign_unified after constants wiring



This Doc is the canonical state anchor for the God of Murder / Sanguine Architecture campaign as of 2026-07-21. All four source files are live on origin/main (V1) or PR #8488 (V2 overlay).

============================================================
SCENE 1
============================================================
Game Master:
[Character Creation Mode - Story begins after character is complete]

Player (freeform):
run char creation process

============================================================
SCENE 2
============================================================
[Timestamp: 1492 DR, Post-Apotheosis
Location: Baldur's Gate (The Apex of the Balduran Statue)
Status: Lvl 12 Gestalt | HP: 136/136 | Gold: 27,000gp | XP: 100000/120000
Conditions: Normal | Exhaustion: 0 | Inspiration: No]
Resources: HD: 12/12 | Spells: L1 4/4, L2 3/3, L3 3/3 | Sneak Attack: 6d6 | Tithes: 125/125

Game Master:
[CHARACTER CREATION - Review]

**FIREBASE SANITY CHECK:** Campaign data loaded successfully. Setting: Baldur's Gate 3 Post-Game.

**CAMPAIGN SUMMARY**
Title: God of Murder — The Sanguine Architecture
Character: Nocturne (Dark Urge)
Setting: Faerûn, 1492 DR (Post-Netherbrain)
Description: You have consumed Bhaal's spark and the Crown of Karsus. You are the nascent Goddess of Murder.
AI Personalities: StoryModeAgent, CharacterCreationAgent
Options: Mechanics Enabled, Gestalt Leveling, God Mechanics V2

I have generated your character based on the Sanguine Architecture campaign bible and high-level gestalt rules. Please review the details below:

### Character Sheet: Nocturne (Level 12)
**Race:** High Elf | **Class:** Gloomstalker Ranger / Assassin Rogue (Gestalt)
**Level:** 12 | **Divine Rank:** 0 (Quasi-Deity)

**Ability Scores:**
- STR: 12 (+1) [Base 10]
- DEX: 22 (+6) [Base 20]
- CON: 16 (+3) [Base 14]
- INT: 12 (+1)
- WIS: 16 (+3)
- CHA: 8 (-1)
*Justification: Ability scores reflect a high-level gestalt character who has consumed a divine spark and benefits from the Physical Surge feature (+2 STR/DEX/CON).* 

**Combat:**
- HP: 136/136
- AC: 20 (Studded Leather +2 + DEX mod + Physical Surge bonus)
- Initiative: +9 (+6 DEX, +3 WIS)

**Skills:** Stealth (Expertise +14), Perception (Expertise +11), Acrobatics (+10), Insight (+7), Investigation (+5), Deception (+3).

**Equipment:**
- **Melee (Main):** Sussur Dagger +2 (Silences on hit)
- **Melee (Off):** Dagger +2
- **Ranged:** Gontr Mael (Legendary Longbow +2)
- **Armor:** Studded Leather +2
- **Backpack:** Assassin's Kit, Scholar's Pack, Bhaalist Sigil

⚠️ **GOLD VERIFICATION:** Starting gold set to 27,000gp (Level 12 WBL baseline for a Commoner-tier origin). State updated.

**Spells Known (Ranger):**
- 1st: Disguise Self, Longstrider, Fog Cloud, Hunter's Mark
- 2nd: Rope Trick, Pass Without Trace, Silence, Lesser Restoration
- 3rd: Fear, Conjure Animals, Spike Growth

**Cantrips:** Minor Illusion (High Elf)

**Passive Features:**
- **Physical Surge:** +2 STR/DEX/CON, +2 AC (Rank 0 Divinity)
- **Dread Ambusher:** +WIS to Initiative, extra attack + 1d8 damage on Round 1
- **Umbral Sight:** Invisible to Darkvision in darkness
- **Assassinate:** Advantage on targets that haven't acted; auto-crit on surprised targets
- **Sneak Attack:** 6d6

Does this character meet your approval, or would you like to make changes?

Player (freeform):
lets do 8 str and give points to wis/cha maybe 18 wis and 14 cha if possible? lets assume i am level 12 and had 3 ASI

maybe more gold since we defeated the absolute and on paper or publically are legendary heroes, lets assume i have a good/moral public face i can exploit as a legendary hero who beat netherbrarin

give me the best gear in bg3 for my build

make sure i really have all aspects of a level 12 gloomstalker + assassin rogue and brainstorm some special mechanics as the nascent god of murder, i dont have any divine powers yet until demi god level 20 and level 26+ when i start using real divine stats but some things can trickle in

============================================================
SCENE 3
============================================