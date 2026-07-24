---
name: coderabbit-changes-requested-can-hide-real-bugs-on-docs-only-pr
description: "A CodeRabbit CHANGES_REQUESTED review on a \"docs-only\" PR is not automatically low-risk lint noise — always read the actual comment bodies, one finding was a real functional-correctness bug embedded in documentation text"
metadata: 
  node_type: memory
  type: feedback
  bead: jleechan-wqz
  originSessionId: 0ffd19bb-d81f-4079-804c-1cea8a822f5b
---

On PR jleechanorg/dark-factory#251 (a markdown-only thin-skill-migration refactor, classified as low-risk/docs-only), CodeRabbit returned `CHANGES_REQUESTED` with 3 findings. Two were trivial markdownlint MD040 (missing language identifier on a code fence) — the kind of finding easy to assume ALL CodeRabbit findings on a docs-only PR will be. The third was flagged "Major/Functional Correctness": the migrated skill documentation said `--feature <name>` "defaults to `hello`" unconditionally, which directly contradicted a Honesty rule in the SAME file added earlier in the same PR ("do not invent `--feature` values; confirm the holdout directory exists before passing it"). This is a real logic/contract bug living inside prose documentation that an LLM agent reads and acts on — not a style nit.

**Why it's easy to dismiss prematurely**: "docs-only" correctly describes the file-extension/diff-shape of the change, but for prompt/instruction/skill files, the CONTENT is executable in the sense that an agent reading it will follow the documented default literally. A "docs-only" PR touching agent-instruction files carries the same functional risk class as code — the CI/review gates should be treated accordingly, not waved through as automatically safe.

**How to apply**: never skip reading CodeRabbit's full comment bodies on the assumption that a docs-only PR's findings will all be lint noise. When CodeRabbit returns CHANGES_REQUESTED, fetch every comment via `gh api repos/OWNER/REPO/pulls/N/comments` and read the actual finding text and severity tag (e.g. "🎯 Functional Correctness | 🟠 Major") before triaging — don't assume, verify. This generalizes the existing "unit-only proof is insufficient" principle to review-gate handling: docs-only classification changes the EVIDENCE TIER required (per `/green`'s two-tier standard), but it does not change whether individual review findings need to be read and evaluated on their actual content.
