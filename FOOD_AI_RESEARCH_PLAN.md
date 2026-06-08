# 2024–2026 Food AI Research: Strategic Summary & Product Plan

> Compiled for the Epicure Explorer product team.
> Sources: arXiv, GitHub, industry platforms, food science databases, startup landscape.
> Date: June 2026.

---

## Executive Summary

The food AI landscape has undergone a seismic shift between 2024–2026. We are now in the **third wave**:

| Wave | Period | Hallmark | Maturity |
|------|--------|----------|----------|
| **1. Recognition** | 2017–2021 | Food image classification (Food-101, Recipe1M). Cross-modal embeddings (im2recipe, ACME). | Academic |
| **2. Representation** | 2022–2025 | Ingredient embeddings (food2vec, FoodBERT). Knowledge graphs (FoodKG). Recipe generation (Chef Transformer). | Academic + Early commercial |
| **3. Reasoning** | 2026+ | Multilingual chemistry-aware embeddings (Epicure). Topological recipe generation (Losses that Cook). Agentic RAG for food (MARC, GLEN-Bench). CVPR 2026 had 5+ food AI papers. | Production-ready |

**The key insight:** The technology stack for a "chef's kiss" food AI product is now mature. The academic pieces exist. The data exists. The commercial platforms exist (Spoonacular, Foodpairing.ai, Tastewise). What doesn't exist yet is a **unified consumer product** that connects molecular flavor science → ingredient embeddings → recipe intelligence → personalized nutrition → cooking execution.

**That's the opportunity. Epicure Explorer is already the closest thing to it.**

---

> **🧭 Implementation Status — June 2026 (Session 5: Bug-Fix Audit)**
> 
> Month 1 & Month 2 features are **fully shipped** in `index.html` (~4,957 lines, ~259 KB, zero-dependency single-file app). See the [90-Day Roadmap](#section-6-90-day-product-roadmap) below for checkboxes.
> 
> | Area | Status | Notes |
> |------|--------|-------|
> | GLP-1 Diet Mode | ✅ Live | `checkGLP1()`, GLP-1 filter toggle, dietary badges in Chef's Toolkit |
> | Explainable Substitutions | ✅ Live | `explainSubstitute()`, 💡 panel showing molecular+sensory+cuisine overlap |
> | Nutrition Heatmap | ✅ Live | Overlay on Map tab: calories/protein/fat/carbs/fiber |
> | Seasonal Calendar | ✅ Live | 149-ingredient peak-season browser + map overlay |
> | Cocktail Mixology | ✅ Live | Spirit + mixers → embedding centroid + presets |
> | Flavour Arithmetic | ✅ Live | Visual chip UI with history (6 recent expressions) |
> | Spoonacular API | ✅ Live | Recipe search, nutrition, wine pairing (requires user API key) |
> | Fusion Explorer | ✅ Live | Cross-culture bridge ingredients in Games tab |
> | Dish Analyzer | ✅ Live | Comma-separated → dietary + flavour + category analysis |
> | Ingredient Comparator | ✅ Live | Side-by-side comparison of two ingredients |
> | Games (Guess/Compass) | ✅ Live | Quiz + Flavour Compass radar chart |
> | Describe a Dish | ✅ Live | Natural-language → ingredient keyword matching → centroid |
> | Image→Ingredient search (Snap) | ✅ Shipped | Food photo upload → Spoonacular classify → ingredient clickthrough |
> | Ingredient2Vec API | ✅ Shipped | Nearest-neighbour query + flavour arithmetic in 🔬 tab |
> | Personalized Food Agent | ✅ Shipped | Natural language → embedding match in 🤖 tab |
> | What's Trending panel | ✅ Shipped | Seasonal + rarity + diet signals in 📈 tab |
> | GLP-1 Meal Plan Generator | ✅ Shipped | 7-day plan from GLP-1-friendly clusters in 💊 tab |
> | `getForceGraphLayout()` | ✅ Fixed | Fruchterman-Reingold spring-force layout using top-15 neighbour edges |
| Export Summary (📋) | ✅ Live | Clipboard export of ingredient intelligence: substitutes, cuisine, flavour profile, GLP-1 |
| Onboarding Tour (🎓) | ✅ Live | 5-step guided walkthrough overlay on first visit |

## Section 1: The Most Actionable Findings

### 1.1 The GLP-1 Dietary Gap — $500M+ Opportunity

**The finding:** 15M+ Americans now take GLP-1 drugs (Ozempic, Wegovy, Mounjaro, Zepbound). These users need radically different meal plans: high protein, low fat, small portions, appetite-suppressing foods. **No dedicated food AI platform exists for this.**

**Why it's a gap:**
- MyFitnessPal doesn't have a "GLP-1 mode"
- No recipe app adapts for delayed gastric emptying
- No meal planner optimizes for appetite suppression + satiety
- Tastewise reports +85.7% YoY growth in GLP-1-related food signals

**What Epicure Explorer could do:**
- "GLP-1 Friendly" dietary mode in Chef's Toolkit — flags ingredients that work well (high protein, low glycemic, satiety-promoting) vs poorly (high fat, ultra-processed, large portions)
- Recipe suggestions that maximize protein-per-bite while minimizing volume
- Portion-size guidance based on GLP-1 meal patterns (smaller, more frequent)
- **First-mover advantage:** No competitor has this. Ever.

### 1.2 The Ingredient Embedding Moat — No Production API Exists

**The finding:** food2vec (Word2Vec for food, 2016) is archived. FoodBERT (2021) is research-only. Epicure (2026) is the first production-ready multilingual chemistry-aware ingredient embedding — and it's the one we built our app on.

**The gap:** No company offers "Ingredient2Vec-as-a-Service" — a hosted API that takes ingredient names and returns embedding vectors, nearest neighbours, direction arithmetic, or substitution scores.

**What Epicure Explorer could do:**
- Be the **first production embedding API for food**
- Offer: `GET /nearest?ingredient=miso&model=chem&k=10` → JSON of nearest neighbours
- Offer: `GET /substitute?ingredient=butter&constraint=dairy_free` → ranked substitutes
- Offer: `POST /arithmetic` → `{ "expression": "chicken + coconut_milk + ginger" }` → centroid results
- License to meal planning apps, restaurant tech, CPG R&D

### 1.3 Explainable Food AI — The Trust Gap

**The finding:** Every consumer food recommendation system is a black box. Samsung Food, Yummly, Epicurious — none explain *why* a recipe is recommended. Yet the research exists:
- GLEN-Bench (arXiv:2601.18106): Graph-grounded explanations for "why this food?"
- PFoodReq (WSDM 2021): KBQA formulation with constraint handling
- LLM-RAG HEI (arXiv:2605.15213): "This substitute improves your Healthy Eating Index by 6.45 points"

**What Epicure Explorer could do:**
- Every recommendation includes explanation: "Suggested because it's 78% similar to miso in fermentation chemistry (Amino Acid note) AND it's used in similar recipes (gochujang appears in 82% of the same dishes)"
- Chef's Toolkit already has the data — just need an explanation panel: "Why this substitute?"

### 1.4 Cross-Modal Food Search — One Search to Rule Them All

**The finding:** The research supports unified food search across modalities:
- F4-ITS (arXiv:2508.17037): Training-free image→text fusion for food search
- Thought-For-Food (arXiv:2511.01213): Reasoned answers about food from images
- DietDelta (arXiv:2604.06352): Before/after meal photos → what was eaten

**No consumer product combines these.** You can't say "show me high-protein vegetarian dinners under 500 calories I can make with chicken" — and get a useful answer.

**What Epicure Explorer could do:**
- A single natural language search bar that queries across: ingredients, recipes, nutrition, dietary constraints, what's in your fridge
- "What can I make with chicken, coconut milk, and ginger that's under 600 calories?" → embedding arithmetic + nutrition + recipe retrieval

### 1.5 Consumer Molecular Gastronomy — The Democratization Opportunity

**The finding:** Foodpairing.ai is the leader in molecular flavor pairing — but it's B2B/enterprise only, costing thousands per year. No consumer product exists for "what flavors go with X?" at the molecular level.

**Epicure Explorer already has:** The Chem model (FlavorDB-derived molecular relationships), 12 molecular flavour notes (Lactone, Ester, Terpene, etc.), sensory direction vectors.

**The gap:** No consumer app explains "why" chocolate and chili work together (they share pyrazine compounds — Maillard reaction products).

**What Epicure Explorer could do:**
- "Molecule of the Dish" feature — show the chemical compounds that explain a pairing
- "Why This Works" panel in Chef's Toolkit — "Miso + butter work because miso contributes Amino Acid notes (savory/fermented) while butter contributes Lipid notes (creamy/fatty) — they occupy complementary sensory directions"

---

## Section 2: Technical Enrichments Already Built

These are features that the 2024–2026 research validates and that exist in the current Epicure Explorer:

| Feature | Research Backing | Status |
|---------|-----------------|--------|
| 3-model embeddings (Cooc/Chem/Core) | Epicure (arXiv:2605.22391) | ✅ Built |
| Multilingual ingredient coverage (7 languages) | Epicure training data | ✅ Built |
| Direction arithmetic (SLERP toward sensory directions) | Epicure direction vectors | ✅ Built |
| Substitution with model toggle | FoodBERT + Epicure model comparison | ✅ Built (Chef's Toolkit Pro) |
| 12 molecular flavour notes | FlavorDB + Epicure Chem model | ✅ Built |
| Cross-culture bridge analysis | Epicure 7-language embedding space | ✅ Built (Fusion Explorer) |
| Dish Analyzer (full ingredient list → dietary + category + suggestions) | MIGP + FoodKG approaches | ✅ Built |
| Ingredient Comparator (side-by-side flavour, cuisine, neighbours) | Recipe similarity research | ✅ Built |
| Flavour Arithmetic (centroid from expressions) | Epicure embedding arithmetic | ✅ Built |
| Force-Directed Graph projection | Embedding visualization best practices | ✅ Built |
| Cost/waste/seasonal hints | Real-world chef knowledge | ✅ Built |

---

## Section 3: Highest-Impact New Features to Build

### P0 = Build now (weeks). P1 = Build next (months). P2 = Research phase (quarters).

| Priority | Feature | Effort | Research Backing | Why Now |
|----------|---------|--------|------------------|---------|
| **P0** | GLP-1 Diet Mode — toggle in Chef's Toolkit that flags GLP-1-friendly ingredients, suggests high-protein/satiety substitutions, adapts meal recommendations | Low (heuristic + tags) | Tastewise data (+85.7% YoY), no competitor exists | **Massive underserved market, trivial to implement** |
| **P0** | Explainable Substitutions — "Why This Substitute?" panel showing molecular overlap, recipe co-occurrence, sensory direction match | Low (data already displayed, just need explanation text) | GLEN-Bench, PFoodReq, LLM-RAG HEI | Builds trust + educational value |
| **P0** | Flavour Arithmetic Explorer — turn the tab into a visual playground with ingredient chips, drag-to-add, instant results, saved expressions | Medium (UI work) | Epicure arithmetic validated | Most "wow" feature for chefs |
| **P1** | Recipe Generation from Ingredients — Ingredient list → topologically sound recipe with timing, temperature, procedure | High (needs LLM integration) | Losses that Cook (arXiv:2601.02531) | Game-changer for meal planning |
| **P1** | Image→Ingredient Search — Upload a food photo → identify ingredients → search in embedding space | Medium (F4-ITS integration) | F4-ITS (arXiv:2508.17037), Thought-For-Food | Natural onboarding channel |
| **P1** | Cocktail/Mixology Mode — Enter available spirits + mixers → embedding finds best cocktail recipes | Low-Med (reuses arithmetic + neighbours) | MARC (arXiv:2511.08181) | Hospitality industry use case |
| **P1** | Seasonal & Regional Ingredient Calendar — Overlay seasonal peak data, regional availability on the embedding map | Medium (needs data) | Seasonality heuristics + USDA data | Practical chef tool |
| **P1** | Nutrition Heatmap Overlay on UMAP — Color projection by calories/protein/fat/carbs/fiber | Low (pre-computed data) | USDA FoodData Central | Scientific insight layer |
| **P2** | Personalised Food Agent — "I have chicken, coconut milk, ginger. What's for dinner under 600 calories that's GLP-1 friendly?" → multi-agent reasoning | High | FinAgent (arXiv:2512.20991), FedTREK-LM | Long-term moat |
| **P2** | Fermentation AI — Predict fermentation outcomes for sourdough, kimchi, kombucha based on ingredient inputs | Very High | Emerging research area | Niche but defensible |
| **P2** | 3D Photo→Nutrition — Snap a plate → 3D mesh → volume → calorie/nutrient estimation | High (needs 3D model) | PerBite (arXiv:2606.02021), OmniFood8K (arXiv:2604.12356) | Cutting-edge accuracy |
| **P2** | RecipeCrit Integration — Paste a recipe, get ingredient-level critiques and rewrite suggestions | High (needs LLM) | RecipeCrit (EACL 2023) | Professional kitchen tool |

---

## Section 4: Strategic Partnerships & Data Sources

| Partner | Asset | Integration Strategy |
|---------|-------|---------------------|
| **Spoonacular** (spoonacular.com) | 1M+ recipes, 600K+ products, nutrition API, wine pairing | Primary recipe + nutrition data API. Use for recipe search, nutrition analysis, cost breakdowns. 253K registered developers — existing ecosystem. |
| **Open Food Facts** (world.openfoodfacts.org) | 3M+ scanned food products, crowd-sourced | Barcode scanning for packaged foods. "Scan an ingredient → find its flavour profile." |
| **FlavorDB** (cosylab.iiitd.edu.in/flavordb/) | 25,595 flavor molecules, 936 ingredients | Chemical ground truth layer. Already used by Epicure's Chem model. Extend molecular notes with specific compound names. |
| **FooDB** (foodb.ca) | 28K+ foods, 2,400+ bioactive compounds | Nutrient-compound relationships. "This ingredient is rich in quercetin (anti-inflammatory)." |
| **Tastewise** (tastewise.io) | 1T+ food signals, trend prediction, 96% F&B accuracy | Trend data for "what's trending" features. Could license trend signals for professional chef tier. |
| **Foodpairing.ai** (foodpairing.com) | Enterprise molecular gastronomy KG | Too expensive to license directly. Study their approach as a reference for our molecular notes. |
| **Samsung Food** (samsungfood.com) | 50M+ users, Whisk AI | Competitor reference. Study their UX for recipe recommendation + meal planning. |
| **USDA FoodData Central** | Comprehensive US nutrition database | Free, authoritative nutrition data. Use for nutrition heatmap and dietary analysis. |

---

## Section 5: The Competitive Landscape

```
                    B2B                         B2C
                    +----------------+----------------+
                    |                |                |
    FLAVOR/         |  Foodpairing   |  ⭐ EPICURE   |
    MOLECULAR       |  Climax Foods  |  EXPLORER      |
                    |  NotCo/Giuseppe|  (GAP)         |
                    |                |                |
    +---------------|----------------|----------------|
                    |                |                |
    RECIPE/         |  Winnow        |  Samsung Food  |
    NUTRITION       |  Deliverect    |  Yummly        |
                    |  Sunday        |  MyFitnessPal  |
                    |                |                |
    +---------------|----------------|----------------|
                    |                |                |
    KITCHEN         |  Miso Robotics |  Kū inc        |
    EXECUTION       |  Picnic        |  (GAP)         |
                    |  Dexai         |                |
                    +----------------+----------------+
```

**Epicure Explorer occupies the top-right quadrant — consumer molecular gastronomy + intelligent ingredient AI — a space with NO dominant player.**

### Key Competitor Analysis

| Competitor | What They Do | Where They're Weak | Our Advantage |
|-----------|-------------|-------------------|---------------|
| **Samsung Food (Whisk)** | Recipe recommendation, meal planning, 50M+ users | No molecular/ingredient layer. Black-box recommendations. No explainability. No embedding arithmetic. | **Ingredient-first approach.** Explainable AI. Molecular notes. Embedding arithmetic. |
| **Foodpairing.ai** | Enterprise flavor pairing, CPG innovation | B2B only, expensive ($10K+/yr), not consumer-friendly. No recipe integration. | **Free, consumer-friendly.** Chef's Toolkit Pro approaches their capabilities. |
| **Yummly** | Personalized recipe search | Limited AI depth. No ingredient intelligence. | **Embedding layer** — understanding ingredients, not just recipes. |
| **MyFitnessPal** | Calorie tracking | Manual logging. No flavor intelligence. | **Nutrition from ingredients + flavour context** — what you eat AND why. |
| **Tastewise** | Trend prediction for food brands | B2B only. Not a consumer app. | Could be a data source for trend features, not a direct competitor. |

---

## Section 6: 90-Day Product Roadmap

### Month 1: Foundation
- [x] Chef's Toolkit Pro (substitution toggle, molecular notes, cost hints)
- [x] Fusion Explorer (cross-culture bridge ingredients)
- [x] Dish Analyzer (ingredient list → dietary + category + suggestions)
- [x] Ingredient Comparator (side-by-side flavour, cuisine, neighbours)
- [x] Flavour Arithmetic (expression-based vector maths)
- [x] Professional Chef's Playbook (GUIDE.md rewrite)
- [x] **GLP-1 Diet Mode** — heuristic tags and substitution logic (GLP1_RULES, checkGLP1(), GLP-1 filter in Chef's Toolkit)
- [x] **Explainable Substitutions** — "Why This Substitute?" panel (explainSubstitute(), 💡 button, molecular+sensory+cuisine overlap)

### Month 2: Extension
- [x] **Nutrition Heatmap Overlay** — color UMAP by calories/protein/fat/carbs/fiber (nutrientOverlay dropdown in Map tab)
- [x] **Seasonal Ingredient Calendar** — peak season overlays (SEASONAL_DATA, isIngredientInSeason(), renderSeasonal())
- [x] **Cocktail/Mixology Mode** — spirit + mixer → cocktail suggestions (runCocktail(), presets)
- [x] **Flavour Arithmetic Explorer** — visual chip-based UI, saved expressions (renderArithChips(), arithHistory)
- [x] **Spoonacular API integration** — recipe search + nutrition lookup (UI + JS complete, requires user API key)

### Month 3: Differentiation
- [x] **Image→Ingredient search** — upload food photo → identify ingredients → explore
- [x] **Ingredient2Vec API** — nearest-neighbour query & flavour arithmetic UI (🔬 tab)
- [x] **Personalized Food Agent prototype** — natural language food queries via embedding matching (🤖 tab)
- [x] **"What's Trending" panel** — seasonal + rarity + GLP-1 trend signals (📈 tab)
- [x] **GLP-1 meal plan generator** — 7-day GLP-1-optimized meal plan from embedding clusters (💊 tab)

---

## Section 7: Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Spoonacular API changes/deprecation | Medium | Cache aggressively. Keep local recipe index as fallback. |
| Competitor builds GLP-1 mode first | High (mitigated — shipped June 8, 2026) | GLP-1 tags, filter, and substitution logic now live in Chef's Toolkit. First-mover advantage. |
| LLM-based recipe generation (Losses that Cook) requires too much compute | Medium | Start with small models (Qwen3 0.6B-4B as in FedTREK-LM). Offer as premium tier. |
| Foodpairing.ai launches consumer product | Low-Medium | Our embedding approach is different (Epicure vs molecular KG). We have recipe integration they don't. |
| Samsung Food adds molecular features | Low | They're a recipe platform, not an ingredient platform. Architecture change would be massive for them. |

---

## Section 8: Research Sources & References

All sources listed in the full research document (`FOOD_AI_RESEARCH_COMPLETE.md` if you want the exhaustive version). Key starting points:

| Topic | Best Source |
|-------|-------------|
| Ingredient embeddings | Epicure (arXiv:2605.22391) |
| Recipe generation | Losses that Cook (arXiv:2601.02531) |
| Food image search | F4-ITS (arXiv:2508.17037) |
| Food KG + Graph-RAG | GLEN-Bench (arXiv:2601.18106), MARC (arXiv:2511.08181) |
| Meal optimization | MIGP (arXiv:2605.13849) |
| Multi-agent food AI | FinAgent (arXiv:2512.20991) |
| Nutrition from images | PerBite (arXiv:2606.02021), OmniFood8K (arXiv:2604.12356) |
| Industry trends | Tastewise.io data, Spoonacular API docs |
| Molecular flavor data | FlavorDB2, Foodpairing.ai blog |
| Open-source repos | Food-101 (712★), KERL (14★), RecipeRec (16★) |

---

*This plan is a living document. Re-check arXiv and GitHub monthly. The food AI field is accelerating rapidly — CVPR 2026 alone produced 5+ major food AI papers, signaling that this is now a mainstream research area with production-ready outputs.*
