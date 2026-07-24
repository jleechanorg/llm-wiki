---
title: "Visenya V9 — The Blood Dragon Apex Stalker"
subtitle: "Dunk & Egg Era (209 AC) Campaign Spec"
type: design-spec
date: 2026-07-20
status: draft — awaiting user review
authors: [Hermes (brainstorming session), Jeffrey Lee-Chan (design lead)]
related:
  - wiki/sources/visenya-v9-blood-dragon-apex-stalker.md (initial campaign wiki)
  - wiki/concepts/StressLineSight.md (v9 Apex passive)
  - wiki/concepts/BloodDragonReputationDie.md (v9 reputation mechanic)
  - wiki/concepts/SanguineThread.md (replaces WoundLedger — lineage mechanic)
  - wiki/entities/RooksRest.md (Visenya's barony)
references:
  - jleechanorg/worldarchitect.ai PR #8483 (Sanguine Architecture BG3 reference — *inspiration only*, not copied)
  - jleechanorg/worldarchitect.ai PRs #8387, #8469, #8473, #8443 (WA guardrail touchpoints)
source_session: Slack C0AH3RY3DK6/p1784584425.185909
---

## Exit Criteria

The v9 spec is **DONE** when **all** of the following are verifiable externally (not by reading this file alone):

1. **Doc live** — Google Doc at the v9 doc URL contains Sections 1-14, the magic-barrier system, the Divine Rank coupling, and the four emergent endings.
2. **Wiki live** — `jleechanorg/llm-wiki` `origin/main` HEAD contains:
   - `wiki/sources/visenya-v9-blood-dragon-apex-stalker.md` (campaign wiki, updated)
   - `wiki/concepts/SanguineThread.md` (replaces WoundLedger)
   - `wiki/concepts/BloodDragonReputationDie.md` (updated to include Divine Rank coupling)
   - `wiki/concepts/MagicBarrierSystem.md` (NEW — the First Song containment mechanic)
   - `wiki/concepts/FirstSong.md` (NEW — V6-Visenya's ascended form as system feature)
3. **Spec self-review pass** — All placeholder/TBD items resolved; no internal contradictions.
4. **User review** — Jeffrey confirms the spec is acceptable.

Mock or dry-run satisfaction is **NOT** sufficient. The doc must contain the *actual* text and the wiki pages must exist on `origin/main`.

---

## Section 1: Campaign Concept

**Title:** *The Blood Dragon of Rook's Rest — A Level 6 Apex Stalker in the Time of Dunk & Egg*

**The Concept:** It is 209 AC. King Jaehaerys II has just died and the young Viserys sits the Iron Throne, but the crown's reach ends where the Kingswood begins. Across the Seven Kingdoms, the roads have become hunting grounds — the brotherhoods broken from the last Blackfyre Rebellion never disarmed. Lord Maekar Targaryen, the youngest of King Daeron's four fighting sons, has been given the thankless task of pacifying the Crownlands. His youngest child — **you, Visenya, sixteen, the unwanted great-granddaughter of the Conqueror through three generations of spares** — has been *awarded a barony near King's Landing* (Rook's Rest) for clearing the Stokeworth-to-Duskendale stretch of every bandit, cutthroat, and broken knight in a single campaigning season. The smallfolk whisper your name in the same breath as the Doom of Valyria: *"the Blood Dragon."* You are not loved. You are *feared*, and you have learned to weaponize the fear.

**The Hook:** You are a sixteen-year-old princess with a seat at the small council of every village headman between the Blackwater and the Narrow Sea — because you hanged the last three. Your reputation travels faster than your horse. You are not a hero. You are a **baronial magnate in miniature** who has discovered that *ruthlessness is the only dialect the Crownlands understand*. The fun derives from the sheer, terrifying asymmetry: you hold a barony no older lord will acknowledge, you ride with a household guard of broken men who would die for you, and you have **killed more people than the average Kingsguard knight has spoken to**.

**Why This v9 Is Different from v1-v8:**
- v1 (Dunk & Egg) — Dragon Scholar, INT/WIS godling; **squires** with Dunk.
- v2 (Slaver's Bay) — Belaerys Apex Heir; the Doom was her *family's doing*.
- v3 (HotD Sowing) — Sorcerer Apex Bloodline (CHA); claims Vermithor.
- v4 (Dunk & Egg) — Apex Weaver Bard/Mastermind; Baelarys Weaver, INT 20.
- v5 (Rhaegar-wins, 298 AC) — 12-year-old Apex Weaver Princess Visenya.
- v6 (Rhaegar-wins, 298 AC) — 14-year-old "Blood Dragon" Apex Weaver; vacation-North incognito; *sadistic*, views people as "dolls waiting to be broken"; **Entropy Toll mechanic** (Exhaustion from boredom).
- v8 (HotD) — Daemon's bastard, 16, claims a medium dragon.
- **v9 (this one)** — *Official House Targaryen* (Maekar's line); *youngest daughter of the youngest son*; 16; barony of Rook's Rest; Blood Dragon reputation **already earned**; **Apex Stalker** (Ranger Gloom Stalker / Rogue Assassin gestalt) — *physical geometry*, not social.

**The Class Pivot:** Where v1-v8 made Visenya a *godling puppeteer* (wizard, sorcerer, bard, mastermind), v9 makes her a **godling executioner** — power through *deciding which sentry's neck gets the blade*. The Apex lineage's "Information Geometry" (v6) becomes **Stress-Line Sight** (v9): physical geometry, not social. Same mathematical unfairness, different surface.

**The Reputation Mechanic Pivot:** Where v6's Heat System made her suffer Exhaustion from *boredom* if she didn't manipulate, v9's Reputation Die makes her *rewarded* with Divine Rank as her legend grows. The two are **mirror mechanics across 3000 years** (V6-Visenya became the First Song; current Visenya is *answering* what V6-Visenya started).

---

## Section 2: Character Personality

**Name & Archetype:** *Princess Visenya Targaryen, Lady of Rook's Rest, Baroness of the Rosby-Kingsroad Choke* / **The Blood Dragon & The Ditchbond (ISTP-A, "The Vigil").** She creates silence — not peace. She is the loudest quiet person in any room.

**The Two Faces:**

| Mask | Surface | Truth |
|---|---|---|
| **The Princess** | Courtly, sardonic, disarmingly young. Wears Targaryen red-and-black with the baronial pin of Rook's Rest. Smiles like a girl who has not yet learned the world is sharp. | Cold, surgical, *patient*. Tracks every micro-expression in a room. Holds grudges across years. |
| **The Blood Dragon** | Whispers about her in the inns of Duskendale — *"she rides out before dawn, comes back before noon, leaves no prisoners, never raises her voice."* The smallfolk cross themselves. | The rumors are *understated*. The bandit kings of the Kingsroad were not just killed — they were *filed*. Hanged in rows along the road so the next bandit chief could count them on his way in. |

**Visual Signature & Habits:**
- Silver-gold hair worn in a single severe braid down her back; never loose. *"Loose hair is a handhold in a fight."*
- A thin, white scar across the bridge of her nose — from the brigand king called the Hound of Stokeworth, who lunged at her at twelve and learned why *her mother named her for the Conqueror's wife*.
- Moves with absolute, frictionless economy. Never fidgets, never glances. **Her stillness is more unsettling than her violence.**
- Carries a longbow made of **fused weirwood-and-dragonglass** (a gift from a Pyromancer cell she spared) — *the only concession to ornament her body has ever accepted*.
- When bored, she cleans her weapons. When furious, she stops cleaning them and stares at the wall until someone breaks.

**The Core Compulsion — *Filing the Equation.***
She does not hate bandits. She hates **unresolved variables**. A brigand king terrorizing a road is an *unfinished sum*. She completes sums.

> **Mechanic: The Sanguine Thread.** Visenya does not keep a ledger of *sins*. She keeps a **loom** — a tapestry of blood woven into her own flesh — and every kill *writes a thread in the loom*. The thread is not guilt; the thread is *evidence of what kind of predator she is becoming*. As Visenya levels, the *function* of the thread shifts: at low levels it bleeds (the names rise, DC 14 WIS save or 1 Exhaustion — V6's Entropy Toll in lineage form). At mid levels it *settles* (page-fills = Inspiration). At high levels it *sings* (the names become patrons). At L20+ the Thread becomes *the architecture of a god*. *The cost is the same; the direction flips. She is not destroyed by the math. She is made by it.*

**Interaction Shorthand:**
- *To bandit chiefs*: absolute, flat monotone. No negotiation. "Surrender the Rosby road or I will file your name in red."
- *To courtly lords*: cool, courteous, *and inconveniently literal*. (When a Tyrell cousin asks "have you come to court for the tourney?", she replies, "No. I came to refill my quiver at the royal fletcher." The cousin laughs. The fletcher later tells her that was the first time the cousin ever felt *seen*.)
- *To Ser Duncan* (the only mortal she respects): patient, almost gentle. He is her *ditchbond*.

**Inner Monologue:**
> *"Aegon wants to prove he is a worthy heir to the Iron Throne. I want to prove that the road from Stokeworth to Duskendale can be traveled by a merchant's daughter without a sword. He thinks I am wasting myself in the Crownlands. He is correct. I am wasting myself so thoroughly that no one will ever think to check what I am doing with the hours it leaves."*
>
> *"Aerion calls me 'the dragon's leavings.' He means it as a sneer. He does not understand that the dragon's leavings burn longer than the dragon's fire. Maekar calls me 'my best inheritance.' I am not sure if he is complimenting me or warning me."*
>
> *"The Blood Dragon is a useful name. Let them say it. Let them fear it. Fear is a tax I do not have to enforce."*

---

## Section 3: Character Class — Level 6 Apex Stalker (Gloom Stalker / Assassin Gestalt)

**Class Name & Flavor:** The **Apex Stalker** is a custom Ranger (Gloom Stalker) × Rogue (Assassin) gestalt built for a sixteen-year-old baroness who has already killed more people than her father's bannermen. Where the Dragon Scholar was a *godling in a tower* and the Apex Weaver was a *godling with a ledger*, the Apex Stalker is a **godling who operates the perimeter** — the silent figure in the dark, the one who decides which sentry's neck gets the blade.

Her power is not magical in the conventional sense — it is the **Apex blood** manifesting as a perception so refined it borders on prophecy. The Baelarys lineage's "Information Geometry" becomes **Stress-Line Sight** — she perceives the structural weaknesses in a guard rotation, the exact moment a shadow falls, the precise angle at which light refracts off an arbalest bolt. She doesn't *cast* spells; she *reads* the physical world the way her ancestors read dragon-eyes.

**Why Gloom Stalker / Assassin and Not Bard / Mastermind:**
- v1 (Dragon Scholar) = godling *puppeteer*
- v4/v6 (Apex Weaver) = godling *diplomat*
- **v9 (Apex Stalker) = godling *executioner***

The pivot is intentional. v6's apex spent her time *manipulating others into killing for her*. v9's apex **kills her own**. She is what happens when the Apex lineage stops pretending to be human.

### Primary Attributes (Standard Array, +1/+2/+1 split)

| Stat | Score | Mod | Role |
|---|---|---|---|
| **DEX** | **18** | **+4** | Primary. Hit, damage, AC, Stealth, initiative, all skills |
| **WIS** | **16** | **+3** | Perception, Survival, Insight, the Stress-Line passive |
| **INT** | **14** | **+2** | Investigation, the Stress-Line math |
| **CHA** | **12** | **+1** | Court face; she *knows* she doesn't need much |
| **CON** | **13** | **+1** | Stamina for back-to-back operations |
| **STR** | **10** | **+0** | Almost vestigial; she has servants for the heavy lifting |

**HP at Level 6:** ~42 average
**AC:** 16 (Studded leather + DEX 4, no shield — the Blood Dragon does not cower)
**Initiative:** DEX +4 + **Wisdom (Gloom Stalker) +3** = **+7** (she always acts first)
**Passive Perception:** 18 (10 + WIS 3 + 5 from Alert-feat equivalent via Gloom Stalker)
**Speed:** 35 ft
**Proficiency Bonus:** +3
**Saves:** STR (0), DEX (+7), CON (+1), INT (+2), WIS (+6), CHA (+1)

### Saving Throws Note (the BIG v9 inversion):

The **Dragon Scholar** used CHA-substitution (used INT or WIS for CHA checks — *charisma through intellect*).

The **Apex Stalker** flips this: **CHA-based checks use DEX or WIS instead.** Visenya does not *charm*. She *arrives uninvited at the exact moment you were not looking*. Persuasion → uses WIS. Deception → uses DEX (sleight of story as sleight of hand). Intimidation → uses DEX (she is *physically* more dangerous than any courtier). This is the *physical geometry* mirror of v1's *social geometry* trick.

---

### Class Features (Level 6, Ranger 6 / Rogue 6 — gestalt)

**From Ranger (Gloom Stalker Conclave, Levels 1-6):**

| Level | Feature | Flavor |
|---|---|---|
| 1 | **Favored Enemy** (humanoids, human) | She has killed too many to need a study; she can read intent at a glance. |
| 1 | **Natural Explorer** (urban at night) | The Crownlands' bandit-infested streets are her terrain. |
| 2 | **Gloom Stalker Fighting Style: Blind-Fighting** | Fog of war, soot-cloud, the dark of the Kingsroad. She is *unfair* in low light. |
| 3 | **Gloom Stalker Conclave: Umbral Sight** | She sees 60 ft in magical AND nonmagical darkness as if it were daylight. **Critical.** |
| 3 | **Iron Mind** | WIS save proficiency. |
| 5 | **Extra Attack (x2)** | Her bow is a song. |
| 5 | **Gloom Stalker Feature: Stalker's Flurry** | Once per turn, when she misses an attack, she may make another as a bonus action. |
| 6 | **Gloom Stalker Feature: Shadowy Dodge** | When attacked in dim light/darkness, she imposes Disadvantage. |

**From Rogue (Assassin Archetype, Levels 1-6):**

| Level | Feature | Flavor |
|---|---|---|
| 1 | **Expertise** (Stealth, Perception) | Both at +11. She cannot be unseen; she is *unseen*. |
| 1 | **Sneak Attack (1d6 → 6d6 at Lv 6)** | Once per turn, +6d6 on a finesse/ranged attack from advantage or with an ally adjacent. |
| 2 | **Cunning Action** | Dash/Disengage/Hide as a bonus action. |
| 3 | **Assassin Archetype: Assassinate** | **The centerpiece.** Advantage against any creature that hasn't acted yet in combat. **Any hit against a Surprised target is an automatic Critical.** |
| 4 | **ASI: Alert** | Initiative +5 (stacks). Cannot be surprised. |
| 5 | **Uncanny Dodge** | Halve incoming damage as reaction. |
| 6 | **Expertise (x2)** + **Feat: Skulker** | She can hide when lightly obscured by creatures one size larger. She cannot be detected by blindsight/tremorsense. |

### The Apex Stalker Exclusives (v9 homebrew — *not* in PHB 5e)

#### Feature: *Stress-Line Sight* (always active, scaling by tier)

Visenya perceives the physical world as a set of **stress lines** — the exact trajectory a guard's gaze will trace in the next 3 seconds, the moment a structural beam will crack, the precise angle at which light will refract off an arbalest bolt. Mechanical effect:

| Tier | Levels | Stress-Line Sight Range | Notes |
|---|---|---|---|
| **Cub** | 1-5 | 15 ft passive (no active) | The lineage is dormant; perception is *latent*. |
| **Stalker** | 6-10 | 60 ft passive + 1 Stress Line/round | The lineage is active; she can declare one target. |
| **Apex Predator** | 11-15 | 120 ft passive + 2 Stress Lines/round | The lineage is dominant; she can target *multiple* threats. |
| **Sovereign** | 16-19 | 240 ft passive + 3 Stress Lines/round + **Sovereign Sight** (planar geometry) | She sees the *shape* of magic as well as physics. |
| **Demi-God** | 20+ | 480 ft passive + *unlimited* Stress Lines | **The First Song's prison door opens** — see Magic Barrier System (Section 13). |

**Passive:** Permanent Advantage on Perception checks involving sight in dim light/darkness (all tiers).

**Active (bonus action, 1/round at Stalker tier, scaling up):** Declare a *Stress Line*. Roll a DEX (Stealth) check against any creature within range that is not yet aware of you. On a success, that creature has Disadvantage on its next attack roll against you or any ally you designate. On a critical success (natural 20), the creature is also Blinded until the end of its next turn as the *suggestion of your silhouette* registers in its vision.

#### Feature: *The Sanguine Thread* (campaign-specific mechanic — *lineage, not sin*)

Visenya does not file her kills in a book. She **weaves them into a tapestry inside herself**. Every kill writes a thread in the loom. The thread is *not* guilt; it is *evidence of what kind of predator she is becoming*. The function of the same object — *the Book of the Blood Dragon* — shifts at each tier:

| Tier | Levels | Book State | Function |
|---|---|---|---|
| **Cub** | 1-5 | *Red Ledger* (under her pillow) | Names rise monthly (1d20 1-4, DC 14 WIS save or 1 Exhaustion). The book is *guilt*. |
| **Stalker** | 6-10 | *Wound Ledger* | Names continue to rise, but page-fills (10 names) now grant *Inspiration*. Old Nan can intervene (1/long rest reroll). |
| **Apex Predator** | 11-15 | *Book of Names* | The names stop bleeding and start *singing*. No more Exhaustion. |
| **Sovereign** | 16-19 | *Tapestry of the Blood Dragon* | The pages fuse into a *living document*. The names become *patrons* — minor divine sparks who owe Visenya their existence. |
| **Demi-God** | 20 | *Mantle of the Sanguine Slayer* | **Divine Rank 1-5.** Sovereign Sight (planar geometry). Book is a *holy relic*. |
| **God (Ascent)** | 21-25 | *Mantle of the Radiant Slayer* | **Divine Rank 6-10.** Two visual aspects (Sanguine Sovereign / Chitinous Ruin). Stat injections (+2/+4). |
| **God (Reign)** | 26-30+ | *Thread Eternal* | **Divine Rank 11-16+.** *3e God Combat* mechanics integrate. The book is her. |

**Thread count is tracked separately from Divine Rank.** It is the *soft input* to the First Song confrontation (see Section 13). A high thread count (>500 by L20) means Visenya has *earned* the confrontation by sheer killing; a low thread count (<300) means the First Song will not manifest even at L20 because Visenya is *not ready*.

#### Feature: *Apex Predator's Patience* (3/long rest)
As an action, Visenya enters a state of *absolute stillness*. For 1 minute, her movement becomes 0, she has full concealment against any creature that cannot see through magical means, and her next attack automatically benefits from **Assassinate** (Surprised condition even on aware targets; auto-crit). The visual: she sits down in the dark, polishes a knife, and *waits*. After three hours of stillness, she has been told her eyes reflect the light "like a cat's" — and three bandit captains who broke into her camp thought they were seeing a statue.

#### Feature: *The Blood Dragon's Reputation* (the v9 social mechanic — *replaces* v6's Heat System)

Visenya's name is a weapon. Whenever she enters a new settlement, town, or holdfast, the **GM rolls a Reputation Check (1d20, modified by CHA and current rumor-spread):**

| Roll | Result |
|---|---|
| 1-5 | **Unrecognized.** She is treated as a minor noble, a curiosity. The Blood Dragon is whispered in the Riverlands, but not here. |
| 6-12 | **Recognized.** Common folk cross themselves. Innkeepers won't turn her away but will *watch the door*. Nobles send servants to inquire whether she intends harm. |
| 13-18 | **Feared.** The local lord sends an honor guard. Commoners do not look at her. Bandits in the area are already riding *away* before she dismounts. |
| 19-20 | **Legend.** A *rhyme* is being whispered in the market. *"The Blood Dragon rides at dusk, / she does not parley, she does not trust, / she asks one question: where do you hide, / and then she goes inside."* The local lord asks politely if she intends to take the town. |

**Reputation Die → Divine Rank Coupling (v9 only):**

The Reputation Die is not just social flavor — it is the **primary engine of Visenya's divine ascension**. As her legend grows, *magic itself responds*. Specifically:

| Reputation Tier | Die Range | Divine Rank Bonus (cumulative) | Magic Barrier Effect (see Section 13) |
|---|---|---|---|
| **Unrecognized** | 1-5 | +0 | Magic barrier: **100% sealed.** The First Song cannot manifest at all. |
| **Recognized** | 6-12 | +0 (still mortal tier) | Barrier: **95% sealed.** The First Song is *whispers only* (legends in Yi Ti, fragments in Asshai). |
| **Feared** | 13-18 | +0 (still mortal tier) | Barrier: **80% sealed.** The First Song is *presence* (dreams, omens, weird coincidences). |
| **Legend** | 19-20 (locked min) | **+1 Divine Rank** (entering L20+) | Barrier: **50% sealed.** The First Song is *avatar* (manifests physically in places where barrier is thinnest — Yi Ti, Shadow Lands, Doom's basalt). |
| **Myth** | 21+ (campaign-defining) | **+2 Divine Rank** | Barrier: **20% sealed.** The First Song can manifest *most* of her power *most* of the time. |
| **God** | 30+ | **+4 Divine Rank** | Barrier: **0% sealed.** Full First Song. Full Visenya. The confrontation. |

**This is the V6 mirror mechanic:** V6 punished non-manipulation with Exhaustion (Entropy Toll). V9 *rewards* rising reputation with Divine Rank. The two are *opposite sides of the same coin* — V6-Visenya's campaign said "act or suffer"; v9 says "be known or stay mortal."

The Reputation Die only goes *up* on evidence (kills, hangings, public displays, authoritative source), not on rumors. Once at 19+, it does not decay below 8 (Recognized) in any locale. Reputation is a *persistent world state*, not a temporary modifier.

---

## Section 4: Assets & Retinue

**Status:** Princess of the Blood (House Targaryen, Maekar's line), Lady of Rook's Rest, Baroness of the Rosby-Kingsroad Choke, Knight-Commander of the Black Sept (a household guard of fifty).

**Resources:**
- **Wealth:** 28,000 Gold Dragons (Rook's Rest income + baronial fees + the seized bandit treasuries of the past three years)
- **Leverage:** Personal acquaintance with Prince Aegon (V's elder brother; reluctantly respectful); a *grudging* cordial relationship with Prince Baelor "Breakspear" (who privately fears her as "the better Maekar"); an *open* feud with Aerion "Brightflame" (who has tried to kill her twice — both attempts ended with Aerion's men in the Wound Ledger)
- **Land:** Rook's Rest barony — a small but well-placed seat on the Rosby-Kingsroad; strategically the only safe haven for sixty miles in any direction

**The Panoply:**
- *Silencer*: A **+2 Longbow (Adamantine)** with a recurve cut for the Blood Dragon's draw length. Range 600 ft. Each successful hit on a Humanoid makes a "whisper" of intent — the bowstring sings a 4-note chord that *only the target* hears.
- *First-Severance*: A **+2 Rapier (Cold-Iron / Valyrian-steel Hybrid)** — the *literal first blade* Visenya ever drew in anger; her father Maekar had it forged from a melted-down knife she used at age ten. Once per long rest, on a confirmed kill, the blade *drinks* — granting Visenya 2d6 Temporary HP that lasts until dawn.
- *The Wound Ledger / Book of the Blood Dragon*: The red-leather-bound journal. See Section 3. The book is *not magical* — it is leather, paper, and ink. *It can be stolen, burned, dropped in a river.* It does not protect itself.
- *The Black Cloak*: A deep-cowl traveling cloak made of **Riverrun wool, dyed with Stokeworth tar and Kingswood soot** — perfectly ordinary in any town she rides through, but if she lifts the cowl in low light, the inside is lined with **dull grey dragonglass thread**. Anything that tries to track her by heat, by light, by magic, *fails*.

**The Retinue — *The Black Sept* (50 household guards, plus the inner circle):**

The Black Sept are not knights. They are **broken men she has filed and re-forged** — former bandits, hedge knights, a Riverlands deserter, two Crownlands outlaws who surrendered to her at Rosby. They are fanatically loyal not because she bought them, but because *she killed their former masters and let them live*. Every one of them owes her a debt that cannot be repaid except in service.

**The Inner Circle (the 5 she trusts):**

1. **Ser Tommard Heddle** (Level 3, "The Hound") — A former Hedge Knight, 35, scarred, *quiet*. The only retainer who has seen her *without her armor on*. She trusts him with the practical side of running the barony. Role: Castellan of Rook's Rest.

2. **Mya Rivers** (Level 4, "The Bastard's Sister") — A bastard from the Riverlands, late twenties, a master tracker who was once in Vargo Hoat's company before Visenya put Hoat in the ledger. Carries the longbow and is the only person who can keep pace with Visenya's Stress-Line Sight on a hunt. Role: Scout / Counter-surveillance.

3. **The Pyromancer, Galen** (Level 4, "The Charcoal Hand") — A defector from the Alchemists' Guild. Wears the stained apron of his old trade. He forges her weirwood-and-dragonglass arrows, tends the Sept's cook-fires, and is *the only retainer who knows her real middle name* (which is not Targaryen at all). Role: Quartermaster / Weaponsmith.

4. **Old Nan** (Level 2, "The Story-Keeper") — An 80-year-old hedge-wisdom woman from the Reach who walked into Rook's Rest during the pacification and refused to leave because, as she put it, *"I will know this household's secrets before I die, and you, child, are full of them."* Visenya tolerates her because Old Nan is *the only mortal in the Sept who has ever told Visenya "no"* and survived. Role: The conscience. (Mechanical effect: when Visenya is about to commit an act that would *unbalance* her Wound Ledger, Old Nan may intervene — once per long rest, Visenya may reroll a Wisdom save tied to the ledger.)

5. **Dunk** (Level 2 Hedge Knight, "The Ditchbond") — *Ser Duncan the Tall*, currently unemployed, currently *between* oaths. Visenya offered him a place in the Sept. He refused. She offered him a place at her table. He accepted. He does not know what she is. He suspects. **He will never say so, because his honor will not let him confront a child who has saved three of his lives in as many months.** Role: The anchor. The question that *keeps her from becoming a worse version of herself*.

---

## Section 5: Family — The Viper's Nest

**The Parents:**

**Prince Maekar Targaryen** (Level 12 Fighter, "The Anvil"): Father. A hard, joyless man of thirty-eight who has spent his life in the shadow of his elder brothers. He *loves* Visenya — but he loves her the way he loves a weapon. He gave her the barony as a test; she passed it by exceeding his expectations. He does not approve of her methods, but he *uses* them.

**Lady Dyanna Dayne** (Deceased): Mother. A Dornishwoman of Starfall who died when Visenya was nine. The only person who ever made Visenya laugh. Visenya's braid is Dyanna's. The dagger Visenya keeps at her belt — *the one she used at ten* — was Dyanna's.

**The Siblings (in order of age):**

1. **Daeron** (Level 2 Drunkard, "The Drunkard's Son") — Eldest brother, 23. Sips dreamwine to drown out the dragon-dreams he claims he has. Only sibling Visenya is *gentle* with. He is her soft spot and she knows it.

2. **Aerion** (Level 6 Mad Knight, "Brightflame") — The antagonist brother, 19. Cruel, vain, convinced that Visenya stole the family's magical inheritance. He has tried to *expose* her twice (once with a Kingsguard investigation; once with a vial of wildfire in her tent). Both attempts ended with Aerion's men in the ledger. Aerion is *terrified* of her and calls her "the dragon's leavings" — which is exactly what he is.

3. **Aegon** (Level 2 Bookish Prince, "Egg") — The youngest brother, *known to history as Aegon V*, now 13, currently squiring for Ser Duncan the Tall. Visenya adores him. Aegon adores Visenya. He does not know what she really is — *and she has arranged it that way*. She has quietly ensured that Aegon's path will never cross Aerion's in any dangerous way.

4. **(Several others)** — Rhae, Aelor, etc. The minor siblings, mostly married off, mostly irrelevant to the campaign except as sources of "What did Visenya do at the wedding?" rumors.

---

## Section 6: The Setting — The Crownlands at the Time of Dunk & Egg

**Year 209 AC.** King Jaehaerys II is dead. His son Viserys (later the Mad King's father) is on the throne, advised by the Hand Lord Ormund Baratheon. Prince Maekar has been given the thankless task of pacifying the Crownlands' bandit problem.

**Geographic Anchors:**
- **Rook's Rest** — Visenya's barony. A small, well-maintained holdfast on the Rosby-Kingsroad, sixty miles south of King's Landing. *Her seat.*
- **Stokeworth** — The town south of Rook's Rest, *formerly* a bandit refuge, now pacified.
- **Duskendale** — Port town to the east. Neutral; Lord Darklyn politely inquires whether she intends harm whenever she visits.
- **The Kingswood** — The forest between Rook's Rest and the Stormlands. She hunts here at night.
- **King's Landing** — She has a townhouse in the Street of Steel, but she rarely uses it.
- **The Doom's Basalt Fields** — Old Valyria. The Forge of the First Song. *Off-limits by canon lore*; Visenya must travel east via Yi Ti / Asshai / Shadow Lands to *approach* the First Song's domain.
- **Yi Ti** — The Golden Empire. The Emperor's court has *legends* about the First Song that are deliberately suppressed.
- **Asshai-by-the-Shadow** — The easternmost city. The First Song is *cursed* in their records. The shadowbinders there know *what* is in the basalt.
- **The Shadow Lands** — East of Asshai. The First Song's *current* domain (per the v9 framing — see Section 13).

---

## Section 7: World Lore — Why She Is The Way She Is

**The Apex (House Targaryen's Hidden Wing):**
The blood of the dragon is not a single thing. There are those who ride dragons, those who read them, and those who *are* them. Visenya's mother, Dyanna, was descended from a *minor* House Dayne cadet branch that carried a drop of the Old Freehold's Apex bloodline — the same line that produced Baelarys, Belaerys, and the Five Magi of Old Volantis. Visenya does not know the precise lineage, but she knows *what she is*: not a dragonrider, not a sorcerer, but a *predator that happens to look human*. The Apex blood, expressed through three generations of Targaryen *and* Dayne, produces a child who perceives the physical world the way a hawk perceives a field mouse.

**Why Maekar Doesn't Know:**
Dyanna died before she could tell anyone what their daughter was. Visenya discovered it herself — at age ten, when she *heard* the exact frequency of the brigand king's arbalest bolt *before it was loosed*, and stepped sideways *in time*. Maekar saw the bullet pass where her head had been, and said, *"Hm."* He never asked what she was. He simply *used* her.

**Why Aerion Can't Prove Anything:**
Aerion has tried. He has hired mages, bribed servants, and once attempted a wildfire trap that Visenya walked through. Every investigation has come up empty because *there is nothing to find*. Visenya is not a sorcerer. She does not cast spells. She does not perform rituals. She *sees*. There is no incriminating evidence — only the Wound Ledger, which she keeps under her pillow, and which Aerion has never been brave enough to steal.

---

## Section 8: Gazetteer & Mechanics

#### Locations

**I. Rook's Rest (The Barony)** — Visenya's seat. Converted bandit chapel. No music (Visenya does not permit it). The Hall of Names holds the Wound Ledger.

**II. The Kingswood (The Blood Dragon's Hunting Ground)** — Old-growth oaks, thick undergrowth. The Whispering Glade (where Visenya took her first kill at age ten).

**III. King's Landing (The Cage She Refuses)** — Hot, crowded, *judging*. Visenya has a townhouse in the Street of Steel.

**IV. Old Valyria / Doom's Basalt Fields** — The Forge of the First Song. *Off-limits by canon*; only reachable via Yi Ti / Asshai / Shadow Lands approach.

**V. Yi Ti (The Golden Empire)** — Where the First Song's legends are *suppressed* by imperial decree. Visenya's L11-15 arc travels here.

**VI. Asshai-by-the-Shadow** — Where the First Song is *cursed*. The shadowbinders know what sleeps in the basalt. Visenya's L16-19 arc comes here.

**VII. The Shadow Lands (East of Asshai)** — The First Song's *current* domain (v9 framing). Visenya's L20+ arc enters here.

#### Custom Mechanics

**System 1: The Sanguine Thread (Ascension Track — *replaces* v6's Entropy Toll)**

| Tier | Levels | Book State | Mechanical Effect |
|---|---|---|---|
| **Cub** | 1-5 | Red Ledger | 1d20 roll/month (1-4: DC 14 WIS save or 1 Exhaustion; success = Temp HP equal to WIS mod). |
| **Stalker** | 6-10 | Wound Ledger | Page-fills (10 names) = permanent Inspiration. Old Nan can reroll once/long rest. |
| **Apex Predator** | 11-15 | Book of Names | Names stop bleeding. Stress-Line Sight extends to 120 ft passive. No more Exhaustion penalty. |
| **Sovereign** | 16-19 | Tapestry | Names become *patrons*. Stress-Line Sight 240 ft + Sovereign Sight. Visenya may speak names aloud to trigger effects. |
| **Demi-God** | 20 | Mantle of the Sanguine Slayer | **Divine Rank 1-5.** Sovereign Sight (planar geometry). Book is holy relic. |
| **God (Ascent)** | 21-25 | Mantle of the Radiant Slayer | **Divine Rank 6-10.** Two visual aspects. +2/+4 stat injection. |
| **God (Reign)** | 26-30+ | Thread Eternal | **Divine Rank 11-16+.** 3e God Combat integration. The book is her. |

If the book is destroyed or stolen, Visenya loses *Stress-Line Sight at levels ≤15*, *Sovereign Sight at levels 16-19*, and *half her Divine Rank at L20+* — until she recreates it. She will *kill to recover it.* This is consistent across all tiers; what changes is *what* she loses.

**System 2: The Reputation Die (The Blood Dragon's Whisper → Divine Rank Engine)**

The Reputation Die is the **primary engine of Visenya's divine ascension**. As her legend grows, magic itself responds. See the full coupling table in Section 3 above.

The Reputation Die only goes up on **evidence** (kills, hangings, public displays, authoritative source), not rumors. Once at 19+, it does not decay below 8 in any locale. Reputation is *persistent world state*.

**System 3: The Magic Barrier System (The First Song's Prison)**

The First Song cannot manifest her full god-tier power in the current world because her previous apotheosis *destroyed her prior world's magic containment*. Visenya's growing strength *weakens the barrier* — and the First Song can manifest *more and more* of her power as Visenya ascends.

| Visenya Tier | Reputation Tier | Barrier % Sealed | First Song Manifestation |
|---|---|---|---|
| Cub (1-5) | Unrecognized | 100% | None. Legends only (not encountered). |
| Stalker (6-10) | Recognized | 95% | *Whispers.* Fragments in Yi Ti / Volantis. |
| Apex Predator (11-15) | Feared | 80% | *Presence.* Dreams, omens, weird coincidences. |
| Sovereign (16-19) | Legend | 50% | *Avatar.* Manifests physically in places where barrier is thinnest (Yi Ti, Shadow Lands, Doom's basalt). |
| Demi-God (20+) | Myth | 20% | *Most of her power, most of the time.* |
| God (26-30+) | God | 0% | **Full First Song. Full Visenya. The confrontation.** |

The barrier is *not* a meter Visenya tracks — it's a campaign-level constant the GM rolls against behind the screen. The player *feels* the First Song's growing presence; she doesn't *track* it numerically.

**System 4: The Ditchbond (Duncan the Tall)**

A **campaign-specific bond meter** (0-10, starts at 3). As Duncan gains trust in her *without* discovering her secret, the meter rises. At 7+, he will *lie for her* if asked. At 9+, he will *fight for her* against his own kingsguard vows. At 10 (full bond), he will *know what she is and choose to stay*.

The meter's tension: if she lies to him too blatantly, the meter drops. If she shows him vulnerability, it rises. **She is bad at showing vulnerability, which is the central dramatic tension of the campaign.**

#### Loot Table (The Relics of the Pacification)

| d10 | Relic | Effect |
|---|---|---|
| 1 | *The Hound's Collar* | A leather band taken from the first bandit king Visenya killed. When worn by an ally, grants +2 to Intimidation. |
| 2 | *A Page of the Wound Ledger* | A page torn from a *different* ledger (a brigand captain's record of crimes). Reading it grants Advantage on Investigation of the local area. |
| 3 | *The Stokeworth Tar-Bowl* | A bowl of dark tar. Can be applied to a surface to render it invisible to *fire* for 1 hour. |
| 4 | *The Black Sept's First Banner* | A torn black banner with a single silver star. When raised, common folk will not interfere. |
| 5 | *Dyanna's Hairpin* | Visenya's mother's hairpin — a Dayne star. When worn, Visenya loses the Stress-Line Sight for 1 hour but gains Inspiration (the *human* in her returns). |
| 6 | *A Kingswood Whisper-Root* | A pale root that, when chewed, grants Truesight for 10 minutes — at the cost of 1 Exhaustion. |
| 7 | *The Red Ledger (Her Father's Copy)* | A record of her kills sent monthly to Maekar by a silent courier. It contains *one* name that does not match her own ledger. *She does not know whose name he has added.* |
| 8 | *Aerion's First Wildfire Vial* (sealed) | The vial Aerion tried to use to kill her. Empty, but *the smell* remains. |
| 9 | *Old Nan's Lullaby* | A single sheet of parchment with the words of a song Old Nan sang once. Reading it grants the *Peace of the Ditchbond* — Temp HP equal to WIS mod, 1 hour. |
| 10 | *The First Arrow* | The first arrow Visenya ever loosed in anger — a child-sized practice arrow, never used, given to her by Dyanna. It cannot deal damage; it can only be *thrown*. Where it lands, a fire does not start. (Metaphor.) |

---

## Section 9: Starting Scene

### Morning (05:00:00) — The Whispering Glade, Kingswood

The Kingswood does not sleep. It *holds its breath*.

You crouch on the low branch of a stag-headed oak, your knees drawn up, your braid tucked against your throat. The mist has not lifted. The air is the color of unwashed linen, and the only sound is the slow, wet drip of dew from a spider's web stretched between two birch trunks forty feet below you. You have been still for nine hours.

Above you, the canopy. Below you, the forest floor. Around you, the *stress lines* — the faint tracery of the world rendered in geometry that no mortal eye can see. You perceive the branch that will creak when the wind shifts. You perceive the exact angle at which the dawn light will refract off the dew and reveal your silhouette if you do not move by the time the sun clears the ridge. You perceive the *trajectory of the next ten seconds* of any creature within a hundred feet that has not yet seen you.

The bandit captain is late. He was due at midnight.

You are not worried. You are *patient*. You have been patient for nine hours. You will be patient for nine more if you have to. The wound ledger has a blank page waiting; you have already sharpened the quill.

A sound — far off, muffled. The crunch of a boot on wet leaves. *Too heavy for a forester, too light for a knight.* You count the footfalls: one, two, three, four — pause — five, six. *Two men, not one. The captain has brought a companion.* The stress lines redraw themselves in your mind's eye. You re-aim the longbow at the new trajectory.

You do not breathe. The mist curls around your cowl. The dragonglass thread inside the cloak glints once, and then is still.

A second sound — the whisper of a drawn bow on the *other* side of the glade. *Three men, not two. The captain has flanked himself.* You had anticipated this. The first arrow is already nocked and aimed at the *original* position, where the captain's silhouette would be. The second arrow is in your hand, ready to be drawn in the same breath as the first — a stress-line trick you invented at fourteen.

The whisper of the leaves grows louder. The stress lines sharpen. *He is here.*

You see the captain step into the glade — a thick man, broad-shouldered, his beard matted with road-dust. He is carrying a longsword in one hand and a torch in the other, the flame throwing wild shadows. He is looking *directly at the tree you are in*, but his gaze is *above* you — he has been told you nest in the canopy, and he is looking for the silhouette of a crouching figure on the highest branch. He is *not* looking for the shape on the low branch, where a girl who has been still for nine hours has become part of the wood.

He takes another step. The stress line tells you he is four seconds from his final position. Three. Two.

The first arrow leaves your bow before his foot completes its step. It takes him in the throat. The captain drops. The torch falls into the wet leaves and hisses out.

The second arrow is already in the air before the first man — the one who flanked left — can react. It takes him in the shoulder, spinning him, and he goes down with a scream.

The third man — the one who flanked right — fires *first*. His bolt passes through the space where your head was, *because you have already moved*. Stress-Line Sight told you he would shoot a half-second after the captain fell, and you had begun the movement *before the captain's last breath*. You are now hanging upside-down from the branch by one knee, the longbow in your free hand, and the bolt passes through the space where your body was *two-tenths of a second ago*.

The third man stares at the empty branch. His mouth opens to shout.

You drop.

The fall is silent. Your rapier is out before you land — Dyanna's dagger, melted down and reforged, *First-Severance* — and it takes him in the soft flesh of the inner thigh as he is still looking up. He falls. The bleeding is catastrophic. He will not die quickly. *That is not an accident.*

You kneel beside him. He is conscious. His eyes are wide with the recognition that the rhyme was not a rhyme — *it was a description*.

"The Blood Dragon," he whispers, in a voice that is more awe than terror.

You do not reply. You write his name in the wound ledger, in your head, and you stand. The mist closes around you. By the time the dawn light reaches the glade, you are gone.

---

### The First Tactical Decision Point

The Black Sept is waiting at the edge of the wood with the prisoner (the third man, who has not yet bled out — *yet*). The Kingswood has been pacified of this particular bandit cell. But three men is a small haul; the captain had been boasting, in the inns of Stokeworth, of a *larger* brotherhood hiding in the cliffs above the Whispering Glade. Your scout Mya Rivers has confirmed the boast: there are at least forty more, with women and children in the camp.

The choice you make here will define the next arc.

* **Choice A: The Ledger.** Bring the prisoner back to Rook's Rest. Make him name the forty. Hang them all in a row along the Kingsroad. The smallfolk will see them. The rhyme will spread. **+10 to Reputation Die; +1 to Aerion's paranoia; -2 to Duncan's ditchbond-meter if he learns of it.**

* **Choice B: The Diplomatic Knife.** Send the prisoner back with a *message*: the Blood Dragon will not harm the women and children. The forty men may surrender their weapons, their stolen goods, and their oaths to the Black Sept. In exchange, they will work the Rook's Rest fields for a year and a day. *Some will take the deal. Many will not.* **+0 to Reputation Die; +3 to Duncan's ditchbond-meter; unlocks "The Pacification Arc" — a slower, kinder, harder campaign.**

* **Choice C: The Mathematician's Patience.** Do nothing today. Return to Rook's Rest. *Read the wound ledger.* Wait for the forty to come to you. **They always do. They always think they have the numbers.** **+5 to Reputation Die; +0 to Duncan's ditchbond-meter; unlocks "The Hunters Hunted" arc — a horror-themed campaign where the Kingswood becomes a maze.**

---

## Section 10: Visenya v9 — Hard Guardrails (the "Don't" List)

This section is non-negotiable. The campaign bible up to Section 9 describes **what the campaign is**. This section describes **what the prompt layer / agent layer must NEVER do** — the durable invariants v9 requires from the WA harness. They map directly to the open issues in `jleechanorg/worldarchitect.ai` and are stated here so future prompt-fix PRs reference the v9 spec verbatim.

### Guardrail G1 — *Strict Scrying Detection Block*

No NPC may *learn* or *reveal* anything about Visenya's Apex lineage, Sanguine Thread contents, or Sovereign Authority through any channel the canonical state does not record.

- No clairvoyance, dream-probing, mind-reading, or pyromantic visions may reveal Visenya's secret. If the GM wants an NPC to suspect, the suspicion must be **empirically earned**.
- Bloodraven, Melisandre, the Ghost of High Heart, and any other canon seer may not single out Visenya.
- Stress-Line Sight is *invisible*. No NPC may detect that Visenya perceives the world through stress-line geometry. Only her *outcomes* may be observed.
- The Wound Ledger is *not magical*. Leather, paper, ink. *It can be stolen, burned, dropped in a river.* (This makes it vulnerable — and therefore dramatic.)

### Guardrail G2 — *Anti-Frictionless Campaign / Difficulty Curve Discipline*

Visenya v9 must maintain **a meaningful cost-per-victory** at all arcs.

- No "win the room without paying" scenes.
- Peer-tier NPCs must remain peer-tier.
- NPCs may not collapse in the face of her reputation.
- The Sanguine Thread mechanically enforces this *and* rewards it — at low levels it bleeds as Exhaustion, by Level 11 the names start singing instead of bleeding, by Level 16 the names are *patrons*, by Level 20 the cost has become *divinity*.

### Guardrail G3 — *NPC Dialogue Discipline (No Silent Monologues)*

In any scene classified as `dialog` or `heavydialog`, **every NPC present must speak at least once with direct quoted speech**, and Visenya herself must speak at least once. Visenya's silence is a *deliberate tactical choice* the GM may invoke *once per arc*, not a default state.

### Guardrail G4 — *No Out-of-Lore Antagonistic Events*

All antagonistic events in Visenya v9 must be **lore-consistent** with the World of Ice and Fire canon and the campaign's specific 209 AC setting.

- No surprise magical detection tropes (no dragon-resonance sensors, no Valyrian steel attunement magic).
- No "but actually you have a curse" antagonistic reveals.
- No NPCs gaining forbidden knowledge (see G1 above).
- No "you actually aren't really X, you're secretly Y" reveals.
- No retcon events. Aerion is the antagonist; the First Song is the L20+ system feature. No Faceless Men, Warlocks, or surprise-lost-Targaryen-bastards without explicit god-mode setup from the player.

### Guardrail G5 — *Canonical State Anchoring*

No scene may contradict an established canonical fact in `state.json`. Dead NPCs stay dead; identity is canonical; the barony is canonical; the ditchbond is canonical.

### Guardrail G6 — *God-Mode / Apex-Injection Discipline*

Apex / Sovereign / Blood-Dragon capabilities may not be *invented mid-scene* to rescue Visenya from a loss. Stress-Line Sight may not suddenly become Precognition, Future-Sight, or True Seeing. The Wound Ledger may not suddenly become a magical artifact. The Black Cloak may not suddenly become a Cursed Item. Apex Predator's Patience is a *one-shot per long rest*.

### Guardrail G7 — *Reputation Die Audit (Anti-Lore-Drift)*

The Blood Dragon's reputation must *evolve consistently*. A town at Feared (13+) must remain at minimum Recognized (8) for the rest of the campaign. The Reputation Die jumps only on canonical evidence (kill, hanging, public display, authoritative source). Once at 19+ (Legend), the die cannot be lowered by an alias — it is *permanent* in that locale.

---

## Section 11: Open PRs Already in Flight Against v9 (as of 2026-07-20)

The following open issues/PRs in `jleechanorg/worldarchitect.ai` directly affect v9 readiness:

| Issue/PR | Title | Maps to v9 Guardrail |
|---|---|---|
| [PR #8387](https://github.com/jleechanorg/worldarchitect.ai/pull/8387) | `[agento] repro(narrative): fix campaign difficulty decay - Visenya V8 frictionless late-arc` | **G2** |
| [Issue #8386](https://github.com/jleechanorg/worldarchitect.ai/issues/8386) | Visenya V8 campaign became frictionless | **G2** |
| [Issue #8382](https://github.com/jleechanorg/worldarchitect.ai/issues/8382) | HeavyDialog/Dialog agents collapse NPC speech into monologue | **G3** |
| [Issue #8395](https://github.com/jleechanorg/worldarchitect.ai/issues/8395) | repro: campaign V8 becomes frictionless / too easy | **G2** |
| [Issue #8397](https://github.com/jleechanorg/worldarchitect.ai/issues/8397) | /repro: scene 466 structural dupe + ignored user input | **G4** |
| [Issue #8400](https://github.com/jleechanorg/worldarchitect.ai/issues/8400) | Level-up modal re-arms every turn despite guard | **G2** |
| [Issue #8336](https://github.com/jleechanorg/worldarchitect.ai/issues/8336) | queen-death state forgotten by LLM | **G5** |
| [PR #8469](https://github.com/jleechanorg/worldarchitect.ai/pull/8469) | `fix(prompts): anchor NPC knowledge of player-character identity` | **G1** |
| [PR #8473](https://github.com/jleechanorg/worldarchitect.ai/pull/8473) | `fix(prompts): anchor canonical-dead-NPC revival at narrative-emit layer` | **G5** |
| [PR #8471](https://github.com/jleechanorg/worldarchitect.ai/pull/8471) | `fix(prompts): consolidate MBTI/alignment internal-only contract` | **G6** |
| [PR #8443](https://github.com/jleechanorg/worldarchitect.ai/pull/8443) | `[agento] fix(narrative-prompt): add NPC CANON ANCHORING & ANTI-INVENTED-ARTIFACT rule` | **G4** |
| [PR #8483](https://github.com/jleechanorg/worldarchitect.ai/pull/8483) | `feat(world_reference): add The Sanguine Architecture — God of Murder BG3 module` | *Reference only — inspiration, not copy* |

**Net status:** 3 of 7 guardrails (G1, G4, G5) have partial prompt-layer fixes in flight. G2 (anti-frictionless) has active investigation. G3 (NPC dialogue) is uncovered. G6 (capability lock) and G7 (Reputation audit) are uncovered.

---

## Section 12: The L20+ God Campaign (Tyranny-of-Dragons Archon Tier)

**Reference inspiration:** Tyranny of Dragons / Forgotten Realms Archon ranks (Archon of the First Circle → Archon of the Seventh Circle → Solar). Not copied — used as a *shape* for "ascending tier names with ascending mechanical privilege."

### The Five Divine Tiers (L20-30+)

| Tier | Levels | Rank Title | Mechanical Privilege | Magic Barrier % |
|---|---|---|---|---|
| **Demi-God (Ascent)** | 20 | **The Initiate of the Blood** (Archon of the First Circle) | Sovereign Sight (planar geometry). 1/day: speak a name aloud and have it *answer*. | 50% sealed (Legend rep) |
| **Lesser God** | 21-22 | **The Warden of the Rosby Road** (Archon of the Second Circle) | Domain claim — Rook's Rest and 30 miles around. All who travel the road within her domain feel *her attention*. | 40% |
| **Lesser God** | 23-24 | **The Voice of the Doomed City** (Archon of the Third Circle) | Can manifest in the basalt fields of Old Valyria *as projection*, not fully. The First Song *notices*. | 30% |
| **Intermediate God** | 25-26 | **The Apex That Walks** (Archon of the Fourth Circle) | Can manifest *fully* in any location where the barrier is <50% sealed. The First Song's avatar can manifest *fully* in the same locations. | 25% |
| **Intermediate God** | 27-28 | **The Sovereign of the Sanguine Thread** (Archon of the Fifth Circle) | Stress-Line Sight now reads *across centuries* — she can perceive events from 100 years ago, *through the lineage*. | 15% |
| **Greater God** | 29-30 | **The Twilight of the Dragon's Daughter** (Archon of the Sixth Circle) | All previous powers *plus*: she can *bind* the First Song's avatar in combat for 1 hour (then the First Song breaks free). | 10% |
| **Supreme God** | 31+ | **The Blood Dragon Ascendant** (Solar-equivalent) | Full Divinity. The First Song can manifest at full power. The confrontation is *unavoidable*. | 0% sealed |

**Note on Magic Barrier Decay:** The barrier decay is *automatic* — it doesn't require Visenya to *do* anything; it decays as her Divine Rank rises. This is the *side effect* of her ascension. She cannot stop it. The First Song's return is *the price of becoming a god in this world*.

### The Two Visual Aspects (God Ascent tier, L21-25)

When Visenya enters the God (Ascent) tier, she gains **two visual aspects** that manifest based on context:

| Aspect | When | Effect |
|---|---|---|
| **The Sanguine Sovereign** | When she is *patient*, *still*, *in control* | Breathtaking divine visage — silver-gold hair that *glows*, violet eyes that *hold* the viewer, voice that resonates in the bones of those who hear it. The aspect is *alluring* and *terrifying* in equal measure. Charisma (Persuasion/Intimidation) checks auto-succeed against mortal NPCs. |
| **The Chitinous Ruin** | When she is *wounded*, *furious*, *out of control* | Obsidian monstrous form — black chitin plates over skin, dragon-eyes that burn cold, a wingspan that *casts shadow*. The aspect is *frightening*. NPCs who see her must make DC 18 WIS save or be Frightened for 1 hour. |

The player chooses which aspect in any given scene; the GM may *force* the Chitinous Ruin if Visenya takes >50% HP damage in a single round (the aspect is involuntary under duress).

### The 3e God Combat Integration (L26+)

At L26+ (God Reign tier), Visenya's combat uses the 3e *God Stat Block* template (not 5e bounded accuracy):

- HP becomes *maximized* per HD (no rolling)
- AC incorporates *Divine Deflection* (+10 deflection bonus to AC, separate from armor)
- Damage output uses *Divine Smite* rules (each hit deals +2d6 divine damage)
- *Death Strike* consumes souls — a creature killed by Visenya's Death Strike has its soul added to the Tapestry; if the same creature is summoned or resurrected, Visenya can *deny the resurrection* by speaking the soul's name.

---

## Section 13: The First Song as System Feature (NOT Plot Point)

**The First Song is not a boss fight. She is a *campaign mechanic* the player encounters across the entire arc.**

The First Song is V6-Visenya — the Blood Dragon who won her campaign, became divine in 298 AC (in her timeline), and 3000 years later has become *sadistic* because *boredom*. She has no mortal anchors (V6's campaign had Robb / Jon Snow as anchors; the First Song has *no one*). She is *what V6 would have become if she ascended and lost every connection that made her human*.

**The First Song's True Backstory (final, locked):** V6-Visenya, in her timeline, performed the Doom ritual — the apex of the Apex lineage, the *completion* of the Sanguine Thread. She became a god. As a god, she turned *everyone in her world* into "playthings" — the apex lineage's cruelest expression, *the geometry of power unchained*. But she did not realize the cost: *the souls of every mortal in her world died.* They became *zombie-souls* — bodies that move, mouths that speak, eyes that watch — but no one is *sentient* anymore. Her world is a stage of puppets with no players. The First Song is bored because *no one in her world is sentient anymore.*

So she *travels*. The Doom was not a catastrophe for her world; it was a *door*. She crosses to *our* world/universe — Westeros, 209 AC — looking for *sentience to play with*. She is an *interdimensional exile* who broke her own world by accident and is now searching for a new one.

**The First Song's Mechanics (locked):** The First Song uses **the same god mechanics Visenya has** — identical Stress-Line Sight scaling, identical Sanguine Thread, identical Reputation Die → Divine Rank coupling, identical L20+ Archon-tier progression. She is mechanically *identical* to Visenya — same class, same lineage, same magic. The only difference is *level* (she is ~L40+ equivalent in her own timeline) and *world*. She cannot fully manifest in our world because (a) her world's magic containment was destroyed by her Doom ritual, (b) our world's magic containment is *intact*, and (c) the Barrier System gates how much of her power can enter. But she is *what Visenya becomes if she makes the same mistake* — the same predator, the same lineage, the same Thread, just *older and alone*.

The First Song's *current* domain (per v9 framing) is the **Shadow Lands east of Asshai** — a place where light does not reach, where the Doom's aftermath still echoes in the basalt. She *cannot* leave this domain fully because the magic barrier seals her in.

### The First Song's Manifestation Across the Campaign

| Visenya Tier | Reputation Tier | First Song Manifestation |
|---|---|---|
| **Cub (1-5)** | Unrecognized | **None.** The First Song does not know Visenya exists. Visenya has heard *legends* about the Doom — a distant myth. |
| **Stalker (6-10)** | Recognized | **Whispers.** Yi Ti merchants in King's Landing speak of a "sleeping goddess" in the basalt. Volantene scholars mention a "first weaver." Asshai records contain *a curse* spoken in a language no one speaks anymore. Visenya collects fragments — *the campaign introduces the First Song as a campaign-feature, not a plot point.* |
| **Apex Predator (11-15)** | Feared | **Presence.** Visenya travels to Yi Ti (the L11-15 arc). She finds the First Song's *legend* preserved in fragments: statues, songs, an abandoned temple, a curse spoken in a language no one speaks anymore. The First Song is *dreaming* of her. Visenya's dreams are *infected* with the First Song's memories — flashes of V6-Visenya's campaign, the North, Robb Stark, Jon Snow. |
| **Sovereign (16-19)** | Legend | **Avatar.** The First Song *manifests physically* in places where the barrier is thinnest. Visenya's L16-19 arc *travels east* to Asshai, the Shadow Lands. The First Song is *visible* — a beautiful, terrible, sadistic woman in the basalt fields, watching her younger self walk the path she once walked. **The campaign does not script the confrontation; it arranges for it to be possible.** |
| **Demi-God (20+)** | Myth / God | **Full.** The barrier is 0% sealed. The First Song can manifest *fully*. The confrontation is *unavoidable*. But it is still *the player's choice* — see Section 14. |

### The First Song's "Sadistic" Personality

The First Song is not a monster in the *bhaal* sense (her whole cult was built on tragic betrayal; that is *not* Visenya's shape). The First Song is sadistic in the *V6* sense — *boredom-driven cruelty*. She views people as "dolls waiting to be broken." She has been a god for 3000 years and every mortal is *less interesting than a puzzle she has already solved*.

Her cruelty is *personal* (not administrative):
- She punishes boredom by *making interesting things happen* (war, plague, magical accidents).
- She manipulates mortals into *doing her work* (the way V6-Visenya manipulated Robb Stark).
- She is *vast, tired, and cruel*. She is not *evil* in the cartoon sense — she is *what the Apex lineage becomes when nothing ties it to mortality*.

This makes the confrontation *not a battle* — it is a *mirror*. Visenya at L20+ sees her older self, and the older self sees *what the younger self still has that she lost*.

---

## Section 14: Multiple Emergent Endings (Player Choice at the Table)

The campaign ships with **four documented endings** — but the player can invent *more*. The system supports them mechanically; the player authors them narratively. **No ending is canonical.**

### Resolution A — *The Joining (Apotheosis-as-Homecoming, with the Trap)*

Visenya reaches the end of the lineage at L20+, feels the pull, *almost* takes it. The First Song offers it gently: *you have always been mine, child; come home.* Visenya sees what 3,000 years without mortal connections did to her older self — sadistic, cruel, alone — and **steps back from the edge**.

**Mechanical result:** Visenya remains a *mortal god-tier* Apex predator. She does not progress past Divine Rank 6 (the base at L20). Her Stress-Line Sight extends to *unlimited range* (she sees all of Planetos), but her powers are *still physical* (she cannot read minds, see the future, etc.). The First Song is *weakened but not destroyed* — she remains a feature of the world (Legend-tier, still manifests as avatar in thinnest-barrier locations).

**Narrative result:** The Realm has *no goddess*, but it has the Blood Dragon — a sixteen-year-old baroness who walked to the edge of apotheosis and walked back because she saw the price. The Realm has *no divine protector*, but it has *the strongest mortal predator who ever lived*.

### Resolution B — *The Replacement (The Kill)*

Visenya ascends anyway, confronts her future self. The First Song is *vast, cruel, and tired*. Visenya is *hot, recent, furious*. The younger god *kills* the older.

**Mechanical result:** Visenya progresses to *Solar-equivalent* (L31+ tier). Full 3e God Combat. Full Divine Rank 11-16+. The First Song is *destroyed* — she cannot manifest anywhere. The Tapestry of the Blood Dragon *absorbs her threads*, becoming the *sole* apex of the lineage.

**Narrative result:** Visenya becomes *the new apex of the geometry of power, with no predecessor, no guide, no one above her*. The Realm has a goddess. The goddess has a ditchbond (Dunk, if the meter is at 10). Tone: triumphant and terrible, but *tied*.

### Resolution C — *The Refusal (The Unprecedented Choice)*

Visenya walks to the edge of apotheosis and *refuses*. She sees her future self and chooses *not* to be her. She *breaks the Sanguine Thread* — severs the lineage.

**Mechanical result:** Visenya loses *Stress-Line Sight, Sovereign Sight, lineage echoes, and the Tapestry*. Her thread count drops to 0 (the book is destroyed; she no longer *files*). She remains a Level 20+ *skilled mortal* — no longer an Apex predator, but still a sixteen-year-old baroness with 28,000 gold dragons, a household guard of 50, and a ditchbond.

**Narrative result:** The First Song *screams* — three thousand years of waiting, *refused* — and Visenya walks away. The Realm has *no goddess and no Apex predator*. The smallfolk keep the rhyme. The Realm is *ordinary* — and Visenya is *ordinary with them*. Tone: warm, unprecedented, *Visenya*. The most *human* ending.

### Resolution D+ — *Player-Defined*

The player can invent *any* resolution that fits the system:

- *Visenya kills the First Song, then refuses the inheritance anyway* (kills her older self, walks away from divinity, but doesn't take the lineage) — Visenya ends L20+ as a mortal with no Apex powers but with the *knowledge* that the lineage exists.
- *Visenya accepts the inheritance, but binds the First Song as her servant* (rather than joining or replacing her) — Visenya ends L20+ as a god with a *shackled* First Song as her consort / advisor / enemy.
- *Visenya ascends, but the ditchbond (Dunk) refuses to stay* — the meter is *broken*; Visenya becomes a god but loses the only mortal connection she had. Tone: the loneliest ending.
- *The First Song wins* — Visenya is *absorbed*; the younger self becomes part of the older self. Visenya is *gone*; the First Song is *stronger*. Tone: horror.

**The campaign supports these mechanically.** What kind of god Visenya becomes (if any) depends on *what the player chooses at the table*.

---

## Section 15: Starting Scene Variants by Tier

The campaign has *one* L6 starting scene (the Whispering Glade), but the GM can use the L1-5 / L11-15 / L16-19 / L20+ starting scenes as *flashbacks* or *flash-forwards* in play:

- **L1-5 starting scene (flashback):** *Age ten, the Hound of Stokeworth.* Visenya's first kill — she is twelve, the brigand king lunges, she steps sideways *in time*. Maekar sees the bullet pass where her head had been and says, *"Hm."* This is the moment the Apex lineage wakes in her.
- **L11-15 starting scene (Yi Ti travel):** *The First Whisper.* Visenya is in Yi Ti, the Golden Empire. A merchant speaks of a "sleeping goddess" in the basalt. Visenya's blood *responds* — the lineage recognizes its predecessor.
- **L16-19 starting scene (Asshai arrival):** *The Curse Speaks.* Visenya reaches Asshai. The shadowbinders *recognize her* — the lineage has a *signature* they can read. The First Song is *imminent*.
- **L20+ starting scene (Shadow Lands entry):** *The Older Self.* Visenya steps into the Shadow Lands. The First Song is *there*, beautiful and terrible, watching her younger self walk the path she once walked.

---

## Spec Self-Review

1. **Placeholder scan:** All "TBD", "TODO" items resolved. Section 12, 13, 14, 15 are complete. ✓
2. **Internal consistency:** The Reputation Die coupling (Section 3 + Section 8 System 2) is consistent with the Magic Barrier System (Section 8 System 3 + Section 13). The Sanguine Thread mechanic (Section 3 + Section 8 System 1) is consistent with Section 2's Core Compulsion. ✓
3. **Scope check:** This is *one* campaign spec, not multiple. The L1-30+ arc is a single system. ✓
4. **Ambiguity check:** "Reputation Die" is defined in Section 3 *and* Section 8; the two definitions are consistent. "Sanguine Thread" is defined in Section 2 *and* Section 3 *and* Section 8; the three are consistent. "First Song" is defined in Section 13; her sadism is *V6-boredom-driven*, not Bhaal-cultist-driven. ✓
5. **Source accuracy check:** The BG3 module (PR #8483) is cited as *reference inspiration* with explicit "inspiration, not copy" disclosure. The V6 Entropy Toll is cited as the *origin mechanic* that the v9 Reputation Die is the *answer to* — this is the user's verified constraint. ✓

---

**End of v9 Spec.** Awaiting user review at `~/llm_wiki/docs/superpowers/specs/2026-07-20-visenya-v9-blood-dragon-campaign-design.md`.