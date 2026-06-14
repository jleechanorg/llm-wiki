---
name: feedback-2026-06-13-ao-status-partial-output-missed-live-workers
description: "When `ao session ls` shows \"no active sessions\" for a project, ALWAYS cross-check with `tmux list-sessions` and `ao status` before reporting. Partial output filtering can hide live workers."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

**Mistake (2026-06-13, 13:23Z):** Reported "0 active AO workers" to the user after `ao session ls` was piped through `head` and the worldarchitect.ai project header scrolled past my grep filter. I never ran `tmux list-sessions` or full `ao status` to cross-check. The truth was: **wa-2325 had been WORKING for 11 minutes** (branch `fix-smoke-comment-only-restore`, driving PR #7534 to green) and `wa-orchestrator` was a zombie I had not yet reaped. I told the user there was nothing to babysit, and they had to push back ("did some AO workers die? /history") before I noticed.

Hermes (already dispatched) called me out in the Slack thread: "This contradicts Jeffrey's claim that there are no [active sessions]."

**Rule:** When a state-gathering command's output is multi-section, full, or paginated, **never** rely on a single pipe-filter. The minimum verification triple for "any AO workers alive?" is:
1. `ao status` (full output, no `head`/`grep` truncation)
2. `tmux list-sessions` (live panes exist independently of AO state DB)
3. `ls -lat ~/.agent-orchestrator/*/sessions/archive/ | head` (recent archive = recent deaths)

If all three agree, report. If any disagrees, **the most-recent signal wins** — `tmux list-sessions` is ground truth because a live tmux pane means something is running whether or not AO state DB has been updated.

**Why `tmux list-sessions` is the source of truth:** AO state DB updates lag the tmux pane by minutes (wa-orchestrator was "2h ago" while the tmux pane was still there). A pane that exists is alive until proven dead by capture-pane showing no activity + zombie indicators (empty prompt, no tool calls in 5+ min). A missing pane is dead.

**How to apply:**
- Never run `ao session ls | head -N` or `| grep -v "no active"` as the basis for "no workers." Use full output.
- When claiming "0 active," the next line in the reply must show: `tmux list-sessions` output + the ao state as a cross-check.
- When `tmux list-sessions` shows panes that `ao session ls` doesn't list, those are either in-flight (recent spawn) or zombies (stale state) — verify with `tmux capture-pane -t <name> -p -S -20` before declaring either way.
- Zombies (live tmux pane, no AO heartbeat, empty/old prompt) → `ao cleanup <name>` to reap.
- The `953501c04ccc-` prefix in pane names is the container ID; `ao-` and `wa-` are worker prefixes; `mt-` is merge-train; `bc-` is build-coordinator.

**See also:** [[feedback-2026-06-13-claw-always-show-attach-urls]] (post-dispatch output must include attach + dashboard), [[feedback-2026-06-13-claw-pre-dispatch-pr-open-check]] (verify before claiming, same root cause class).
