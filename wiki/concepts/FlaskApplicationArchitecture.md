---
title: "Flask Application Architecture"
type: concept
tags: [backend, python, flask, api]
sources: ["worldarchitect-ai-comprehensive-code-review-summary", "services-layer-architecture"]
last_updated: 2026-04-08
---

Backend web framework used for WorldArchitect.AI API. The main.py entry point contains approximately 985 lines defining Flask application setup and API routes.

## Key Components
- **main.py**: Flask application entry point and API routes (985 lines)
- **Service Layer**: Business logic abstraction between controllers and data access
- **Dependency Injection**: External dependencies injected for testability

## Best Practices Observed
- Single Responsibility per service
- Stateless operations between calls
- Structured logging with correlation IDs
- Comprehensive error handling
