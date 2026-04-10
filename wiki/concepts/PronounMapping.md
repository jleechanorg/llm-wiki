---
title: "Pronoun Mapping"
type: concept
tags: [narrative-generation, gender, nlp]
sources: []
last_updated: 2026-04-08
---

## Description
A helper concept that maps gender values to appropriate pronouns for narrative text generation. Ensures consistency between NPC gender field and generated pronouns in story text.

## Mapping Table
| Gender | Subject | Object | Possessive |
|--------|---------|--------|------------|
| female | she | her | her |
| male | he | him | his |
| non-binary | they | them | their |
| other (default) | they | them | their |

## Related
- [[GenderConsistency]] — principle requiring pronoun mapping
- [[NPC]] — provides gender field that drives mapping
- [[NarrativeGeneration]] — applies pronoun mapping to generated text
