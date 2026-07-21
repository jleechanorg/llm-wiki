---
name: runner-fleet-stale-snapshot-false-alarms-during-jit-registration
description: "GH API runner status snapshots during ezgha JIT registration bursts show 'missing' runners that are actually running on the host. ezgha registers 1-2 runners per 20s cycle; a snapshot mid-burst can capture 4-5 of 10 runners. No fix needed — wait 1-2 minutes for registration to complete."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-linux-c-runners-missing
  originSessionId: 6d6509e7-ea7b-44a2-8aa5-e0699e99ba2c
---

# Runner fleet stale-snapshot false alarms during JIT registration

## Context
- 2026-07-13 around 12:30Z: User reported the c-runner fleet appeared to drop from 9 to 4 runners on the GitHub API
- Investigation: ezgha config on jeff-ubuntu already set to `count = 10`, containers were running, but only 4 had completed GitHub registration at the snapshot moment
- 5 of the 5 "missing" runners (c-4, c-5, c-6, c-7, c-9, c-10) were physically up as Docker containers on jeff-ubuntu and completed registration within 1-2 minutes after the snapshot

## The pattern (second false alarm in this session)
1. Round 4 (earlier today): "c-4 offline + c-5 missing" — was heartbeat-gap stale snapshot, not a real outage
2. This case (round 7+): "5 c-runners missing" — was JIT registration delay, not a real outage

Both cases presented the same way: a low-count snapshot that suggested an outage, but the actual host state was healthy.

## Root cause
`ezgha` reaper registers runners 1-2 at a time with a configurable `serve_tick_seconds` (default 20s). When the fleet config changes (e.g., count bumped from 3 to 6, or 6 to 10) or the host is recovering from a hiccup, there's a burst of pending registrations. A `gh api runners` call during this burst can capture a partial state where only some runners have completed the GitHub registration flow.

## Rule for future runner fleet debugging

1. **ALWAYS wait 1-2 minutes** after any fleet config change before pulling the GitHub API. Re-pull at least 2-3 times with ~30s gaps to confirm a real outage vs transient.
2. **Cross-check with the host** — SSH to the runner host (`jeff-ubuntu` for c-runners, the Mac for b-runners) and check:
   - `docker ps --filter label=ezgha=managed` (containers actually running?)
   - `ps aux | grep ezgha` (orchestrator alive?)
   - `cat /home/jleechan/.config/ezgha/config.toml` (what's the configured count?)
3. **The Mac and Linux fleets have SEPARATE ezgha configs** — Mac at `~/Library/Application Support/org.jleechanorg.ezgha/config.toml`, Linux at `/home/jleechan/.config/ezgha/config.toml`. Don't assume one config covers both.
4. **Off-by-default ezgha config location on macOS**: ProjectDirs: `~/Library/Application Support/<bundle-id>/config.toml`. XDG path `~/.config/ezgha/config.toml` is NOT read on macOS.

## Verification pattern (re-measure)
```bash
# Snap 1
gh api orgs/jleechanorg/actions/runners --paginate | jq '.runners | length'

# Wait 60s

# Snap 2
gh api orgs/jleechanorg/actions/runners --paginate | jq '.runners | length'

# If Snap 2 > Snap 1, registration was in-flight. Wait more.
# If Snap 1 == Snap 2 and both are below configured count, real outage.
```

## References
- `/home/jleechan/.config/ezgha/config.toml` on jeff-ubuntu (Linux c-runner config)
- `~/Library/Application Support/org.jleechanorg.ezgha/config.toml` on Mac (b-runner config)
- ezgha source: `jleechanorg/ez-gh-actions` (PR #77 ezgha memory detection fix)
- Session transcript: `/Users/jleechan/projects/worktree_runner_342423` (round 7+ investigation)
- Bead `rev-linux-c-runners-missing` — investigation-only, no PR needed

## Verification
- This case: config was already at count=10; 9 of 10 registered within 2 minutes of snapshot
- No fix was needed
- Avoided: false alarm investigation that would have led to a "fix" that made things worse
