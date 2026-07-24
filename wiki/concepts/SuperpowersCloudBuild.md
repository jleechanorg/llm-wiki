# SuperpowersCloudBuild

The remote coding-box service at `cloud.superpowers.build:22`, reached via SSH with the shared cloud-build key. Runs GLM-5.2 through its OWN internal proxy (`10.0.100.1:65500`) — NOT OpenRouter (so OpenRouter credit exhaustion does not affect the box). Box commits as `Cloud Build <supervisor@cloud-build.local>`.

## Enrollment
Both Mac and jeff-ubuntu are enrolled [[CloudBuildBastionHost|bastion hosts]] sharing one cloud-build SSH key. New machine = copy keypair + state.json + scripts from a sibling. See [[cloud-build-install-enrollment]].

## Constraints
- Git-secret guard rejects repos with secret-bearing ancestry → use [[CloudBuildOrphanSnapshotHandoff]].
- Work branch must be `private/*`.
- Heartbeat stale ≥240s = wedged → abort + fresh run.

## Dispatch entry
[[SuperCommand]] (`/super`) is the slash entry; `/superlight` is the legacy local router (NOT the box).

## Provenance
Confirmed 2026-07-19 via box identity-disclosure probes (memory `superpowers-cloud-build-orphan-snapshot`). First successful worldarchitect.ai dispatch 2026-07-19 (run `cb-wa-8353-...`, orphan-snapshot). jeff-ubuntu enrolled 2026-07-20 by copying Mac artifacts.
