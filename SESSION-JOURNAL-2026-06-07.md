# Epicure Explorer — Session Journal (2026-06-07)

**Agent:** Reasonix (DeepSeek Flash)
**Project:** `/Users/alex.maksimchuk/projects/playground/epicure-explorer`
**Duration:** Single session, ~2 hours

## Context

Started from a code review of the Epicure Explorer — an interactive single-page web app for exploring 300-D food ingredient embeddings (arXiv:2605.22391). The review had 6 actionable items plus 3 "remaining gaps" the session itself identified.

## What Changed

### Phase 1 — Core Feedback (initial 6 items)

| # | Item | Fix |
|---|---|---|
| 1 | "Is preprocess.py doing real computation?" | Answered inline: L2 norm, 3.2M-pair similarity, k-NN, UMAP, direction vectors — real non-trivial preprocessing |
| 2 | "PCA loses too much info" | Replaced with UMAP (cosine metric, 15 neighbours). Added .venv + `requirements.txt` |
| 3 | "Only 8 sensory directions, missing paper's 8 cuisine probes" | Added 8 cuisine macro-region direction vectors with curated keyword lists (25–40 ingredients each). Later refined with NN expansion |
| 4 | "Mode atlas 150–200 modes with no filtering" | Added text label filter + min-members dropdown + live count |
| 5 | "Section 5.8 is a dev artifact" | Stripped the Reasonix nil-pointer workaround from GUIDE.md entirely |
| 6 | "12 MB upfront load is painful" | Split into 4 files: 128 KB shared (loaded first) + 3× ~4 MB per-model (lazy-loaded on tab switch) |

### Phase 2 — Gaps Identified and Fixed (3 items)

| # | Gap | Fix |
|---|---|---|
| 1 | Cuisine directions were heuristic keyword centroids | Added embedding-space NN expansion (cosine ≥ 0.4 threshold) from seed centroid — propagates cuisine labels through the embedding, typically doubles ingredient coverage per cuisine |
| 2 | No way to search for an ingredient across all modes | Added cross-mode ingredient search field with partial matching, purple highlighting, result sorting |
| 3 | UMAP coordinates not reproducible across library upgrades | `requirements.txt` with pinned versions; `_metadata` in each JSON stores `umap_version`, `sklearn_version`, `proj.params`; data frozen at generation time |

### Phase 3 — Documentation

- `SESSION-2026-06-07.md` — full technical summary with architecture decisions
- `GUIDE.md` — updated pipeline diagrams, data table, feature walkthroughs, rebuild instructions
- `ANALYSIS.md` — unchanged (paper analysis, no web-app changes needed)

## Key Architecture Decisions

- **UMAP over t-SNE**: global structure preservation, 3× faster, deterministic
- **4-file split over streaming**: zero-dependency, cache-friendly, right granularity
- **base64 float32 packing**: 2.5:1 compression vs raw CSV, browser-native decode, no deps
- **NN-expanded cuisine directions**: recovers paper's intent without Claude-tagged probe vectors
- **Pinned requirements.txt**: coordinates frozen at generation time, version metadata for debugging

## File Inventory (at session end)

```
epicure-explorer/
├── index.html               ~43 KB   (1069 lines)  — web app
├── preprocess.py             ~19 KB   (479 lines)   — data pipeline
├── requirements.txt          ~99 B    (6 lines)     — pinned deps
├── ANALYSIS.md               ~10 KB   (195 lines)   — paper analysis
├── GUIDE.md                  ~22 KB   (476 lines)   — user guide
├── SESSION-2026-06-07.md     ~10 KB                  — tech summary
├── SESSION-JOURNAL-2026-06-07.md  — this file
└── data/
    ├── epicure_shared.json   ~128 KB                  — ingredients + directions
    ├── epicure_cooc.json     ~4.0 MB                  — Cooc model data
    ├── epicure_core.json     ~4.1 MB                  — Core model data
    └── epicure_chem.json     ~4.0 MB                  — Chem model data
```

## To Launch

```bash
cd epicure-explorer && python3 -m http.server 8080
# Open http://localhost:8080
```

## To Rebuild Data Bundle

```bash
cd epicure-explorer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 preprocess.py   # ~3-5 min (UMAP bottleneck)
```
