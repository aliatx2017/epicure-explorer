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
| `index.html` lines | **~8,459** |
| JS functions | **~207** (named + nested) |
| Tabs | **19** (4 categories) |
| File size | **~444 KB** |
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

## 📋 Unstarted Features — Full Todo

All known client-side limitations are resolved. These are the **next things to build**, sourced from GUIDE.md §4.9, ANALYSIS.md §5, and FOOD_AI_RESEARCH_PLAN.md.

### 🔧 Client-Side (no server needed)

| # | Feature | Source | Effort | Notes |
|---|---------|--------|--------|-------|
| 1 | **Ingredient Direction Arithmetic** — "Add truffle flavour to risotto without truffle": vector arithmetic `risotto + (truffle - mushroom)` | GUIDE.md §4.9 | Low | Reuses existing SLERP + neighbour infrastructure |
| 2 | **Graph-RAG Chef Assistant** — natural-language query over full embedding space: "What replaces eggs in a gluten-free brunch?" | GUIDE.md §4.9 | Medium | Could be a search-like UI over modes + neighbours |
| 3 | **MCP-Native Architecture** — expose the embedding space as an MCP server so any AI assistant can query your food layer | GUIDE.md §4.9 | Medium | Standalone server exposing ingredient lookup + SLERP |
| 4 | **Continuous Model Mixing** — slider blending Cooc/Core/Chem into a tunable chemistry-recipe axis | ANALYSIS.md §5 | Medium | Interpolate between model vectors at query time |
| 5 | **Richer SLERP Operators** — intra-mode interpolation, multidirection blends, constrained traversal ("rotate toward Mediterranean *but stay in dairy mode*") | ANALYSIS.md §5 | Medium-High | Requires mode-membership filtering on SLERP results |
| 6 | **Real-Time Trend Integration** — pull trending ingredient signals from Tastewise/industry APIs | GUIDE.md §4.9 | Medium | Needs API key / data source |
| 7 | **Cross-Modal Grounding** — cross from ingredient space into recipe-text, image, or sensory-descriptor space | ANALYSIS.md §5 | High | Research-phase, fundamentally new data modality |

### 📸 Photo / Image Features

| # | Feature | Source | Effort | Notes |
|---|---------|--------|--------|-------|
| 8 | **Photo-to-Nutrition** — photograph a plated dish → ingredient mass estimation → nutritional breakdown | GUIDE.md §4.9 | High | Needs ML model (NutriFusionNet GAIE architecture) |
| 9 | **3D Photo→Nutrition** — PerBite-style: snap a plate → 3D mesh → volume → calorie/nutrient estimation | FOOD_AI_RESEARCH_PLAN.md (P2) | Very High | Needs 3D model |

### 🧪 Recipe / LLM Features (needs LLM or external API)

| # | Feature | Source | Effort | Notes |
|---|---------|--------|--------|-------|
| 10 | **RecipeCrit Integration** — paste a recipe → ingredient-level critiques and rewrite suggestions | FOOD_AI_RESEARCH_PLAN.md (P2) | High | Needs LLM integration |
| 11 | **Fermentation AI** — predict fermentation outcomes for sourdough, kimchi, kombucha from ingredient inputs | FOOD_AI_RESEARCH_PLAN.md (P2) | Very High | Emerging research area |

### ❌ Cancelled (needs backend server)

| Item | Reason |
|------|--------|
| ~~LLM Recipe Generation~~ | Cancelled — requires backend infrastructure |
| ~~Ingredient2Vec REST API~~ | Cancelled — requires backend infrastructure |
| ~~Personalized Food Agent~~ | Cancelled — requires backend infrastructure |

### ✅ Resolved This Session

- ~~Cuisine direction vector heuristic~~ → GMM mode-atlas based
- ~~Inline SEASONAL_DATA / NUTRITION_DATA drift~~ → Guarded by `tools/check-fallbacks.mjs`

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
