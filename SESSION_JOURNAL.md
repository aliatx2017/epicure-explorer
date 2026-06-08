# Session Journal — Epicure Explorer

**Session 1:** June 8, 2026 — Crash recovery, missing functions, accessibility, GLP-1 filter persistence  
**Session 2:** June 8, 2026 (continued) — Documentation audit, stale metrics, bug surfacing  
**Session 3:** June 8, 2026 (eval) — Codebase truth audit, SESSION_JOURNAL.md refresh  
**Session 4:** June 14, 2026 — Force-graph fix + Month 3 features shipped (Ingredient2Vec, Food Agent, Trending, GLP-1 Meal Plan)
**Session 5:** June 2026 — 12-bug audit & fix pass across all Month 3 features + force-graph + CSS

---

## Session 1 — Crash Recovery & Feature Gap Fixes

**Focus:** `renderGames()`, `setupDescribeDish()`, `setupMapControls()` were called in `init()` but never defined, causing the entire app to crash on load.

### What Was Done

#### Problem 1: `renderGames()` missing → whole app broken
`renderGames()` was called in `renderAll()` and `setupTabs()` but never defined. `ReferenceError` during `selectIngredient('miso')` in `init()`, halting JS entirely.

- Added `renderGames()` — Flavour Compass radar chart (Canvas) + initialises Guess-the-Neighbour game
- Added `newGuessGame()` — picks a random ingredient, shows 4 options (1 correct + 3 decoys), tracking score

#### Problem 2: `setupDescribeDish()` missing
Called in `init()` but never defined. The Describe a Dish UI was decorative only.

- Added `describeDish()` — parses natural language ("creamy garlic pasta with mushrooms") into ingredient tags with multi-word phrase matching + fuzzy fallback
- Added `setupDescribeDish()` — wires Enter key + auto-trigger debounce on input

#### Problem 3: `setupMapControls()` missing
Called in `init()` but never defined. The projection method dropdown (`#projMethod`) was decorative.

- Added `setupMapControls()` — wires the selector to re-render the map on change

#### Problem 4: GLP-1 Diet Mode filter reset bug
Hardcoded `class="active"` on first button in `renderChefToolkit()` — toggle lost on re-render.

- Changed to read current state from `dataset.mode` / `dataset.filter` before re-rendering

#### Problem 5: Duplicate `id="arithDropdown"`
Static HTML `arithDropdown` overwritten at runtime by JS template literal → duplicate ID warning.

- Removed the static copy

#### Accessibility
- Added `aria-label` to all 21 `<input>` elements
- Added `for` attributes to `<label>` elements for Compare2 inputs

#### Testing
- 26/26 automated Playwright tests pass across all 13 tabs, model switching, search, Analyzer, Compare2, Arithmetic, Seasonal, SLERP, Games
- GLP-1 filter toggle verified (off → on → off persists)
- Substitution mode switching (current/cooc/chem) verified
- Describe a Dish ("creamy garlic pasta with mushrooms") verified: 4 ingredients matched, tags clickable, Explore + Analyze buttons functional

---

## Session 2 — Documentation & Bug Audit

**Focus:** Closing the loop on documentation gaps, fixing stale metrics, surfacing the `getForceGraphLayout` bug.

### What Was Done

| Item | Action | Status |
|------|--------|--------|
| **FOOD_AI_RESEARCH_PLAN.md** | Added implementation-status crosswalk between research plan and code features. Surfaced `getForceGraphLayout` as known bug. | ✅ Updated |
| **SESSION_JOURNAL.md** | Corrected stale line-count metrics. Added this session's entry. | ✅ Updated |
| **GUIDE.md** | Fixed ToC (9→13 tabs). Updated Architecture line counts (CSS 250→396, HTML 170→~440, JS 950→~2,905). Added Accessibility section. Documented `getForceGraphLayout` bug. | ✅ Updated |

---

## Session 3 — Codebase Truth Audit & Journal Refresh

**Focus:** Verifying every file's actual state against stale mental model. Updating SESSION_JOURNAL.md.

### What Was Done

| Item | Action | Status |
|------|--------|--------|
| **Codebase survey** | Full directory tree, file sizes, line counts, git log check (none — no `.git` directory) | ✅ Documented |
| **FOOD_AI_RESEARCH_PLAN.md** | Verified Implementation Status crosswalk (lines 25–46) is accurate — Month 1&2 ✅ Live, Month 3 ❌ Not started. Research sections complete (8 sections). Line count reference (~3,848) matches actual index.html. **No changes needed.** | ✅ Verified current |
| **GUIDE.md** | Verified Games tab (§3.7), Describe a Dish (§3.9), Map controls (function table), Accessibility (§1.5) all documented. ToC lists all 13 tabs. Architecture metrics (CSS ~395, HTML ~440, JS ~2,900) match actual. **No changes needed.** | ✅ Verified current |
| **SESSION_JOURNAL.md** | Added this session entry. Consolidated stale repetitions. One `getForceGraphLayout` bug reference kept (still unresolved). | ✅ Updated |

#### Key Verification Details

| Check | Result |
|-------|--------|
| `renderGames()` defined? | ✅ Yes, line 1574 |
| `newGuessGame()` defined? | ✅ Yes, line 1649 |
| `describeDish()` defined? | ✅ Yes, line 2605 |
| `setupDescribeDish()` defined? | ✅ Yes, line 2665 |
| `setupMapControls()` defined? | ✅ Yes, line 2686 |
| `getForceGraphLayout()` defined? | ❌ No — still the known bug |
| `aria-label` attributes on `<input>` | ✅ 21 verified across all tabs |
| JS function count | 92 | 92 (includes all helpers) |
| `index.html` line count | 3,848 | 3,848 → **4,165 (after Snap tab)** |

---

## Key Metrics Over Time

| Metric | Session 1 Start | After Session 1 | After Session 2 | Session 3 (audit) | Session 3 (code) | Session 4 | Session 5 |
|--------|----------------|----------------|----------------|-------------------|-------------------|-----------|-----------|
| index.html lines | ~2,290 | ~3,930 | ~3,848 | 3,848 | **4,165** | **4,667** | **4,686** |
| JS functions | ~35 | ~45 | ~46 | 92 | **99** | **~113** | **~113** |
| `aria-label` attributes on `<input>` | 0 | 21 | 21 | 21 | 21 | 26 | **26** |
| Automated test pass rate | — | 26/26 | 26/26 | — | — | — | — |
| Console errors on load | ReferenceError | 0 | 0 | 0 | 0 | 0 | **0** |
| GLP-1 filter persistence | Reset on re-render | Preserved | Preserved | Preserved | Preserved | Preserved | Preserved |
| GUIDE.md ToC tabs | 9 | — | 13 | 13 | 13 | 13 | **18** |
| Tabs | 13 | 13 | 13 | 13 | **14** | **18** | **18** |
| Month 3 items shipped | — | — | — | — | 0/5 | **5/5 ✅** | **5/5 ✅** |
| Known bugs count | — | — | — | — | 1 (force-graph) | ~8+ uncovered | **0 fixed** |

---

## Known Bug: `getForceGraphLayout()` missing

The function `getForceGraphLayout()` is called at line ~3099 in `renderMap()` but **never defined**. When the user selects "Force-Directed" as the projection method in the Map tab, this throws a `ReferenceError`. Root cause: the spring-force layout was planned but never implemented.

**Impact:** PCA and UMAP methods work fine. Force-Directed is broken with no graceful fallback.

**Documented in:** GUIDE.md §5 (Troubleshooting), FOOD_AI_RESEARCH_PLAN.md implementation crosswalk.

---

## State at Session End (Session 3)

- All three documentation files (FOOD_AI_RESEARCH_PLAN.md, GUIDE.md, SESSION_JOURNAL.md) confirmed accurate or updated
- SESSION_JOURNAL.md line count: 156 → **current (~150)**
- No git repository exists (`.gitignore` present, no `.git/`)
- Only unresolved code issue: `getForceGraphLayout()` undefined in `renderMap()`
- **📸 Snap → Ingredient Search tab shipped** (Month 3, item 1) — food photo upload → Spoonacular image classify → recipe auto-fetch → ingredient clickthrough into embedding space
- `index.html` grew from 3,848 → 4,165 lines, functions from 92 → 99

---

## Session 4 — Force-Graph Fix + Month 3 Ship

**Focus:** Fixing the `getForceGraphLayout()` bug and shipping the remaining 4 Month 3 features.

### What Was Done

| Item | Action | Status |
|------|--------|--------|
| **`getForceGraphLayout()` implemented** | Added Fruchterman-Reingold spring-force layout using top-15 neighbour edges, initialised from UMAP coordinates, 35 iterations with cooling | ✅ Fixed |
| **🔬 Ingredient2Vec API tab** | Nearest-neighbour query (`runI2VNearest`) + flavour arithmetic (`runI2VArith`) using cooc model | ✅ Shipped |
| **🤖 Food Agent tab** | Natural language → embedding match via term matching + centroid search (`runFoodAgent`) | ✅ Shipped |
| **📈 Trending panel** | Seasonal + rarity (avg neighbour distance) + GLP-1 trend signals (`renderTrending`) | ✅ Shipped |
| **💊 GLP-1 Meal Plan tab** | 7-day meal plan from GLP-1-friendly embedding clusters, calorie target selector (`renderMealPlan`) | ✅ Shipped |
| **FOOD_AI_RESEARCH_PLAN.md** | Updated status crosswalk, roadmap checkboxes | ✅ Updated |

### Key Metrics Update

| Metric | Session 3 | Session 4 |
|--------|-----------|-----------|
| index.html lines | 4,165 | **4,667** |
| JS functions | 99 | **~113** |
| Tabs | 14 | **18** |
| `getForceGraphLayout()` defined? | ❌ No | ✅ Yes |
| Console errors on load | 0 | 0 |
| Month 3 items shipped | 1/5 | **5/5 ✅** |

---

## Session 5 — Month 3 Bug-Fix Audit

**Focus:** Comprehensive audit of all 5 Month 3 features + force-graph fix. Found and fixed 12 issues across HIGH/MEDIUM/LOW severities.

### What Was Done

| Bug | Severity | Area | Fix |
|-----|----------|------|-----|
| `--text3` CSS variable undefined → invisible text | 🔴 HIGH | CSS | Added `--text3: #6b6b8a` to `:root` |
| `renderTrending()` season off by 1 month vs `getCurrentSeason()` | 🔴 HIGH | Trending | Replaced inline season calc with `getCurrentSeason()` call |
| 4 Month 3 panels outside `.main-grid` → overlapping on tab switch | 🔴 HIGH | Layout | Moved closing `</div>` after mealplan panel |
| `getForceGraphLayout()` missing null guard on `model.pca` | 🔴 HIGH | Force-Graph | Added fallback: return `[]` if missing, random pos as init |
| `explainSubstitute()` sort uses `directions[b]` on both sides | 🔴 HIGH | Chef Toolkit | Fixed to `directions[a] - directions[b]` |
| Snap `FileReader` missing `onerror`/`onabort` | 🟡 MEDIUM | Snap | Added error handlers with user-facing messages |
| Missing Enter key handlers on I2V + Food Agent inputs | 🟡 MEDIUM | UX | Added `onkeydown` to 3 input fields |
| NaN propagation risk in force-graph distance check | 🟡 MEDIUM | Force-Graph | Added `dist !== dist` (NaN) guard |
| Food Agent strips accents/hyphens (`crème`→`crme`) | 🟢 LOW | Food Agent | Regex preserves `à-ÿ`, `æ`, `œ`, `-` |
| I2V arithmetic silently ignores trailing operators | 🟢 LOW | Ingredient2Vec | Detected with regex, yellow warning rendered |
| Meal plan can show "X with X" from singleton clusters | 🟢 LOW | Meal Plan | Filter clusters to `>= 2` members |
| `handleSnapImage()` missing null guard on `file` | 🟢 LOW | Snap | Added `if (!file)` early return |

### Key Metrics Update

| Metric | Session 4 | Session 5 |
|--------|-----------|-----------|
| index.html lines | 4,667 | **4,686** |
| JS functions | ~113 | **~113** (12 fixes, no new functions) |
| Tabs | 18 | **18** |
| `--text3` CSS variable defined? | ❌ No | ✅ Yes |
| `explainSubstitute()` sort fixed? | ❌ No | ✅ Yes |
| Console errors on load | 0 | **0** |
| Month 3 items shipped | **5/5 ✅** | **5/5 ✅ + all bugs cleared** |
| Known bugs remaining | ~8+ | **0** |
