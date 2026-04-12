# Workspace Tracker Handoff

This file is for the parallel `workspace tracker` thread.

It explains what `workspace tracker` should assume about `virtura_content_system`, what it should read from it, and what it should not try to own.

## One-line relationship

`virtura_content_system` stores durable content objects.

`workspace tracker` stores active work state.

They should be connected, not merged.

## What content system owns

These are long-lived objects that may outlast any single task or chat window.

- work
- node
- asset
- event
- venue
- note
- person
- collective
- writing
- spec
- relation
- concept
- method

Content system is the source of truth for:

- canonical IDs
- object metadata
- relation graph
- exported brief packs
- clean public payloads
- cultural memory worth preserving

## What workspace tracker owns

These are time-bound operational records.

- task
- thread
- checkpoint
- decision
- milestone
- blocker
- draft
- handoff

Workspace tracker is the source of truth for:

- what is in progress
- what is blocked
- which thread is responsible
- what changed this week
- what still needs review

## Shared contract

Both systems should agree on these minimum fields:

```json
{
  "id": "task:normalize-content-schema",
  "type": "task",
  "title": "Normalize content schema",
  "status": "active",
  "updatedAt": "2026-04-12T00:00:00Z",
  "relations": [
    {
      "type": "updates",
      "target": "spec:content-schema-v1"
    }
  ],
  "sourceThread": "thread:content-system-mvp",
  "sourceTask": "task:content-system-mvp"
}
```

## What workspace tracker should ingest from this repo

### 1. Canonical docs

- `docs/CONTENT_SYSTEM_STRATEGY.md`
- `docs/MVP_ONBOARDING.md`
- `docs/FACTORY_PIPELINE.md`
- `docs/PRIORITY_BACKLOG.md`

### 2. Canonical object outputs

As they mature:

- `data/objects/*.json`
- `data/memory/*.json`

### 3. Export signals

- `exports/brief-packs/*`
- `exports/website/*`
- `exports/review-sheets/*`

These tell tracker:

- what has already been produced
- what kind of downstream delivery exists
- which content areas are mature enough for reuse

## What workspace tracker should send back

Tracker should not rewrite content objects directly unless explicitly asked.

Instead, it should send back:

- task status
- implementation decisions
- milestone state
- links to related threads
- requests for new objects or schema changes

Preferred shape:

```json
{
  "id": "decision:split-intake-and-canonical-objects",
  "type": "decision",
  "title": "Split intake and canonical objects",
  "status": "accepted",
  "summary": "Raw asset guesses must not be the same layer as durable content objects.",
  "relations": [
    {
      "type": "affects",
      "target": "spec:content-object-schema-v1"
    },
    {
      "type": "originated_in",
      "target": "thread:content-system-mvp"
    }
  ]
}
```

## Operational rule

Use this rule in both threads:

If it is still moving, it belongs to tracker.
If it is stable enough to preserve, it belongs to content system.

## Copy block for workspace tracker

You can paste this into the tracker thread:

```md
Assume `virtura_content_system` is the durable object layer and `workspace tracker` is the active process layer.

Do not merge tasks into content objects.
Link them by typed relations instead.

When tracking this project, prioritize:
- task / thread / checkpoint / decision / milestone
- sourceThread / sourceTask fields
- links to content specs and exported packs

The content system currently needs tracker support for:
- MVP rollout status
- schema freeze checkpoints
- backlog prioritization
- cross-thread decision memory
- handoff records for future derivative tools
```
