---
name: merge-train-conflict-hook-scope
description: "merge_train conflict-warn-pre-tool.sh fires only on Edit/Write (not Read/Bash) and outputs to stderr; users watching the chat transcript see \"allow\" with no banner, which reads as \"hook not firing\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4de5b569-b51b-4a12-9a41-45eee5ee760f
---

In `/Users/jleechan/projects/merge_train`, the `~/.local/bin/conflict-warn-pre-tool.sh` PreToolUse hook IS registered and DOES fire — but it only runs for `Edit`/`Write`/`replace_file_content` tool names. For Read and Bash it short-circuits to `{"permissionDecision":"allow"}` with no logging.

When the check runs on Edit/Write it prints two stderr lines:
- `merge_train: checking conflicts for '<rel_path>' (branch '<branch>')...`
- `merge_train: checked '<rel_path>' — no conflicts found (no other open PRs).` (or conflict block)

The chat UI does not surface these stderr lines as banner messages — only the JSON `permissionDecision` is shown. So users who "don't see hooks firing" are likely either (a) working primarily in Read/Bash which never trigger this hook, or (b) editing files that have no open-PR conflict, so the hook emits a silent allow.

**Why:** User asked "is merge train really working i dont see hooks firing" — investigation showed the hook is wired, registered in `~/.claude/settings.json` (matcher Edit+Write), and emitting correctly. The visibility gap is chat UI, not the hook.

**How to apply:** When debugging "merge train not firing," do not just trust the chat transcript. Run the hook manually:
```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"<abs_path>","new_string":"x"}}' \
  | bash ~/.local/bin/conflict-warn-pre-tool.sh
```
Stderr lines + JSON output confirm the hook ran. To see a real block, edit a file touched by another open PR.
