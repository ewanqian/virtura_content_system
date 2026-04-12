
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export clean JSON data for website and portfolio."""

import os
import json

from export_utils import build_viewer_fallback_records, load_export_data, now_iso

OUTPUT_DIR = "exports/website"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    payload = load_export_data()

    if payload["mode"] == "canonical":
        intake_assets = payload["intake_assets"]
        asset_objects = payload["assets"]
        works = payload["works"]
        nodes = payload["nodes"]
    else:
        intake_assets, asset_objects, works, nodes = build_viewer_fallback_records(payload["viewer_nodes"])

    intake_by_id = {record["id"]: record for record in intake_assets}
    exported_at = now_iso()

    clean_assets = []
    for asset in asset_objects:
        intake = intake_by_id.get(asset["id"], {})
        related_works = [rel["target"] for rel in asset.get("relations", []) if rel.get("type") == "documents" and rel.get("target", "").startswith("work:")]
        related_nodes = [rel["target"] for rel in asset.get("relations", []) if rel.get("type") == "documents" and rel.get("target", "").startswith("node:")]
        clean_assets.append({
            "id": asset.get("id"),
            "type": asset.get("type"),
            "filename": intake.get("filename"),
            "path": intake.get("path"),
            "title": asset.get("title"),
            "summary": asset.get("summary"),
            "caption": intake.get("notes"),
            "year": intake.get("yearGuess"),
            "related_works": related_works,
            "related_nodes": related_nodes,
            "owner": intake.get("ownerGuess"),
            "artist": intake.get("artist"),
            "contributors": intake.get("contributors", []),
            "category": intake.get("category"),
            "featured": intake.get("featuredCandidate", False),
            "is_duplicate": intake.get("isDuplicate", False),
            "image_info": intake.get("imageInfo"),
            "created_at": asset.get("timestamps", {}).get("createdAt"),
            "updated_at": asset.get("timestamps", {}).get("updatedAt"),
            "exported_at": exported_at,
        })

    clean_works = []
    for work in works:
        source_refs = work.get("sourceRefs", [])
        clean_works.append({
            "id": work.get("id"),
            "type": work.get("type"),
            "title": work.get("title"),
            "summary": work.get("summary"),
            "asset_ids": [ref.get("ref") for ref in source_refs if ref.get("kind") == "asset"],
            "exported_at": exported_at,
        })

    clean_nodes = []
    for node in nodes:
        source_refs = node.get("sourceRefs", [])
        clean_nodes.append({
            "id": node.get("id"),
            "type": node.get("type"),
            "title": node.get("title"),
            "summary": node.get("summary"),
            "asset_ids": [ref.get("ref") for ref in source_refs if ref.get("kind") == "asset"],
            "exported_at": exported_at,
        })

    for filename, records in [
        ("assets.json", clean_assets),
        ("works.json", clean_works),
        ("nodes.json", clean_nodes),
    ]:
        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported {len(clean_assets)} assets")
    print(f"✅ Exported {len(clean_works)} works")
    print(f"✅ Exported {len(clean_nodes)} nodes")

if __name__ == '__main__':
    main()
