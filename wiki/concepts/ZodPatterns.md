---
title: "Zod Patterns"
type: concept
tags: [canonical, typescript, zod, schema-validation, runtime-types]
sources: [canonical-code-repos/zod]
last_updated: 2026-04-14
---

## Summary

Zod provides TypeScript-first schema validation where schemas are also TypeScript types. The key insight: define validation logic once, and both runtime checks and type inference come for free. Zod bridges the gap between runtime validation and compile-time types without code generation.

## Key Patterns

### Schema as Type
```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(0).max(150),
  role: z.enum(['admin', 'user', 'guest']),
});

// TypeScript type inferred automatically
type User = z.infer<typeof UserSchema>;
// { id: string; email: string; age: number; role: 'admin' | 'user' | 'guest' }
```

Define once, get both validation and types. No separate type declaration needed.

### Refinement and Custom Checks
```typescript
const PasswordSchema = z.string()
  .min(8)
  .refine((pwd) => /[A-Z]/.test(pwd), {
    message: "Password must contain an uppercase letter",
  })
  .refine((pwd) => /[0-9]/.test(pwd), {
    message: "Password must contain a number",
  });
```

Chained refinements allow complex validation rules with custom error messages.

### Discriminated Unions
```typescript
const EventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
  z.object({ type: z.literal('scroll'), delta: z.number() }),
]);

// TypeScript knows exact shape based on 'type' field
type Event = z.infer<typeof EventSchema>;
```

Discriminated unions give exhaustive checking and precise types for each variant.

### ZodEffects for Transformation
```typescript
const DateSchema = z.string().transform((val) => new Date(val));

// Output type is Date, input is string
type TransformedDate = z.infer<typeof DateSchema>; // Date
```

Transform allows parsing and converting data while validating in a single pass.

### ZodError Handling
```typescript
const result = UserSchema.safeParse(data);

if (!result.success) {
  result.error.issues.forEach((issue) => {
    console.log(`Path: ${issue.path.join('.')}, Message: ${issue.message}`);
  });
}
```

ZodError provides detailed issue paths and messages for debugging validation failures.

### Composable Schemas
```typescript
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zip: z.string().regex(/^\d{5}$/),
});

const UserWithAddressSchema = UserSchema.extend({
  address: AddressSchema,
});

// Or merge
const FullUserSchema = UserSchema.merge(AddressSchema);
```

Schemas compose through `.extend()` and `.merge()` for building complex types from simpler ones.

## What This Means for Code Generation

Generated TypeScript validation code should:
1. Prefer Zod (or similar) over manual validation — schemas ARE types
2. Use `.transform()` for parsing/casting, not separate parse functions
3. Model discriminated unions for variant types — enables exhaustive checking
4. Chain `.refine()` for complex rules, not custom validators
5. Use `.safeParse()` for user input — returns result object, doesn't throw
6. Extract types with `z.infer<typeof Schema>` — single source of truth