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

---

## Features — 18 Tabs (4 Categories)

Navigate tabs via the category bar: 🧠 **Core** | 🎮 **Play** | 🔬 **Analyze** | 🚀 **Advanced**

| Category | Tabs |
|----------|------|
| **🧠 Core** | Neighbours, Compare, Direction (SLERP), Map, Modes, Recipes |
| **🎮 Play** | Games, Arith (Flavour Arithmetic), Cocktails |
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
| **🎮 Games** | "Guess the Neighbour" quiz + "Flavour Compass" radar chart |
| **🍽️ Analyzer** | Comma-separated ingredient list → dietary + flavour + category analysis |
| **⚔️ Compare 2** | Side-by-side ingredient comparison |
| **🧮 Arith** | Visual chip-based flavour arithmetic builder with history |
| **🍸 Cocktails** | Spirit + mixer → cocktail suggestions from embedding centroid |
| **🗓️ Seasonal** | 149-ingredient peak-season browser + map overlay |

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
| **🌐 Spoonacular** | Live recipe search, nutrition lookup, wine pairing (requires free API key) |

### Professional Toolbar
| Feature | What It Does |
|---------|-------------|
| **👨‍🍳 Chef's Toolkit Pro** | Dietary profile, substitutes with "Why This Substitute?" explanations, cuisine affinity, molecular notes, GLP-1 filter, cost/waste/seasonal hints |
| **🔍 Map Search** | Find any ingredient on the 2D map — auto-centers, zooms, and pulses |

### UI/UX Highlights
- **Tab categorization** — 18 tabs grouped into 4 categories with filtering bar
- **Responsive design** — works on desktop, tablet, and mobile
- **Deep-link URLs** — shareable `#tab=map&model=chem&ingredient=miso` links
- **Keyboard & screen-reader** — ARIA roles, arrow key navigation
- **Skeleton loading** — shimmer placeholder layout during data fetch
- **Empty states** — contextual guidance when no ingredient is selected

---

## Architecture

```
epicure-explorer/
├── index.html          ← THE APP — single self-contained HTML file (259 KB)
├── preprocess.py       ← Python pipeline to generate data bundles from raw CSVs
├── requirements.txt    ← Pinned dependencies (umap-learn, scikit-learn)
├── data/
│   ├── epicure_shared.json   ← Shared data (128 KB) — ingredients + direction vectors
│   ├── epicure_cooc.json     ← Cooc model (~4 MB) — neighbours + UMAP + vectors
│   ├── epicure_core.json     ← Core model (~4 MB)
│   ├── epicure_chem.json     ← Chem model (~4 MB)
│   ├── *.csv                 ← Raw arXiv embeddings + mode atlases
│   └── README.txt            ← Original authors' notes
├── GUIDE.md            ← Professional chef's playbook (full user guide)
├── FOOD_AI_RESEARCH_PLAN.md ← Strategic product roadmap & competitive analysis
├── SESSION_JOURNAL.md  ← Development session log
└── ANALYSIS.md         ← Paper analysis & summary
```

- **Zero dependencies** — no build step, no package manager, no server required
- **Lazy-loaded models** — initial load is 128 KB, model data (~4 MB each) loads on-demand
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

This project was built across 8 development sessions (June–July 2026). See [`SESSION_JOURNAL.md`](SESSION_JOURNAL.md) for the full log.

### Quick Stats
- **5,430 lines** of HTML/CSS/JS in a single file
- **~112 JavaScript functions** across 18 tabs and Chef's Toolkit
- **~4,100 lines** of JavaScript application logic
- **24 files** tracked in version control

---

## License

## License

- **Code:** [MIT](LICENSE) — Epicure Explorer contributors
- **Embeddings:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Radzikowski & Chen (2026), [arXiv:2605.22391](https://arxiv.org/abs/2605.22391)
- **Nutrition data:** [USDA FoodData Central](https://fdc.nal.usda.gov/) (public domain)
- **Spoonacular API:** Subject to [Spoonacular terms of service](https://spoonacular.com/food-api) — requires a free API key
