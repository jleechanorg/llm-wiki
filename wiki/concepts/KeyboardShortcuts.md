---
title: "Keyboard Shortcuts"
type: concept
tags: [keyboard-accessibility, usability, interaction-pattern]
sources: ["inline-editor-component"]
last_updated: 2026-04-08
---

## Definition
Standard keyboard shortcuts in inline editing interfaces:
- **Enter**: Save current value and exit edit mode
- **Escape**: Cancel current edit and revert to original value

## Implementation
```javascript
handleKeydown(e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    this.save();
  } else if (e.key === 'Escape') {
    e.preventDefault();
    this.cancel();
  }
}
```

## Why It Matters
- Power users can edit faster without reaching mouse
- Follows common text editor conventions
- Reduces time to complete edit workflow

## Related Concepts
- [[ClickToEdit]] — the pattern this shortcuts support
- [[Accessibility]] — keyboard navigation support
