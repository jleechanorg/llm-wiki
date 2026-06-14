---
name: local-port-env-contaminates-ci-tests
description: Running local dev server (PORT=9130) contaminates test_gunicorn_config.py — use PORT=8080 to match CI
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 7fb93c82-6491-4f2c-9a75-6a996471316c
---

## Local PORT env var causes false test failures

### The Pattern

`test_gunicorn_config.py::test_bind_address_is_cloud_run_compatible` asserts gunicorn binds to `0.0.0.0:8080`. When a local dev server is running on port 9130, the `PORT=9130` env var leaks into the test process and the test fails:

```
AssertionError: '0.0.0.0:9130' != '0.0.0.0:8080'
```

This looks like a real failure but is purely an env-contamination artifact.

### Solution

Run with `PORT=8080` (or unset PORT) to match CI:

```bash
TESTING=true PORT=8080 MOCK_SERVICES_MODE=true ... ./run_tests.sh --test-dirs=mvp_site ...
```

In CI, the self-hosted runner has PORT=8080, so this test passes. Locally with a dev server running, PORT is set to whatever port the server bound to (9130 in this case).

### How to Apply

Before reporting a local test failure, check if the test involves port/bind config and whether a dev server is running. If `ps aux | grep flask` shows a server on a non-8080 port, set `PORT=8080` in the test run command.

**Affected test**: `mvp_site/tests/test_gunicorn_config.py::TestGunicornConfiguration::test_bind_address_is_cloud_run_compatible`

### Also Pre-existing

`test_agent_architecture_end2end.py` (god mode rewards_box guard) and `test_shared_cache_probe.py` (probe errors) are pre-existing failures unrelated to the BQ logging PR. Confirmed: neither file was modified in PR #7439 (`git diff origin/main..HEAD` shows no diff).

### References

- PR [#7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439) — BQ forensic logging merged 2026-06-12
- Discovered during local CI verification before merge
