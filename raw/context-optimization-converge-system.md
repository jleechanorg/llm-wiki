# Context Optimization Plan for /converge System

**Document**: Context Reduction Architecture and Implementation Plan
**Created**: August 18, 2025
**Branch**: converge-command-implementation
**Status**: Implementation Ready

---

## 🎯 Problem Statement

The current /converge system suffers from context exhaustion due to monolithic context accumulation:

**Current Context Consumption**:
- Large file reads: 50-100K tokens per operation
- Historical context buildup: Each step accumulates previous context
- Cross-reference loading: Multiple related files loaded simultaneously
- Monolithic intelligence: One agent tries to maintain awareness of everything

**Result**: Context exhaustion after 2-3 convergence iterations, limiting system effectiveness

---

## 🏗️ Architectural Solution: Independent Subagent Pattern

### Core Design Principle

**FROM**: Monolithic Context Agent
```
Main Agent: [Goal + Plans + History + Files + Memory + Guidelines] = 200K+ tokens
```

**TO**: Distributed File-Coordinated Agents
```
Orchestrator: [Goal + Status] = 5K tokens
├── Goal Agent: [Goal Statement] = 5K tokens
├── Planning Agent: [Goal + Command Index] = 10K tokens  
├── Execution Agents: [Single Task + Required Files] = 15K tokens each
├── Validation Agent: [Criteria + Current State] = 8K tokens
└── Learning Agent: [Outcomes + Patterns] = 5K tokens
```

### State Management: File-Based Coordination

**Session Directory Structure**:
```
/tmp/converge/{branch_name}/
├── session-{timestamp}/
│   ├── goal-spec.json          # Goal definition and success criteria
│   ├── command-index.json      # Lightweight command summaries
│   ├── execution-plan.json     # Step-by-step command plan
│   ├── reviewed-plan.json      # Plan + confidence assessment
│   ├── current-state.json      # Progress tracking
│   ├── session-metadata.json   # Timing, resources, metrics
│   ├── results/
│   │   ├── step-01-output.json # Individual task results
│   │   ├── step-02-output.json
│   │   └── step-NN-output.json
│   └── validation/
│       ├── criteria-status.json
│       └── evidence-log.json
├── command-cache/              # Pre-built command summaries
└── session-history/            # Completed sessions for learning
```

---

## 🚀 Implementation Phases

### Phase 1: Immediate Optimizations (60% Context Reduction)

**What Can Be Done NOW with Normal Subagents (No /orch Required)**:

#### 1.1 Command Index Generation
Create lightweight command summaries to avoid reading full .md files:

**Implementation**:
- **Subagent Task**: "Create command index by reading all .claude/commands/*.md files and extracting purpose, usage, and context requirements"
- **Output**: `/tmp/converge/{branch_name}/command-cache/index.json`
- **Context Savings**: 80% reduction in command discovery (10K vs 50K tokens)

#### 1.2 State Externalization
Move progress tracking from context to filesystem:

**Implementation**:
- **Subagent Task**: "Convert current TodoWrite tracking to JSON file persistence"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/current-state.json`
- **Context Savings**: 70% reduction in state tracking overhead

#### 1.3 Lazy File Loading
Only read files when actually needed for execution:

**Implementation**:
- **Subagent Task**: "Modify file reading patterns to load on-demand rather than preemptively"
- **Result**: Read files only during actual command execution, not planning
- **Context Savings**: 50% reduction in unnecessary file loading

#### 1.4 Goal Processing Agent
Separate goal definition from main workflow:

**Implementation**:
- **Subagent Input**: Raw goal statement only
- **Subagent Task**: "Parse goal, generate success criteria, create goal-spec.json"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/goal-spec.json`
- **Context Usage**: 5K tokens (isolated from main workflow)

### Phase 2: Specialized Agent Architecture (80% Context Reduction)

#### 2.1 Planning Agent (Independent)
**Subagent Specification**:
- **Input**: `goal-spec.json` + `command-index.json`
- **Task**: "Create execution plan using command summaries, not full docs"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/execution-plan.json`
- **Context**: 10K tokens maximum
- **Independence**: No shared context with other agents

#### 2.2 Review Agent (Independent)  
**Subagent Specification**:
- **Input**: `execution-plan.json` + confidence scoring rules
- **Task**: "Assess plan quality and assign confidence score (High/Medium/Low)"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/reviewed-plan.json`
- **Context**: 8K tokens maximum
- **Isolation**: No awareness of goal details or command internals

#### 2.3 Execution Agents (Parallel Independent)
**Subagent Specification**:
- **Input**: Single task from `execution-plan.json`
- **Task**: "Execute one specific command with required files only"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/results/step-{N}-output.json`
- **Context**: 15K tokens per agent
- **Parallelism**: Multiple agents can execute simultaneously

#### 2.4 Validation Agent (Independent)
**Subagent Specification**:
- **Input**: `reviewed-plan.json` + validation criteria
- **Task**: "Validate execution results against success criteria"
- **Output**: `/tmp/converge/{branch_name}/session-{id}/validation/criteria-status.json`
- **Context**: 8K tokens maximum
- **Focus**: Binary pass/fail with evidence, not remediation

#### 2.5 Learning Agent (Independent)
**Subagent Specification**:
- **Input**: All `step-*-output.json` files
- **Task**: "Extract patterns, success factors, failure modes"
- **Output**: `/tmp/converge/{branch_name}/session-history/{session-id}-learnings.json`
- **Context**: 5K tokens maximum
- **Output**: Appends to `session-history/all-learnings.json`

### Phase 3: Advanced Optimizations (90% Context Reduction)

#### 3.1 Cached Command Index
Pre-compute and cache command indices:

**Implementation**:
- **Trigger**: Daily cron or on .claude/commands/ changes
- **Output**: `/tmp/converge/command-index-cache.json`
- **Format**: { command: { purpose, usage, context_requirements, file_dependencies } }

#### 3.2 Semantic File Grouping
Group files by semantic relationship:

**Implementation**:
- **Subagent Task**: "Analyze file dependencies and group by functionality"
- **Output**: `file-groups.json` mapping task types to required file sets
- **Benefit**: Load entire group in one pass instead of incremental reads

#### 3.3 Progress Checkpointing
Save/restore orchestration state:

**Implementation**:
- **Trigger**: After each execution step
- **Output**: `checkpoint-{step}.json` with full state
- **Recovery**: Resume from checkpoint on failure

#### 3.4 Context Budget Enforcement
Hard limits per agent type:

**Implementation**:
- **Orchestrator**: 5K tokens max
- **Planning**: 10K tokens max  
- **Execution**: 15K tokens max
- **Validation**: 8K tokens max

---

## 📊 Expected Results

| Metric | Current | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|---------|
| Context per iteration | 200K | 80K | 40K | 20K |
| Max iterations | 2-3 | 5-6 | 10-12 | 20-25 |
| Token savings | - | 60% | 80% | 90% |
| Parallelism | 1 | 2-3 | 5-10 | 10-20 |

---

## 🔧 Implementation Checklist

- [ ] Create `/tmp/converge/` directory structure
- [ ] Implement command index generator (Phase 1.1)
- [ ] Add state externalization to orchestrator (Phase 1.2)
- [ ] Implement lazy file loading patterns (Phase 1.3)
- [ ] Create goal processing agent prompt (Phase 1.4)
- [ ] Design specialized agent prompts (Phase 2)
- [ ] Implement caching layer (Phase 3.1)
- [ ] Add context budget enforcement (Phase 3.4)

---

## ⚠️ Risks & Mitigations

1. **File system latency**: Use in-memory cache for hot paths
2. **Stale state files**: Add timestamps and TTL to all JSON
3. **Parallel race conditions**: Use file locking or sequential writes
4. **Lost intermediate results**: Checkpoint after every step