---
title: "Event Listener Memory Leak (.bind(this) Anti-Pattern)"
type: concept
tags: [javascript, memory-leak, frontend, anti-pattern]
---

`addEventListener` with `.bind(this)` creates a new function reference per call. `removeEventListener` with `.bind(this)` creates yet another reference — it never matches. The listener leaks silently.

## Detection

ESLint rule: flag `.bind(this)` inside `addEventListener`/`removeEventListener` call pairs.

## Fix options

1. Store bound reference: `this._boundHandler = this.handler.bind(this)`
2. Arrow function class property: `handler = () => { ... }`
3. AbortController pattern: `controller = new AbortController(); addEventListener('click', handler, { signal: controller.signal }); controller.abort()`

## Found in

PR #6841 — `mvp_site/frontend_v1/js/inline-editor.js`

## Related

- [[InlineEditing]] — where discovered
- [[FrontendV1]] — affected codebase
- [[DOMManipulation]] — broader DOM event patterns
