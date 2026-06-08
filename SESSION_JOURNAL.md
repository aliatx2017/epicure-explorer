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

### Key Metrics Update

| Metric | Session 8 | Session 9 |
|--------|-----------|-----------|
| index.html lines | **5,430** | **5,755** |
| JS functions | ~112 | ~117 |
| Tabs | 18 (4 categories) | 18 (4 categories) |
| Console errors on load | **0** | **0** |
| Known bugs remaining | **0** | **0** |
| E2E tests passing | — | **57/57 ✅** |
| Files tracked | 24 | **28** (+sw.js, tests/e2e.mjs, package.json, package-lock.json) |
| Service Worker | ❌ | ✅ sw.js (1.7 KB) |
| PWA manifest | ❌ | ✅ Inline data URI |

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
| **PWA manifest** | Very low | Manifest for "Add to Home Screen" on mobile | ✅ **Shipped Session 9** |
| **Seasonal heatmap** | Medium | Month-by-month ingredient availability heatmap | ✅ **Shipped Session 9** |
| **Dark mode toggle** | Very low | CSS variable swap | ✅ **Shipped Session 9** |
| **Service worker caching** | Medium | Cache JSON bundles for offline use | ✅ **Shipped Session 9** |
| **Map viewport culling** | Low | Skip off-screen points during pan/zoom | ✅ **Shipped Session 9** |
| **Cross-model consensus** | Medium | Compare substitute scores across all 3 models | ✅ **Shipped Session 9** |
| **Unified search bar** | Low | Merge search + describe into one input | ✅ **Shipped Session 9** |
| **Molecular compound cards** | Medium | Visual compound intensity bars in Chef's Toolkit | ✅ **Shipped Session 9** |
| **Spoonacular graceful degradation** | Low | Hide features when no API key | ✅ **Shipped Session 9** |
| **i18n / multi-language** | High | Ingredient names and UI in multiple languages | ❌ Not started |
| **Performance optimization** | Medium | Larger-scale virtualized rendering | ❌ Not started |
| **Export/Share workflows** | Medium | Export pairing as image, share via QR | ❌ Not started |

#### Known Non-Issues
- **Force-graph layout** — fully fixed since Session 4
- **GLP-1 filter persistence** — preserved since Session 1
- **Console errors on load** — zero since Session 1
- **All data attribution** — MIT license + CC BY 4.0 credits + USDA attribution in footer and JSON metadata
