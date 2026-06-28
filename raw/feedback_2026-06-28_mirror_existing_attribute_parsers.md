---
name: mirror-existing-attribute-parsers
description: When adding a conformance/validator rule that reads a graph attribute (class, type, feature, ...), mirror the tokenization of every existing parser of that attribute — scalar equality on `class` falsely fails graphs that combine role + styling tokens.
bead: none
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5c957adc-ff57-4e2f-811a-331074aa6f70
---

## Lesson

Adding a new validator rule that reads a graph attribute is **not** a greenfield exercise. Real graphs tokenize attributes (`class="codergen explore"`, `class="codergen,implement"`, multi-line `feature` scripts, etc.), and a scalar `==` comparison silently produces false failures that only show up when a downstream graph lands with the multi-token form. The first review pass on PR #130 caught one such case — Codex cold-review flagged the multi-class issue **on the same commit** that introduced the rule. Without Codex the bug would have shipped.

## Why scalar comparison fails

DOT graph attributes are free-form strings. In dark-factory's parser convention (`runner/parser.py:_selector_matches`, line 223-230):

```python
def _selector_matches(selector: str, node: Node) -> bool:
    if selector == "*":
        return True
    if selector.startswith("."):
        token = selector[1:]
        classes = str(node.attrs.get("class", "")).replace(",", " ").split()
        return token in classes
    return selector == node.name
```

`class` is normalized as `str(...).replace(",", " ").lower().split()` and compared via `in` (membership). The new `bin/conformance:_check_level5` rule initially used `class_val == "explore"` — which is fine for the first authoring pass, but fails the moment a real graph combines the role token with a routing/styling class:

```dot
explore   [type="codergen", class="codergen explore",  prompt="@prompts/hello/explore.md"]
implement [type="codergen", class="codergen,implement", prompt="@prompts/hello/implement.md"]
```

Both cases would have triggered `missing_coding_role` errors despite the role token being present.

## How to apply — the mirror-attribute-parsers rule

Before writing any new rule that reads a graph attribute, do this **first**:

1. **Grep for every existing parser of that attribute** in `runner/` and `bin/conformance`:
   ```bash
   grep -rn 'node\.attrs\.get("class"\|"class".*split' runner/ bin/conformance
   ```
2. **Copy the tokenization convention verbatim** from the closest match (typically the parser).
3. **Test the new rule with multi-token fixtures** before merging — single-token fixtures alone hide the bug.

For `class` specifically, the canonical pattern is:

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

The same principle applies to other tokenizable attributes (`type` is currently single-token, but if multi-`type` ever becomes a thing, the same mirror rule applies).

## Verification

PR #130 fix commit `0fd3e2e`:
- `bin/conformance` lines 215-225: switched from `class_val == "explore"` to membership check using the mirrored tokenization.
- `tests/fixtures/level5_multi_class.dot`: new fixture that exercises both `class="codergen explore"` (space-separated) and `class="codergen,implement"` (comma-separated).
- `tests/test_conformance.py::test_level5_multi_class_role_attributes_pass`: regression test that fails on the pre-fix code and passes on the fix.
- Verified: `pytest tests/test_conformance.py -k level5` → 8/8 pass; `bin/conformance validate pipelines/factory/{level5_feature,gates,pr_gates}.dot` → 0 errors.

## References

- PR: https://github.com/jleechanorg/dark-factory/pull/130
- Merge commit on main: `e73e230`
- Head commit with fix: `0fd3e2e`
- Initial introducing commit: `1cfb057`
- Codex P2 finding on `bin/conformance:218`: review thread id `3488274002`, line `/bin/conformance:218`
- Existing parser reference: `runner/parser.py:_selector_matches` (line 223)
- Related (broader P0 default-graph contract): [[Dark-factory P0 default Level-5 graph contract]] in `~/roadmap/learnings-2026-06.md`

## Why Codex catches this but I don't

Codex reads the full repo and compares each rule to existing parsers of the same attribute. My self-review treats each new rule in isolation. The mirror-attribute-parsers rule above is the manual equivalent of what Codex does automatically — apply it pre-merge and the Codex finding class drops to near-zero.
