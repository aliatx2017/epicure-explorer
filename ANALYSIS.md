# Epicure: Navigating the Emergent Geometry of Food Ingredient Embeddings

**Paper Analysis & Summary**

| Field | Detail |
|---|---|
| **arXiv** | [2605.22391](https://arxiv.org/abs/2605.22391) (cs.AI) |
| **Submitted** | 21 May 2026 |
| **Authors** | Jakub Radzikowski & Josef Chen (KAIKAKU.AI) |
| **License** | CC BY 4.0 |
| **Code & artefacts** | Not publicly released at time of publication |

---

## 1. Motivation & Context

### 1.1 The Gap

Computational gastronomy has two main traditions:

- **Flavour networks** (Ahn et al., 2011) — descriptive graphs of compound sharing between ingredients.
- **Knowledge graphs** (FoodKG, 2019) — symbolic RDF ontologies for recipe/nutrition recommendation.
- **Distributed embeddings** (FlavorGraph, Park et al., 2021) — Metapath2Vec over FlavorDB chemistry + Recipe1M+ co-occurrence.

**FlavorGraph**, the most comprehensive public food embedding before Epicure, fused chemistry and recipe-context as a **fixed inductive bias** — a single model with a single answer to "what is this ingredient like?" Epicure's central insight: **chemistry-vs-recipe-context should be a *controllable design axis*, not a hidden architectural constant.**

### 1.2 Prior Work

- **Radzikowski & Chen (2026)** — earlier analysis of FlavorGraph found ≥15 interpretable culinary dimensions (taste, texture, nutrition, geography, processing). That work was limited by: (a) English-only corpus, (b) fixed chemistry/recipe mix, (c) noisy raw vocabulary.
- **Mikolov et al. (2013)** — word2vec linear directions (`king − man + woman ≈ queen`); underwrites both the supervised probes and the SLERP operator.
- **Mu et al. (2017)** — embedding isotropy as precondition for stable directional operations.
- **Caliskan et al. (2017)** — WEAT for semantic-bias diagnostics.

---

## 2. Methods

### 2.1 Corpus

| Source | Language | Recipes | Share |
|---|---|---|---|
| RecipeNLG | English | 2.2M | 53.9% |
| XiaChuFang | Chinese | 1.5M | 37.4% |
| Povarenok | Russian | ~145K | 3.5% |
| +8 smaller corpora | VI, ES, TR, ID, DE, IN-EN | ~190K | ~5% |
| **Total** | **7 languages** | **4,135,189** | **100%** |

Non-English terms machine-translated to English via Claude Opus (temperature 0). After dedup + canonical-vocabulary intersection: **4,103,118 usable recipes.**

### 2.2 Canonical Vocabulary

~200,000 raw NER ingredient strings → LLM-augmented canonicalisation pipeline (Claude Opus for classification, Gemini Embedding for semantic clustering) + manual curation → **1,790 canonical ingredients**.

Each canonical entry anchored to:
- FlavorDB (chemical compounds)
- USDA FoodData Central (nutrients, sensory)

**Cuisine taxonomy:** 8 macro-regions (East Asian, Western Atlantic, Mediterranean, Eastern European, SE Asian, South Asian, Latin American, Japanese). 986/1790 ingredients receive ≥1 cuisine label; 808 are tagged universal.

### 2.3 Graph Construction

| Graph | Nodes | Edges | Notes |
|---|---|---|---|
| **Cooc** | 1,790 ingredients | 203,508 NPMI | Co-occurrence only |
| **Core/Chem** | +2,247 typed compound nodes | +80,019 typed I–C edges | FlavorDB compounds in 15 categories |

**Key design choice:** Compounds are *replicated per flavour category* (citrus, earthy, fatty, floral, fruity, green, meaty, minty, nutty, spicy, vegetable, wine-like, woody, balsamic + residual) — unlike FlavorGraph's single-type node.

### 2.4 The Three Epicure Models

All identical architecture & hyperparameters (300-dim, 100 walks/node, walk_length=50, context=7, 5 neg samples, batch=32,768, lr=0.0025, 20 epochs). They differ only in the **walk schema**:

| Model | Walks | What it captures |
|---|---|---|
| **Cooc** | ingredient↔ingredient only | Pure recipe co-occurrence context |
| **Chem** | typed compound metapaths only | Chemical/flavour-profile similarity |
| **Core** | Cooc + Chem blended (10× I–I injection) | Both signals, recipe-context-dominant |

> Core's 10× ingredient–ingredient walk injection is deliberate — it produces a **concentrated geometry** (participation ratio 94.2 vs 173.6/183.1) that coincides with stronger linear probes and tighter emergent modes. This is a *design lever*, not a defect.

### 2.5 Evaluation

Four evaluation regimes:

1. **Direction quality** — 27 continuous sensory/nutrient directions + 8 cuisine macro-regions, tested for linear recoverability
2. **Intrinsic geometry** — isotropy (participation ratio, avg pairwise cosine), food-group clustering
3. **Emergent geometry** — multi-seed-stable FastICA (20 factors/model) + GMM clustering (~150–200 modes/model)
4. **Operators** — top-K nearest neighbours, mode-membership lookup, SLERP direction arithmetic

---

## 3. Key Results

### 3.1 Geometry & Isotropy

| Metric | Cooc | Core | Chem |
|---|---|---|---|
| Participation ratio | **173.6** (most isotropic) | **94.2** (most concentrated) | **183.1** (most isotropic) |
| Mean pairwise cosine | Lower | Higher | Lower |
| Cuisine separability (Cohen's *d*) | **2.43** | **2.70** | **3.07** |

> **Core is the least isotropic but best-performing on linear probes.** This directly contradicts the premise that isotropy is always desirable — concentration via recipe-context injection is a *feature* for culinary embeddings.

### 3.2 Direction Quality

All three models **linearly recover** the full probe set. The ordering Cooc < Core < Chem holds on **every probe stratum**, including basic-taste, macronutrient, and cuisine probes that the compound schema never sees. **Chemistry walks act as a structural prior** whose reach extends beyond the labels they directly encode.

### 3.3 Emergent Factors (FastICA)

20 interpretable factors per model, including:

- **F0:** Indian Subcontinental Pantry Staples / Global Spice Blends
- **F1:** Steeped & Fermented Beverages / Cocktail Spirits & Liqueurs
- **F4:** Japanese Pantry Staples / Freshwater Fish & Savory Bases
- **F5:** Northern European Rich Cuisine / Eastern Mediterranean & Turkish Pantry
- **F10:** SE Asian Aromatic Pantry / Mediterranean & Atlantic Herbs
- **F18:** Italian-American Deli / Rustic Stocks, Dairy & Game

These are **bipolar factors** — each pole names a coherent culinary cluster, and ingredients sit on a continuum between them.

### 3.4 Culinary Modes (GMM)

| Model | Modes | Mean coherence | Random baseline |
|---|---|---|---|
| Cooc | ~150–200 | **0.611** | 0.097 |
| Core | ~150–200 | **0.833** | 0.348 |
| Chem | ~150–200 | **0.703** | 0.115 |

Core produces the **tightest, most coherent modes** — e.g. "East Asian fermented sauces and processed staples" (196 members), "Italian-Mediterranean deli and cheese" (158), "Processed condiments and Tex-Mex" (142).

### 3.5 Direction Arithmetic (SLERP)

SLERP interpolates between a seed ingredient vector and a target direction vector by a continuous angle θ (0–90°). Examples from the paper:

- **`rice` + `South-Asian` at 30°** → `curry_leaf`, `urad_dal`, `chana_dal`, `fenugreek_seed`
- **`chicken` + `Japanese` at 60°** → `dashi`, `mirin`, `kombu`, `bonito_flakes`
- **`milk` + `Latin_American` at 45°** → `ancho_chile`, `poblano_pepper`, `salsa_verde`

The angle is a **continuous dial**: 0° = seed's own neighbours, 90° = pure target direction. This lets chefs navigate the embedding space at arbitrary resolution.

---

## 4. Critical Assessment

### 4.1 Strengths

1. **Controlled comparison** — three siblings share everything except the one variable (walk schema), making the comparison causal
2. **Multilingual corpus** — first food embedding trained on 7-language data, addressing English-centric bias
3. **Dual operator families** — nearest-neighbour (discrete) + SLERP (continuous) on the same 300-D space
4. **Methodological move** — treating walk schema as a named axis is applicable beyond food (any heterogeneous graph fusion)
5. **LLM-free geometry** — the embeddings themselves are pure skip-gram; LLMs only touch the pipeline (canonicalisation, tagging)

### 4.2 Limitations

1. **Corpus imbalance** — ~50% East Asian, ~10% Mediterranean, single-digit shares for South Asian, Latin American. Limits resolution in underrepresented cuisines.
2. **Hub coverage** — only 523/1790 ingredients have direct compound edges; 1267 get chemistry signal indirectly through via-compound metapaths
3. **LLM dependence in pipeline** — canonical vocabulary, cuisine tagging, and factor labels all use Claude. Embeddings are LLM-free but the node set is LLM-shaped.
4. **No public release** — code and trained artefacts not available at publication time

### 4.3 Connections to FlavorGraph

Epicure extends FlavorGraph in four directions:
- **Vocabulary** — 1,790 canonical vs 6,653 noisy
- **Languages** — 7 vs 1
- **Walk schema** — controllable axis vs fixed
- **Operators** — SLERP + mode lookup vs raw nearest-neighbour

---

## 5. Conclusions & Future Work

The paper argues that a 300-D vector becomes useful to a chef only when wrapped in navigation operators: nearest-neighbour pairings, closest-mode lookup, and SLERP rotation. Three openings are identified:

1. **Continuous mixing** — turn the three siblings into a parameterised family with a tunable chemistry/recipe slider
2. **Richer operators** — intra-mode interpolation, multidirection blends, constrained traversal ("rotate toward Mediterranean *but stay in the dairy mode*")
3. **Cross-modal grounding** — shared canonical vocabulary lets SLERP cross from ingredient space into recipe-text, image, or sensory-descriptor space

---

## 6. Data Files from arXiv

The paper's supplementary bundle (downloaded locally) contains:

| File | Rows | Description |
|---|---|---|
| `epicure_cooc.csv` | 1,790 × 301 | Cooc embeddings (dim_0…dim_299) |
| `epicure_core.csv` | 1,790 × 301 | Core embeddings |
| `epicure_chem.csv` | 1,790 × 301 | Chem embeddings |
| `vocab.csv` | 1,790 × 4 | Cross-model node ID mapping |
| `mode_atlas_*.csv` | ~150–200 modes | GMM culinary modes per model |
| `direction_arithmetic_full.csv` | 2,160 rows | SLERP evaluation results |
| `factor_top_alignments_ica_*.csv` | 20 rows | FastICA factor ↔ supervised label alignments |
| `README.txt` | 38 lines | Authors' notes on the supplementary bundle |
| Additional CSVs | various | WEAT, linear probe, procrustes, cross-modal |

All embeddings are raw skip-gram outputs (not L2-normalised); normalisation applied in analyses. The `data/README.txt` file (from the original authors) documents the CSV schema, cross-referencing via `vocab.csv`, and notes that compound-node embeddings are omitted from the bundle.
