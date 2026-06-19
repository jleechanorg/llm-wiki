---
title: "PR body wipe by Python env var error + Green Gate evidence anchor rules"
type: source
tags: [green-gate, ci, pr-workflow, bash, python]
date: 2026-06-19
source_file: raw/feedback_2026-06-19_pr_body_wipe_and_gate6_anchor.md
---

## Summary

When using `NEW_BODY=$(python3 -c "..." VAR="$VALUE")` in bash, the Python subprocess does NOT receive the variable — `os.environ['VAR']` raises `KeyError`, the script errors, and stdout is empty. Running `gh pr edit --body ""` wipes the entire PR body. Additionally, Green Gate Gate-6 requires a gist/media URL; Gate-6b requires triple-backtick fenced code blocks, not single-backtick inline code.

## Key Claims

- `python3 -c "..." VAR="$VALUE"` does NOT export `VAR` into the subprocess's environment; use `export VAR` first
- `gh pr edit --body ""` (empty string) silently wipes the entire PR body with no undo
- Gate-6 HAS_EVIDENCE check requires: `gist.github.com/`, `asciinema.org/a/`, `loom.com/share/`, `user-attachments.githubusercontent.com/`, or URLs ending in `.mp4/.gif/.cast`
- Gate-6b anchor check requires `FENCED_CODE_RE = re.compile(r"```[\s\S]+?```")` — triple backticks only
- Recovery from body wipe: reconstruct from `git diff origin/main..HEAD`, Gate-6b section density counts in failed run logs, and session context

## Key Quotes

> "Never use `python3 -c '...' VAR='$VALUE'` to pass env vars; always `export VAR` first or use a temp file."

## Connections

- [[GreenGateEvidence]] — Gate-6 URL pattern and Gate-6b anchor requirements
- [[PRBodyRecovery]] — reconstruct from git diff + gate run logs
- [[BashPythonEnvVarScope]] — variable assignment in command position does NOT export to subprocess

## PR Reference

- PR [#7588](https://github.com/jleechanorg/worldarchitect.ai/pull/7588) — `refactor(dice-audit): use GOOGLE_APPLICATION_CREDENTIALS_JSON env var for Firebase SA key`
- Green Gate run 27519652330 (PASS at 2026-06-15T02:01:36Z)
- Evidence gist: https://gist.github.com/jleechan2015/b475e0d4399ebfca231b6e45e1af113c
- Bead: rev-18glq

[[jeffrey-oracle]]: NO.
