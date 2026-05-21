---
name: windows-footgun-gated-suppression
description: Windows footguns checker does naive grep; code already gated by `if not _IS_WINDOWS:` is a false positive; suppress with `# windows-footgun: ok`
type: feedback
bead: none
date: 2026-05-14
---

## Context

`hermes-agent` CI has a "Windows footguns (blocking)" check that runs:
```bash
python scripts/check-windows-footguns.py --all
```

It scans Python files for Windows-incompatible patterns like `os.killpg` and `signal.SIGKILL`.

## Problem

`tools/process_registry.py:588` triggered two footgun violations:
```
tools/process_registry.py:588: [bare os.killpg]
tools/process_registry.py:588: [bare signal.SIGKILL]
    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
```

The code is ALREADY gated:
```python
if not _IS_WINDOWS:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    ...
else:
    proc.kill()
```

The checker uses naive text matching and does not understand conditional guards.

## Solution

Add `# windows-footgun: ok` on the flagged line:
```python
os.killpg(os.getpgid(proc.pid), signal.SIGKILL)  # windows-footgun: ok
```

Both violations (`os.killpg` and `signal.SIGKILL`) are on the same line, so one suppression covers both.

## Verification

Committed to `fix/gitignore-ao-bearer-token` at `c589b00f`. CI re-run pending.

## Reusable Pattern

**Rule:** When `check-windows-footguns.py` flags code that is already inside `if not _IS_WINDOWS:`, add `# windows-footgun: ok` on the flagged line. Do NOT restructure the code.

**jeffrey-oracle**: not affected (CI tooling)
