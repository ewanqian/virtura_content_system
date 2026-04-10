
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export clean JSON data for website and portfolio.
"""

import os
import json
from datetime import datetime

NODES_PATH = 'viewer/data/nodes.json'
OUTPUT_DIR = 'exports/website'

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(NODES_PATH):
        print(f"⚠️  Nodes file not found at {NODES_PATH}")
        return
    
    with open(NODES_PATH, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    clean_nodes = []
    for node in nodes:
        clean_node = {
            'id': node.get('id'),
            'type': 'asset',
            'filename': node.get('filename'),
            'title': node.get('title_guess', node.get('filename')),
            'caption': node.get('notes', ''),
            'year': node.get('year_guess'),
            'related_work': node.get('related_work_guess'),
            'related_node': node.get('related_node_guess'),
            'owner': node.get('owner_guess'),
            'artist': node.get('artist', 'Ewan'),
            'category': node.get('category'),
            'featured': node.get('featured_candidate', False),
            'is_duplicate': node.get('is_duplicate', False),
            'image_info': node.get('image_info'),
            'created_at': node.get('created_at'),
            'exported_at': datetime.now().isoformat()
        }
        clean_nodes.append(clean_node)
    
    output_path = os.path.join(OUTPUT_DIR, 'assets.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(clean_nodes, f, ensure_ascii=False, indent=2)
    
    works = {}
    for node in nodes:
        work = node.get('related_work_guess')
        if work and work not in works:
            works[work] = {
                'id': work.lower().replace(' ', '-'),
                'type': 'work',
                'title': work,
                'assets': []
            }
        if work:
            works[work]['assets'].append(node.get('id'))
    
    works_list = list(works.values())
    works_path = os.path.join(OUTPUT_DIR, 'works.json')
    with open(works_path, 'w', encoding='utf-8') as f:
        json.dump(works_list, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Exported {len(clean_nodes)} assets to {output_path}")
    print(f"✅ Exported {len(works_list)} works to {works_path}")

if __name__ == '__main__':
    main()

