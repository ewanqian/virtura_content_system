
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export review CSV for quick manual review."""

import os
import csv

from export_utils import build_viewer_fallback_records, load_export_data

OUTPUT_DIR = "exports/review-sheets"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    payload = load_export_data()

    if payload["mode"] == "canonical":
        intake_assets = payload["intake_assets"]
    else:
        intake_assets, _, _, _ = build_viewer_fallback_records(payload["viewer_nodes"])

    output_path = os.path.join(OUTPUT_DIR, "assets_review.csv")

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID",
            "Filename",
            "Title (Guess)",
            "Year (Guess)",
            "Related Work (Guess)",
            "Related Node (Guess)",
            "Type (Guess)",
            "Category",
            "Owner",
            "Artist",
            "Featured",
            "Duplicate",
            "Notes",
            "Width",
            "Height",
            "Orientation"
        ])

        for intake in intake_assets:
            img_info = intake.get("imageInfo", {})
            writer.writerow([
                intake.get("id", ""),
                intake.get("filename", ""),
                intake.get("titleGuess", ""),
                intake.get("yearGuess", ""),
                intake.get("relatedWorkGuess", ""),
                intake.get("relatedNodeGuess", ""),
                intake.get("typeGuess", ""),
                intake.get("category", ""),
                intake.get("ownerGuess", ""),
                intake.get("artist", ""),
                "Yes" if intake.get("featuredCandidate") else "No",
                "Yes" if intake.get("isDuplicate") else "No",
                intake.get("notes", ""),
                img_info.get("width", ""),
                img_info.get("height", ""),
                img_info.get("orientation", "")
            ])

    print(f"✅ Exported review CSV with {len(intake_assets)} rows to {output_path}")

if __name__ == '__main__':
    main()
