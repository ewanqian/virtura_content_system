# Priority Backlog

This file keeps the current expansion ideas from being lost while still protecting the MVP.

## P0

These are the current must-do items for the next few conversations.

- split intake records from canonical objects
- introduce typed IDs across durable objects
- add a first `relations.json`
- add an onboarding doc for new use of the system
- define the contract with `workspace tracker`
- keep the local viewer as the inspection panel
- preserve voice-to-Codex editing as a core workflow

## P1

These are high-value next steps once the basic split works.

- add memory files for semantic / episodic / procedural records
- support old material ingestion from notes and chat exports
- create a derivative-tool export format
- add a schema version field and migration notes
- improve the viewer payload to show object relations, not just files

## P2

These are valuable, but should not block MVP delivery.

- add venue / spec / concept / method object types
- add batch conversion pipelines for old databases
- add optional SQLite metadata layer
- add better diffing and update propagation between derivatives
- add stronger search and retrieval flows

## Parking lot

These should be remembered without forcing them into the MVP.

- richer speech-driven editing commands
- PDF and document ingestion
- video-heavy asset support
- more advanced web dashboards
- vector retrieval layer
- broader multi-repo distribution tooling

## Decision rule

If a feature does not improve one of these directly, it is not P0:

- ingest messy material
- normalize into stable objects
- review visually
- update through Codex quickly
- export for reuse
