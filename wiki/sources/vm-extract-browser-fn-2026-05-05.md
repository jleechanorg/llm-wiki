# node:vm extraction pattern for closure-scoped browser JS functions

**Date**: 2026-05-05  
**Type**: Best Practice  
**Bead**: bd-spvv  
**Source**: worldarchitect.ai PR #6782 CR comment r3177473405

## Summary

`const` declared inside `vm.runInContext` is NOT accessible on the context object. To behaviorally test a function scoped inside a `DOMContentLoaded` closure:

1. Extract the function source via regex
2. Replace `const ` with `var ` in the extracted snippet
3. Run via `vm.runInContext(snippet, ctx)` — this hoists the binding onto ctx
4. Inject mock DOM objects as ctx properties
5. Call via string eval: `vm.runInContext('fnName(arg1, arg2)', ctx)` — do NOT call `ctx.fnName()` directly

## Code

```js
const fnMatch = appJsContent.match(
  /const scrollToEntryTop = \(entryEl, container\) => \{[\s\S]*?\n  \};/
);
const ctx = vm.createContext({});
vm.runInContext(fnMatch[0].replace('const ', 'var '), ctx);

ctx.entry = { getBoundingClientRect: () => ({ top: 300 }) };
ctx.container = { getBoundingClientRect: () => ({ top: 100 }), scrollTop: 200, scrollTo(opts) { captured = opts; } };
vm.runInContext('scrollToEntryTop(entry, container)', ctx);
// captured.top === 400  ✅
```

## References

- worldarchitect.ai PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6782
- Test file: `mvp_site/tests/frontend/test_app_js_structured_fields.js` tests 31-34
- Commit: `5edd8a87a`
