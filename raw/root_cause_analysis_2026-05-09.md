# Root Cause Analysis: Bug Fix PRs (#6839 - #6844)

Per the new policy, here is the Git archaeology and root cause analysis for the 5 active/recent bug fix PRs. 

---

## 1. PR #6844: `fix(god-mode): clear stale combat state trapping game in CombatAgent loop`

**The Bug:**
Campaigns using God Mode (or triggering it via console) could get permanently trapped in the `CombatAgent`. This occurred because the game state had `in_combat=True` and `combat_phase=active`, which routed every subsequent turn to the high-priority `CombatAgent` (priority 5c) instead of `StoryMode`.

**Root Cause:**
God Mode turns intentionally bypass the standard story and combat resolution logic. Because there was no specific cleanup path to clear combat flags during a God Mode override, any active combat state was left intact ("stale"), poisoning the routing logic for all future turns. 

**Original Breaking PR:**
- **PR #3020** (`fix(prompts): Require level-up planning_block on GOD MODE return to story`) and **PR #2553** (`Add combat-focused agent with system prompts`). 
- This was an architectural gap introduced when God Mode and Combat Mode were initially implemented and intersected. There was never a backend safety net to force-clear combat state when entering God Mode.

---

## 2. PR #6843: `fix: map world_data.location to current_location_name in location progress`

**The Bug:**
The player's `current_location_name` was becoming stale. The LLM was correctly outputting the new location inside the `state_updates.world_data.location` JSON field (as instructed by `game_state_instruction.md`), but the backend was ignoring it.

**Root Cause:**
In `mvp_site/preventive_guards.py`, the `_ensure_location_progress` guard relied strictly on a top-level `location_confirmed` property. If the LLM omitted `location_confirmed` or returned `"Unknown"`, the guard silently ignored `world_data.location` and fell back to the previous location, causing the frontend UI to display stale location data.

**Original Breaking PR:**
- **PR #5563** (`Schema Validation Infrastructure - Truly Squashed`). 
- This PR introduced the strict schema extraction for `location_confirmed` in the preventive guards, inadvertently severing the fallback to the legacy `world_data.location` object that the LLMs were still using.

---

## 3. PR #6842: `fix(world_logic): correct character creation modal guard for god_mode campaigns`

**The Bug:**
Players using God Mode or pre-populated character templates were getting soft-locked. The character creation modal would appear and refuse to dismiss, preventing any gameplay.

**Root Cause:**
The backend "correction guard" designed to clear the modal state contained a logically flawed dual-condition: it required BOTH `character_creation_in_progress=True` AND `character_creation_completed=True`. Because pre-populated templates start with `completed=False` (since they skip the manual creation flow), the guard never fired.

**Original Breaking PR:**
- **PR #6225** (`fix: skip character creation modal for pre-populated character templates`). 
- This PR introduced the flawed dual-condition (`cc_in_progress is True and cc_completed is True`) while attempting to fix template initialization, accidentally breaking the exit path for the modal.

---

## 4. PR #6841: `[antig] Fix campaign UI renaming regression and fantasy theme visibility`

**The Bug:**
When users tried to click the campaign title to rename it inline, the editor would prematurely dismiss itself. Additionally, select dropdowns in the "Fantasy" theme were illegible due to poor contrast.

**Root Cause:**
In `mvp_site/frontend_v1/js/inline-editor.js`, the code attempted to remove an event listener like this: 
`document.removeEventListener('click', this.handleOutsideClick.bind(this));`
Because `.bind(this)` creates a *new* function reference every time it is called, the original listener was never removed. The dangling listeners caused premature dismissal on subsequent clicks. 

**Original Breaking PR:**
- **PR #1082** (`Apply formatting fixes and migrate static to frontend_v1 from PR #1038`).
- This was the original PR that migrated the `inline-editor.js` script to the V1 frontend and introduced the flawed event binding logic.

---

## 5. PR #6839: `Canonicalize cooldown living-world strip fields`

**The Bug:**
The application crashed with a `NameError` in `mvp_site/world_logic.py` when attempting to process certain Living World events, specifically complaining about a missing `_cooldown_lw_fields` variable.

**Root Cause:**
The logic for stripping "cooldown" fields (like `world_events`, `faction_updates`, `rumors`) was heavily duplicated across `world_logic.py` and `llm_parser.py` using inline tuples. During a recent merge/rebase, one of the re-strip blocks was updated, but a variable name was misspelled/lost (`_cooldown_lw_fields_resp` vs `_cooldown_lw_fields`), causing a fatal crash on the execution path.

**Original Breaking PR:**
- **PR #6308** / **Commit `6d29d8eed`** (`feat(level-up): rewards_engine single-responsibility + llm_parser single orchestration root`). 
- This major architectural refactor fractured the Living World stripping logic across multiple files, introducing the duplicated inline lists that ultimately caused the `NameError` during subsequent merges. PR #6839 successfully fixes this by moving all logic to a single source of truth (`living_world_contract.py`).
