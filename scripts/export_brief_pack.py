
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export markdown brief pack for agent workflows.
"""

import os
import json
from datetime import datetime

NODES_PATH = 'viewer/data/nodes.json'
OUTPUT_DIR = 'exports/brief-packs'

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(NODES_PATH):
        print(f"⚠️  Nodes file not found at {NODES_PATH}")
        return
    
    with open(NODES_PATH, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    works = {}
    for node in nodes:
        work = node.get('related_work_guess')
        if work and work not in works:
            works[work] = []
        if work:
            works[work].append(node)
    
    for work_name, work_nodes in works.items():
        work_slug = work_name.lower().replace(' ', '-').replace('/', '-')
        pack_dir = os.path.join(OUTPUT_DIR, work_slug)
        os.makedirs(pack_dir, exist_ok=True)
        
        featured_nodes = [n for n in work_nodes if n.get('featured_candidate')]
        public_nodes = [n for n in work_nodes if n.get('type_guess') in ['public node', 'poster', 'hero']]
        years = list(set([n.get('year_guess') for n in work_nodes if n.get('year_guess')]))
        
        brief_content = f"""# Project Brief Pack: {work_name}

## Project
{work_name}

## Current Status
- total assets: {len(work_nodes)}
- featured assets: {len(featured_nodes)}
- public-ready assets: {len(public_nodes)}
- years: {', '.join(years) if years else 'Unknown'}

## Key Assets
"""
        for i, node in enumerate(work_nodes[:10], 1):
            brief_content += f"{i}. {node.get('title_guess', node.get('filename'))}\n"
            brief_content += f"   - Type: {node.get('type_guess', 'unknown')}\n"
            brief_content += f"   - Featured: {'Yes' if node.get('featured_candidate') else 'No'}\n"
            brief_content += f"   - Category: {node.get('category', 'unknown')}\n"
        
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
Generated at: {datetime.now().isoformat()}
"""
        
        brief_path = os.path.join(pack_dir, 'brief.md')
        with open(brief_path, 'w', encoding='utf-8') as f:
            f.write(brief_content)
        
        nodes_path = os.path.join(pack_dir, 'nodes.json')
        with open(nodes_path, 'w', encoding='utf-8') as f:
            json.dump(work_nodes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exported brief pack for '{work_name}' to {pack_dir}")
    
    print(f"\n📦 Total: {len(works)} brief packs exported")

if __name__ == '__main__':
    main()

