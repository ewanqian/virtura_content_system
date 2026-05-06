#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a staged selection manifest for Drop Flow wave 01.

This pass is intentionally heuristic-first:
- it works from the approval queue inventory
- it does not require the archive source path to be mounted
- it groups media into review buckets for later selective copy
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "data" / "intake" / "content_approval_queue.json"
JSON_OUTPUT = ROOT / "data" / "intake" / "drop_flow_wave01_staging.json"
MD_OUTPUT = ROOT / "docs" / "DROP_FLOW_WAVE01_STAGING_2026-05-07.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_drop_flow_item() -> dict:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    return next(item for item in queue["items"] if item["bundleId"] == "drop-flow-pack")


def classify_image(display_path: str) -> tuple[str, str, str]:
    name = display_path.split("/")[-1]
    if "/图片/现场拍摄/" in display_path and name.startswith("IMG_"):
        return (
            "现场拍摄-相机原图",
            "keep",
            "优先保留为现场文档层，可后续再选封面与现场代表图。",
        )
    if re.fullmatch(r"\d+\.png", name):
        return (
            "编号渲染图",
            "review-hero",
            "优先作为主视觉候选，需要后续补人工质量评分。",
        )
    if "UFO TERMINAL CREATION CAMP" in name and "mov_" in name:
        return (
            "创作营视频抽帧",
            "collapse-sequence",
            "序列性很强，建议后续按片段折叠，只保留少量关键帧。",
        )
    if name.startswith("IMG_") and "mov_" in name:
        return (
            "手机视频抽帧",
            "collapse-sequence",
            "保留少量关键帧即可，其他可视作过程抽帧。",
        )
    if re.fullmatch(r"[0-9a-f]{32}\.(jpeg|jpg|png)", name, re.I):
        return (
            "哈希命名散图",
            "manual-review",
            "缺少语义命名，建议人工复核后再决定是否保留。",
        )
    if name.startswith("微信图片_"):
        return (
            "微信导出图",
            "manual-review",
            "来源语义弱，建议人工确认是否只是临时流转截图。",
        )
    return (
        "其他图像",
        "manual-review",
        "暂不自动归并，留给人工再判。",
    )


def build_payload() -> dict:
    item = load_drop_flow_item()
    groups: dict[str, dict] = defaultdict(
        lambda: {"decision": "", "reason": "", "count": 0, "files": []}
    )

    for image in item.get("imageFiles", []):
        label, decision, reason = classify_image(image["displayPath"])
        group = groups[label]
        group["decision"] = decision
        group["reason"] = reason
        group["count"] += 1
        group["files"].append(image["displayPath"])

    ordered_labels = [
        "现场拍摄-相机原图",
        "编号渲染图",
        "创作营视频抽帧",
        "手机视频抽帧",
        "哈希命名散图",
        "微信导出图",
        "其他图像",
    ]

    categories = []
    for label in ordered_labels:
        if label not in groups:
            continue
        group = groups[label]
        categories.append(
            {
                "label": label,
                "decision": group["decision"],
                "reason": group["reason"],
                "count": group["count"],
                "sampleFiles": group["files"][:10],
                "files": group["files"],
            }
        )

    return {
        "generatedAt": now_iso(),
        "bundleId": item["bundleId"],
        "workId": "work:drop-flow",
        "approvalStatus": item["status"],
        "intakeClass": item["intakeClass"],
        "sourcePaths": item["sourcePaths"],
        "operatorNote": item.get("reviewNotes", ""),
        "summary": {
            "imageCount": item.get("imageFileCount", 0),
            "categoryCount": len(categories),
        },
        "categories": categories,
        "nextActions": [
            "先人工复核 `编号渲染图`，补一轮主视觉质量评分。",
            "从 `现场拍摄-相机原图` 中挑现场代表图，用于版本节点与工作线文档。",
            "把 `创作营视频抽帧` 与 `手机视频抽帧` 折叠为少量关键帧，而不是整包直入。",
            "对 `哈希命名散图` 与 `微信导出图` 做人工去语义噪音判断。",
        ],
    }


def write_markdown(payload: dict) -> None:
    lines = [
        "# Drop Flow Wave 01 Staging",
        "",
        "## Scope",
        "",
        "- work: `work:drop-flow`",
        f"- approval status: `{payload['approvalStatus']}`",
        f"- intake class: `{payload['intakeClass']}`",
        f"- total images: `{payload['summary']['imageCount']}`",
        "",
        "## Operator Note",
        "",
        payload["operatorNote"] or "无补充备注。",
        "",
        "## Category Split",
        "",
    ]

    for category in payload["categories"]:
        lines.extend(
            [
                f"### `{category['label']}`",
                "",
                f"- decision: `{category['decision']}`",
                f"- count: `{category['count']}`",
                f"- rationale: {category['reason']}",
                "- sample files:",
            ]
        )
        for sample in category["sampleFiles"]:
            lines.append(f"  - `{sample}`")
        lines.append("")

    lines.extend(
        [
            "## Next Actions",
            "",
        ]
    )
    for action in payload["nextActions"]:
        lines.append(f"- {action}")
    lines.append("")

    MD_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    payload = build_payload()
    JSON_OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(payload)
    print(f"Wrote {JSON_OUTPUT}")
    print(f"Wrote {MD_OUTPUT}")
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
