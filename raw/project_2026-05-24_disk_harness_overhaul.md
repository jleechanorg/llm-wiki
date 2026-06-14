---
name: project-2026-05-24-disk-harness-overhaul
description: 2026-05-24 disk investigation reclaimed ~14 GB and rebuilt the snapshot system to detect blindness. Root cause was 575 GB invisible to disk_snapshot.json due to silent du timeouts + sparse-file overcounting + missing trackers.
metadata: 
  node_type: memory
  type: project
  originSessionId: 3adc0978-ca90-406b-96fa-7e8f6cd197d2
---

**What happened:** Disk hit 93% (869/926 GB) on 2026-05-23, triggered alert. Investigation revealed `disk_snapshot.sh` had 71% blindness — `.gemini` (138 GB), `.ao-sessions` (62 GB), `~/projects` (71 GB), and others were either untracked or silently reporting 0 KB.

**Why:** Three compounding bugs in `~/projects_other/user_scope/scripts/disk_snapshot.sh`:
1. **Silent du timeout → 0** — `dir_size_kb()` had no rc-124 handling, so timed-out measurements looked identical to empty dirs (see [[feedback-silent-zero-anti-pattern]])
2. **Sparse file apparent vs allocated** — `Docker.raw` measured by `stat -f%z` reporting 926 GB instead of 60 GB allocated (see [[feedback-sparse-file-du-not-stat]])
3. **Missing trackers** — `.gemini`, `.ao-sessions`, `.hermes_prod`, `.openclaw`, `library_containers`, `library_logs`, several project dirs absent from `MONITORED_DIRS`

**Fixes landed:**
- `dir_size_kb()` returns empty string on timeout/error; main loop converts to JSON `null`
- Added 13 new monitored entries including the previously-hidden 200 GB
- Per-entry timeout overrides (slow paths get 120–300s)
- New `snapshot_coverage_pct` field + `snapshot_warning: "low_coverage"` when <70%
- New `timeout_keys` array listing entries that returned null
- New `--discover` mode scans `~/.[!.]* ~/*` for >5 GB dirs not yet tracked
- `dir_size_kb()` now uses `du -sk` for both files and dirs (sparse-file fix)
- New `tests/test_disk_snapshot.py` with 10 regression tests (8s runtime)
- Updated `~/.claude/skills/disk-audit/SKILL.md` with snapshot-validation Phase 0

**Reclaimed in this session (~14 GB):**
- 9 GB — `~/.codex/*.codex-repair-*.bak` (orphan SQLite repair backups from 2026-05-18)
- 1.2 GB — Library/Caches (claude-cli-nodejs, antigravity-updater, granolaelectron-updater)
- 1 GB — Stale venvs in 4 abandoned projects
- 1 GB — Old `__pycache__` dirs (>30d) across projects
- 756 MB — `~/Library/Logs/cmux-focus.log` (truncated, log keeps writing)

**Reclaim NOT executed (need user judgment):**
- `~/.gemini/antigravity-ide/worktrees` (17 GB) — NOT a true dupe; contains unique 2.7 GB `worktree_antig`; Antigravity actively running. Close IDE first.
- ~~`~/.ao-sessions/ao-5847` (52.7 GB)~~ — **DELETED 2026-05-24** (WORKTREE APPROVED). Was `ao-5847/.gemini/antigravity/worktrees/worktree_worldarchitect/` with 79 sub-worktrees × ~1 GB each. Freed 49 GB on disk.
- `~/projects` deep venv prune — 60+ GB potential in active projects' venvs/node_modules; needs project-by-project review.

**AO session bloat prevention (implemented 2026-05-24):**
- Approach 3 (launchd cron): `com.jleechan.cleanup-ao-sessions.plist` — runs `scripts/cleanup-ao-sessions.sh --clean --days 14` at 4:23 AM daily. Prunes worktree venvs from sessions ≥14 days old with no active tmux. Loaded.
- Approach 1 (agent self-cleanup): Added post-task cleanup rule to `backup/Mac/gemini/GEMINI.md` — agents delete their own worktree on task completion.
- Approach 2 (uv hardlink): NOT implemented — `venv_utils.sh` uses pip not uv; would require worldarchitect.ai code changes. Estimated 98% venv size reduction if done (79 × 671MB → 671MB shared). Low priority vs. approaches 1+3.

**How to apply (future sessions):**
- Before quoting `disk_snapshot.json` numbers, run Phase 0 of disk-audit skill (check `snapshot_coverage_pct`)
- Before recommending IDE-worktree cleanup, check `ps aux | grep -i <ide>` and `lsof +D <path>`
- Before deleting venvs/.venv, check parent dir's `git log -1 --format=%ai` ≥90 days old
- The 2026-05-12 + 2026-05-21 disk sessions both hit this snapshot blindness too — they should have caught it earlier. Now there's coverage_pct + tests + skill rules to prevent recurrence.

**Follow-up cleanup 2026-06-08 (disk hit 99% / 12 GiB free):**
- Confirmed Antigravity worktrees are STILL the dominant recurring bloat: `~/.gemini` = 45 GB, with `~/.gemini/antigravity/worktrees/worldarchitect.ai/fix-pr-7126-green` alone = 27 GB (one clean+pushed git worktree, branch `fix-light-fantasy-gate-macos`). Removed via `git -C ~/worldarchitect.ai worktree remove --force <path>` (WORKTREE APPROVED) → `.gemini` dropped to 17 GB.
- **NEW recurring big safe win: `~/Library/Developer/Xcode/DerivedData` = 21 GB** — mostly `cmux-*` + Ghostty build caches; 100% safe (regenerates). Not deleted by `disk_audit.sh --clean`'s analysis phase reliably because that phase is slow (timed out twice at 120s+ on the home-dir `du`). Direct `rm -rf ~/Library/Developer/Xcode/DerivedData/*` is the fast path. Consider adding Xcode DerivedData as an explicit early target in disk_audit.sh.
- npm `~/.npm/_cacache` = 1.9 GB (safe). openclaw conversation-backups now 0 B.
- **APFS snapshot pinning gotcha:** deleted ~50 GB (du-measured) but `df` only showed ~20 GB freed immediately (55→75 GiB). The other ~30 GB was pinned by 3 `com.apple.os.update-*` local snapshots (one is `MSUPrepareUpdate` = pending macOS update). Did NOT delete them (system-managed, may be needed for the queued OS update). They release when the update installs or snapshots age out. Lesson: after a big cleanup, `df` free-gain < du-deleted is normal when APFS local snapshots exist — check `tmutil listlocalsnapshots /`.
- `disk_audit.sh --clean` is impractical for "I need space now" because its analysis phase (`du` over big home dirs) times out before reaching the deletion phase. For urgent cleanup, target the known wins directly (Xcode DerivedData, antigravity worktrees) rather than running the full script.
