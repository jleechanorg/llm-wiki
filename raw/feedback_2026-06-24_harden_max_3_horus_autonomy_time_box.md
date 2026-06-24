---
name: harden-max-3-hour-autonomy-time-box-across-all-long-running-flows-2026-06-24
description: "/babysit has --max-min 180; /converge, /eloop, /goal_harness, /auton, /f, /goal had no shared cap. New rule: any autonomy flow MUST stop after 10,800 s and require `CONTINUE N HORUS` to extend. Helper: ~/.claude/scripts/check_autonomy_time_box.sh."
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 119226a9-d30b-4b43-93af-9857792505eb
---

**Context (2026-06-24):** You asked "5 horus is way too long wtf is going on?" (`~/.claude/history.jsonl:1780704230249`, dd43a7a4 session) and "run /auton on AO workers last 12 horus and read actual tmux convos" (history.jsonl:1781373147260). Goal: **harden max 3 horus** = enforce a 3-hour wall-clock cap on every autonomous flow with an explicit re-approval gate.

**Asymmetry discovered:** `/babysit --max-min 180` already enforces the cap for one-shot watches (default 90, hard ceiling 180 without approval — `~/.claude/skills/babysit/SKILL.md:240`). But `/converge`, `/eloop`, `/goal_harness`, `/auton`, `/f` dark-factory, and repeated `/goal` invocations had **no shared cap** — they could run indefinitely until token budget or cron failure killed them.

**FIX (apply now, durably):**

1. **Policy** added to `~/.claude/CLAUDE.md` "Autonomy time-box — max 3 hours without explicit re-approval" — single canonical rule, references the helper + bypass phrase.
2. **Helper** `~/.claude/scripts/check_autonomy_time_box.sh` — sources of truth: (a) `~/.hermes/runtime/<flow>-<id>.started_at` markers, (b) tmux `ao-*` worker creation epochs. Returns rc=1 with `CONTINUE <N> HORUS` re-approval instruction if any entry > 10,800 s. Honors `.approved_until` companion file (epoch) for explicit extensions.
3. **Bypass phrase (literal):** `CONTINUE <N> HORUS` or `EXTEND TO <N> HORUS` typed in the **most recent user message** lifts the cap to N hours × 3600 s. Paraphrases like "keep going" / "ship it" are NOT authorization.

**Verification (2026-06-24):** 4 scenario tests on the helper: empty (rc=0), 4-hour-old marker (rc=1, blocks), approved extension (rc=0, OK-extended), post-cleanup (rc=0). All pass.

**Why this matches the harness-fix-durability rule:** Severity = **silent degradation** (multi-hour runs masking stuck loops + burning token/Slack budget). Right fix layer = **CLAUDE.md rule + script check**, not a PreToolUse hook (too heavy, blocks every iteration) and not just a memory entry (no enforcement). Sibling to `/babysit --max-min` (which already enforced this for one-shot watches) and `ao-spawn-safety` 20-worker cap (which caps worker COUNT, not wall-clock).

**Reusable pattern:** Any time-box policy must have: (1) canonical rule in one place, (2) a script helper with rc=1 on violation, (3) a literal bypass phrase that's a non-paraphraseable token (not "go ahead" / "yes"), (4) a sibling file (`.approved_until`) so extensions are visible + reversible.
