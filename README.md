# Epicure Explorer 🍽️

**Navigate the flavour universe.** A zero-dependency, single-file web app for interactively exploring 1,790 canonical food ingredients across three embedding models, built on the [Epicure paper](https://arxiv.org/abs/2605.22391) (arXiv:2605.22391).

[![GitHub](https://img.shields.io/badge/GitHub-epicure--explorer-8b5cf6?style=flat&logo=github)](https://github.com/aliatx2017/epicure-explorer)
[![arXiv](https://img.shields.io/badge/arXiv-2605.22391-b31b1b?style=flat&logo=arxiv)](https://arxiv.org/abs/2605.22391)

---

## What It Is

Epicure Explorer is not a recipe database. It's a **flavour relationship engine** — the same class of technology behind molecular gastronomy platforms like Foodpairing.ai, but in a **zero-dependency, single HTML file** you can run on a laptop in a kitchen.

Three sibling embedding models — **Cooc** (recipe co-occurrence), **Chem** (molecular flavour profiles), and **Core** (blended) — trained on 4.14M recipes across 7 languages, mapping every ingredient into a 300-dimensional semantic space.

---

## Quick Start

```bash
git clone https://github.com/aliatx2017/epicure-explorer.git
cd epicure-explorer
python3 -m http.server 8080
```

Then open **http://localhost:8080** in any modern browser. No build step, no npm install, no API keys needed.

> **Note:** For Spoonacular API features (recipe search, image classification, nutrition, wine pairing), get a free API key at [spoonacular.com](https://spoonacular.com/food-api) and enter it in the 🌐 Spoonacular tab.  
> **No key?** Recipe search falls back to [TheMealDB](https://www.themealdb.com/) (free, no key needed).

---

## Features — 19 Tabs (4 Categories)

Navigate tabs via the category bar: 🧠 **Core** | 🎮 **Play** | 🔬 **Analyze** | 🚀 **Advanced**

| Category | Tabs |
|----------|------|
| **🧠 Core** | Neighbours, Compare, Direction (SLERP), Map, Modes, Recipes |
| **🎮 Play** | Games, **Build Dish**, Arith (Flavour Arithmetic), Cocktails |
| **🔬 Analyze** | Analyzer, Compare 2, Snap, Seasonal |
| **🚀 Advanced** | Spoonacular, Ingredient2Vec, Food Agent, Trending, Meal Plan |

### Tab Detail

### Core Ingredient Intelligence
| Tab | What It Does |
|-----|-------------|
| **🔗 Neighbours** | Top-25 nearest ingredients ranked by cosine similarity |
| **⚖️ Compare** | Side-by-side neighbour lists across all 3 models |
| **🎯 Direction (SLERP)** | Rotate an ingredient toward a sensory/cuisine direction |
| **🗺️ Map** | 2D projection (UMAP/PCA/Force-Directed) with zoom/pan/search, cuisine region labels, nutrition heatmap overlay |
| **🏷️ Modes** | GMM culinary mode memberships with cuisine-group filters |
| **🍲 Recipes** | Cuisine browser, bridge finder, flavour boosters |

### Creative & Analytical Tools
| Tab | What It Does |
|-----|-------------|
| **🎮 Games** | Two modes: "Guess the Neighbour" + "Cuisine ID" with localStorage leaderboard, plus "Flavour Compass" radar chart |
| **👨‍🍳 Build Dish** | Multi-ingredient chip selector → centroid pairings + flavour profile compass + dietary flags |
| **🍽️ Analyzer** | Comma-separated ingredient list → dietary + flavour + category analysis |
| **⚔️ Compare 2** | Side-by-side ingredient comparison |
| **🧮 Arith** | Visual chip-based flavour arithmetic builder with history |
| **🍸 Cocktails** | Spirit + mixer → cocktail suggestions from embedding centroid |
| **🗓️ Seasonal** | 149-ingredient peak-season browser + heatmap grid |

### Month 3 — Differentiators
| Tab | What It Does |
|-----|-------------|
| **📸 Snap** | Upload food photo → Spoonacular identifies dish → explore ingredients in embedding space |
| **🔬 Ingredient2Vec** | Direct nearest-neighbour query + flavour arithmetic API |
| **🤖 Food Agent** | Describe a craving in natural language → embedding-matched ingredient suggestions |
| **📈 Trending** | Seasonal + rarity + GLP-1 trend signals scored across all ingredients |
| **💊 Meal Plan** | 7-day GLP-1-optimized meal plan from embedding clusters with calorie targeting |

### External Integrations
| Tab | What It Does |
|-----|-------------|
| **🌐 Spoonacular** | Live recipe search (with <a href="https://www.themealdb.com/">TheMealDB</a> free fallback), nutrition lookup, wine pairing (requires free API key) |
| **🌿 TheCocktailDB** | Real cocktail recipes alongside embedding-based suggestions in the Cocktail tab (free, no key needed) |

### Professional Toolbar
| Feature | What It Does |
|---------|-------------|
| **👨‍🍳 Chef's Toolkit Pro** | Dietary profile, substitutes with "Why This Substitute?" explanations, cuisine affinity, molecular notes, GLP-1 filter, cost/waste/seasonal hints |
| **🔍 Map Search** | Find any ingredient on the 2D map — auto-centers, zooms, and pulses |
| **🧬 Molecular Fingerprint** | Compound intensity bars showing active flavour compound categories |
| **🔬 Cross-Model Consensus** | Substitute scores compared across all 3 embedding models |
| **🌙 Dark Mode** | Toggle between dark and light themes, persisted across sessions |
| **📱 QR Code Share** | Generate a scannable QR code for the current deep-link view |

### Infrastructure
| Feature | What It Does |
|---------|-------------|
| **📱 PWA Manifest** | "Add to Home Screen" on mobile with inline data URI manifest |
| **📴 Service Worker** | Offline caching of app shell and model data JSONs |
| **⚡ Viewport Culling** | Only renders visible map points during pan/zoom |
| **⚡ RAF Coalescing** | Batch-coalesced map renders for smooth pan/zoom interactions |

### UI/UX Highlights
- **Tab categorization** — 19 tabs grouped into 4 categories with filtering bar
- **Responsive design** — works on desktop, tablet, and mobile
- **Deep-link URLs** — shareable `#tab=map&model=chem&ingredient=miso` links
- **Keyboard & screen-reader** — ARIA roles, arrow key navigation
- **Skeleton loading** — shimmer placeholder layout during data fetch
- **Empty states** — contextual guidance when no ingredient is selected
- **🌐 i18n** — UI in 5 languages (EN/ES/FR/中文/日本語) with ingredient name translations for ~120 common ingredients

---

## Architecture

```
epicure-explorer/
├── index.html          ← THE APP — single self-contained HTML file (435 KB)
├── build_nutrition.py   ← Nutrition pipeline — generates epicure_nutrition.json in im2recipe format
├── requirements.txt    ← Pinned dependencies (umap-learn, scikit-learn)
├── icon-192.png        ← PWA home-screen icon (2.3 KB)
├── icon-512.png        ← PWA splash-screen icon (6.8 KB)
├── data/
│   ├── epicure_shared.json   ← Shared data (146 KB) — ingredients + direction vectors + seasonal + nutrition
│   ├── epicure_cooc.json     ← Cooc model (~4 MB) — neighbours + UMAP + vectors
│   ├── epicure_core.json     ← Core model (~4 MB)
│   ├── epicure_chem.json     ← Chem model (~4 MB)
│   ├── epicure_nutrition.json ← Per-ingredient FSA nutrition (789 KB) — im2recipe format
│   ├── nutrition_vocab.json  ← im2recipe↔Epicure name mapping (114 KB)
│   ├── recipe_nutrition.json ← 51K per-recipe FSA nutrition (98 MB) — im2recipe 35K dataset
│   ├── recipe_detections_slim.json ← 622-ingredient→recipe link index (2.1 MB)
│   ├── recipe_ingredient_map.json ← Full USDA-ingredient→recipe map (5.7 MB)
│   ├── *.csv                 ← Raw arXiv embeddings + mode atlases
│   └── README.txt            ← Original authors' notes
├── GUIDE.md            ← Professional chef's playbook (full user guide)
├── FOOD_AI_RESEARCH_PLAN.md ← Strategic product roadmap & competitive analysis
├── SESSION_JOURNAL.md  ← Development session log
└── ANALYSIS.md         ← Paper analysis & summary
```

- **Zero dependencies** — no build step, no package manager, no server required
- **Lazy-loaded models** — initial load is 146 KB, model data (~4 MB each) loads on-demand
- **All client-side** — runs entirely in the browser, no backend

---

## The Three Models

| Model | Training Signal | Best For |
|-------|----------------|----------|
| **Cooc** | Ingredient co-occurrence in recipes | Finding recipe companions — what's commonly used together |
| **Chem** | Molecular compound sharing (FlavorDB) | Finding flavour-profile peers — ingredients that taste similar |
| **Core** | Blended (cooc + chem with recipe bias) | Balanced results combining both signals |

---

## Data Source

The embeddings come from the [Epicure paper](https://arxiv.org/abs/2605.22391) (*Navigating the Emergent Geometry of Food Ingredient Embeddings*, arXiv:2605.22391, May 2026) by Jakub Radzikowski & Josef Chen. The supplementary bundle provides raw skip-gram embeddings for all three models. This project preprocesses them (L2 normalisation, k-NN computation, UMAP projection) into a browser-friendly format.

---

## Development

This project was built across 15 development sessions (June–July 2026). See [`SESSION_JOURNAL.md`](SESSION_JOURNAL.md) for the full log.

### Quick Stats
- **~8,293 lines** of HTML/CSS/JS in a single file
- **~202 JavaScript functions** across 19 tabs and Chef's Toolkit
- **~6,814 lines** of JavaScript application logic
- **31 files** tracked in version control
- **80 automated E2E tests** — all passing
- **51K per-recipe nutrition records** — FSA-scored from the im2recipe 35K dataset
- **im2recipe-format data pipeline** — USDA-matched nutrition for all 1,790 ingredients
- **PWA icons**: 192×192 + 512×512 PNG (purple plate/fork)

---

## License

## License

- **Code:** [MIT](LICENSE) — Epicure Explorer contributors
- **Embeddings:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Radzikowski & Chen (2026), [arXiv:2605.22391](https://arxiv.org/abs/2605.22391)
- **Nutrition data:** [USDA FoodData Central](https://fdc.nal.usda.gov/) (public domain)
- **Spoonacular API:** Subject to [Spoonacular terms of service](https://spoonacular.com/food-api) — requires a free API key
- **TheMealDB API:** Free recipe data from [TheMealDB](https://www.themealdb.com/) — no key needed for development
- **TheCocktailDB API:** Free cocktail data from [TheCocktailDB](https://www.thecocktaildb.com/) — no key needed for development
