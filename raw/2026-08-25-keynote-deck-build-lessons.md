# Keynote deck build — two lessons (2026-08-25)

Source: session building the "Develop at Idea Velocity" keynote deck
(Google Slides `1rGk2ZUIlJw3AkVJmJbdVB5OqAixR6M_xp7lc6lP2awA`) for the
Agentic AI Summit LA talk.

## Lesson 1 — screenshot beats source reconstruction

An architecture diagram's HTML source lived only in `/tmp`, and its
`tokens.css` import was already gone by the time a legend fix was needed.
Reconstructed the palette by histogramming the live render pixel-by-pixel —
it worked, but the reconstruction lost the SVG connector-arrow geometry,
which was tied to an unrecorded original render viewport width.

The user's actual ask, given after seeing the reconstruction: "just
screenshot it." `gog slides export --format pdf` + `pdftoppm -png -r 150`
produced a 3000×1688 render with every connector arrow intact — strictly
higher fidelity than the reconstruction, for two commands.

Rule: when the goal is "back this up" (not "make this editable again"),
render/export the live output rather than reconstructing a lost source. A
render can't be wrong in the ways a reconstruction can (missing dependency,
drifted geometry, guessed values), because it's the artifact that already
shipped and was already verified.

## Lesson 2 — categorize against the source's own structure

Drafting a short conference-abstract summary, split six bullets into "dev
workflow" vs. "the AI RPG." Miscategorized three bullets — query-aware
routing, token-budget context design, call avoidance — under "dev workflow"
because they read like generic engineering-process concepts. They are
actually the AI RPG's own engine internals, living in the deck's own
"WorldAI, in depth" section, not the pipeline/Hermes/pyramid section that is
the actual dev workflow. The deck's own agenda slide, written earlier in the
same session, already had the correct boundary.

Rule: when categorizing content pulled from an existing structured source (a
deck's sections, a codebase's modules, a doc's own headings), verify each
item against that source's actual boundary before writing the summary — not
from how the content superficially reads. Surface topic-matching is a
hypothesis, not a classification.

## Where these landed

- `~/.claude/skills/slides/SKILL.md` — "Standing rules from the 2026-08-25
  keynote-build session"
- `~/.claude/skills/document-standards/SKILL.md` — lane 1, Truth & contract
- `~/roadmap/learnings-2026-08.md`
