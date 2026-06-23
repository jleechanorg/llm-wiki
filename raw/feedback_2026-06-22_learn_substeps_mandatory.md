---
name: feedback-2026-06-22-learn-substeps-mandatory
description: "/learn's wiki-ingest + roadmap-log + bead-creation sub-steps are MANDATORY every time, not gate-blocking optional skips. User correction 2026-06-22: 'do this always dont skip'."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 79a12801-6187-4144-846a-f1b1d003e14d
  bead: rev-i1spe
---

When running the `/learn` skill (or executing the protocol manually), do NOT skip any of the five required persistence targets. The protocol's language ("report the exact blocker and continue with the remaining targets", "wiki ingest is mandatory", "A closed or referenced bead in `.beads/issues.jsonl` when the current repo has beads") is **not** a "best-effort" tier — every target is a first-class deliverable.

**Why:** User correction 2026-06-22: "do this always dont skip Skipped the wiki-ingest + roadmap-log + bead-creation sub-steps of /learn's protocol". My justification at the time was "those target other persistence targets (~/llm_wiki, ~/roadmap/learnings-2026-06.md, .beads/issues.jsonl) that aren't reachable from this worktree without a cross-write, and the project CLAUDE.md doesn't enforce them as gate-blocking." The user rejected that framing: cross-write to those paths IS the work. The /learn protocol is the contract.

**How to apply:**
- For every `/learn` invocation, always produce **all five** persistence targets:
  1. `~/.claude/projects/<project_key>/memory/<type>_YYYY-MM-DD_<slug>.md` + `MEMORY.md` index entry
  2. `~/roadmap/learnings-YYYY-MM.md` log entry
  3. A bead in `.beads/issues.jsonl` (or `none` if beads truly unavailable + report why)
  4. LLM wiki ingest via the `wiki-ingest` skill (mandatory, never direct write)
  5. mem0 save when available (optional; report missing dep if not)
- The `cd` to the worktree boundary is **not** a reason to skip — those paths live in `$HOME` and the worktree writes to its own git tree; the persistence targets are *outside* the worktree by design.
- The only legitimate "skip" is when the target is **actually unreachable** (e.g., no `br` CLI installed, no write access to `~/llm_wiki`). When that happens, **report the exact blocker** and continue with the remaining targets — do NOT skip silently.
- "Project CLAUDE.md doesn't enforce them as gate-blocking" is a wrong argument. /learn is a skill contract, not a CI gate.

**Verification:**
- Before reporting `/learn` complete, run through the 5-step checklist and confirm each target was attempted (or report the precise blocker).
- The checklist is also in `~/.claude/skills/learn/SKILL.md` "Required outputs" — re-read before claiming done.

**Reference:** correction issued in the session that drove PR #7815 (Mobile Auth Same-Origin Regression test timeout fix) to merge.
