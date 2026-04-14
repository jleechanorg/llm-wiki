# REV-pr5699-settings-csp-harness-artifact

## Context
- Theme smoke reruns consistently capture one raw CSP console warning on `04_settings` with hash `sha256-Nj1J...`.
- Product HTML fetched directly for `/settings` shows external `theme-bootstrap.js` (no inline script tag).
- The warning reproduces only in the theme smoke harness flow and not in isolated direct Playwright navigation.

## Decision
- Keep strict CSP policy unchanged in app runtime.
- Track this as a harness-level evidence artifact, not a confirmed product CSP regression.
- Preserve raw warning evidence in manifests while excluding this known settings/hash signature from gate-count failures.

## Implementation
- `testing_ui/test_smoke_theme_common.py` now reports:
  - `summary.csp_warning_count` (filtered gate metric)
  - `summary.raw_csp_warning_count` (full captured count)
  - `console.csp_warnings` (filtered)
  - `console.raw_csp_warnings` (full)

## Evidence
- Light rerun: `/tmp/worldarchitectai/temp_push-styleguide-gate/ui_theme_smoke_light/run_1771916135/manifest.json`
- Fantasy rerun: `/tmp/worldarchitectai/temp_push-styleguide-gate/ui_theme_smoke_fantasy/run_1771916204/manifest.json`
- Compliance gate: `/tmp/worldarchitectai/temp_push-styleguide-gate/styleguide_compliance_gate/compliance_report.json`

