---
title: "Boolean Coercion"
type: concept
tags: [types, validation, sanitization]
sources: [simplified-structured-narrative-generation-schemas]
last_updated: 2026-04-08
---

Pattern for consistently converting truthy/falsey values to proper boolean type. Handles bool, str ("true"/"yes"/"1" → True, "false"/"no"/"0" → False), and numeric inputs.

Ensures validation and sanitization layers use identical boolean handling to prevent subtle bugs.

Related: [[InputValidationUtilities]]
