---
title: "Lazy Loading"
type: concept
tags: [python, import, performance, optimization]
sources: [startup-import-lazy-loading-tests]
last_updated: 2026-04-08
---

## Definition
A design pattern where module loading is deferred until first use. In Python, `importlib.util.LazyLoader` registers modules in `sys.modules` immediately but defers body execution until first attribute access.

## How It Works
1. **Registration**: LazyLoader adds module to `sys.modules` right away
2. **Deferral**: Module body (including transitive imports) only runs on first attribute access (`module.__spec__.loader` triggers exec)
3. **Cold Start**: Heavy dependencies like `google.genai` or `google.cloud.firestore` never load if never accessed

## Use Cases
- **Web services**: Keep cloud SDKs out of startup path for faster cold starts
- **CLI tools**: Defer optional feature imports until needed
- **Plugin systems**: Load plugins on-demand

## Wiki Connections
- Tested by [[StartupImportLazyLoadingTests]]
- Related to [[ColdStartOptimization]]
- Enables [[ImportPerformance]] improvements
