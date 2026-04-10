# VIRTURA-Content

VIRTURA-Content is a file-based, agent-friendly content protocol for the broader VIRTURA ecosystem.

It is not a traditional CMS dashboard.
It is a structured content layer that allows multiple public-facing sites and tools to read from the same source of truth.

## Purpose

This repository is designed to support:

- personal portfolio sites
- VIRTURA Collective
- VIRTURA SpacePort
- VIRTURA Newsroom
- artist microsites
- viewer / venue / delivery pages
- archive and exhibition systems
- future agent / skill based content operations

## Core Idea

One content object can appear in multiple site contexts.

For example, a single work can be:

- a featured work on a personal portfolio
- a collective collaboration on the team site
- a public node in SpacePort
- a review subject in Newsroom
- a spec-linked delivery case in a viewer page

This repository is therefore a content protocol, not just a website backend.

## Core Object Types

- `person` — artists, collaborators, organizers
- `collective` — teams, groups, networks
- `work` — works, series, project lines
- `node` — public presentations, camps, performances, exhibitions, workshops
- `asset` — images, posters, videos, screenshots, files
- `writing` — essays, reviews, research notes, curatorial texts
- `venue` — spaces, screen environments, playback contexts
- `spec` — resolution, frame rate, codec, hardware, delivery requirements
- `relation` — links between all objects above

## Repository Structure

```text
schemas/
content/
manifests/
scripts/
generated/
```

### `schemas/`
Defines the shape of each content object.

### `content/`
Stores the actual source content as JSON / YAML / Markdown.

### `manifests/`
Stores site profiles, featured logic, route maps, and image indexes.

### `scripts/`
Contains validators, generators, importers, and link checkers.

### `generated/`
Contains derived data for public sites and tools.

## Site Profiles

Different frontends read the same content differently.

Examples:

- `portfolio.json` — foreground works, trajectory, services
- `collective.json` — foreground network, selected collaborations, stations
- `spaceport.json` — foreground stations, archive, public nodes
- `newsroom.json` — foreground writings, commentaries, reviews
- `viewer.json` — foreground venue and delivery specs

## Recommended Workflow

1. add or update source content in `content/`
2. validate content against schemas
3. generate site-specific data into `generated/`
4. let downstream sites consume only generated outputs
5. keep frontend sites presentation-focused, not content-authoring focused

## What this repo is not

- not a visual page builder
- not a traditional admin panel
- not a replacement for SpacePort or Collective
- not the only public-facing layer

## Relationship to other VIRTURA repositories

- `VIRTURA-Collective` — team-facing public entry
- `VIRTURA-SpacePort` — public foyer, stations, archive, knowledge routing
- `VIRTURA-Newsroom` — publication, reviews, commentary
- `SceneForge` — viewer / previsualization / scene tool layer
- `RepoForge` — repo governance and public infra shell
- `Research Laboratory` — research mother layer
- `Skill Forge` — research compressed into reusable skills

## Phase 1 Goal

Start with a minimal but real content system that can support:

- Drop Flow
- TIMER
- Kashiwa collaboration
- UFO Terminal node
- Hangzhou opening node
- at least one venue/spec object

Then expand from there.
