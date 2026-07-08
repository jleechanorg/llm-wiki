---
name: archive-not-delete-and-verify-before-prune
description: "two durable rules from the 2026-07-07 skill cleanup — always archive (move to _archive/) rather than delete, and always diff actual content before pruning based on usage stats alone, since zero-usage can reflect selection bias rather than quality"
metadata: 
  node_type: memory
  type: feedback
  bead: "rev-im8tc, jleechan-fmf1, jleechan-9iql"
  originSessionId: ed376cb6-f347-4237-a510-b404c88d46f0
---

**Rule 1 — archive, never delete, for any tooling/skill/config cleanup.** When removing a skill, config entry, or any harness artifact based on a usage or redundancy claim, move it to a dated `_archive/_removed-YYYY-MM-DD/` directory (this repo's existing convention — precedent dirs already existed: `_removed-2026-06-18`, `_removed-2026-06-19`) rather than `rm`. This costs nothing extra and makes every prune decision fully reversible if the usage/redundancy claim later turns out to be wrong.

**Rule 2 — verify actual content before pruning on a usage-stat claim alone.** A 2026-07-07 skill-usage audit found 16 `tessl__X` skill directories with zero invocations in a 14-day window, each with a same-concept `superpowers:X` plugin alternative that WAS used — the initial recommendation was to blanket-archive all 16 as redundant duplicates. Diffing the actual body content (not just comparing descriptions or trusting the zero-usage stat) found only 4 of 14 comparable pairs were true duplicates; the other 10 had **genuine methodology differences**: one had a materially different review workflow (combined task-reviewer + broad final review vs. two sequential reviewers), one had an entire extra "Detect Environment" worktree-detection step the alternative completely lacked, one had an entire "Task Right-Sizing" section missing from the alternative. Blanket-archiving on the usage stat alone would have silently deleted potentially-better methodology that the model simply wasn't picking — the zero-usage signal reflected **model selection bias** (a naming/ordering preference between offered skill options), not a judgment that the content itself was worse.

**How to apply:** before archiving/deleting ANYTHING based on "this is unused" or "this is a duplicate of that," run an actual diff of the real content (not descriptions, not usage counts) and read a sample of the differences yourself. If the content differs only in wording/branding (verified: trivial 4-8 line diffs, de-branding style rewording), archiving is safe. If the content differs in actual logic/steps/workflow (even a handful of substantive lines), do NOT archive — the better disposition is usually "back-port the superior content into the actively-used version, THEN archive the redundant copy" rather than a blind keep-or-delete choice. This generalizes beyond skills: applies to removed MCP servers, deprecated config keys, or any "looks unused, safe to remove" claim — see also [[tool-use-grep-adjacency-false-negative]] from the same day, where a similar "trust the usage stat" mistake nearly cost two actively-used MCP servers before an adversarial review caught it.

Real numbers and full per-pair categorization: bead `rev-im8tc`; diff artifacts persisted at `~/roadmap/skill-cleanup-2026-07-07/diff_bodies/` (37 files, survives past the originating session).
