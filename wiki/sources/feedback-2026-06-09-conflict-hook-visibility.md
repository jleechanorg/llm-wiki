---
title: "merge_train conflict hook visibility (2026-06-09)"
type: source
tags: [feedback, merge-train, hooks, pre-tool, visibility, settings.json]
date: 2026-06-09
source_file: raw/feedback_2026-06-09_conflict_hook_visibility.md
---

## Summary
`~/.local/bin/conflict-warn-pre-tool.sh` in `~/projects/merge_train` is wired and firing — but it is registered as a `matcher` for `Edit`/`Write`/`replace_file_content` only, so `Read`/`Bash` never trigger it (silent `{"permissionDecision":"allow"}`). Even on Edit/Write, the only thing the chat UI surfaces is the JSON decision; the two stderr banner lines (`merge_train: checking conflicts for ...`) are not rendered as visible banners. Users who "don't see hooks firing" are usually working in Read/Bash or editing a file with no open-PR conflict — both produce silent allows.

## Key Claims
- PreToolUse hooks gated on `matcher` only fire for matching tool names. The hook's `matcher` in `~/.claude/settings.json` is `Edit|Write|replace_file_content`.
- For non-matching tools, the hook body still runs and returns `{"permissionDecision":"allow"}` — there is no log line, so the user cannot tell from chat that anything happened.
- Even on Edit/Write, the chat UI only shows the `permissionDecision`, not the hook's stderr banners. So an "allow" with no banner is NOT evidence of "hook not firing."
- Operational check: pipe a synthetic Edit event to the hook and look for the stderr lines + JSON:
  ```bash
  echo '{"tool_name":"Edit","tool_input":{"file_path":"<abs_path>","new_string":"x"}}' \
    | bash ~/.local/bin/conflict-warn-pre-tool.sh
  ```

## Key Quotes
> The chat UI does not surface these stderr lines as banner messages — only the JSON `permissionDecision` is shown. So users who "don't see hooks firing" are likely either (a) working primarily in Read/Bash which never trigger this hook, or (b) editing files that have no open-PR conflict, so the hook emits a silent allow.

## Connections
- [[GreenGateWorkflow]] — another example of a gate that runs in the background with no visible banner
- [[HookVisibility]] — general principle: silent allows ≠ hook absent; verify by manual invocation
- [[merge-train]] — repo that owns the conflict-warn-pre-tool.sh
- [[PreToolUseHooks]] — matchers gate firing; Read/Bash short-circuit to silent allow
