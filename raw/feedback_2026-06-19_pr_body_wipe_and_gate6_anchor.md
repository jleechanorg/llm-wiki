---
name: PR body wipe by Python env var error + Green Gate evidence anchor rules
description: Python KeyError in bash heredoc wiped PR body; Gate-6/6b anchor rules require triple-backtick or URL, not inline code
type: feedback
bead: none
---

## PR body accidentally wiped by Python script error in bash heredoc

When running `NEW_BODY=$(echo "$BODY" | python3 -c "..." NEW_VARIABLE="$VALUE")`,
if the Python script errors (e.g. `KeyError` on `os.environ['NEW_VARIABLE']` because
the variable was not exported), the subprocess exits non-zero but stdout is empty.
`gh pr edit --body "$NEW_BODY"` then sets the PR body to the empty string, wiping it.

**FIX / Rule:** Always use one of these safe patterns instead:
- Export the env var before using it: `export NEW_VARIABLE="$VALUE"` then `python3 -c "..."`
- Write a temp file and read it: `python3 -c "..." > /tmp/new_body.md && gh pr edit --body "$(cat /tmp/new_body.md)"`
- Use heredoc with python3 reading stdin for transformation (no env var needed)

**Recovery:** GitHub API has no PR body edit history. Reconstruct from:
1. `git diff origin/main..HEAD` for code changes
2. Gate-6b JSON output (section density counts in failed run logs)
3. Session context / prior successful gate run logs

## Green Gate evidence anchor requirements

**Gate-6b `## Evidence` and evidence sections** require either:
- A fenced triple-backtick code block: ` ``` ... ``` ` (matched by `FENCED_CODE_RE = re.compile(r"```[\s\S]+?```")`)
- OR an `https?://` URL

**Single-backtick inline code `` `gcloud logging read ...` `` does NOT satisfy the anchor requirement.**

**Gate-6 specifically** requires one of these patterns in the PR body or comments:
- `gist.github.com/` URL
- URL ending in `.mp4`, `.gif`, `.webm`, `.cast`
- `asciinema.org/a/` URL
- `loom.com/share/` URL
- `user-attachments.githubusercontent.com/` URL

A Cloud Run log gcloud command in inline code does NOT satisfy Gate-6.

**Fix:** Use `gh gist create <logfile>` to create a gist, then embed the gist URL
in the `## Evidence` section alongside a triple-backtick block with sample output.

## Gate passes once fixed

PR #7588 `refactor(dice-audit): use GOOGLE_APPLICATION_CREDENTIALS_JSON env var for Firebase SA key`
- Branch: `dev1781484835`
- SHA: `664fe05d00b15a02021877cbe794c1f61a67498f`
- Green Gate run `27519652330` PASSED at 2026-06-15T02:01:36Z after:
  1. Adding gist URL to `## Evidence` and `## Non-Unit Test Evidence`
  2. Converting inline code to triple-backtick fenced block in `## Evidence`
  3. Evidence gist: https://gist.github.com/jleechan2015/b475e0d4399ebfca231b6e45e1af113c

**Why:** Gate-6 regex checks for media/gist URLs; Gate-6b FENCED_CODE_RE requires triple backticks.

**How to apply:** When writing PR body evidence sections, always include a gist URL AND
a triple-backtick block with actual output. Never rely on single-backtick inline code
spans for anchors. Never pass Python script output through bash variable substitution
without first verifying the env var is exported.
