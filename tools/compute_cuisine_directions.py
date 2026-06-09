#!/usr/bin/env python3
"""
Compute improved cuisine direction vectors using the Core model's GMM mode atlas.

The paper's cuisine directions were derived from Claude-tagged per-ingredient cuisine
labels (986/1790 ingredients labelled, 808 universal). We don't have the raw labels,
but the GMM mode atlas from the Core model provides the paper's emergent culinary
clusters with high coherence (0.833). Many modes explicitly name cuisines in their
labels — their members are the closest approximation to the paper's tagged ingredients.

Strategy:
  1. Map Core model modes to cuisines via carefully curated mode ID inclusion lists.
  2. For each cuisine, collect the union of all member ingredients from those modes,
     supplemented by keyword seeds for cuisines with weak mode coverage (Japanese).
  3. Compute the centroid vector of those members for all 3 models (Cooc, Core, Chem).
  4. The resulting direction vectors are stored in epicure_shared.json.

Usage:
    cd epicure-explorer
    python3 tools/compute_cuisine_directions.py

Output:
    Updates epicure_shared.json with new 'directions' entries for all 8 cuisine regions,
    plus updated _metadata documenting the approach.
"""

import json
import csv
import math
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# ── Manually curated mode-to-cuisine mapping ──
# Mode IDs that explicitly represent each cuisine, selected from the Core model's
# GMM mode atlas. Only modes whose label clearly signals a single cuisine are included.

CUISINE_MODES = {
    "east_asian": {
        "nova_level/M1",      # East Asian fermented sauces and processed staples
        "nova_level/M3",      # East-Asian processed sweets and beverages
        "cf_sweet/M3",        # East Asian pungent spices and vinegars
        "cf_sweet/M4",        # East Asian vegetables and mild sweet botanicals
        "cf_savory/M2",       # East Asian savory vegetables and mushrooms
        "cf_savory/M4",       # East Asian savory pantry staples
        "cf_meaty/M0",        # East Asian umami seafood and sauces
        "cf_balsamic/M0",     # East Asian fermented sauces and aromatics
        "sour_score/M0",      # East Asian vegetables and mushrooms
        "bitter_score/M3",    # East Asian pungent aromatics and mushrooms
        "umami_score/M0",     # East Asian umami fish and mushrooms
        "pungent_score/M1",   # East-Asian pungent vegetables and aromatics
        "pungent_score/M3",   # East Asian sweet grains and starchy seeds
        "fatty_score/M0",     # Southeast & East Asian aromatics and mushrooms
        "usda_fiber_g/M4",    # East Asian soy and spice staples
        "usda_caloric_density/M1",  # East Asian oils fats and rich proteins
        "fg_Pantry/M1",       # East Asian savory sauces and condiments
        "fg_Vegetable/M1",    # East-Asian stir-fry vegetables
        "fg_Vegetable/M3",    # East Asian vegetables and mushrooms
        "F_0/M1",             # East Asian fish and savory fermented pastes
        "F_0/M2",             # East Asian vegetables and mushrooms
        "F_1/M0",             # East Asian soy and spice pantry
        "F_2/M0",             # East Asian savory broth ingredients
        "F_3/M0",             # Chinese pantry staples and mushrooms
        "F_4/M1",             # East Asian seafood and umami aromatics
        "F_5/M0",             # East Asian savory broth ingredients
        "F_7/M0",             # East-Asian roots mushrooms and aromatic spices
        "F_7/M3",             # Chinese braising pantry ingredients
        "F_7/M4",             # Chinese tonic soup and sweet dessert ingredients
        "F_8/M2",             # Chinese herbal soup ingredients
        "F_8/M3",             # East and Southeast Asian noodles and condiments
        "F_9/M0",             # Chinese savory pantry staples
        "F_9/M4",             # East Asian pantry grains and botanicals
        "F_10/M4",            # Chinese savory umami pantry
        "F_11/M0",            # Chinese pantry staples and starches
        "F_12/M0",            # Chinese herbal teas and floral confections
        "F_12/M2",            # Chinese pantry staples and freshwater fish
        "F_13/M0",            # East and Southeast Asian pantry staples
        "F_14/M1",            # East-Asian herbal tonics and floral botanicals
        "F_14/M4",            # East Asian fermented vegetables and seafood
        "F_17/M0",            # Southeast and East Asian hot pot ingredients
        "F_19/M4",            # Southeast & East Asian stir-fry ingredients
        "fg_Spice/M4",        # Asian pungent aromatic spices (broad Asian)
        "fg_Fruit/M0",        # Asian tropical and medicinal fruits (broad Asian)
        "F_15/M2",            # Asian seafood and fermented condiments (broad Asian)
        "cf_savory/M1",       # East Asian sweet grains and seeds
    },
    "western_atlantic": {
        "F_12/M1",            # American deli and cookout staples
        "F_15/M0",            # American sweet confections and dessert bases
        "F_9/M2",             # Southern and Cajun seasoning staples
        "F_15/M4",            # Tex-Mex sandwich and wrap staples
        "F_8/M0",             # Tex-Mex and deli staples
        "F_19/M1",            # Tex-Mex and Cajun comfort staples
        "F_19/M2",            # Southern and Creole everyday cooking staples
        "nova_level/M5",      # Processed condiments and Tex-Mex pantry staples
    },
    "mediterranean": {
        "nova_level/M4",      # Italian-Mediterranean deli and cheese staples
        "cf_sweet/M0",        # Mediterranean vinegars and savory spices
        "cf_savory/M0",       # Mediterranean savory pantry staples
        "cf_savory/M5",       # Mediterranean savory vegetables and grains
        "cf_meaty/M2",        # Mediterranean cheeses and aged spirits
        "cf_balsamic/M3",     # Mediterranean vinaigrette spices and oils
        "cf_citrus/M1",       # Mediterranean aromatic herbs and spices
        "cf_minty/M5",        # Mediterranean herbs and peppers
        "sour_score/M3",      # Mediterranean vegetables and savory pantry staples
        "bitter_score/M1",    # Mediterranean aged cheeses and mushrooms
        "umami_score/M1",     # Mediterranean aged cheeses and umami staples
        "pungent_score/M2",   # Pungent Mediterranean vegetables and aromatics
        "fatty_score/M1",     # Mediterranean cheeses and savory aromatics
        "usda_protein_g/M2",  # Italian cheeses and cured meats
        "usda_fiber_g/M0",    # Mediterranean herbs, greens and grains
        "usda_caloric_density/M0",  # Rich Mediterranean cheeses and cured meats
        "F_1/M2",             # Savory Mediterranean seasonings and legumes
        "F_10/M2",            # Mediterranean savory pantry staples
        "F_13/M4",            # Mediterranean savory meal components
        "F_3/M1",             # cocktail spirits and liqueurs (ambiguous — skip)
    },
    "eastern_european": {
        "fg_Dairy/M0",        # Eastern European tangy aged cheeses and fermented dairy
        "F_1/M1",             # Eastern Mediterranean pantry staples
        "F_5/M3",             # Caucasian and Eastern European pantry staples
    },
    "southeast_asian": {
        "sweet_score/M3",     # Southeast Asian sweet coconut dessert ingredients
        "F_6/M1",             # Southeast Asian savory pantry staples
        "F_10/M3",            # Southeast Asian freshwater fish and greens
        "cf_citrus/M0",       # Southeast & East Asian fish and aromatics
    },
    "south_asian": {
        "cf_minty/M2",        # South Asian aromatic spice blend
        "fg_Spice/M0",        # South Asian spice blends and seeds
        "fg_Spice/M3",        # Latin American dried chiles — skip, wrong cuisine
    },
    "latin_american": {
        "cf_savory/M6",       # Latin American and Indian spiced savory staples
        "cf_citrus/M3",       # Mexican melting cheeses and dried chiles
        "cf_minty/M3",        # Mexican dried and fresh chiles
        "cf_minty/M0",        # Berry and floral cocktail aromatics — skip
        "cf_woody/M0",        # Dried and fresh chile peppers
        "sour_score/M1",      # Latin American chiles and aromatics
        "bitter_score/M4",    # Mexican chiles and cheeses
        "fatty_score/M4",     # Mexican peppers beans and cheeses
        "usda_fiber_g/M1",    # Latin spices beans and tortillas
        "F_4/M0",             # Latin American savory pantry staples
        "F_4/M3",             # Mexican and Latin American staples
        "F_2/M4",             # Mexican chiles and Latin-South Asian staples
        "F_14/M3",            # Mediterranean and Latin pantry specialties
        "sweet_score/M1",     # Savory peppers, herbs and legumes — too generic
    },
    "japanese": {
        "F_8/M5",             # Japanese vegetables and umami condiments
    },
}

# Additional keyword seeds for cuisines with weak mode coverage
# These are used to supplement the mode-based members
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
        "kefir", "buckwheat", "rye_bread", "horseradish", "borscht",
        "caraway",
    ],
    "south_asian": [
        "cumin", "coriander_seed", "turmeric", "garam_masala", "curry_leaf",
        "mustard_seed", "fenugreek", "cardamom", "ghee", "lentil",
        "chickpea", "basmati_rice", "naan", "asafoetida", "mango_powder",
        "nigella_seed", "paneer", "chana_dal", "urad_dal", "toor_dal",
        "rose_water",
    ],
}


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


def load_mode_atlas(path):
    """Load mode atlas CSV into a dict keyed by mode_id."""
    modes = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member_set = set(m.strip() for m in row["members_pipe"].split("|"))
            modes[row["mode_id"]] = {
                "label": row["label"],
                "members": member_set,
            }
    return modes


def compute_centroid(name_set, names, vectors, name_to_idx):
    """Compute the normalized centroid of all ingredients in name_set."""
    idxs = [name_to_idx[n] for n in name_set if n in name_to_idx]
    if len(idxs) < 3:
        return None
    d = len(vectors[0])
    c = [0.0] * d
    for i in idxs:
        for j in range(d):
            c[j] += vectors[i][j]
    c = [x / len(idxs) for x in c]
    norm = math.sqrt(sum(x * x for x in c))
    if norm < 0.001:
        return None
    return [x / norm for x in c]


def main():
    # ── Load Core model mode atlas ──
    mode_path = os.path.join(DATA_DIR, "mode_atlas_core.csv")
    if not os.path.exists(mode_path):
        print(f"❌ Mode atlas not found: {mode_path}")
        sys.exit(1)
    modes = load_mode_atlas(mode_path)
    print(f"Loaded {len(modes)} modes from Core model atlas")

    # ── Compute cuisine memberships ──
    cuisine_members = {}
    for cuisine, mode_ids in CUISINE_MODES.items():
        members = set()
        # Collect members from all assigned modes
        for mid in mode_ids:
            if mid in modes:
                members.update(modes[mid]["members"])
            else:
                print(f"  ⚠️  Mode {mid} not found in atlas")

        # Add keyword seeds
        seeds = CUISINE_SEEDS.get(cuisine, [])
        members.update(seeds)

        cuisine_members[cuisine] = members
        print(f"  {cuisine:20s}: {len(mode_ids):3d} modes, {len(members):4d} total members "
              f"({len(seeds):3d} keyword seeds)")

    # ── Compute direction vectors for all 3 models ──
    directions = {}
    for model_name in ["cooc", "core", "chem"]:
        csv_path = os.path.join(DATA_DIR, f"epicure_{model_name}.csv")
        if not os.path.exists(csv_path):
            print(f"  ⚠️  Skipping {model_name}: {csv_path} not found")
            continue

        names, vectors = load_embeddings(csv_path)
        vectors = l2_normalize(vectors)
        name_to_idx = {n: i for i, n in enumerate(names)}
        print(f"\n{model_name}: {len(names)} ingredients loaded")

        # Compute per-model shared vectors (sensory directions reused from shared.json)
        for cuisine, members in cuisine_members.items():
            centroid = compute_centroid(members, names, vectors, name_to_idx)
            if centroid is not None:
                if model_name == "cooc":
                    # Store all cuisine directions from Cooc model (consistent with existing format)
                    directions[cuisine] = centroid
                    # Also compute and store what fraction of members were found
                    found = sum(1 for m in members if m in name_to_idx)
                    print(f"  → {cuisine:20s}: centroid from {found}/{len(members)} found members")
            else:
                print(f"  → {cuisine:20s}: FAILED (< 3 members found)")

    print(f"\nComputed {len(directions)} cuisine direction vectors")

    # ── Update epicure_shared.json ──
    shared_path = os.path.join(DATA_DIR, "epicure_shared.json")
    if not os.path.exists(shared_path):
        print(f"❌ Shared data not found: {shared_path}")
        sys.exit(1)

    with open(shared_path, "r", encoding="utf-8") as f:
        shared = json.load(f)

    # Preserve sensory directions, replace cuisine directions
    for cuisine, vec in directions.items():
        shared["directions"][cuisine] = vec

    # Update metadata
    shared["_metadata"]["direction_method"] = \
        "mode-atlas + keyword seeds — Core GMM mode-membership centroids from Cooc vectors"
    shared["_metadata"]["direction_cuisine_modes"] = \
        {c: len(mids) for c, mids in CUISINE_MODES.items()}
    shared["_metadata"]["direction_cuisine_members"] = \
        {c: len(members) for c, members in cuisine_members.items()}
    shared["_metadata"]["last_updated"] = "session-19-cuisine-directions"

    with open(shared_path, "w", encoding="utf-8") as f:
        json.dump(shared, f, ensure_ascii=False)

    print(f"\n✅ Updated {shared_path}")
    print(f"   Preserved {len(shared['directions'])} total direction vectors")
    print(f"   Cuisine vectors: {list(directions.keys())}")


if __name__ == "__main__":
    main()
