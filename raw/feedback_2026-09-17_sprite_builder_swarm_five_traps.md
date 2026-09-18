---
name: sprite-builder-swarm-five-traps
description: Five traps from the 2026-09-17 sprite-builder swarm (PR #436) — squash-merge doclint break recurs, fixed starfield hides static screens, reviewer CLI quirks, Workflow junk StructuredOutput, verify_pr_claims false negatives
type: feedback
bead: wc-m11km (follow-ups wc-yxptc)
metadata:
  type: feedback
---

Context: /swarm mission `dragon-knight-modular-sprite-builder` (bead wc-az1vq), draft [PR #436](https://github.com/jleechanorg/worldai_claw/pull/436), sealed at 1548f688 with all five ironclad criteria at one HEAD. Evidence gist: https://gist.github.com/jleechan2015/3a50daa5b64913b1812cc3a9386d2bc0.

**1. Squash-merge breaks main's AUTHORITY doclint — it recurred (Anti-Pattern, Critical).** PR #434 was squash-merged as 5a903f80; `docs/plans/worldai-2d/contracts/AUTHORITY.md` still recorded the pre-squash SHA 3821894c, so `packages/game-contracts/test/doclint/authority.test.ts` fails on main and on every PR that merges main (#431, #432, #436 after update-branch). **Fix recipe:** at the BASE of the stacked PRs, rewrite each `this repo` row to `git log -1 --format=%H -- <path>` (script in the swarm transcript), run the doclint locally (30/30), push, then merge upward (#431 869c118b → #432 e3043042 → #436). Root fix is a branch-protection rule "merge commits only" or a doclint job that runs on main pushes — neither exists yet. See [[pr320-merged-spec-on-main]] (2026-07-28, same trap).

**2. `#root`'s `position:fixed; z-index:0` starfield paints over any static-positioned screen (Critical for new web screens).** A new `<main>` at `position:static` renders under the ambient canvas; only elements with their own stacking context (e.g. `opacity:.8`) show through. jsdom tests were 100% green while the page was invisible; the headless live check caught it. **Rule:** every new top-level screen in `packages/web` gets `position: relative; z-index: 1` (the repo already does this for `.card > *`, styles.css:1637). Fix applied in 316ccc96 (`spritebuilder.css`). Filed as a follow-up to fix at the shell level (bead wc-yxptc).

**3. Reviewer CLIs on this host (Reference).** codex: usage limit ("try again at Sep 19th, 2026 1:25 AM"). `gemini -m gemini-3-flash-preview -p "<long tool-using prompt>" --yolo` hangs silently with 0 output; the same CLI answers static `-p` prompts (≈100 KB diff inline) fine. `cursor-agent -f -p --output-format text "<prompt>"` executes tests, writes attack scripts, and returns a report — it is the working executing reviewer when codex is out. Pass prompts via `"$(cat file)"`; write outputs to files under `~/dk2d_evidence/…`, never /tmp.

**4. Workflow-tool readers can return junk after repeated schema failures.** A `read:web` agent failed `StructuredOutput` validation three times (facts must be an array) and finally submitted `{"summary":"test",…}`; the workflow recorded that junk as its result. The real report was the LONGEST `StructuredOutput` attempt in `subagents/workflows/<run>/agent-<id>.jsonl` — recover from there instead of re-running. Also: a Fable synthesis agent died on the 20k output-token cap; write the lane brief yourself from the reader outputs.

**5. `verify_pr_claims.py` false negatives.** It resolves every path token from the repo root and treats any 7–40 hex token with a letter as a git SHA. `tests/x.test.ts` (cwd `packages/web`) → "not found"; a 12-hex bundle hash → "dangling commit". Write repo-relative paths (`packages/web/tests/…`), use vitest name filters in commands (`npx vitest run spritebuilder-compose`), and cite content hashes as the full 64-hex string. After that: 19/19, exit 0.

**How to apply:** before any PR that touches AUTHORITY-tracked docs, plan a merge commit; before claiming a new web screen works, run a real headless capture (`testing_ui/spritebuilder_live_check.py` pattern); pick the reviewer CLI by a 60-second live probe; inspect workflow journals for junk results; make PR bodies machine-verifiable.
