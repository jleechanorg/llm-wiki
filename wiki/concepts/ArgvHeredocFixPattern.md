---
title: "Argv + Heredoc Fix Pattern"
type: concept
tags: [security, shell-quoting, python, ruby, node, perl, eval]
date: 2026-06-23
---

# Argv + Heredoc Fix Pattern

The canonical fix for shell-quoting injection when calling an external
interpreter with user-controlled values.

## Anti-pattern (DO NOT use)

```bash
python3 -c "import json, sys; sys.exit(0 if '$project' in ...)"
ruby  -e "puts ENV['$TOKEN']"
node  -e "console.log('$MSG')"
perl  -e "print '$DATA'"
eval  "$USER_INPUT"
```

User-controlled value in the source string is injection-prone.

## Fix (use this)

```bash
python3 - "$project" "$running_json" <<'PYEOF' 2>/dev/null
import json, sys
cfg = json.load(open(sys.argv[2]))
sys.exit(0 if sys.argv[1] in cfg.get("projects", []) else 1)
PYEOF
```

Three safety properties:
1. `python3 - "$VAR"` passes `$VAR` as `sys.argv[1]` — never interpolated
2. `<<'PYEOF'` (single-quoted heredoc tag) prevents bash from expanding `$` in the body
3. `try/except` around `open()` handles missing/corrupt files gracefully

## When to apply
- `python3 -c` / `ruby -e` / `node -e` / `perl -e` with `$VAR` from yaml config, env, CLI args, file content
- `eval` of user input
- `source <(echo "$VAR")` patterns

## Source
PR #718 ([5ebd4cc2](https://github.com/jleechanorg/agent-orchestrator/commit/5ebd4cc2))

## See also
- [[PR717SkepticVerdict]] — the verdict that triggered this fix
