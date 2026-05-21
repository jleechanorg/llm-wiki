---
name: Windows Footgun False Positive Suppression
description: check-windows-footguns.py is a naive grep; suppress with `# windows-footgun: ok` when code is already gated by `if not _IS_WINDOWS:`
type: feedback
date: 2026-05-14
raw: raw/feedback_2026-05-14_windows-footgun-gated-suppression.md
---

## Summary

`hermes-agent` CI "Windows footguns (blocking)" uses naive text matching. Code inside `if not _IS_WINDOWS:` guards still triggers false positives for `os.killpg` and `signal.SIGKILL`.

## Rule

Add `# windows-footgun: ok` on the flagged line when the code is already inside a Windows guard:

```python
if not _IS_WINDOWS:
    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)  # windows-footgun: ok
```

One comment suppresses both `os.killpg` and `signal.SIGKILL` on the same line.

## References

- `tools/process_registry.py:588` in `jleechanorg/hermes-agent`
- PR #13: https://github.com/jleechanorg/hermes-agent/pull/13
- Commit: `c589b00f`
