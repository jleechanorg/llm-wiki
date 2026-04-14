# REV-pr5699-styleguide-convergence-pass

## ID
REV-pr5699-styleguide-convergence-pass

## Title
Converge light/fantasy major pages to styleguide and produce complete screenshot evidence

## Status
closed

## Type
bugfix

## Priority
high

## Created
2026-02-24

## Why
Visual review shows fantasy settings page is unthemed, logged-out fantasy has gutters, and planning-block readability regresses under fantasy during character creation. We need updated screenshots/videos for each major page to validate convergence.

## Scope
- Theme CSS and template wiring only (no UI component relocation)
- Major pages in both themes: logged-out landing, dashboard, new campaign, settings, game, post-character-creation
- Fresh screenshot/video evidence from smoke tests

## Acceptance
- Fantasy styling applies on settings page.
- Logged-out fantasy page no longer shows white gutters.
- Planning blocks/choice text remain readable in fantasy game flow.
- New screenshot set exists for every major page in both themes.

## Notes
- Keep layout/components in place; changes are visual only.

## Close Reason
- Fantasy settings now renders with theme tokens instead of light fallback.
- Logged-out fantasy no longer shows the prior white gutters.
- Planning block readability in fantasy is corrected (no inline light-mode backgrounds).
- Fresh full major-page screenshot sets were generated for both themes:
  - light: `run_1771899343`
  - fantasy: `run_1771899893`
- Compliance gate rerun passed with `overall_score: 98.5` at threshold `92`.
