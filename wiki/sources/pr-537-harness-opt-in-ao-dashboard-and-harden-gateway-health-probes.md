---
title: "harness: opt-in AO dashboard and harden gateway health probes"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-10
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/537
pr_number: 537
pr_repo: jleechanorg/jleechanclaw
---

## Summary
### Background
Deploy and monitor runs were intermittently failing on prod heartbeat checks while the gateway process was otherwise reachable. At the same time, AO dashboard launchd wiring remained default-on, which kept re-enabling dashboard behavior even when the operator wanted HTTP-first validation only.

### Goals
1. Stop auto-enabling dashboard behavior unless explicitly requested.
2. Reduce false/indefinite monitor hangs by bounding direct HTTP health probe timings.
3. Lower gateway event...

## Key Changes
- 6 commit(s) in this PR
- 8 file(s) changed

- Merged: 2026-04-10

## Commit Messages
1. harness: disable dashboard auto-open and bound health probes
2. fix: call launchctl enable after dashboard opt-in install
  
  When dashboard is initially disabled, launchctl disable persists a disabled flag.
  On subsequent opt-in install, install_plist bootstraps the service but the persistent
  disable flag prevents it from running. Add launchctl enable call after successful
  bootstrap to clear the flag, matching pattern used in deploy.sh and
  install-openclaw-scheduled-jobs.sh.
3. fix(launchd): enable dashboard before bootstrap
4. fix: resolve merge conflict markers, dashboard opt-in persistence, and LEARNINGS.html
  
  - Remove unresolved git merge conflict markers from workspace/MEMORY.md
  - Add state-file-based persistence for AO dashboard opt-in so it survives
    across installer runs without requiring OPENCLAW_INSTALL_AO_DASHBOARD env
    var to be set each time (fixes CodeRabbit CHANGES_REQUESTED)
  - Add paired docs/context/LEARNINGS.html update for 2026-04-08 entry
    (fixes CodeRabbit CHANGES_REQUESTED)
  - Add regression test for state-file persistence pattern
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
5. fix(install-launchagents): address 4 Bugbot findings in dashboard opt-in logic
  
  1. Unbound variable: add `:-0` default to OPENCLAW_INSTALL_AO_DASHBOARD
     so script does not crash under `set -u` when env var is unset.
  2. Tilde expansion: use `${HOME}` instead of `~` inside double-quoted
     parameter default so path resolves correctly.
  3. Explicit opt-out: handle `=0` to remove state file and enforce
     disabled state, preventing silent re-enable from stale state file.
  4. Persistent disable: `launchctl enable` is now called unconditionally
     before `install_plist` in the opt-in path so a previously-disabled
     service transitions to enabled on re-install.
  
  BugBot IDs: c555f2a6, 5b9e8978, ref1_d0ef7a8e, 0dd9da82
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
6. fix(install-launchagents): correct unset/env-var handling for dashboard opt-in state file
  
  Fixes the dashboard opt-in state file persistence logic:
  - Change ${OPENCLAW_INSTALL_AO_DASHBOARD:-0} to ${OPENCLAW_INSTALL_AO_DASHBOARD:-}
    for the "0" branch so unset env var falls through to state-file read
    instead of incorrectly treating unset as explicit opt-out (which deleted
    the state file on every re-run, breaking durable opt-in).
  - Update test assertion to use ${HOME} instead of ~ (tilde does not expand
    inside double quotes, which was a latent bug also flagged by cursor[bot]).

## Files Changed
- `docs/context/LEARNINGS.html`
- `docs/context/LEARNINGS.md`
- `launchd/ai.openclaw.gateway.plist`
- `launchd/ai.openclaw.staging.plist`
- `monitor-agent.sh`
- `scripts/install-launchagents.sh`
- `tests/test_openclaw_configs.py`
- `workspace/MEMORY.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **2...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #537: harness: opt-in AO dashboard and harden gateway health probes — claims to make dashboard install opt-in, bound health probe timing, reduce gateway event-loop pressur...

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check current review state on the PR
gh pr view 537 --repo jleechanorg/jleechanclaw --json reviews,state,body | jq '{state: .state, reviews: .reviews}'

# Check ...

4. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

5. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR state, mergeable status, and CI checks
gh pr view 537 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,statusCheckRollup,reviews | ...

6. @coderabbitai all good?

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR.

---

🏁 Script executed:
```
#!/bin/bash
# Get fresh PR state
gh pr view 537 --rep...

8. @coderabbitai all good?

Pushed `487eff55763882fcfd7a4c5d793336f90e7064f9`, which moves `launchctl enable` before `install_plist` for the AO dashboard opt-in path and adds a regression test covering that ordering.

9. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get fresh PR state, CI checks, reviews, and mergeable status
gh pr view 537 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,statusCheckRo...

10. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

11. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at latest commit
gh pr view 537 --repo jleechanorg/jleechanclaw --json s...

12. @coderabbitai all good?

13. @coderabbitai all good?

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state
gh pr view 537 --repo jleechanorg/jleechanclaw --json state,mergeable,me...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state
gh pr view 537 --repo jleechanorg/jleechanclaw --json state,mergeable,me...

16. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #537: harness: opt-in AO dashboard and harden gateway health probes — claims to make the AO dashboard opt-in, bound health probe timeouts, lower gateway event-loop pressur...

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state, CI, reviews
gh pr view 537 --repo jleechanorg/jleechanclaw --json state...

18. @coderabbitai all good?

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state, CI, reviews
gh pr view 537 --repo jleechanorg/jleechanclaw --json state...

20. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at fbfbf501
gh pr view 537 --repo jleechanorg/jleechanclaw --json state,...

22. @coderabbitai all good?

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at latest commit
gh pr view 537 --repo jleechanorg/jleechanclaw --json s...

24. @coderabbitai all good?

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at latest commit
gh pr view 537 --repo jleechanorg/jleechanclaw --json s...

26. @coderabbitai all good?

27. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at latest commit
gh pr view 537 --repo jleechanorg/jleechanclaw --json s...

28. @coderabbitai all good?

29. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Fresh PR state at latest commit
gh pr view 537 --repo jleechanorg/jleechanclaw --json s...

30. **VERDICT: PASS** — skeptic-cron evaluated and merged this PR. All 6 criteria confirmed green.  \n\n<!-- HEAD-SHA: 44ed18719e8c5465ff725a5cccf69b4c0727d7bd -->

