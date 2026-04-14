# BD-refs

## GOAL
Verify and, where needed, correct design-document references for runner reliability control-plane paths.

## MODIFICATION
- Re-reviewed `docs/ci/runner-reliability-control-plane-design.md` integration references.
- Confirmed workflow/script links resolve to existing files under repo root paths:
  - `../../.github/workflows/test.yml`
  - `../../scripts/ci-detect-changes.sh`
  - `../../scripts/ci/runner_preflight.sh`
  - `../../scripts/ci/classify_infra_failure.sh`

## NECESSITY
Accurate references are required so operational playbooks can be trusted during incident response and future migration.

## INTEGRATION PROOF
- Reference check executed and logged:
  - `python3` Markdown link validation on `docs/ci/runner-reliability-control-plane-design.md`
  - Confirmed all 4 tracked links resolve from file location.
