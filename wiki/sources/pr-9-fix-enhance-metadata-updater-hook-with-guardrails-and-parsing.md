---
title: "fix: enhance metadata-updater hook with guardrails and parsing"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-04-03
pr_url: https://github.com/jleechanorg/smartclaw/pull/9
pr_number: 9
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary
- Add hook_event detection to distinguish PreToolUse vs PostToolUse hooks
- Strip leading cd and env variable prefixes from commands
- Add [agento] prefix guardrail on gh pr create titles
- Add gh pr merge guardrail to block agent-triggered merges by default
- Fix sed escaping bug

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds enforcement that can deny `gh pr create`/`gh pr merge` executions and changes merge-detection parsing, which cou...

## Key Changes
- 1 commit(s) in this PR
- 3 file(s) changed

- Merged: 2026-04-03

## Commit Messages
1. feat(sma-2): add merge guardrails and [agento] title enforcement to metadata hook
  
  - PreToolUse guard: require [agento] prefix on gh pr create titles
  - PreToolUse guard: block gh pr merge in all chained forms (&amp;&amp;, ;, end-of-string)
  - Merge pattern catches merge at any position: start, after separators, or trailing
  - Fix python3 parse failure: exit 1 propagates to hook deny (no silent bypass)
  - Fix sed | delimiter escaping in metadata value replacement
  - settings.json: register hook for both PreToolUse and PostToolUse
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

## Files Changed
- `.claude/metadata-updater.sh`
- `.claude/settings.json`
- `README.md`

## Review Notes
1. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->

<!-- walkthrough_start -->

<details>
<summary>📝 Walkthrough</summary>



</details>

<!-- walkthrough_end -->


<!-- pre_merge_checks_walkthrough_start -->

<details>
<summary>🚥 Pre-merge checks | ✅ 3</summary>

<details>
<summ...

2. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #9: fix: enhance metadata-updater hook with guardrails and parsing — claims to add Pre/Post hook-event handling, command prefix stripping, PR title/merge guardrails, and s...

3. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check PR `#9` status, CI checks, and reviews
gh pr view 9 --repo jleechanorg/smartclaw ...

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
# Get PR status, CI checks, reviews, and mergeable state
gh pr view 9 --repo jleechanorg/...

6. @coderabbitai all good?

7. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```846ddb6```_
<!-- HEAD-SHA: 846ddb6363baf1359f5c0368c25e61d69df92c0b -->

8. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```846ddb6```_
<!-- HEAD-SHA: 846ddb6363baf1359f5c0368c25e61d69df92c0b -->

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

10. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```846ddb6```_
<!-- HEAD-SHA: 846ddb6363baf1359f5c0368c25e61d69df92c0b -->

11. @coderabbitai review please

12. @coderabbitai all good?

13. <!-- This is an auto-generated reply by CodeRabbit -->
`@jleechan2015` Sure! Kicking off a fresh review of PR `#9` now. 🐰

<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This com...

14. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,reviews,comments | jq '{
  state,
  mergeable,
  reviews: [.reviews[] | {a...

15. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

17. @coderabbitai review please

18. @coderabbitai all good?

19. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```fe87ec1```_
<!-- HEAD-SHA: fe87ec1971deea4a35312dbbc89c7c07665624d9 -->

20. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```fe87ec1```_
<!-- HEAD-SHA: fe87ec1971deea4a35312dbbc89c7c07665624d9 -->

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

22. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

`@jleechan2015` — Kicking off a fresh review now. Let me pull the current state of the PR.






---

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state,...

23. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```fe87ec1```_
<!-- HEAD-SHA: fe87ec1971deea4a35312dbbc89c7c07665624d9 -->

24. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

26. @coderabbitai review please

27. @coderabbitai all good?

28. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```550f6dd```_
<!-- HEAD-SHA: 550f6dd09b8aa872c47718fd90e0201f530e353c -->

29. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```550f6dd```_
<!-- HEAD-SHA: 550f6dd09b8aa872c47718fd90e0201f530e353c -->

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

31. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```550f6dd```_
<!-- HEAD-SHA: 550f6dd09b8aa872c47718fd90e0201f530e353c -->

32. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

33. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

34. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

35. @coderabbitai review please

36. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a53ee5f```_
<!-- HEAD-SHA: a53ee5f365f938d9f94b557c9c07038c6ee47b5d -->

37. @coderabbitai all good?

38. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a53ee5f```_
<!-- HEAD-SHA: a53ee5f365f938d9f94b557c9c07038c6ee47b5d -->

39. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

40. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state, and latest commit
gh pr vie...

41. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

42. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

43. @coderabbitai all good?

44. @coderabbitai all good?

45. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```32cc2d2```_
<!-- HEAD-SHA: 32cc2d2cd296bf8f6f925be1fc63da689c833963 -->

46. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```32cc2d2```_
<!-- HEAD-SHA: 32cc2d2cd296bf8f6f925be1fc63da689c833963 -->

47. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

48. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

49. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

50. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

51. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #9: fix: enhance metadata-updater hook with guardrails and parsing — the PR claims to enforce `PreToolUse`/`PostToolUse` guardrails for `gh pr create`/`gh pr merge`, impro...

52. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

53. @coderabbitai all good?

54. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```9b6a353```_
<!-- HEAD-SHA: 9b6a353ea64f31cd56a00c7a443da6efa9f07501 -->

55. @coderabbitai all good?

56. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```9b6a353```_
<!-- HEAD-SHA: 9b6a353ea64f31cd56a00c7a443da6efa9f07501 -->

57. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state, and latest commit
gh pr vie...

58. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

59. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
## Background
PR #9: fix: enhance metadata-updater hook with guardrails and parsing — claims to add Pre/Post hook-event handling, `gh pr create`/`gh pr merge` guardrails, command-prefix pa...

60. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
gh pr view 9 --repo jleechanorg/smartclaw --json title,state,mergeable,statusCheckRollup,...

61. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

62. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state, and latest commit
gh pr vie...

63. @coderabbitai review

64. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

65. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```9b6a353```_
<!-- HEAD-SHA: 9b6a353ea64f31cd56a00c7a443da6efa9f07501 -->

66. @coderabbitai review

67. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

68. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

69. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

70. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state
gh pr view 9 --repo jleechan...

71. @coderabbitai all good?

72. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current PR status, CI checks, reviews, mergeable state, and latest commit
gh pr vie...

73. @coderabbitai resume

74. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Reviews resumed.

</details>

75. @coderabbitai approve

76. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

