---
title: "Interface Mode Detection"
type: concept
tags: [ui, mode-switching, feature-flag]
sources: [enhanced-search-filter-milestone-4]
last_updated: 2026-04-08
---

## Description
Pattern for detecting and responding to interface mode changes (modern vs legacy). The EnhancedSearch class checks `interfaceManager.isModernMode()` and listens to `interfaceModeChanged` events to enable/disable functionality.

## Implementation
1. Check `window.interfaceManager.isModernMode()` on init
2. Add event listener for `interfaceModeChanged` custom event
3. Enable/disable feature based on mode

## Related Concepts
- [[ModernComponentStylesWithBootstrapCompatibility]] — modern mode styling
- [[FeatureFlag]] — control mechanism for optional features
