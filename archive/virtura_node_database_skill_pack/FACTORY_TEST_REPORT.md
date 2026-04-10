# Factory Test Report

## Goal
Test whether the skill can support different content repo levels and multiple agent windows.

## Test 1 — personal repo
Input:
- personal portfolio with featured works, projects, bio, services

Result:
- skill can separate works from nodes
- skill can mark bio/services as person-facing views
- skill can export starter database and note plan

Status: PASS

## Test 2 — collective repo
Input:
- collective repo with about, works, artists, activities

Result:
- skill can identify collective-first objects
- skill can treat artists as people objects
- skill can separate activity timeline from activity nodes

Status: PASS

## Test 3 — distributed system repo
Input:
- content protocol repo intended to feed multiple public sites

Result:
- skill can keep objects as source-of-truth
- skill can avoid treating views as objects
- skill can split roles across multiple agent windows

Status: PASS

## Test 4 — multi-window management
Input:
- scanner / normalizer / note writer / exporter windows

Result:
- role separation avoids silent conflicts
- object IDs remain stable if all windows use shared inventory and starter database

Status: PASS

## Final release judgment
This skill is suitable for first-wave production use in:
- personal content repos
- collective content repos
- distributed content protocol repos

It should not be treated as a one-shot page editing tool.
It should be treated as a node-based content structuring workflow.
