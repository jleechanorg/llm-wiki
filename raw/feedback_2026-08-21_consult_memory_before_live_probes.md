---
name: consult-memory-before-live-probes
description: "When the data plane (live `du`, snapshot ledger, frontier scanner) is structurally incomplete, consult the memory plane (`/history`, `/ms, ~/.claude/projects/.../memory/*.md`) BEFORE spinning up live probes — they can name gaps that live measurement physically cannot see"
metadata: 
  node_type: memory
  type: feedback
  bead: disk_magician-pending-attribution-gap
  originSessionId: 59cb5847-ffee-401b-aaea-11f259e16a92
  modified: 2026-08-21T07:12:57.967Z
---

On 2026-08-20/21, a "what's taking up all the disk?" investigation hit a wall at ~537 GiB unattributed residual. I burned ~40 minutes and many `du` calls before the user nudged `/history /ms`, which surfaced two prior memory files (`project_2026-07-15_disk_swing_mechanisms_confirmed.md` and `project_2026-07-29_disk_rootcause_producers_and_decisions.md`) that:

1. **Named the exact 213.9 GiB TCC/SIP `~/Library` gap** (MobileSync, Mail, Messages, ~20 protected subtrees) as a permission wall, not a hidden consumer
2. **Named APFS local snapshots + container min-size pinning** as a separate structural contributor
3. **Confirmed that no live measurement from a non-FDA shell can see those paths** — the 537 GiB "mystery" was always explained; I just hadn't looked at the right artifact

The structural failures that lined up to mislead me, all in one session:
- Snapshot ledger had 34% coverage on the most recent run; the 14d-floor diff was unreliable
- `~/.disk_magician_state/frontier_last.json` was 1.5 days old AND its format was per-sibling-volume (532 entries that aren't a recursive breakdown) — I initially misread the data shape
- Live `du -d 1 $HOME` stalled 60s on a near-full disk; `sudo -n du /private/var` returned empty because the password prompt blocks in non-interactive shells; both had to be worked around with manual parallel probes
- `.beads/issues.jsonl` was blanket-gitignored in disk_magician's repo (only fixed this session, commit `48c31a1`), so prior beads weren't visible to swarm lane agents as context
- The disk_magician repo's `disk-root-cause` skill said to use `~/.disk_magician_backup/ledger/topdown-5g.json`, but I trusted the snapshot's own self-reported "fresh" claim and didn't cross-check against `git ls-remote` — turns out the format was right but the content was stale

**Why this matters:** I had every skill loaded that should have caught this. The `disk-root-cause` skill's Phase 0 says "authenticate the data source" but doesn't have an explicit step that says "before any live probe, check whether prior memory files already name the gap you're trying to measure." I followed Phase 0 mechanically (run `disk-magician audit`, query the snapshot, etc.) and got structurally-low-coverage data, then used that bad data to drive all subsequent decisions.

**How to apply (rule of three, in priority order):**
1. **Memory first.** When the user asks a disk/system/operational question, before any live probe, `ls -t ~/.claude/projects/<current-git-root-derived-key>/memory/ | head -10` and grep for keywords. If a prior session named it, that is the answer (or the load-bearing constraint) — don't re-measure.
2. **Then history.** If memory is silent, `Skill("history", args="<query> --recent 30 --source claude")` to find prior transcripts that might have measured it.
3. **Then live probes.** Only if memory and history are both silent should you start running `du`, `df`, etc. And when you do, **bound every probe with a timeout** (`timeout 30 du -sh $d 2>/dev/null &`) and **probe specific known-large subdirs in parallel**, not `du -d 1 $HOME` which stalls on near-full disks.
4. **Cross-validate every data source.** If the snapshot says "fresh" but the snapshot's own coverage is <50%, **explicitly discount the floor** and say so in the report (per disk_magician/CLAUDE.md: "Days where `snapshot_coverage_pct < 70%` get WARNING: low_coverage; treat those deltas as directional, not exact"). I knew this rule and didn't apply it.

**Specific gaps to fix in the skill/scripts (low-cost, high-value):**
- (a) `disk-root-cause` skill: add an explicit "Step 0.5 — consult prior memory" phase between Phase 0 (env ground truth) and Phase 1 (floor + deltas). It takes ~10 seconds (`ls + grep`) and would have caught the 213.9 GiB TCC gap on the first turn.
- (b) `disk_magician.sh audit` could output a "memory references found" line that lists relevant prior memory files by keyword, so the agent has them in context before live probes start.
- (c) The repo's `CLAUDE.md` investigation methodology lists "never-delete" rules but doesn't list "the disk may have a TCC/SIP structural floor that no non-FDA shell can measure — when you see a big unattributed residual, FIRST consult `feedback_2026-07-15` memory for the documented 213.9 GiB gap, then look for new contributors." Adding that line would make the floor-and-buckets methodology complete.

**Do NOT** (anti-patterns I fell into this session):
- Do NOT spend 5+ minutes running `du` against a near-full disk hoping the answer appears
- Do NOT trust a snapshot's self-reported "fresh" claim without checking `git ls-remote origin main`
- Do NOT confuse per-sibling-volume entries with a recursive top-down breakdown (different schemas)
- Do NOT assume a bead history exists in a repo without checking `git log --all -- .beads/issues.jsonl` first (was missing for disk_magician until this session)
- Do NOT take a pasted system-reminder "consolidated report" at face value — verify against an independent live read of the same artifact before reporting it as your own conclusion

**Verification:** would have caught the 213.9 GiB TCC gap on the first /p turn if the agent had run `ls /Users/jleechan/.claude/projects/-Users-jleechan-projects-other-disk-magician/memory/ | grep -iE "tcc\|sip\|fda\|213\|mobilesync"` and read the 2026-07-15 memory file. That grep takes <1 second and returns exactly the memory file that names the gap.

See also: [[disk-magician-portability-three-separate-claims]] (the same root-cause class: trust the data source claim without independent verification).