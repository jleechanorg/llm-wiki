---
name: PR 6841 Root Cause — .bind(this) Event Listener Leak from PR #1082
description: inline-editor.js .bind(this) in addEventListener silently breaks removeEventListener
type: feedback
bead: rev-98n8m
---

PR #6841: Click-outside listener in `inline-editor.js` was never removed because `.bind(this)` creates a new function reference each call. `removeEventListener('click', this.handleOutsideClick.bind(this))` creates a different reference than the one passed to `addEventListener`.

**Breaking PR**: #1082 (Migrate static to frontend_v1 from PR #1038). This PR migrated the `inline-editor.js` script and introduced the flawed event binding logic. The bug existed from day 1 of the V1 frontend but was only noticed when the campaign renaming feature was added.

**Lesson**: `.bind(this)` in `addEventListener`/`removeEventListener` pairs is ALWAYS a bug. It creates a silent memory leak that grows with each interaction cycle. The fix is either: (1) store the bound reference, (2) use arrow function class properties, or (3) use AbortController.

**How to apply**: ESLint rule (bead `rev-98n8m`) should flag any `.bind(this)` inside `addEventListener`/`removeEventListener` call pairs. Check all `mvp_site/frontend_v1/js/` files.

**Verification**: PR #6841 already has `testing_ui/test_ui_campaign_rename.py` (Layer 5 Browser test).
