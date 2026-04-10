---
title: "Flask"
type: concept
tags: [framework, python, web-development]
sources: []
last_updated: 2026-04-08
---

## Summary
Flask is a lightweight WSGI web application framework in Python. It is designed to be simple and extensible, providing core web framework functionality while allowing developers to add extensions as needed.

## Key Characteristics
- **Micro-framework**: Minimal core with extension ecosystem
- **WSGI**: Uses the WSGI (Web Server Gateway Interface) standard
- **Routing**: URL route decorator-based routing (@app.route)
- **Templating**: Jinja2 template engine built-in

## Common Patterns
- `from flask import Flask` → Create app instance
- `app = Flask(__name__)` → Initialize Flask application
- `create_app()` → Factory function pattern for app creation (often used in larger applications)

## Connections
- [[TestDrivenDevelopment]] — Flask apps commonly tested using TDD
- [[FactoryPattern]] — create_app is a factory function pattern
- [[WebApplication]] — Flask is a web application framework
