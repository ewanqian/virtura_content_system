#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared helpers for export scripts.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


INTAKE_ASSETS_PATH = "data/intake/assets.json"
OBJECT_ASSETS_PATH = "data/objects/assets.json"
OBJECT_WORKS_PATH = "data/objects/works.json"
OBJECT_NODES_PATH = "data/objects/nodes.json"
VIEWER_NODES_PATH = "viewer/data/nodes.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_export_data() -> dict:
    if all(os.path.exists(path) for path in [INTAKE_ASSETS_PATH, OBJECT_ASSETS_PATH, OBJECT_WORKS_PATH]):
        return {
            "mode": "canonical",
            "intake_assets": load_json(INTAKE_ASSETS_PATH),
            "assets": load_json(OBJECT_ASSETS_PATH),
            "works": load_json(OBJECT_WORKS_PATH),
            "nodes": load_json(OBJECT_NODES_PATH) if os.path.exists(OBJECT_NODES_PATH) else [],
        }

    if os.path.exists(VIEWER_NODES_PATH):
        return {
            "mode": "viewer",
            "viewer_nodes": load_json(VIEWER_NODES_PATH),
        }

    raise FileNotFoundError(
        "No export source found. Expected canonical data in data/intake + data/objects or fallback data in viewer/data/nodes.json"
    )


def build_viewer_fallback_records(viewer_nodes: list[dict]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    exported_at = now_iso()
    intake_assets = []
    asset_objects = []
    works_by_title = {}
    nodes_by_title = {}

    for node in viewer_nodes:
        source_id = node.get("id")
        filename = node.get("filename")
        intake_id = f"asset:{str(filename or source_id).lower().replace(' ', '-').replace('.', '-')}"
        intake = {
            "id": intake_id,
            "sourceId": source_id,
            "filename": filename,
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
        intake_assets.append(intake)

        asset_objects.append({
            "id": intake_id,
            "type": "asset",
            "title": node.get("title_guess") or filename or str(source_id),
            "summary": f"Asset record for {node.get('title_guess') or filename or source_id}.",
            "status": "archived" if node.get("is_duplicate") else "active",
            "primaryContext": "personal" if node.get("owner_guess") == "personal" else "shared",
            "owners": [f"person:{(node.get('artist') or 'ewan').lower().replace(' ', '-')}"],
            "tags": [value for value in [node.get("category"), node.get("type_guess")] if value and value != "unknown"],
            "sourceRefs": [{"kind": "viewer", "ref": str(source_id)}],
            "relations": [],
            "memory": {"semantic": [], "episodic": [], "procedural": []},
            "timestamps": {
                "createdAt": node.get("created_at") or exported_at,
                "updatedAt": exported_at,
            },
        })

        work_title = node.get("related_work_guess")
        if work_title and work_title not in works_by_title:
            work_id = f"work:{work_title.lower().replace(' ', '-').replace('/', '-')}"
            works_by_title[work_title] = {"id": work_id, "type": "work", "title": work_title, "sourceRefs": []}
        if work_title:
            works_by_title[work_title]["sourceRefs"].append({"kind": "asset", "ref": intake_id})

        node_title = node.get("related_node_guess")
        if node_title and node_title not in nodes_by_title:
            node_id = f"node:{node_title.lower().replace(' ', '-').replace('/', '-')}"
            nodes_by_title[node_title] = {"id": node_id, "type": "node", "title": node_title, "sourceRefs": []}
        if node_title:
            nodes_by_title[node_title]["sourceRefs"].append({"kind": "asset", "ref": intake_id})

    return intake_assets, asset_objects, list(works_by_title.values()), list(nodes_by_title.values())
