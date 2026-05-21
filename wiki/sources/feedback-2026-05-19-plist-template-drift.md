# Plist Template Drift Anti-Pattern — Hermes Launchd (2026-05-19)

**Source**: `~/.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-05-19_plist_template_drift.md`
**Bead**: `orch-oxdm`
**PR**: [#584](https://github.com/jleechanorg/jleechanclaw/pull/584) merged 2026-05-19

## Summary

Four classes of silent plist breakage discovered during deep audit of all Hermes launchd jobs:

1. **Wrong placeholder format**: `setup-launchd.sh` only substitutes `@HOME@`, `@HERMES_BIN@`, `@REPO_ROOT@`, `@HERMES_EXTRA_PATH@`. Any other format (`@NODE_BIN_DIR@`, `__HOME__`) survives as a literal string in the installed plist.

2. **Orphaned installed plists**: `ao-notifier`, `gh-actions-cost-monitor`, `spend-alert-daily` installed in LaunchAgents with hardcoded `/Users/jleechan/` paths but no repo templates. Invisible until re-install.

3. **MINIMAX vars behind `.bashrc` interactive guard**: `MINIMAX_API_KEY` at line 894, guard at line 283. Fix: `_extract_bashrc_var` pattern in `launchd-env-wrapper.sh` greps `.bashrc` directly.

4. **`source .bashrc` in bash -c ProgramArguments**: Hits the same interactive guard. Fix: use `launchd-env-wrapper.sh` as ProgramArguments entry point.

## Additional deploy.sh fixes

- `sleep 1→3` after `launchctl bootout` (port-release race on port 8642)
- Stage 0 now auto-renames ALL non-canonical duplicates to `.disabled` (was only `ai.hermes.gateway`)
- Plist existence check before `launchctl bootstrap`
- `mkdir -p logs` before bootstrap
- Wrapper existence/executable check in `hermes_preflight`

## Audit commands

```bash
# Find installed plists with no repo template:
diff \
  <(ls ~/Library/LaunchAgents/ | grep -E "^(ai\.hermes|com\.hermes)" | sed 's/\.disabled$//' | sort -u) \
  <(ls ~/.hermes/launchd/ | sed 's/\.template$//' | sort -u)

# Find templates with unrecognized placeholders:
grep -r "@[A-Z_]*@" ~/.hermes/launchd/*.template \
  | grep -v "@HOME@\|@HERMES_BIN@\|@REPO_ROOT@\|@HERMES_EXTRA_PATH@"
```

## Related

- [[hermes-launchd-meta-pattern]] — broader meta-pattern
- [[feedback-2026-04-30-launchd-env-isolation]] — original MINIMAX launchd issue
