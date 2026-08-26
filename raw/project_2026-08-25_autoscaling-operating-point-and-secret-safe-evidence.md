# Autoscaling operating points need stochastic evidence and secret-safe publication

WorldArchitect Cloud Run testing proved real concurrency-driven autoscaling,
but did not prove a deterministic trigger number. A clean target-171 trial
completed 2,185/2,185 terminals with concurrency recommending two instances,
CPU recommending one, and the fleet scaling 1 to 2. Five comparable
authenticated target-180 trials all reached two instances; their pooled
load-driver terminal error rate was 27/10,066 (0.268%), with two
concurrency-attributed and three unattributed scale events.

The operational decision was to use CPU8 / containerConcurrency180 /
Gunicorn180 as an aggressive dev learning profile while retaining 4 / 16 / 16
for production and previews because memory-heavy level-up traffic was not
tested.

The evidence branch had credential-bearing history, so the publication rule is
to rebuild a sanitized claim-scoped gist from primary data. The bundle must
include raw platform metrics, exact configuration, provenance classes, a
claim-to-artifact map, explicit non-claims, checksums, and a secret scan.

References:

- https://github.com/jleechanorg/worldarchitect.ai/pull/9330
- https://github.com/jleechanorg/worldarchitect.ai/commit/aa8400c345cad0280dccf6efc7723fe75c488588
- https://gist.github.com/jleechan2015/1be36c09f91141e4cd1f90931fb4d6f5
- Bead `rev-0eo4n`

