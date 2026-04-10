---
title: "Gender Consistency"
type: concept
tags: [narrative-generation, bug-fix, pronouns]
sources: []
last_updated: 2026-04-08
---

## Description
The principle that narrative generation must respect explicit gender fields when generating text about NPCs. Without gender enforcement, LLM-generated narratives could use incorrect pronouns (e.g., "he/him" for a female character) or mismatched names (e.g., "Eldrin" for a character created as "young woman").

## Solution
NPC gender field with explicit values ("female", "male", "non-binary", or creative values like "shapeshifter") enables narrative generation systems to deterministically select correct pronouns:
- female → she/her/hers
- male → he/him/his
- non-binary/other → they/them/their

## Related
- [[NPC]] — stores gender field
- [[NarrativeGeneration]] — must read gender field for pronoun consistency
- [[PronounMapping]] — concept mapping gender to pronouns
