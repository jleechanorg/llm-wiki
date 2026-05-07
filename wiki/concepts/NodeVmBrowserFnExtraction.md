# NodeVmBrowserFnExtraction

**Category**: Testing Pattern  
**First seen**: 2026-05-05 (worldarchitect.ai PR #6782)

## Problem

Browser JS functions declared with `const` inside a `DOMContentLoaded` closure cannot be accessed via `ctx.fnName` after `vm.runInContext`. Only `var` declarations hoist to the context object.

## Pattern

```js
// 1. Extract function source
const match = src.match(/const myFn = \([^)]*\) => \{[\s\S]*?\n  \};/);
// 2. Hoist via var rewrite
const ctx = vm.createContext({});
vm.runInContext(match[0].replace('const ', 'var '), ctx);
// 3. Inject mock DOM as ctx properties
ctx.mockEl = { getBoundingClientRect: () => ({ top: 300 }) };
// 4. Call via string eval — NOT ctx.myFn()
vm.runInContext('myFn(mockEl)', ctx);
```

## When to use

- Pure functions inside DOMContentLoaded closures in large browser JS files
- When loading the full file would require heavy DOM mocking (thousands of lines)
- TDD behavioral tests for geometry/scroll math, string transforms, DOM calculations

## References

- Source: [vm-extract-browser-fn-2026-05-05.md](../sources/vm-extract-browser-fn-2026-05-05.md)
- Bead: bd-spvv
