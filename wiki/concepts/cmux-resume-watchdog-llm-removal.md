---
title: "CmuxResumeWatchdogLlmRemoval"
type: concept
tags: [claude-code, watchdog, daemon, fastembed, token-burn]
last_updated: 2026-08-14
---

# cmux-resume-watchdog LLM Removal

The `com.jleechan.cmux-resume-watchdog` LaunchAgent was the dominant token source in the user's 2026-08 token burn: **94.8 MB / 6,505 JSONL files in 7 days** (vs ~150 MB total across all other Claude Code sessions combined).

## What it did

The watchdog scans every cmux terminal surface every 600 seconds (`--daemon --interval 600`). For each surface, it classifies the screen as QUOTA / NETWORK / CLEAR. If the fastembed anchor-phrase classifier is uncertain (semantic score 0.45–0.65), it called `classify_with_llm()` which spawned a `codex` (gpt-5.3-codex-spark) or `claude -p` subprocess with a 12-second timeout.

## Fix applied 2026-08-14

`~/.claude/skills/cmux-resume-watchdog/scripts/cmux_resume_watchdog.py:526`:

```python
# LLM fallback removed 2026-08-14 per token-burn investigation
llm_predict = None  # was: llm_predict = None if dry_run else classify_with_llm
```

`classify_with_llm()` function retained as dead code for easy revert. Ambiguous surfaces now default to "clear" (no auto-resume) — fastembed with anchor phrases at threshold 0.65 is sufficient for QUOTA/NETWORK/CLEAR classification.

## Expected impact

- Per-tick LLM subprocess calls: removed
- 6,505 JSONL files/week → near zero for the watchdog bucket
- Side effect: ambiguous surfaces are left alone rather than auto-resumed. If a session is genuinely stuck on quota but the fastembed classifier doesn't score it high enough, it won't be auto-resumed. Manual intervention (or future improvement to fastembed anchors) is the workaround.

## Detection pattern for future investigations

When asked "what used my tokens?", always check LaunchAgents before assuming user sessions are the cause:

```bash
ls ~/Library/LaunchAgents/ | grep -i claude
# Or hermes-owned:
ls ~/Library/LaunchAgents/ | grep -i hermes
```

Each LaunchAgent script should be inspected for LLM subprocess calls (`subprocess.run` with `codex` / `claude` / `agy` in the command list).

## Related

- [[feedback-2026-08-12-token-burn-investigation-learnings]]
- [[WorkAttributionPattern]] — JSONL → worktree → PR → commits mapping