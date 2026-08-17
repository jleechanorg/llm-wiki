---
name: firebase-admin-app-divergence-real-firestore-tests
description: "Service-integration glue bugs (multiple Firebase admin apps, divergent Firestore clients) cannot be caught by Layer 1 unit tests alone — pair with a Layer 2 E2E test that drives the tool through its real dispatch path."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fbc646c2-60a5-4592-bc94-d3b37adeb83e
  modified: 2026-08-15T20:30:14.427Z
---

Bead `rev-t6mtv` (WorldAI MCP `admin_download_campaign_entries` returned zero
entries) — the bug lived in the seam between two Firebase admin apps
(`firestore_service.get_db()` vs the dedicated
`worldai-tools-local-firestore` returned by `_get_firestore_db`). A pure
Layer 1 unit test that mocks both clients the same way **cannot** reproduce
this bug class.

**Why:** Two different admin apps pointing at the same Firestore project
*should* see the same data, but in practice they can diverge (init order,
credentials resolution, cache state). The bug only manifests in the gap
between the two clients; mocking both identically hides it.

**How to apply:** When fixing a bug whose root cause lives in service-integration
glue (multiple service identities, divergent clients, async boundaries, retry
coordination across boundaries):
1. **Layer 1 unit test** must mock the two clients **differently** (one sees
   the data, the other does not) to prove the code routes through the right
   client.
2. **Layer 2 E2E test** that drives the tool through its real dispatch path
   (JSON-RPC handler, Flask route, request lifecycle) is required to prove the
   wire layer still works.
3. Confirm RED by reverting the fix — if the regression tests don't fail
   without the fix, they don't actually catch the regression.

Reference: `mvp_site/tests/test_end2end/test_worldai_admin_download_entries_end2end.py`
and `mvp_site/tests/test_worldai_tools_mcp_proxy.py::test_download_entries_uses_canonical_db_when_proxy_db_sees_no_story`
were added together for this bug. Confirmed RED → GREEN cycle. See also
[[testing-layers-service-integration-glue]] (the matching skill update).