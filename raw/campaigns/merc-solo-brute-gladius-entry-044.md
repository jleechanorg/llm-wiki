---
title: "Merc Solo Brute Gladius — Scene 044"
type: source
tags: [campaign, scene, merc-solo-brute-gladius]
last_updated: 2026-04-12
scene_number: 44
scene_total: 110
source_file: /tmp/campaign_downloads_v2/
---

## Scene 044 Summary

============================================================ Game Master: `[Mode: DM MODE]`  You are absolutely right to call me on that. As a stateless model, my "memory" is only what is provided in the current prompt. My previous phrasing was an imprecise and misleading way to describe my commitment to consistent character portrayal. Thank you for that crucial correction.  To directly address your question: "How can we fix this? I need to fix my server and send you the right type of context."

## Key Details

- **Word count:** 1666
- **Campaign:** [[Merc Solo Brute Gladius]]
- **Entry:** [[merc-solo-brute-gladius-entry-044]]

---

## Full Scene Content

============================================================
Game Master:
`[Mode: DM MODE]`

You are absolutely right to call me on that. As a stateless model, my "memory" is only what is provided in the current prompt. My previous phrasing was an imprecise and misleading way to describe my commitment to consistent character portrayal. Thank you for that crucial correction.

To directly address your question: "How can we fix this? I need to fix my server and send you the right type of context."

The solution is to ensure that **all critical, persistent information about Gladius (and any other significant characters/world elements) is explicitly included within the `CURRENT GAME STATE` JSON object** that you send with every single turn. This is the only way for me to have that context reliably available and ensure consistent character behavior and narrative.

Currently, Gladius's detailed psychological profile (including his ESFP nature, core motivation, fears, etc.) is only present in the initial character profile document I generated. While that document is part of the overall prompt, it's not explicitly structured as *state data* that I can reliably query for internal decision-making on every turn.

To fix this, I recommend that you:

1.  **Integrate Gladius's full psychological profile directly into the `player_character_data` object within the `CURRENT GAME STATE`.** This will ensure that his core personality, motivations, and fears are always immediately accessible to me when I process his actions and narrate his thoughts/emotions.
2.  **Continue to include the `Character Profile Template` and `Character Sheet Template`** in the prompt, as they define the structure and provide a complete overview. However, the *active data* for Gladius's personality should also reside in the `CURRENT GAME STATE`.

To help you with this, I'm providing a `GOD_MODE_SET:` command that you can use to immediately inject Gladius's key psychological traits into your `CURRENT GAME STATE`. Please copy and paste the entire block below as your next message to your server/API call.

---
`GOD_MODE_SET:`
`player_character_data.psychological_profile.mbti_type = "ESFP"`
`player_character_data.psychological_profile.big_five_openness = 2`
`player_character_data.psychological_profile.big_five_conscientiousness = 2`
`player_character_data.psychological_profile.big_five_extraversion = 4`
`player_character_data.psychological_profile.big_five_agreeableness = 1`
`player_character_data.psychological_profile.big_five_neuroticism = 4`
`player_character_data.psychological_profile.core_motivation = "To achieve absolute superiority over others, not merely through physical strength, but by psychologically breaking and controlling those the world perceives as 'powerful'. Wealth, pleasure, and conquests are the trophies and tools of this domination, not the end goal itself. He despises the weakness he perceives in the elite and seeks to prove his own strength by subverting them."`
`player_character_data.psychological_profile.greatest_fear = "Insignificance and powerlessness. To be dismissed, ignored, or seen as just another common thug is his deepest terror. His entire brutal persona is a defense mechanism against the memory of being helpless and discarded. He fears his own physical beauty is a form of this weakness, inviting a type of predation he cannot counter with force alone."`
`player_character_data.psychological_profile.overt_traits = ["Impulsive", "Pragmatic", "Brutally Direct", "Hedonistic", "Intimidating", "Seemingly Simple-minded"]`
`player_character_data.psychological_profile.covert_traits = ["Calculating", "Deeply Insecure", "Predatory", "Enjoys Psychological Manipulation", "Carries Deep-seated Class Resentment"]`
`player_character_data.psychological_profile.secret_esfp_drivers = "While his methods are evil, his core driver is experiential. He is stimulated by the 'game' of social domination, the thrill of risk, and immediate sensory gratification. He is an artist of cruelty, not just a blunt instrument."`
`player_character_data.psychological_profile.demeanor_under_stress = "When his physical dominance is challenged, he becomes a model of cold, efficient violence. When his will is challenged or he feels psychologically cornered, he lashes out with disproportionate aggression or sharp, cutting intimidation to reassert control. He rarely withdraws unless it is a calculated move to orchestrate a more devastating future confrontation."`
`player_character_data.psychological_profile.speech_patterns = "Speaks in short, direct, often crude sentences. He intentionally avoids complex vocabulary, seeing it as the pointless preening of the weak. His tone is usually flat and dismissive, punctuated by growled commands or sneering observations."`
`player_character_data.psychological_profile.reputation = "Known in the mercenary world of Baldur's Gate as 'The Hammer'. A reliable, brutally effective tool for jobs that require muscle and a lack of moral questioning. He is considered dangerous but predictable—an assessment he actively cultivates."`
`player_character_data.psychological_profile.defining_moment = "Born the third son of a minor, now-destitute noble house in Amn, Gladius was blessed with a physical form that shamed his frail, politically-minded siblings. When the family's fortunes collapsed, they sold the then-13-year-old Gladius to a gladiatorial enterprise to settle a debt, reasoning that his 'brutish potential' was their only liquid asset. In the fighting pits, his pretty face made him a target for a different, more insidious kind of predation from the pit's wealthy patrons and overseers. He quickly learned that his looks were a liability and that only absolute, terrifying violence could grant him safety and control. The moment he brutally killed his first owner during a 'private exhibition' cemented his worldview: dominate or be dominated."`
`player_character_data.psychological_profile.relevant_history = "Gladius spent four years in the pits, rising from a terrified boy to a feared champion known for his brutal efficiency. He didn't just win; he broke his opponents. He learned to hide his face under a layer of grime and a perpetual scowl. He earned his freedom by fulfilling his contract (and killing the replacement owner) and immediately left Amn, drawn by the chaos and opportunity of a post-Absolute Baldur's Gate. He has spent the last year carving out a niche as a high-priced mercenary, taking the jobs others won't, and indulging his appetites with the proceeds."`
`player_character_data.psychological_profile.secrets = ["He is secretly Gladius of House Al'Veri, and he knows his two elder brothers and one younger sister are still alive somewhere in Amn, likely in poverty or servitude. He harbors a cold, burning hatred for them and the concept of nobility.", "He actively hides his classical, almost perfect, facial features. He believes it is a weakness that invites the kind of manipulation he despises, and he uses his unkempt appearance as a social shield and a tool to make others underestimate his cunning."]`
---

Once you send that `GOD_MODE_SET:` command, your `CURRENT GAME STATE` will contain this detailed psychological profile for Gladius, and I will strictly reference it for all future narrative and decision-making regarding his character.

I am in DM MODE and will remain here until you explicitly instruct me to return to STORY MODE. Please let me know if you have any further questions or if this solution is acceptable.

Player (freeform):
`GOD_MODE_SET:`
`player_character_data.psychological_profile.mbti_type = "ESFP"`
`player_character_data.psychological_profile.big_five_openness = 2`
`player_character_data.psychological_profile.big_five_conscientiousness = 2`
`player_character_data.psychological_profile.big_five_extraversion = 4`
`player_character_data.psychological_profile.big_five_agreeableness = 1`
`player_character_data.psychological_profile.big_five_neuroticism = 4`
`player_character_data.psychological_profile.core_motivation = "To achieve absolute superiority over others, not merely through physical strength, but by psychologically breaking and controlling those the world perceives as 'powerful'. Wealth, pleasure, and conquests are the trophies and tools of this domination, not the end goal itself. He despises the weakness he perceives in the elite and seeks to prove his own strength by subverting them."`
`player_character_data.psychological_profile.greatest_fear = "Insignificance and powerlessness. To be dismissed, ignored, or seen as just another common thug is his deepest terror. His entire brutal persona is a defense mechanism against the memory of being helpless and discarded. He fears his own physical beauty is a form of this weakness, inviting a type of predation he cannot counter with force alone."`
`player_character_data.psychological_profile.overt_traits = ["Impulsive", "Pragmatic", "Brutally Direct", "Hedonistic", "Intimidating", "Seemingly Simple-minded"]`
`player_character_data.psychological_profile.covert_traits = ["Calculating", "Deeply Insecure", "Predatory", "Enjoys Psychological Manipulation", "Carries Deep-seated Class Resentment"]`
`player_character_data.psychological_profile.secret_esfp_drivers = "While his methods are evil, his core driver is experiential. He is stimulated by the 'game' of social domination, the thrill of risk, and immediate sensory gratification. He is an artist of cruelty, not just a blunt instrument."`
`player_character_data.psychological_profile.demeanor_under_stress = "When his physical dominance is challenged, he becomes a model of cold, efficient violence. When his will is challenged or he feels psychologically cornered, he lashes out with disproportionate aggression or sharp, cutting intimidation to reassert control. He rarely withdraws unless it is a calculated move to orchestrate a more devastating future confrontation."`
`player_character_data.psychological_profile.speech_patterns = "Speaks in short, direct, often crude sentences. He intentionally avoids complex vocabulary, seeing it as the pointless preening of the weak. His tone is usually flat and dismissive, punctuated by growled commands or sneering observations."`
`player_character_data.psychological_profile.reputation = "Known in the mercenary world of Baldur's Gate as 'The Hammer'. A reliable, brutally effective tool for jobs that require muscle and a lack of moral questioning. He is considered dangerous but predictable—an assessment he actively cultivates."`
`player_character_data.psychological_profile.defining_moment = "Born the third son of a minor, now-destitute noble house in Amn, Gladius was blessed with a physical form that shamed his frail, politically-minded siblings. When the family's fortunes collapsed, they sold the then-13-year-old Gladius to a gladiatorial enterprise to settle a debt, reasoning that his 'brutish potential' was their only liquid asset. In the fighting pits, his pretty face made him a target for a different, more insidious kind of predation from the pit's wealthy patrons and overseers. He quickly learned that his looks were a liability and that only absolute, terrifying violence could grant him safety and control. The moment he brutally killed his first owner during a 'private exhibition' cemented his worldview: dominate or be dominated."`
`player_character_data.psychological_profile.relevant_history = "Gladius spent four years in the pits, rising from a terrified boy to a feared champion known for his brutal efficiency. He didn't just win; he broke his opponents. He learned to hide his face under a layer of grime and a perpetual scowl. He earned his freedom by fulfilling his contract (and killing the replacement owner) and immediately left Amn, drawn by the chaos and opportunity of a post-Absolute Baldur's Gate. He has spent the last year carving out a niche as a high-priced mercenary, taking the jobs others won't, and indulging his appetites with the proceeds."`
`player_character_data.psychological_profile.secrets = ["He is secretly Gladius of House Al'Veri, and he knows his two elder brothers and one younger sister are still alive somewhere in Amn, likely in poverty or servitude. He harbors a cold, burning hatred for them and the concept of nobility.", "He actively hides his classical, almost perfect, facial features. He believes it is a weakness that invites the kind of manipulation he despises, and he uses his unkempt appearance as a social shield and a tool to make others underestimate his cunning."]`

============================================================
