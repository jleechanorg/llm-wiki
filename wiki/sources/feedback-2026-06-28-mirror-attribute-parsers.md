---
title: "Mirror existing attribute parsers — tokenization pattern"
type: source
tags: [dark-factory, code-review, conformance, dot-graphs, pr-130]
date: 2026-06-28
source_file: ../../raw/feedback_2026-06-28_mirror_existing_attribute_parsers.md
---

## Summary
When adding a conformance/validator rule that reads a graph attribute (`class`, `type`, `feature`, ...), mirror the tokenization of every existing parser of that attribute in the codebase. Scalar equality (`class_val == "explore"`) silently false-fails graphs that combine role + styling tokens (`class="codergen explore"`); the canonical pattern is `str(...).replace(",", " ").lower().split()` + membership, as in `runner/parser.py:_selector_matches`. PR #130 shipped a P2 fix (`0fd3e2e`) for exactly this case after Codex cold-review caught it on the introducing commit.

## Key Claims
- **Mirror-attribute-parsers rule**: `grep -rn 'node.attrs.get("<attr>"' runner/ bin/conformance` BEFORE writing any new rule that reads that attribute; copy the tokenization convention verbatim.
- **Scalar `==` on `class` is broken by design** — DOT `class` is a multi-token free-form string; `class_val == "explore"` fails any graph using `class="codergen explore"` or `class="codergen,implement"`.
- **Codex catches this, self-review doesn't** — Codex reads the full repo and compares each new rule to existing parsers; self-review treats each new rule in isolation. The mirror-attribute-parsers rule is the manual equivalent.
- **Regression coverage needs multi-token fixtures** — single-token fixtures alone hide the bug. PR #130 added `tests/fixtures/level5_multi_class.dot` covering both separator forms.
- **Existing canonical parser**: `runner/parser.py:_selector_matches` line 223-230.

## Key Quotes
> "DOT graph attributes are free-form strings. In dark-factory's parser convention... `class` is normalized as `str(...).replace(',', ' ').lower().split()` and compared via `in` (membership). The new `bin/conformance:_check_level5` rule initially used `class_val == 'explore'` — which is fine for the first authoring pass, but fails the moment a real graph combines the role token with a routing/styling class."

> "Why Codex catches this but I don't: Codex reads the full repo and compares each rule to existing parsers of the same attribute. My self-review treats each new rule in isolation. The mirror-attribute-parsers rule above is the manual equivalent of what Codex does automatically — apply it pre-merge and the Codex finding class drops to near-zero."

## Connections
- [[Codex]] — the cold-review bot that caught this P2 finding on PR #130's introducing commit.
- [[AttributeError]] (concept) — sibling concept; runtime attribute parsing errors. This entry is about static validation, not runtime.
- `pipelines/factory/level5_feature.dot` (real-world graph) — has the `explore`/`plan`/`implement`/`fix` nodes the new rule checks for. Currently uses bare `name=`, not multi-token `class`, but future graphs will.
- `bin/conformance` (file) — rule at lines 215-225 post-fix; was scalar at line 218 pre-fix.
- `runner/parser.py:_selector_matches` — the canonical tokenization pattern this rule now mirrors.
- PR [#130](https://github.com/jleechanorg/dark-factory/pull/130) — full PR thread; merge commit `e73e230`, fix commit `0fd3e2e`.
