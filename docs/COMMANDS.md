# Commands

## Main MVP pipeline

Run the whole local pipeline:

```bash
python3 scripts/build_pipeline.py
```

## Individual steps

Normalize intake records into canonical objects:

```bash
python3 scripts/normalize_intake_to_objects.py
```

Export clean website payloads:

```bash
python3 scripts/export_clean_json.py
```

Export viewer payload:

```bash
python3 scripts/export_viewer_payload.py
```

Export review CSV:

```bash
python3 scripts/export_review_csv.py
```

Export brief packs:

```bash
python3 scripts/export_brief_pack.py
```

## Recommended usage rhythm

1. put new material into `incoming/`
2. run `python3 scripts/build_pipeline.py`
3. inspect outputs in `exports/`
4. open the viewer for visual review
5. tell Codex what to revise
