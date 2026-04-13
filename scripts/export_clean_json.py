#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal public-safe example exporter for Node Weaver sample data.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "OBJECT_INVENTORY_SAMPLE.csv"
OUTDIR = ROOT / "exports"


def main() -> None:
    OUTDIR.mkdir(exist_ok=True)

    rows = list(csv.DictReader(SOURCE.open("r", encoding="utf-8")))
    works = [row for row in rows if row["type"] == "work"]
    nodes = [row for row in rows if row["type"] == "node"]

    payload = {
        "meta": {
            "kind": "public-safe-sample",
            "source": SOURCE.name,
        },
        "works": works,
        "nodes": nodes,
    }

    outpath = OUTDIR / "public_sample.json"
    outpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {outpath}")


if __name__ == "__main__":
    main()
