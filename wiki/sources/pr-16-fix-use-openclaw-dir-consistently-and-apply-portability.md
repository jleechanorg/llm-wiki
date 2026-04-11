---
title: "fix: use openclaw dir consistently and apply portability"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-04-09
pr_url: https://github.com/jleechanorg/smartclaw/pull/16
pr_number: 16
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary
Apply portability fixes: replace hardcoded /Users/jleechan with $HOME

Use .openclaw directory consistently:
- openclaw-upgrade-safe.sh: BASELINE_FILE uses ~/.openclaw
- gateway-preflight.sh: baseline file consistency  
- install-openclaw-launchd.sh: baseline path consistency

Based on jleechanclaw PR #538

Supersedes #15

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Touches deployment/upgrade and launchd automation; incorrect paths/labels o...

## Key Changes
- 6 commit(s) in this PR
- 7 file(s) changed

- Merged: 2026-04-09

## Commit Messages
1. fix: apply portability and use openclaw dir consistently
2. Fix SDK version path mismatch between preflight and upgrade scripts
  
  Update gateway-preflight.sh to use ~/.openclaw/.current-sdk-version instead
  of ~/.smartclaw/.current-sdk-version to match openclaw-upgrade-safe.sh.
  
  This fixes a bug where preflight would write the SDK version to the old path,
  but the upgrade script would read from the new path, causing the SDK
  compatibility check to be silently skipped.
3. fix: add migration fallback for legacy .smartclaw SDK version path
4. Fix baseline path split: migrate gateway-preflight.sh to ~/.openclaw paths
  
  Fixes inconsistency where gateway-preflight.sh used ~/.smartclaw paths while
  mem0-native-module-watchdog.sh, install-openclaw-launchd.sh, and
  openclaw-upgrade-safe.sh all migrated to ~/.openclaw paths.
  
  Changed paths in gateway-preflight.sh:
  - MODVER_BASELINE: ~/.smartclaw/.gateway-node-version → ~/.openclaw/.gateway-node-version
  - extensions dir: ~/.smartclaw/extensions/openclaw-mem0 → ~/.openclaw/extensions/openclaw-mem0
  
  This ensures watchdog (runs every 4 hours) and preflight (runs before upgrades)
  coordinate on the same baseline file and directory paths.
5. fix: address CR comments - cd guard, mkdir for baseline, labels, staging port
6. fix: add mkdir guard and remove dead code per CodeRabbit
  
  - Add mkdir -p before writing BASELINE_FILE (line 228)
  - Remove redundant if [ ! -d BETTER_SQLITE3_DIR ] check (dead code)
  - Consistent indentation throughout rebuild block

## Files Changed
- `scripts/gateway-preflight.sh`
- `scripts/install-openclaw-launchd.sh`
- `scripts/mem0-native-module-watchdog.sh`
- `scripts/openclaw-upgrade-safe.sh`
- `scripts/stability-report.launchd.sh`
- `scripts/staging-canary.sh`
- `scripts/staging-gateway.sh`

## Review Notes
1. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```f0167d3```_
<!-- HEAD-SHA: f0167d39cd409993a06f95602c88e3f0351a89fc -->

2. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```f0167d3```_
<!-- HEAD-SHA: f0167d39cd409993a06f95602c88e3f0351a89fc -->

3. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```f0167d3```_
<!-- HEAD-SHA: f0167d39cd409993a06f95602c88e3f0351a89fc -->

4. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

5. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```f0167d3```_
<!-- HEAD-SHA: f0167d39cd409993a06f95602c88e3f0351a89fc -->

6. @coderabbitai all good?

7. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a7ee9e3```_
<!-- HEAD-SHA: a7ee9e3a67a7a9c74585d4a575fe363eab089235 -->

8. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a7ee9e3```_
<!-- HEAD-SHA: a7ee9e3a67a7a9c74585d4a575fe363eab089235 -->

9. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check for any remaining hardcoded /Users/ paths
echo "=== Remaining hardcoded /Users/ p...

10. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a7ee9e3```_
<!-- HEAD-SHA: a7ee9e3a67a7a9c74585d4a575fe363eab089235 -->

11. @coderabbitai all good?

12. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a4727c8```_
<!-- HEAD-SHA: a4727c85e2c7933e8d66510f8c6f84ef64f8e9ac -->

13. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a4727c8```_
<!-- HEAD-SHA: a4727c85e2c7933e8d66510f8c6f84ef64f8e9ac -->

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== gateway-preflight.sh MODVER_BASELINE ==="
rg -n 'MODVER_BASELINE' scripts/gatew...

15. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```a4727c8```_
<!-- HEAD-SHA: a4727c85e2c7933e8d66510f8c6f84ef64f8e9ac -->

16. @coderabbitai all good?

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the branch.

---

🏁 Script executed:
```
#!/bin/bash
echo "=== MODVER_BASELINE in gateway-...

18. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

19. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== MODVER_BASELINE in gateway-preflight.sh ==="
rg -n 'MODVER_BASELINE' scripts/ga...

20. @coderabbitai all good?

21. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```93f2213```_
<!-- HEAD-SHA: 93f2213048b3a11f47e82170d2a6e00314772f33 -->

22. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```93f2213```_
<!-- HEAD-SHA: 93f2213048b3a11f47e82170d2a6e00314772f33 -->

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== MODVER_BASELINE in gateway-preflight.sh ==="
rg -n 'MODVER_BASELINE' scripts/ga...

24. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```93f2213```_
<!-- HEAD-SHA: 93f2213048b3a11f47e82170d2a6e00314772f33 -->

25. @coderabbitai all good?

26. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```d608fd5```_
<!-- HEAD-SHA: d608fd5f3ca387dfc1788261a3e4155ec478234f -->

27. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```d608fd5```_
<!-- HEAD-SHA: d608fd5f3ca387dfc1788261a3e4155ec478234f -->

28. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== MODVER_BASELINE in gateway-preflight.sh ==="
rg -n 'MODVER_BASELINE' scripts/ga...

29. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```d608fd5```_
<!-- HEAD-SHA: d608fd5f3ca387dfc1788261a3e4155ec478234f -->

30. @coderabbitai all good?

31. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```2009134```_
<!-- HEAD-SHA: 2009134c99afdb46d754f613f30f10d1f68118c9 -->

32. ## Skeptic Gate Findings

```
VERDICT: SKIPPED - ANTHROPIC_API_KEY not configured.
Add it in repo Settings > Secrets and Variables > Actions.
```

_Skeptic gate ran on commit ```2009134```_
<!-- HEAD-SHA: 2009134c99afdb46d754f613f30f10d1f68118c9 -->

33. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== git log last 3 ==="
git log --oneline -3

echo ""
echo "=== MODVER_BASELINE in ...

34. @coderabbitai all good?

35. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== git log last 3 ==="
git log --oneline -3

echo ""
echo "=== MODVER_BASELINE in ...

36. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

37. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== git log last 3 ==="
git log --oneline -3

echo ""
echo "=== MODVER_BASELINE in ...

