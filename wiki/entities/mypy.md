---
title: "mypy"
type: entity
tags: [tool, type-checker, python]
sources: [python-typing-guide]
last_updated: 2026-04-08
---

mypy is a static type checker for Python that validates type annotations at compile-time. WorldArchitect.AI uses mypy with configuration in `mvp_site/mypy.ini` to enforce type safety across the codebase.

## Usage in WorldArchitect.AI
```bash
python -m mypy mvp_site --config-file mvp_site/mypy.ini
```

## Related
- [[PythonTypingGuide]] — typing guide documentation
- [[TypeStubs]] — required type stubs for Flask and Requests
