---
name: prompt-fixes-must-be-generic-not-class-specific
description: "When fixing a prompt content issue surfaced by a test, fix the GENERIC rule (LLM looks up the specific facts from source of truth / input state), not a hardcoded class-specific list. Per ZFC, the LLM owns the choice/benefit selection; the prompt should give it the rule + a reference, not enumerate specific cases."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 65fcb9f7-3fca-4299-aafa-89506240a1a1
---

When a real-LLM test fails on prompt content quality (e.g. recommended loadout missing an item, wrong spell list, incomplete feature list), the **fix is the generic rule**, not a hardcoded enumeration of the specific items that the test flagged.

**Anti-pattern (what I did wrong, 2026-06-12, PR #7467):**
Codex leveling review flagged: "story seq 42's first Level 3 modal package recommends Oath of Devotion but does not correctly account for additive Devotion oath spells. It lists a 5-spell prepared loadout with `Command` and omits `Sanctuary`."

I authored commit `7610402bc3` to enumerate the L1+L2 oath-granted always-prepared spells for all three Paladin oaths (Devotion: Sanctuary/Protection from Evil and Good/Lesser Restoration/Zone of Truth; Ancients: Ensnaring Strike/Speak with Animals/Moonbeam/Misty Step; Vengeance: Bane/Hunter's Mark/Hold Person/Misty Step).

User pushed back: **"i see something concerning about fix oath devotion prompt, it shouldnt be overly specific to paladin"**.

**Why this is wrong:**
- ZFC says the LLM owns the choice/benefit selection. The prompt should give the LLM the **rule** + a **reference to the source of truth**, not a hardcoded list.
- A hardcoded list drifts from actual D&D 5e rules (which change with errata and edition updates). A reference like "consult the player's chosen subclass in `player_character_data.subclass` or the SRD reference" lets the LLM pick the right list per class.
- The same defect class repeats for every class with subclass-granted features (Cleric domain spells, Warlock patron spells, Druid circle spells, Sorcerer origin spells, etc.). Enumerating per-class spells is unmaintainable. A generic rule covers all of them.
- The user's directive "needs to be geenric" applies because the underlying defect is not "the LLM didn't know Sanctuary was a Devotion spell" — it's "the LLM wasn't told to enumerate all subclass-granted features when recommending a loadout." The first framing is over-fit; the second is a real prompt contract.

**Correct shape (what the prompt should say):**
> "When recommending a subclass's prepared-spell/feature loadout, include ALL subclass-granted always-known/always-prepared features, not just core class features. The specific spells and features granted by each subclass are defined in the SRD / the player's chosen subclass; surface them by name in the `Recommended package:` narrative paragraph. Omitting granted features from the recommended loadout is a HARD INVARIANT violation."

That one rule covers Paladin oaths, Cleric domains, Warlock patrons, Druid circles, Sorcerer origins, Artificer specialists, Ranger archetypes, and every future subclass. The LLM applies the rule using its own D&D knowledge or whatever the input state provides.

**Reusable pattern:**
1. Test fails on content quality → ask: "Is this a **rule the LLM should learn** or a **list of facts**?"
2. If a **rule**: write the rule. Don't enumerate.
3. If a **list of facts**: tell the LLM where to look (input state field, SRD reference, etc.), not what to memorize.
4. If a rule and a list are both needed (rare), put the rule in the prompt and the list in a token-efficient lookup table that the LLM consults on demand.
5. Always ask: "Does this generalize to other classes/scenarios, or is it over-fit to one?"

**Verification:**
- User's exact words: "it shouldnt be overly specific to paladin" / "needs to be generic"
- 7610402bc3 needs to be reverted or amended to a generic rule before push
- Bead: `rev-pr7467-prompt-rework` (to be created in `.beads/issues.jsonl` for the rework task)

**Related:**
- `feedback_2026-06-12_live_pr_head_staleness.md` (the related PR-head tracking lesson from the same review)
- `~/.claude/skills/root-cause-first/SKILL.md` (fix prompt/schema/agent instructions first; backend correction is a last resort)
- `~/.claude/skills/zero-framework-cognition/SKILL.md` (LLM owns choice/benefit selection)
