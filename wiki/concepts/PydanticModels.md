---
title: "Pydantic Models"
type: concept
tags: [python, pydantic, schema, validation, type-safety]
sources: [pydantic-schema-models-entity-tracking]
last_updated: 2026-04-08
---

## Definition
Pydantic is a Python library for data validation and settings management using Python type annotations. Models are defined as Python classes inheriting from `BaseModel` with field validation via decorators like `@field_validator`.

## Key Patterns
- **Field validation**: `@field_validator("field_name", mode="before")` for pre-processing
- **Model validation**: `@model_validator` for cross-field validation
- **Field constraints**: `Field(ge=X, le=Y)` for range validation
- **Config**: `model_config = ConfigDict(...)` for model-level settings

## Usage in WorldArchitect.AI
The entity schema uses Pydantic to enforce D&D stat ranges (1-30), convert defensive numeric values, and provide type-safe enums for entity classification.

## Related
- [[DefensiveNumericConverter]] — defensive value conversion for edge cases
- [[EntityTrackingSchema]] — application of Pydantic models to entity tracking
