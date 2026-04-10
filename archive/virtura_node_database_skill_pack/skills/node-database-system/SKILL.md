# Node Database System Skill
### A repository skill for building, maintaining, and exporting node-based content systems

## What this skill is for
Use this skill when a repository is trying to stop treating pages as the primary unit, and instead wants to organize content as structured objects.

This skill is designed for repositories that need to handle:
- works
- nodes
- people
- collectives
- assets
- writings
- venues
- specs
- relations

It is especially useful when the same content must appear in multiple views, such as:
- personal portfolio
- collective site
- public foyer / SpacePort
- newsroom / writing layer
- viewer / spec pages
- local asset tool / Node Library

## Core principle
Pages are not objects.
Pages are views.

Objects are the source of truth.
Views are site-specific readings of the same objects.

## What this skill does
This skill helps an agent:
1. scan a repo and identify candidate objects
2. separate objects from views
3. classify content into:
   - person
   - collective
   - work
   - node
   - asset
   - writing
   - venue
   - spec
   - relation
4. assign ownership and context
5. prepare starter database files
6. prepare note plans
7. prepare export packs for websites and agent workflows

## Required decisions before running
Before building or updating the database, the agent must confirm:
- which objects are personal-first
- which objects are collective-first
- which are shared
- which are external collaborations
- which pages are only views, not primary objects

Use only these values for `primaryContext` in the first wave:
- personal
- collective
- shared
- external

## Recommended first-wave objects
Do not objectify everything at once.

Start with:
- works
- nodes
- people
- collective
- relations

Only add:
- assets
- writings
- venues
- specs

after the first wave is stable.

## Standard workflow
### Phase 1 — scan
Scan repo entry files and create:
- work inventory
- node inventory
- people inventory
- view-only inventory

### Phase 2 — classify
For each candidate object, assign:
- id
- type
- primaryOwner
- primaryContext
- visibility
- sourceRefs

### Phase 3 — starter database
Build a starter database in JSON.

### Phase 4 — note planning
For each high-value object, create a note plan:
- artistic note
- production note

### Phase 5 — validation
Verify:
- one object is not duplicated across multiple repos as separate truths
- views are not mistaken as objects
- node/work distinction is stable
- ownership/context is filled
- relation graph is minimally present

### Phase 6 — export
Prepare:
- clean JSON data
- review CSV
- markdown brief packs for agent use

## Rules for multiple conversation windows / agent windows
If multiple agent windows are working at once, split them by role, not by random file ownership.

Recommended split:

### Window A — repository scan
- reads the repo
- inventories candidate objects
- does not rewrite front-end pages

### Window B — object normalization
- converts candidate content into structured objects
- adds ownership / context / visibility

### Window C — note drafting
- writes artistic / production notes
- does not alter object IDs or sourceRefs

### Window D — export / sync
- prepares clean JSON / CSV / brief packs
- validates links and output consistency

Do not let every window edit everything.

## Outputs this skill should produce
At minimum, produce:
1. `OBJECT_INVENTORY.csv`
2. `STARTER_DATABASE.json`
3. `NOTE_PLAN.md`
4. `VIEW_VALIDATION_REPORT.md`
5. `BRIEF_PACK_TEMPLATE.md`

## What this skill must not do
- do not directly rewrite the whole site first
- do not treat navigation sections as objects
- do not collapse works and nodes into the same type
- do not use markdown alone as the only structured source
- do not create multiple conflicting truths for the same object
