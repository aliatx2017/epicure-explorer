"""
Preprocess Epicure embeddings for the web explorer.
Computes nearest neighbours, UMAP projection, and direction vectors.
Outputs separate shared + per-model JSON files for lazy-loading.

Usage:
    cd epicure-explorer
    python3 -m venv .venv && .venv/bin/pip install umap-learn
    .venv/bin/python3 preprocess.py
"""
import json
import math
import csv
import struct
import base64
import sys
import os

DATA_DIR = "data"

# ── UMAP ──
# Falls back to PCA if umap is not available.
_UMAP_AVAILABLE = False
_UMAP_VERSION = None
_SKLEARN_VERSION = None
try:
    import umap
    _UMAP_AVAILABLE = True
    _UMAP_VERSION = getattr(umap, "__version__", "unknown")
    import sklearn
    _SKLEARN_VERSION = getattr(sklearn, "__version__", "unknown")
except ImportError:
    pass

# ── Helpers ──

def load_embeddings(path):
    """Load embedding CSV, return (names, vectors) where vectors is list of lists."""
    names = []
    vectors = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        dim_cols = [c for c in reader.fieldnames if c.startswith("dim_")]
        for row in reader:
            names.append(row["name"])
            vec = [float(row[c]) for c in dim_cols]
            vectors.append(vec)
    return names, vectors

def l2_normalize(vectors):
    """In-place L2 normalization."""
    for i, v in enumerate(vectors):
        norm = math.sqrt(sum(x * x for x in v))
        if norm > 0:
            vectors[i] = [x / norm for x in v]
    return vectors

def compute_similarities(vectors):
    """Compute cosine similarity matrix."""
    n = len(vectors)
    sims = [[0.0] * n for _ in range(n)]
    for i in range(n):
        vi = vectors[i]
        for j in range(i, n):
            vj = vectors[j]
            s = sum(vi[k] * vj[k] for k in range(len(vi)))
            sims[i][j] = s
            sims[j][i] = s
    return sims

def top_neighbours(sims, k=30):
    """For each item, return list of (index, similarity) for top-k neighbours.
    Excludes self (index == i)."""
    n = len(sims)
    result = []
    for i in range(n):
        pairs = [(j, sims[i][j]) for j in range(n) if j != i]
        pairs.sort(key=lambda x: -x[1])
        result.append(pairs[:k])
    return result

def pca_2d(vectors):
    """Compute 2D PCA projection using power iteration. Fallback when UMAP unavailable."""
    n = len(vectors)
    d = len(vectors[0])

    # Center the data
    mean = [0.0] * d
    for v in vectors:
        for j in range(d):
            mean[j] += v[j]
    mean = [m / n for m in mean]
    centered = [[v[j] - mean[j] for j in range(d)] for v in vectors]

    def mat_vec_mul(vec):
        temp = [sum(row[j] * vec[j] for j in range(d)) for row in centered]
        return [sum(centered[i][j] * temp[i] for i in range(n)) for j in range(d)]

    def normalize_vec(vec):
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec]

    import random
    # First component
    v = [random.gauss(0, 1) for _ in range(d)]
    for _ in range(100):
        v = mat_vec_mul(v)
        v = normalize_vec(v)
    pc1 = v
    scores1 = [sum(row[j] * pc1[j] for j in range(d)) for row in centered]

    # Deflate
    centered2 = []
    for row in centered:
        proj = sum(row[j] * pc1[j] for j in range(d))
        centered2.append([row[j] - proj * pc1[j] for j in range(d)])

    # Second component
    v2 = [random.gauss(0, 1) for _ in range(d)]
    for _ in range(100):
        temp = [sum(row[j] * v2[j] for j in range(d)) for row in centered2]
        v2_new = [sum(centered2[i][j] * temp[i] for i in range(n)) for j in range(d)]
        v2 = normalize_vec(v2_new)
    pc2 = v2
    scores2 = [sum(row[j] * pc2[j] for j in range(d)) for row in centered]

    return list(zip(scores1, scores2))

def umap_2d(vectors):
    """Compute 2D UMAP projection — better visual clustering than PCA."""
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=15,
        min_dist=0.1,
        metric="cosine",
        random_state=42,
        verbose=False,
    )
    embedding = reducer.fit_transform(vectors)
    return [(float(x), float(y)) for x, y in embedding]

# ── Cuisine mode-atlas mapping ──
# Mode IDs from the Core model GMM atlas that explicitly represent each cuisine.
# These are the paper's emergent culinary clusters — their members are the closest
# approximation to the Claude-tagged per-ingredient cuisine labels.
# See tools/compute_cuisine_directions.py for the full curated mapping.

CUISINE_MODE_IDS = {
    "east_asian": {
        "nova_level/M1", "nova_level/M3", "cf_sweet/M3", "cf_sweet/M4",
        "cf_savory/M1", "cf_savory/M2", "cf_savory/M4",
        "cf_meaty/M0", "cf_balsamic/M0",
        "sour_score/M0", "bitter_score/M3", "umami_score/M0",
        "pungent_score/M1", "pungent_score/M3", "fatty_score/M0",
        "usda_fiber_g/M4", "usda_caloric_density/M1",
        "fg_Pantry/M1", "fg_Vegetable/M1", "fg_Vegetable/M3", "fg_Spice/M4", "fg_Fruit/M0",
        "F_0/M1", "F_0/M2", "F_1/M0", "F_2/M0", "F_3/M0", "F_4/M1", "F_5/M0",
        "F_7/M0", "F_7/M3", "F_7/M4", "F_8/M2", "F_8/M3",
        "F_9/M0", "F_9/M4", "F_10/M4", "F_11/M0", "F_12/M0", "F_12/M2",
        "F_13/M0", "F_14/M1", "F_14/M4", "F_15/M2", "F_17/M0", "F_19/M4",
    },
    "western_atlantic": {
        "F_12/M1", "F_15/M0", "F_9/M2", "F_15/M4", "F_8/M0",
        "F_19/M1", "F_19/M2", "nova_level/M5",
    },
    "mediterranean": {
        "nova_level/M4", "cf_sweet/M0",
        "cf_savory/M0", "cf_savory/M5",
        "cf_meaty/M2", "cf_balsamic/M3", "cf_citrus/M1", "cf_minty/M5",
        "sour_score/M3", "bitter_score/M1", "umami_score/M1",
        "pungent_score/M2", "fatty_score/M1",
        "usda_protein_g/M2", "usda_fiber_g/M0", "usda_caloric_density/M0",
        "F_1/M2", "F_10/M2", "F_13/M4",
    },
    "eastern_european": {
        "fg_Dairy/M0", "F_1/M1", "F_5/M3",
    },
    "southeast_asian": {
        "sweet_score/M3", "cf_citrus/M0", "F_6/M1", "F_10/M3",
    },
    "south_asian": {
        "cf_minty/M2", "fg_Spice/M0",
    },
    "latin_american": {
        "cf_savory/M6", "cf_citrus/M3", "cf_minty/M3",
        "cf_woody/M0", "sour_score/M1", "bitter_score/M4", "fatty_score/M4",
        "usda_fiber_g/M1", "F_4/M0", "F_4/M3", "F_2/M4", "F_14/M3",
    },
    "japanese": {
        "F_8/M5",
    },
}

# Additional keyword seeds for cuisines with weak mode coverage
CUISINE_SEEDS = {
    "japanese": [
        "soy_sauce", "miso", "sake", "mirin", "dashi", "kombu",
        "bonito_flakes", "nori", "wasabi", "tofu", "edamame", "shiso",
        "sesame", "rice_vinegar", "tempura", "udon", "soba", "matcha",
        "green_tea", "shiitake", "enoki", "daikon", "natto", "umeboshi",
        "yuzu", "ponzu", "teriyaki_sauce", "katsuobushi", "panko", "mochi",
        "azuki_bean", "shichimi_togarashi", "shoyu",
    ],
    "eastern_european": [
        "sour_cream", "dill", "beetroot", "cabbage", "sauerkraut",
        "kefir", "buckwheat", "rye_bread", "horseradish", "borscht", "caraway",
    ],
    "south_asian": [
        "cumin", "coriander_seed", "turmeric", "garam_masala", "curry_leaf",
        "mustard_seed", "fenugreek", "cardamom", "ghee", "lentil",
        "chickpea", "basmati_rice", "naan", "asafoetida", "mango_powder",
        "nigella_seed", "paneer", "chana_dal", "urad_dal", "toor_dal", "rose_water",
    ],
}

def load_mode_atlas(path):
    """Load mode atlas CSV into a dict keyed by mode_id."""
    modes = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member_set = set(m.strip() for m in row["members_pipe"].split("|"))
            modes[row["mode_id"]] = member_set
    return modes

def compute_directions(names, vectors, mode_atlas_path=None):
    """Compute sensory + cuisine direction vectors as centroid differences.

    Sensory directions use keyword centroid.
    Cuisine directions use the Core model's GMM mode atlas members + keyword seeds.
    This replaces the old approach of heuristic keyword lists + NN expansion.
    """
    name_to_idx = {n: i for i, n in enumerate(names)}
    name_to_vec = {n: v for n, v in zip(names, vectors)}

    # ── Sensory directions (8) — unchanged ──
    sensory_keywords = {
        "sweet": ["sugar", "honey", "chocolate", "vanilla", "caramel", "maple_syrup", "candy", "butterscotch", "marshmallow", "syrup"],
        "spicy": ["chili_pepper", "cayenne", "jalapeno", "sriracha", "red_pepper_flakes", "habanero", "serrano_pepper", "chile_powder", "black_pepper"],
        "savory_umami": ["soy_sauce", "miso", "fish_sauce", "mushroom", "parmesan_cheese", "tomato", "worcestershire_sauce", "yeast", "anchovy"],
        "citrus_sour": ["lemon", "lime", "orange", "grapefruit", "vinegar", "rice_vinegar", "balsamic_vinegar", "tamarind", "yuzu"],
        "fermented": ["kimchi", "sauerkraut", "yogurt", "miso", "soy_sauce", "tempeh", "kefir", "pickle", "kombucha", "sourdough"],
        "bitter": ["coffee", "dark_chocolate", "kale", "brussels_sprout", "radicchio", "dandelion_green", "grapefruit", "espresso", "cacao_nib"],
        "creamy_dairy": ["butter", "cream", "milk", "cheese", "yogurt", "sour_cream", "cottage_cheese", "cream_cheese", "mozzarella", "brie"],
        "herbal": ["basil", "oregano", "thyme", "rosemary", "mint", "cilantro", "parsley", "dill", "sage", "chive"],
    }

    directions = {}

    # Helper: centroid + normalize
    def centroid_of(names_subset):
        vecs = [name_to_vec[n] for n in names_subset if n in name_to_idx]
        if len(vecs) < 3:
            return None
        c = [sum(v[j] for v in vecs) / len(vecs) for j in range(len(vectors[0]))]
        norm = math.sqrt(sum(x * x for x in c))
        if norm == 0:
            return None
        return [x / norm for x in c]

    # Process sensory directions (keyword centroid — unchanged)
    for direction, keywords in sensory_keywords.items():
        c = centroid_of(keywords)
        if c is not None:
            directions[direction] = c

    # ── Process cuisine directions using mode atlas ──
    # Load mode atlas (Core model) to get cuisine-tagged ingredient clusters
    mode_members = {}
    if mode_atlas_path and os.path.exists(mode_atlas_path):
        mode_members = load_mode_atlas(mode_atlas_path)
        print(f"  Loaded {len(mode_members)} modes from Core atlas")
    else:
        print(f"  ⚠️  Mode atlas not found at {mode_atlas_path}, falling back to keyword-only mode")
        # Fallback: use old keyword-based approach
        _fallback_cuisine_directions(names, vectors, directions, name_to_idx, name_to_vec)

    for direction, mode_ids in CUISINE_MODE_IDS.items():
        # Collect members from assigned modes
        members = set()
        for mid in mode_ids:
            if mid in mode_members:
                members.update(mode_members[mid])

        # Add keyword seeds
        seeds = CUISINE_SEEDS.get(direction, [])
        members.update(seeds)

        if len(members) < 3:
            print(f"    ⚠️  {direction}: only {len(members)} members, skipping")
            continue

        centroid = centroid_of(list(members))
        if centroid is not None:
            directions[direction] = centroid
            print(f"    {direction:20s}: {len(members):4d} members → centroid computed")
        else:
            print(f"    ⚠️  {direction}: centroid failed")

    return directions, sensory_keywords, dict(CUISINE_MODE_IDS)

def _fallback_cuisine_directions(names, vectors, directions, name_to_idx, name_to_vec):
    """Original keyword-list + NN-expansion approach — used when mode atlas is unavailable."""
    # (kept for backward compatibility)
    cuisine_keywords = {
        "east_asian": ["soy_sauce", "miso", "gochujang", "doubanjiang", "kimchi", "natto", "tofu",
            "kombu", "dashi", "nori", "wasabi", "rice_vinegar", "sake", "mirin",
            "bonito_flakes", "shiso", "perilla", "seaweed", "edamame", "bok_choy",
            "sesame_oil", "oyster_sauce", "hoisin_sauce", "udon_noodle", "soba_noodle",
            "ramen_noodle", "wonton_wrapper", "five_spice", "star_anise",
            "sichuan_peppercorn", "shiitake", "enoki", "bean_sprout",
            "water_chestnut", "bamboo_shoot", "chinese_cabbage", "chili_paste",
            "fermented_black_bean", "char_siu", "chow_mein_noodle",
        ],
        "western_atlantic": ["butter", "cream", "milk", "cheddar_cheese", "parmesan_cheese",
            "mozzarella", "brie", "camembert", "bread", "potato", "carrot",
            "celery", "black_pepper", "olive_oil", "parsley", "thyme", "rosemary",
            "sage", "chicken", "beef", "pork", "bacon", "egg", "flour", "sugar",
            "tomato", "lettuce", "cucumber", "apple", "pear", "grape",
            "cinnamon", "nutmeg", "clove", "vanilla", "cheese", "mayonnaise",
            "mustard", "ketchup", "worcestershire_sauce", "bay_leaf",
        ],
        "mediterranean": ["olive_oil", "basil", "oregano", "tomato", "mozzarella", "parmesan_cheese",
            "balsamic_vinegar", "caper", "anchovy", "rosemary", "thyme",
            "eggplant", "zucchini", "bell_pepper", "lemon", "garlic", "onion",
            "feta_cheese", "kalamata_olive", "pine_nut", "artichoke",
            "sun_dried_tomato", "sardine", "mint", "couscous", "chickpea",
            "lamb", "yogurt", "cucumber", "pita_bread", "hummus", "tahini",
            "pistachio", "saffron", "cinnamon", "oregano",
        ],
        "eastern_european": ["sour_cream", "dill", "potato", "beetroot", "cabbage", "sauerkraut",
            "kefir", "buckwheat", "rye_bread", "pickle", "horseradish", "mustard",
            "mushroom", "pork", "sausage", "apple", "cottage_cheese", "barley",
            "onion", "garlic", "parsley", "dill_pickle", "caraway", "dill_weed",
            "beef", "potato_starch", "borscht",
        ],
        "southeast_asian": ["lemongrass", "galangal", "kaffir_lime", "coconut_milk", "fish_sauce",
            "chili", "shallot", "ginger", "turmeric", "coriander", "thai_basil",
            "cilantro", "peanut", "shrimp_paste", "tamarind", "palm_sugar",
            "rice_noodle", "rice", "mung_bean", "long_bean", "coconut_cream",
            "thai_chili", "sambal", "satay", "soy_sauce", "rice_flour",
            "pandan_leaf", "lime", "banana_leaf",
        ],
        "south_asian": ["cumin", "coriander_seed", "turmeric", "garam_masala", "curry_leaf",
            "mustard_seed", "fenugreek", "cardamom", "cinnamon", "clove",
            "ginger", "garlic", "onion", "ghee", "yogurt", "lentil", "chickpea",
            "basmati_rice", "naan", "chili", "coconut", "tamarind", "asafoetida",
            "mango_powder", "nigella_seed", "fennel_seed", "poppy_seed",
            "paneer", "saffron", "rose_water", "cashew", "almond", "raisin",
            "chana_dal", "urad_dal", "toor_dal", "rice_flour",
        ],
        "latin_american": ["jalapeno", "habanero", "ancho_chile", "poblano_pepper", "salsa_verde",
            "tortilla", "cumin", "black_bean", "cilantro", "lime", "avocado",
            "corn", "tomato", "onion", "garlic", "oregano", "chili_powder",
            "cayenne", "bell_pepper", "sweet_potato", "plantain", "pinto_bean",
            "rice", "refried_bean", "chipotle", "guajillo_chile", "achiote",
            "coconut", "cassava", "quinoa", "amaranth",
        ],
        "japanese": ["soy_sauce", "miso", "sake", "mirin", "dashi", "kombu", "bonito_flakes",
            "nori", "wasabi", "ginger", "tofu", "edamame", "shiso", "sesame",
            "rice_vinegar", "tempura", "udon", "soba", "matcha", "green_tea",
            "shiitake", "enoki", "daikon", "natto", "umeboshi", "yuzu",
            "shichimi_togarashi", "mitsuba", "myoga", "sansho_pepper",
            "ponzu", "teriyaki_sauce", "katsuobushi", "shoyu",
            "japanese_mayonnaise", "panko", "mochi", "azuki_bean",
        ],
    }

    def centroid_of(names_subset):
        vecs = [name_to_vec[n] for n in names_subset if n in name_to_idx]
        if len(vecs) < 3:
            return None
        c = [sum(v[j] for v in vecs) / len(vecs) for j in range(len(names[0]))]
        norm = math.sqrt(sum(x * x for x in c))
        if norm == 0:
            return None
        return [x / norm for x in c]

    for direction, keywords in cuisine_keywords.items():
        seed_centroid = centroid_of(keywords)
        if seed_centroid is None:
            continue
        # NN expansion
        sims = []
        for i, v in enumerate(vectors):
            s = sum(seed_centroid[j] * v[j] for j in range(len(v)))
            sims.append((names[i], s))
        sims.sort(key=lambda x: -x[1])
        expanded = set(keywords)
        for name, sim in sims:
            if sim >= 0.4:
                expanded.add(name)
            else:
                break
        expanded_centroid = centroid_of(list(expanded))
        if expanded_centroid is not None:
            directions[direction] = expanded_centroid
        else:
            directions[direction] = seed_centroid

    print("    (fallback: keyword + NN expansion used for cuisine directions)")


# ── Mode Atlas ──

def load_mode_atlas(path):
    """Load mode atlas CSV into a dict keyed by member ingredient name."""
    mode_map = {}
    mode_list = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mode_id = row["mode_id"]
            label = row["label"]
            kind = row["kind"]
            property_name = row["property"]
            members = [m.strip() for m in row["members_pipe"].split("|")]
            mode_list.append({
                "id": mode_id,
                "label": label,
                "kind": kind,
                "property": property_name,
                "n_members": int(row["n_members"]),
                "members": members
            })
            for member in members:
                if member not in mode_map:
                    mode_map[member] = []
                mode_map[member].append({
                    "mode_id": mode_id,
                    "label": label,
                    "kind": kind,
                    "property": property_name
                })
    return mode_list, mode_map


# ── Main ──

def main():
    print("Loading embeddings...")

    models_data = {}
    for model_name in ["cooc", "core", "chem"]:
        path = os.path.join(DATA_DIR, f"epicure_{model_name}.csv")
        names, vectors = load_embeddings(path)
        vectors = l2_normalize(vectors)
        print(f"  {model_name}: {len(names)} ingredients, {len(vectors[0])} dims")

        # Compute nearest neighbours
        print(f"  Computing similarities for {model_name}...")
        sims = compute_similarities(vectors)
        neighbours = top_neighbours(sims, k=25)

        # 2D projection (UMAP preferred, PCA fallback)
        if _UMAP_AVAILABLE:
            print(f"  Computing UMAP for {model_name}...")
            proj = umap_2d(vectors)
        else:
            print(f"  Computing PCA for {model_name}...")
            proj = pca_2d(vectors)

        models_data[model_name] = {
            "names": names,
            "vectors": vectors,
            "neighbours": neighbours,
            "proj": proj,
        }

    # Compute direction vectors (sensory + cuisine)
    print("Computing direction vectors...")
    mode_atlas_path = os.path.join(DATA_DIR, "mode_atlas_core.csv")
    directions, sensory_keywords, cuisine_sources = compute_directions(
        models_data["cooc"]["names"],
        models_data["cooc"]["vectors"],
        mode_atlas_path=mode_atlas_path
    )
    cuisine_keywords = cuisine_sources  # For directionGroups output
    print(f"  Sensory: {list(sensory_keywords.keys())}")
    print(f"  Cuisine: {list(cuisine_keywords.keys())}")

    # Load mode atlases
    print("Loading mode atlases...")
    mode_atlases = {}
    for model_name in ["cooc", "core", "chem"]:
        path = os.path.join(DATA_DIR, f"mode_atlas_{model_name}.csv")
        if os.path.exists(path):
            mode_list, mode_map = load_mode_atlas(path)
            mode_atlases[model_name] = {"list": mode_list, "map": mode_map}
            print(f"  {model_name}: {len(mode_list)} modes")

    # Shared vocabulary (all models share the same ingredient list)
    all_names = models_data["cooc"]["names"]

    # ── Write shared data (small: ingredients + directions) ──
    print("\nWriting shared data...")
    shared = {
        "ingredients": all_names,
        "directions": {k: v for k, v in directions.items()},
        "directionGroups": {
            "sensory": list(sensory_keywords.keys()),
            "cuisine": list(cuisine_keywords.keys()),
        },
        "_metadata": {
            "preprocess_version": "2.1",
            "generated": "2026-06-07",
            "n_ingredients": len(all_names),
            "n_directions": 16,
            "direction_method": "sensory: keyword centroid; cuisine: Core GMM mode-atlas members + keyword seeds",
            "direction_cuisine_sources": {k: list(v) for k, v in cuisine_sources.items()},
        },
    }
    shared_path = os.path.join(DATA_DIR, "epicure_shared.json")
    with open(shared_path, "w", encoding="utf-8") as f:
        json.dump(shared, f, ensure_ascii=False)
    shared_size = os.path.getsize(shared_path)
    print(f"  {shared_path} ({shared_size / 1024:.1f} KB)")

    # ── Write per-model data (large: neighbours + pca + vectors) ──
    for model_name in ["cooc", "core", "chem"]:
        data = models_data[model_name]
        print(f"\n  Writing {model_name} model data...")

        neighbour_export = []
        for nlist in data["neighbours"]:
            neighbour_export.append([[data["names"][idx], round(sim, 4)] for idx, sim in nlist])

        proj_export = [[round(x, 4), round(y, 4)] for x, y in data["proj"]]

        # Pack vectors as base64 float32
        flat = []
        for v in data["vectors"]:
            flat.extend(v)
        packed = struct.pack(f"{len(flat)}f", *flat)
        vec_b64 = base64.b64encode(packed).decode("ascii")

        model_out = {
            "neighbours": neighbour_export,
            "pca": proj_export,
            "vectorsB64": vec_b64,
            "dim": len(data["vectors"][0]),
            "n": len(data["vectors"]),
            "proj": {
                "method": "UMAP" if _UMAP_AVAILABLE else "PCA",
                "params": {
                    "metric": "cosine",
                    "n_neighbors": 15,
                    "min_dist": 0.1,
                    "random_state": 42,
                } if _UMAP_AVAILABLE else {"method": "power-iteration-PCA"},
            },
            "_metadata": {
                "preprocess_version": "2.0",
                "generated": "2026-06-07",
                "umap_version": _UMAP_VERSION,
                "sklearn_version": _SKLEARN_VERSION,
                "n_ingredients": len(data["vectors"]),
                "dim": len(data["vectors"][0]),
            },
        }

        # Attach mode atlas for this model
        if model_name in mode_atlases:
            modes_info = []
            for m in mode_atlases[model_name]["list"]:
                modes_info.append({
                    "id": m["id"],
                    "label": m["label"],
                    "kind": m["kind"],
                    "property": m["property"],
                    "n": m["n_members"],
                    "members": m["members"],
                })
            model_out["modeAtlas"] = modes_info

        out_path = os.path.join(DATA_DIR, f"epicure_{model_name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(model_out, f, ensure_ascii=False)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"    {out_path} ({size_kb:.0f} KB)")

    # Summary
    print("\n── Done! ──")
    print(f"Total ingredients: {len(all_names)}")
    print(f"Direction groups: {len(directions)}")
    proj_name = "UMAP" if _UMAP_AVAILABLE else "PCA"
    print(f"Projection:       {proj_name}")
    total_mb = shared_size / (1024 * 1024)
    for m in ["cooc", "core", "chem"]:
        fp = os.path.join(DATA_DIR, f"epicure_{m}.json")
        total_mb += os.path.getsize(fp) / (1024 * 1024)
        n_m = os.path.getsize(fp)
        print(f"  {m}: {n_m / 1024:.0f} KB")
    print(f"Total bundle:     {total_mb:.1f} MB (shared + 3 models)")


if __name__ == "__main__":
    main()
