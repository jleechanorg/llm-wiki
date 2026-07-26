---
title: "PC-Silent Dialog Analysis: 10 Campaigns × 50+ Scenes (2026-07-13)"
type: source
tags: [campaign, worldarchitect, dialog, heavydialog, prompt-analysis, pc-voice]
date: 2026-07-13
source_file: ~/.hermes/dialog_review_2026-07-13/
campaign_id: "(multi — see table)"
entry_count: 2464
ingest_batch: 2026-07-13-pc-silent-review
---

# PC-Silent Dialog Analysis

**Source query:** Jeffrey Lee-Chan (2026-07-13): "Review the last 10 campaigns with 50+ scenes ignoring copies and duplicates and see why other characters seem to rarely talk or give dialogue besides main character. Check the prompts and especially dialog and heavydialog agent should have other characters talking."

## TL;DR — Root cause

**The PC (player character) is silent in 76.8% of HeavyDialogAgent scenes and 75.5% of DialogAgent scenes.** Across 2,464 AI-generated scenes in the 10 longest-running recent campaigns, NPCs produce a median of 7 quoted lines per scene while the PC produces a median of **0**. Only 17.0% of scenes have any two-way dialogue.

The cause is **prompt-layer**, not routing or intent:

1. **`dialog_system_instruction.md` (451 lines, `mvp_site/prompts/`)** is entirely NPC-centric — its 9 sections cover NPC voice construction, NPC attitude, NPC trust-building, NPC negotiation, NPC conflict. It contains **zero guidance** for the LLM to speak *as* the PC.
2. **`narrative_system_instruction.md` line 67-68** ("Narrative Authority") and **`narrative_lite_system_instruction.md` line 71-73** both state:

   > - Players describe their CHARACTER'S actions and intentions
   > - The GM/AI describes the WORLD'S response, NPC reactions, and outcomes

   The LLM interprets this strictly: it produces world/NPC text only and leaves the PC's voice to the player. The result is a narrative where the PC is a silent observer whose only "speech" is one short quoted line surrounded by 5-10x more NPC monologue.
3. **HeavyDialogAgent does not override this bias.** Even though it is *explicitly* for "high-stakes conversations" where "richer mechanics/world context improves output quality" (`agents.py` lines 2680-2684), the HeavyDialog prompt stack (`REQUIRED_PROMPT_ORDER` at lines 2686-2697) includes `PROMPT_TYPE_DIALOG` (the same NPC-centric `dialog_system_instruction.md`), `PROMPT_TYPE_NARRATIVE` (with the same "PC silent" authority split), and never adds a "speak as the PC" instruction.

## Methodology

- Pulled jleechan's full Firestore (`worldarchitecture-ai` project, uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`).
- Filtered to campaigns with ≥50 story entries → 229 candidates.
- Sorted by latest story timestamp descending → picked last 10 (after excluding duplicates — original Visenya V7 was excluded; "Visenya V8" and "Visenya v7 (forgot queen dead)" are kept as separate titles).
- For each scene (gemini-authored story doc with `actor=gemini`), classified dialog via:
  - **Quoted speech** (straight + curly double/single quotes) — first-person ("I/My/We/Our") counted as PC, all other quoted lines counted as NPC.
  - **Name-prefixed dialog** (`Name: "..."`) — speaker name matched against `player_character_data.name` and `npc_data` keys; matched-name → PC, otherwise NPC.
  - **Indirect speech** (`<Name> said/replied/asked/...`) — classified same way.
- Counted per-scene PC and NPC line totals.
- Aggregated by `debug_info.agent_name` (the actual agent that produced the scene — not the user-intent `mode` field, which records `character`/`god`/`think` regardless of routing).

## Last 10 campaigns analyzed (sorted by latest activity)

| # | ID | Name | Entries |
|---|----|------|--------:|
| 1 | RMCPAPdf | Visenya V8 | 454 |
| 2 | 6IL5OTf3 | Bg3 Nocturna good | 372 |
| 3 | FsiyESY9 | swtor - tenebria | 388 |
| 4 | a1OGXHNx | Re:zero Theresa | 236 |
| 5 | MU0xmGES | Visenya v7 | 1408 |
| 6 | xK3fp5Xr | Visenya v7 (forgot queen dead) | 1306 |
| 7 | CokxQn4Z | Bran the broken | 342 |
| 8 | V8KORvEi | Bran the broken (ignore directive) | 248 |
| 9 | AR5iVC4j | Bg3 shy (brother still here) | 62 |
| 10 | dUfl4Adb | Iseki v1 | 112 |

## Per-agent dialog statistics (gemini scenes only, 2,464 total)

| Agent | Scenes | % of total | Median PC lines | Median NPC lines | % PC-silent | % two-way | Median words/scene |
|-------|-------:|-----------:|--------:|---------:|-----------:|---------:|------------:|
| HeavyDialogAgent | 676 | 27.4% | 0 | 17 | 67.8% | 32.2% | 436 |
| GodModeAgent | 476 | 19.3% | 0 | 6 | 99.8% | 0.2% | 188 |
| StoryModeAgent | 344 | 14.0% | 0 | 15.5 | 79.7% | 20.3% | 374 |
| DialogAgent | 286 | 11.6% | 0 | 20 | 75.5% | 24.5% | 432 |
| LevelUpAgent | 206 | 8.4% | 0 | 4 | 97.6% | 2.4% | 204 |
| PlanningAgent | 164 | 6.7% | 0 | 2 | 100.0% | 0.0% | 50 |
| CharacterCreationAgent | 96 | 3.9% | 0 | 4 | 96.9% | 3.1% | 306 |
| FactionManagementAgent | 90 | 3.7% | 0 | 20 | 75.6% | 24.4% | 401 |
| CombatAgent | 55 | 2.2% | 0 | 9 | 80.0% | 20.0% | 345 |
| RewardsAgent | 48 | 1.9% | 0 | 16 | 70.8% | 29.2% | 417 |
| InfoAgent | 14 | 0.6% | 0 | 13.5 | 85.7% | 14.3% | 320 |
| SpicyModeAgent | 5 | 0.2% | 0 | 12 | 60.0% | 40.0% | 276 |

**Key observations:**
- HeavyDialogAgent is the largest single contributor (676 scenes = 27% of all AI scenes), and despite its mandate to "improve output quality" for high-stakes conversations, it produces **67.8% PC-silent** scenes with **only 32.2% two-way dialog**.
- DialogAgent itself (286 scenes) is **75.5% PC-silent** with **24.5% two-way dialog**.
- Even StoryModeAgent (344 scenes, the narrative default) is 79.7% PC-silent.
- **Top PC-line count in any single scene across all 2,464 scenes: 8 PC lines, surrounded by 50 NPC lines** — this was the most PC-talkative HeavyDialog scene found. The "best case" is still 6.25x more NPC speech than PC speech.
- 96.4% of scenes have ≥1 NPC line (NPCs are not the problem). The problem is exclusively that the PC is missing from the conversation.

## Sample HeavyDialog scene (verbatim, `CokxQn4Z` / `x6M0Q8B4T31EMH2dYdcL`)

The strongest PC-voice HeavyDialog scene in the dataset (8 PC lines, 50 NPC lines, 852 words):

> Lord Robett Glover's voice echoes off the glass dome. He points a gauntleted hand toward the south. "Tyrosh was a tragedy, yes, but those technologists knew the risks of crossing the sea. We have built a paradise in the ice, Lord Stark. Why throw our sons into the fire of an Essosi crusade?"
>
> Lord Manderly rises, his many chins trembling with indignation. "And what happens when the 'Grand Coalition' finishes with the Dragon Queen, Robett? Do you think the Iron Bank will stop at the Narrow Sea? They fear our steel and our heat. If we do not break them at the Stepstones, they will find a way to freeze us out of our own world!"
>
> **You listen to the debate** [second-person narrator, no PC speech], your 'Permanent Foresight' showing you the jagged lines of their dissent. **You attempt to weave a middle path** [no PC speech].
>
> Sansa Stark, sitting as Co-Consul, watches the lords with a cold, political eye. "They are afraid, Bran," she says later, as the hall clears. "Half are afraid of the East, and the other half are afraid of *you*. My perspective? We cannot help Daenerys. Not yet. The North is still a fragile miracle."
>
> Arya, leaning against a pillar in the shadows, her hand never far from the hilt of a Valyrian blade, shakes her head. "I've seen the East. They don't understand 'Peace.' They only understand when the thing they fear is dead."
>
> [later, after the third NPC monologue]
>
> "There is something else," **you say**, your voice carrying a resonance that makes the frost on the windows shiver.
>
> "I can bring him back," **you continue**, your eyes soft with a rare, human empathy.

Notice the pattern:
1. NPC monologue → NPC monologue → NPC monologue (multiple).
2. ONE short PC quoted line.
3. NPC monologue continues.

The PC never gets a turn in the conversation; the LLM is producing NPC dialogue *around* the PC rather than *with* the PC.

## Root cause: prompt bias

### 1. `narrative_system_instruction.md` lines 66-68

```markdown
**NARRATIVE AUTHORITY:**
- Players describe their CHARACTER'S actions and intentions
- The GM/AI describes the WORLD'S response, NPC reactions, and outcomes
```

### 2. `narrative_lite_system_instruction.md` lines 70-73

```markdown
## 🎲 NARRATIVE AUTHORITY

- Players describe their CHARACTER'S actions and intentions
- The GM/AI describes the WORLD'S response, NPC reactions, and outcomes
- When players declare outcomes, use Action Resolution Protocol
```

### 3. `dialog_system_instruction.md` (entire file, 451 lines)

- Section 1: "Character Voice Consistency" — entirely about NPCs ("Each NPC's voice is built from...")
- Section 2: "Dialog Flow Principles" — "Structure each NPC response: React, Respond, Redirect" (no "PC response" entry)
- Section 4: "NPC Relationship Dynamics" — uses `npc.attitude_to_party`
- Section 5: "Conversation Types" — Information Gathering, Negotiation, Conflict — all from NPC perspective
- Section 7: "Output Format" — lists "Setting, NPC Reaction, Quoted Dialog, Nonverbal Details" — the "Quoted Dialog" is implicitly NPC; the file never specifies whose voice the LLM should put inside quotes
- Section 8: "NPC Data Reference" — only NPC fields
- Section 9: "Anti-Patterns to Avoid" — does NOT list "PC silent" or "NPC monologue dominance"
- **Search results: zero matches** for "player character speaks", "speak as the PC", "PC voice", "on behalf of the player", "your character says", or any equivalent

### 4. HeavyDialogAgent's `REQUIRED_PROMPT_ORDER` (`agents.py` lines 2686-2697)

```python
REQUIRED_PROMPT_ORDER: tuple[str,