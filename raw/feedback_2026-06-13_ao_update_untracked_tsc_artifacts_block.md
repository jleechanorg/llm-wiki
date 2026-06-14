---
name: ao-update-untracked-tsc-artifacts-block
description: "scripts/ao-update.sh's ensure_repo_clean check fails when packages/cli/src/{commands,lib}/*.js and *.d.ts are present as untracked colocated tsc output from prior builds. The fix: do a manual deploy (rebuild + pkill + scripts/start-all.sh) instead of fighting the check, or add the patterns to .gitignore."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

**Why:** 2026-06-13 deploy after merging #683/#681/#679. After `git pull --ff-only origin main`, `bash scripts/ao-update.sh` exited with "Working tree is dirty" because `packages/cli/src/commands/skeptic/{gh-client,posting,verdict-utils}.{js,d.ts,d.ts.map,js.map}` and `packages/cli/src/lib/shell.{js,d.ts,...}` were untracked. These are stale tsc output files — when tsc is run with `outDir: dist` (the actual config), it should write to `dist/`, not `src/`. But a prior `tsc` invocation without proper config emitted these colocated artifacts in `src/`, and they're now sticky.

**How to apply (manual deploy path that works):**

1. `git pull --ff-only origin main` (main clone must be on main, FF-clean)
2. `pnpm --filter @jleechanorg/ao-core build` (rebuilds core/dist)
3. `pnpm --filter @jleechanorg/ao-cli build` (rebuilds cli/dist)
4. **Verify new code is in dist** (greps for the symbols from your PRs):
   ```bash
   grep -c "perPrCooldownMs" packages/core/dist/skeptic-cron-local.js
   grep -c "headSha" packages/cli/dist/commands/skeptic/mergeGate.js
   ```
5. **Kill existing workers** (they hold old code in memory):
   ```bash
   pgrep -f "lifecycle-worker" | xargs -r kill -TERM
   sleep 2
   pgrep -f "lifecycle-worker" | xargs -r kill -KILL
   ```
6. **Re-fork workers with new dist**:
   ```bash
   bash scripts/start-all.sh
   ```
7. **Verify deployment**:
   ```bash
   node packages/cli/dist/index.js doctor
   # Should show all workers using canonical binary /Users/jleechan/bin/ao
   # Should show "core package is built" and "CLI package is built" as PASS
   ```

**Adjacent learning — why `pkill` alone is insufficient**: The first `pkill -f "lifecycle-worker"` returned 17 workers (the count grew, not shrank). The `pkill` was likely being absorbed by the launchd-wrapped process group. Use `pgrep | xargs kill -TERM` first, wait 2s, then `pgrep | xargs kill -KILL` for any survivors. Verify with `pgrep | wc -l` == 0.

**Permanent fix (for next time someone wants `ao-update.sh` to work)**:
- Add to `.gitignore`:
  ```
  packages/*/src/**/*.js
  packages/*/src/**/*.js.map
  packages/*/src/**/*.d.ts
  packages/*/src/**/*.d.ts.map
  ```
- OR clean before running: `git clean -fd packages/cli/src/ packages/core/src/` (risky — wipes test fixtures)

**Watchdog BASH scripts don't need process restart**: `scripts/ai.agento.health-guardian.sh` and `scripts/hermes-watchdog.sh` are BASH; they re-read from disk on each launchd invocation. With `StartInterval=3600` (1 hour), the new code is picked up on the next tick. Verify the file content matches HEAD main: `diff -q scripts/ai.agento.health-guardian.sh <(git show HEAD:scripts/ai.agento.health-guardian.sh)`.
