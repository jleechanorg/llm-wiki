---
name: launchd-template-orphan-prevention
description: Committing plist template to repo is the only reliable way to prevent orphan launchd jobs; deploy.sh Stage 1b adds belt-and-suspenders cleanup
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-xty2
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

## Rule

Every plist installed to `~/Library/LaunchAgents/` must have a `@HOME@`-placeholder template committed to the owning repo *before* the plist is bootstrapped. A plist with no repo template is orphaned — cleanup scripts cannot find it.

## Why

`install-launchagents.sh` gates cleanup on the template existing in `~/.hermes/launchd/<label>.plist`. When `launchd/ai.hermes.prod.plist` was never committed, the cleanup step silently skipped removing the legacy `ai.hermes.gateway.plist` orphan on every deploy — causing the two-gateway drift that ran for months.

Root cause confirmed: commit `ae17c1bb28` added the missing template + deploy.sh Stage 1b cleanup (2026-06-09 incident, bead jleechan-eeql, GH issue [#602](https://github.com/jleechanorg/jleechanclaw/issues/602)).

## How to apply

- Before `launchctl bootstrap ...`, write the `@HOME@`-placeholder template and commit it.
- `/launchd` skill Step 4 is mandatory (not optional): "Commit the template to the owning repo."
- `deploy.sh` Stage 1b unconditionally removes `ai.hermes.gateway` and `com.hermes.gateway` as belt-and-suspenders regardless of installer state.

## Prod residue cleanup

Migration residue (e.g. `~/.hermes_prod/launchd/ai.openclaw.*`) must be explicitly `rm -f`'d — they are NOT removed by the installer or deploy.sh. Pattern:
```bash
rm -f ~/.hermes_prod/launchd/ai.openclaw.*
rm -f ~/.hermes_prod/launchd/com.openclaw.*
```

## Cherry-pick pattern for diverged session branches

When session work lands on `dev<N>` but `/integrate` created a newer `dev<M>` from main:
1. `git log --oneline main..dev<N>` — find commits not yet on main
2. `git cherry-pick <sha1> <sha2> <sha3>` in chronological order onto the new branch
3. Skip any commit whose equivalent is already on main (same message, different SHA)
4. Use `deploy.sh --skip-pull` when branch has no upstream set yet

## Verification

- 2026-06-10: cherry-picked 3 commits, deploy.sh canary PASS in 6s, gateway port 8642, HEAD `b8228777e3`
- `launchctl list | grep openclaw` = empty (all 26 removed from LaunchAgents)
- `~/.hermes_prod/launchd/ | grep openclaw` = empty (38 files removed)

## References

- Commit `ae17c1bb28` — ai.hermes.prod.plist template + deploy.sh Stage 1b
- Commit `11892b36e0` — rm 3 stale gateway plists, add 5 `@HOME@` templates
- `~/.hermes/launchd/ai.hermes.prod.plist` — canonical prod template
- `~/.hermes/scripts/deploy.sh` Stage 1b — orphan cleanup
- [[hermes-dual-gateway-drift]] — prior memory on dual-gateway root cause

## Reusable pattern

"Missing template = orphan survives cleanup" is the general law. Any cleanup script that gates on `[[ -f repo/launchd/$label.plist ]]` silently passes if the template is missing. The fix is not a smarter cleanup script — it's committing the template.
