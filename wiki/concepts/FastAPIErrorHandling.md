---
title: "FastAPI Error Handling"
type: concept
tags: [canonical, python, fastapi, error-handling, exceptions, types]
sources: [canonical-code-repos/fastapi]
last_updated: 2026-04-14
---

## Summary

FastAPI's error handling is the canonical example of typed, middleware-coordinated exception handling in Python. Exceptions are classes (not strings/codes), are handled by registered handlers, integrate with OpenAPI docs automatically, and flow through ASGI middleware. The pattern: define typed exceptions → register handlers → let them propagate. Every layer only catches what it understands.

## Key Patterns

### Typed Exception Hierarchy
```python
from fastapi.exceptions import (
    FastAPIError,        # base, shouldn't be raised directly
    RequestValidationError,  # from pydantic, 422
    WebSocketRequestValidationError,
)
from starlette.exceptions import HTTPException  # HTTP-level exceptions
```

Exceptions carry structured data. `RequestValidationError` contains the field-level validation errors. `HTTPException` carries status code + detail.

### Exception Handler Registration
```python
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    websocket_request_validation_exception_handler,
)

# Registered in FastAPI __init__
app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
```

Handlers are registered on the app, not scattered. One place to audit all error behavior.

### Context Manager for Resource Safety
```python
with sessions.Session() as session:  # ASGI exit stack pattern
    return session.request(method=method, url=url, **kwargs)
```

`AsyncExitStackMiddleware` coordinates cleanup across async layers. Resources are tied to request lifespan.

### ASGI Middleware Chain
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
```

Exception flow: code throws → ExceptionMiddleware catches → looks up registered handler → runs it → returns structured response. If no handler, returns 500.

## What This Means for Code Generation

Generated API code should:
1. Define typed exceptions per error type (not generic `Error(Exception)`)
2. Register handlers in one place (not catch/return in every function)
3. Use context managers for resource-bound code
4. Let exceptions propagate to the appropriate handler layer
5. Include OpenAPI documentation via exception handler behavior
