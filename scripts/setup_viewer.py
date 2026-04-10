
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copy images and prepare nodes.json for Node Library viewer.
"""

import os
import json
import shutil

SOURCE_IMAGES_DIR = '/Users/ewanqian/Documents/Sync/image-library/data/assets/processed'
SOURCE_NODES_PATH = '/Users/ewanqian/Documents/Sync/image-library/app/cms/data/nodes.json'

TARGET_IMAGES_DIR = 'viewer/data/images'
TARGET_NODES_PATH = 'viewer/data/nodes.json'

def main():
    os.makedirs(TARGET_IMAGES_DIR, exist_ok=True)
    
    if os.path.exists(SOURCE_NODES_PATH):
        with open(SOURCE_NODES_PATH, 'r', encoding='utf-8') as f:
            nodes = json.load(f)
        
        for node in nodes:
            if 'path' in node:
                filename = os.path.basename(node['path'])
                node['path'] = f'data/images/{filename}'
                
                src_path = os.path.join(SOURCE_IMAGES_DIR, filename)
                dst_path = os.path.join(TARGET_IMAGES_DIR, filename)
                
                if os.path.exists(src_path) and not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
        
        with open(TARGET_NODES_PATH, 'w', encoding='utf-8') as f:
            json.dump(nodes, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Prepared {len(nodes)} nodes in {TARGET_NODES_PATH}")
    else:
        print(f"⚠️  Source nodes not found at {SOURCE_NODES_PATH}")
        with open(TARGET_NODES_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

