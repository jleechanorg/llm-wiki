---
title: "tRPC API Design"
type: concept
tags: [trpc, api, typescript, type-safety]
last_updated: 2026-04-14
---

## Summary

tRPC provides end-to-end type-safe APIs for TypeScript applications without requiring a schema definition file. Types flow from the server router directly to the client.

## Core Pattern

**Server router**:
```typescript
const appRouter = router({
  campaign: router({
    get: publicProcedure
      .input(z.object({ campaignId: z.string() }))
      .query(async ({ input }) => {
        return await db.campaign.findUnique(input);
      }),
    launch: publicProcedure
      .input(z.object({ campaignId: z.string() }))
      .mutation(async ({ input }) => {
        return await launchCampaign(input.campaignId);
      }),
  }),
});

export type AppRouter = typeof appRouter;
```

**Client usage**:
```typescript
const client = createTRPCClient<AppRouter>({
  url: '/api/trpc',
});

// Fully typed — no code generation needed
const campaign = await client.campaign.get.query({ campaignId: '123' });
await client.campaign.launch.mutate({ campaignId: '123' });
```

## Key Benefits

1. **No schema drift** — Server types always match client
2. **No codegen** — Types inferred directly
3. **Full autocomplete** — IDE knows exact input/output shapes
4. **Runtime validation** — Zod schemas validate at runtime

## Why It Matters for WorldAI

For the WorldAI UI, tRPC provides type-safe RPC between the frontend and Flask backend, eliminating the category of "API response shape doesn't match what frontend expects" bugs.

## Connections
- [[tRPCTypeSafety]] — tRPC type safety deep dive
- [[APIDesign]] — General API design
- [[TypeScriptBestPractices]] — TypeScript patterns
