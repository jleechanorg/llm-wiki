# REV: PR #5699 landing/theme goal alignment

## Context
- PR goal: implement Arcane Scholar visuals from styleguide.
- Constraint: do not move UI components or change placement.
- Issue observed: fantasy logged-out CSS introduced full-bleed breakout and hid the existing splash section, causing layout drift from existing UI structure.

## Fix applied
- Kept existing logged-out/auth layout structure intact.
- Removed fantasy-specific login rules that changed geometry/placement.
- Retained Arcane Scholar visual tokens (gradients, frosted surfaces, color system).
- Scoped theme menu event listener to dropdown container to reduce global click side effects.

## Remaining follow-up
- Optional: add a focused UI test for logged-out landing under `data-theme='fantasy'` to prevent future layout regressions.

## Priority
- Medium (visual regression and PR-goal drift).
