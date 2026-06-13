---
title: "Ported Campaign"
type: concept
tags: [wiki, ingest, ttrpg, source-type]
date: 2026-06-13
---

## Summary
Wiki category for campaign sources ingested from external streams, podcasts, or transcripts (rather than authored in-world). The Voyage first dev playthrough is the inaugural entry in this category — a livestream transcript being preserved as a wiki source for future reference and analysis.

## Why "Ported"
The campaign was authored on the Voyage / Larion platform during a livestream, then ported to a markdown transcript (text), then ported into the wiki as a source page. Each step is a lossy format transformation; the goal is to preserve the original text and key narrative beats for future context.

## Ingest Pattern
1. Locate the original transcript
2. Reformat into Reddit-style sections (Setup → Beats → Highlights → System Notes → What's Next)
3. Preserve all original dialog verbatim in blockquotes
4. Tag as `ported-campaign` so future wiki tools can filter for it
5. Extract entities (NPCs, party members) and concepts (abilities, locations, platform features) as separate wiki pages

## Connections
- [[voyage-first-dev-playthrough-campaign]] — first ported campaign
- [[wiki-ingest]] — the workflow that produces ported campaigns
- [[voyage-platform]] — most ported campaigns will likely be Voyage / AI Dungeon transcripts
