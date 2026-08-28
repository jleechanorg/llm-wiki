---
name: Skill archive dependency and migration closure
description: Archive candidates must close active workflow dependencies, and home migration must be transactional and cross-platform verified.
type: feedback
bead: bd-7nx
---

# Skill archive dependency and migration closure

PR [#376](https://github.com/jleechanorg/jleechan-skills/pull/376) showed that historical zero-use is only an archive candidate filter. Active commands, skill contracts, policies, and tests must be scanned before archival; installed-home migration must preflight collisions and parents, serialize moves, avoid clobbering, verify exact source identity at the exact destination, roll back failures, release locks on interruption, and exercise both BSD/macOS and GNU/Linux semantics.

The final archive contains 110 skills and 7 commands. `/efficiency`, `/engplan`, and `/evidence-coverage` were retained because active skills invoke them. Real `~/.claude` has zero archived names under active discovery roots. The final suite passed 76 tests, exact-head CI passed at `66d26f6f9c0867ec0f2fe76a910d7f2dee3db385`, and the squash merge is `d3ce6fead25dc5bc906a62d67cb7e9a050784b02`.

