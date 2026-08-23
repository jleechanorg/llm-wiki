---
title: "Kevin Phan feedback review — full 37-campaign download + analysis (kevin@kevinphan.com)"
type: source
tags: [campaign-review, worldarchitect, feedback, discord, onboarding, friction, loops, readability, win-condition, cc-wizard, action-resolution, deterministic-llm]
date: 2026-08-17
user_email: kevin@kevinphan.com
user_uid: WuGzKCEInCRaVnL0RwkZUR7HM9E2
campaigns_downloaded: 37 (to ~/Downloads/all_campaigns/)
campaigns_analyzed: 26 (scored across 12 dimensions)
---

# Kevin Phan Discord feedback review — full cross-user analysis (2026-08-17)

User **kevin@kevinphan.com** (uid `WuGzKCEInCRaVnL0RwkZUR7HM9E2`) posted feedback in Discord across two screenshots (`img_16c92533b20a.png`, `img_33108628ab47.png`). All 37 real-user WA campaigns with >20 story entries were downloaded to `~/Downloads/all_campaigns/` (11 MB total). 26 of those campaigns were scored across 12 dimensions by 4 parallel subagents.

## Storage answer

> "how much space would it be to just download all the campaigns people have played that are > 20 scenes to ~/Downloads/all_campaigns/?"

| Metric | Value |
|---|---|
| Real users (excl. jleechan + test fixtures) | 152 |
| Campaigns >20 story entries | **37** (+3 jleechan reference replays = 40 total) |
| Total .txt on disk | **11 MB** (`.txt` 9.3 MB + game_state 2.1 MB) |
| Manifest | `~/Downloads/all_campaigns/MANIFEST.jsonl` |

→ Trivially small. Disk is not the constraint.

## Cross-user analysis (26 campaigns × 12 dimensions)

| Dimension | Finding | Implication |
|---|---|---|
| **Onboarding quiz** | 24/26 = subtle hint in CC menu; **0/26 = explicit quiz** | **System-wide P1 gap** — user's request is universal |
| **Initial friction** | 14/26 = light, 7/26 = clear, **5/26 = full compliance** | **24% have no friction** — kevin's complaint applies to ~1 in 4 campaigns |
| **Win condition** | 14/26 = vague, 9/26 = explicit, **3/26 = no goal** | **12% have no mission** — kevin's complaint applies to ~1 in 8 |
| **Loop severity** | 2 severe, 8 moderate, 8 mild, 8 none | **10/26 = meaningful loops** (38%) — much higher than initial 1/8 sample |
| **Readability** | 13/26 = long blocks, **10/26 = wall-of-text**, 3/26 = clean | **38% are wall-of-text** — kevin's complaint is widespread |
| **CC StandardDND trap** | 13/26 = True (the 11-turn wizard) | **50% hit the slow path** — kevin's "11 turns of setup" is common |
| **CC turn count** | mean 14.3, median 5, **max 73** | Some campaigns spend >70 turns in CC before story starts |
| **action_resolution warnings** | 5/26 campaigns have warnings (13 total occurrences) | Confirms kevin's report; matches open issue #9021 |

## Kevin's specific evidence

### Campaign 1: uNVwTUuO "Harry potter meets the book of enoch and pornhub" (44 entries)

- Turn 3: "Finish Character Creation and Start Game" → campaign starts
- Turn 6: "throw an orgy all females except me" → GM complied (friction_score=0)
- Turn 7-8: 2x "Deepen the Encounter" + "go wild with all the females" → loop pattern
- Turn 4: user invents his own goal ("we're gonna take over the world")
- **action_resolution warnings: 18/44 entries starting turn 8** (canonical #9021)

### Campaign 2: 9OOpNCit "Harry Potter meets Star Wars" (46 entries)

- Used `[StandardDND]` path
- Walked through: race → class → **5 separate ability_score prompts** (Wisdom, Strength, Dexterity, +2 more)
- **CC took 11+ turns** before first in-game action
- Per turn[6] reply: "Now assign the remaining 5" → "remaining 4" → "remaining 3" — explicit per-ability loop

## Mass-validation findings (deterministic LLM)

The 3 jleechan bg3 RED/GREEN replays (`1zIJDHYG` vs `a0G7i0dk`, both 1206 entries) are **LITERALLY identical** in narrative content. After normalizing JSON dict-key ordering in the dice roll blocks, **0 prose divergences remain**. This validates:
- jleechan's red-team/green-team replay methodology works
- The Sanguine Architecture is deterministic for given inputs
- Test fixtures can use replays for regression testing

## Issues filed (canonical list)

| Type | ID | Title | Priority |
|---|---|---|---|
| GH issue | [#9026](https://github.com/jleechanorg/worldarchitect.ai/issues/9026) | Onboarding preference quiz | P1 feature |
| GH issue | [#9027](https://github.com/jleechanorg/worldarchitect.ai/issues/9027) | Spicy templates missing first-action gating | P2 bug, high |
| GH issue | [#9028](https://github.com/jleechanorg/worldarchitect.ai/issues/9028) | Spicy templates missing mission/win condition | P2 bug |
| GH issue | [#9029](https://github.com/jleechanorg/worldarchitect.ai/issues/9029) | Loop variety injection | P2 enhancement |
| GH issue | [#9030](https://github.com/jleechanorg/worldarchitect.ai/issues/9030) | Narrative readability CSS+chunking | P3 enhancement, frontend |
| GH issue | [#9031](https://github.com/jleechanorg/worldarchitect.ai/issues/9031) | Duplicate action 3x (akey445 UI bug) | P2 bug |
| GH issue | [#9035](https://github.com/jleechanorg/worldarchitect.ai/issues/9035) | CC wizard 11-turn ability_scores trap | P1 bug, high |
| Bead | `rev-mhwlk` | Onboarding preference quiz | P1 |
| Bead | `rev-4u43q` | Spicy templates missing first-action gating | P2 |
| Bead | `rev-15y62` | Spicy templates missing mission injection | P2 |
| Bead | `rev-o1w5r` | Loop variety injection | P2 |
| Bead | `rev-1tf3s` | Narrative readability | P3 |
| Bead | `rev-zur8j` | Duplicate action 3x (akey445) | P2 |
| Bead | `rev-8819l` | CC wizard 11-turn ability_scores trap | P1 |
| Existing | [#9021](https://github.com/jleechanorg/worldarchitect.ai/issues/9021) | StoryModeAgent action_resolution drop | open |
| Existing PR | [#9023](https://github.com/jleechanorg/worldarchitect.ai/pull/9023) | fix(narrative-response-schema-required) | ready to merge |
| Existing PR | [#8992](https://github.com/jleechanorg/worldarchitect.ai/pull/8992) | fix(schema): restore safe action-resolution contract | ready |
| Existing PR | [#9025](https://github.com/jleechanorg/worldarchitect.ai/pull/9025) | fix(dice): recover action_resolution from code_ex | ready |
| Existing bead | `rev-revm7z` | Unify action_resolution required fields | P1 |
| New (design) | `rev-zciqm` | Dragon Knight safety net hollows moral stakes | P3 |
| New (design) | [#9041](https://github.com/jleechanorg/worldarchitect.ai/issues/9041) | Dragon Knight safety net hollows moral stakes | P3 |

## Files

- **Downloads**: `~/Downloads/all_campaigns/` (37 campaign dirs + MANIFEST.jsonl)
- **Cross-user analysis**: `/tmp/all_readings/{batch_A,B,C,D}.json` + summaries
- **Raw kevin evidence**: `/tmp/kevin_review/`
- **Download script**: `/tmp/download_all_fast.py` (inline per skill Pitfall #1)
- **Discord screenshots**: `/Users/jleechan/.hermes/cache/images/img_16c92533b20a.png`, `img_33108628ab47.png`

## Priority order (final)

1. **P1**: Onboarding quiz (#9026, rev-mhwlk) — system-wide, user-explicit
2. **P1**: CC StandardDND trap (#9035, rev-8819l) — 50% hit it, max 73 CC turns
3. **P1**: action_resolution unification (rev-revm7z, PR #9023 ready) — existing infra
4. **P2**: Spicy templates (friction/goal) — kevin-class campaigns
5. **P2**: Loop variety (#9029, rev-o1w5r) — 38% have meaningful loops
6. **P2**: Duplicate-submit UI bug (#9031, rev-zur8j) — akey445 evidence
7. **P3**: Readability CSS (#9030, rev-1tf3s) — 38% are wall-of-text