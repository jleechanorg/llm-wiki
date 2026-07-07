---
name: swarm-orchestration-learnings-2026-07-07
description: Six durable /swarm-orchestration lessons from the design-retro-2026-06 mission (PR
metadata: 
  node_type: memory
  type: feedback
  bead: rev-ewnuu
  originSessionId: 1774e7dc-113d-4c02-a943-e957779170b6
---

Six lessons from running the design-retro-2026-06 swarm mission (session e3cce9b6, PR https://github.com/jleechanorg/worldarchitect.ai/pull/8191, 2026-07-06/07), all folded into `~/.claude/skills/swarm/SKILL.md` (hardlinked to `~/.claude-wa/skills/swarm/SKILL.md` — same inode, one edit updates both) as rules 3/4/5/7/9/11 plus a new "Bead runbook" subsection and a sidekick-durability-limitation note.

**1. False-empty completion pattern — a workflow returning 0 confirmed findings after mass agent death is a VOID, not a verdict.**
Why: hit twice in one session. `pr-retro-gapfill` (wf_fab477ef-899): Collect phase succeeded (4 miners → 5 real candidate findings), but ALL 15 Verify-phase agents (3 lenses × 5 findings) died to provider 429s — every `rejected[].why` read `DEAD_VERIFIER: agent errored/died, not a real refutation`. `code-quality` (wf_98073447-fe5): same shape, 60/60 verify agents died, 20 real Collect-phase findings falsely zeroed. Both looked identical to a clean "nothing here" result unless you read the `failures[]` array.
How to apply: before accepting/reporting/shipping a 0-finding workflow result, check whether `failures[]` is dominated by `Server is temporarily limiting requests` or every rejection reason is a dead-verifier placeholder. If so, treat the run as VOID — re-run the affected stage, don't record the empty result as ground truth. See [[sidekick-multi-mission-state-namespacing]].

**2. Rate-limit concurrency is aggregate across sibling swarms, not per-workflow.**
Why: two individually-reasonable workflows (pr-retro-gapfill ~20 agents, code-quality resume ~60 agents) both died to 429 in the same window once their COMBINED in-flight count hit ~75. Neither alone would have looked risky.
How to apply: don't launch a new multi-agent fan-out while another large workflow is mid-fan-out — serialize big stages across sibling swarms. On mass 429: cool down ~20min, then use a tiny **sibling-workflow-as-canary** (a throwaway 1-agent workflow used purely as a health probe) before resuming/relaunching the real fan-out(s). Keep any other concurrently-running lane to ≤4 sub-agents during cooldown.

**3. Multi-sidekick STATE.md namespacing — never rewrite another live sidekick's section.**
Why: a retro-mission sidekick (this session) initially overwrote a concurrently-running CI/fleet sidekick's live `## Next Actions` heading by reusing the same generic section name in the shared `/tmp/<repo>/sidekick/STATE.md`. Caught by a team-lead amendment mid-session; required a manual revert.
How to apply: if STATE.md already has a Mission/Ground-truth/Next-Actions section owned by a different live sidekick, treat it as read-only. Append your own mission in a clearly separated `## <mission> (session <id>, owner: sidekick — <scope>)` block at the bottom instead.

**4. Sidekick durability gap — the current sidekick is a Claude Code teammate, which dies with the parent CLI process.**
Why: "crash-recoverable" sidekick only survives *conversation* crashes/restarts, not a full host/process death (parent CLI exit kills the teammate too). True crash-durability (surviving reboots, terminal closes, CLI quits) needs the supervisor to run as an Agent Orchestrator (AO) worker — a long-lived process spawned via `ao spawn`, independent of any CLI session tree.
How to apply: until the AO-worker upgrade ships (tracked as a separate build task in the `dark-factory` repo), treat STATE.md + a tracking `br` bead as the actual durable state — not the teammate process itself. See the "Bead runbook" pattern below.

**5. Bead runbook — cross-session recovery beyond /tmp.**
Why: `/tmp/<repo>/sidekick/STATE.md` does not survive a host reboot or `/tmp` cleanup, and Workflow-tool `resumeFromRunId` journals are same-session only. Real example: bead `rev-ewnuu` ("Design-retro 2026-06 swarm completion...") contains session id, script scratchpad paths, live workflow runIds, output-dir/doc-numbering state, and close-out steps — enough for a completely fresh session with no `/tmp` file to `br search` its way back to full context.
How to apply: at mission start, create/update one P1 `br` bead as the durable, host-independent recovery pointer; update it at the same cadence as STATE.md.

**6. Publishability gate — adversarial verification attacks candidate findings, never the rendered docs that actually ship.**
Why: a cold review of the 2026-07-06 design-retro docset (~180 agents, 5 workflows, 7/10+ "confirmed" findings) found 6 real defect classes that survived the entire chain: leaked credential/workstation paths, a stale 89%-vs-14–36% metric contradiction never propagated upstream, a ZFC-leveling-forbidden recommendation, 3 contradicting route-count claims across sibling docs, a false-green acceptance recipe, and — root cause of all five — no final whole-docset gate. Full writeup: `docs/design-retro-2026-06-adversarial-gaps.md` (commit `0f7628b26f`), beads `rev-pem65`/`rev-fihi7`/`rev-d6jfa`/`rev-2ipmt`/`rev-ccl4m`/`rev-qj6qb`.
How to apply: run one final single-agent gate over the ENTIRE docset after all writer lanes, before calling the PR done — redaction sweep, cross-doc numeric consistency, freshness re-baseline vs current head SHA, supersession markers, a policy lens (ZFC/credential-discipline/regex-approval) the evidence/severity/design lenses never covered, recipe-validity check, and `git diff --check`.

**Related**: [[commit-per-doc-writer-plus-commit-phase]] (two-layer commit discipline: per-doc-writer commit + final sweeping Commit-phase agent) is the same session's rule-7 update — smaller/more mechanical than the above six, folded into the same SKILL.md edit but not written up as its own memory entry.
