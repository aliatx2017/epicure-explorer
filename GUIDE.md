# Epicure Explorer — Professional Chef's Playbook

**The AI-powered ingredient intelligence platform for menu design, cross-cultural fusion, and flavour-driven substitutions.** Powered by the Epicure paper (arXiv:2605.22391) — three sibling embedding models trained on 4.14M recipes across 7 languages, mapping 1,790 canonical ingredients into a 300-dimensional semantic space.

This is not a recipe database. This is a **flavour relationship engine** — the same class of technology behind molecular gastronomy (Foodpairing.ai), trend intelligence (Tastewise.io), and industrial menu optimization. But in a zero-dependency, single-HTML file you can run on a laptop in a kitchen.

**Who this is for:** Executive chefs, R&D chefs, menu developers, restaurateurs, culinary educators, and anyone who thinks about food in terms of relationships — not just ingredients.

---

## Table of Contents

1. [Architecture & File Structure](#1-architecture--file-structure)
2. [Quick Start & Launch](#2-quick-start--launch)
3. [Feature Walkthrough — 19 Professional Modules](#3-feature-walkthrough--19-professional-modules)
   - [🔗 Neighbours — Flavour-Proximity Radar](#31--neighbours)
   - [⚖️ Compare — Model Divergence Analysis](#32--compare)
   - [🎯 Direction (SLERP) — Flavour Rotation](#33--direction-slerp)
   - [🗺️ Map — Ingredient Topography](#34--map-umap)
   - [🏷️ Modes — Culinary Role Atlas](#35--modes)
   - [🍲 Recipes — Menu Engineering Workspace](#36--recipes)
   - [🎮 Mini-Games — Embedding Intuition Training](#37--mini-games)
   - [👨‍🍳 Chef's Toolkit Pro — Ingredient Intelligence Hub](#38--chefs-toolkit-pro)
   - [✏️ Describe a Dish — Natural Language → Shopping List](#39--describe-a-dish)
   - [🧮 Flavour Arithmetic — Visual Expression Builder](#310--flavour-arithmetic)
   - [🍸 Cocktail Mixology — Spirit-Driven Drink Intelligence](#311--cocktail-mixology)
   - [🗓️ Seasonal Calendar — Menu Planning by Peak Season](#312--seasonal-ingredient-calendar)
   - [🌐 Spoonacular API — Live Recipe Search & Nutrition](#313--spoonacular-api)
   - [📸 Snap — Image→Ingredient Search](#314--snap)
   - [🔬 Ingredient2Vec — Embedding Query API](#315--ingredient2vec)
   - [🤖 Food Agent — Natural Language Ingredient Search](#316--food-agent)
   - [📈 Trending — What's Trending Panel](#317--trending)
   - [💊 Meal Plan — GLP-1 Meal Plan Generator](#318--meal-plan)
   - [👨‍🍳 Build-A-Dish — Ingredient Composition Studio](#319--build-a-dish)
   - [🔬 Nutrition Deep-Dive & FSA Health Direction](#320--nutrition-deep-dive--fsa-health-direction)
4. [Professional Workflows & Strategies](#4-professional-workflows--strategies)
5. [Troubleshooting](#5-troubleshooting)
   - [Force-Directed Map — Fixed](#51-force-directed-map--fixed)
   - [Browser performance](#52-browser-performance)
   - [PWA & Offline Support](#53-pwa--offline-support)
   - [Dark Mode](#54-dark-mode)
   - [Unified Smart Search Bar](#55-unified-smart-search-bar)
   - [Cross-Model Consensus in Substitutions](#56-cross-model-consensus-in-substitutions)
   - [Molecular Fingerprint Card](#57-molecular-fingerprint-card)
   - [Seasonal Heatmap](#58-seasonal-heatmap)
   - [Spoonacular Graceful Degradation](#59-spoonacular-graceful-degradation)
   - [Map Gesture Hint (Mobile)](#510-map-gesture-hint-mobile)
   - [Density Threshold Slider](#517-density-threshold-slider)
   - [QR Code Share](#518-qr-code-share)
   - [ℹ️ Ingredient Name Translation](#519-ingredient-name-translation)
   - [Nutrition Data Not Loading](#520-nutrition-data-not-loading)
   - [FSA Health Direction Not in SLERP Dropdown](#521-fsa-health-direction-not-in-slerp-dropdown)

---

## 1. Architecture & File Structure

### 1.1 Directory Layout

```
epicure-explorer/
├── index.html          ← THE WEB APP — single self-contained HTML file (425 KB)
├── preprocess.py       ← Python script that generates the data bundle
├── requirements.txt    ← Pinned Python dependencies (umap-learn, scikit-learn, etc.)
├── icon-192.png        ← PWA home-screen icon (2.3 KB)
├── icon-512.png        ← PWA splash-screen icon (6.8 KB)
├── data/
│   ├── epicure_shared.json  ← Shared data (168 KB) — ingredients + 16 direction vectors + seasonal
│   ├── epicure_cooc.json    ← Cooc model data (~4 MB) — neighbours + UMAP + vectors
│   ├── epicure_core.json    ← Core model data (~4 MB)
│   ├── epicure_chem.json    ← Chem model data (~4 MB)
│   ├── epicure_cooc.csv     ← Raw Cooc embeddings from arXiv (300D, 1,790 rows)
│   ├── epicure_core.csv     ← Raw Core embeddings from arXiv
│   ├── epicure_chem.csv     ← Raw Chem embeddings from arXiv
│   ├── vocab.csv            ← Cross-model node_id mapping (1,790 rows)
│   ├── mode_atlas_cooc.csv  ← GMM culinary modes for Cooc
│   ├── mode_atlas_core.csv  ← GMM culinary modes for Core
│   ├── mode_atlas_chem.csv  ← GMM culinary modes for Chem
│   ├── direction_arithmetic_full.csv  ← SLERP evaluation (paper results)
│   ├── factor_top_alignments_ica_*.csv ← FastICA ↔ supervised label alignments
│   └── README.txt           ← Original authors' notes on the supplementary bundle
├── ANALYSIS.md         ← ← THIS DOCUMENT's companion: paper analysis & summary
└── GUIDE.md            ← ← THIS FILE: comprehensive user guide
```

### 1.2 Data Pipeline

```
arXiv supplementary CSV files
  (epicure_cooc.csv, epicure_core.csv, epicure_chem.csv,
   mode_atlas_*.csv, vocab.csv)
          │
          ▼
preprocess.py
  │  • Loads 3 embedding CSVs → 1,790 × 300-D vectors each
  │  • L2-normalises all vectors
  │  • Computes 25-nearest-neighbour lists (cosine similarity)
  │  • Computes 2D UMAP projection (cosine metric, 15 neighbours)
  │  • Computes 16 direction vectors (8 sensory + 8 cuisine)
  │  • Loads mode atlases and indexes by ingredient name
  │  • Packs float32 vectors as base64 for compact transfer
  │  • Splits output into shared + per-model JSONs for lazy loading
  │
  ├── data/epicure_shared.json  (128 KB — loaded first)
  ├── data/epicure_cooc.json   (~4 MB — loaded on demand)
  ├── data/epicure_core.json   (~4 MB — loaded on demand)
  └── data/epicure_chem.json   (~4 MB — loaded on demand)
          │
          ▼
index.html
  │  • Fetches epicure_shared.json at startup (128 KB)
  │  • Loads model data on demand when tab is switched
  │  • Decodes base64 vectors back to Float32Array
  │  • Renders all 5 tabs from in-memory data
  │  • Zero server-side processing — everything in the browser
```

### 1.3 Data Sizes

| Data item | Size | Notes |
|---|---|---|
| Raw CSVs (3 models × 1,790 × 300 floats) | ~4.9 MB each | 6 decimal places; raw skip-gram outputs (not L2-normalised) per `data/README.txt` |
| `epicure_shared.json` | 128 KB | Ingredients + 16 direction vectors — loaded first |
| `epicure_cooc.json` / `epicure_core.json` / `epicure_chem.json` | ~4.1 MB each | Per-model: neighbours, UMAP, vectors, mode atlas — lazy-loaded |
| Mode atlases | ~175–196 KB each | GMM cluster definitions |
| `direction_arithmetic_full.csv` | 147 KB | Paper's SLERP evaluation results — 2,160 rows of hit-rank/hit-sim data across all models, angles, and test cases (see [§3.3](#33--direction-slerp) for how the app recomputes SLERP live) |
| `factor_top_alignments_ica_*.csv` | ~1.6–1.7 KB each | FastICA factor ↔ supervised label alignments |
| `vocab.csv` | 43 KB | Cross-model `node_id` mapping (see `data/README.txt` for notes) |
| `README.txt` | 1.7 KB | Original authors' notes on the supplementary bundle: raw-vs-normalised, compound-node omission, quick-load snippet |
| Nutrition database (embedded in `index.html`) | ~8 KB (gzipped) | 416 ingredients × 5 nutrients (calories, protein, fat, carbs, fiber) — inline fallback for heatmap overlay; extended data from `epicure_nutrition.json` covers all 1,790 ingredients with FSA traffic lights |

### 1.4 App Architecture (index.html)

The entire application is a **single HTML file** (7,756 lines) containing:

- **CSS** (~650 lines) — dark theme, responsive grid, panel layout, card components, canvas styling, mode filter controls, game cards, chef sidebar overlay, describe-dish input, snap upload zone, tab category bar, skeleton loading screen, responsive breakpoints, accessibility support
- **HTML** (~780 lines) — shell structure with 19 tab panels grouped into 4 categories, search bar, model switcher, mode filter bar, games panel, chef's toolkit overlay drawer, describe-dish input row, snap upload/preview area, accessibility labels, credit footer
- **JavaScript** (~5,000 lines) — all application logic, organised as:

| Function | Purpose |
|---|---|
| `loadSharedData()` | Fetch `epicure_shared.json` (128 KB — ingredients + directions) |
| `loadModelData()` | Lazy-fetch per-model JSON (~4 MB) on model tab switch |
| `base64ToArrayBuffer()` | Decode base64 → Float32Array |
| `setupSearch()` | Fuzzy search over 1,790 ingredient names |
| `selectIngredient()` | Set active ingredient, re-render all panels |
| `renderNeighbours()` | Top-25 neighbours with similarity bars |
| `renderCompare()` | Side-by-side neighbours across 3 models |
| `renderSlerp()` | SLERP rotation toward sensory or cuisine direction |
| `renderMap()` | 2D UMAP/PCA/Force-Directed scatter plot on canvas with hover/click |
| `renderModes()` | GMM mode memberships with label + member-count filters |
| `renderCrossModeSearch()` | Ingredient search across all modes (independent of selected ingredient) |
| `renderGames()` | Mini-games: "Guess the Neighbour" quiz + "Flavour Compass" radar chart |
| `newGuessGame()` / `guessPick()` | Quiz logic — pick random ingredient, 4-choice neighbour guess, scoring |
| `renderFlavourCompass()` | Polar radar chart of 8 sensory direction similarities for selected ingredient |
| `renderChefToolkit()` / `toggleChefToolkit()` | Sidebar with dietary tags (incl. GLP-1), substitutes (w/ explain + filter), cuisine affinity bars, flavour profile |
| `checkGLP1()` / `toggleGlpFilter()` | GLP-1 diet mode: ingredient friendliness tag + filter toggle for GLP-1-safe substitutes |
| `explainSubstitute()` / `toggleSubExplain()` | "Why This Substitute?" explanation panel: shared molecular notes, aligned sensory directions, cuisine overlap |
| `describeDish()` / `setupDescribeDish()` | Free-text input → keyword tokenization → vector centroid → ingredient suggestions |
| `getForceGraphLayout()` | Fruchterman-Reingold spring-force layout from top-15 neighbour edges, initialised from UMAP coords, 35 iterations with cooling. Used by `renderMap()` when "Force-Directed" is selected. |
| `setupMapInteractions()` | One-time canvas event setup: wheel zoom, drag pan, double-click reset, click-to-select, touch drag+pinch. Avoids listener accumulation. |
| `mapSearchAndFocus()` / `pulseLoop()` | Search-to-highlight on map: finds ingredient, centers view at 3× zoom, plays 2s expanding ring pulse animation |
| `setupMapControls()` | Projection switcher (UMAP / PCA / Force-Directed) + nutrient overlay handler + map search wiring |
| `getNutrientValue()` / `nutrientToColor()` | Nutrition heatmap colour coding from 416-ingredient per-100g database |
| `renderArithChips()` / `addArithChip()` / `removeArithChip()` | Flavour Arithmetic Explorer: visual chip UI — click ingredients from search dropdown, remove with ✕, auto-computes centroid on change |
| `saveArithHistory()` / `renderArithHistory()` / `loadArithHistory()` | Expression history (up to 6 recent) — click any to reload that ingredient combination |
| `runCocktail()` / `loadCocktailPreset()` | Cocktail Mixology: spirit + mixers → embedding centroid → top 12 companions + drink profile. 6 preset classic cocktails |
| `renderSeasonal()` / `getSeasonForIngredient()` / `isIngredientInSeason()` | Seasonal Calendar: 149-ingredient peak-season map, season browser with category grouping, season overlay on Map tab |
| `goToCurrentSeason()` / `goToNextSeason()` | Quick-navigate to today's season or advance to next |
| `renderSpoonacular()` / `saveSpoonKey()` / `clearSpoonKey()` | Spoonacular API integration: API key management (localStorage), connection status |
| `spoonFetch()` / `spoonSearchRecipes()` / `spoonGetRecipeInfo()` | Recipe search by ingredients + per-recipe nutrition widget with cook time, health score, servings |
| `spoonWinePairing()` | Wine pairing: dish/ingredient → recommended wine types + pairing explanation + product matches |
| `spoonNutritionLookup()` | Quick nutrition lookup: food item → calories, protein, fat, carbs from Spoonacular database |
| `setupSnapTab()` / `handleSnapImage()` / `classifySnapImage()` | Snap → Ingredient Search: food photo upload → Spoonacular image classify → recipe + ingredient cross-ref |
| `clearSnapImage()` / `snapFetchRecipes()` / `snapShowIngredients()` | Snap preview management, recipe card rendering, ingredient detail toggle with canonical-name clickthrough |
| `runI2VNearest()` / `runI2VArith()` | Ingredient2Vec API: nearest-neighbour query by ingredient name + flavour arithmetic (ingredient1 + ingredient2 - ingredient3) |
| `runFoodAgent()` | Food Agent: natural language query → token matching → centroid search → ranked ingredient suggestions |
| `renderTrending()` | Trending panel: seasonal + rarity (avg neighbour distance) + GLP-1 trend scoring → top 30 + seasonal spotlight |
| `renderMealPlan()` | GLP-1 Meal Plan: cluster GLP-1-friendly ingredients by embedding similarity → 7-day meal table with calorie targets |
| `setupTabs()` / `setupModelTabs()` | Tab switching with category filtering (4 groups: Core/Play/Analyze/Advanced), lazy model switching, URL hash deep-linking, ARIA roles + keyboard arrow navigation |
| `showEmptyState()` | Centralised empty-state helper — renders contextual placeholder text for all 18 panels when no ingredient is selected |
| `closeChefToolkit()` | Close the Chef's Toolkit overlay drawer and backdrop |

The **lazy-loading** architecture means initial load is only 128 KB (`epicure_shared.json`). Model data (~4 MB each) is fetched only when the user switches to that model tab. This makes the app feel instant on desktop and friendly on mobile connections.

### 1.5 Accessibility

The app includes accessibility improvements implemented during June 2026 maintenance cycles:

| Feature | Implementation | Coverage |
|---------|---------------|----------|
| **`aria-label` attributes** | Every `<input>` element has a descriptive `aria-label` | 26 inputs across all tabs |
| **Label bindings** | `<label for="">` attributes associate labels with their inputs | Comparator (Compare 2) ingredient fields |
| **ARIA roles** | `role="tablist"`, `role="tab"`, `aria-selected` toggled dynamically | All 4 category tabs + 18 sub-tabs |
| **Keyboard navigation** | ArrowLeft/ArrowRight navigation on category tabs. Tab order follows visual layout. | Category tabs |
| **Colour contrast** | Dark theme with high-contrast text (`--text3` at #8a8aad, above WCAG AA threshold) | Entire UI |
| **Error states** | Missing features (Spoonacular without API key) show clear error messages rather than silent failure | Conditional |
| **Smart tooltip** | Map tooltip repositions to avoid clipping off right/bottom viewport edges | Map tab hover |

---

## 2. Quick Start & Launch

### 2.1 Prerequisites

- **A modern web browser** (Chrome, Firefox, Safari, Edge — any with ES2020+ support)
- **(Optional) Python 3** — only needed if you want to regenerate the data bundle

### 2.2 Launching the Explorer

**Option A — Python HTTP server (recommended):**

```bash
cd epicure-explorer
python3 -m http.server 8080
```

Then open **http://localhost:8080** in your browser.

> ⚠️ **Don't just open index.html directly (file://)** — the browser's CORS policy blocks `fetch()` of local files. Always serve via HTTP.

**Option B — Any static server:**

```bash
# Node.js
npx serve epicure-explorer

# Python 2
cd epicure-explorer && python -m SimpleHTTPServer 8080

# VS Code
# Right-click index.html → "Open with Live Server"
```

### 2.3 What You'll See

1. **Loading screen** — a spinner while the 12 MB data bundle downloads (1–3 seconds on broadband)
2. **Header** — title, arXiv link, and 3 model tabs (Cooc / Core / Chem), plus the **👨‍🍳 Chef's Toolkit** toggle button
3. **Search bar** — type to find ingredients; autocompletes as you type
4. **✏️ Describe a Dish input** — type a free-form dish description (e.g. "creamy garlic pasta") to get ingredient suggestions via embedding centroid
5. **13 feature tabs** — Neighbours, Compare, Direction, Map, Modes, Recipes, Games, Analyzer, Compare 2, Arith, Cocktails, Seasonal, Spoonacular
6. **Default selection** — `miso` is pre-selected as a starting ingredient

### 2.4 Rebuilding the Data Bundle

If you want to regenerate the data bundle (e.g. after tweaking the preprocess script):

```bash
cd epicure-explorer
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python3 preprocess.py
```

This reads the raw CSV files from `data/` and writes `data/epicure_shared.json` (128 KB) + three per-model JSON files (~4 MB each). It takes about 3–5 minutes on a modern machine (UMAP is the bottleneck).

---

## 3. Feature Walkthrough — The 19 Tabs

### 3.1 🔗 Neighbours

**What it does:** Shows the 25 nearest neighbours of the selected ingredient in the current model's embedding space, ranked by cosine similarity.

**How to use:**
1. Search for an ingredient (e.g. `chocolate`, `olive_oil`, `curry_paste`)
2. The Neighbours panel shows similar ingredients as cards
3. Each card has:
   - **Ingredient name** (underscores → spaces automatically)
   - **Similarity bar** — visual indicator (colour-coded: green >0.7, accent >0.5, blue >0.3, yellow >0.2, grey below)
   - **Similarity percentage** — exact cosine similarity × 100
4. **Click any neighbour** to jump to it — the search bar updates and all panels re-render

**What to look for:**
- Cooc neighbours are typically **recipe co-occurrence** companions (ingredients used together in dishes)
- Chem neighbours are **flavour-profile peers** (share aroma compounds regardless of cuisine)
- Core neighbours blend both signals

**Example: `miso` (default) neighbours in Cooc:**
- `fermented_black_bean`, `gochujang`, `doubanjiang`, `chili_paste`, `soy_sauce` — all fermented bean products used in East Asian cooking

### 3.2 ⚖️ Compare

**What it does:** Side-by-side comparison of the top 10 neighbours across all three models (Cooc, Core, Chem) for the same ingredient.

**How to use:**
1. Select any ingredient
2. Switch to the Compare tab
3. Read across the table: each row is rank #1–10, each column is a model

**What to look for:**
- **Divergence** — where the models disagree reveals the chemistry-vs-context axis in action
- **Shared entries** — ingredients that are neighbours in all three models are robustly similar

**Example: `chicken` in Compare:**

| Rank | Cooc | Core | Chem |
|---|---|---|---|
| 1 | garlic | pork | chicken_broth |
| 2 | onion | beef | turkey |
| 3 | black_pepper | chicken_broth | egg |
| 4 | turkey | peanut | duck |
| 5 | carrot | cream_of_chicken_soup | chicken_liver |

Notice how Cooc gives recipe companions (garlic, onion, black_pepper), while Chem gives flavour-profile peers (chicken_broth, turkey, egg — same savoury/meaty compounds). Core blends both, leaning toward recipe context.

### 3.3 🎯 Direction (SLERP)

**What it does:** Spherical Linear Interpolation (SLERP) between the seed ingredient vector and a semantic direction vector, controlled by a continuous angle (0–90°). This lets you *rotate* an ingredient toward a desired flavour profile.

**How to use:**
1. Select a seed ingredient
2. Choose a **direction** from the dropdown (two groups):
   - **Sensory:** Sweet, Spicy, Savory/Umami, Citrus/Sour, Fermented, Bitter, Creamy/Dairy, Herbal
   - **Cuisine (paper §2.2):** East Asian, Western Atlantic, Mediterranean, Eastern European, Southeast Asian, South Asian, Latin American, Japanese
3. Drag the **angle slider** (0–90°):
   - **0°** = the seed ingredient's own neighbours
   - **30°** = mild rotation toward the target direction
   - **60°** = strong rotation
   - **90°** = pure target direction (seed fully projected onto the semantic pole)
4. The results panel shows the 12 nearest ingredients to the interpolated vector

**What's happening under the hood:**
```
v_result = sin((1-t)·Ω)/sin(Ω) · v_seed  +  sin(t·Ω)/sin(Ω) · v_target

where:
  Ω = angle between v_seed and v_target (radians)
  t = θ / Ω  (θ = user's chosen angle, clamped to [0, Ω])
```

> **💡 Paper reference data:** The `data/direction_arithmetic_full.csv` file contains the paper's SLERP evaluation results — 2,160 rows covering all three models, all 16 directions, and angles 0°, 30°, 60°, and 90°. Each row records the hit rank and similarity of the closest target-cuisine ingredient, so you can compare the app's live results with the paper's published benchmarks. Note: the paper used a slightly different ingredient hit-detection methodology, so live results will approximate but not exactly match the CSV. The app's live SLERP is interactive (any angle, any seed), while the CSV reports fixed-angle evaluations from a prepared set of test cases.

**Example: `olive_oil` + Fermented at 30°**
- Cooc: moves toward pickles, capers, preserved lemon
- Chem: moves toward wine, vinegar, aged cheese

**Example: `chicken` + Japanese at 60°**
- Cooc: → mentsuyu, dashi, bonito_flakes, burdock_root, mirin
- Core: → dashi, mirin, kombu, bonito_flakes, udon_noodle
- Chem: → dashi, bonito_flakes, sake, kombu, mirin

### 3.4 🗺️ Map (UMAP / PCA / Force-Directed Graph + Nutrition Heatmap)

**What it does:** A 2D scatter plot of the 300-D embedding space projected to 2D. Three projection methods are available via the dropdown above the canvas. A **nutrition heatmap overlay** lets you colour-code points by nutritional content — revealing how ingredients cluster by dietary profile, not just flavour.

- **UMAP** (Uniform Manifold Approximation and Projection, cosine metric, 15 neighbours) — preserves local neighbourhood structure, producing tight, interpretable clusters. Best for exploring local relationships.
- **PCA** (Principal Component Analysis) — shows the linear variance of the data. Useful as a baseline comparison to see how non-linear methods differ.
- **Force-Directed Graph** — a spring-force simulation (Fruchterman-Reingold) built from the top-15 neighbour edges per ingredient. Shows the actual graph structure of the embedding rather than a geometric projection. Initialised from UMAP coords for fast convergence (35 iterations with temperature cooling).

Unlike PCA, UMAP preserves local neighbourhood structure, producing tighter, more interpretable clusters.

**How to use:**
1. Switch to the Map tab
2. Choose a projection method from the dropdown
3. **Optional:** Select an overlay from the **Overlay** dropdown below the projection selector:
   - **Nutrients** — points coloured by nutritional content per 100g (green → yellow → red):
     - 🔥 **Calories**, 🥩 **Protein**, 🧈 **Fat**, 🌾 **Carbs**, 🥬 **Fiber**
   - **🗓️ Season** — points coloured by peak season (green=spring, yellow=summer, orange=autumn, blue=winter)
4. The legend shows the colour gradient with min/max values for the selected nutrient
5. **Search** — type an ingredient name in the 🔍 Find on map input and press Enter or click Find. The view centers at 3× zoom with a purple pulse ring animation for 2 seconds
6. **Hover** over any point to see its ingredient name (tooltip repositions to avoid screen edges)
7. **Click** any point to select that ingredient — all other tabs update
8. **Drag** to pan around the map
9. **Scroll wheel** to zoom in/out (0.5×–20×), centered on cursor position
10. **Double-click** to reset zoom/pan to initial view
11. The selected ingredient is highlighted in **purple** with a white ring and label
12. **Touch:** single-finger drag to pan, two-finger pinch to zoom
13. Switch models (Cooc/Core/Chem) to see how the geometry changes (viewport resets automatically)

**What to look for:**
- **Clusters** — ingredients that group together in the projection are nearby in the original 300-D space
- **Core's concentration** — Core's points are more tightly clustered (participation ratio 94.2) vs Cooc and Chem (173.6 and 183.1)
- **Method differences** — compare UMAP's tight clusters vs PCA's linear spread vs Force-Directed's explicit graph edges
- **Axis meanings** — while PCA axes don't have fixed culinary interpretations, consistent regions often correspond to broad categories (fermented ingredients in one area, dairy in another)
- **Nutrition heatmap insight** — enable the nutrition overlay to see how ingredients with similar nutritional profiles form cross-cuisine clusters (e.g., low-calorie vegetables cluster together regardless of cuisine origin; high-fat ingredients like oils, nuts, and fatty meats occupy a separate region)

**Canvas features:**
- Canvas is 480px tall (300px on tablets, 220px on mobile), fills the panel width
- High-DPI rendering (respects devicePixelRatio)
- Points are 2.5px radius (semi-transparent); selected is 8px with stroke
- Hover threshold: 12px; click threshold: 20px (drag movements over 2px are treated as pan, not click)
- Region labels: cuisine centroids auto-computed and drawn as coloured pill labels when zoomed in above 0.3×
- Status bar dynamically shows the active projection method (UMAP / Force-Directed / PCA)

### 3.5 🏷️ Modes

**What it does:** Shows the GMM-discovered culinary modes that the selected ingredient belongs to. These are named clusters of co-occurring ingredients that share a coherent culinary role.

**How to use:**
1. Select an ingredient
2. Switch to the Modes tab
3. See a list of all modes containing the ingredient, each showing:
   - **Mode label** (e.g. "East Asian fermented sauces and processed staples")
   - **Mode kind** (continuous or discrete) + property name
   - **Member count** and **full member list**

**What to look for:**
- An ingredient can belong to **multiple modes** — a versatile ingredient like `soy_sauce` may appear in 2–3 modes
- Mode labels are human-readable names derived from the GMM cluster's members
- Core's modes are the **tightest** (mean coherence 0.833 vs 0.611 for Cooc)
- **Filter modes** by label text or minimum member count using the controls above the list
- **Cross-mode ingredient search** — use the "Search ingredient across all modes" field below the filters to find every mode containing an ingredient, independent of what's selected. Matching ingredient names are highlighted in purple.

**Example: `miso` in Core mode atlas:**
- Mode `nova_level/M1`: "East Asian fermented sauces and processed staples" (196 members) — alongside gochujang, doubanjiang, soy_sauce, etc.

---

## 3.6 🍲 Recipes

**What it does:** A practical recipe-building workspace that turns the embedding space into actionable ingredient lists. Three sub-tabs let you explore ingredient pairings from different angles.

### 3.6.1 🌍 By Cuisine

Rotates the selected ingredient toward any of the 8 cuisine macro-regions (East Asian, Western Atlantic, Mediterranean, etc.) via SLERP and groups the resulting top-16 neighbours by ingredient category. The angle slider (15°–75°) controls how far the ingredient is "translated" toward the target cuisine.

**How to use:**
1. Select a seed ingredient (e.g. `chicken`)
2. Pick a cuisine direction from the dropdown (e.g. `Southeast Asian`)
3. Drag the angle slider to your desired intensity
4. See the result organised by category: produce, protein, spices, dairy, grains, condiments, legumes/nuts

**What to look for:**
- At low angles (15–30°) you get subtle cuisine inflections — a few ingredients shift
- At higher angles (60–75°) the list is dominated by the target cuisine
- 45° is a good default — a balanced blend of the seed and cuisine

**Example: `chicken` + Japanese at 45°:**
| Category | Ingredients |
|---|---|
| 🥬 Produce | shiso, daikon, negi, mitsuba, enoki |
| 🥩 Protein | bonito_flakes, dashi, katsuobushi, chicken_liver |
| 🌿 Spices & Herbs | shichimi_togarashi, sansho_pepper, wasabi |
| 🧂 Condiments & Sauces | soy_sauce, mirin, sake, ponzu, teriyaki_sauce |
| 🍚 Grains & Pantry | soba, udon, rice, panko |

### 3.6.2 🔗 Bridge Finder

**What it does:** Average the embedding vectors of 2–3 ingredients and find the nearest neighbours to the combined point. This reveals ingredients that *bridge* the gap between your selections — items that pair well with everything you've chosen.

**How to use:**
1. The main selected ingredient is always the first bridge ingredient
2. Type ingredient names into the additional search fields (press Enter to confirm)
3. Leave a field blank to use only 2 ingredients
4. The results show neighbours of the averaged vector, grouped by category

**What to look for:**
- Ingredients that appear in all three selections' individual neighbourhoods are the strongest bridges
- The bridge often finds ingredients that neither seed has as a close neighbour alone
- Try contrasting pairs: `chocolate` + `chili`, `miso` + `butter`, `olive_oil` + `soy_sauce`

**Example: `miso` + `butter` bridge:**
- The bridge finds savoury-fermented-rich crossovers like aged cheeses, roasted nuts, and umami-loaded vegetables — ingredients that work in both Japanese and Western contexts.

### 3.6.3 🧂 Flavour Boosters

**What it does:** Shows the selected ingredient's top neighbours from the **Chem model** (flavour-profile peers), grouped by category. These are ingredients that share aroma compounds regardless of recipe context — ideal for finding flavour affinities you wouldn't normally consider.

**How to use:**
1. Select any ingredient
2. Switch to the Flavour Boosters sub-tab
3. See Chem-model neighbours organised by category

**What to look for:**
- These are *chemistry*-driven pairings, not recipe-driven ones — they reveal latent flavour commonalities
- When the Chem model isn't loaded yet, Cooc neighbours are shown instead with a note
- Great for finding unexpected substitutes or "why does this work?" pairings

**Example: `parmesan_cheese` flavour boosters:**
| Category | Ingredients |
|---|---|
| 🥬 Produce | tomato, mushroom, garlic |
| 🧀 Dairy | pecorino, grana_padano, asiago, romano |
| 🌿 Spices & Herbs | black_pepper, nutmeg, oregano |
| 🥩 Protein | anchovy, prosciutto, egg |
| 🍚 Grains & Pantry | bread_crumb, pasta, rice |

---

### 3.7 🎮 Mini-Games

**What it does:** Three games that test and train your culinary intuition using the embedding space — no extra data needed, everything comes from the pre-computed neighbours and direction vectors.

#### 🌍 Cuisine Fusion Explorer

A professional tool for discovering **cross-cultural bridge ingredients** — ingredients that are equally at home in two different cuisines. Powered by the embedding's cuisine direction vectors.

**How to use:**
1. Select two cuisines from the dropdowns (e.g. Japanese and Mediterranean)
2. Click **"Find Bridges"** — or change either dropdown to trigger an auto-search
3. The engine scores all 1,790 ingredients by `min(sim_to_A, sim_to_B)`, then applies a symmetry boost (ingredients equally similar to both cuisines rank highest)
4. Results show the top 24 bridge ingredients with colour-coded similarity bars
5. **Click any ingredient** to select it and explore its full profile

**What to look for:**
- Genuinely bilingual ingredients: e.g. `soy_sauce` bridges Japanese and East Asian at 80%+ for both
- Surprising crossovers: `sesame_oil` bridges East Asian and Mediterranean; `chili_flake` connects Latin American and SE Asian
- A balanced score (45%/45%) is more valuable than a skewed one (80%/20%) — the symmetry boost highlights these
- Try unexpected pairs: Latin American × Japanese, Mediterranean × SE Asian, Eastern European × South Asian

**Professional use case:** A chef designing a fusion tasting menu uses the Fusion Explorer to find the **affinity zones** between two cuisines' flavour vocabularies. The bridge ingredients become the menu's conceptual anchors — a soy-lime vinaigrette that works on both a Japanese sashimi and a Peruvian ceviche.

#### 🔮 Guess the Neighbour

A quiz that shows an ingredient and asks: "Which of these 4 options is the closest embedding neighbour?"

**How to play:**
1. Switch to the Games tab (🎮 Play category)
2. A random ingredient is chosen (e.g. "miso"), and 4 options are shown
3. Click the ingredient you think is the closest neighbour
4. Correct answers turn **green**; wrong answers turn **red** with the correct answer revealed
5. Click **"New Question"** for another round
6. Your **stats** (won/played, streak) are tracked in the leaderboard and persist across sessions via localStorage

**What to look for:**
- The closest neighbour is **not always obvious** — embeddings capture subtle semantic relationships
- Cooc neighbours are recipe companions; Chem neighbours are flavour-profile peers
- The game works with any model — switch to Cooc/Core/Chem to change the challenge

#### 🌍 ID the Cuisine

A quiz that shows 3–4 ingredients and asks: "Which cuisine do these belong to?"

**How to play:**
1. Click **"🌍 ID the Cuisine"** in the game mode selector bar
2. 3–4 ingredients from a random cuisine are displayed (e.g. "miso, soy_sauce, nori")
3. Choose from 4 cuisine options (East Asian, Western Atlantic, Mediterranean, Eastern European, SE Asian, South Asian, Latin American, Japanese)
4. Correct answers turn **green**; wrong answers turn **red** with the correct cuisine revealed
5. Click **"New Question"** for another round
6. Stats are tracked separately from Guess the Neighbour

**How it works:** The embedding's 8 cuisine direction vectors score every ingredient. Ingredients with a dot-product > 0.15 against a cuisine vector are candidates — this reliably identifies cuisine-affiliated ingredients.

#### 🗄️ Game Leaderboard

Three stat cards show your performance:
- **🔮 Neighbour** — won/played, best streak for Guess the Neighbour
- **🌍 Cuisine ID** — won/played, best streak for Cuisine ID
- **🏆 Total** — combined win rate percentage

The leaderboard auto-updates after every guess and is persisted in localStorage under the key `epicure_games`.

#### 🧭 Flavour Compass

A polar radar chart showing how the selected ingredient relates to all 8 sensory directions simultaneously.

**How to use:**
1. Select an ingredient (or click one on the map)
2. Switch to the Games tab to see the radar chart
3. Each axis represents a sensory direction: Sweet, Spicy, Savory/Umami, Citrus/Sour, Fermented, Bitter, Creamy/Dairy, Herbal
4. The distance from centre shows the cosine similarity between the ingredient vector and each direction vector
5. Ingredients with a strong affinity for a direction reach further out on that axis

**What to look for:**
- A well-rounded ingredient (e.g. `tomato`) shows moderate affinity across many directions
- Strongly directional ingredients (e.g. `sugar` → Sweet, `lemon` → Citrus/Sour) have one dominant axis
- The purple polygon's shape gives an at-a-glance flavour profile

**Example: `miso` flavour compass:**
- Strong Savory/Umami and Fermented axes
- Moderate Bitter and Sweet
- Low Creamy/Dairy and Citrus/Sour

### 3.8 👨‍🍳 Chef's Toolkit Pro — Ingredient Intelligence Hub

**What it does:** A slide-out overlay drawer that serves as a professional ingredient intelligence hub. It slides in from the right with a dimmed backdrop — click the backdrop or the close button to dismiss. Six data sections — including molecular flavour notes, a substitution context toggle, GLP-1 dietary mode, explainable substitutions, cross-culture bridge analysis, and cost/waste reduction hints — all computed from the embedding space and built-in heuristics. No external API calls.

**How to use:**
1. Click the **"👨‍🍳 Chef's Toolkit"** button in the header to open the overlay
2. Click the backdrop or the **✕** button to close
3. Select any ingredient to see its complete intelligence profile

**The sidebar shows six sections:**

| Section | Content | Pro Feature |
|---|---|---|
| 🥗 **Dietary Profile** | 6 heuristic dietary tags + **💊 GLP-1 friendliness** badge (green/yellow/red) — 15M+ Americans on GLP-1 drugs (Ozempic, Wegovy) need high-protein, satiety-promoting ingredients | First consumer food AI tool with dedicated GLP-1 dietary awareness |
| 🔄 **Best Substitutes** | Top 5 nearest embedding neighbours with similarity percentages. **Context toggle:** switch between 📊 Current, 📖 Recipe-context (Cooc), 🧪 Flavour-chemistry (Chem). **💊 GLP-1 filter toggle:** shows only GLP-1-friendly substitutes. **💡 Explain button:** click to see *why* a substitute works — shared molecular notes, aligned sensory directions, overlapping cuisine affinities | **GLP-1 filter** is a first-mover feature — no competitor offers diet-mode ingredient filtering. **Explain button** builds trust by showing the embedding's reasoning, not just a score |
| 🌍 **Cuisine Affinity** | Horizontal bar chart of cosine similarity to 8 cuisine macro-regions. Longer bars = stronger affinity | Combined with the **Fusion Explorer** in the Games tab, you can find specific bridge ingredients for any cuisine pair |
| 🧪 **Flavour Profile** | Tag badges for 8 sensory directions with similarity percentages | **🧬 Molecular Notes** are automatically derived from directional combos — e.g. high Savory + high Fermented = "Amino Acid" note; high Sweet + high Creamy = "Lactone" note |
| 💎 **Cost & Waste Hints** | Dynamic tips based on ingredient name: luxury alternatives, root-to-stem usage, seasonal peak alerts | Kitchen-tested cost-saving and zero-waste strategies |
| 📋 **Export Summary** | Button at the bottom of the sidebar — copies a formatted text summary of the current ingredient to clipboard (name, model, GLP-1 status, top 5 substitutes with similarity %, cuisine affinity %, flavour profile) | Turn exploration into action — paste findings into menu docs, recipe cards, or team notes |

**What to look for:**
- **GLP-1 badge** in Dietary Profile: 💚 Friendly (high protein, satiety-promoting, low glycemic), ⚠️ Poor (high fat, ultra-processed, high glycemic), 💊 Neutral. 15M+ GLP-1 users — this is the first consumer food AI tool with dedicated GLP-1 awareness
- **GLP-1 filter toggle** below the substitution mode toggle: click "💚 GLP-1 Friendly" to filter substitutes to only GLP-1-compatible ingredients. Combined with Chemistry substitution mode, it finds flavour peers that are also GLP-1 safe
- **💡 Explain button** on each substitute: click to see *why* the embedding considers it a good swap — shared molecular notes (e.g., both are Amino Acid + Maillard), aligned sensory directions (both score high on Savory/Umami and Fermented), and overlapping cuisine affinities
- **Substitution mode toggle**: switch to "Chemistry" to see flavour-profile peers (ideal for plating substitutions where you want the same molecular impression) or "Recipe" to see recipe-context peers (ideal for structural substitutions where function matters more than flavour)
- **Molecular notes** (Lactone, Ester, Terpene, Pyrazine, Polyphenol, Amino Acid, Maillard, Pungent, Acetic, Lipid, Vanillic, Sulfurous) are derived from sensory direction combinations — they're computational approximations of the molecular families that flavour chemists use
- **Cost hints** flag luxury ingredients (truffle, saffron, caviar, foie gras, lobster, uni) with budget-friendly alternatives
- **Waste reduction hints** suggest root-to-stem usage, herb storage, and stock-making from bones
- **📋 Export Summary** button at the bottom: click to copy a formatted ingredient intelligence summary to clipboard — paste it into a menu brief, recipe card, or team collaboration doc

**Example: `miso` Chef's Toolkit Pro:**
- Dietary: ✅ Vegan, ✅ Vegetarian, ⚠️ Gluten-Free, ❌ Soy-Free, ✅ Nut-Free, ✅ Dairy-Free, 💚 **GLP-1 Friendly** (fermented soy is high-protein, satiety-promoting)
- Substitutes (Current): gochujang 72%, doubanjiang 70%, soy_sauce 68%, tamari 65%, fermented_black_bean 63%
  - 💡 *Why gochujang?* → 🧬 Shared molecular notes: Amino Acid, Maillard, Acetic. 🧪 Aligned on: Savory/Umami (76%), Fermented (68%). 🌍 Overlap in: East Asian (82%)
  - 💡 *Why doubanjiang?* → 🧬 Shared molecular notes: Amino Acid, Fermented. 🧪 Aligned on: Savory/Umami (72%), Fermented (65%). 🌍 Overlap in: East Asian (79%), SE Asian (51%)
- Substitutes (Chemistry): soy_sauce 58%, fish_sauce 52%, nutritional_yeast 48%, vegemite 44%, marmite 43%
- Cuisine: East Asian 91%, SE Asian 62%, Japanese 58%, others <30%
- Flavour: Savory/Umami 78%, Fermented 71%, Bitter 42%, Sweet 31%
- Molecular notes: Amino Acid, Maillard, Acetic
- Cost hint: soy-based products are typically cost-effective; no luxury flag


### 3.9 ✏️ Describe a Dish — Natural Language → Shopping List

**What it does:** A professional free-text input that turns dish descriptions into ingredient suggestions — like having a sous-chef who instantly translates "creamy garlic pasta with mushrooms" into a shopping list of the 12 most relevant canonical ingredients. No API calls — everything is resolved from a pre-bundled keyword-to-ingredient mapping (200+ food-description words mapped to canonical ingredient names) combined with the embedding's vector centroid.

**How to use:**
1. Type a dish description in the input field below the search bar (e.g. "creamy garlic pasta with mushrooms and lemon")
2. Results appear automatically as you type (debounced at 300ms) or press Enter
3. Matched keywords are shown as purple tags above the results — gives visibility into what the system "heard"
4. Suggested ingredients appear as clickable cards with similarity percentages to the computed centroid
5. Click any suggestion to select it, then explore its neighbours, substitutes, and flavour profile

**What's happening under the hood:**
1. Your text is tokenized and stop-words are filtered
2. Each keyword is looked up in the 200+ entry keyword-to-ingredient map (e.g. "creamy" → cream, yogurt, coconut_milk)
3. The matched ingredients' embedding vectors are averaged into a **centroid**
4. The centroid is normalised and searched against the full 1,790-ingredient embedding space
5. The matched ingredients themselves are excluded from results — you only see *new* suggestions

**What to look for:**
- The keyword map is hand-curated by a chef/AI expert: it covers ingredients (chicken, garlic), descriptors (creamy, spicy, smoky, velvety, zesty), and cooking styles (roasted, fresh, toasted)
- Results change across models: Cooc gives recipe-driven suggestions, Chem gives flavour-profile-driven ones
- The centroid captures the *semantic centre* of your description — not just the individual keywords but their combined flavour territory

**Example: "creamy garlic pasta with mushrooms":**
- Matches: cream, garlic, pasta, mushroom
- Cooc suggestions: olive_oil, parmesan, butter, black_pepper, onion, parsley, white_wine, thyme, chicken_broth, rosemary
- Chem suggestions: butter, parmesan, cream, mushroom, garlic, shallot, white_wine, thyme, egg_yolk, truffle

**Example: "spicy thai curry with coconut":**
- Matches: spicy, coconut
- Suggestions: lemongrass, galangal, kaffir_lime, fish_sauce, chili, thai_basil, shallot, palm_sugar, tamarind, cilantro

**Professional use case:** A chef developing a new dish types a rough description into the input to see what the embedding space "recommends" as the canonical ingredient list. The suggestions often include ingredients the chef hadn't considered — because the centroid captures latent relationships that aren't obvious from the keywords alone.

### 3.10 🧮 Flavour Arithmetic Explorer — Visual Expression Builder

**What it does:** An interactive chip-based UI for building flavour expressions. Add ingredients as visual chips, and the app instantly computes the embedding centroid and shows the closest neighbours — just like vector arithmetic with a visual playground.

**How to use:**
1. Switch to the **🧮 Arith** tab
2. You'll see default chips: `chicken` + `coconut milk` + `ginger` — the results are shown instantly
3. **Add ingredients:** start typing in the "Add ingredient…" search field — a dropdown shows matching ingredients; click one to add it as a chip
4. **Remove ingredients:** click the ✕ on any chip to remove it — results update automatically
5. **Clear all:** click 🗑️ **Clear** to start fresh
6. **Reset example:** click ↺ **Reset example** to restore the default chicken + coconut milk + ginger combination
7. **History:** the last 6 expressions are shown above the results — click any to reload that combination
8. **Click any result** ingredient to jump to its full profile (neighbours, substitutes, map, etc.)

**What's happening under the hood:**
1. Each chip ingredient's embedding vector is averaged into a **centroid**
2. The centroid is normalised and all 1,790 ingredients are ranked by cosine similarity
3. The input ingredients are excluded from results — you only see *new* suggestions
4. The flavour profile shows the centroid's affinity to all 8 sensory directions

**What to look for:**
- **Unexpected combinations**: try `chocolate + chili + cinnamon` → the centroid reveals ingredients that bridge sweet, spicy, and warm flavours
- **Taste the difference**: `tomato + basil + mozzarella` → the classic Caprese profile; try swapping mozzarella for `avocado` to see how the profile shifts
- **Cross-cultural fusion**: `soy_sauce + olive_oil` → ingredients that work in both East Asian and Mediterranean contexts
- **Model effects**: switch models (Cooc/Core/Chem) to see how the arithmetic changes — Chem gives chemistry-driven results, Cooc gives recipe-driven ones

**Example: `chicken + coconut_milk + ginger`:**
- Top result in Cooc: `garlic`, `onion`, `chili`, `lemongrass`, `fish_sauce`
- Flavour profile: Savory/Umami 60%, Spicy 40%, Citrus/Sour 35% — a classic Southeast Asian curry base
- Try adding `thai_basil` as a fourth chip to see how the profile tightens toward Thai flavours

### 3.11 🍸 Cocktail Mixology — Spirit-Driven Drink Intelligence

**What it does:** Enter your available spirits and mixers to discover cocktail-adjacent ingredients from the embedding space. The app computes the flavour centroid of your spirit + mixers and finds ingredients that would complement the combination — like having a virtual bartender suggest unexpected but harmonious pairings.

**How to use:**
1. Switch to the **🍸 Cocktails** tab
2. **Pick a base spirit** from the dropdown: Vodka, Gin, Rum, Tequila, Mezcal, Whiskey, Bourbon, Scotch, Cognac, Brandy, Sake, or Soju
3. **Add mixers/modifiers** in the text fields (up to 3): e.g. `lime`, `simple_syrup`, `mint`, `tonic_water`, `ginger_beer`
4. Click **🍸 Mix** or change the spirit dropdown — results update instantly
5. **Try the presets** for classic cocktails:
   - 🍹 **Moscow Mule** — vodka + lime + ginger beer
   - 🍹 **Margarita** — tequila + lime + triple sec
   - 🍹 **Gin & Tonic** — gin + tonic water + lime
   - 🍹 **Mojito** — rum + mint + lime + simple syrup
   - 🍹 **Old Fashioned** — whiskey + bitters + simple syrup
   - 🍹 **Bloody Mary** — vodka + tomato juice + worcestershire sauce + lemon
6. **Click any result** ingredient to jump to its full profile (neighbours, substitutes, map)

**What's happening under the hood:**
1. The spirit and mixer names are matched to canonical ingredient names in the embedding space (exact match → fuzzy fallback)
2. The matched ingredients' embedding vectors are averaged into a **centroid** — the "flavour centre" of your cocktail
3. All 1,790 ingredients are ranked by cosine similarity to the centroid
4. The input ingredients are excluded from results — you only see *new* suggestions
5. The drink profile shows the centroid's affinity to all 8 sensory directions
6. Molecular notes are derived from the centroid's directional combos — e.g. high Citrus/Sour + high Sweet = "Ester" note

**What to look for:**
- **Spirit effects**: switching from vodka (neutral) to gin (botanical) dramatically shifts the result set. Try the same mixer set with different spirits
- **Unexpected companions**: the embedding often suggests ingredients you wouldn't think of as "cocktail ingredients" — the flavour centroid captures latent relationships
- **Model switching**: switch to Chem model to see chemistry-driven results (flavour-compound peers) vs Cooc (recipe-driven peers)
- **Preset exploration**: load a preset, then swap one mixer to see how the profile tilts

**Example: Moscow Mule (vodka + lime + ginger_beer):**
- Top results: cucumber, mint, simple_syrup, soda_water, lime_juice, lemon
- Drink profile: Citrus/Sour 55%, Sweet 35%, Herbal 30% — bright, refreshing, slightly sweet
- Molecular notes: Ester, Terpene, Acetic — fruity, botanical, and tangy notes

### 3.12 🗓️ Seasonal Ingredient Calendar — Menu Planning by Peak Season

**What it does:** Browse 149 ingredients by their peak growing season. Each ingredient is tagged with Spring, Summer, Autumn, and/or Winter based on its natural harvest period. Ingredients spanning multiple seasons (e.g., carrots are in season spring through winter) are included in all relevant views.

**How to use:**
1. Switch to the **🗓️ Seasonal** tab
2. **Pick a season** from the dropdown: 🌱 Spring (Mar–May), ☀️ Summer (Jun–Aug), 🍂 Autumn (Sep–Nov), ❄️ Winter (Dec–Feb)
3. The app shows all ingredients that peak in that season, **grouped by category**: 🥬 Produce, 🥩 Meat & Protein, 🌿 Spices & Herbs, 🧀 Dairy, 🍚 Grains & Pantry
4. The **"Current" button** jumps to today's season automatically
5. The **"Next" button** advances through the seasons — great for menu planning
6. **Click any ingredient** to select it and explore its full profile (neighbours, substitutes, map)
7. **Map overlay:** Switch to the 🗺️ Map tab and select **"🗓️ Season"** from the Overlay dropdown — points are coloured by peak season (green=spring, yellow=summer, orange=autumn, blue=winter)

**What's happening under the hood:**
1. Every ingredient name is checked against a curated 149-ingredient peak-season database
2. Multi-season ingredients (e.g., kale peaks in autumn AND winter) appear in all applicable seasons
3. Ingredients are assigned to categories using the same rules as the Dish Analyzer
4. The summary bar shows how many seasonal ingredients are available vs the total 1,790

**What to look for:**
- **Seasonal produce clusters** on the Map: when you enable the Season overlay, you'll see spring and summer ingredients clustering differently — reflecting their different flavour profiles
- **Cross-season ingredients**: many items like carrots, beets, and cabbage span 3+ seasons — they're the workhorses of menu planning
- **Protein seasonality**: game meats (venison, pheasant) peak in autumn; lamb in spring; shellfish have distinct seasonal windows
- **Menu planning workflow**: use the Next button to plan ahead — see what will be in season next month and start designing dishes around it

**Example: ☀️ Summer:**
- 50+ seasonal ingredients across all categories
- Top produce: tomato, zucchini, corn, eggplant, bell pepper, cucumber, berries, stone fruits, melon
- Top herbs: basil, cilantro, oregano, rosemary, thyme, sage
- Seafood: salmon, trout, mackerel, lobster, crab, shrimp


### 3.13 🌐 Spoonacular API — Live Recipe Search & Nutrition

**What it does:** Connects to the [Spoonacular Food API](https://spoonacular.com/food-api) for live recipe search, nutrition data, and wine pairing — extending the embedding intelligence with real-world recipe and nutrition databases. A free API key is required.

**Setup:**
1. Go to [spoonacular.com/food-api](https://spoonacular.com/food-api) and sign up for a **free API key** (150 daily calls)
2. Switch to the 🌐 Spoonacular tab
3. Paste your API key in the key field and click **💾 Save Key** — it's stored in your browser (localStorage) and persists across sessions
4. The key is valid until you click **🗑️ Clear**

**Three features, side by side:**

**🔍 Search Recipes by Ingredients**
1. Enter ingredients separated by commas (e.g. `chicken, garlic, lemon, olive oil`)
2. Choose result count (5/10/15) and optional diet filter (Vegetarian, Vegan, Gluten-Free, Ketogenic, Whole30)
3. Click **🍲 Find Recipes** — results show recipe cards with images, used/missed ingredient counts, and likes
4. **Click any recipe** to view per-serving nutrition data (calories, protein, fat, carbs, fiber), cook time, servings, and health score
5. Click **⬅️ Back to results** to return to the recipe list

**🍷 Wine Pairing**
1. Enter a dish or ingredient (e.g. `steak`, `salmon`, `pasta with cream sauce`)
2. Click **🍷 Find Wine** — Spoonacular returns recommended wine types and a pairing explanation
3. If available, specific wine product matches are shown with ratings and prices

**📊 Nutrition Lookup**
1. Enter a food item with quantity (e.g. `1 cup rice`, `100g chicken breast`, `large avocado`)
2. Click **🥗 Get Nutrition** — returns calories, protein, fat, and carbs from Spoonacular's nutrition database

**Let's there be no API, there is no API:** If no API key is set or the daily quota is exceeded, clear error messages guide the user. The app works fully without Spoonacular — this is an optional enhancement layer.

**What to look for:**
- **Cross-reference with embedding data**: the recipes found by Spoonacular often mirror the embedding neighbours — ingredients that co-occur in recipes
- **Diet filter synergy**: combine the diet filter with the app's built-in GLP-1 mode for GLP-1-friendly recipe discovery
- **Wine + ingredient pairing**: find a wine for a dish, then use the embedding's Chef's Toolkit to explore flavour affinities between the wine and the dish's ingredients

### 3.14 📸 Snap — Image→Ingredient Search

**What it does:** Upload a food photo → Spoonacular AI identifies the dish → fetches matching recipes → cross-references recipe ingredients against the embedding space for clickthrough exploration.

**How to use:**
1. Drop or click to upload a food photo (JPG, PNG)
2. Click **🔍 Identify Dish** — Spoonacular's image classification API identifies the dish category
3. Recipe cards appear with ingredient lists — click **▶** to expand
4. Any ingredient that matches the canonical embedding space shows a 🔗 link — click it to jump to that ingredient

**Requires:** A [Spoonacular API key](https://spoonacular.com/food-api) entered in the 🌐 Spoonacular tab.

### 3.15 🔬 Ingredient2Vec — Embedding Query API

**What it does:** Direct query interface for the embedding space — nearest-neighbour search and flavour arithmetic without selecting a base ingredient.

**How to use:**
- **🔍 Nearest Neighbour:** Enter an ingredient name, pick a model (Cooc/Core/Chem), click Query → top 25 neighbours with similarity bars
- **➕ Flavour Arithmetic:** Enter an expression like `chicken + coconut_milk + ginger` or `miso + rice - salt` → centroid results ranked by similarity
- Press **Enter** in either input field to trigger the query

### 3.16 🤖 Food Agent — Natural Language Ingredient Search

**What it does:** Describe what you're craving in plain English — the agent parses your description into embedding-matching terms and finds the closest ingredients.

**How to use:**
1. Enter a craving like `"creamy garlic pasta with mushrooms"` or `"something light and citrusy"`
2. Click **🤖 Ask Agent** (or press Enter)
3. The agent shows matched terms and ranked ingredient suggestions with similarity percentages
4. Click any ingredient to load it in the full embedding view

**Best results with:** Descriptive terms (creamy, spicy, umami, smoky), specific ingredients (mushrooms, garlic, ginger), or cuisine adjectives (Japanese, Italian, Thai).

### 3.17 📈 Trending — What's Trending Panel

**What it does:** Computes a trend score for all 1,790 ingredients based on three signals: seasonal relevance (what's in season now), embedding rarity (uniqueness in flavour space), and GLP-1 friendliness.

**How to use:**
1. Switch to the 📈 Trending tab — scores compute automatically
2. **🔥 Top Trending Now** — the 18 highest-scoring ingredients with badges (🗓️ seasonal, 💊 GLP-1 friendly, 🌟 rare)
3. **🗓️ Seasonal Spotlight** — in-season ingredients sorted by rarity
4. Click any ingredient card to jump to it

**Scoring:** Trend score = 0.4 × seasonal + 0.4 × rarity + 0.2 × GLP-1 (or -0.1 for GLP-1 unfriendly).

### 3.18 💊 Meal Plan — GLP-1 Meal Plan Generator

**What it does:** Generates a 7-day, 3-meals-per-day plan using only GLP-1-friendly ingredients, grouped into embedding-similar flavour clusters for complementary pairings.

**How to use:**
1. Select a calorie target: 1,200 (weight loss), 1,500 (moderate), 1,800 (maintenance), or 2,000 (active)
2. Click **🔄 Generate Plan**
3. The table shows Monday–Sunday with 🌅 Breakfast, ☀️ Lunch, and 🌙 Dinner pairings
4. Scroll below the table for the full list of GLP-1-friendly ingredients used — click any to explore

**How it works:** GLP-1-friendly ingredients are clustered by embedding similarity. Each meal picks two ingredients from the same cluster, ensuring complementary flavours. Meals cycle through clusters deterministically for variety.

### 3.19 👨‍🍳 Build-A-Dish — Ingredient Composition Studio

**What it does:** Combine 2–6 ingredients and discover what the embedding space suggests to complete your dish. Shows centroid-based pairings, a flavour profile radar chart, category breakdown, and dietary flags.

**How to use:**
1. Switch to the **👨‍🍳 Build Dish** tab (🎮 Play category)
2. Start typing an ingredient in the chip input — an autocomplete dropdown shows matching names
3. Press Enter or click a suggestion to add it as a chip (up to 6)
4. Click **🔍 Find Pairings** to run the analysis
5. The results panel shows:
   - **Top 12 suggested additions** — ingredients whose vectors are closest to the computed centroid
   - **🧭 Flavour Profile** — a radar chart of the combined dish's 8 sensory directions
   - **📦 Category breakdown** — colour-coded badges showing ingredient categories (Produce, Protein, Spice, etc.)
   - **🏷️ Dietary flags** — GLP-1 Friendly, Vegan, High Protein badges when applicable
6. Click any suggested ingredient to explore its full profile
7. Click **📋 Copy Ingredients** to copy the list to your clipboard
8. Click **🗑️ Clear All** to start fresh

**How it works:** The embedding centroid of all selected ingredients is computed (vector average). All other ingredients are scored by cosine similarity to this centroid. The highest-scoring ingredients represent flavours that naturally complement the combination — they're the embeddings' best guess at "what goes with everything you've chosen."

**Professional use case:** A chef has a base of chicken, garlic, and olive oil. Build-A-Dish might suggest rosemary, lemon, white_wine, and thyme — the embedding space recognizes this as a classic Mediterranean poultry profile and fills in the expected companions.

### 3.20 🔬 Nutrition Deep-Dive & FSA Health Direction

**What it is:** For every ingredient, the app shows a **Nutrition Deep-Dive** card in the Chef's Toolkit sidebar with FSA traffic lights (🟢🟡🔴) per 100g for energy, protein, fat, saturates, sugars, salt, carbs, and fiber. An additional **🥗 Nutrition** subtab in the Recipe Explorer shows per-recipe FSA scores from the im2recipe 35K dataset (51K+ recipes). A **💚 FSA Health** SLERP-able direction vector lets you rotate any ingredient toward healthier alternatives.

**How it works:** The nutrition data comes from the im2recipe-Pytorch 35K per-recipe dataset (MIT license), matched via USDA FoodData Central. The app's `build_nutrition.py` pipeline (45 KB) covers all 1,790 Epicure ingredients with 409 exact USDA matches and 1,381 food-group-heuristic estimates. When the 35K per-recipe dataset was obtained (via Recipe1M data access), `build_nutrition.py --import-im2recipe` indexed all 51,235 recipes with their per-recipe FSA traffic lights.

**Where to find it:**
- **Chef's Toolkit Pro** → scroll to the **🔬 Nutrition per 100g (im2recipe)** section — shows the ingredient's FSA traffic light breakdown
- **Recipe Explorer** → click the **🥗 Nutrition** subtab — shows per-100g base nutrition + sample recipes with per-recipe FSA scores
- **Direction (SLERP)** → new **💪 Health** optgroup with **💚 FSA Health** direction — rotate any ingredient toward healthier alternatives

**FSA thresholds (UK Food Standards Agency, per 100g):**
| Category | 🟢 Low | 🟡 Medium | 🔴 High |
|----------|--------|-----------|--------|
| Fat | ≤ 3g | ≤ 17.5g | > 17.5g |
| Saturates | ≤ 1.5g | ≤ 5g | > 5g |
| Sugars | ≤ 5g | ≤ 22.5g | > 22.5g |
| Salt | ≤ 0.3g | ≤ 1.5g | > 1.5g |

**Professional use case:** A chef developing a health-conscious menu can SLERP an indulgent ingredient (e.g. butter) toward `💚 FSA Health` — the resulting substitutions trend toward lower-fat, lower-salt alternatives (olive oil, avocado, yogurt) that preserve the culinary role while improving the FSA profile. The per-recipe nutrition tab then shows real-world recipes using each substitution, with their actual FSA scores.

**Technical note:** The `build_nutrition.py` pipeline is designed to accept the actual im2recipe 35K nutritional dataset. When the Recipe1M data access form is submitted and the JSON is placed at `data/im2recipe_recipes.json`, running `python3 build_nutrition.py --import-im2recipe` generates the per-recipe index. The app auto-detects the new data on next reload.

## 4. Professional Workflows & Strategies

This section is written for the professional kitchen. Each workflow is a complete, end-to-end strategy that combines multiple app features to solve a real culinary problem.

---
### 4.1 Menu Engineering — From Concept to Plated Dish

**The goal:** Take a rough idea and develop it into a menu-ready dish with pairings, substitutions, and flavour profile documentation.

**Full workflow (10 minutes):**

1. **Ideate:** Type your rough idea into the **Describe a Dish** input (e.g. "smoky mushroom risotto with truffle"). See what canonical ingredients the embedding suggests — often including forgotten essentials.
2. **Anchor:** Click the most interesting suggestion to select it as your anchor ingredient.
3. **Profile:** Open the **Chef's Toolkit Pro** → check the flavour profile tags and molecular notes. If you're building a dish around mushrooms, what molecular families dominate? (Amino Acid, Maillard, Lipid — brothy, roast, and fat-friendly)
4. **Substitute:** Use the **substitution mode toggle** in Chef's Toolkit to compare recipe-context vs flavour-chemistry substitutes. If truffle is too expensive, chemistry-mode will show porcini powder and mushroom soy as molecular peers.
5. **Pair:** Check the **Neighbours** tab for classic pairings. Then switch to **Direction (SLERP)** to rotate the anchor toward different cuisines — a mushroom risotto rotated toward East Asian at 30° reveals soy sauce, sesame, and ginger as subtle inflections.
6. **Fusion:** If you want a cross-cultural angle, open **Cuisine Fusion Explorer** in the Games tab and find bridge ingredients between Mediterranean and your target cuisine.
7. **Verify:** Check the **Map** tab to see how your anchor ingredient sits in the embedding landscape relative to its neighbours.
8. **Document:** The flavour profile tags and molecular notes from Chef's Toolkit form ready-made menu copy: "A mushroom risotto with Amino Acid depth and Maillard richness, anchored by a Lactone-creamy finish."

---
### 4.2 Cost-Effective Substitution Strategy

**The goal:** Replace expensive or unavailable ingredients without compromising the dish's flavour integrity — the single highest-ROI skill a chef can develop.

**The insight:** Substitutions work differently depending on *why* an ingredient is in a dish. An embedding space captures both chemistry and recipe context, and the **substitution mode toggle** in Chef's Toolkit Pro lets you choose the right lens.

| Context | Use Model | Example |
|---|---|---|
| **Flavour-first** (the ingredient's taste is the point) | Chemistry mode | Substituting truffle oil: chemistry mode shows porcini oil, mushroom soy, nutritional yeast — flavour-profile peers |
| **Structure-first** (the ingredient's physical function matters) | Recipe mode | Substituting eggs in baking: recipe mode shows banana, applesauce, flaxseed — co-occurrence peers that serve the same structural role |
| **Both** | Compare both modes | The intersection of chemistry and recipe modes gives the safest substitution — ingredients that *taste* similar *and* are used similarly |

**Workflow for cost-effective substitutions:**
1. Select the expensive ingredient (e.g. saffron, truffle, lobster, foie gras, uni)
2. Open **Chef's Toolkit Pro** — the cost hint at the bottom gives a direct budget alternative
3. Toggle between **Recipe** and **Chemistry** substitution modes
4. Look for substitutes that appear in *both* lists — these are the safest swaps
5. Check the **Chef's Cost Hint** section for seasonal and waste-reduction tips

**Example: Saffron substitution**
- Cost hint: 💎 Luxury item — turmeric + paprika mimics colour; avoid if budget-sensitive
- Chemistry substitutes: turmeric (52%), annatto (45%), safflower (41%), paprika (38%)
- Recipe substitutes: turmeric (48%), paprika (42%), cayenne (38%), cumin (35%)
- **Best swap:** turmeric + paprika — appears in both chemistry and recipe lists, covers colour + warmth

---
### 4.3 Cross-Cultural Fusion Menu Design

**The goal:** Design a tasting menu that genuinely bridges two cuisines — not by juxtaposing them, but by finding the ingredients, techniques, and flavour principles they share.

**The insight:** Most fusion cooking fails because it forces incompatible flavour vocabularies together. The embedding space reveals which ingredients are *naturally bilingual* — they have high similarity to both cuisines' direction vectors.

**Workflow (15 minutes):**

1. **Choose your pair:** Pick two cuisines that interest you. Start with a pair that has *some* historical connection (Japanese × Latin American, Mediterranean × Middle Eastern) for higher-likelihood bridges.
2. **Find bridges:** Open the **Cuisine Fusion Explorer** in the Games tab. Select your two cuisines. Look at the top 24 bridge ingredients.
3. **Analyse the bridges:** Click the highest-ranked bridge ingredient to select it. Open **Chef's Toolkit Pro** and check its flavour profile. Does it lean more toward one cuisine than the other? An ingredient with 50%/50% balance is a genuine bridge — use it as a menu anchor.
4. **Build around bridges:** The bridge ingredients become your menu's conceptual anchors. For example, if soy sauce bridges Japanese and Latin American at 75%/65%, build a dish around soy-based umami that works in both contexts.
5. **Rotate for nuance:** Select a bridge ingredient → **Direction (SLERP)** → rotate it toward one cuisine to see how that ingredient "translates" into that culinary context.
6. **Check the compass:** Use **Flavour Compass** in the Games tab to visualise the bridge ingredient's sensory profile — this helps you design dishes that honour both cuisines' flavour principles.

**Example: Japanese × Mediterranean fusion menu:**

| Bridge ingredient | Japanese sim | Mediterranean sim | Menu idea |
|---|---|---|---|
| sesame_oil | 74% | 61% | Sesame-grilled octopus with olive oil and shiso |
| garlic | 52% | 78% | Roasted garlic miso aioli |
| scallion | 65% | 58% | Scallion and feta salad with yuzu vinaigrette |
| soy_sauce | 82% | 55% | Soy-marinated tomato caprese with basil |
| ginger | 58% | 45% | Ginger and oregano roasted chicken |

- **Menu concept:** "The Silk Route" — a 5-course tasting menu where each dish features a different bridge ingredient
- **Why it works:** Every dish is anchored by an ingredient that genuinely belongs to both culinary traditions — it's fusion from the ingredient level up, not from the concept level down

---
### 4.4 Seasonal Menu Adaptation

**The goal:** Adapt your menu to seasonal ingredient availability without redesigning every dish from scratch.

**The insight:** When a key ingredient goes out of season, you need a substitute that preserves the dish's flavour structure — not just the ingredient's taste in isolation.

**Workflow:**
1. Select the out-of-season ingredient
2. Open **Chef's Toolkit Pro** → check the **cost hint** for seasonal peak information
3. Switch to **Chemistry mode** in the substitution toggle to find flavour-profile peers
4. The Chef's Toolkit cost hint section automatically shows seasonal peak info for common ingredients:
   - 🍂 Autumn: pumpkin, squash, apple, fig, mushroom — best roasted with warming spices
   - 🌱 Spring: asparagus, pea, artichoke, fava, ramp, morel — treat gently
   - ☀️ Summer: tomato, zucchini, peach, berry, eggplant, corn, melon — minimal cooking
   - ❄️ Winter: kale, brussels, cauliflower, pomegranate, persimmon — braise or slow-cook
5. Verify the substitute's flavour profile matches the original using **Flavour Compass**
6. Check cross-model consistency: the Direction tab can show how the substitute "performs" when rotated toward the original ingredient's dominant cuisine

---
### 4.5 Dietary Adaptation at Scale

**The goal:** Adapt existing menu items for dietary restrictions (vegan, gluten-free, nut-free) while preserving the eating experience.

**The insight:** Dietary substitution is a two-axis problem: the substitute must *taste* right (chemistry) and *function* right (recipe context). The Chef's Toolkit's dietary tags provide the constraint, while the substitution mode toggle provides the solution.

**Workflow:**
1. Select the problematic ingredient (e.g. butter, eggs, cheese)
2. **Chef's Toolkit Pro** shows dietary tags — if an ingredient is tagged ❌ "No" for a restriction, it needs substitution
3. Switch to **Chemistry mode** to find flavour-profile peers that taste similar
4. Switch to **Recipe mode** to find co-occurrence peers that serve the same structural role
5. The **intersection** of both lists is the ideal substitute

**Example: Dairy-free `butter` substitution**
- Chemistry mode: ghee (82%), coconut_oil (65%), olive_oil (58%), avocado (52%)
- Recipe mode: olive_oil (70%), ghee (68%), coconut_oil (60%), margarine (55%)
- ⭐ **Best swap:** ghee (if tolerated) or coconut oil — appears high in both lists

---
### 4.6 Flavour Boostering — Elevating Existing Dishes

**The goal:** Take a working dish and add a new dimension — a flavour booster that elevates without overwhelming.

**The insight:** The SLERP (Direction Arithmetic) feature lets you rotate an ingredient toward a flavour direction, revealing which other ingredients "add" that dimension.

**Workflow:**
1. Select your dish's primary ingredient
2. Go to **Direction (SLERP)** tab
3. Choose a sensory direction you want to boost (e.g. Spicy for heat, Herbal for freshness, Citrus/Sour for brightness)
4. Start at 15° (gentle inflection) and increase to see how the neighbour list changes
5. At each angle, note which new ingredients appear — these are the ones that "bring" that flavour dimension
6. Check those ingredients in **Chef's Toolkit Pro** to verify their overall profile

**Example: Boost `chocolate` with spice**
- Direction: Spicy at 30° → chili, cayenne, ancho, cinnamon, nutmeg appear
- Direction: Spicy at 45° → black pepper, ginger, allspice, cardamom
- Direction: Spicy at 60° → cumin, coriander, turmeric, mustard
- The 30° list gives *subtle* heat enhancers; 60° list gives *structural* flavour changers — use accordingly

---
### 4.7 Embedding Literacy — Training Your Team

**The goal:** Help your kitchen team develop intuition for how the embedding space works so they can use it effectively.

**The insight:** The mini-games are not just entertainment — they're training tools that build "embedding literacy."

**Training session (30 minutes):**
1. **Guess the Neighbour (10 min):** Everyone plays 10 rounds. Discuss: was the correct neighbour obvious or surprising? This builds intuition for what "similarity" means in the embedding space
2. **Cuisine Fusion Explorer (10 min):** The team picks two cuisines and discusses the bridge ingredients. Which bridges are obvious (soy sauce in East Asian cuisine)? Which are surprising (sesame oil bridging Mediterranean and Asian)?
3. **Flavour Compass (10 min):** Each person picks a different ingredient and presents its radar chart. Compare: how does `salt`'s compass differ from `sugar`'s? From `soy_sauce`'s? This builds intuition for multi-dimensional flavour profiles

---
### 4.8 The Research Behind the App — Why This Works

This app is built on peer-reviewed research and production-grade food AI platforms:

| Source | What It Contributes | Why It Matters for Chefs |
|---|---|---|
| **Epicure (arXiv:2605.22391, 2026)** | Three sibling embedding models (Cooc/Core/Chem) trained on 4.14M recipes across 7 languages | Most production-ready ingredient embedding system as of 2026 — multilingual, chemistry-aware, with an interactive UI |
| **Foodpairing.ai** | Enterprise molecular gastronomy knowledge graph founded by a Michelin-starred chef | The Chem model mirrors their approach — ingredient relationships grounded in molecular compound data |
| **Tastewise.io** | Agentic AI platform tracking 1T+ food signals with 96% F&B-specific accuracy | Trend-informed menu design — the same intelligence used by Nestlé, PepsiCo, and Givaudan |
| **FlavorDB (IIIT-Delhi)** | 25,595 flavour molecules across 936 natural ingredients | The chemical ground truth layer — Epicure's Chem model was built on FlavorDB compound data |
| **FoodBERT / Food2Vec** | Ingredient substitution via skip-gram and BERT embeddings | Academic validation that embedding-based substitution outperforms heuristic approaches |
| **Swiss Food Knowledge Graph (arXiv:2507.10156, 2025)** | Unified graph of recipes, ingredients, substitutions, nutrients, and dietary guidelines | Graph-RAG pattern for answering complex queries like "What's a nut-free, high-protein breakfast?" |

The app brings all of this together in a single HTML file — no API keys, no cloud dependencies, no subscription.

---
### 4.9 Future Directions — What's Next

The embedding space opens the door to features that are **architecturally possible** but not yet implemented in this version:

- **Ingredient Direction Arithmetic:** "Add the flavour of truffle to a mushroom risotto without truffle" — vector arithmetic (risotto_vector + (truffle_vector - mushroom_vector))
- **Photo-to-Nutrition:** Photograph a plated dish → ingredient mass estimation → nutritional breakdown (like NutriFusionNet's GAIE architecture)
- **Real-Time Trend Integration:** Pull trending ingredient signals from Tastewise/industry APIs to inform menu specials
- **Graph-RAG Chef Assistant:** Natural-language query over the full embedding space — "What replaces eggs in a gluten-free brunch?"
- **MCP-Native Architecture:** Expose the embedding space as an MCP server so any AI assistant can query your food intelligence layer

> **Already shipped:** GLP-1 Diet Mode (💊 badge + 💚 filter toggle), Explainable Substitutions (💡 "Why This Substitute?" panel), Nutrition Deep-Dive (🔬 per-ingredient FSA traffic lights), FSA Health Direction (💚 healthy↔indulgent SLERP vector), Per-Recipe Nutrition (🥗 51K recipe FSA scores in Recipe tab), Nutrition Heatmap Overlay (🔥 colour-coded UMAP), Flavour Arithmetic Explorer (🧮 visual chip UI with history), Cocktail Mixology (🍸 spirit + mixer → drink intelligence), Seasonal Calendar (🗓️ peak-season browser + map overlay), Spoonacular API (🌐 live recipe search, nutrition, wine pairing), Snap→Ingredient Search (📸 food photo → classify → explore), Ingredient2Vec API (🔬 nearest-neighbour + arithmetic), Food Agent (🤖 natural language → ingredient match), Trending panel (📈 seasonal + rarity + GLP-1 signals), and GLP-1 Meal Plan Generator (💊 7-day plan from embedding clusters) — see §3.4, §3.8, §3.10–§3.20 for details.
>
> **Bug fix:** Force-Directed graph projection now works — `getForceGraphLayout()` implements a Fruchterman-Reingold spring-force layout from top-15 neighbour edges. See §3.4 and §5.1.

---

## 5. Troubleshooting

### 5.1 "Cannot fetch data/epicure_shared.json" / CORS error

**Problem:** You opened `index.html` directly via `file://` protocol.

**Fix:** Serve the files via HTTP:
```bash
cd epicure-explorer && python3 -m http.server 8080
```
Then visit `http://localhost:8080`.

> **🎓 New to the app?** A 5-step guided tour appears on your first visit (1.5s after load) — walk through Search, Chef's Toolkit, Tab navigation, Map, and Describe a Dish. You can skip it anytime.

### 5.2 Loading screen never finishes

**Possible causes:**
- The data files (`epicure_shared.json`, `epicure_cooc.json`, etc.) are missing or corrupted
- The browser is blocking large downloads

**Fix:**
- Verify the files exist: `ls -la data/epicure_shared.json data/epicure_cooc.json`
- Regenerate them: `python3 preprocess.py` (using the `.venv` with umap-learn installed)
- Check browser console (F12 → Console) for specific error messages

### 5.3 Python script fails with error

**Common issues:**
- Missing `data/` directory: the script expects CSV files in `data/`
- Missing CSV files: ensure all three `epicure_cooc.csv`, `epicure_core.csv`, `epicure_chem.csv` are present, plus `mode_atlas_*.csv` files
- Missing `umap-learn` dependency: the script requires it for UMAP projection. Install it in a virtual environment:
  ```bash
  python3 -m venv .venv
  .venv/bin/pip install umap-learn
  .venv/bin/python3 preprocess.py
  ```
  The script falls back to PCA if UMAP is not available.

**Minimum required files for `preprocess.py`:**
- `data/epicure_cooc.csv` (4.9 MB)
- `data/epicure_core.csv` (4.9 MB)
- `data/epicure_chem.csv` (4.9 MB)
- `data/mode_atlas_cooc.csv`
- `data/mode_atlas_core.csv`
- `data/mode_atlas_chem.csv`

> ⚠️ The raw embeddings are the **raw skip-gram outputs** (not L2-normalised) — `preprocess.py` handles normalisation. See `data/README.txt` for the full notes from the original authors, including a quick-load snippet for pandas and cross-referencing `vocab.csv`.

### 5.4 Missing mode atlases

**Symptom:** Modes tab shows "Mode atlas not available for this model"

**Cause:** The mode atlas CSV files (`mode_atlas_*.csv`) aren't in the `data/` directory, or `preprocess.py` didn't find them when the JSON was generated.

**Fix:** Place the CSV files in `data/` and re-run `python3 preprocess.py`.

### 5.5 The PCA canvas looks wrong

**Possible causes:**
- Browser zoom level: reset to 100%
- Window resize: the canvas should auto-resize; if not, reload the page
- Very narrow window: the canvas has a minimum width; use a wider viewport

### 5.6 The SLERP slider doesn't seem to do anything

**Check:**
- Is the direction dropdown set to a valid option? (Sweet, Spicy, etc.)
- Are there enough matching ingredients for the direction vector? Each direction needs ≥3 matching ingredients from the vocabulary to compute a centroid.
- At small angles (0–10°) the change is subtle; drag to 45°+ to see clear differences.

### 5.1 Force-Directed Map — Fixed

**Problem:** Previously, selecting "Force-Directed" from the Map projection dropdown threw `ReferenceError: getForceGraphLayout is not defined`. UMAP and PCA methods worked normally.

**Fix (Session 5, June 2026):** `getForceGraphLayout()` was implemented as a Fruchterman-Reingold spring-force layout. It builds undirected edges from the top-15 nearest neighbours per ingredient (weighted by similarity), initialises node positions from UMAP coordinates for fast convergence, and runs 35 iterations with exponential temperature cooling (0.88 × per iteration). Sub-sampled repulsion (~1/4 of nodes per iteration) keeps performance reasonable for 1,790-node graphs.

**If Force-Directed still seems slow:** The sub-sampled repulsion trades some accuracy for speed. UMAP or PCA projection are faster alternatives when exploring.

### 5.2 Browser performance

The 12 MB data bundle is loaded once. After that:
- Neighbours, Compare, Modes are instant (precomputed lookups)
- SLERP is fast (one dot product per ingredient — 1,790 operations)
- PCA Map re-renders on resize (debounced to 200ms)

If the map is sluggish on low-end devices, the point rendering (1,790 arc() calls) was historically the bottleneck. **Session 9** added viewport-frustum culling — only points visible within the canvas area (+10px margin) are rendered, making zoomed-in navigation smooth.

### 5.9 PWA & Offline Support

Epicure Explorer supports "Add to Home Screen" on mobile via an inline data URI manifest. After the first visit, the Service Worker (`sw.js`) caches:
- `index.html` (the app shell) — cached on install
- `epicure_shared.json` (128 KB, ingredient list + direction vectors) — cached on install
- Per-model JSON bundles (~4 MB each) — cached on first fetch via stale-while-revalidate

**Result:** Returning users can browse the app without network access. The shared data and last-used model are available offline.

### 5.10 Dark Mode

Click the 🌙/☀️ button in the header to toggle between dark and light themes. The preference is saved to `localStorage('epicure_theme')` and restored on subsequent visits. The `.light` CSS class swaps all 15 color variables (background, surface, text, accents, semantic colors).

### 5.11 Unified Smart Search Bar

The ingredient search and "Describe a Dish" inputs have been merged into a single smart search bar at the top of the page. The system auto-detects:

- **Single-word query** → ingredient autocomplete (fuzzy match, same as before)
- **Multi-word query with spaces** → describe-dish parsing (350ms debounce), matching ingredient names and fuzzy synonyms

Examples:
- `miso` → shows ingredient dropdown
- `creamy garlic pasta with mushrooms` → parses into tags: garlic, mushroom, cream → click any tag to explore

### 5.12 Cross-Model Consensus in Substitutions

When viewing substitutes in the Chef's Toolkit, each substitution now shows a **cross-model consensus badge** — color-coded glyphs indicating agreement across all three embedding models:

- ◆ (purple diamond) = Core blended model
- ◇ (blue diamond) = Cooc recipe model  
- ◈ (green diamond) = Chem chemistry model

Each glyph is colored: green (≥0.6), yellow (≥0.4), or red (<0.4). Click 💡 to see the full per-model breakdown.

### 5.13 Molecular Fingerprint Card

The Chef's Toolkit Flavour Profile section now includes a **Molecular Fingerprint** card showing the top 5 active compound categories for the selected ingredient. Each compound is displayed as:

- A **compound pill** with description on hover
- An **intensity bar** (green > 60%, yellow > 35%, purple default) estimated from the ingredient's sensory direction scores

Example: Miso shows `🧬 Amino Acid ████████ 80%` indicating strong umami/fermented compound presence.

### 5.14 Seasonal Heatmap

The Seasonal Calendar tab now includes a **month-by-month heatmap view**. Click the "📊 Heatmap" button to toggle between the traditional season view and a full grid showing:

- **12 columns** (January–December)
- **~150 ingredients** grouped by category (Produce, Meat & Seafood, Spices & Herbs, Dairy, Grains)
- **Color intensity** = peak availability in that month
- **Clickable ingredient names** — click any name to select it in the embedding space

The current month is highlighted in the table header.

### 5.15 Spoonacular Graceful Degradation

When no Spoonacular API key is saved, the Spoonacular tab now shows a friendly **onboarding banner** instead of empty features. The banner lists what functionality is available (recipe search, nutrition, wine pairing, image recognition) and links to spoonacular.com to get a free key. Once a key is saved, the banner hides and the feature panels appear.

### 5.16 Map Gesture Hint (Mobile)

On touch devices, the first visit to the Map tab shows a subtle overlay: "Drag to pan · Pinch to zoom · Double-tap to reset". It fades out after 4 seconds and never appears again (tracked via `localStorage`).

### 5.17 Density Threshold Slider

When the **🔬 Density** overlay is selected on the Map tab, a **Min%** slider appears next to the overlay dropdown. It controls the minimum intensity threshold for KDE heatmap cells:

- **0%** — all cells rendered (noisiest, shows background density everywhere)
- **2%** (default) — hides sparse cells, shows only meaningful clusters
- **10%** — only the densest hotspots remain visible

The slider range is 0–10% in 0.5% steps. Use it to declutter the density heatmap when zoomed in, or to see subtle clustering patterns at low thresholds.

### 5.18 QR Code Share

The Chef's Toolkit sidebar includes a **"📱 Show QR Code"** button. Click it to open a modal overlay with a scannable QR code encoding the current deep-link URL (`#tab=...&model=...&ingredient=...`). This lets you:

- Share the current view with colleagues by scanning from another device
- Save the QR code as a PNG via screenshot
- Close the modal by clicking the backdrop or the Close button

The QR generation is fully inline — no external dependencies, no network calls, works offline.

### 5.19 ℹ️ Ingredient Name Translation

The app's i18n system has been extended from UI strings to **ingredient names** themselves. When a non-English language is selected (🇪🇸 ES, 🇫🇷 FR, 🇨🇳 中文, 🇯🇵 日本語), ~120 commonly viewed ingredients display in the local language throughout the app:

- **Selected ingredient label** — shows the translated name
- **Chef's Toolkit title** — translated ingredient name at the top of the sidebar
- **Map tooltip** — translated name on hover over map points
- **Neighbour substitution list** — translated ingredient names
- **Flavour Compass target** — translated name

Fallback: If an ingredient has no translation in the current language, its English underscored name is displayed with underscores converted to spaces.

### 5.20 Nutrition Data Not Loading

**Symptom:** Chef's Toolkit shows no "🔬 Nutrition per 100g" section, or the Recipe tab's "🥗 Nutrition" subtab shows "Nutrition data loading…"

**Possible causes:**
- `data/epicure_nutrition.json` is missing or wasn't fetched (check browser console for 404)
- For per-recipe data, `data/recipe_nutrition.json` and `data/recipe_detections_slim.json` must be present

**Fix:**
- Verify files exist: `ls -la data/epicure_nutrition.json data/recipe_nutrition.json data/recipe_detections_slim.json`
- Regenerate per-ingredient data: `python3 build_nutrition.py`
- Process per-recipe data (requires im2recipe 35K dataset): `python3 build_nutrition.py --import-im2recipe`
- The `loadNutritionData()` call is fire-and-forget — if the file isn't available, the app falls back to inline `NUTRITION_DATA` (165 ingredients)

### 5.21 FSA Health Direction Not in SLERP Dropdown

**Symptom:** The "💚 FSA Health" option doesn't appear in the Direction (SLERP) tab.

**Fix:** The health direction is computed on-the-fly when both `epicure_nutrition.json` and model vectors are loaded. If you're seeing it, open the SLERP tab and select any seed ingredient — the direction should appear. It requires at least 5 healthy ingredients (3+ green lights) and 5 indulgent ingredients (2+ red lights) in the nutrition data to create a stable centroid vector.
