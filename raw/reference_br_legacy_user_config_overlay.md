---
name: reference-br-legacy-user-config-overlay
description: "br v0.2.16 silently overlays /Users/jleechan/.beads/config.yaml as a legacy user config into every workspace's br invocation; explains unexpected jleechan- prefix in sandboxes and home no-auto-flush true. /learn 2026-07-09."
metadata: 
  node_type: memory
  type: reference
  bead: jleechan-zlaw
  originSessionId: b77c4d5b-01af-466a-b5a9-38d7534a1d3b
---

## `br` v0.2.16 — legacy user-config overlay quirk

`br` reads `~/.beads/config.yaml` as a **legacy user-config overlay** for *any* cwd.
For users whose real workspace lives at `~/.beads/`, that file serves double duty
as both the project config and the legacy user config. `br config path` shows it:

```
User config:        ~/.config/beads/config.yaml (not found)
Legacy user config: ~/.beads/config.yaml         (found)   ← silently wins
Project config:     <cwd>/.beads/config.yaml     (exists)  ← ignored while commented
```

### Symptom 1: `br init` in a sandbox prints a custom prefix but IDs use `jleechan-…`

`br init` writes a **commented-out** template into `<cwd>/.beads/config.yaml`:
```yaml
# issue_prefix: br-sandbox-…
```
Because the line is commented, the legacy overlay's `issue-prefix: "jleechan"`
wins and every bead in that sandbox gets `jleechan-…` IDs.

**Fix**: after `br init`, uncomment the line:
```bash
sed -i.bak 's/^# issue_prefix:/issue_prefix:/' <cwd>/.beads/config.yaml
```
Verified 2026-07-09 in `/tmp/br-fix2-…`: post-uncomment, new beads used `br-fix2-…`.

### Symptom 2: JSONL doesn't auto-flush after `br create`

The home workspace's config had `no-auto-flush: true` set. With that flag,
br writes to SQLite only — JSONL stays stale until you run `br sync --flush-only`.
Flipping it to `no-auto-flush: false` (in `/Users/jleechan/.beads/config.yaml`,
2026-07-09) fixed it AND reconciled ~169 dirty records that had been sitting in
the DB but not the JSONL.

**FIX applied 2026-07-09**: `~/.beads/config.yaml` line 5 — `no-auto-flush: true`
→ `no-auto-flush: false`. Pre-edit backup at
`/Users/jleechan/.beads/config.yaml.bak.20260709-105524`.

### Pre-flight before any "br is broken / JSONL is missing X" claim

1. `br config path` — see what's overlaying.
2. `br config list` — confirm `no_auto_flush:` and `prefix:`.
3. `wc -l .beads/issues.jsonl` vs `br count` — drift = dirty backlog.

### Related

- [[reference-bashrc-wrapper-claudem-minimax]] — similar "config file silently
  read from a path you didn't expect" failure mode.
- Beads primary store is SQLite (`beads.db`); JSONL is the export/sync artifact.
  Reading `.beads/*.jsonl` raw is forbidden in many repos — use `br show` /
  `br list` / `br search` instead.