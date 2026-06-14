---
name: ruff-comment-block-quoted-string-false-positive
description: "Ruff's \"commented-out code\" rule false-positives on quoted strings inside multi-line comment blocks (e.g. example UAs in"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7b99c2ed-d694-4f87-8f85-5ff965594f98
---

Ruff's "commented-out code" rule false-positives on quoted strings inside multi-line comment blocks.

Trigger pattern (FAILED in PR #7440 follow-up commit):
```python
# A real iPhone Safari UA like
# "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)"
# contains 10+ spaces ...
```

Ruff flagged the quoted line as commented-out code:
```
3938 |             # "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X)"
     |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
help: Remove commented-out code
```

**Fix**: rephrase the comment to avoid the quoted-string pattern. Drop the literal example and describe it abstractly:

```python
# A real iPhone Safari UA contains many spaces and would
# split the log line into ~13 tokens instead of 1, breaking
# `textPayload=~"cdiag_ua=..."` queries.
```

**Why**: This is the same class of error as pre-commit false positives. Encountering it during a hot Bugbot fix wastes a commit cycle. **How to apply**: when writing explanatory comments that include example values (UAs, JSON, log lines), use backticks `` ` `` or paraphrase to avoid double-quoted literals that ruff interprets as code.
