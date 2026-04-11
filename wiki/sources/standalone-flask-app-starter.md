---
title: "Standalone Flask App Starter"
type: source
tags: [flask, testing, smoke-test, python, web-server]
source_file: "raw/standalone-flask-app-starter.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Standalone Flask application starter script that resolves import path issues when running in subshells. Used as part of smoke test PR workflow to verify the application can start correctly.

## Key Claims
- **Import Path Resolution**: Adds current directory to Python path to resolve module import issues in subshell execution
- **Environment Configuration**: Supports PORT and FLASK_DEBUG environment variables for deployment flexibility
- **Smoke Test Integration**: Part of the /smoke workflow for verifying application startup

## Key Code Patterns
```python
sys.path.insert(0, os.path.dirname(__file__))
from main import app
app.run(host="0.0.0.0", port=port, debug=debug)
```

## Connections
- [[MainModule]] — references the main Flask application module
- [[SmokeTestWorkflow]] — part of smoke test verification process
