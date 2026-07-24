---
name: mergeability-drift-coderabbit-rate-limit-cosmetic-success-2026-07-10
description: "PR verified CLEAN flipped CONFLICTING 2h later via same-author sibling PR on same CI lines; CodeRabbit conclusion=success masked \"Skipped - Review rate limited\"; swarm refuted all 5 tooling fixes"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-73mzt (related infra bead; drift incident referenced there)
  originSessionId: 8a7c0272-d1b5-4785-96ca-1724a78a9409
---

# Mergeability drift + CodeRabbit rate-limit cosmetic success

**Context** (2026-07-10, worldarchitect.ai session driving PRs #8312/#8268 to /green):

## 1. PR mergeability drift is routine, not a detection failure

PR #8268 was verified `mergeable=MERGEABLE, mergeStateStatus=CLEAN` at 10:02Z. At 12:19Z,
PR #8310 (same author, jleechan2015, different concurrent session) merged to main editing the
exact same `.github/workflows/test.yml` checkout `fetch-depth` block — both PRs were
independently fixing the same detect-changes CI-history pain point. #8268 silently flipped
`CONFLICTING`; nobody noticed until the human asked ~9h later.

**Rules (now encoded in `~/.claude/skills/pr-green-definition.md` + repo copy + CLAUDE.md/AGENTS.md/GEMINI.md/cursor/SOUL.md):**
- Re-run `gh pr view <N> --json headRefOid,mergeable,mergeStateStatus` before EVERY /green claim,
  repeat of a claim, or merge action. Report as `mergeable=X as of <SHA> @ <UTC ts>` — a snapshot, not a fact.
- ANY conflict = automatic Gate-2 FAIL; no other gate compensates.
- Merge conflicts are ROUTINE: resolve autonomously (rebase, take correct side of mechanical
  collisions, reapply own changes, push, report after). Only escalate genuinely ambiguous business logic.
- `merge_train` (~/.local/bin/conflict-warn-pre-tool.sh) is a WRITE-TIME guard — fires when this
  session writes a file; structurally cannot catch post-merge base drift. By design, not a gap.

## 2. CodeRabbit check-run `conclusion=success` can be cosmetic

The check-run API showed `conclusion: "success"` while `output.summary` read
**"Result: Skipped - Review rate limited"**. Always read the summary text, never trust the
conclusion field alone. Detection: `gh api repos/OWNER/REPO/commits/<SHA>/check-runs --paginate
--jq '.check_runs[] | select(.name=="CodeRabbit / Review") | .output.summary'`.
The rate limit was account-wide (~18h, 03:44Z→~22:07Z), cleared on its own; retry comments
(`@coderabbitai full review`) don't force it — cadence ≤1/hour, then wait.

## 3. Same-author concurrent-session collisions are invisible to standard tooling

A 9-agent swarm (research + brainstorm + codex adversarial verify) REFUTED all 5 of its own
harness-fix proposals with live repo evidence:
- TTL-on-claims: trigger never fires when no agent re-enters the loop during the drift window
- overlap-cron: 172 live open same-file PR pairs → pure alert noise
- CODEOWNERS gate: per-PR isolation can't see sibling PRs; rubber-stamp fatigue
- GitHub merge queue: repo has ZERO required status checks (`branches/main/protection` → `contexts: []`), nothing to gate on
- pr-conflict-detector bot: hard-coded same-author exclusion — both colliding PRs were jleechan2015

**Reframe**: this failure class is same-account concurrent Claude-session collision, which
multi-contributor tooling structurally cannot see. The durable fix is behavioral (autonomous
resolution + fresh verification), not tooling.

## Verification
- PR #8268 conflict resolved autonomously (merge commit c2ae5411e2, took main's #8310 side), merged 23:33:03Z (a7ed9fce56).
- PR #8312 CodeRabbit CHANGES_REQUESTED addressed autonomously (6acebbb132: comment hygiene + dict-only docstring), APPROVED at head 22:25Z, merged 23:33:48Z (b9f379a8d5).

## Reusable pattern
Status claims about live external state (mergeable, CI, reviews) expire the moment they're made.
Re-fetch before re-stating or acting; read payload bodies not just status labels; when tooling
can't see a failure class, fix the agent behavior instead.

Related: [[feedback_2026-07-10_cr_approved_requires_commit_id_equals_head]]
