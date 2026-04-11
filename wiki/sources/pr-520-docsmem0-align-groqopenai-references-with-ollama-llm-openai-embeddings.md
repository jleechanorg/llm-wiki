---
title: "docs(mem0): align Groq/OpenAI references with Ollama LLM + OpenAI embeddings"
type: source
tags: [github, pr, jleechanorg-jleechanclaw]
sources: []
date: 2026-04-06
pr_url: https://github.com/jleechanorg/jleechanclaw/pull/520
pr_number: 520
pr_repo: jleechanorg/jleechanclaw
---

## Summary
## Background
The jleechanclaw harness was previously using Groq for fact extraction in mem0 hooks, which introduced external API dependencies and costs. To improve local-first capabilities and reduce reliance on third-party providers for extraction tasks, we are transitioning to using local OSS LLMs (specifically Ollama with llama3.2:3b) as the default fact-extraction provider.

## Goals
- Transition the default mem0 fact-extraction provider from Groq to local Ollama.
- Centralize mem0 configur...

## Key Changes
- 9 commit(s) in this PR
- 14 file(s) changed

- Merged: 2026-04-06

## Commit Messages
1. feat(mem0): default OSS LLM to Ollama (replace Groq for extraction)
  
  Hooks use mem0_hooks_enabled(); Claude hooks + auto_fact_capture support ollama/groq.
  Beads: rename orch-7kf/kg to jleechan-*; fix jleechan-9nt closed_at; close jleechan-i5sf.
  Docs: roadmap rolling entry, SHARED_MEM0 + openclaw-mem0 README (full-local oss example).
  
  Made-with: Cursor
2. fix(mem0): mirror live OpenAI embedder + Ollama LLM (llama3.2:3b)
  
  Hooks must match gateway Qdrant embedding space; document openclaw_prod config path.
  
  Made-with: Cursor
3. docs(mem0): align Groq/OpenAI embedding references with Ollama LLM + OpenAI embed
  
  - Roadmaps, openclaw-mem0 README, SYSTEM_SNAPSHOT: document harness default and historical context
  - Hooks: clarify comments (OpenAI embedder + Ollama LLM)
  - auto_fact_capture: docstrings + default Ollama model llama3.2:3b; Groq path documented as legacy
  - Testing logs: add 2026-04 context notes
  
  Made-with: Cursor
4. fix(hooks/mem0_recall): re-add os import used by _THROTTLE_FILE
  
  The GROQ_API_KEY guard was replaced with mem0_hooks_enabled() in
  this PR, but _THROTTLE_FILE = os.path.join(...) still requires os.
  Without this import the hook crashes with NameError at module load time.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
5. fix(pr-520): mem0 hooks fail-open, openclaw.json embedder sync, testing_llm cleanup
  
  - Load hook embedder + Qdrant dims from OPENCLAW_CONFIG_PATH openclaw.json
  - Wrap mem0_hooks_enabled() in try/except; stderr warn and exit 0 on errors
  - auto_fact_capture + mem0_shared_client honor OPENCLAW_CONFIG_PATH
  - Align Ollama model fixtures with llama3.2:3b; remove unscoped testing_llm context lines
  
  Made-with: Cursor
6. chore: retrigger CI after resolving review threads
  
  Made-with: Cursor
7. fix(hooks/mem0_config): sync full vector_store.config and add guarded failure diagnostic
8. fix(hooks/mem0_config): resolve syntax error and duplicate content
9. chore(beads): align prefixes with main (orch-)

## Files Changed
- `.beads/issues.jsonl`
- `.claude/hooks/mem0_config.py`
- `.claude/hooks/mem0_recall.py`
- `.claude/hooks/mem0_save.py`
- `bug_reports/bug-hunt-20260326_090009.md`
- `docs/context/SYSTEM_SNAPSHOT.md`
- `extensions/openclaw-mem0/README.md`
- `roadmap/AUTO_FACT_CAPTURE.md`
- `roadmap/MEM0_INGEST_RESUME.md`
- `roadmap/README.md`
- `roadmap/SHARED_MEM0_ARCHITECTURE.md`
- `scripts/auto_fact_capture.py`
- `scripts/mem0_shared_client.py`
- `src/tests/test_ollama_embedder.py`

## Review Notes
1. @coderabbitai all good?

2. <!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: review paused by coderabbit.ai -->

> [!NOTE]
> ## Reviews paused
> 
> It looks like this branch is under active development. To avoid overwhelming you with review comments due to an influx...

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Check PR status, reviews, and CI checks
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,statusCheckRollup,comments,reviews 2...

4. <!-- skeptic-agent-verdict -->
**🤖 Skeptic Agent Verdict (bd-qw6)**

VERDICT: FAIL

--- Full skeptic output ---
Based on my analysis of the PR #520 context provided:

## Background
PR #520: docs(mem0): align Groq/OpenAI references with Ollama LLM + OpenAI embeddings — State: MERGED

## Current Probl...

5. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get current review state and inline comments
gh pr view 520 --repo jleechanorg/jleechan...

6. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

7. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

8. @coderabbitai all good?

9. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,mergeable,reviewDecision,statusCheckRollup 2>/dev/null | jq '.'

echo ""
echo "...

10. import os restored in mem0_recall.py -- the GROQ guard was replaced with mem0_hooks_enabled() but _THROTTLE_FILE = os.path.join(...) still needs it. Copilot comment about hardcoded openclaw.json is pre-existing in main, out of this PR scope.

11. ## Evidence Review Result

**Verdict: FAIL**

**Bundle: No evidence bundle found** — searched canonical paths:
- \`/tmp/worldarchitect.ai/worktree_memory/**/\`
- \`tmp/worldarchitect.ai/jleechanclaw/PR-520/\`
- \`docs/evidence/PR-520/\`
- \`docs/evidence/worktree_memory/\`

The PR changes behavioral...

12. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

13. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

14. @coderabbitai all good?

15. @coderabbitai all good?

16. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

17. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

18. @coderabbitai all good?

19. @coderabbitai all good?

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — Yes, all good! I already approved the PR in my previous response. All actionable comments were resolved at commit `028685c73c`:

- ✅ `import os` regressi...

21. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

22. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

23. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

24. @coderabbitai all good?

25. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

26. @coderabbitai all good?

27. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

28. @coderabbitai all good

29. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

31. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

32. @coderabbitai all good

33. <!-- This is an auto-generated reply by CodeRabbit -->
Merge conflict resolution requires a Pro plan. Please upgrade to access this feature.

34. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

Let me check the current state of the PR to give an accurate answer to the Skeptic.

---

🏁 Script executed:
```
#!/bin/bash...

35. @coderabbitai all good?

36. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

37. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

38. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015` — The Skeptic verdict is based on **stale data**. I've already verified and addressed this exact assessment earlier in this thread. Here is the authoritati...

39. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

40. ## Skeptic Gate — Deterministic 6-Green Check

| Gate | Result | Detail |
|------|--------|--------|
| 1. CI green | PASS | commit-status=null
error, failed-checks=0, pending-checks=0, total-checks=4 |\n| 2. No conflicts | PASS | already merged |\n| 3. CR approved | PASS | state=APPROVED |\n| 4. Bug...

41. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATE ==="
gh pr view 520 --repo jleechanorg/jleechanclaw --json state,merge...

