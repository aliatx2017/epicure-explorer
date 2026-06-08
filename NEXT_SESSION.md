# Next Session — Starting Point

**Branch:** `main`  
**Last commit:** Session 13 — TheMealDB + TheCocktailDB + 200-area labels  
**All 72 E2E tests pass · 0 console errors · 0 known bugs**

---

## Current State

| Metric | Value |
|--------|-------|
| `index.html` lines | **7,756** |
| JS functions | **~168** |
| Tabs | **19** (4 categories) |
| File size | **408 KB** |
| Console errors | **0** |
| Known bugs | **0** |
| E2E tests | **72/72 ✅** |
| Languages | EN, ES, FR, 中文, 日本語 |

---

## What Session 13 Shipped

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🌿 | **TheMealDB recipe provider** | `mealDBSearchRecipes()` + `mealDBGetRecipeInfo()` — free recipe search by ingredient, no API key needed. Fetches `filter.php`, `lookup.php` via test key. Shows recipe thumbnails, ingredients, instructions, YouTube links |
| **2** 🔄 | **Spoonacular → TheMealDB fallback** | When no Spoonacular key is set, the tab shows a "Use TheMealDB (Free)" button. Clicking it activates recipe search routed through TheMealDB. Wine/nutrition sections gracefully show "needs API key". `spoonSearchRecipes()` auto-degrades if no key |
| **3** 🗺️ | **200-cuisine map labels** | `MEALDB_AREAS` array + `MEALDB_AREA_CUISINE` mapping. Map cuisine labels now show TheMealDB sub-area names (e.g. "Italian, Greek, Turkish") beneath the main region label when zoomed in ≥0.8× |
| **4** 🍸 | **TheCocktailDB integration** | `searchCocktailDB()` + `showCocktailDBDetail()` added. Cocktail tab now shows real cocktail recipes from TheCocktailDB alongside the embedding-based suggestions |
| **5** ✅ | **2 new E2E tests** | TheMealDB fallback button visibility, useMealDBFallback activates recipe search input |
| **🐛** | **Bug fix** | Fixed `eastern_europeon` → `eastern_european` typo in `exportSummary()` |

---

## Open Items & Gaps for Next Session

### Unstarted Opportunities — Still Open
| Item | Effort | Notes |
|------|--------|-------|
| **Recipe generation (LLM)** | High | Needs backend — FastAPI/Node server, API key management, cost control |
| **Ingredient2Vec REST API** | High | Server-side project: auth, rate-limiting, billing |

### Feedback Items Not Yet Addressed
All known feedback items addressed through Sessions 1–13.

### Future Architectural Directions (Separate Project)
- Ingredient2Vec REST API + OpenAPI spec (requires server)
- Recipe generation via LLM (requires backend + API keys)
- Professional/Creator paid tier (requires auth, billing)
- Analytics dashboard (requires server logs or third-party service)

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
node tests/e2e.mjs   # 72 tests, ~50s
```
