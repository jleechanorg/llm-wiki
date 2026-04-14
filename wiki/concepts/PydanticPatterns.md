---
title: "Pydantic Patterns"
type: concept
tags: [canonical, python, pydantic, type-safety, validation]
sources: [canonical-code-repos/pydantic]
last_updated: 2026-04-14
---

## Summary

Pydantic v2 is the canonical reference for runtime type validation in Python. Its core insight: define data structures with Python type annotations, and Pydantic handles validation, coercion, serialization, and error reporting automatically. Every `BaseModel` subclass is a self-validating, self-documenting data contract. The error model — structured `ValidationError` with per-field detail — is the gold standard for API input validation.

## Key Patterns

### BaseModel as Self-Validating Contract
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None

# Validation happens at construction — invalid data raises ValidationError
user = User(id=1, name="Alice", email="alice@example.com")
```

`BaseModel` provides `__pydantic_fields__` (field registry), `__pydantic_validator__` (validation logic), and `model_config: ClassVar[ConfigDict]` (class-level settings). Construction validates; errors are structured.

### Field Constraints
```python
from pydantic import Field, EmailStr

class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(description="User email address")
    age: int = Field(ge=0, le=150, default=0)
    website: EmailStr | None = None
```

`Field()` is the canonical way to express constraints: `ge`/`gt`/`le`/`lt` for numeric bounds, `min_length`/`max_length` for strings, `pattern` for regex, `description` for docs. Constraints are declarative alongside the type.

### Field Validators
```python
from pydantic import field_validator

class User(BaseModel):
    name: str
    email: str

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        if not v.islower():
            raise ValueError('email must be lowercase')
        return v.lower()
```

Field validators run per-field after raw type coercion. Multiple validators can stack on the same field. The `@classmethod` pattern gives access to the model class for cross-field checks.

### Model Validators
```python
from pydantic import model_validator

class Signup(BaseModel):
    password: str
    confirm: str

    @model_validator(mode='after')
    def passwords_match(self) -> 'Signup':
        if self.password != self.confirm:
            raise ValueError('passwords do not match')
        return self
```

Model validators run after all fields are validated. `mode='before'` handles raw dict input; `mode='after'` works on the coerced model. Essential for cross-field constraints.

### ConfigDict
```python
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        frozen=True,           # immutable instances
        extra='forbid',         # reject unknown fields
        str_strip_whitespace=True,
        populate_by_name=True,  # allow alias or field name
    )
```

Configuration is a typed dict on the class, not constructor kwargs. Key settings: `frozen` (immutability), `extra` (allow/forbid/ignore unknown fields), `str_strip_whitespace`, `populate_by_name`.

### Structured ValidationError
```python
from pydantic import ValidationError

try:
    User(id="not-an-int", name="")
except ValidationError as e:
    for err in e.errors():
        print(err['loc'], err['msg'], err['type'])
    # ('id',) "Input should be a valid integer" int_type
    # ('name',) 'String should have at least 1 character' string_too_short
```

`ValidationError` is the canonical structured error type. Each error has `loc` (field path as tuple), `msg` (human-readable), `type` (machine-readable slug), and `input` (the offending value). This structure is what FastAPI's `RequestValidationError` wraps for HTTP 422 responses.

### Discriminated Unions
```python
from pydantic import Discriminator, Field
from typing import Union

class Cat(BaseModel):
    pet_type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    pet_type: Literal["dog"]
    bark_volume: int

Pet = Union[Cat, Dog]

class Zoo(BaseModel):
    pet: Annotated[Pet, Discriminator('pet_type')]
```

Discriminated unions use a literal field as the discriminator. Pydantic validates the discriminator first, then only attempts to validate against the matching variant. Eliminates ambiguous union errors.

### Serialization Control
```python
class User(BaseModel):
    password_hash: str

    def to_summary(self) -> dict:
        return self.model_dump(exclude={'password_hash'})

# Or at the model level:
class Config:
    json_schema_extra = {"exclude": {"password_hash"}}
```

`model_dump()` (v2) / `dict()` (v1 compat) with `exclude_unset=True`, `exclude_defaults=True`, or explicit `exclude={'field'}` sets. Serialization is explicit and controllable at call site.

### Frozen Immutability
```python
class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

config = Config(host="api.example.com", port=443)
config.host = "other.example.com"  # raises ValidationError: frozen_instance
```

`frozen=True` makes the entire instance immutable after construction. Useful for configuration objects, constants, and value objects where identity should be stable.

## Connections

- [[FastAPIErrorHandling]] — FastAPI uses Pydantic's `BaseModel` and `ValidationError` as its input/output backbone. `RequestValidationError` is a FastAPI wrapper around Pydantic's `ValidationError`.
- [[RequestsAPIDesign]] — Both Pydantic and Requests share the "explicit params, clear contracts" philosophy. Pydantic makes those contracts machine-checkable.
- [[APIResponseValidation]] — Pydantic's `model_validate()` is the canonical pattern for validating API responses.

## What This Means for Code Generation

Generated code should:
1. Use `BaseModel` subclasses for all structured input/output — never raw `dict` or `TypedDict` for external data
2. Express constraints in `Field()` declarations, not ad-hoc validation functions
3. Raise `ValidationError` (not generic `ValueError`) for validation failures
4. Use `model_validator` for cross-field constraints — avoid scattered `@field_validator` doing the same job
5. Treat `ConfigDict(frozen=True)` as the default for configuration/data-transfer objects
6. Return structured `ValidationError.errors()` results, not string messages, for API error responses
