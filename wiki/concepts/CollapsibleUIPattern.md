---
title: "Collapsible UI Pattern"
type: concept
tags: [ui-pattern, javascript, accessibility, dom-manipulation]
sources: [shared-ui-utility-functions]
last_updated: 2026-04-08
---

## Definition
A UI pattern where content containers can be expanded or collapsed by user interaction, typically triggered by a toggle button. The state is managed through CSS classes (e.g., 'show') that control visibility.

## Key Aspects
- **Toggle Button**: Interactive element that triggers expand/collapse
- **State Management**: CSS class toggling (e.g., .show) controls visibility
- **Accessibility**: aria-expanded attribute communicates state to screen readers
- **Visual Feedback**: Icons update to reflect current state (chevron-up vs chevron-down)

## Implementation Pattern
```javascript
toggleButton.addEventListener('click', () => {
  const isExpanded = container.classList.contains('show');
  container.classList.toggle('show');
  toggleButton.setAttribute('aria-expanded', !isExpanded);
});
```

## Related Concepts
- [[JavaScriptUtilityModules]] — module export patterns
- [[AccessibilityInWebUI]] — ARIA attribute usage
