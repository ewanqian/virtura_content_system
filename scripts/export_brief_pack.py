
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export markdown brief pack for agent workflows."""

import os
import json

from export_utils import build_viewer_fallback_records, load_export_data, now_iso

OUTPUT_DIR = "exports/brief-packs"

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
    assets_by_id = {record["id"]: record for record in asset_objects}
    nodes_by_id = {record["id"]: record for record in nodes}
    exported_at = now_iso()

    for work in works:
        work_id = work.get("id")
        work_title = work.get("title")
        work_slug = work_id.split(":", 1)[-1]
        pack_dir = os.path.join(OUTPUT_DIR, work_slug)
        os.makedirs(pack_dir, exist_ok=True)

        asset_ids = [ref.get("ref") for ref in work.get("sourceRefs", []) if ref.get("kind") == "asset"]
        work_intake = [intake_by_id[asset_id] for asset_id in asset_ids if asset_id in intake_by_id]
        related_node_ids = sorted({
            relation.get("target")
            for asset_id in asset_ids
            for relation in assets_by_id.get(asset_id, {}).get("relations", [])
            if relation.get("type") == "documents" and relation.get("target", "").startswith("node:")
        })
        featured_assets = [record for record in work_intake if record.get("featuredCandidate")]
        public_assets = [record for record in work_intake if record.get("typeGuess") in ["public node", "poster", "hero"]]
        years = sorted({record.get("yearGuess") for record in work_intake if record.get("yearGuess")})

        brief_content = f"""# Project Brief Pack: {work_title}

## Project
{work_title}

## Current Status
- canonical work id: {work_id}
- total assets: {len(work_intake)}
- featured assets: {len(featured_assets)}
- public-ready assets: {len(public_assets)}
- related nodes: {len(related_node_ids)}
- years: {', '.join(years) if years else 'Unknown'}

## Related Nodes
"""
        if related_node_ids:
            for node_id in related_node_ids:
                node = nodes_by_id.get(node_id, {})
                brief_content += f"- {node.get('title', node_id)} ({node_id})\n"
        else:
            brief_content += "- none yet\n"

        brief_content += "\n## Key Assets\n"
        for i, intake in enumerate(work_intake[:10], 1):
            brief_content += f"{i}. {intake.get('titleGuess') or intake.get('filename')}\n"
            brief_content += f"   - Asset ID: {intake.get('id')}\n"
            brief_content += f"   - Type Guess: {intake.get('typeGuess', 'unknown')}\n"
            brief_content += f"   - Featured: {'Yes' if intake.get('featuredCandidate') else 'No'}\n"
            brief_content += f"   - Category: {intake.get('category', 'unknown')}\n"

        brief_content += f"""
## Suggested Uses
- homepage hero
- project page
- media kit
- review sheet
- social post reference

## Questions for Agent
- Which assets are strongest for homepage use?
- Which ones are duplicate or weaker?
- Which ones should be kept for archive only?
- What wording is suitable for a project page based on these materials?

---
Generated at: {exported_at}
"""

        with open(os.path.join(pack_dir, "brief.md"), "w", encoding="utf-8") as f:
            f.write(brief_content)

        pack_payload = {
            "work": work,
            "nodes": [nodes_by_id[node_id] for node_id in related_node_ids if node_id in nodes_by_id],
            "assets": [assets_by_id[asset_id] for asset_id in asset_ids if asset_id in assets_by_id],
            "intake_assets": work_intake,
        }
        with open(os.path.join(pack_dir, "pack.json"), "w", encoding="utf-8") as f:
            json.dump(pack_payload, f, ensure_ascii=False, indent=2)

        print(f"✅ Exported brief pack for '{work_title}' to {pack_dir}")

    print(f"\n📦 Total: {len(works)} brief packs exported")

if __name__ == '__main__':
    main()
