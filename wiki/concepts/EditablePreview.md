---
title: "EditablePreview"
type: concept
tags: [ui-pattern, interaction-design, forms]
sources: []
last_updated: 2026-04-08
---

## Description
A UI interaction pattern enabling inline editing of form fields directly within a preview or display context. Combines three behaviors:

1. **Click-to-Edit**: Clicking a field activates edit mode
2. **Click-Outside-to-Save**: Clicking outside the field persists changes
3. **Escape-to-Cancel**: Pressing Escape reverts to original values

## Use Cases
- Form previews that need inline editing without modal dialogs
- Live configuration editors where immediate feedback is valuable
- Non-destructive editing where cancel is one keystroke away

## Related Tests
- [[Campaign Wizard Editable Preview Tests]] — validates these behaviors in the campaign wizard context
