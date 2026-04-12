#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run the MVP content pipeline end-to-end.
"""

from __future__ import annotations

import subprocess
import sys


STEPS = [
    ("normalize", "scripts/normalize_intake_to_objects.py"),
    ("export viewer payload", "scripts/export_viewer_payload.py"),
    ("export website", "scripts/export_clean_json.py"),
    ("export review csv", "scripts/export_review_csv.py"),
    ("export brief packs", "scripts/export_brief_pack.py"),
]


def main() -> int:
    for label, script in STEPS:
        print(f"\n==> {label}: {script}")
        result = subprocess.run([sys.executable, script], check=False)
        if result.returncode != 0:
            print(f"\nPipeline stopped at step: {label}")
            return result.returncode

    print("\nPipeline completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
