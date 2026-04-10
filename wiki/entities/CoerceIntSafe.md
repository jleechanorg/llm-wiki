---
title: "CoerceIntSafe"
type: entity
tags: [worldarchitect, utility, numeric-conversion]
sources: [campaign-divine-multiverse-upgrade-detection-logic]
last_updated: 2026-04-08
---
Numeric converter utility from mvp_site.numeric_converters that safely converts string values to integers with a default fallback. Used throughout upgrade detection to handle Firestore-persisted string representations.

## Usage
```python
from mvp_site.numeric_converters import coerce_int_safe as _coerce_int
divine_potential = _coerce_int(divine_potential_raw, 0)
```
