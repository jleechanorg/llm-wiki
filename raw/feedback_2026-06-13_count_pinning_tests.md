---
name: count-pinning-tests-catch-silent-regressions-before-they-happen
description: "A test that asserts a count (e.g., \"9 codergen nodes, 3 per sprint\") fails the moment a structural change happens without a contract update. Cheaper than a process document, harder to skip than a comment."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When shipping a contract test for a multi-instance structure (e.g., one pipeline per sprint, one node per stage), also ship a count-pinning test that asserts the EXPECTED count of instances. The pattern is:

```python
def test_codergen_count_is_stable() -> None:
    g = parse(MY_PIPELINE)
    n = sum(1 for ... if node_type == "codergen")
    assert n == EXPECTED, "if you added an X, update the contract test too"
```

**Why**: A future maintainer who adds a 4th sprint (or 4th node) WITHOUT updating the timeout contract test will pass the contract test against the existing 3 sprints and silently miss the new one. The count-pinning test fails immediately, forcing an explicit decision: either add `timeout=600` to the new sprint's nodes (good), or relax the count test (and acknowledge the new sprint needs different treatment — also good). The cheapest way to force "new structure = new contract" without writing a process document.

**How to apply**:
1. Any time you ship a contract test for a multi-instance structure (per-sprint, per-stage, per-foo), add a count-pinning test alongside it.
2. The count-pinning test reads as documentation: "this is the expected count, and the count is the contract."
3. The test message should be a hint, not a lecture: "if you added a sprint, update the timeout contract test too" — tells the maintainer what to do, doesn't tell them why (the why is in the commit message and the contract test).

**Anti-pattern**: trusting that "if the contract test passes, the structure is right." Contract tests assert per-instance behavior; they don't assert that the right number of instances exist. A 4th instance with NO timeout will pass the contract test against the existing 3.

**When NOT to use**:
- Single-instance structures (one pipeline, one node, one config) — no count to pin.
- Structures where the count is supposed to grow over time (e.g., a test that asserts "≥1 codergen node" is fine; pinning to a specific number is too brittle).

**Related**: [[frozen-set-allow-list-as-contract]] — same idea at the type level. The allow-list asserts "these types are in scope"; the count-pinning test asserts "this many instances of these types exist." Both force deliberate updates when the structure changes.
