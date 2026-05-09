---
name: JS bind-this event listener anti-pattern
description: addEventListener with .bind(this) silently breaks removeEventListener
type: feedback
bead: rev-bindthis-eslint
---

`addEventListener('click', this.handler.bind(this))` creates a new function reference each call. `removeEventListener('click', this.handler.bind(this))` creates yet another new reference — it never matches the original. The event listener leaks silently.

**Found in**: PR #6841 (`mvp_site/frontend_v1/js/inline-editor.js`). Fix: store bound reference as `this._boundHandler = this.handler.bind(this)` or use arrow function class property.

**Why**: Silent leak — no error thrown, just growing listener count and memory. Hard to diagnose in production.

**How to apply**: Add ESLint rule flagging `.bind(this)` inside `addEventListener`/`removeEventListener` call pairs. Check all `mvp_site/frontend_v1/js/` files.
