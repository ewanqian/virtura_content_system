# MVP Onboarding

## What this repo is

`virtura_content_system` is the protocol and source-layer repo.

`Node Library` is the first usable local product inside it.

The practical goal of this MVP is:

- accept files and previous materials as input
- turn them into structured nodes and objects
- let a human review them through a local visual panel
- let Codex update them through voice/text instructions
- export clean packages for websites, agents, and future tools

## How to think about the system

This is not just an image organizer.

It is a local-first content factory with multiple processing levels:

1. input
2. first-pass analysis
3. normalization
4. review
5. object linking
6. export
7. reuse in derivative tools

## Core interaction model

The main usage pattern is:

1. you drop files or old materials into the repo
2. Codex ingests and restructures them
3. the local web panel helps you browse and inspect visually
4. you speak or type updates to Codex instead of manually clicking through every field
5. Codex writes changes back into the local source layer

This means:

- the browser is a visual dashboard
- Codex is the main editing operator
- local files are the durable source

## The four user-facing jobs

### 1. Feed material in

Examples:

- old image folders
- old project notes
- exported chat notes
- PDFs
- markdown files
- asset batches

### 2. Process material

Examples:

- classify
- rename
- extract entities
- detect duplicates
- infer project grouping
- identify candidate events / works / venues / notes

### 3. Review visually

Examples:

- scan thumbnails
- spot gaps
- compare duplicates
- inspect relation coverage
- understand what matters quickly

### 4. Export outward

Examples:

- agent brief pack
- clean public JSON
- review CSV
- derivative app payload

## Recommended local folder model

### Input

- `incoming/`
- `manifests/`

### Working

- `processed/`
- `thumbs/`

### Durable structured data

- `data/intake/`
- `data/objects/`
- `data/memory/`

### Outputs

- `exports/brief-packs/`
- `exports/review-sheets/`
- `exports/website/`
- `exports/portfolio/`

## Minimal first-run workflow

1. Place raw assets or old materials into `incoming/`
2. Run ingest scripts
3. Generate intake records
4. Normalize selected records into canonical objects
5. Review in local viewer
6. Ask Codex to adjust fields by voice/text
7. Export the pack you need

## What counts as success for this MVP

The MVP is successful when:

- you can feed in messy material
- the system can create usable first-pass structure
- you can understand it visually
- you can update it through Codex quickly
- you can export something downstream without manual rewriting

## What is intentionally not required yet

- server deployment
- multi-user auth
- heavy online CMS logic
- perfect auto-classification
- complete vector database stack

## How future derivative versions should grow

When deriving a new version from this project:

1. keep the canonical object contract
2. add a new view or pipeline, not a new truth source
3. keep exports layered by audience
4. add new object types only when they survive repeated use

That keeps the ecosystem compatible instead of creating many incompatible clones.
