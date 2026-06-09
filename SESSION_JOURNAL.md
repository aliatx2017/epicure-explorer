# Session Journal — Epicure Explorer

**Session 1:** June 8, 2026 — Crash recovery, missing functions, accessibility, GLP-1 filter persistence  
**Session 2:** June 8, 2026 (continued) — Documentation audit, stale metrics, bug surfacing  
**Session 3:** June 8, 2026 (eval) — Codebase truth audit, SESSION_JOURNAL.md refresh  
**Session 4:** June 14, 2026 — Force-graph fix + Month 3 features shipped (Ingredient2Vec, Food Agent, Trending, GLP-1 Meal Plan)
**Session 5:** June 2026 — 12-bug audit & fix pass across all Month 3 features + force-graph + CSS
**Session 6:** June 2026 — Chef workflow features: Export Summary, onboarding tour, GitHub publish, README, full chef review
**Session 7:** June 2026 — Map zoom, pan, cuisine region labels, touch support (Phase 2 completed)
**Session 8:** July 2026 — Full design audit: tab categories, empty states, Chef overlay drawer, deep-link URLs, responsive, ARIA+keyboard, skeleton loading + licensing cleanup
**Session 9:** June 2026 — 10-feature sprint: PWA manifest, dark mode, Spoonacular graceful degradation, map gesture hint, cross-model consensus, unified search, molecular fingerprint card, seasonal heatmap (Phase 3), Service Worker + offline, map viewport culling. 57/57 E2E tests pass. Repo pushed to GitHub.
**Session 10:** July 2026 — Feedback-driven polish sprint: Spoonacular call tracking + 429 handling, offline banner, search alias system (50+ culinary variants), density heatmap overlay, CSV + PNG exports, share link, 5-language i18n (EN/ES/FR/中文/日本語), semantic search intent detection, usage analytics, offline-aware APIs. 57/57 E2E tests pass.
**Session 18:**  — All 3 Tier-2 features shipped: Nutrition tab E2E tests, Build-A-Dish → TheMealDB recipe integration, Flavour Pair of the Day. 80/80 E2E tests pass.
**Session 19:**  — Cuisine direction vectors upgraded from heuristic keyword lists to Core GMM mode-atlas members. Resolves documented "future work" limitation. 80/80 E2E tests pass.

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

| Metric | Session 1 Start | After Session 1 | After Session 2 | Session 3 (audit) | Session 3 (code) | Session 4 | Session 5 | Session 6 | Session 7 |
|--------|----------------|----------------|----------------|-------------------|-------------------|-----------|-----------|-----------|-----------|
| index.html lines | ~2,290 | ~3,930 | ~3,848 | 3,848 | **4,165** | **4,667** | **4,686** | **4,957** | **5,055** |
| JS functions | ~35 | ~45 | ~46 | 92 | **99** | **~113** | **~113** | **~116** | **~112** |
| `aria-label` attributes on `<input>` | 0 | 21 | 21 | 21 | 21 | 26 | **26** | **26** | **26** |
| Automated test pass rate | — | 26/26 | 26/26 | — | — | — | — | — |
| Console errors on load | ReferenceError | 0 | 0 | 0 | 0 | 0 | **0** | **0** | **0** |
| GLP-1 filter persistence | Reset on re-render | Preserved | Preserved | Preserved | Preserved | Preserved | Preserved | Preserved | Preserved |
| GUIDE.md ToC tabs | 9 | — | 13 | 13 | 13 | 13 | **18** | **18** | **18** |
| Tabs | 13 | 13 | 13 | 13 | **14** | **18** | **18** | **18** | **18** |
| Month 3 items shipped | — | — | — | — | 0/5 | **5/5 ✅** | **5/5 ✅** | **5/5 ✅** | **5/5 ✅** |
| Known bugs count | — | — | — | — | 1 (force-graph) | ~8+ uncovered | **0 fixed** | **0** | **0** |
| Map zoom/pan | — | — | — | — | ❌ Static | ❌ Static | ❌ Static | ❌ Static | **✅ Zoom+Pan** |
| Cuisine region labels | — | — | — | — | ❌ | ❌ | ❌ | ❌ | **✅ 8 labels** |
| Touch support | — | — | — | — | ❌ | ❌ | ❌ | ❌ | **✅ Drag+Pinch** |

---


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

---

## Session 6 — Chef Workflow & GitHub Launch

**Focus:** Chef's review, Export Summary, onboarding tour, README, GitHub publishing.

### What Was Done

| Item | Detail |
|------|--------|
| **Chef's review** | Full professional chef audit across 10 dimensions — design, 18 tabs, Chef's Toolkit, games, map, seasonal, missing pro features. |
| **📋 Export Summary** | Added to Chef's Toolkit sidebar — copies formatted ingredient summary to clipboard with visual feedback |
| **🎓 Onboarding Tour** | 5-step guided walkthrough with overlay highlight, progress dots, Next/Skip. Fires once per user (localStorage) |
| **README.md** | Created with overview, quick start, 18-tab feature table, architecture, 3-model explainer |
| **GitHub repo** | Created `aliatx2017/epicure-explorer` (public). Precomputed JSON bundles included |
| **Bug fixes** | Fixed `exportSummary` cuisine key typo (eastern_europeon → eastern_european) |

### Remaining Scoped Phases

| Phase | Feature | Effort |
|-------|---------|--------|
| 3 | Seasonal month heatmap | Medium |
| 4 | Games interactivity upgrade | Medium |
| 5 | Build-A-Dish mode | High |
| 6 | Responsive mobile/tablet layout | Medium |
| 7 | Semantic Describe a Dish | Medium |

### Key Metrics Update

| Metric | Session 5 | Session 6 |
|--------|-----------|-----------|
| index.html lines | 4,686 | **4,957** |
| JS functions | ~113 | **~116** |
| Tabs | 18 | **18** |
| Console errors on load | 0 | **0** |
| Known bugs remaining | **0** | **0** |

---

## Session 7 — Map Zoom, Pan, Region Labels

**Focus:** Adding zoom, pan, double-click reset, cuisine region labels, and touch support to the Map tab.

### What Was Done

| Feature | Detail |
|---------|--------|
| **🔍 Zoom** | Scroll-wheel zoom centered on cursor, clamped 0.5×–20×, with stable cursor-under-pointer behavior |
| **✋ Pan** | Drag-to-pan via mousedown/mousemove/mouseup with click-vs-drag disambiguation |
| **🔄 Reset** | Double-click resets to initial view (scale=1, panX=0, panY=0) |
| **🏷️ Cuisine Region Labels** | Each ingredient classified to its dominant cuisine (max dot-product above 0.15). Centroids computed in the current projection space. Coloured pill labels drawn on canvas (hidden when zoomed out < 0.3×) |
| **📱 Touch Support** | Single-finger drag to pan, two-finger pinch to zoom |
| **🔄 Projection/Model Reset** | View resets when projection method or model is switched |
| **♻️ Architecture** | Event listeners attached once via `setupMapInteractions()`, avoiding accumulation bug. `MAP_VIEW` and `MAP_DRAG` states at module level |

### Key Metrics Update

| Metric | Session 6 | Session 7 |
|--------|-----------|-----------|
| index.html lines | 4,957 | **5,055** |
| JS functions | ~116 | **~112** (consolidated event wiring into setupMapInteractions) |
| Tabs | 18 | **18** |
| Console errors on load | **0** | **0** |
| Known bugs remaining | **0** | **0** |
| Map zoom/pan | ❌ Static | ✅ Zoom + pan + reset |
| Cuisine region labels | ❌ None | ✅ 8 cuisine centroids |
| Touch support | ❌ None | ✅ Drag + pinch-zoom |

---

## Session 8 — Full Design Audit & Polish

**Focus:** Comprehensive UI/UX design audit — 16 improvements across accessibility, responsive, navigation, and discoverability.

### What Was Done

#### Phase 1 — Quick Fixes
| Fix | Detail |
|-----|--------|
| **🎨 Contrast fix** | `--text3: #6b6b8a` → `#8a8aad` for WCAG AA compliance |
| **🍽️ Favicon** | SVG emoji favicon — shows 🍽️ in browser tab |
| **📝 Tagline** | Changed from academic subtitle to human-readable: "Discover flavour relationships · Find perfect substitutes · Explore 1,790 ingredients" |
| **🖱️ Smart tooltip** | Map tooltip avoids clipping off right/bottom screen edges |
| **🏷️ Input labels** | "🔍 Find an ingredient" / "✏️ Describe any dish" labels above search/describe inputs |
| **🎞️ Model-switch animation** | 200ms panel fade on model change |

#### Phase 2 — Empty States
| Panel | Before | After |
|-------|--------|-------|
| All 6 core panels | Silent return (blank box) | Contextual placeholder: "🔍 No ingredient selected — Search for an ingredient to see..." |

#### Phase 3 — Tab Categorization
| Before | After |
|--------|-------|
| 18 flat tabs wrapping 6+ rows | 4 categories (🧠 Core / 🎮 Play / 🔬 Analyze / 🚀 Advanced) with filtering sub-bar |

#### Phase 4 — Chef's Toolkit Overlay
| Before | After |
|--------|-------|
| Static sidebar below content | Fixed overlay drawer: slides from right, backdrop click-to-close, 250ms animation |

#### Phase 5 — Deep-Link URLs
| Before | After |
|--------|-------|
| No shareable state | `#tab=map&model=chem&ingredient=miso` — updates on every interaction, restored on page load |

#### Phase 6 — Responsive Design
| Breakpoint | Adjustments |
|------------|-------------|
| 768px (tablet) | Stacked header, column search, 2-col grids, 300px map, compact model tabs |
| 480px (mobile) | 1-col grids, 220px map, compact tab/category buttons |

#### Phase 7 — Accessibility
| Feature | Detail |
|---------|--------|
| ARIA roles | `role="tablist"`, `role="tab"`, `aria-selected` on all tabs |
| Keyboard nav | ArrowLeft/ArrowRight on category tabs |

#### Phase 8 — Loading Screen
| Before | After |
|--------|-------|
| Spinner + text | Skeleton layout with shimmer animation (header/tabs/search/panel shapes) |

### Key Metrics Update

| Metric | Session 7 | Session 8 |
|--------|-----------|-----------|
| index.html lines | 5,055 | **5,430** |
| JS functions | ~112 | **~112** (helper additions, no net increase) |
| Tabs | 18 | **18 (grouped into 4 categories)** |
| Console errors on load | **0** | **0** |
| Known bugs remaining | **0** | **0** |
| Empty states | ❌ None | ✅ All 6 core panels |
| Tab organization | Flat 18 | ✅ 4 categories with filtering |
| Chef's Toolkit | Static sidebar | ✅ Overlay drawer |
| Deep-link URLs | ❌ None | ✅ Hash-based |
| Responsive | ❌ None | ✅ 768px + 480px |
| ARIA / Keyboard | ❌ None | ✅ Roles + arrow nav |
| Skeleton loading | ❌ Spinner | ✅ Shimmer layout |
| PWA manifest | ❌ | ✅ Inline data URI manifest |
| Dark mode toggle | ❌ | ✅ CSS variable swap + localStorage |
| Spoonacular graceful degradation | ❌ | ✅ Feature panels hidden when no key |
| Map gesture hint | ❌ | ✅ First-visit touch overlay |
| Cross-model consensus | ❌ | ✅ All 3 models compared in Chef substitutes |
| Unified smart search | ❌ | ✅ Single input auto-detects ingredient vs describe |
| Molecular fingerprint card | ❌ | ✅ Compound intensity bars in Chef Toolkit |
| Seasonal heatmap | ❌ | ✅ Month-by-month grid (Phase 3 shipped) |
| Service Worker + offline | ❌ | ✅ sw.js caches index.html + model data |
| Map viewport culling | ❌ | ✅ Off-screen points skipped during render |

---

## Session 9 — Deep Analysis & 10-Feature Implementation Sprint

**Focus:** Responding to a comprehensive strategic review with 10 concrete improvements spanning PWA, UX, accessibility, performance, and new features.

### What Was Done

#### Tier 1 — Quick Wins (4 items, ~1 hr)

| # | Feature | Detail |
|---|---------|--------|
| 1 | **📱 PWA Manifest + Home Screen Icon** | Inline `data:application/json` manifest + `theme-color` + `apple-mobile-web-app-capable` meta tags. "Add to Home Screen" works on mobile. |
| 2 | **🌙 Dark Mode Toggle** | `.light` CSS class swapping all 15 color variables. `toggleTheme()` with `localStorage('epicure_theme')` persistence. Button in header. |
| 3 | **🔑 Spoonacular Graceful Degradation** | `renderSpoonacular()` hides feature panels when no API key, shows friendly onboarding banner with feature list and link to spoonacular.com. |
| 4 | **✋ Map Gesture Hint** | First-visit overlay on touch devices: "Drag to pan · Pinch to zoom · Double-tap to reset". Fades after 4s, fires once per user via `localStorage('epicure_map_hint_done')`. |

#### Tier 2 — Medium Impact (4 items, ~5 hrs)

| # | Feature | Detail |
|---|---------|--------|
| 5 | **🔬 Cross-Model Consensus** | New `crossModelConsensus()` computes similarity across all 3 loaded models. Substitutions show color-coded agreement glyphs (◆ ◈ ◇ in green/yellow/red). 💡 panel shows full per-model breakdown. |
| 6 | **🔍 Unified Smart Search Bar** | Merged search + describe-a-dish into one input. Auto-detects: single-word → ingredient autocomplete; multi-word with spaces → describe-dish parsing (350ms debounce). Hidden `#describeInput` preserved for backward compat. |
| 7 | **🧬 Molecular Fingerprint Card** | Enhanced Chef's Toolkit flavour profile section. Shows top 5 active compound categories as horizontal intensity bars (color-coded green > 60%, yellow > 35%, purple default). Pills show descriptions on hover. |
| 8 | **🗓️ Seasonal Heatmap (Phase 3 shipped)** | Month-by-month heatmap grid: 12 columns (Jan–Dec) × ~150 ingredients grouped by category (Produce, Protein, Spices, Dairy, Grains). Color intensity = peak availability. Toggle between season view and heatmap view. |

#### Tier 3 — Infrastructure (2 items, ~2 hrs)

| # | Feature | Detail |
|---|---------|--------|
| 9 | **📴 Service Worker + Offline Caching** | `sw.js` (60 lines, 1.7 KB) caches `index.html` + `epicure_shared.json` on install, lazy-caches model JSONs on first fetch via stale-while-revalidate. Registers silently in `init()`. |
| 10 | **⚡ Map Viewport-Frustum Culling** | Point rendering loop skips points outside `[-10, W+10]` × `[-10, H+10]` — when zoomed in, only visible points are drawn instead of all 1,790. |

#### Gap Audit Fix
| Issue | Fix |
|-------|-----|
| `.consensus-badge` CSS class referenced but undefined | Added full styling rules |
| `#mapSearch` missing `aria-label` | Added `aria-label="Find ingredient on map"` |
| `#snapFileInput` missing `aria-label` | Added `aria-label="Upload food photo"` |
| Deep-link hash overwritten by `setupSearch()` → `selectIngredient('miso')` before hash was read | Captured initial hash into `deepLinkIngredient` before any setup runs |

#### Testing
- **57/57 Playwright end-to-end tests pass** across all 18 tabs, new features, responsive layouts, accessibility, deep-links, service worker, onboarding tour, gesture hints, and Chef's Toolkit
- All tests run headless against a static HTTP server with no dependencies beyond Playwright
- 0 console errors on load

---

## Session 10 — Feedback-Driven Polish Sprint

**Focus:** Responding to feedback on UX gaps, offline experience, exports, multilingual support, and semantic search.

### What Was Done

#### Tier 1 — Quick Wins
| # | Feature | Detail |
|---|---------|--------|
| 1 | **🗄️ Spoonacular Call Tracking + 429 Handling** | Daily 150-call limit tracked in localStorage with date-stamp reset. Live "X/150 calls left" display in Spoonacular tab. 429 and 402 HTTP responses produce user-facing messages including current usage. |
| 2 | **📡 Offline Banner** | Sticky amber bar at top of page: "📡 No internet connection — some features may be unavailable". Event-driven via `online`/`offline` listeners, also checked on `init()`. |
| 3 | **🔍 Search Alias System** | ~50 culinary name variants mapped (coriander→cilantro, aubergine→eggplant, prawn→shrimp, scallion→green_onion, etc.). Alias matches boosted to top of search results with "→ alias" visual indicator in dropdown. |
| 4 | **🔬 Density Heatmap Overlay** | New Map overlay option. 60×40 grid kernel density estimation with inverse-distance weighting. 5-color gradient (deep blue→cyan→lime→yellow→orange). Reveals ingredient clustering hotspots. Legend shows "Sparse"→"Dense". |
| 5 | **📴 Offline-Aware APIs** | `spoonFetch()` checks `navigator.onLine` before making API calls. `classifySnapImage()` shows retry button when offline. Network errors enhanced with clear "📡 Network error" messages. |

#### Tier 2 — Professional Exports
| # | Feature | Detail |
|---|---------|--------|
| 6 | **📥 CSV Neighbour Export** | "Download Neighbours CSV" button in Chef's Toolkit. Exports top neighbours across all loaded models + flavour profile as CSV with descriptive filename. Shows "✅ Downloaded" feedback momentarily. |
| 7 | **📸 Map PNG Export** | "PNG" button in Map legend area. Captures canvas directly via `canvas.toDataURL('image/png')`. Filename includes model + projection method. |
| 8 | **🔗 Share Link** | "Copy Share Link" button in Chef's Toolkit. Builds current deep-link URL (tab+model+ingredient+overlay) and copies to clipboard. |

#### Tier 3 — i18n & Semantic Search
| # | Feature | Detail |
|---|---------|--------|
| 9 | **🌐 5-Language i18n** | `UI_STRINGS` with 12 translated keys in EN, ES, FR, 中文, 日本語. `tr()` helper and `setLanguage()`. Language picker dropdown in header. Persisted in localStorage. Dynamic UI updates. |
| 10 | **🎯 Search Intent Detection** | 15 cuisine, 10 diet, and 3 nutrition keywords. `detectSearchIntent()` scans query text. Clickable pill chips below search: cuisine → SLERP tab, diet → GLP-1 filter / Spoonacular diet, nutrition → Map overlay. |

#### Tier 4 — Analytics
| # | Feature | Detail |
|---|---------|--------|
| 11 | **📊 Usage Tracking** | Lightweight localStorage-based analytics. `trackEvent()` with 500-event cap and aggregated counts. Tracks tab visits, ingredient selections, model switches. Privacy-preserving — no external calls. Viewable via 📊 footer link. |

#### Gap Audit Fixes
| Issue | Fix |
|-------|-----|
| No Spoonacular call tracking or quota feedback | Added `SPOON_DAILY_LIMIT`, `spoonGetCallsToday()`, `spoonTrackCall()` with date-stamped localStorage |

#### Testing
- **57/57 Playwright end-to-end tests pass** — all existing tests continue to pass after 598-line addition
- 0 console errors on load
- New features verified: alias search, intent chips, density heatmap, all exports (JS passes syntax validation)

### Key Metrics Update

| Metric | Session 9 | Session 10 |
|--------|-----------|------------|
| index.html lines | **5,755** | **6,343** |
| JS functions | ~117 | **136** |
| index.html file size | 312 KB | **339 KB** |
| Tabs | 18 (4 categories) | 18 (4 categories) |
| Console errors on load | **0** | **0** |
| Known bugs remaining | **0** | **0** |
| E2E tests passing | **57/57 ✅** | **57/57 ✅** |
| Spoonacular call tracking | ❌ | ✅ localStorage daily tracker |
| Offline banner | ❌ | ✅ Sticky amber bar |
| Search aliases | ❌ | ✅ 50+ culinary variants |
| Density heatmap | ❌ | ✅ KDE grid overlay |
| CSV/PNG/Share exports | ❌ | ✅ 3 export options |
| i18n (5 languages) | ❌ | ✅ EN/ES/FR/中文/日本語 |
| Semantic search intents | ❌ | ✅ Cuisine/diet/nutrition detection |
| Usage analytics | ❌ | ✅ localStorage tracking |

### Open Items & Future Plans

#### Remaining Scoped Phases (from Session 6)
| Phase | Feature | Effort | Priority | Status |
|-------|---------|--------|----------|--------|
| 3 | Seasonal month heatmap | Medium | Medium | ✅ **Shipped Session 9** |
| 4 | Games interactivity upgrade (more game modes, leaderboard) | Medium | Low | ❌ Not started |
| 5 | Build-A-Dish mode (compose ingredient combinations with flavour preview) | High | Medium | ❌ Not started |
| 6 | Semantic Describe a Dish (upgrade natural-language parsing with semantic understanding) | Medium | Low | ❌ Not started |

#### Newly Identified Opportunities
| Item | Effort | Notes | Status |
|------|--------|-------|--------|
| **i18n / multi-language** | High | Ingredient names and UI in multiple languages | ✅ **Foundation shipped Session 10** (5 languages, UI only) |
| **Spoonacular call tracking** | Very low | Track daily API usage and display quota | ✅ **Shipped Session 10** |
| **Offline banner + retry** | Low | Communicate offline state, retry buttons | ✅ **Shipped Session 10** |
| **Search aliases** | Low | Map common culinary name variants | ✅ **Shipped Session 10** |
| **Density heatmap** | Medium | Ingredient clustering visualization | ✅ **Shipped Session 10** |
| **CSV/PNG/Share exports** | Medium | Professional export workflows | ✅ **Shipped Session 10** |
| **Semantic search intents** | Medium | Recognise cuisine/diet/nutrition in search | ✅ **Shipped Session 10** |
| **Usage analytics** | Low | Self-hosted, privacy-preserving | ✅ **Shipped Session 10** |
| **Performance optimization** | Medium | Larger-scale virtualized rendering | ❌ Not started |
| **Export/Share workflows** | Medium | Export pairing as image, share via QR | ❌ Not started |

#### Known Non-Issues
- **Force-graph layout** — fully fixed since Session 4
- **GLP-1 filter persistence** — preserved since Session 1
- **Console errors on load** — zero since Session 1
- **All data attribution** — MIT license + CC BY 4.0 credits + USDA attribution in footer and JSON metadata

### Key Metrics Over Time

| Metric | Session 9 | Session 10 | Session 11 |
|--------|-----------|------------|------------|
| index.html lines | 5,755 | **6,343** | **7,312** |
| JS functions | ~117 | **136** | **~154** |
| Tabs | 18 (4 categories) | 18 (4 categories) | **19 (4 categories)** |
| Console errors on load | **0** | **0** | **0** |
| Known bugs | **0** | **0** | **0** |
| E2E tests | **57/57** | **57/57** | **66/66** |

### State at Session End

- All 15 sub-steps complete across 4 phases
- 598 lines added to index.html (588 net growth after minor removals)
- Zero console errors, zero known bugs
- 57/57 E2E tests pass
- GitHub repo: `aliatx2017/epicure-explorer`

---

## Session 11 — Remaining Phases + Unstarted Opportunities Sprint

**Focus:** Shipped all remaining scoped phases (4, 5, 6) and 3 unstarted opportunities (map heatmap perf, QR exports, i18n ingredient names).

### What Was Done

#### Phase 4 — Games Interactivity Upgrade
| Feature | Detail |
|---------|--------|
| **🗄️ localStorage leaderboard** | Persists win/loss, best streak, current streak per game mode across sessions |
| **🌍 Cuisine ID game mode** | Shows 3–4 ingredients from a random cuisine (dotProduct > 0.15), player picks from 8 cuisine options |
| **🎮 Game mode selector** | Tab bar toggling between Guess-the-Neighbour and Cuisine ID |
| **📊 Stats cards** | 3-card leaderboard (Neighbour/Cuisine/Total) in games panel |
| **✅ 3 E2E tests** | Game UI renders, Cuisine ID mode, stats persistence |

#### Phase 5 — Build-A-Dish Mode
| Feature | Detail |
|---------|--------|
| **👨‍🍳 New tab button** | "👨‍🍳 Build Dish" in Play category (19th tab) |
| **🏷️ Multi-ingredient chip selector** | Autocomplete dropdown, chip tokens (max 6), Enter/click to add, ✕ to remove |
| **🧮 Centroid pairings** | Computes embedding centroid of selected ingredients → top-12 suggested additions |
| **🧭 Flavour profile compass** | 200×200 radar chart drawn from centroid's 8 sensory direction scores |
| **🥗 Category breakdown** | Auto-categorizes ingredients into produce/protein/spice/dairy/grain/condiment |
| **🏷️ Dietary flags** | GLP-1, Vegan, High Protein detection via keyword matching |
| **📋 Copy ingredients button** | One-click clipboard copy of ingredient list |
| **🔗 Deep-link support** | Tab wiring in `setupTabs()` |
| **✅ 2 E2E tests** | Panel renders, chip interaction + pairing results |

#### Phase 6 — Semantic Describe a Dish
| Feature | Detail |
|---------|--------|
| **🧠 5-stage matching pipeline** | (1) Multi-word phrase + alias → (2) Individual alias + exact → (3) Fuzzy substring → (4) Descriptive-word→embedding direction → (5) Broad embedding scan |
| **🔤 Improved tokenization** | Handles accented chars (à-ÿ, æ, œ), hyphens→spaces, possessive removal |
| **📊 Confidence badges** | Each tag shows match % with color coding: green=exact, purple=fuzzy, yellow=semantic |
| **👨‍🍳 Build-A-Dish button** | "Open in Build-A-Dish" button populates the new Build Dish tab |
| **✅ 2 E2E tests** | Confidence percentages, Build-A-Dish button present |

#### Phase 7 — Map Heatmap & Performance
| Feature | Detail |
|---------|--------|
| **🎚️ Density threshold slider** | User-controlled 0–10% minimum intensity for KDE cells, live label update |
| **🔍 Zoom-adaptive grid** | `GRID_X/Y` scales inversely with `MAP_VIEW.scale` (finer at high zoom) |
| **💾 KDE grid caching** | `MAP_DENSITY_CACHE` keyed on zoom + pan to avoid recomputation on every frame |
| **⚡ RAF coalescing** | `MAP_RENDER_PENDING` flag batches multiple renderMap() calls per frame |

#### Phase 8 — Export/Share Workflows
| Feature | Detail |
|---------|--------|
| **📱 Inline QR code generator** | Zero-dependency, version-adaptive byte-mode encoding with Reed-Solomon EC. `generateQRCode()` + `showQRCode()` functions |
| **🖼️ QR overlay modal** | Centered popup with canvas QR, scan-to-share text, close button + backdrop dismiss |
| **🔘 QR button in Chef's Toolkit** | "📱 Show QR Code" button alongside share link |

#### Phase 9 — i18n Ingredient Names
| Feature | Detail |
|---------|--------|
| **📖 Translation tables** | ~120 common ingredient names in ES, FR, 中文, 日本語 (`INGREDIENT_TRANSLATIONS`) |
| **🔤 `trIngredient(name)` / `displayName(name)`** | Helpers with English fallback, underscore-to-space conversion |
| **🔗 Wired into key UI** | Selected ingredient label, Chef's Toolkit name, map tooltip, compass target, neighbour substitutions |
| **🔄 `setLanguage()` refresh** | Re-renders ingredient names when language is switched |
| **✅ 1 E2E test** | Spanish ingredient names displayed correctly |

### Metrics Update

| Metric | Session 10 | Session 11 |
|--------|-----------|------------|
| index.html lines | 6,343 | **7,312** |
| JS functions | ~136 | **~154** |
| Tabs | 18 (4 categories) | **19 (4 categories)** |
| File size | 339 KB | **392 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **57/57 ✅** | **66/66 ✅** |
| Languages | 5 (UI only) | **5 (UI + ingredient names)** |

### State at Session End

- All 3 remaining scoped phases (4, 5, 6) shipped
- All 3 unstarted opportunities shipped (map heatmap, QR exports, i18n ingredient names)
- 969 lines added, ~154 functions, 392 KB
- Zero console errors, zero known bugs
- **66/66 E2E tests pass**
- GitHub repo: `aliatx2017/epicure-explorer`

---

## Session 12 — Map Performance, KDE Legend, Mobile UX

**Focus:** Map canvas rendering optimization, spatial index for click/hover, KDE scatter accumulation, interactive density legend, mobile chef sidebar, +4 E2E tests.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🗺️ | **Batch point rendering** | Color-grouped points: single beginPath + one fill() per color group instead of 1790 individual arc/fill calls |
| **1** 🗺️ | **Spatial grid index** | 30×30 cell grid built after screenPts → click/hover checks 9 cells instead of 1790 points. Hover handler moved to setupMapInteractions (bound once, not re-created every frame) |
| **1** 🗺️ | **KDE scatter optimization** | Point-to-cell KDE accumulation: O(n × r²) instead of O(cells × n). Each point scatters to nearby grid cells, ~90× fewer distance checks |
| **2** 🌡️ | **Interactive KDE legend** | `nutrientBar` converted from CSS gradient to rendered canvas with exact 5-color density gradient + threshold marker line. Density info toggle explains colors. Clicking empty map area in density mode shows local density popup (auto-hides after 3s) |
| **3** 📱 | **Mobile chef sidebar** | New `@media (max-width: 420px)` breakpoint: padding 12px (from 20px), font-size 0.75rem, tighter tags/sub-items. Chef-toggle button compacted. No horizontal overflow |
| **4** ✅ | **4 new E2E tests** | Canvas content verification (sparse random sampling), KDE legend gradient rendering, density click info popup, chef sidebar mobile responsive at 420px |

### Metrics Update

| Metric | Session 11 | Session 12 |
|--------|-----------|------------|
| index.html lines | 7,312 | **~7,350** |
| JS functions | ~154 | **~157** |
| Tabs | 19 (4 categories) | **19 (4 categories)** |
| File size | 392 KB | **~392 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **66/66 ✅** | **70/70 ✅** |

---

## Session 13 — TheMealDB + TheCocktailDB + 200-Cuisine Map Labels

**Focus:** Adding free recipe providers (TheMealDB, TheCocktailDB) as Spoonacular fallbacks, enriching map cuisine labels with TheMealDB's 200+ area taxonomy.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🌿 | **TheMealDB recipe provider** | `mealDBSearchRecipes()` searches by ingredient via `filter.php?i=...`. `mealDBGetRecipeInfo()` fetches full recipe via `lookup.php?i=...`. Shows thumbnails, ingredient list with measures, step-by-step instructions, YouTube links, source attribution. No API key needed (test key `1`) |
| **2** 🔄 | **Spoonacular → TheMealDB fallback** | `renderSpoonacular()` shows "🌿 Use TheMealDB (Free)" button when no Spoonacular key. `useMealDBFallback()` wires recipe search button to TheMealDB, hides wine/nutrition sections with "needs API key" messages, adds attribution bar. `spoonSearchRecipes()` auto-degrades via `if (!SPOON_KEY) { mealDBSearchRecipes(...); return; }`. Preference persisted in localStorage |
| **3** 🗺️ | **200-cuisine map labels** | `MEALDB_AREAS` (31 curated areas) + `MEALDB_AREA_CUISINE` (area → direction mapping). Map cuisine labels now show TheMealDB sub-areas beneath the main label when zoom ≥ 0.8× (e.g. "Mediterranean" with "Italian · Greek · Turkish" below it) |
| **4** 🍸 | **TheCocktailDB integration** | `cocktailDBFetch()` + `searchCocktailDB()` + `showCocktailDBDetail()`. Cocktail tab's `runCocktail()` now calls `searchCocktailDB(spirit)` at end, showing real cocktail recipes with ingredients, instructions, glass type, YouTube links alongside embedding-based suggestions |
| **5** ✅ | **2 new E2E tests** | Spoonacular tab shows TheMealDB fallback button, useMealDBFallback shows recipe search input. **72/72 tests pass** |

### Metrics Update

| Metric | Session 12 | Session 13 |
|--------|-----------|------------|
| index.html lines | ~7,350 | **~7,450** |
| JS functions | ~157 | **~165** |
| Tabs | 19 (4 categories) | **19 (4 categories)** |
| File size | ~392 KB | **~395 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **70/70 ✅** | **72/72 ✅** |

---

## Session 14 — Bug Fix Pass + im2recipe Nutritional Integration

**Focus:** Comprehensive bug/issue fix pass (Session 14), then im2recipe-Pytorch 35K nutritional data integration (Week 1).

### Session 14a — Bug Fix Pass (HIGH/MEDIUM/LOW)

| Fix | Severity | Detail |
|-----|----------|--------|
| **🐛 Missing `<div class="game-card">`** | 🔴 HIGH | Flavour Compass section was missing its opening `game-card` div, causing broken game grid layout |
| **🐛 Dead GLP-1 intent chip path** | 🔴 HIGH | `applyIntent('diet', 'glp1')` referenced non-existent `glp1Filter` element and undefined `updateChefToolkit()` — now correctly calls `toggleGlpFilter()` |
| **🐛 roundRect polyfill** | 🔴 HIGH | `ctx.roundRect()` threw TypeError on older browsers — added inline polyfill |
| **🐛 Stale file size in docs** | 🟡 MEDIUM | GUIDE.md and README.md said 259 KB — actual is 422 KB |
| **🐛 Unused variables removed** | 🟡 MEDIUM | `pcaAnimationId`, `DENSITY_INFO_VISIBLE`, `DENSITY_INFO_POPUP` cleaned up |
| **🐛 Missing CSS class** | 🟡 MEDIUM | `.spoon-recipe-grid` CSS class added |
| **🐛 Hardcoded Spoonacular limit** | 🟡 MEDIUM | `SPOON_DAILY_LIMIT` configurable via localStorage + UI field |
| **🐛 Test file fixes** | 🟡 MEDIUM | "All 18 Tab Panels" → 19 with builddish; removed 4 redundant tests (72→68) |
| **🐛 Redundant test removed** | 🟢 LOW | Build-Dish panel existence test removed (covered by 19-tab loop) |

### Session 14b — im2recipe Week 1: Nutritional Integration

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🔬 | **`build_nutrition.py`** | USDA-derived nutrition DB for 500+ ingredients, food-group heuristics for all 1,790 Epicure ingredients, FSA traffic lights. Outputs im2recipe-Pytorch format |
| **2** 📦 | **`data/epicure_nutrition.json`** | 789 KB — all 1,790 ingredients with `nutr_values_per100g`, `fsa_lights_per100g`, `nutr_per_100g_extended`. 409 exact USDA matches, 1,381 food-group estimated |
| **3** 🗺️ | **Vocabulary bridge** | `data/nutrition_vocab.json` (114 KB) — 3,531 entries mapping im2recipe names ↔ Epicure canonical names |
| **4** 🧠 | **FSA Health Direction** | `computeHealthDirection()` — computes embedding centroid of healthy (3+ green) vs indulgent (2+ red) ingredients, creates direction vector. `💚 FSA Health` in SLERP dropdown under `💪 Health` |
| **5** 🥗 | **Recipe Nutrition tab** | 4th Recipe Explorer subtab (`🥗 Nutrition`). Shows per-ingredient FSA traffic lights when no 35K data loaded; shows per-recipe FSA scores when data is present |
| **6** 📥 | **35K per-recipe importer** | `build_nutrition.py --import-im2recipe` — processes the im2recipe 35K JSON into `data/recipe_nutrition.json` |
| **7** 🔗 | **Ingredient→Recipe index** | `det_ingrs.json` (1M+ Recipe1M detections) processed into `data/recipe_detections_slim.json` (2.1 MB) — 622 ingredients linked to nutrition recipes |
| **8** 💾 | **Offline caching** | `sw.js` caches `epicure_nutrition.json`, `recipe_nutrition.json`, `recipe_detections_slim.json` |

### What was downloaded (im2recipe data access)

| File | Size | App derivative |
|------|------|----------------|
| `recipes_with_nutritional_info.json` | 213 MB | → `data/recipe_nutrition.json` (98 MB, 51,235 recipes) |
| `det_ingrs.json` | 345 MB | → `data/recipe_detections_slim.json` (2.1 MB, 622 ingredients) |
| `recipe1M_layers.tar.gz` | 381 MB | Not used (category hierarchy only) |

### Metrics Update

| Metric | Session 13 | Session 14 |
|--------|-----------|------------|
| index.html lines | ~7,450 | **8,025** |
| JS functions | ~165 | **~163** |
| Tabs | 19 (4 categories) | **19 (4 categories)** |
| File size | ~395 KB | **~422 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **72/72 ✅** | **68/68 ✅** (4 redundant removed) |
| Nutrition coverage | — | **1,790 ingredients** (FSA per-100g) + **51,235 recipes** (per-recipe FSA) |

---

## Session 15 — Safety, Performance, a11y & Seasonal Data Extraction

**Focus:** Responding to a deep codebase audit: fix runtime safety gaps, add search debounce, fix branding/a11y gaps, extract seasonal data from hardcoded JS into data-driven format.

### What Was Done

#### Phase 1 — Runtime Safety
| Fix | Detail |
|-----|--------|
| **🔄 Retry on load failure** | `init()` catch now shows ❌ message + "🔄 Retry" button that re-invokes `init()` |
| **🔄 Model-load error display** | `setupModelTabs()` shows user-visible error in active panel with refresh button on model load failure |
| **🧮 NaN/Infinity guard** | `dotProduct()` now skips non-finite products, returns 0 on degenerate inputs; vector decode replaces NaN/Infinity vectors with zeros |
| **🛡️ Spoonacular null guard** | `spoonGetRecipeInfo()` checks info response is a valid object before accessing nested properties |

#### Phase 2 — Search Debounce
| Fix | Detail |
|-----|--------|
| **⏱️ 150ms debounce** | Smart search `input` handler wrapped in `clearTimeout`/`setTimeout` pattern — no longer fires on every keystroke |
| **👂 Listener audit** | Confirmed `setupMapInteractions()` one-time guard prevents accumulator leak on model/tab switch |

#### Phase 3 — Branding & a11y
| Fix | Detail |
|-----|--------|
| **🎨 theme-color sync** | `toggleTheme()` now updates `<meta name="theme-color">` — `#0f0f13` (dark) ↔ `#f5f5fa` (light) |
| **📱 PWA icons** | Generated 192×192 and 512×512 PNG icons (purple plate/fork design); added to manifest + `apple-touch-icon` + SW cache preload |
| **♿ Canvas aria-label** | `#pcaCanvas` now has descriptive `aria-label="Map of ingredient embeddings — navigation, cuisine regions, and density overlay"` |

#### Phase 4 — Data-Driven Seasonal
| Fix | Detail |
|-----|--------|
| **📦 Seasonal extraction** | 149 seasonal entries moved from `const SEASONAL_DATA` in `index.html` into `epicure_shared.json["seasonal"]` |
| **🔄 Runtime override** | `loadSharedData()` sets `SEASONAL_DATA = json.seasonal` if available; inline constant preserved as fallback |
| **📏 `const` → `var`** | `SEASONAL_DATA` changed from `const` to `var` to allow reassignment |

### Metrics Update

| Metric | Session 14 | Session 15 |
|--------|-----------|------------|
| index.html lines | 8,025 | **8,060** |
| JS functions | ~163 | **~163** |
| Tabs | 19 (4 categories) | **19 (4 categories)** |
| File size | ~422 KB | **~425 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **68/68 ✅** | **68/68 ✅** |
| PWA icons | ❌ emoji only | ✅ 192×192 + 512×512 PNG |
| Seasonal data | Hardcoded JS constant | ✅ Data-driven from `epicure_shared.json` |
| Search debounce | ❌ per-keystroke | ✅ 150ms trailing-edge |
| theme-color sync | ❌ hardcoded | ✅ dark/light toggle updates meta |
| Canvas aria-label | ❌ missing | ✅ descriptive label added |

---

## Session 15b — Docs Refresh, Metrics Audit & Final Wrap

**Focus:** Comprehensive documentation audit: fix stale metrics across all docs, append session journal entry, refresh handoff doc, commit and push.

### What Was Done

| Item | Detail |
|------|--------|
| **🔍 Metrics audit** | Verified: index.html 8,060 lines, 424 KB, 176 JS functions, 686 CSS lines, ~6,595 JS script lines. 68/68 E2E tests pass. 0 console errors, 0 known bugs. |
| **📝 NEXT_SESSION.md** | Rewritten with fresh line/function/CSS/JS counts. Added cache versioning (`'epicure-v1'` hardcoded) as #1 open technical debt. Updated test gap table. |
| **📖 README.md** | Fixed stale JS function count (163→176) and JS logic lines (~6,200→~6,595). |
| **📘 GUIDE.md** | Fixed architecture metrics: 7,756→8,060 lines, CSS ~650→686, HTML ~780→~775, JS ~5,000→~6,595. |
| **📗 SESSION_JOURNAL.md** | Added this entry (Session 15b). |
| **📦 Git** | Committed all doc changes as `44600f0`, pushed to `origin/main`. |

### Metrics Update

| Metric | Session 15 | Session 15b |
|--------|-----------|-------------|
| index.html lines | 8,060 | **8,060** (unchanged) |
| JS functions | ~163 | **176** (corrected count) |
| CSS lines | — | **~686** (first measured) |
| JS script lines | — | **~6,595** (first measured) |
| File size | ~425 KB | **~424 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **68/68 ✅** | **68/68 ✅** |
| GUIDE.md metrics | Stale (7,756) | ✅ **Corrected** (8,060) |
| README.md function count | ~163 | **176** |
| NEXT_SESSION.md | Sessions 14→15 delta | ✅ **Fresh handoff with gaps** |
| Cache versioning | Unaddressed | **⚠️ Still open — `'epicure-v1'` hardcoded** |

### State at Session End

- All docs updated with verified metrics
- 68/68 E2E tests pass, 0 bugs, 0 console errors
- Cache versioning remains the single highest-priority technical debt
- `origin/main` up to date

---

## Session 16 — SW Cache Versioning & Handoff Refresh

**Focus:** Resolving the oldest open technical debt — replacing hardcoded `'epicure-v1'` SW cache key with a content-hash derived version that auto-invalidates when data files change.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🏷️ | **`tools/version-sw.js`** | Node.js script that reads all cached files (STATIC pre-cache + lazy-loaded model JSONs + sw.js itself), normalizing sw.js's own CACHE line to a placeholder to avoid self-feedback, computes SHA-256 hash (truncated to 12 hex chars), and patches sw.js. Idempotent — same input files always produce the same version. |
| **2** 📦 | **`package.json` script** | `"version-sw": "node tools/version-sw.js"` added to scripts. |
| **3** 🧪 | **Idempotency verified** | Running the script twice produces identical `epicure-c82486bc87a3` — confirmed stable. |
| **4** 📖 | **NEXT_SESSION.md** | Cache versioning moved from "Open Items" to resolved; workflow docs updated with `node tools/version-sw.js` step. |

### Metrics Update

| Metric | Session 15b | Session 16 |
|--------|-----------|------------|
| index.html lines | 8,060 | **8,060** (unchanged) |
| JS functions | 176 | **176** (unchanged) |
| File size | ~424 KB | **~424 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **68/68 ✅** | **68/68 ✅** |
| SW cache key | `'epicure-v1'` (hardcoded) | **`'epicure-c82486bc87a3'` (content-hash)** |
| Cache versioning | ⚠️ Still open | ✅ **Resolved** |

### Files Added
| File | Size | Description |
|------|------|-------------|
| `tools/version-sw.js` | 3.0 KB | Content-hash SW versioner |
| `.sw-version` | 19 B | Current version record |

### Files Modified
| File | Change |
|------|--------|
| `sw.js` | `'epicure-v1'` → `'epicure-c82486bc87a3'` (auto-generated) |
| `package.json` | Added `version-sw` script |
| `NEXT_SESSION.md` | Resolved cache versioning; documented workflow |

---

## Session 17 — Tier-1 Cleanup Sprint: NUTRITION_DATA migration, E2E coverage, dotProduct audit

**Focus:** Resolving all remaining Tier-1 items: move hardcoded NUTRITION_DATA to data-driven, add E2E feature tests for 5 untested tabs, add error-state tests, complete i18n E2E coverage for all 5 languages, and audit dotProduct consistency.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 📦 | **Data-driven NUTRITION_DATA** | Extracted 413-ingredient nutrition object from inline `const` in `index.html` into `data/epicure_shared.json` under `"nutrition"` key. Changed `const` → `var` fallback. `loadSharedData()` overrides `NUTRITION_DATA` from `json.nutrition` (same pattern as `SEASONAL_DATA`). |
| **2** 🧪 | **E2E feature tests for 5 untested tabs** | Added tests for Neighbours (`.neighbour-card`), Compare (model panels), Modes (mode content), Recipes (`.recipe-subtab` + programmatic subtab switch), Snap (file input + upload instructions). |
| **3** 🛡️ | **Error-state E2E tests** | Offline banner: verify element exists, hidden initially, show/hide toggles. Model resilience: navigate Chem model tab, verify no crash. |
| **4** 🌐 | **i18n E2E coverage all 5 languages** | French, Chinese, Japanese ingredient display tests — same pattern as existing Spanish test. |
| **5** 🔍 | **dotProduct callsite audit** | All 36+ callers verified using single centralized `dotProduct()` helper with NaN/Infinity guards. Zero inline reimplementations. No missed opportunities. |
| **6** 📖 | **Docs refresh** | NEXT_SESSION.md rewritten with fresh state, resolved items, Tier 2/3 surfaced. README.md metrics updated (8,062 lines, 78 E2E tests, 428 KB). GUIDE.md updated (8,062 lines, 428 KB). |

### Metrics Update

| Metric | Session 16 | Session 17 |
|--------|-----------|------------|
| index.html lines | 8,060 | **8,062** |
| JS functions | 176 | **176** (unchanged) |
| File size | ~424 KB | **~428 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **68/68 ✅** | **78/78 ✅** |
| SW cache key | `'epicure-c82486bc87a3'` | **`'epicure-64adfa564ac8'`** |
| Cache versioning | ✅ Resolved | ✅ Resolved |
| NUTRITION_DATA | Inline const fallback | **Data-driven from shared.json** |
| Untested tabs | 5 (Snap, Neighbours, Compare, Modes, Recipes) | **0 — all 19 tabs tested** |
| Error-state tests | 0 | **2 (offline, model)** |
| i18n E2E coverage | Spanish only | **All 5 languages** |
| dotProduct callsites | Untracked | **Audited — all consistent** |

### Files Modified
| File | Change |
|------|--------|
| `index.html` | `const NUTRITION_DATA` → `var`; override in `loadSharedData()` |
| `data/epicure_shared.json` | Added `nutrition` key (413 entries) |
| `tests/e2e.mjs` | +211 lines: 5 tab-feature tests + 2 error-state tests + 3 i18n tests |
| `sw.js` | `'epicure-c82486bc87a3'` → `'epicure-64adfa564ac8'` (auto-generated) |
| `NEXT_SESSION.md` | Full rewrite: resolved items removed, Tier 2/3 surfaced, 78 tests |
| `README.md` | Metrics: 8,062 lines, 78 E2E tests, 428 KB |
| `GUIDE.md` | Metrics: 8,062 lines, 428 KB |

### State at Session End

- All Tier-1 items resolved: cache versioning, NUTRITION_DATA migration, E2E test gaps, i18n coverage, dotProduct audit
- 78/78 E2E tests pass, 0 bugs, 0 console errors
- Remaining: Tier 2 (Nutrition E2E, Build-A-Dish→Recipe, Flavour Pair feature) and Tier 3 (LLM recipe gen, Ingredient2Vec API, Food Agent)
- `origin/main` up to date (commits: d31b857, d3076b3, be9d8e7, 528599e)

---

## Session 18 — Tier-2 Complete: Nutrition E2E, Build-A-Dish → TheMealDB, Flavour Pair of the Day

**Focus:** All 3 Tier-2 client-side items shipped: Nutrition sub-tab E2E tests, Build-A-Dish → TheMealDB recipe integration, and Flavour Pair of the Day.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🧪 | **Nutrition tab E2E tests** | 2 new tests: FSA traffic-light display (🟢🟡🔴 emojis + "Per 100g" header) and per-recipe nutrition data for common ingredients (chicken). Verifies `recipeContent` contains FSA icons and "Recipes Using" section. |
| **2** 🍲 | **Build-A-Dish → TheMealDB** | New "🍲 Find Recipes with These Ingredients" button below centroid pairing results. `searchBuildRecipes()` uses `mealDBFetch()` searching by the first build ingredient, renders up to 12 recipe cards (thumbnail, title, area/category) with a "✓ matches" badge when other build ingredients appear in recipe names. Recipe details scroll into focus on card click. |
| **3** 🧪 | **Flavour Pair of the Day** | New expandable banner below the search bar showing a random molecularly-interesting ingredient pair. `generateFlavourPair()` samples 200 random pairs (similarity 0.4–0.88, prefers cross-cuisine). `explainFlavourPair()` shows shared molecular notes, sensory-direction alignment, and cuisine info. Persisted in localStorage per day. Triggered on first model load in `loadModelData()`. |

### Metrics Update

| Metric | Session 17 | Session 18 |
|--------|-----------|------------|
| index.html lines | 8,062 | **~8,130** |
| JS functions | 176 | **~182** |
| File size | ~428 KB | **~427 KB** |
| Console errors on load | **0** | **0** |
| Known bugs | **0** | **0** |
| E2E tests | **78/78 ✅** | **80/80 ✅** |
| Nutrition tab E2E | 0 tests | **2 tests** |
| Build-A-Dish → Recipes | Centroid-only | **TheMealDB integration** |
| Flavour Pair of the Day | — | **✅ Shipped** |

### Files Modified
| File | Change |
|------|--------|
| `index.html` | +Build-A-Dish "Find Recipes" button + `searchBuildRecipes()` + `escapeHtml()`; +Flavour Pair banner HTML + `generateFlavourPair()`/`explainFlavourPair()`/`renderFlavourPair()`/`formatName()`/`toggleFlavourPairDetail()`; +generation hook in `loadModelData()` |
| `tests/e2e.mjs` | +55 lines: 2 Nutrition subtab tests (FSA traffic lights + per-recipe data). 78→80 tests |
| `README.md` | Quick stats updated: ~8,130 lines, ~182 functions, ~6,640 JS lines, 80 E2E tests |
| `NEXT_SESSION.md` | Full rewrite: Tier 2 shipped, Tier 3 remaining, 80 tests |

### State at Session End

- All Tier-2 items resolved: Nutrition E2E tests, Build-A-Dish → TheMealDB recipe integration, Flavour Pair of the Day
- **80/80 E2E tests pass**, 0 bugs, 0 console errors
- Remaining: **Tier 3** (LLM Recipe Generation, Ingredient2Vec REST API, Personalized Food Agent) — requires backend infrastructure
- `origin/main` ready for push

---

## Session 19 — Cuisine Direction Vectors: Mode-Atlas Upgrade

**Focus:** Replacing heuristic keyword-list cuisine direction vectors with the Core model's GMM mode-atlas members — resolving the documented "future work" limitation.

### What Was Done

| Phase | Feature | Detail |
|-------|---------|--------|
| **1** 🔍 | **Research** | Mapped all 194 Core model GMM modes to the 8 cuisine macro-regions. Found strong mode coverage for East Asian (46 modes), Mediterranean (20), Latin American (14), and Western Atlantic (8). Weaker coverage for Japanese (1 mode) and South Asian (3 modes) — supplemented with keyword seeds. |
| **2** 🧮 | **`tools/compute_cuisine_directions.py`** | New standalone script: loads Core mode atlas, collects member ingredients per cuisine from assigned modes + keyword seeds, computes centroid vectors. Output: 8 improved cuisine direction vectors. |
| **3** 🔧 | **`preprocess.py` updated** | `compute_directions()` now takes a `mode_atlas_path` argument and uses mode-atlas membership instead of heuristic keyword + NN expansion. Fallback preserves old keyword approach. Metadata version bumped to 2.1. |
| **4** ✅ | **`epicure_shared.json` updated** | 8 cuisine direction vectors recomputed. Sensory directions preserved unchanged. Old `direction_expansion` metadata replaced with `direction_method`. |
| **5** 🧪 | **Tests pass** | 80/80 E2E ✅ |

### What Changed

| File | Change |
|------|--------|
| `tools/compute_cuisine_directions.py` | Created — standalone mode-atlas cuisine direction generator (15 KB) |
| `preprocess.py` | `compute_directions()` now takes mode_atlas_path; added `CUISINE_MODE_IDS` mapping, `CUISINE_SEEDS`, `load_mode_atlas()`, `_fallback_cuisine_directions()`. Old keyword lists preserved as fallback. |
| `data/epicure_shared.json` | 8 cuisine direction vectors replaced. Metadata updated: `direction_method` = "mode-atlas + keyword seeds". SW cache key updated. |
| `sw.js` | Cache key: `'epicure-25e8f4a27cf8'` (content-hash regenerated after data change) |

### Cuisine Mode Coverage

| Cuisine | Modes | Members (vocabulary matched) |
|---------|-------|------|
| East Asian | 46 | 951 (385 in vocab) |
| Western Atlantic | 8 | 447 (209 in vocab) |
| Mediterranean | 20 | 737 (340 in vocab) |
| Eastern European | 3 + seeds | 102 (65 in vocab) |
| Southeast Asian | 4 | 380 (153 in vocab) |
| South Asian | 2 + seeds | 75 (35 in vocab) |
| Latin American | 14 | 542 (257 in vocab) |
| Japanese | 1 + 33 seeds | 72 (42 in vocab) |

### Metrics

| Metric | Session 18 | Session 19 |
|--------|-----------|------------|
| index.html lines | ~8,130 | **~8,293** (docs/metrics updates) |
| JS functions | ~182 | **~202** (script-level count) |
| E2E tests | **80/80 ✅** | **80/80 ✅** |
| Console errors | **0** | **0** |
| Known bugs | **0** | **0** |
| File size | ~427 KB | **~435 KB** |
| CSS lines | ~686 | **~686** (unchanged) |
| JS script lines | ~6,640 | **~6,814** |
| SW cache key | `'epicure-64adfa564ac8'` | **`'epicure-25e8f4a27cf8'`** |
| Cuisine directions | Heuristic keywords + NN | **GMM mode-atlas + seeds ✅** |
