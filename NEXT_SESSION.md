# Next Session — Starting Point

**Branch:** `main`  
**Last commit:** (session 19)  
**All 80 E2E tests pass · 0 console errors · 0 known bugs · Working tree clean**

---

## What Session 19 Shipped

**Cuisine direction vectors** — replaced heuristic keyword-list approximation with Core model GMM mode-atlas members. This resolves the documented "future work" limitation from `SESSION-2026-06-07.md` line 111.

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🧮 | **`tools/compute_cuisine_directions.py`** | Standalone script mapping 194 Core GMM modes to 8 cuisine macro-regions, collecting member ingredients, computing centroid vectors. |
| **2** 🔧 | **`preprocess.py` updated** | `compute_directions()` now accepts `mode_atlas_path` argument; uses mode membership instead of keyword + NN expansion. |
| **3** ✅ | **`epicure_shared.json` updated** | 8 cuisine direction vectors recomputed. Sensory directions unchanged. Metadata: `direction_method = "mode-atlas + keyword seeds"`. |
| **4** 🧪 | **80/80 E2E ✅** | All tests pass with new direction vectors. |

### Cuisine Mode Coverage

| Cuisine | Modes | Members | Method |
|---------|-------|---------|--------|
| East Asian | 46 | 951 | Mode atlas |
| Western Atlantic | 8 | 447 | Mode atlas |
| Mediterranean | 20 | 737 | Mode atlas |
| Eastern European | 3 | 102 | Modes + 11 keyword seeds |
| Southeast Asian | 4 | 380 | Mode atlas |
| South Asian | 2 | 75 | Modes + 21 keyword seeds |
| Latin American | 14 | 542 | Mode atlas |
| Japanese | 1 | 72 | Mode + 33 keyword seeds |

### Files Modified

| File | Change |
|------|--------|
| `tools/compute_cuisine_directions.py` | **Created** — 15 KB standalone script for mode-atlas cuisine direction generation |
| `preprocess.py` | `compute_directions()` signature changed: now takes optional `mode_atlas_path`. Added `CUISINE_MODE_IDS`, `CUISINE_SEEDS`, `load_mode_atlas()`, `_fallback_cuisine_directions()`. |
| `data/epicure_shared.json` | 8 cuisine direction vectors replaced. Metadata updated. SW cache key regenerated. |
| `sw.js` | Cache key: `'epicure-25e8f4a27cf8'` |
| `SESSION_JOURNAL.md` | Session 19 entry added |
| `NEXT_SESSION.md` | Full rewrite for this session |

---

## Current State

| Metric | Value |
|--------|-------|
| `index.html` lines | **~8,293** |
| JS functions | **~202** (named + nested) |
| Tabs | **19** (4 categories) |
| File size | **~435 KB** |
| Console errors | **0** |
| Known bugs | **0** |
| E2E tests | **80/80 ✅** |
| Languages | EN, ES, FR, 中文, 日本語 (all verified in E2E) |
| Nutrition data | **1,790 ingredients** (FSA per-100g) + **51,235 recipes** (per-recipe FSA) |
| Cuisine directions | **GMM mode-atlas based** — replaces heuristic keyword lists |
| Sensory directions | **Keyword centroid** (unchanged, 8 directions) |
| CSS | **~686 lines** |
| JavaScript (script block) | **~6,814 lines** |
| SW cache key | `'epicure-25e8f4a27cf8'` — content-hash derived, auto-invalidates |

---

## What's Next

All known client-side limitations are resolved. No remaining open items:

- ~~Tier 3~~ (cancelled — requires backend infrastructure)
- ~~Cuisine direction vector heuristic~~ ✅ Resolved — now mode-atlas based
- ~~Inline SEASONAL_DATA / NUTRITION_DATA drift~~ ✅ Guarded by `tools/check-fallbacks.mjs`

If you want to start fresh feature work, consider the future directions from `GUIDE.md` §4.9 (Ingredient Direction Arithmetic, Photo-to-Nutrition, Graph-RAG Chef Assistant, MCP-Native Architecture).

---

## Quick Start

```bash
cd epicure-explorer
python3 -m http.server 8080
# Open http://localhost:8080
```

### After changing data files, index.html, or sw.js

```bash
node tools/version-sw.js            # Updates sw.js cache key
node tools/check-fallbacks.mjs       # Verifies inline fallbacks haven't drifted
```

### To regenerate cuisine direction vectors

```bash
python3 tools/compute_cuisine_directions.py
node tools/version-sw.js
```

### Full data reprocess

```bash
python3 preprocess.py                # Full pipeline (embeddings → JSON)
node tools/version-sw.js
```

### Run Tests

```bash
node tests/e2e.mjs                   # 80 tests, ~60s
```
