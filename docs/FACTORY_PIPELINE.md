# Factory Pipeline

This document turns the current idea into a practical processing pipeline.

## Product metaphor

Think of the system as a local-first factory.

It has:

- raw input
- lower-stage processing
- higher-stage processing
- review checkpoints
- export lines

## Pipeline layers

### Layer 0. Raw feed

This is where old or messy material enters the system.

Examples:

- images
- folders
- old notes
- past chats
- project archives
- portfolio source material

Output:

- untouched source files

### Layer 1. Intake analysis

This is the first-pass machine reading layer.

Jobs:

- fingerprint files
- infer title guesses
- infer year guesses
- infer candidate work / node / venue references
- detect duplicates
- generate thumbnails

Output:

- intake records

Suggested file:

- `data/intake/assets.json`

### Layer 2. Canonical normalization

This is where guessed material becomes stable objects.

Jobs:

- assign typed IDs
- split assets from works / nodes / events
- attach owners and contexts
- create relation edges
- mark visibility and status

Output:

- canonical objects

Suggested files:

- `data/objects/assets.json`
- `data/objects/works.json`
- `data/objects/nodes.json`
- `data/objects/relations.json`

### Layer 3. Memory extraction

This is where repeated meaning is preserved.

Jobs:

- extract stable facts
- record key decisions
- preserve reusable procedures

Output:

- semantic memory
- episodic memory
- procedural memory

Suggested files:

- `data/memory/semantic.json`
- `data/memory/episodic.json`
- `data/memory/procedural.json`

### Layer 4. Visual review

This is the dashboard layer.

Jobs:

- show what exists
- show what is missing
- show duplicates and conflicts
- help the user inspect visually

Output:

- review-ready local panel

### Layer 5. Export lines

This is where the same source becomes different outputs.

Jobs:

- agent pack export
- website export
- review export
- derivative app export

Output:

- brief packs
- clean JSON
- review CSV
- tool-specific payloads

## Processing levels

You described two broad processing modes. They fit well here.

### Secondary processing

This is cleanup and structuring.

Examples:

- rename files
- add metadata
- group similar assets
- identify duplicates
- create first-pass object candidates

### Advanced processing

This is interpretation and reusable knowledge extraction.

Examples:

- identify cultural motifs
- extract methods and techniques
- connect older material into one lineage
- create project summaries
- build reusable brief packs and memory records

## Distribution and update model

To keep derivatives aligned, use this flow:

1. freeze a canonical schema version
2. update source objects in this repo
3. regenerate exports
4. let derivative tools consume exports, not invent their own schema

That means:

- this repo is the protocol and object source
- derivative apps are readers, editors, or specialized processors

## Build efficiency rule

Do not rebuild everything every time.

Prefer:

- incremental ingest
- incremental normalization
- targeted export regeneration
- schema versioning with migration notes

## Suggested MVP script groups

### Ingest

- import files
- fingerprint
- thumbnail
- first-pass metadata

### Normalize

- convert intake records into canonical objects
- assign IDs
- build relations

### Review

- prepare viewer payload
- build review sheet

### Export

- build brief pack
- build public JSON
- build derivative tool payload
