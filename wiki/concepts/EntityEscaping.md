---
title: "Entity Escaping"
type: concept
tags: [security, frontend, xss-prevention, html-encoding]
sources: ["frontend-structured-fields-tests-simple"]
last_updated: 2026-04-08
---

## Definition
Security practice of encoding HTML special characters to prevent cross-site scripting (XSS) attacks. The escapeHtml() function converts characters like <, >, &, " to their HTML entity equivalents.

## Usage in Structured Fields
All dynamic content (actor names, actions, descriptions, resource values) passes through escapeHtml() before being inserted into HTML output.

## Related Concepts
- [[Structured Fields Rendering]]
- [[XSS Prevention]]
