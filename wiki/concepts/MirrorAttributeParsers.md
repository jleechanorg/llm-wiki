---
title: "MirrorAttributeParsers"
type: concept
tags: [dark-factory, code-review, conformance, dot-graphs, parser-pattern]
sources: ["feedback-2026-06-28-mirror-attribute-parsers"]
last_updated: 2026-06-28
---

## Summary
When adding a new validator/conformance rule that reads a graph attribute (`class`, `type`, `feature`, ...), grep for every existing parser of that attribute in the codebase and copy the tokenization convention verbatim. Scalar `==` comparison silently false-fails graphs that combine role + styling tokens (e.g., `class="codergen explore"`), producing errors that only surface once a downstream graph lands with the multi-token form.

## Why it fails without mirroring
DOT graph attributes are free-form strings. In dark-factory's parser convention (`runner/parser.py:_selector_matches` line 223-230), `class` is normalized as `str(...).replace(",", " ").lower().split()` and compared via membership (`token in classes`). New validator rules that compare with `class_val == "explore"` work for the first authoring pass but fail the moment a real graph combines the role token with a routing/styling class.

## Canonical pattern
```python
class_tokens = (
    str(node.attrs.get("class", ""))
    .replace(",", " ")
    .lower()
    .split()
)
if "explore" in class_tokens or node.name.lower() == "explore":
    ...
```

## Pre-write checklist
1. `grep -rn 'node\.attrs\.get("<attr>"' runner/ bin/conformance` — enumerate every existing parser.
2. Copy the tokenization convention from the closest match (typically the parser).
3. Add a multi-token fixture to the regression suite before merging. Single-token fixtures alone hide the bug.

## Code origin (PR #130)
- Initial introducing commit `1cfb057` used `class_val == "explore"` (scalar).
- Codex P2 finding flagged this on the same commit.
- Fix commit `0fd3e2e` mirrored `runner/parser.py:_selector_matches` tokenization.
- Regression fixture: `tests/fixtures/level5_multi_class.dot` (covers both `class="codergen explore"` space-separated and `class="codergen,implement"` comma-separated).
- Regression test: `tests/test_conformance.py::test_level5_multi_class_role_attributes_pass`.

## Related
- [[AttributeError]] — runtime counterpart; this concept is about static validation.
- [[Codex]] — the cold-review bot that catches this pattern (self-review misses it because new rules are reviewed in isolation).
- [[RuntimeMirrorInstall]] — sister concept: ensure parse-then-validate consistency.
- Source: [Mirror existing attribute parsers (2026-06-28)](../sources/feedback-2026-06-28-mirror-attribute-parsers.md)
