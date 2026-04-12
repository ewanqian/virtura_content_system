#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalize viewer intake records into a split data model.

Input:
- viewer/data/nodes.json

Outputs:
- data/intake/assets.json
- data/objects/assets.json
- data/objects/works.json
- data/objects/nodes.json
- data/objects/relations.json
- data/memory/semantic.json
- data/memory/episodic.json
- data/memory/procedural.json
"""

from __future__ import annotations

import json
import os
import re
from collections import OrderedDict
from datetime import datetime, timezone


SOURCE_PATH = "viewer/data/nodes.json"
INTAKE_DIR = "data/intake"
OBJECTS_DIR = "data/objects"
MEMORY_DIR = "data/memory"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def typed_id(prefix: str, value: str) -> str:
    return f"{prefix}:{slugify(value)}"


def load_source() -> list[dict]:
    if not os.path.exists(SOURCE_PATH):
        raise FileNotFoundError(f"Source file not found: {SOURCE_PATH}")

    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dirs() -> None:
    for path in [INTAKE_DIR, OBJECTS_DIR, MEMORY_DIR]:
        os.makedirs(path, exist_ok=True)


def build_intake_record(node: dict, exported_at: str) -> dict:
    asset_slug = slugify(node.get("filename") or str(node.get("id")))
    return {
        "id": typed_id("asset", asset_slug),
        "sourceId": node.get("id"),
        "filename": node.get("filename"),
        "path": node.get("path"),
        "titleGuess": node.get("title_guess"),
        "yearGuess": node.get("year_guess"),
        "dateGuess": node.get("date_guess"),
        "relatedWorkGuess": node.get("related_work_guess"),
        "relatedNodeGuess": node.get("related_node_guess"),
        "typeGuess": node.get("type_guess"),
        "category": node.get("category"),
        "ownerGuess": node.get("owner_guess"),
        "artist": node.get("artist"),
        "contributors": node.get("contributors", []),
        "contributions": node.get("contributions", []),
        "isDuplicate": bool(node.get("is_duplicate")),
        "featuredCandidate": bool(node.get("featured_candidate")),
        "fingerprint": node.get("fingerprint"),
        "imageInfo": node.get("image_info"),
        "notes": node.get("notes"),
        "createdAt": node.get("created_at"),
        "normalizedAt": exported_at,
    }


def build_asset_object(intake: dict, exported_at: str) -> dict:
    tags = [tag for tag in [intake.get("category"), intake.get("typeGuess")] if tag and tag != "unknown"]

    relations = []
    if intake.get("relatedWorkGuess"):
        relations.append({"type": "documents", "target": typed_id("work", intake["relatedWorkGuess"])})
    if intake.get("relatedNodeGuess"):
        relations.append({"type": "documents", "target": typed_id("node", intake["relatedNodeGuess"])})

    summary = intake.get("titleGuess") or intake.get("filename") or intake["id"]

    return {
        "id": intake["id"],
        "type": "asset",
        "title": summary,
        "summary": f"Asset record for {summary}.",
        "status": "archived" if intake.get("isDuplicate") else "active",
        "primaryContext": "personal" if intake.get("ownerGuess") == "personal" else "shared",
        "owners": [typed_id("person", intake.get("artist") or "ewan")],
        "tags": tags,
        "sourceRefs": [
            {"kind": "intake", "ref": intake["id"]},
            {"kind": "file", "ref": intake.get("path") or ""}
        ],
        "relations": relations,
        "memory": {
            "semantic": [],
            "episodic": [],
            "procedural": []
        },
        "timestamps": {
            "createdAt": intake.get("createdAt") or exported_at,
            "updatedAt": exported_at
        }
    }


def build_parent_object(object_id: str, object_type: str, title: str, exported_at: str) -> dict:
    summary_type = "work" if object_type == "work" else "node"
    return {
        "id": object_id,
        "type": object_type,
        "title": title,
        "summary": f"Canonical {summary_type} object for {title}.",
        "status": "active",
        "primaryContext": "shared",
        "owners": [],
        "tags": [],
        "sourceRefs": [],
        "relations": [],
        "memory": {
            "semantic": [],
            "episodic": [],
            "procedural": []
        },
        "timestamps": {
            "createdAt": exported_at,
            "updatedAt": exported_at
        }
    }


def write_json(path: str, payload) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    ensure_dirs()
    source_nodes = load_source()
    exported_at = now_iso()

    intake_assets = []
    asset_objects = []
    work_objects: OrderedDict[str, dict] = OrderedDict()
    node_objects: OrderedDict[str, dict] = OrderedDict()
    relations = []
    relation_seen = set()

    for source_node in source_nodes:
        intake = build_intake_record(source_node, exported_at)
        intake_assets.append(intake)
        asset_object = build_asset_object(intake, exported_at)
        asset_objects.append(asset_object)

        related_work = intake.get("relatedWorkGuess")
        if related_work:
            work_id = typed_id("work", related_work)
            if work_id not in work_objects:
                work_objects[work_id] = build_parent_object(work_id, "work", related_work, exported_at)
            work_objects[work_id]["sourceRefs"].append({"kind": "asset", "ref": intake["id"]})

            rel_key = ("documents", intake["id"], work_id)
            if rel_key not in relation_seen:
                relations.append({
                    "id": typed_id("relation", f"documents-{intake['id']}-{work_id}"),
                    "type": "relation",
                    "title": f"{intake['id']} documents {work_id}",
                    "summary": "Asset documents work.",
                    "status": "active",
                    "timestamps": {
                        "createdAt": exported_at,
                        "updatedAt": exported_at
                    },
                    "from": intake["id"],
                    "to": work_id,
                    "relationType": "documents"
                })
                relation_seen.add(rel_key)

        related_node = intake.get("relatedNodeGuess")
        if related_node:
            node_id = typed_id("node", related_node)
            if node_id not in node_objects:
                node_objects[node_id] = build_parent_object(node_id, "node", related_node, exported_at)
            node_objects[node_id]["sourceRefs"].append({"kind": "asset", "ref": intake["id"]})

            rel_key = ("documents", intake["id"], node_id)
            if rel_key not in relation_seen:
                relations.append({
                    "id": typed_id("relation", f"documents-{intake['id']}-{node_id}"),
                    "type": "relation",
                    "title": f"{intake['id']} documents {node_id}",
                    "summary": "Asset documents node.",
                    "status": "active",
                    "timestamps": {
                        "createdAt": exported_at,
                        "updatedAt": exported_at
                    },
                    "from": intake["id"],
                    "to": node_id,
                    "relationType": "documents"
                })
                relation_seen.add(rel_key)

        if related_work and related_node:
            node_id = typed_id("node", related_node)
            work_id = typed_id("work", related_work)
            rel_key = ("presented_as", node_id, work_id)
            if rel_key not in relation_seen:
                relations.append({
                    "id": typed_id("relation", f"presented-as-{node_id}-{work_id}"),
                    "type": "relation",
                    "title": f"{node_id} presented as {work_id}",
                    "summary": "Node is a presentation or reading of a work.",
                    "status": "active",
                    "timestamps": {
                        "createdAt": exported_at,
                        "updatedAt": exported_at
                    },
                    "from": node_id,
                    "to": work_id,
                    "relationType": "presented_as"
                })
                relation_seen.add(rel_key)

    write_json(os.path.join(INTAKE_DIR, "assets.json"), intake_assets)
    write_json(os.path.join(OBJECTS_DIR, "assets.json"), asset_objects)
    write_json(os.path.join(OBJECTS_DIR, "works.json"), list(work_objects.values()))
    write_json(os.path.join(OBJECTS_DIR, "nodes.json"), list(node_objects.values()))
    write_json(os.path.join(OBJECTS_DIR, "relations.json"), relations)

    write_json(os.path.join(MEMORY_DIR, "semantic.json"), [])
    write_json(os.path.join(MEMORY_DIR, "episodic.json"), [])
    write_json(os.path.join(MEMORY_DIR, "procedural.json"), [])

    print(f"Normalized {len(source_nodes)} source records")
    print(f"- intake assets: {len(intake_assets)}")
    print(f"- canonical assets: {len(asset_objects)}")
    print(f"- canonical works: {len(work_objects)}")
    print(f"- canonical nodes: {len(node_objects)}")
    print(f"- relations: {len(relations)}")


if __name__ == "__main__":
    main()
