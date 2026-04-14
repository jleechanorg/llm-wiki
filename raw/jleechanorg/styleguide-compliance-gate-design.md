# Styleguide Compliance Gate Design

## Goal
Create a CI quality gate that enforces visual styleguide compliance for both supported themes (`light`, `fantasy`) using deterministic browser smoke artifacts.

This gate is visual-only:
- in scope: color/token consistency, themed surface treatment, readability/contrast
- out of scope: UI component movement, structural layout redesign

## Inputs
From existing smoke runs:
- `testing_ui/test_smoke_light.py`
- `testing_ui/test_smoke_fantasy.py`
- manifest files:
  - `/tmp/worldarchitectai/<branch>/ui_theme_smoke_light/run_<id>/manifest.json`
  - `/tmp/worldarchitectai/<branch>/ui_theme_smoke_fantasy/run_<id>/manifest.json`

Each manifest already includes:
- screen list + screenshot paths
- theme checks
- video + subtitle paths

## Single-Number Output
For each theme and each screen:
- `token_score` (0-100)
- `visual_score` (0-100)
- `contrast_score` (0-100)
- `screen_score = 0.45*token + 0.45*visual + 0.10*contrast`

Rollups:
- `theme_score = mean(screen_score)`
- `overall_score = min(theme_score_light, theme_score_fantasy)`

Gate policy:
- fail if `overall_score < 92`
- fail if any critical check fails:
  - wrong active theme (`data-theme`)
  - missing required screen
  - contrast below AA threshold for required text checks

## Architecture
Add a small scoring pipeline under `testing_ui/visual_gate/`:

1. `collect.py`
- reads both smoke manifests
- normalizes artifact paths
- validates required screens:
  - `01_logged_out_landing`
  - `02_dashboard`
  - `03_new_campaign`
  - `04_settings`
  - `05_game`
  - `06_game_post_character_creation`

2. `token_checks.js` (Playwright eval helper) or Python equivalent
- loads each captured page state and samples computed styles for canonical selectors
- compares against expected styleguide token map (per theme)
- examples:
  - body background gradient family
  - navbar background family
  - card/surface border color family
  - primary text/readability colors

3. `visual_diff.py`
- compares screenshots to approved baselines using perceptual diff (SSIM or pixelmatch-style thresholding)
- applies masks for dynamic regions:
  - story content blocks
  - timestamps
  - user email labels
- emits heatmaps for failures

4. `contrast_checks.py`
- samples required text/background pairs and calculates WCAG contrast
- required minimum: AA normal text where applicable

5. `report.py`
- outputs:
  - `compliance_report.json` (machine-readable)
  - `compliance_report.md` (PR-readable summary)

## Baseline Strategy
Store approved baselines in repo (or versioned artifact store):
- `testing_ui/visual_gate/baselines/light/*.png`
- `testing_ui/visual_gate/baselines/fantasy/*.png`
- `testing_ui/visual_gate/masks/<screen>.json`

Baseline update flow:
1. run smoke + scorer on candidate branch
2. open PR with baseline diffs and report
3. human approval required (no auto-baseline update in CI)

## CI Integration
Add job in GitHub Actions (e.g. `visual-stylegate`):

1. Run smoke tests:
- `./vpython testing_ui/test_smoke_light.py`
- `./vpython testing_ui/test_smoke_fantasy.py`

2. Run scorer:
- `./vpython testing_ui/visual_gate/run_compliance_gate.py`

3. Upload artifacts:
- screenshots, videos, manifests
- diff heatmaps
- compliance reports

4. Enforce fail/pass:
- non-zero exit when gate policy fails

## Report Schema (JSON)
```json
{
  "overall_score": 95.1,
  "threshold": 92.0,
  "pass": true,
  "themes": {
    "light": {
      "theme_score": 95.3,
      "screens": [
        {"name": "02_dashboard", "token_score": 96, "visual_score": 95, "contrast_score": 100, "screen_score": 95.6}
      ]
    },
    "fantasy": {
      "theme_score": 94.8,
      "screens": []
    }
  },
  "critical_failures": []
}
```

## Rollout Plan
Phase 1:
- run scorer in CI as non-blocking, publish report only

Phase 2:
- enforce critical checks only (theme correctness + required screens + contrast minimums)

Phase 3:
- enforce full threshold gate (`overall_score >= 92`)

## Risks and Mitigations
- Flake from dynamic content:
  - use stable test-mode user + masks + deterministic waits
- Baseline drift noise:
  - explicit/manual baseline updates only
- Overfitting to pixel-perfect snapshots:
  - token and contrast checks weighted alongside visual diffs

## Definition of Done
- CI job exists and runs on PRs touching frontend/theme files
- compliance report generated and attached to CI artifacts
- gate blocks regressions by policy
- baseline update process documented and usable by maintainers
