# PR #2: Add Linux GTK tests (Layer 1-3) with evidence passing /er

**Repo:** jleechanorg/cmux_ubuntu
**Merged:** 2026-03-14
**Author:** jleechan2015
**Stats:** +5164/-588 in 93 files

## Summary
- Add Layer 1 AT-SPI tests (25/25 passing)
- Add Layer 2 screenshot capture tests
- Add Layer 3 socket integration tests
- Evidence bundle with SHA256 checksums proving Linux environment
- Improve cmux-ascii error handling for non-TTY

## Test Plan
- [x] Layer 1: AT-SPI tree tests pass 25/25
- [x] Layer 2: Screenshot capture works
- [x] Evidence review (/er) passes with PASS verdict
- [ ] Review PR

## Raw Body
## Summary
- Add Layer 1 AT-SPI tests (25/25 passing)
- Add Layer 2 screenshot capture tests
- Add Layer 3 socket integration tests
- Evidence bundle with SHA256 checksums proving Linux environment
- Improve cmux-ascii error handling for non-TTY

## Test plan
- [x] Layer 1: AT-SPI tree tests pass 25/25
- [x] Layer 2: Screenshot capture works
- [x] Evidence review (/er) passes with PASS verdict
- [ ] Review PR

## Evidence Bundle
Located at `/tmp/cmux-evidence-unified-20260309T055627Z/`:
- `run.json` - Test results (25/25 + 1/1)
- `linux_proof.md` - System metadata proof
- `uname_output.txt` - Linux kernel version
- `gtk_version.txt` - GTK 4.14.5
- All files with SHA256 checksums

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds functional pane-closing behavior to the `cmux-core` socket API and adjusts Docker build inputs, which can affect client behavior and CI/runtime images. Most other changes are formatting/diagnostics, but the new `ClosePane` semantics should be validated against GTK/web/TUI clients.
> 
> **Overview**
> **Adds real pane-closing support to the socket API.** `cmux-core` now implements `Command::ClosePane` by mutating the active tab’s split tree via `close_pane`, updating `active_pane_id`, and returning errors when attempting to close the last pane.
> 
> **Improves build/test packaging and CLI ergonomics.** Dockerfiles now copy `cmux-ascii` and `cmux-web` into build/selftest images, and `cmux-core` is explicitly configured as a binary target with a `src/main.rs` entrypoint.
> 
> **Developer-experience/data housekeeping.** `cmux-ascii` adds clearer non-TTY startup errors and logs terminal sizing (early exit on 0-size), `.gitignore` ignores a scheduled-tasks lockfile, and `.beads` issue-tracking JSON/metadata is added/updated.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit ff0d2179916562f6a33efa64618c274f70a7a39e. This will update 
