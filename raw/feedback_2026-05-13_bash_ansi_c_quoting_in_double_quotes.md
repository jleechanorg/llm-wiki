---
name: bash-ansi-c-quoting-in-double-quotes
description: $'\n' inside double quotes is literal text, not a newline — use += outside quotes
type: feedback
bead: rev-bmo6q
---

`$'\n'` ANSI-C escape sequences only expand at the top level of bash assignment.
Inside `"..."` double quotes, `$'\n'` is treated as literal characters `$`, `'`, `\n`, `'`.

**Why:** PR #6913 had `BRANCH_MESSAGE="$BRANCH_MESSAGE$'\n\n'Please review..."` — the
message contained the literal string `$'\n\n'` instead of two newlines. CodeRabbit flagged
this in review comment #3235666318. Fix commit: `5d3c8c412`.

**How to apply:** Use `+=` with ANSI-C quoting outside the double-quoted context:

```bash
# WRONG — $'\n\n' is literal inside "..."
MSG="$MSG$'\n\n'suffix"

# CORRECT — ANSI-C quoting at top level
MSG+=$'\n\nsuffix'
# or with variable interpolation:
MSG+=$'\n'"$VAR"
```

**References:**
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6913
- Fix commit: `5d3c8c412`
- CR comment: `#3235666318`
