---
name: Successful integrate includes mandatory learn
description: Integrate must execute its required learning workflow after success
type: feedback
bead: rev-fnfwj0
---

## Context
After a successful /integrate, the agent skipped /learn because the skill demanded separate memory authorization. The user corrected this explicitly: "run /learn and /integrate always wants learn strengthen the skill if needed".

## Mandatory rule
A request to run /integrate includes its required post-success /learn workflow. Invoke the canonical learn skill; do not invent a separate approval requirement and silently skip it. Respect an explicit no-memory instruction and higher-priority storage restrictions, and report exact blocked persistence targets. Do not claim learning captured from a chat summary alone.

## Fix and verification
FIX: replace the skip-on-missing-separate-approval clause in ~/.claude/skills/integrate/SKILL.md and its tracked export source with a mandatory post-integration learning step. Verify the installed skill matches the tracked source, keep a user_scope backup, and check actual persistence results individually.

## References and reusable pattern
User correction 2026-09-08; ~/.claude/skills/learn/SKILL.md and ~/.claude/skills/integrate/SKILL.md. Existing installation source: https://github.com/jleechanorg/jleechan-skills/pull/425 . Treat required subcommands as part of the explicitly requested workflow, subject to higher-priority restrictions; do not add a redundant approval gate.

## 2026-09-09 live workflow verification

The installed /integrate script exited 0 and created clean dev1788993718 tracking origin/main at e1c776e11d74c2679794e49deefaa8610edf4848. Earlier attempts correctly stopped for a behind-upstream branch; fast-forward-only synchronization allowed success without --force. Previous branch was preserved when merged-PR status could not be verified. The session invoked canonical /learn after success, reusing this lesson rather than fabricating a new one. Graph and prompt-substitution audits both passed. Evidence: ~/.claude/state/integrate-test-20260909/final.json and integrate-final.log. Bead rev-fnfwj0.
