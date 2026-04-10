---
title: "Test Fixtures"
type: concept
tags: [pytest, testing, fixtures, python]
sources: []
last_updated: 2026-04-08
---

## Description
Pytest fixtures that set up test state and provide resources to test functions. Use @pytest.fixture decorator.

## In This Source
Two key fixtures:
- `client()`: Flask test client with TESTING config
- `reset_mcp_client()`: Resets MCP client state between tests

## Fixture Pattern
```python
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client, app.app_context():
        yield client
```

## Connections
- [[FlaskTesting]] — uses client fixture
- [[Mocking]] — reset_mcp_client fixture for cleanup
