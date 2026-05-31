# Automatic Merge Bypass in AO Reactions

**Source**: Claude memory — `feedback_2026-05-31_ao_reactions_auto_merge_bypass.md`
**Date**: 2026-05-31
**Project**: agent-orchestrator
**PR**: https://github.com/jleechanorg/agent-orchestrator/pull/648

## Summary

When a Pull Request (PR) is approved and all 7-green criteria pass, the system responds dynamically based on configured `reactions`. In some cases, operators expect the PR to automatically merge. However, PRs like #648 can remain open in an `approved-and-green` state indefinitely.

## Technical Detail

In `packages/core/src/lifecycle-manager.ts`, the background daemon implements automatic merging under certain reaction configurations.
Specifically:
1. The daemon triggers an automatic merge override **only if** the reaction to `approved-and-green` is explicitly set to the default value of `"notify"`.
2. If `~/.hermes/agent-orchestrator.yaml` (or equivalent configuration files) overrides the `approved-and-green` event to a custom action like `"send-to-agent"`, the daemon-side auto-merge bypasses the override logic.
3. When `"send-to-agent"` is triggered, the worker agent is spawned to handle the event.
4. However, the worker agent's standard `agentRules` strictly forbid direct GitHub API merges (e.g., `NEVER run gh pr merge. The orchestrator merges.`).
5. This creates a perpetual lock: the daemon delegates the PR resolution to the agent (via `send-to-agent`), but the agent refuses to merge because of its system rules.

## The Fix / Policy

To resolve or avoid this automatic merge deadlock:
- **Explicit Auto-Merge Config**: If automatic merging is desired without agent intervention, set the reaction action to `"auto-merge"` in the configuration:
  ```yaml
  reactions:
    approved-and-green:
      action: auto-merge
  ```
- **Operator Authorization**: Do NOT execute `gh pr merge` or merge any PR unprompted, even if it is 7-green, unless explicitly authorized by the user via typing `MERGE APPROVED` in the chat.

## Related Concepts

- [[AgentOrchestratorReactions]]
- [[ApprovedAndGreenReaction]]
- [[AgentRulesMergeLock]]
- [[ZeroTouchAutomation]]
