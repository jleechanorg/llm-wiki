---
name: Testing closure-scoped browser JS functions with node:vm regex extraction
description: Extract a const function from DOMContentLoaded closure via regex, rewrite to var, run in vm.createContext with mock DOM stubs
type: feedback
bead: bd-spvv
originSessionId: dd013bfe-dbfb-4960-93a3-7e5320cb3f47
---
## Context

PR [#6782](https://github.com/jleechanorg/worldarchitect.ai/pull/6782) renamed `scrollToBottom` to `scrollToEntryTop` in `mvp_site/frontend_v1/app.js`. The function lives inside a `document.addEventListener('DOMContentLoaded', () => { ... })` closure, making it invisible to simple `vm.runInContext` loads of the full file. We needed behavioral unit tests that actually invoke the function with mock DOM geometry.

## Technical detail

The function signature:
```js
const scrollToEntryTop = (entryEl, container) => {
  if (!entryEl || !container) return;
  const relTop = entryEl.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop;
  container.scrollTo({ top: relTop, behavior: 'instant' });
};
```

`const` inside a `vm.runInContext` call does NOT expose the binding on the context object. `var` does. The extraction pattern:

```js
const fnMatch = appJsContent.match(
  /const scrollToEntryTop = \(entryEl, container\) => \{[\s\S]*?\n  \};/
);
const ctx = vm.createContext({});
vm.runInContext(fnMatch[0].replace('const ', 'var '), ctx);
// now ctx has no scrollToEntryTop property — pass mock args via context props:
ctx.entry = { getBoundingClientRect: () => ({ top: 300 }) };
ctx.container = { getBoundingClientRect: () => ({ top: 100 }), scrollTop: 200, scrollTo(opts) { captured = opts; } };
vm.runInContext('scrollToEntryTop(entry, container)', ctx);
// captured.top === 400  ✅
```

## Solution / rule

**When a pure function is closure-scoped inside a browser event listener:**
1. Extract its source text via regex (match from `const fnName =` to closing `};`)
2. Replace leading `const ` with `var ` in the extracted snippet
3. `vm.runInContext(snippet, ctx)` — this hoists `scrollToEntryTop` as a var on ctx
4. Inject mock DOM objects as ctx properties, then call via `vm.runInContext('fnName(arg1, arg2)', ctx)`
5. Do NOT try `ctx.scrollToEntryTop(...)` directly — it is undefined; use the string eval form

## Verification

Tests 31-34 committed at `5edd8a87a` on `fix/scroll-entry-to-top`, 39/39 pass:
- Test 31: relTop = 300 − 100 + 200 = 400 ✅
- Test 32: behavior:'instant' ✅
- Test 33: null entryEl → no-op ✅
- Test 34: entry at container top → scrollTo(0) ✅

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6782
- CR comment: https://github.com/jleechanorg/worldarchitect.ai/pull/6782/files#r3177473405
- Test file: `mvp_site/tests/frontend/test_app_js_structured_fields.js` (tests 31-34)
- Fix commit: `93d6574be` (worldarchitect.ai)
- Test commit: `5edd8a87a` (worldarchitect.ai)

## Reusable pattern

```js
// Generic: extract and behaviorally test any closure-scoped browser function
function extractAndTest(sourceText, fnName, arrowArity) {
  const pattern = new RegExp(
    `const ${fnName} = \\([^)]*\\) => \\{[\\s\\S]*?\\n  \\};`
  );
  const match = sourceText.match(pattern);
  if (!match) throw new Error(`${fnName} not found`);
  const ctx = vm.createContext({});
  vm.runInContext(match[0].replace('const ', 'var '), ctx);
  return (mockArgs) => {
    Object.assign(ctx, mockArgs);
    const callArgs = Object.keys(mockArgs).join(', ');
    return vm.runInContext(`${fnName}(${callArgs})`, ctx);
  };
}
```
