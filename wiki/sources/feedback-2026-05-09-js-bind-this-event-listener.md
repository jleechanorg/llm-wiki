---
title: "JS .bind(this) Event Listener Anti-Pattern"
type: source
tags: [javascript, event-listener, memory-leak, worldarchitect, frontend]
date: 2026-05-09
source_file: raw/feedback_2026-05-09_js_bind_this_event_listener.md
---

## Summary

`addEventListener('click', this.handler.bind(this))` creates a new function reference each call, so `removeEventListener('click', this.handler.bind(this))` never matches. The event listener leaks silently — no error thrown, just growing listener count and memory. Found in PR #6841 (`mvp_site/frontend_v1/js/inline-editor.js`).

## Key Claims

- `.bind(this)` in addEventListener creates a new reference per call, breaking removeEventListener
- The leak is silent — no error, just growing listener count
- Fix: store bound reference as `this._boundHandler = this.handler.bind(this)` or use arrow function class property
- ESLint rule should flag `.bind(this)` inside addEventListener/removeEventListener pairs

## Key Quotes

> "addEventListener('click', this.handler.bind(this)) creates a new function reference each call. removeEventListener('click', this.handler.bind(this)) creates yet another new reference — it never matches the original." — PR #6841 analysis

## Connections

- [[EventListenerMemoryLeak]] — concept page
- [[InlineEditing]] — where it was found
- [[FrontendV1]] — affected codebase
