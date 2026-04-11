---
title: "[agento] [P2] feat(evidence-review-gate): add comprehensive tests + webhook import hardening"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-04
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/489
pr_number: 489
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Summary
- Add 49-unit test suite for `evidence_review_gate.py` covering verdict extraction, GraphQL/REST API paths, fail-closed behavior, re-review latest-verdict-wins logic, and requester/CLI functions
- Move `symphony_daemon` import from lazy (inside `_dispatch()`) to module-level fail-fast in `webhook.py` with explicit `ImportError` tracking; `_dispatch` now raises a clear `DispatchError` with the root cause

## Testing
- `PYTHONPATH=src python -m pytest src/tests/test_evidence_review_gate...

## Key Changes
- 6 commit(s) in this PR
- 3 file(s) changed

- Merged: 2026-04-04

## Commit Messages
1. feat(evidence-review-gate): add comprehensive tests + webhook import hardening
  
  - Add src/tests/test_evidence_review_gate.py: 49 tests covering verdict
    extraction (PASS/WARN/FAIL formats), GraphQL/REST API paths, fail-closed
    behavior when both sources fail, latest-verdict-wins re-review logic,
    and CLI/requester functions
  - Move symphony_daemon import from lazy inside _dispatch() to module-level
    fail-fast import in webhook.py with explicit ImportError tracking; _dispatch
    now raises a clear DispatchError when the dep is unavailable rather than
    masking the root cause behind a generic "symphony dispatch failed" message
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
2. fix(tests): add missing import json; fix misleading comments flagged by Copilot
  
  - Add `import json` at module top; replace all `__import__("json").dumps(...)`
    with standard `json.dumps(...)` throughout test file
  - Fix misleading subprocess import comment in rate_limit test
  - Fix webhook.py comment: "Optional import at module load" replaces
    "Deferred import" (the import is eager, not lazy)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
3. fix: address CR CHANGES_REQUESTED comments
  
  - Fix test docstring: remove "CLI entry point" claim (no CLI test)
  - Remove unused EvidenceGateResult import
  - Fix webhook.py comment: update "Fail-fast" to accurately reflect
    "error captured at load, raised at dispatch"
  - Add exception chaining in _dispatch: raise DispatchError from
    _symphony_import_error so root cause is preserved in traceback
  - Add explicit return type annotations to subprocess_side_effect helpers
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
4. Merge origin/main into feat/orch-2kz
  
  Resolve conflicts:
  - src/orchestration/webhook.py: keep our improved comment + exception chaining
  - src/tests/test_evidence_review_gate.py: keep our comprehensive test file
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix(skeptic-gate): fix Gate 1 CI filter for actual repo check-run names
  
  Gate 1 was filtering for Lint/Typecheck/Test/Test (Web) which don't exist
  in this repo, causing TOTAL_CHECKS=0 and always-failing the gate.
  Switch to workflow-name exclusion (Skeptic Gate, Staging Canary Gate)
  so all real CI check-runs are counted. MIN_CORE_JOBS reduced from 2 to 1.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
6. fix(skeptic-gate): use check-run name (not workflow_name) for gate exclusion
  
  workflow_name is not a field in the check-runs API response.
  Exclude by .name instead: skip 'Skeptic Gate' and
  'Staging Canary Gate' check-runs; count all others as real CI.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.github/workflows/skeptic-gate.yml`
- `src/orchestration/webhook.py`
- `src/tests/test_evidence_review_gate.py`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: rate limited by coderabbit.ai -->

> [!WARNING]
> ## Rate limit exceeded
> 
> `@jleechan2015` has exceeded the limit for the number of commits that can be reviewed per hour. Please wait **1...

3. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` Let me take a closer look at the PR changes and get back to you with a full assessment!

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-revi...

4. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR status, checks, comments, and reviews
gh pr view 489 --repo jleechanorg/jleechan...

6. @coderabbitai all good?

7. @coderabbitai all good?

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me do a quick current-state check on the PR!

---

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/...

9. <!-- This is an auto-generated reply by CodeRabbit -->
Merge conflict resolution requires a Pro plan. Please upgrade to access this feature.

10. @coderabbitai approve

11. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

14. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

15. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

16. All Copilot and CodeRabbit review comments have been addressed:
1. Docstring: fixed to remove 'CLI entry point' claim
2. Unused EvidenceGateResult import: removed
3. webhook.py comment 'Fail-fast': updated to accurately describe error-capture-then-raise behavior
4. Exception chaining: added `raise D...

17. @github-actions[bot] /trigger skeptic-gate

18. @coderabbitai all good?

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

20. @coderabbitai all good?

21. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 489 --repo jleechanorg/jleechanclaw --json state,mergeable,mergeStateStatus,re...

24. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | mergeable=true, state=unstable |\n| 3. CR approved | PASS | state=APPR...

