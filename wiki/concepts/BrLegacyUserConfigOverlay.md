---
title: "BrLegacyUserConfigOverlay"
type: concept
tags: [beads, config, troubleshooting]
sources:
  - sources/reference-br-legacy-user-config-overlay-2026-07-09.md
related_entities: [BrCLI]
last_updated: 2026-07-09
---

## Definition

`br` v0.2.16 silently overlays `~/.beads/config.yaml` as a "legacy user config"
into *every* cwd's br invocation. The resolution chain, in priority order, is:

```
User config:        ~/.config/beads/config.yaml    (not found)
Legacy user config: ~/.beads/config.yaml           (found)   ← silently wins
Project config:     <cwd>/.beads/config.yaml       (exists)  ← ignored while commented
```

For users whose real workspace lives at `~/.beads/`, that file serves double duty
as both the project config and the legacy user config. Because the resolution
chain is undocumented and the `br init` template writes project-level settings
as commented-out lines, the legacy overlay's values silently shadow the intended
project settings.

## Symptom

`br init` in a sandbox prints "Prefix set to: br-sandbox-…" but every bead created
in that sandbox gets `jleechan-…` IDs (or whatever prefix the legacy overlay has).

## Diagnostic

```bash
br config path    # reveals the resolution chain
br config list    # shows the resolved `prefix:` and `no_auto_flush:` values
```

## Fix

After `br init`, uncomment the template line in the project config:

```bash
sed -i.bak 's/^# issue_prefix:/issue_prefix:/' <cwd>/.beads/config.yaml
```

Verified 2026-07-09 in `/tmp/br-fix2-1783619767`: pre-uncomment, prefix =
`jleechan-…`; post-uncomment, prefix = `br-fix2-…`.

## Why It Matters

This is a non-obvious source of bugs because:
- `br init` output suggests the prefix was set correctly.
- The project YAML visually contains the prefix (commented).
- Only the user-config overlay chain explains the divergence.

Same failure mode as [[reference-bashrc-wrapper-claudem-minimax]] — silent
config-file shadowing across scopes.

## Related Concepts

- [[BrNoAutoFlushDrift]] — the second config quirk discovered in the same audit
- [[BrCLI]] — the tool exhibiting the quirk

## References

- Source page: `sources/reference-br-legacy-user-config-overlay-2026-07-09.md`
- Memory: `~/.claude/projects/-Users-jleechan/memory/reference_br_legacy_user_config_overlay.md`