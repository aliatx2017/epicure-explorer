# Next Session — Starting Point

**Branch:** `main`  
**Last commit:** Session 14 — Bug fix pass + im2recipe 35K nutritional integration  
**All 68 E2E tests pass · 0 console errors · 0 known bugs**

---

## Current State

| Metric | Value |
|--------|-------|
| `index.html` lines | **8,025** |
| JS functions | **~163** |
| Tabs | **19** (4 categories) |
| File size | **422 KB** |
| Console errors | **0** |
| Known bugs | **0** |
| E2E tests | **68/68 ✅** |
| Languages | EN, ES, FR, 中文, 日本語 |
| Nutrition data | **1,790 ingredients** (FSA per-100g) + **51,235 recipes** (per-recipe FSA) |

---

## What Session 14 Shipped

### Bug Fix Pass (14a)
| Fix | Severity | Detail |
|-----|----------|--------|
| **🐛 Missing `<div class="game-card">`** | 🔴 HIGH | Flavour Compass game-card div missing — added |
| **🐛 Dead GLP-1 intent chip** | 🔴 HIGH | `applyIntent('diet','glp1')` now calls `toggleGlpFilter()` |
| **🐛 roundRect polyfill** | 🔴 HIGH | Inline polyfill for older browsers |
| **🐛 Stale doc sizes** | 🟡 MEDIUM | GUIDE.md/README.md 259→408 KB |
| **🐛 Unused vars removed** | 🟡 MEDIUM | `pcaAnimationId`, `DENSITY_INFO_*` |
| **🐛 Missing CSS class** | 🟡 MEDIUM | `.spoon-recipe-grid` added |
| **🐛 Spoonacular limit** | 🟡 MEDIUM | Configurable via localStorage |
| **🐛 Test file fixes** | 🟡 MEDIUM | 19-tab loop, removed 4 redundant tests |

### im2recipe Nutritional Integration (14b)
| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🔬 | **`build_nutrition.py`** | USDA nutrition DB → im2recipe format with FSA traffic lights |
| **2** 📦 | **epicure_nutrition.json** | 789 KB, all 1,790 ingredients |
| **3** 🧠 | **FSA Health Direction** | `💚 FSA Health` in SLERP dropdown under `💪 Health` |
| **4** 🥗 | **Recipe Nutrition tab** | Per-recipe FSA traffic lights from im2recipe 35K dataset |
| **5** 📥 | **35K importer** | `build_nutrition.py --import-im2recipe` |
| **6** 🔗 | **Ingredient→Recipe index** | 622 ingredients → 157K recipe links |
| **7** 💾 | **Offline caching** | All nutrition data cached by Service Worker |

### Data Files Added

| File | Size | Description |
|------|------|-------------|
| `build_nutrition.py` | 45 KB | Python nutrition pipeline |
| `data/epicure_nutrition.json` | 789 KB | 1,790 ingredients, FSA per-100g |
| `data/nutrition_vocab.json` | 114 KB | im2recipe↔Epicure name mappings |
| `data/recipe_nutrition.json` | 98 MB | 51,235 per-recipe FSA records |
| `data/recipe_detections_slim.json` | 2.1 MB | 622-ingredient→recipe link index |
| `data/recipe_ingredient_map.json` | 5.7 MB | Full USDA-ingredient→recipe map |

---

## Open Items & Gaps for Next Session

### Unstarted Opportunities — Still Open
| Item | Effort | Notes |
|------|--------|-------|
| **Recipe generation (LLM)** | High | Needs backend — FastAPI/Node server, API key management, cost control |
| **Ingredient2Vec REST API** | High | Server-side project: auth, rate-limiting, billing |

### Test Coverage Gaps
| Area | Gap | Notes |
|------|-----|-------|
| 5 tabs lack feature tests | Snap, Neighbours, Compare, Modes, Recipes | Only "panel renders" checked |
| Error states untested | API 429/500, offline, model-not-loaded | Graceful paths, low risk |
| Nutrition tab untested | No E2E for FSA display or per-recipe data | New feature, manual check only |
| i18n coverage | Only Spanish tested; FR/zh/ja never verified | |

### Future Architectural Directions (Separate Project)
- Ingredient2Vec REST API + OpenAPI spec (requires server)
- Recipe generation via LLM (requires backend + API keys)
- Professional/Creator paid tier (requires auth, billing)
- Analytics dashboard (requires server logs or third-party service)

### im2recipe Data Cleanup
The `~/Downloads/` originals can be deleted:
- `det_ingrs.json` (345 MB) — ✅ Already processed into `recipe_detections_slim.json`
- `recipes_with_nutritional_info.json` (213 MB) — ✅ Already processed into `recipe_nutrition.json`
- `recipe1M_layers.tar.gz` (381 MB) — Not used by Epicure Explorer

---

## Quick Start

```bash
cd epicure-explorer
python3 -m http.server 8080
# Open http://localhost:8080
```

## Run Tests

```bash
cd epicure-explorer
node tests/e2e.mjs   # 68 tests, ~50s
```
