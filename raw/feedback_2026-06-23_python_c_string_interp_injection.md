---
name: python-c-string-interp-injection
description: "never interpolate user-controlled values into `python3 -c \"...\"` source; use `python3 - \"$arg\" <<'PYEOF'` heredoc + argv pattern"
metadata: 
  node_type: memory
  type: feedback
  bead: bd-2oll
  originSessionId: 4920971d-1790-4e87-8227-a17d7f18ef21
---

# Shell-quoting injection in `python3 -c "..."` — fix with argv + heredoc

## Anti-pattern

```bash
# DANGEROUS: $project is interpolated unescaped into python SOURCE
if python3 -c "import json, sys; sys.exit(0 if '$project' in json.load(open('$running_json')).get('projects', []) else 1)" 2>/dev/null; then
```

A project name containing a single quote (or any other python-meaningful token)
**breaks the script and can allow command injection** — bash sees the closing
`'` of `'$project'` and the python invocation becomes syntactically valid but
semantically attacker-controlled.

## Fix

```bash
if python3 - "$project" "$running_json" <<'PYEOF' 2>/dev/null; then
import json, sys
try:
    cfg = json.load(open(sys.argv[2]))
except (OSError, ValueError):
    sys.exit(1)
sys.exit(0 if sys.argv[1] in (cfg.get("projects") or []) else 1)
PYEOF
```

Three safety properties:
1. `python3 - "$arg" ...` passes `$arg` as `sys.argv[1]` — never interpolated
2. `<<'PYEOF'` (single-quoted heredoc tag) prevents bash from expanding `$` in the
   python body, so the python source is exactly what you see
3. `try/except` around `open()` avoids crashing on a corrupt/missing file

## When this pattern triggers a Skeptic finding

The Skeptic scans PR diffs for unescaped `$var` inside backtick / `"..."` / `python3 -c`
invocations. A flag lands as Gate 7 (security). It does not require a working exploit —
just the pattern recognition that the variable is user-controlled (yaml config, env,
CLI flag) and the interpreter isn't.

## Verification (PR #718)

- RED: reverted `start-all.sh` to the vulnerable form; test Section 6 failed
  both assertions (`$project` still interpolated; no argv pattern)
- GREEN: 33/33 checks pass with the heredoc fix
- Test file: `scripts/test-ao-health.sh` Section 6 (2 checks)
  - `start-all.sh does not interpolate $project into python`
  - `start-all.sh uses python3 - "$project" argv pattern`

## Apply when

- `python3 -c "...$VAR..."` with `$VAR` from yaml config, env, CLI args, file content
- Same pattern applies to `ruby -e`, `node -e`, `perl -e`, `bash -c` with user-controlled `$VAR`
- Same pattern applies to `eval` and `source <(echo "$VAR")`

## Files

- `scripts/start-all.sh:130` — original vulnerable line in `is_lifecycle_worker_running()`
- `scripts/start-all.sh:130` (post-fix) — heredoc replacement

## References

- PR [#718](https://github.com/jleechanorg/agent-orchestrator/pull/718) — fix landed
- Skeptic verdict on PR #717: Gate 7 FAIL on shell-quoting injection in
  `start-all.sh` `is_lifecycle_worker_running()`
- `feedback_2026-06-23_testable_bash_extracted_helpers.md` — test harness context
