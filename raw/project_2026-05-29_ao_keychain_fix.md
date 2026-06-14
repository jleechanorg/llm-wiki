---
name: project_2026-05-29_ao_keychain_fix
description: "Root cause and fix for \"Keychain Not Found — antigravity\" GUI dialogs from AO workers"
metadata: 
  node_type: memory
  type: project
  originSessionId: d1759262-c2bc-40df-804a-adaa3e48ac4b
---

## AO Antigravity keychain dialog — root cause and fix

**Root cause**: AO workers run with `HOME=~/.ao-sessions/<session-id>/`. macOS Security framework resolves the login keychain path from `$HOME/Library/Keychains/`. That directory doesn't exist in the fake session home → Security Agent shows "A keychain cannot be found to store 'antigravity.'" GUI dialog when `agy` tries to write/refresh its OAuth token.

**Fix (committed 2026-05-29)**:
- File: `packages/plugins/agent-antigravity/src/index.ts` in `jleechanorg/agent-orchestrator`
- Creates a symlink `~/.ao-sessions/<sid>/Library/Keychains → ~/Library/Keychains` before launching the worker
- Committed to `main` as `5588a1601` and cherry-picked to `feat/runtime-antigravity` as `694c1937c`

**Existing sessions**: Patch existing `~/.ao-sessions/*/Library/Keychains` symlinks manually when issue recurs:
```bash
for sid in $(ls ~/.ao-sessions/ 2>/dev/null); do
  kd=~/.ao-sessions/$sid/Library/Keychains
  [[ ! -e "$kd" ]] && mkdir -p ~/.ao-sessions/$sid/Library && ln -s ~/Library/Keychains "$kd" && echo "Patched $sid"
done
```

**Why pre-seeding the keychain entry didn't work**: The entry was stored in the login keychain but `agy` couldn't find ANY keychain to write to (different HOME), so it still showed the dialog on token refresh.

**Related**: `antig-cmux-loop.sh` has a socket guard (`[[ -S "$CMUX_SOCKET_PATH" ]] || exit 0`) to prevent cmux from triggering keychain access when cmux socket is absent. `com.jleechan.antigravity-loop.plist` was manually unloaded.
