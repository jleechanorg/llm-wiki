---
name: worldlogic-loc-ratchet-hit-by-legit-fix-relocate-not-bump
description: "A real bug fix pushed world_logic.py over its CI LOC ratchet; the right response was relocating new logic to the owning helper module, not bumping the ratchet"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-n8roa
  originSessionId: cee0bb0d-c457-403a-b13c-ed9ae755aa1c
  modified: 2026-09-18T01:52:43.060Z
---

While landing PR #9913 (jleechanorg/worldarchitect.ai, fix for bead rev-n8roa —
wizard IP fields silently dropped on a Dragon Knight fallback), two rounds of
independent review (`/wa` ChatGPT, `/advice` Opus, then a follow-up round with
cursor-agent + Gemini + ChatGPT again) each surfaced a real, non-obvious bug
in the previous commit's fix — not false positives. Both were legitimately
fixed in-place after verifying against the actual code (grep'd the exact
call sites, confirmed the failure scenario was reachable, RED-verified before
GREEN). The final ~34-line addition to `mvp_site/world_logic.py` then tripped
CI's "Design Doc Grep Gates" whole-file LOC ratchet (`world_logic.py line
count <= 12681`), which had been correctly tightened by a prior session's
real refactor earlier in this same day.

**Why:** `world_logic.py` carries a CI-enforced upper-bound LOC ratchet
(`.github/workflows/design-doc-gate.yml`, "world_logic.py line count" gate).
A genuinely necessary bug fix can still trip it if the fix needs even a few
lines of new logic plus explanatory comments. The reflexive fix — bump the
ratchet number — is explicitly discouraged by this repo's own history (an
earlier bump from 12672→12699 by a previous session was later superseded by
a real refactor that tightened it to 12681; bumping again would silently
re-inflate a metric multiple sessions worked to shrink).

**How to apply:** When a legitimate fix in `world_logic.py` needs new logic
and pushes it over the LOC ratchet, first check whether the new logic
naturally belongs in a helper module `world_logic.py` already imports from
(here: `mvp_site/prompt_utils.py`, which already owned
`stamp_wizard_intake_answers()` — the exact function that needed the new
gating logic). Move the computation + its comments into that helper,
leaving `world_logic.py`'s call site as a thin pass-through of the already-
available local variables. This is usually a 5-minute, behavior-preserving
refactor (verified via the same test suite before/after) and gets you back
under budget without touching the ratchet number or asking for an exception.
Watch for import-cycle risk when doing this — `campaign_template_dragon_knight.py`
already imported `_build_campaign_prompt` FROM `prompt_utils.py`, so the new
helper function needed a deferred (in-function-body) import back the other
direction rather than a module-level one.

Secondary pattern from the same PR: three independently-run reviewers
(cursor-agent as `/advice`'s A3 fallback, Gemini, and ChatGPT via `/wa`) each
independently found the exact same subtle ordering bug (a match-classification
computed before vs. after a prompt-rewrite block) without being told what the
others found. When multiple independent reviewers converge on the same
specific finding unprompted, treat it as strong confirmation signal, not
coincidence — worth fixing immediately rather than requesting a fourth opinion.
