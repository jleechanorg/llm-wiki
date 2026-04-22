# Fork Plugin Refactor Design

## Executive Summary

The fork (jleechanorg/agent-orchestrator) has accumulated ~3,739 lines of changes in `lifecycle-manager.ts`, ~2,079 lines in `scm-github/src/index.ts`, and ~106 lines in `spawn.ts`. These changes create merge conflicts on every upstream import. This document designs a plugin-based refactor that pushes fork-specific behavior into plugins, keeping the fork's core as close to upstream as possible.

**Goal**: Reduce merge conflicts from ~2,000+ lines per import to under 100 lines (plugin registration only).

---

## 1. Current Divergence Analysis

### 1.1 `lifecycle-manager.ts` (fork: 3,032 LOC vs upstream: 2,077 LOC)

| Fork Addition | Type | Plugin Candidate? |
|---|---|---|
| `lastSkepticSha` tracking | Fork-specific | YES → `lifecycle-skeptic` |
| `lastSkepticCommentId` tracking | Fork-specific | YES → `lifecycle-skeptic` |
| `runSkepticReviewReaction` import | Fork-specific | YES → `lifecycle-skeptic` |
| `runLocalSkepticCron` import | Fork-specific | YES → `lifecycle-skeptic-cron` |
| `agento` prefix tagging | Fork-specific | YES → `lifecycle-agento-prefix` |
| `skeptic-review` reaction handler | Fork-specific | YES → `lifecycle-skeptic` |
| `skeptic-cr-approval-trigger` block | Fork-specific | YES → `lifecycle-skeptic` |
| `skeptic-first-seen-dispatch` block | Fork-specific | YES → `lifecycle-skeptic` |
| `claim-verification` reaction | Fork-specific | YES → `lifecycle-claim-verification` |
| `lifecycle-skeptic-cron` polling | Fork-specific | YES → `lifecycle-skeptic-cron` |
| `logAoAction` calls throughout | Fork-specific | YES → `lifecycle-ao-action-log` |
| `useSessionEvents` closure | Fork-specific | YES → `lifecycle-session-events` |
| `dedup-head-sha-store` integration | Fork-specific | YES → `lifecycle-head-sha-dedup` |
| MCP mail integration | Fork-specific | YES → `lifecycle-mcp-mail` |
| PR enrichment batching (upstream) | Upstream | Keep in core |

**Key insight**: The fork's `lifecycle-manager.ts` is ~1,000 LOC larger than upstream, but virtually all of that is either:
- Skeptic integration (~500 LOC)
- AO action logging (~200 LOC)
- Session event tracking (~200 LOC)
- MCP mail (~100 LOC)

### 1.2 `scm-github/src/index.ts` (fork: 2,924 LOC vs upstream: 1,065 LOC)

| Fork Addition | Type | Plugin Candidate? |
|---|---|---|
| GraphQL-based `detectPR()` with REST fallback | Fork-specific | YES → `scm-github-graphql` |
| `getSkepticComments()` method | Fork-specific | YES → `scm-github-skeptic` |
| `getReviews()` GraphQL enhancement | Fork-specific | Partial → keep in SCM |
| `getPendingComments()` GraphQL | Fork-specific | YES → `scm-github-comments` |
| `getAutomatedComments()` GraphQL | Fork-specific | YES → `scm-github-comments` |
| Rate limit handling (`isRateLimitError`) | Fork-specific | YES → `scm-github-rate-limit` |
| Bot author set (DEFAULT_BOT_AUTHORS) | Fork-specific | YES → `scm-github-bot-filter` |
| `enrichSessionsPRBatch` batch enrichment | Fork-specific | YES → `scm-github-batch` |
| Review backlog throttling | Fork-specific | YES → `scm-github-comments` |
| MCP mail comment methods | Fork-specific | YES → `scm-github-mail` |

**Key insight**: Fork's SCM is 2.7x larger than upstream because it adds:
- GraphQL queries (~400 LOC)
- Skeptic comment retrieval (~150 LOC)
- Comment enrichment with throttling (~300 LOC)
- Batch PR enrichment (~200 LOC)
- Extended bot filtering (~100 LOC)

### 1.3 `spawn.ts` (fork: 490 LOC vs upstream: 384 LOC)

| Fork Addition | Type | Plugin Candidate? |
|---|---|---|
| Spawn queue (`enqueueSpawnRequest`) | Fork-specific | YES → `spawn-queue` |
| `resolveSpawnProjectId()` helper | Fork-specific | YES → `spawn-project-resolution` |
| `warnIfAONotRunning()` | Fork-specific | Maybe → `spawn-lifecycle-check` |
| Prompt override support | Fork-specific | Keep as minor extension |
| Session prefix resolution | Fork-specific | YES → `spawn-session-prefix` |

**Key insight**: Most spawn divergence is queue-related. Upstream doesn't have spawn queues at all.

### 1.4 `session-manager.ts` (fork: 2,941 LOC vs upstream: 2,829 LOC)

| Fork Addition | Type | Plugin Candidate? |
|---|---|---|
| `GLOBAL_PAUSE_*` metadata tracking | Fork-specific | YES → `session-global-pause` |
| `getAoManagedSessionWorktreePattern` | Fork-specific | YES → `session-worktree-pattern` |
| `applySlashCommandRouting` | Fork-specific | YES → `session-slash-commands` |
| OpenCode agent discovery changes | Minor | Keep as-is |
| Session status tracking | Upstream | Keep in core |

**Key insight**: session-manager divergence is smaller. Most changes are helper functions that could be plugins.

---

## 2. Plugin Architecture Design

### 2.1 Plugin Slot Extension Model

Upstream's plugin architecture has defined slots:
```typescript
// Existing slots in plugin-registry
type SCM = { /* ... */ }
type Tracker = { /* ... */ }
type Notifier = { /* ... */ }
type Workspace = { /* ... */ }
type Agent = { /* ... */ }
```

**New slots needed:**
```typescript
// Lifecycle extension slots
type LifecycleExtension = {
  name: string;
  onSessionStatusChange?: (ctx: SessionContext, oldStatus, newStatus) => Promise<void>;
  onPollCycle?: (ctx: PollContext) => Promise<void>;
  onReaction?: (ctx: ReactionContext, reactionKey: string) => Promise<void>;
};

type SCMExtension = {
  name: string;
  enrichPR?: (pr: PRInfo, project: ProjectConfig) => Promise<EnrichedPR>;
  getSkepticComments?: (pr: PRReference) => Promise<SkepticComment[]>;
  getReviews?: (pr: PRReference, options?: ReviewOptions) => Promise<Review[]>;
};

type SpawnExtension = {
  name: string;
  beforeSpawn?: (ctx: SpawnContext) => Promise<void>;
  afterSpawn?: (ctx: SpawnContext, session: Session) => Promise<void>;
  queueRequest?: (ctx: SpawnRequest) => Promise<QueuedSpawn>;
};
```

### 2.2 Lifecycle Plugins Design

#### 2.2.1 `lifecycle-skeptic` Plugin

**Purpose**: All skeptic-related lifecycle behavior.

**Interface:**
```typescript
export interface SkepticLifecycleConfig {
  enabled: boolean;
  triggerOnPrOpen: boolean;
  triggerOnCRApproval: boolean;
  triggerOnFirstSeen: boolean;
  triggerOnNewCommit: boolean;
  evaluationCooldownMs: number;
}

export function createSkepticLifecyclePlugin(
  deps: LifecyclePluginDeps,
  config: SkepticLifecycleConfig,
): LifecycleExtension {
  const lastSkepticSha = new Map<string, string>();
  const lastSkepticCommentId = new Map<string, string>();

  return {
    name: "lifecycle-skeptic",
    onReaction: async (ctx, reactionKey) => {
      if (reactionKey === "skeptic-review" || reactionKey === "skeptic-trigger") {
        await triggerSkepticReaction(ctx, lastSkepticSha);
      }
    },
    onPollCycle: async (ctx) => {
      // Check for new skeptic FAIL comments
      // Fire skeptic-advice reaction
    },
    onSessionStatusChange: async (ctx, oldStatus, newStatus) => {
      if (newStatus === "pr_open" && oldStatus !== "pr_open") {
        await triggerSkepticFirstSeen(ctx, lastSkepticSha);
      }
      if (newStatus === "approved" && oldStatus !== "approved") {
        await triggerSkepticCRApproval(ctx, lastSkepticSha);
      }
    },
  };
}
```

**Upstream conflict resolution**: Instead of 500+ lines of skeptic code in `lifecycle-manager.ts`, the plugin registration is 5 lines:
```typescript
// In createLifecycleManager()
const skepticPlugin = createSkepticLifecyclePlugin(deps, config.projects[projectId]?.skeptic);
lifecycleExtensions.push(skepticPlugin);
```

#### 2.2.2 `lifecycle-agento-prefix` Plugin

**Purpose**: Enforce `[agento]` commit/PR prefix tagging.

**Interface:**
```typescript
export function createAgentoPrefixPlugin(
  deps: LifecyclePluginDeps,
): LifecycleExtension {
  return {
    name: "lifecycle-agento-prefix",
    onPollCycle: async (ctx) => {
      // Check PR title for [agento] prefix
      // If missing, trigger notification reaction
    },
  };
}
```

#### 2.2.3 `lifecycle-ao-action-log` Plugin

**Purpose**: All `logAoAction()` calls throughout lifecycle.

**Interface:**
```typescript
export function createAoActionLogPlugin(
  deps: LifecyclePluginDeps,
): LifecycleExtension {
  return {
    name: "lifecycle-ao-action-log",
    onSessionStatusChange: async (ctx, oldStatus, newStatus) => {
      const actionMap = {
        killed: "session_kill",
        merged: "pr_merge",
        absorbed: "session_absorbed",
      };
      if (actionMap[newStatus]) {
        await logAoAction({
          ts: new Date().toISOString(),
          session: ctx.session.id,
          action: actionMap[newStatus],
          pr: ctx.session.pr?.number,
          repo: ctx.session.pr ? `${ctx.session.pr.owner}/${ctx.session.pr.repo}` : undefined,
          reason: `status-transition:${oldStatus}->${newStatus}`,
        });
      }
    },
  };
}
```

#### 2.2.4 `lifecycle-mcp-mail` Plugin

**Purpose**: MCP mail integration for session events.

**Interface:**
```typescript
export function createMcpMailPlugin(
  deps: LifecyclePluginDeps,
): LifecycleExtension {
  return {
    name: "lifecycle-mcp-mail",
    onPollCycle: async (ctx) => {
      // Check for incoming messages via MCP mail
      // Route to appropriate session
    },
  };
}
```

### 2.3 SCM Plugins Design

#### 2.3.1 `scm-github-graphql` Plugin

**Purpose**: GraphQL-based PR detection with REST fallback.

**Interface:**
```typescript
export interface SCMGraphQLConfig {
  enabled: boolean;
  preferGraphQL: boolean;
  restFallbackOnRateLimit: boolean;
}

export function createGraphQLSCMExtension(
  gh: GhCommandFn,
  config: SCMGraphQLConfig,
): SCMExtension {
  return {
    name: "scm-github-graphql",
    enrichPR: async (pr, project) => {
      // Use GraphQL for enriched PR data
      // Fall back to REST on rate limit
    },
  };
}

// Usage: extends existing scm-github via composition
const baseSCM = createGitHubSCM();
const graphqlEnrichment = createGraphQLSCMExtension(gh, config);
return {
  ...baseSCM,
  ...graphqlEnrichment,
  // Override detectPR to use GraphQL first
  detectPR: async (session, project) => {
    try {
      return await graphqlEnrichment.detectPR?.(session, project) ?? await baseSCM.detectPR(session, project);
    } catch (e) {
      if (isRateLimitError(e)) {
        return await baseSCM.detectPR(session, project);
      }
      throw e;
    }
  },
};
```

#### 2.3.2 `scm-github-skeptic` Plugin

**Purpose**: Skeptic comment retrieval and analysis.

**Interface:**
```typescript
export function createSkepticSCMExtension(
  gh: GhCommandFn,
): SCMExtension {
  return {
    name: "scm-github-skeptic",
    getSkepticComments: async (pr) => {
      // Retrieve comments matching <!-- skeptic-... --> pattern
    },
  };
}
```

#### 2.3.3 `scm-github-comments` Plugin

**Purpose**: Comment enrichment with GraphQL and throttling.

**Interface:**
```typescript
export interface CommentEnrichmentConfig {
  throttleMs: number;
  useGraphQL: boolean;
}

export function createCommentsSCMExtension(
  gh: GhCommandFn,
  config: CommentEnrichmentConfig,
): SCMExtension {
  return {
    name: "scm-github-comments",
    getPendingComments: async (pr, options) => { /* GraphQL + throttling */ },
    getAutomatedComments: async (pr, options) => { /* GraphQL + throttling */ },
  };
}
```

### 2.4 Spawn Plugins Design

#### 2.4.1 `spawn-queue` Plugin

**Purpose**: Spawn queue with configurable limits.

**Interface:**
```typescript
export interface SpawnQueueConfig {
  enabled: boolean;
  maxActiveSessions: number;
  queueStrategy: "fifo" | "priority";
}

export function createSpawnQueuePlugin(
  deps: SpawnPluginDeps,
  config: SpawnQueueConfig,
): SpawnExtension {
  return {
    name: "spawn-queue",
    beforeSpawn: async (ctx) => {
      if (!config.enabled) return;
      const activeSessions = await countActiveSessions(ctx.projectId);
      if (activeSessions >= config.maxActiveSessions) {
        await enqueueSpawnRequest(ctx);
        throw new QueueFullError("Max active sessions reached");
      }
    },
  };
}
```

---

## 3. Migration Plan

### Phase 1: Extract Lifecycle Plugins (Highest Impact)

1. Create `packages/plugins/lifecycle-skeptic/`
   - Move all skeptic-related code from `lifecycle-manager.ts`
   - Export `createSkepticLifecyclePlugin()`
   - Add `lifecycle-skeptic` to plugin registry

2. Create `packages/plugins/lifecycle-ao-action-log/`
   - Move `logAoAction` calls from `lifecycle-manager.ts`
   - Export `createAoActionLogPlugin()`
   - Add `lifecycle-ao-action-log` to plugin registry

3. **Verification**: Run existing tests — if they pass, migration is safe.

4. **Conflict test**: Cherry-pick a recent upstream lifecycle commit — should have no conflicts.

### Phase 2: Extract SCM Plugins

1. Create `packages/plugins/scm-github-graphql/`
   - Move GraphQL code from `scm-github/src/index.ts`
   - Export `createGraphQLSCMExtension()`
   - Register as SCM plugin composition

2. Create `packages/plugins/scm-github-skeptic/`
   - Move `getSkepticComments()` from `scm-github/src/index.ts`
   - Export `createSkepticSCMExtension()`

3. **Verification**: Run scm-github tests.

### Phase 3: Extract Spawn Plugins

1. Create `packages/plugins/spawn-queue/`
   - Move queue logic from `spawn.ts`
   - Export `createSpawnQueuePlugin()`

2. **Verification**: Run spawn tests.

### Phase 4: Core Cleanup

After all plugins extracted:
1. Remove extracted code from core files
2. Verify all tests still pass
3. Verify upstream cherry-picks have minimal conflicts

---

## 4. Expected Outcomes

### Before Plugin Refactor
- Average merge conflict size: ~2,000 lines per major upstream import
- Conflict resolution time: ~4-8 hours per import
- Risk of conflicts breaking functionality: HIGH

### After Plugin Refactor
- Average merge conflict size: ~50 lines (plugin registration only)
- Conflict resolution time: ~30 minutes per import
- Risk of conflicts breaking functionality: LOW

### Specific Conflict Reduction
| File | Before | After |
|---|---|---|
| `lifecycle-manager.ts` | ~1,000 lines | ~20 lines |
| `scm-github/src/index.ts` | ~1,500 lines | ~30 lines |
| `spawn.ts` | ~100 lines | ~10 lines |
| `session-manager.ts` | ~100 lines | ~20 lines |
| **Total** | **~2,700 lines** | **~80 lines** |

---

## 5. Implementation Notes

### 5.1 Plugin Registration
Plugins should be registered in `agent-orchestrator.yaml`:
```yaml
plugins:
  lifecycle-skeptic:
    enabled: true
    triggerOnPrOpen: true
    triggerOnCRApproval: true
  lifecycle-ao-action-log:
    enabled: true
  scm-github-graphql:
    enabled: true
    preferGraphQL: true
```

### 5.2 Backward Compatibility
- Fork's existing behavior must be preserved
- Default plugin config matches current behavior
- Upstream users get empty plugin config (no fork plugins)

### 5.3 Test Strategy
- Each plugin has its own test suite
- Integration tests verify plugin composition works
- Core tests verify upstream behavior unchanged

### 5.4 Version Boundary
- Plugins target upstream `main` at a specific commit
- Each upstream import updates the target boundary
- Plugin code has its own changelog

---

## 6. Open Questions

1. **Lifecycle extension API**: Is `onPollCycle` the right hook, or should plugins register their own interval?

2. **SCM plugin composition**: Should SCM extensions override methods or extend them?

3. **Config migration**: How to migrate existing fork configs to plugin-based config?

4. **Testing strategy**: Should each plugin have isolated tests, or integration tests only?

5. **Upstream adoption**: Would upstream accept a plugin architecture that accommodates fork-specific extensions?

---

*Generated: 2026-04-21*
*Bead: bd-rn91 (follow-up)*
