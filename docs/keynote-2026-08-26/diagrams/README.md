# Keynote diagram sources and renders

Backup created 2026-08-25 for the Agentic AI Summit LA keynote
(`1rGk2ZUIlJw3AkVJmJbdVB5OqAixR6M_xp7lc6lP2awA`).

## Why this exists

Until now the architecture diagram's source lived only in `/tmp`, and the
`tokens.css` it imported was already gone — deleted along with the directory it
was authored in. That was discovered the day before the talk, when a one-word
legend fix turned out to be unshippable: re-rendering would have produced a
diagram with every colour undefined. The fix shipped as a native text annotation
on the slide instead.

## Contents

| File | What it is |
|---|---|
| `keynote-real-26-architecture-v4.html` | **Current.** Two named Gemini flows (single call vs two calls) + SSE return path. This is what slide 14 renders from. |
| `keynote-real-26-architecture-v3.html` | Prior revision |
| `keynote-real-26-architecture-v2.html` | Prior revision |
| `tokens.css` | **Reconstructed** — see below |
| `renders/` | Every image in the live deck, pulled straight from the presentation |

The three HTML files were edited in one place only: `href="../tokens.css"` became
`href="./tokens.css"` so they resolve against the copy sitting beside them.

## About `tokens.css`

It is a reconstruction, not the original. Half the values were recovered by
sampling the live slide-14 render pixel by pixel — a histogram of the 1600×900
export, where `#f6f4ee` covers 187k sampled pixels, `#fdfcf9` 87k, and `#fdf0e3`
38k, which is what identifies them as canvas / card / proprietary-band rather
than incidental colour. `--accent` `#c9683a` and `--code` `#397b62` were taken as
the most-saturated orange and green with meaningful area. The remaining tokens
(`--ink-2`, `--ink-3`, `--rule`) are the values verified natively elsewhere in
the deck through `gog slides raw`.

## Re-rendering: what works and what doesn't

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --force-device-scale-factor=2 --window-size=1920,1200 \
  --screenshot=/tmp/v4.png "file://$PWD/keynote-real-26-architecture-v4.html"
```

**Verified working:** all boxes, all type, and the full palette resolve correctly
against the reconstructed tokens.

**Known broken:** the SVG connector arrows in `<svg class="connectors">` do not
draw at this viewport. They use raw user units (`M 404,52`) inside an SVG sized
`width:100%; height:100%`, so the original render width matters and it was not
recorded. The legend's inline arrows draw fine; only the body connectors are
affected.

**Therefore:** `renders/s14-architecture.png` is the authoritative artifact, not
a re-render. Treat the HTML as the editable source of truth for *content*, and
expect to re-derive the connector geometry if you ever need to regenerate the
image from scratch.
