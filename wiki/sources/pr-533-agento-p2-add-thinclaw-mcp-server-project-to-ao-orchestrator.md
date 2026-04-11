---
title: "[agento] [P2] add thinclaw MCP server project to AO orchestrator"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-07
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/533
pr_number: 533
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
Adds `jleechanorg/thinclaw` as a new AO-managed project in `agent-orchestrator.yaml`.

## thinclaw repo (https://github.com/jleechanorg/thinclaw)

**Stack:** Node.js (ES modules), `@modelcontextprotocol/sdk` (StdioServerTransport), `axios`, `zod`

**Design:** Zero LLM inference — thinclaw is a pure HTTP REST bridge. Claude Cowork/Perplexity provides all reasoning.

**Architecture:**
```
Claude Cowork/Perplexity (brain)
  → thinclaw MCP stdio (bridge, zero inference)
    → OpenClaw Gat...

## Key Changes
- 2 commit(s) in this PR
- 1 file(s) changed

- Merged: 2026-04-07

## Commit Messages
1. [agento] add thinclaw project to AO orchestrator
2. [agento] thinclaw: replace hardcoded localhost:18789 with $OPENCLAW_GATEWAY_ADDR, add isolated gateway testing note

## Files Changed
- `agent-orchestrator.yaml`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
No actionable comments were generated in the recent review. 🎉

<details>
<summary>ℹ️ Recent review info</summary>

<details>
<summary>⚙️ Run configuration</summary>

**Configuration used**: Path: .coderabbit.yaml

**Review profil...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check what files were changed in the PR
git diff HEAD~1 --name-only

# Show the diff of...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
Error loading config.toml: env is not supported for streamable_http
in `mcp_servers.perplexity-ask`

. C...

5. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR details including CI status, merge status, and comments
gh pr view 533 --repo jl...

7. @coderabbitai all good?

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get latest PR status
gh pr view 533 --repo jleechanorg/jleechanclaw --json state,mergea...

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status
gh pr view 533 --repo jleechanorg/jleechanclaw --json state,merge...

11. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

12. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
Error loading config.toml: env is not supported for streamable_http
in `mcp_servers.perplexity-ask`

. C...

13. ## Evidence Review: PASS ✅

**Reviewer:** evidence-reviewer subagent (independent)
**Codebase:** thinclaw main @ `47003bc`

### Verdict: PASS

All primary claims substantiated by direct artifacts.

| Claim | Artifact | Quality |
|---|---|---|
| All 5 tools route to `/tools/invoke` (live endpoint) | ...

