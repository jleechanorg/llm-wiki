# BD-styleguide-compliance-gate

## ID
BD-styleguide-compliance-gate

## Title
Add CI-enforced styleguide compliance gate for light/fantasy UI smoke evidence

## Status
closed

## Type
feature

## Priority
high

## Created
2026-02-23

## Why
Theme visuals are currently validated by manual screenshot review. This is slow, subjective, and regresses easily. We need an objective, repeatable gate that scores conformance to styleguide visuals without requiring UI layout/component changes.

## Scope
- `testing_ui/` visual smoke evidence outputs
- Compliance scorer (token checks + visual diff + contrast checks)
- GitHub Actions integration for PR blocking/reporting
- Baseline artifact storage and update workflow

## Acceptance
- CI runs both `testing_ui/test_smoke_light.py` and `testing_ui/test_smoke_fantasy.py`.
- Gate computes per-screen and per-theme compliance scores from:
  - computed style token checks,
  - masked perceptual diffs against baselines,
  - minimum contrast checks.
- Gate emits machine-readable report (`compliance_report.json`) and human report (markdown summary with linked artifacts).
- PR fails when score drops below configured threshold or critical checks fail.
- Baseline refresh is explicit (manual approval path), not implicit.

## Notes
- Dynamic regions (story text, timestamps, account-specific content) must be maskable to avoid false positives.
- Layout/component placement must remain excluded from scoring unless explicitly opted in later.

## Close Reason
Initial MVP landed:
- dual-theme visual smoke tests in `testing_ui/`
- compliance scorer (`testing_ui/visual_gate/run_compliance_gate.py`)
- CI gate workflow (`.github/workflows/styleguide-compliance-gate.yml`)
- design doc in `docs/styleguide-compliance-gate-design.md`
