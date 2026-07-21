---
name: fat-command-to-thin-skill-migration-regression-test-check
description: "When relocating content from a Claude Code command file into a canonical SKILL.md (thin-stub pattern), a repo's own test suite may encode the OLD structure and needs updating — grep the target repo's tests before AND after this refactor"
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-wqz
  originSessionId: 0ffd19bb-d81f-4079-804c-1cea8a822f5b
---

During the dark-factory thin-skill migration (`/f`, `/factory`, `/fs`, `/factory-spec` → canonical `SKILL.md` files, PR jleechanorg/dark-factory#251), CI failed after merge review passed docs-only sanity checks (/advice, adversarial verification). Root cause: `tests/test_slash_command_binary_contract.py` was a real repo regression-test guard that asserted specific literal text (the binary proof-block labels, the reviewer-calibration contract) existed **inside `f.md`/`fs.md` themselves**. That assumption was exactly the pre-migration architecture — this PR deliberately moved that content into `dark-factory/SKILL.md` / `factory-spec/SKILL.md` as the single source of truth, with the command files reduced to thin pointer stubs. The test broke not because content was lost, but because it checked the wrong file for the new architecture.

**Why this is easy to miss**: a "docs-only" classification (markdown files only, no `.py`/`.ts` changed) creates a false sense that no code-level regression risk exists. But a repo can have Python (or any language) tests that assert on the CONTENT of markdown/prompt files — a legitimate and common pattern for guarding prompt/instruction contracts. `git diff --stat` alone won't surface this; you have to actually search the test suite for references to the files you're touching.

**Second discovery in the same test run**: the same refactor also flagged a genuine wording regression — the migrated `fs.md` stub used the phrase "in-session review"/"read-only" near `/fs --review`, which a different guard test (`test_fs_has_no_read_only_in_session_modes`) explicitly forbids, because the design intent is that `/fs` must never sound like it has a non-binary shortcut mode (that framing belongs only to `/factory-spec`). This was caught by CI, not by review — a reminder that even careful adversarial doc review (2 rounds of /advice, 1 independent verification pass) can't substitute for actually running the target repo's test suite.

**How to apply**: before merging ANY "content relocation" refactor (fat-file → thin-stub-plus-canonical-source, or any similar consolidation), `grep -rl "<filename-being-trimmed>"` across the target repo's `tests/` directory (or equivalent) for both the file names being changed AND string patterns that might match content you're moving. Run the affected test file(s) locally before pushing. When a test needs updating to match a deliberate architecture change, that's a legitimate fix — but characterize it explicitly as "test encoded the old assumption, updating to check the new source of truth," not as "weakening the test."

See also: [[usage-signal-substring-count-invalid]], [[directive-sentence-cross-check-catches-content-loss]]
