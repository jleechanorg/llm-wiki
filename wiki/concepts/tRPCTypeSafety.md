---
title: "tRPC Type Safety"
type: concept
tags: [canonical, typescript, trpc, type-safety, api-design]
sources: [canonical-code-repos/trpc]
last_updated: 2026-04-14
---

## Summary

tRPC achieves end-to-end type safety without code generation by sharing TypeScript types between server and client at runtime. The server's router type flows directly to the client — no OpenAPI, no schema files, no build step. If it type-checks, the API contract is valid. The key architectural move: the router is the type, and the client infers from it.

## Key Patterns

### Router as the Type
```typescript
// Server: define router with full type safety
const appRouter = router({
  getUser: publicProcedure.input(z.object({ id: z.string() })).query(({ input }) => {
    return db.user.findUnique({ where: { id: input.id } });
  }),
});

// Client: type flows from server — no code gen
const trpc = createTRPCProxyClient<AppRouter>(...);
// trpc.getUser({ id: "123" }) is fully typed, including error cases
```

The `AppRouter` type is the single source of truth. If the server changes the input schema, the client TypeScript breaks at compile time.

### Error Codes as Enum
```typescript
export class TRPCError extends Error {
  public readonly code: TRPC_ERROR_CODE_KEY;
  public override readonly cause?: Error;

  constructor(opts: { message?: string; code: TRPC_ERROR_CODE_KEY; cause?: unknown }) {
    super(message, { cause });
    this.code = opts.code;
  }
}
```

Structured errors with fixed error codes (`INTERNAL_SERVER_ERROR`, `NOT_FOUND`, `UNAUTHORIZED`) — not arbitrary strings.

### Middleware Chain
```typescript
const t = initTRPC.context<Context>().create();
const publicProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.user) throw new TRPCError({ code: 'UNAUTHORIZED' });
  return next({ ctx: { user: ctx.user } });
});
```

Middleware is composable and typed. Each middleware can add to the context (`ctx`) and the chain continues.

### Input/Output Validation at the Boundary
```typescript
publicProcedure.input(z.object({ id: z.string() })).query(({ input }) => {
  // input is { id: string } — validated by zod at the boundary
  // TypeScript knows it's string (not any) because zod parsed it
});
```

Zod schemas do double duty: runtime validation AND TypeScript type inference. No separate type declaration needed.

## What This Means for Code Generation

Generated TypeScript API code should:
1. Prefer type inference over explicit type annotations where possible
2. Use Zod (or similar) for input validation — it generates types automatically
3. Model errors as typed codes, not string messages
4. Build a router/procedure pattern where the type IS the API contract
5. Never use `any` — if you need dynamic shapes, use generics or discriminated unions
