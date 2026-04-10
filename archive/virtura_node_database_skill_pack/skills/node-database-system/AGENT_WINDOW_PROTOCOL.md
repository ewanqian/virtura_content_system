# Agent Window Protocol

## Problem
When many chat windows are used at once, the system becomes unstable if every agent edits the same repo from a different assumption.

## Solution
Use role-based windows.

## Window roles

### 1. Scanner
Reads repo structure and writes:
- inventory files
- candidate lists
- source references

### 2. Normalizer
Builds:
- starter JSON
- object fields
- ownership / context
- relation entries

### 3. Note Writer
Writes:
- artistic notes
- production notes
- does not invent new object IDs

### 4. Exporter
Builds:
- clean JSON
- review CSV
- markdown brief packs
- validation report

## Shared contract
All windows must read the same:
- `OBJECT_INVENTORY.csv`
- `STARTER_DATABASE.json`
- `OWNERSHIP_DECISION_LOG.md`

No window may silently rename object IDs after they have been accepted.
