# PR #2: fix(doctor): quote tilde in expand_home case pattern

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-16
**Author:** jleechan2015
**Stats:** +51/-49 in 2 files

## Summary
(none)

## Raw Body
## Problem

`expand_home()` in `scripts/ao-doctor.sh` used an unquoted `~/*)` case pattern:

```bash
case "$1" in
  ~/*)   # ← bash expands this to /Users/jleechan/* at parse time
```

Bash performs tilde expansion on `case` patterns before matching. The pattern `~/*` becomes `/Users/jleechan/*` at parse time, but the input `~/.agent-orchestrator` is a **literal tilde string** — so the pattern never matches and paths are silently returned unexpanded.

**Symptom:** `ao-doctor` reports `WARN metadata directory is missing at ~/.agent-orchestrator` even when the directory exists at the expanded path.

## Fix

Quote the pattern as `"~/"*)` — quoted strings in `case` are not tilde-expanded:

```bash
case "$1" in
  "~/"*)   # ← literal ~ matches literal ~ in input ✓
    printf '%s/%s' "$DEFAULT_CONFIG_HOME" "${1#\~/}"
```

## Red/Green Proof

A self-contained test is included at `tests/unit/test-doctor-expand-home.sh`:

```
=== RED: broken version (demonstrates the bug) ===
  FAIL  tilde path silently not expanded
        got:      ~/.agent-orchestrator
        expected: /Users/jleechan/.agent-orchestrator
  PASS  absolute path passthrough

=== GREEN: fixed version ===
  PASS  tilde path expands correctly
  PASS  nested tilde path expands correctly
  PASS  absolute path passthrough
  PASS  relative path passthrough
```

Run it yourself:
```bash
bash tests/unit/test-doctor-expand-home.sh
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk: small Bash script change to argument parsing/entrypoint plus a unit test update; behavior changes are localized to `ao-doctor.sh` execution vs sourcing and home-path expansion.
> 
> **Overview**
> Fixes `scripts/ao-doctor.sh` so it can be safely `source`d for tests by moving `set -uo pipefail`/CLI arg parsing into the direct-invocation path and adding a guard that returns early when sourced.
> 
> Updates `tests/unit/test-doctor-expand-home.sh` to source the 
