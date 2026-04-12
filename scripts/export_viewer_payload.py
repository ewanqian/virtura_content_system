#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a viewer payload for the local observation panel.
"""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

from export_utils import build_viewer_fallback_records, load_export_data, now_iso


OUTPUT_PATH = "viewer/data/library.json"


def main() -> None:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    payload = load_export_data()

    if payload["mode"] == "canonical":
        intake_assets = payload["intake_assets"]
        asset_objects = payload["assets"]
        works = payload["works"]
        nodes = payload["nodes"]
    else:
        intake_assets, asset_objects, works, nodes = build_viewer_fallback_records(payload["viewer_nodes"])

    intake_by_id = {record["id"]: record for record in intake_assets}
    works_by_id = {record["id"]: record for record in works}
    nodes_by_id = {record["id"]: record for record in nodes}

    work_asset_counts = Counter()
    node_asset_counts = Counter()
    asset_to_works = defaultdict(list)
    asset_to_nodes = defaultdict(list)

    for work in works:
        for source_ref in work.get("sourceRefs", []):
            if source_ref.get("kind") == "asset":
                asset_id = source_ref.get("ref")
                work_asset_counts[work["id"]] += 1
                asset_to_works[asset_id].append(work["id"])

    for node in nodes:
        for source_ref in node.get("sourceRefs", []):
            if source_ref.get("kind") == "asset":
                asset_id = source_ref.get("ref")
                node_asset_counts[node["id"]] += 1
                asset_to_nodes[asset_id].append(node["id"])

    viewer_assets = []
    for asset in asset_objects:
        intake = intake_by_id.get(asset["id"], {})
        related_work_ids = asset_to_works.get(asset["id"], [])
        related_node_ids = asset_to_nodes.get(asset["id"], [])
        viewer_assets.append({
            "id": asset.get("id"),
            "title": asset.get("title"),
            "summary": asset.get("summary"),
            "path": intake.get("path"),
            "filename": intake.get("filename"),
            "year": intake.get("yearGuess"),
            "date": intake.get("dateGuess"),
            "typeGuess": intake.get("typeGuess"),
            "category": intake.get("category"),
            "owner": intake.get("ownerGuess"),
            "artist": intake.get("artist"),
            "contributors": intake.get("contributors", []),
            "contributions": intake.get("contributions", []),
            "featured": intake.get("featuredCandidate", False),
            "isDuplicate": intake.get("isDuplicate", False),
            "notes": intake.get("notes"),
            "imageInfo": intake.get("imageInfo"),
            "status": asset.get("status"),
            "relatedWorkIds": related_work_ids,
            "relatedWorks": [works_by_id[work_id]["title"] for work_id in related_work_ids if work_id in works_by_id],
            "relatedNodeIds": related_node_ids,
            "relatedNodes": [nodes_by_id[node_id]["title"] for node_id in related_node_ids if node_id in nodes_by_id],
            "timestamps": asset.get("timestamps", {}),
        })

    viewer_works = []
    for work in works:
        work_asset_ids = [ref.get("ref") for ref in work.get("sourceRefs", []) if ref.get("kind") == "asset"]
        related_node_ids = sorted({
            node_id
            for node_id, node in nodes_by_id.items()
            if any(ref.get("ref") in work_asset_ids for ref in node.get("sourceRefs", []) if ref.get("kind") == "asset")
        })
        years = sorted({intake_by_id[asset_id].get("yearGuess") for asset_id in work_asset_ids if asset_id in intake_by_id and intake_by_id[asset_id].get("yearGuess")})
        viewer_works.append({
            "id": work.get("id"),
            "title": work.get("title"),
            "summary": work.get("summary"),
            "assetCount": len(work_asset_ids),
            "featuredCount": sum(1 for asset_id in work_asset_ids if intake_by_id.get(asset_id, {}).get("featuredCandidate")),
            "duplicateCount": sum(1 for asset_id in work_asset_ids if intake_by_id.get(asset_id, {}).get("isDuplicate")),
            "years": years,
            "nodeIds": related_node_ids,
            "nodeTitles": [nodes_by_id[node_id]["title"] for node_id in related_node_ids if node_id in nodes_by_id],
        })

    viewer_nodes = []
    for node in nodes:
        asset_ids = [ref.get("ref") for ref in node.get("sourceRefs", []) if ref.get("kind") == "asset"]
        viewer_nodes.append({
            "id": node.get("id"),
            "title": node.get("title"),
            "summary": node.get("summary"),
            "assetCount": len(asset_ids),
            "workIds": sorted({work_id for asset_id in asset_ids for work_id in asset_to_works.get(asset_id, [])}),
        })

    category_counts = Counter(asset.get("category") or "unknown" for asset in viewer_assets)
    owner_counts = Counter(asset.get("owner") or "unknown" for asset in viewer_assets)

    out = {
        "meta": {
            "generatedAt": now_iso(),
            "assetCount": len(viewer_assets),
            "workCount": len(viewer_works),
            "nodeCount": len(viewer_nodes),
        },
        "metrics": {
            "featuredCount": sum(1 for asset in viewer_assets if asset.get("featured")),
            "duplicateCount": sum(1 for asset in viewer_assets if asset.get("isDuplicate")),
            "publicReadyCount": sum(1 for asset in viewer_assets if asset.get("typeGuess") in ["public node", "poster", "hero"]),
            "categoryCounts": dict(category_counts),
            "ownerCounts": dict(owner_counts),
        },
        "works": viewer_works,
        "nodes": viewer_nodes,
        "assets": viewer_assets,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported viewer payload to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
