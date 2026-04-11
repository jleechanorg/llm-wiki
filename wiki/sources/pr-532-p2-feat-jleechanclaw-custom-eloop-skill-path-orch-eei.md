---
title: "[P2] feat: jleechanclaw custom eloop skill path (orch-eei)"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-07
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/532
pr_number: 532
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
AO `orchestratorRules` and operators expect the dropped-thread eloop at `~/.openclaw/skills/jleechanclaw-eloop.md`, but bootstrap never created that path. This PR wires the canonical repo file (`skills/jleechanclaw-eloop.md`) via symlink and adds a Claude Code skill entry for discovery.

## Changes
- `scripts/bootstrap.sh`: mkdir `~/.openclaw/skills` and `ln -sf` to `skills/jleechanclaw-eloop.md`; add `--eloop-skill-only` for a lightweight refresh.
- `.claude/skills/jleechanclaw-eloop...

## Key Changes
- 3 commit(s) in this PR
- 7 file(s) changed

- Merged: 2026-04-07

## Commit Messages
1. feat: bootstrap symlink for jleechanclaw-eloop skill (orch-eei)
  
  - Link ~/.openclaw/skills/jleechanclaw-eloop.md to repo skills/ via bootstrap
  - Add scripts/bootstrap.sh --eloop-skill-only for lightweight refresh
  - Add .claude/skills/jleechanclaw-eloop/SKILL.md pointer; cross-link evolve_loop
  - Document canonical paths in skills/jleechanclaw-eloop.md; clarify AO orchestratorRules
  
  Made-with: Cursor
2. fix: address Copilot review — eloop bootstrap path + SKILL wording
  
  Made-with: Cursor
3. docs: add PR-532 isolated gateway smoke evidence
  
  Made-with: Cursor

## Files Changed
- `.beads/issues.jsonl`
- `.claude/skills/evolve_loop/SKILL.md`
- `.claude/skills/jleechanclaw-eloop/SKILL.md`
- `agent-orchestrator.yaml`
- `docs/evidence/PR-532/isolated-gateway.md`
- `scripts/bootstrap.sh`
- `skills/jleechanclaw-eloop.md`

## Review Notes
1. @coderabbitai all good?

2. @coderabbitai all good?

3. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **3...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
VERDICT: FAIL — infra: Codex failed: Command failed: /opt/homebrew/bin/codex exec -
Error loading config.toml: env is not supported for streamable_http
in `mcp_servers.perplexity-ask`

. C...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check the key changed files in this PR

echo "=== scripts/bootstrap.sh (eloop-related s...

6. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check the PR diff and key files
echo "=== bootstrap.sh eloop section ==="
grep -n "eloo...

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot] — yes, all good! The PR has already been reviewed in full. Summary:

| Check | Status |
|---|---|
| `bootstrap.sh` syntax | ✅ Clean |
| `agent-orche...

9. @coderabbitai all good?

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — yes, still all good! ✅ Nothing has changed since the prior two reviews. All checks remain green:

| Check | Status |
|---|---|
| `bootstrap.sh` syntax | ...

11. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

12. @coderabbitai all good?

**Isolated gateway (skills touch):** see `docs/evidence/PR-532/isolated-gateway.md` — gateway on **:18999**, `/health` live.

**Copilot threads:** addressed in 8a94f9e041 (REPO_ROOT reuse, missing-skill warning, SKILL wording).

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, CI checks, mergeable state
echo "=== PR Status ==="
gh pr view 532 --rep...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== Check latest commit and changes ==="
git log --oneline -5

echo ""
echo "=== bo...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== Check current REPO_ROOT usage in bootstrap.sh ==="
grep -n "REPO_ROOT\|eloop-sk...

17. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

