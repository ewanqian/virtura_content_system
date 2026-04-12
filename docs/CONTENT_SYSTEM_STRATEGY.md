# Content System Strategy

## Sync status

As of 2026-04-12, local `main` and `origin/main` are aligned.

- `git fetch origin --prune`
- `git pull --ff-only origin main`
- result: `Already up to date.`

This repo currently has no local-vs-cloud conflict to resolve.

## Current repo reading

The repo already contains three distinct layers, even if they are not fully named as such yet.

### 1. Content protocol layer

This is the `virtura_content_system` idea.

Its job is to define:

- what an object is
- what a node is
- what a relation is
- which fields are canonical
- which outputs can be exported for agents, websites, and editors

Relevant files:

- `README.md`
- `node-database-system/SKILL.md`
- `node-database-system/AGENT_WINDOW_PROTOCOL.md`
- `node-database-system/OUTPUTS.md`
- `archive/docs/SITE-RELATION-MAP.md`

### 2. Local product / editor layer

This is currently `Node Library`.

Its job is to:

- ingest files
- guess metadata
- let humans and agents review
- export clean packages

Relevant files:

- `viewer/data/nodes.json`
- `scripts/export_clean_json.py`
- `scripts/export_review_csv.py`
- `scripts/export_brief_pack.py`

### 3. Future operations / workspace layer

This is the role your `workspace tracker` should take.

Its job is not to replace the content system.
Its job is to manage:

- active tasks
- current conversations
- task state
- execution history
- decision trace

It should be a sibling system that is compatible with the content system, not a replacement for it.

## Key architectural judgment

The current direction is strong:

- objects are starting to become the source of truth
- views are already treated as downstream readings
- exports already exist for websites, review flows, and agents

The current weakness is also clear:

- `viewer/data/nodes.json` still mixes asset-level records with guessed semantic meaning
- `STARTER_DATABASE.json` is object-oriented, but separate from the ingestion layer
- there is not yet a stable contract between:
  - object memory
  - task memory
  - conversation memory

In short:

The repo already has a protocol instinct, but not yet a stable memory architecture.

## Recommended system split

Use three sibling concepts:

### A. Content System

Source of truth for durable cultural objects.

Examples:

- work
- node
- person
- collective
- asset
- writing
- venue
- spec
- relation
- concept
- method

These should be durable and referenceable.

### B. Workspace Tracker

Source of truth for active process.

Examples:

- task
- thread
- decision
- milestone
- blocker
- draft
- handoff

These are temporal and operational.

### C. Export / Interface Layer

A shared layer that turns A and B into:

- agent context packs
- editor resources
- website payloads
- review sheets
- search indexes

This is the layer that should be optimized for AI exchange.

## Recommended canonical object shape

Instead of only storing guessed viewer fields, move toward a canonical envelope like this:

```json
{
  "id": "node:hangzhou-opening-drop-flow",
  "type": "node",
  "title": "Hangzhou Opening / Drop Flow",
  "summary": "Public-facing event node for the Hangzhou presentation of Drop Flow.",
  "status": "active",
  "primaryContext": "shared",
  "owners": ["collective:virtura-collective"],
  "tags": ["event", "exhibition", "public-node"],
  "sourceRefs": [
    {
      "kind": "asset",
      "ref": "asset:event-2023-10-lonely-audiovisual-shanghai-broadcast-01"
    }
  ],
  "relations": [
    {
      "type": "presented_as",
      "target": "work:drop-flow"
    }
  ],
  "memory": {
    "semantic": [
      "Used as a public-facing event node in portfolio and collective views."
    ],
    "procedural": [
      "When exporting brief packs, prioritize featured event assets first."
    ],
    "episodic": [
      "Initial starter object was created during first-wave normalization."
    ]
  },
  "timestamps": {
    "createdAt": "2026-04-12T00:00:00Z",
    "updatedAt": "2026-04-12T00:00:00Z"
  }
}
```

This does three useful things:

1. separates canonical fields from guessed ingestion fields
2. gives AI explicit relation edges instead of forcing inference
3. creates a place for long-term memory without mixing it into raw assets

## Recommended data split inside this repo

### 1. Raw ingestion records

Keep the current viewer-oriented records, but treat them as intake records only.

Suggested role:

- file facts
- thumbnail facts
- hash / fingerprint
- guessed metadata
- duplicate detection

Suggested location:

- `data/intake/assets.json`

### 2. Canonical object store

This becomes the durable source layer.

Suggested location:

- `data/objects/*.json`

Examples:

- `data/objects/works.json`
- `data/objects/nodes.json`
- `data/objects/people.json`
- `data/objects/relations.json`
- `data/objects/concepts.json`

### 3. Memory store

This stores extracted memory rather than raw content.

Suggested location:

- `data/memory/semantic.json`
- `data/memory/episodic.json`
- `data/memory/procedural.json`

Or, if you want stronger querying:

- local SQLite first
- PostgreSQL later if cross-tool querying grows

### 4. Workspace tracker store

Keep this as a separate sibling repo or sibling directory tree.

Suggested object types:

- task
- thread
- checkpoint
- decision
- artifact

The important thing is not to merge tasks into content objects.
Link them by relation instead.

Example:

- `task:build-wave-editor` `produces` `node:wave-editor-protocol`
- `thread:workspace-tracker-sync` `decides` `spec:content-workspace-contract-v1`

## Memory strategy

The cleanest memory model here is a 3-layer one.

### 1. Semantic memory

Facts worth preserving.

Examples:

- a work belongs to a period
- a node is public or internal
- a method belongs to a recurring practice

### 2. Episodic memory

What happened and when.

Examples:

- a project was reclassified
- a conversation decided to split asset and node
- a pack was exported for a specific purpose

### 3. Procedural memory

How to do something repeatedly.

Examples:

- export rules
- review rules
- ingestion rules
- style or naming rules

This mirrors current agent-memory practice well and avoids trying to store everything as one giant note.

## What should be optimized for AI exchange

The repo should not optimize only for human reading.
It should optimize for machine legibility in four ways:

### 1. Stable IDs

Use stable typed IDs.

Examples:

- `work:drop-flow`
- `node:hangzhou-opening-drop-flow`
- `asset:event-2023-westbound-art-fair-ewan-artwork`
- `task:normalize-brief-pack-schema`

### 2. Explicit relations

Do not force AI to infer graph structure from filenames alone.

Add relation objects such as:

- `documents`
- `presented_as`
- `belongs_to`
- `produced_by`
- `derived_from`
- `used_in`
- `decided_by`

### 3. Layered exports

Produce different outputs for different consumers.

- `agent-pack`: concise, relation-rich, token-efficient
- `editor-pack`: fuller records with raw notes
- `web-pack`: public-safe only
- `review-pack`: spreadsheet-friendly

### 4. Change trace

Important records should know:

- who changed them
- when
- why
- from which conversation or task

This is the missing bridge between content system and workspace tracker.

## Suggested relation between Content System and Workspace Tracker

Use this rule:

Content System stores what is true enough to preserve.
Workspace Tracker stores what is still in motion.

Then connect them with typed relations.

Examples:

- a task can produce a work draft
- a thread can discuss a node
- a decision can freeze a schema version
- a milestone can publish an export pack

That keeps both systems compatible without collapsing them into one blurry database.

## Practical next steps

### Phase 1

Stabilize the content-side schema.

- split intake assets from canonical objects
- introduce typed IDs
- add `relations.json`
- add `concepts.json` and `methods.json` only if needed

### Phase 2

Create a minimal memory layer.

- `semantic`
- `episodic`
- `procedural`

Do not start with embeddings.
Start with explicit JSON memory records.

### Phase 3

Define the cross-system contract with workspace tracker.

Minimum shared fields:

- `id`
- `type`
- `title`
- `status`
- `updatedAt`
- `sourceThread`
- `sourceTask`
- `relations`

### Phase 4

Only after the schema is stable, add search and retrieval.

Good order:

1. local JSON
2. SQLite or Postgres metadata store
3. optional vector index for semantic recall

## Outside references worth borrowing from

These are not for copying directly, but for design pressure.

### Local-first foundation

Martin Kleppmann's local-first essay argues for systems that preserve offline work, user ownership, long-term preservation, and collaboration.

Source:

- https://martin.kleppmann.com/2019/10/23/local-first-at-onward.html

### AI context exchange

MCP treats tools, resources, and prompts as separate primitives and explicitly separates context exchange from model usage.

Sources:

- https://modelcontextprotocol.io/docs/learn/architecture
- https://modelcontextprotocol.io/docs/concepts/resources

This is directly relevant to your system:

- content objects can become resources
- export actions can become tools
- workflow templates can become prompts

### Long-term memory shape

LangGraph separates:

- thread-scoped short-term memory
- namespace/key-based long-term memory

It also distinguishes semantic / episodic / procedural memory as useful categories.

Sources:

- https://docs.langchain.com/oss/javascript/langgraph/memory
- https://docs.langchain.com/oss/python/langchain/long-term-memory

### Local durable document sync

Automerge Repo shows a concrete pattern for local-first documents with file-system-backed storage and optional network sync.

Sources:

- https://automerge.org/docs/reference/repositories/
- https://automerge.org/docs/reference/repositories/storage/

This is especially relevant if `Node Library`, `Wave`, or a future node editor becomes collaborative or multi-window.

## Final recommendation

Do not turn the content system into a giant all-purpose database immediately.

Instead:

1. make `virtura_content_system` the durable object protocol
2. keep `Node Library` as the first local editor/product on top of it
3. let `workspace tracker` own active process, not durable culture
4. connect them through stable IDs, relations, and memory records
5. optimize exports for agents as a first-class interface, not an afterthought

That path keeps the system legible, local-first, and extensible without losing the cultural layer you care about.
