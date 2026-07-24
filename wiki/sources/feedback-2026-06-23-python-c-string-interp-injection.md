---
title: "`python3 -c \"...$VAR...\"` is shell-quoting injection (2026-06-23)"
type: source
tags: [security, shell-quoting, injection, python]
date: 2026-06-23
source_file: feedback_2026-06-23_python_c_string_interp_injection.md
---

## Summary
`python3 -c "import json, sys; sys.exit(0 if '$project' in ...)"` interpolates user-controlled values into python SOURCE. A single quote in the value breaks the script and can allow command injection. Fix: pass the value as `sys.argv[1]` via `python3 - "$VAR" <<'PYEOF'` (single-quoted heredoc tag prevents bash expansion). Same anti-pattern applies to `ruby -e`, `node -e`, `perl -e`, `eval`.

## Key Claims
- Never interpolate user-controlled values into the source of an external interpreter
- Single-quoted heredoc tag (`<<'PYEOF'`) is the safety boundary — bash does not expand `$` inside the body
- The Skeptic pattern-recognition gate (Gate 7 security) flags this without requiring a working exploit

## Key Quotes
> "A project name containing a single quote (or any other python-meaningful token) **breaks the script and can allow command injection** — bash sees the closing `'` of `'$project'` and the python invocation becomes syntactically valid but semantically attacker-controlled."

## Connections
- [[PR718BashTestSuite]] — same PR fixes the pattern in start-all.sh
- [[ArgvHeredocFixPattern]] — general fix pattern (to be created)
