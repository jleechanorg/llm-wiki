#!/usr/bin/env python3
"""
Campaign Entity Extractor — WorldArchitect.AI

Scans all entry pages for a campaign and creates entity pages for:
- Characters appearing in 3+ scenes
- Named locations from scene metadata
- Factions/organizations mentioned in 3+ scenes

Usage:
    python3 extract_campaign_entities.py --batch N --batch-index I    # parallel agent
    python3 extract_campaign_entities.py --campaign "aemon"         # single
    python3 extract_campaign_entities.py --dry-run                 # preview
"""

import argparse
import os
import re
import json
from pathlib import Path
from collections import defaultdict

WIKI_SOURCES = Path("/Users/jleechan/llm_wiki/wiki/sources")
WIKI_ENTITIES = Path("/Users/jleechan/llm_wiki/wiki/entities")
WIKI_CONCEPTS = Path("/Users/jleechan/llm_wiki/wiki/concepts")


def get_campaign_slugs() -> list[str]:
    """Get all campaign slugs that have entry pages."""
    slugs = set()
    for f in WIKI_SOURCES.glob("*-entry-*.md"):
        m = re.match(r"(.+)-entry-\d+\.md", f.name)
        if m:
            slugs.add(m.group(1))
    return sorted(slugs)


def extract_from_entry(entry_path: Path) -> dict:
    """Extract entities from a single entry page."""
    with open(entry_path) as f:
        content = f.read()

    result = {
        'characters': [],
        'locations': [],
        'factions': []
    }

    # Pull from Key Details section
    key_match = re.search(r"## Key Details\n(.*?)(?:---\n|\Z)", content, re.DOTALL)
    if key_match:
        details = key_match.group(1)

        char_m = re.search(r"Character:\s*(.+?)(?:\n|$)", details)
        if char_m:
            name = char_m.group(1).strip()
            if name and len(name) > 1:
                # Strip title prefixes
                cleaned = re.sub(r'^(Lord|Lady|Ser|Sir|Dame|Prince|Princess|King|Queen|Duke|Duchess|The)\s+', '', name, flags=re.IGNORECASE).strip()
                if cleaned:
                    result['characters'].append(cleaned.title())

        loc_m = re.search(r"Location:\s*(.+?)(?:\n|$)", details)
        if loc_m:
            loc = loc_m.group(1).strip()
            # Clean: remove "Location:" prefix, take first meaningful segment
            loc = re.sub(r'^Location:\s*', '', loc, flags=re.IGNORECASE).strip()
            if loc and len(loc) > 2:
                result['locations'].append(loc)

    # Pull faction-like names from full content
    # Patterns: "House X", "The X Clan/Crew/Guild", "X Kingdom"
    faction_matches = re.findall(
        r'\b(House\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b',
        content
    )
    faction_matches += re.findall(
        r'\b(The\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(Clan|Crew|Guild|Faction|Empire|Kingdom|Republic|Order|Host)\b',
        content
    )
    faction_matches += re.findall(
        r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(Clan|Crew|Guild|Faction|Empire|Kingdom|Republic|Order|Host|Circle)\b',
        content
    )
    # Deduplicate and flatten
    for fm in faction_matches:
        if isinstance(fm, str):
            result['factions'].append(fm.strip())
        else:
            # tuple from the combined pattern - take first group
            result['factions'].append(fm[0].strip())

    return result


def score_campaign(campaign_slug: str) -> dict:
    """Aggregate mentions across all entry pages."""
    entry_files = sorted(WIKI_SOURCES.glob(f"{campaign_slug}-entry-*.md"))

    char_counts = defaultdict(int)
    loc_counts = defaultdict(int)
    faction_counts = defaultdict(int)

    for ef in entry_files:
        e = extract_from_entry(ef)

        for c in e['characters']:
            if c and len(c) > 1:
                char_counts[c] += 1

        for loc in e['locations']:
            if loc and len(loc) > 2:
                # Skip very long strings (probably garbage)
                if len(loc) < 60:
                    loc_counts[loc] += 1

        for f in e['factions']:
            if f and len(f) > 2 and len(f) < 50:
                faction_counts[f] += 1

    return {
        'characters': {k: v for k, v in char_counts.items() if v >= 3},
        'locations': {k: v for k, v in loc_counts.items() if v >= 3},
        'factions': {k: v for k, v in faction_counts.items() if v >= 3},
        'total_scenes': len(entry_files)
    }


def entity_page(name: str, etype: str, campaign: str, appearances: int, total: int, desc: str = "") -> str:
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', name.lower()).strip('-')
    return f"""---
title: "{name}"
type: entity
tags: [{campaign}, {etype}]
sources: [{campaign}]
last_updated: 2026-04-12
appearances: {appearances}
total_scenes: {total}
---

## Overview

{name} appears in {appearances} scenes across the [[{campaign}]] campaign.

## Description

{desc or f"{name} is an entity from the {campaign} campaign."}

## References
- [[{campaign}]] — campaign overview
- [[{campaign}-campaign]]

""", slug


def process_campaign(slug: str, dry_run: bool = False) -> dict:
    scores = score_campaign(slug)

    manifest = {
        'slug': slug,
        'total_scenes': scores['total_scenes'],
        'created': {'entities': [], 'concepts': []}
    }

    for char, cnt in scores['characters'].items():
        content, pslug = entity_page(char, 'character', slug, cnt, scores['total_scenes'])
        path = WIKI_ENTITIES / f"{pslug}.md"
        if dry_run:
            print(f"  char: {pslug} ({cnt} scenes)")
        else:
            with open(path, 'w') as f:
                f.write(content)
            manifest['created']['entities'].append({'name': char, 'slug': pslug, 'type': 'character'})

    for loc, cnt in scores['locations'].items():
        content, pslug = entity_page(loc, 'location', slug, cnt, scores['total_scenes'])
        path = WIKI_ENTITIES / f"{pslug}.md"
        if dry_run:
            print(f"  loc: {pslug} ({cnt} scenes)")
        else:
            with open(path, 'w') as f:
                f.write(content)
            manifest['created']['entities'].append({'name': loc, 'slug': pslug, 'type': 'location'})

    for fact, cnt in scores['factions'].items():
        content, pslug = entity_page(fact, 'faction', slug, cnt, scores['total_scenes'])
        path = WIKI_ENTITIES / f"{pslug}.md"
        if dry_run:
            print(f"  fact: {pslug} ({cnt} scenes)")
        else:
            with open(path, 'w') as f:
                f.write(content)
            manifest['created']['entities'].append({'name': fact, 'slug': pslug, 'type': 'faction'})

    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--campaign', type=str, help='Filter by slug substring')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--manifest', action='store_true')
    parser.add_argument('--batch', type=int, help='Number per batch')
    parser.add_argument('--batch-index', type=int, help='0-indexed batch number')
    args = parser.parse_args()

    slugs = get_campaign_slugs()

    if args.campaign:
        slugs = [s for s in slugs if args.campaign.lower() in s.lower()]

    if args.batch and args.batch_index is not None:
        batch_size = args.batch
        start = args.batch_index * batch_size
        slugs = slugs[start:start + batch_size]
        print(f"Batch {args.batch_index}: processing {len(slugs)} campaigns")

    print(f"Found {len(slugs)} campaigns, processing {len(slugs)}")

    manifest_entries = []
    for slug in slugs:
        print(f"\nProcessing: {slug}")
        entry = process_campaign(slug, dry_run=args.dry_run)
        entities = len(entry['created']['entities'])
        concepts = len(entry['created']['concepts'])
        print(f"  created {entities} entities, {concepts} concepts")
        manifest_entries.append(entry)

    if args.manifest and not args.dry_run:
        mf = Path("/tmp/entity_extraction_manifest.jsonl")
        with open(mf, 'w') as f:
            for e in manifest_entries:
                f.write(json.dumps(e) + '\n')
        print(f"\nManifest: {mf}")

    total = sum(len(e['created']['entities']) for e in manifest_entries)
    print(f"\n=== {len(slugs)} campaigns, {total} total entities created ===")


if __name__ == '__main__':
    main()