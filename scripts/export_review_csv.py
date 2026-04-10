
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export review CSV for quick manual review.
"""

import os
import json
import csv

NODES_PATH = 'viewer/data/nodes.json'
OUTPUT_DIR = 'exports/review-sheets'

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(NODES_PATH):
        print(f"⚠️  Nodes file not found at {NODES_PATH}")
        return
    
    with open(NODES_PATH, 'r', encoding='utf-8') as f:
        nodes = json.load(f)
    
    output_path = os.path.join(OUTPUT_DIR, 'assets_review.csv')
    
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'ID',
            'Filename',
            'Title (Guess)',
            'Year (Guess)',
            'Related Work (Guess)',
            'Related Node (Guess)',
            'Type (Guess)',
            'Category',
            'Owner',
            'Artist',
            'Featured',
            'Duplicate',
            'Notes',
            'Width',
            'Height',
            'Orientation'
        ])
        
        for node in nodes:
            img_info = node.get('image_info', {})
            writer.writerow([
                node.get('id', ''),
                node.get('filename', ''),
                node.get('title_guess', ''),
                node.get('year_guess', ''),
                node.get('related_work_guess', ''),
                node.get('related_node_guess', ''),
                node.get('type_guess', ''),
                node.get('category', ''),
                node.get('owner_guess', ''),
                node.get('artist', ''),
                'Yes' if node.get('featured_candidate') else 'No',
                'Yes' if node.get('is_duplicate') else 'No',
                node.get('notes', ''),
                img_info.get('width', ''),
                img_info.get('height', ''),
                img_info.get('orientation', '')
            ])
    
    print(f"✅ Exported review CSV with {len(nodes)} rows to {output_path}")

if __name__ == '__main__':
    main()

