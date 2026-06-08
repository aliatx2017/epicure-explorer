"""
Build comprehensive nutritional data for Epicure Explorer,
following the im2recipe-Pytorch format (MIT-licensed).

Outputs:
  data/epicure_nutrition.json   — Per-ingredient nutrition with FSA traffic lights
  data/nutrition_vocab.json     — Vocabulary bridge (im2recipe ↔ Epicure names)

The im2recipe-Pytorch format includes:
  - nutr_values_per100g: {energy, fat, protein, salt, saturates, sugars}
  - fsa_lights_per100g: {fat, salt, saturates, sugars}  → "green"/"orange"/"red"
  - nutr_per_ingredient: {nrg, pro, fat, sat, sug, sod}

Usage:
    python3 build_nutrition.py
"""
import json
import csv
import os
import math

DATA_DIR = "data"

# ── USDA-based nutrition data [calories, protein_g, fat_g, carbs_g, fiber_g, saturates_g, sugars_g, sodium_mg] ──
# One entry per 100g. Source: USDA FoodData Central + im2recipe-Pytorch format.
# Format: name -> [energy_kcal, protein_g, fat_g, carbs_g, fiber_g, saturates_g, sugars_g, sodium_mg]
NUTRITION_DB = {
    # Meat & Poultry
    "chicken_breast": [165, 31, 3.6, 0, 0, 1.0, 0, 74],
    "chicken_thigh": [209, 26, 11, 0, 0, 3.1, 0, 86],
    "chicken_wings": [222, 25, 14, 0, 0, 4.0, 0, 82],
    "chicken_liver": [119, 17, 4.8, 0.9, 0, 1.6, 0, 71],
    "chicken": [190, 27, 8, 0, 0, 2.3, 0, 78],
    "turkey": [189, 29, 7, 0, 0, 2.0, 0, 90],
    "duck": [337, 19, 28, 0, 0, 9.7, 0, 74],
    "goose": [371, 24, 30, 0, 0, 9.8, 0, 84],
    "beef": [250, 26, 15, 0, 0, 5.9, 0, 72],
    "beef_tenderloin": [230, 24, 14, 0, 0, 5.5, 0, 60],
    "beef_rib": [290, 22, 22, 0, 0, 8.7, 0, 67],
    "beef_liver": [135, 20, 3.6, 5, 0, 1.2, 0, 70],
    "beef_steak": [271, 26, 18, 0, 0, 7.1, 0, 65],
    "beef_ground": [252, 24, 17, 0, 0, 6.7, 0, 75],
    "bison": [143, 28, 2.4, 0, 0, 0.9, 0, 55],
    "pork": [242, 27, 14, 0, 0, 5.0, 0, 62],
    "pork_loin": [200, 24, 11, 0, 0, 3.9, 0, 57],
    "pork_belly": [518, 9, 53, 0, 0, 19.3, 0, 48],
    "pork_shoulder": [250, 22, 17, 0, 0, 6.0, 0, 70],
    "pork_liver": [134, 21, 3.7, 3, 0, 1.2, 0, 70],
    "pork_rib": [260, 22, 19, 0, 0, 6.8, 0, 65],
    "pork_sausage": [320, 18, 27, 1, 0, 9.5, 0, 720],
    "lamb": [258, 25, 17, 0, 0, 7.2, 0, 72],
    "lamb_rib": [300, 20, 24, 0, 0, 10.1, 0, 68],
    "lamb_shoulder": [280, 23, 20, 0, 0, 8.5, 0, 70],
    "venison": [158, 30, 3.2, 0, 0, 1.4, 0, 54],
    "goat": [143, 27, 3, 0, 0, 0.9, 0, 82],
    "rabbit": [173, 20, 10, 0, 0, 4.0, 0, 42],
    "bacon": [541, 37, 42, 1.4, 0, 14.0, 0, 1717],
    "ham": [145, 20, 5, 1.5, 0, 1.7, 0, 1200],
    "prosciutto": [200, 27, 10, 0, 0, 3.3, 0, 1900],
    "salami": [350, 22, 28, 1.5, 0, 10.0, 0, 1800],
    "pepperoni": [494, 23, 44, 1.2, 0, 15.6, 0, 1900],
    "chorizo": [455, 24, 38, 2, 0, 14.0, 0, 1500],
    "sausage": [300, 15, 26, 2, 0, 9.0, 0, 800],
    "mortadella": [311, 16, 26, 2, 0, 9.2, 0, 1400],
    "pate": [319, 14, 28, 2, 0, 10.0, 0, 750],
    "hot_dog": [290, 11, 26, 3, 0, 9.5, 0, 1100],
    "corned_beef": [250, 22, 17, 0.5, 0, 6.0, 0, 1300],
    "pastrami": [240, 20, 16, 1, 0, 5.7, 0, 1400],
    "spam": [320, 13, 28, 2, 0, 10.0, 0, 1300],
    "meatball": [260, 18, 20, 3, 0, 7.0, 0, 600],
    "meatloaf": [230, 16, 17, 5, 0, 6.0, 0, 550],
    "liverwurst": [305, 14, 26, 3, 0, 9.0, 0, 800],

    # Fish & Seafood
    "salmon": [208, 20, 13, 0, 0, 3.1, 0, 59],
    "smoked_salmon": [117, 18, 4, 0, 0, 0.9, 0, 1880],
    "tuna": [132, 28, 1.3, 0, 0, 0.3, 0, 40],
    "cod": [82, 18, 0.7, 0, 0, 0.1, 0, 74],
    "sardine": [208, 25, 11, 0, 0, 2.4, 0, 307],
    "anchovy": [131, 20, 4.8, 0, 0, 1.2, 0, 3750],
    "mackerel": [262, 19, 20, 0, 0, 4.8, 0, 90],
    "trout": [190, 20, 12, 0, 0, 2.3, 0, 51],
    "halibut": [111, 19, 2.3, 0, 0, 0.3, 0, 61],
    "tilapia": [96, 20, 1.7, 0, 0, 0.4, 0, 52],
    "shrimp": [99, 24, 0.3, 0.2, 0, 0.1, 0, 148],
    "prawn": [99, 24, 0.3, 0.2, 0, 0.1, 0, 148],
    "crab": [87, 18, 0.9, 0, 0, 0.2, 0, 294],
    "crab_stick": [95, 8, 1, 15, 0, 0.2, 6, 700],
    "lobster": [89, 19, 0.9, 0, 0, 0.2, 0, 296],
    "octopus": [164, 30, 4, 4, 0, 0.8, 0, 460],
    "squid": [92, 15, 1.4, 3, 0, 0.4, 0, 44],
    "clam": [148, 25, 1.9, 5, 0, 0.2, 0, 1202],
    "mussel": [172, 24, 4.5, 7, 0, 0.8, 0, 369],
    "oyster": [81, 9, 2.3, 5, 0, 0.5, 0, 417],
    "scallop": [111, 20, 0.8, 5, 0, 0.1, 0, 392],
    "roe": [250, 25, 16, 1.5, 0, 3.5, 0, 100],
    "caviar": [264, 24, 18, 4, 0, 4.0, 0, 1500],
    "uni": [134, 12, 8, 3, 0, 1.5, 0, 120],
    "surimi": [95, 15, 0.9, 6, 0, 0.2, 3, 500],
    "fish_sauce": [35, 5, 0, 4, 0, 0, 4, 5800],
    "eel": [236, 20, 16, 0, 0, 4.0, 0, 65],
    "sea_bass": [124, 22, 3.6, 0, 0, 0.8, 0, 57],
    "red_snapper": [128, 23, 3.6, 0, 0, 0.8, 0, 56],
    "catfish": [135, 18, 6.8, 0, 0, 1.6, 0, 50],
    "turbot": [95, 19, 2.0, 0, 0, 0.4, 0, 60],
    "monkfish": [82, 16, 1.8, 0, 0, 0.3, 0, 52],
    "swordfish": [144, 21, 6.7, 0, 0, 1.6, 0, 60],
    "yellowtail": [195, 23, 11, 0, 0, 2.8, 0, 58],
    "toro": [310, 18, 26, 0, 0, 6.0, 0, 40],

    # Dairy
    "milk": [42, 3.4, 1, 5, 0, 0.6, 5, 44],
    "whole_milk": [61, 3.2, 3.3, 4.8, 0, 2.1, 5, 43],
    "skim_milk": [34, 3.4, 0.1, 5, 0, 0.1, 5, 42],
    "buttermilk": [40, 3.3, 0.9, 4.8, 0, 0.5, 5, 52],
    "half_and_half": [131, 3, 11, 4, 0, 7.0, 4, 61],
    "heavy_cream": [340, 2.8, 36, 3, 0, 22.0, 3, 38],
    "whipping_cream": [340, 2.8, 36, 3, 0, 22.0, 3, 38],
    "sour_cream": [198, 2.4, 19, 4.6, 0, 12.0, 4, 40],
    "creme_fraiche": [343, 2.8, 36, 3, 0, 22.0, 3, 38],
    "clotted_cream": [586, 2.0, 63, 3, 0, 40.0, 3, 30],
    "yogurt": [59, 10, 0.4, 3.6, 0, 0.2, 3.6, 37],
    "greek_yogurt": [97, 16, 0.7, 3.6, 0, 0.4, 3.6, 45],
    "kefir": [61, 3.5, 0.9, 7, 0, 0.5, 7, 52],
    "lassi": [80, 2.5, 1.5, 14, 0, 0.9, 14, 40],
    "ayran": [35, 2.5, 1, 3, 0, 0.6, 3, 55],
    "butter": [717, 0.9, 81, 0.1, 0, 52.0, 0.1, 643],
    "ghee": [876, 0, 99, 0, 0, 62.0, 0, 0],
    "egg": [155, 13, 11, 1.1, 0, 3.3, 1.1, 124],
    "egg_white": [52, 11, 0.2, 0.7, 0, 0, 0.7, 166],
    "egg_yolk": [322, 16, 27, 3.6, 0, 8.0, 3.6, 48],
    "cheese": [402, 25, 33, 1.3, 0, 21.0, 0.5, 620],
    "cottage_cheese": [98, 11, 4.3, 3.4, 0, 2.8, 2.8, 364],
    "cream_cheese": [342, 6, 34, 4, 0, 21.0, 3, 320],
    "mascarpone": [435, 7, 45, 4, 0, 28.0, 3, 40],
    "mozzarella": [280, 28, 17, 3.1, 0, 10.0, 1, 619],
    "parmesan_cheese": [431, 38, 29, 4.1, 0, 17.0, 1, 1376],
    "cheddar": [403, 25, 33, 1.3, 0, 21.0, 0.5, 621],
    "swiss_cheese": [380, 27, 29, 1.3, 0, 17.0, 0.5, 187],
    "gouda": [356, 25, 28, 2.2, 0, 17.0, 2, 750],
    "brie": [334, 21, 28, 0.5, 0, 18.0, 0.5, 629],
    "camembert": [300, 20, 24, 0.5, 0, 15.0, 0.5, 842],
    "blue_cheese": [353, 21, 29, 2.3, 0, 18.0, 0.5, 1395],
    "feta": [264, 14, 21, 4, 0, 15.0, 4, 1116],
    "goat_cheese": [264, 20, 21, 1, 0, 14.0, 1, 350],
    "ricotta": [174, 11, 13, 3, 0, 8.0, 3, 105],
    "provolone": [351, 26, 27, 0.6, 0, 17.0, 0.6, 728],
    "havarti": [352, 22, 28, 0.6, 0, 17.0, 0.6, 700],
    "gruyere": [413, 29, 32, 0.4, 0, 19.0, 0.4, 336],
    "pecorino": [428, 36, 29, 3, 0, 19.0, 1, 1400],
    "manchego": [395, 25, 32, 1, 0, 20.0, 0.5, 800],
    "asiago": [390, 25, 31, 2, 0, 19.0, 0.5, 700],
    "gorgonzola": [353, 21, 29, 2, 0, 18.0, 0.5, 1395],
    "stilton": [353, 21, 29, 2, 0, 18.0, 0.5, 1200],
    "paneer": [321, 18, 26, 3, 0, 16.0, 3, 20],
    "queso_fresco": [276, 19, 22, 3, 0, 14.0, 3, 400],
    "neufchatel": [253, 9, 23, 3, 0, 14.0, 3, 365],
    "processed_cheese": [330, 20, 26, 4, 0, 16.0, 3, 1200],
    "condensed_milk": [321, 8, 9, 54, 0, 5.5, 54, 127],
    "evaporated_milk": [134, 7, 7.6, 10, 0, 4.6, 10, 106],

    # Legumes & Soy
    "tofu": [76, 8, 4.8, 1.9, 0.3, 0.7, 0.7, 7],
    "tempeh": [193, 19, 11, 9, 0, 2.2, 7, 9],
    "edamame": [122, 12, 5, 9, 5.2, 0.6, 2.5, 6],
    "natto": [211, 18, 11, 14, 5.4, 1.6, 6, 7],
    "miso": [199, 12, 6, 26, 5.4, 1.4, 13, 3728],
    "soy_sauce": [53, 8, 0.1, 5, 0.8, 0, 0.8, 5493],
    "tamari": [66, 10, 0.1, 6, 0.5, 0, 0.5, 5000],
    "soy_milk": [54, 3.3, 1.8, 6, 0.6, 0.2, 3, 51],
    "lentil": [116, 9, 0.4, 20, 8, 0.1, 1.8, 2],
    "chickpea": [139, 7.6, 2.6, 23, 7.6, 0.3, 4.8, 7],
    "hummus": [166, 8, 9.5, 14, 4, 1.4, 0.5, 379],
    "black_bean": [132, 8.9, 0.5, 24, 8.7, 0.1, 0.3, 2],
    "kidney_bean": [127, 8.7, 0.5, 23, 7.4, 0.1, 0.3, 2],
    "pinto_bean": [143, 9, 0.7, 27, 9, 0.1, 0.4, 2],
    "white_bean": [139, 9, 0.4, 25, 6.3, 0.1, 0.3, 6],
    "mung_bean": [127, 8.7, 0.4, 23, 7.6, 0.1, 2, 2],
    "fava_bean": [106, 7.6, 0.4, 20, 5.4, 0.1, 1.5, 2],
    "adzuki_bean": [128, 7.5, 0.1, 25, 7.5, 0, 0.5, 3],
    "soybean": [172, 16, 9, 10, 6, 1.3, 3, 1],
    "tofu_skin": [160, 15, 10, 3, 0, 1.5, 0.5, 10],

    # Vegetables
    "broccoli": [34, 2.8, 0.4, 7, 2.6, 0.1, 1.7, 33],
    "spinach": [23, 2.9, 0.4, 3.6, 2.2, 0.1, 0.4, 79],
    "kale": [49, 4.3, 0.9, 9, 3.6, 0.1, 1.5, 43],
    "cauliflower": [25, 1.9, 0.3, 5, 2, 0.1, 2.4, 30],
    "cabbage": [25, 1.3, 0.1, 6, 2.5, 0, 3.2, 18],
    "bok_choy": [13, 1.5, 0.2, 2.2, 1, 0, 1.2, 65],
    "napa_cabbage": [12, 1.1, 0.2, 2.2, 1, 0, 1.2, 11],
    "brussels_sprout": [43, 3.4, 0.3, 9, 3.8, 0.1, 2.2, 25],
    "swiss_chard": [19, 1.8, 0.2, 3.7, 1.6, 0, 1.1, 213],
    "collard_green": [32, 3, 0.6, 5.5, 4, 0.1, 0.5, 17],
    "mustard_green": [27, 2.9, 0.4, 4.7, 3.2, 0, 1.4, 25],
    "arugula": [25, 2.6, 0.7, 3.7, 1.6, 0.1, 2.1, 27],
    "watercress": [11, 2.3, 0.1, 1.3, 0.5, 0, 0.4, 41],
    "lettuce": [15, 1.4, 0.2, 2.9, 1.3, 0, 1.2, 28],
    "romaine": [17, 1.2, 0.3, 3.3, 2.1, 0, 1.2, 8],
    "iceberg": [14, 0.9, 0.1, 3, 1.2, 0, 2, 10],
    "endive": [17, 1.3, 0.2, 3.4, 3.1, 0, 0.3, 22],
    "carrot": [41, 0.9, 0.2, 10, 2.8, 0, 4.7, 69],
    "celery": [16, 0.7, 0.2, 3, 1.6, 0, 1.4, 80],
    "celery_root": [42, 1.5, 0.3, 9, 1.8, 0.1, 1.5, 100],
    "tomato": [18, 0.9, 0.2, 3.9, 1.2, 0, 2.6, 5],
    "cherry_tomato": [18, 0.9, 0.2, 3.9, 1.2, 0, 2.6, 5],
    "cucumber": [15, 0.7, 0.1, 3.6, 0.5, 0, 1.7, 2],
    "zucchini": [17, 1.2, 0.3, 3.1, 1, 0.1, 2.5, 8],
    "yellow_squash": [16, 1.2, 0.2, 3, 1, 0, 2, 3],
    "eggplant": [25, 1, 0.2, 6, 3, 0, 3.5, 2],
    "bell_pepper": [26, 1, 0.2, 6, 2.1, 0, 3.9, 2],
    "chili_pepper": [40, 2, 0.2, 9, 1.5, 0, 5.3, 9],
    "jalapeno": [29, 0.9, 0.4, 6, 2.8, 0, 4.1, 3],
    "habanero": [40, 2, 0.4, 9, 1.5, 0, 5.3, 7],
    "poblano": [25, 1.2, 0.3, 5, 1.9, 0, 2.5, 5],
    "serrano": [32, 1.7, 0.4, 7, 1.6, 0, 3.8, 10],
    "ancho_chile": [282, 12, 14, 50, 29, 2.5, 30, 60],
    "chipotle": [282, 12, 14, 50, 29, 2.5, 30, 60],
    "guajillo_chile": [282, 12, 14, 50, 29, 2.5, 30, 60],
    "onion": [40, 1.1, 0.1, 9, 1.7, 0, 4.7, 4],
    "red_onion": [40, 1.1, 0.1, 9, 1.7, 0, 4.7, 4],
    "sweet_onion": [40, 1.1, 0.1, 9, 1.7, 0, 4.7, 4],
    "white_onion": [40, 1.1, 0.1, 9, 1.7, 0, 4.7, 4],
    "garlic": [149, 6.4, 0.5, 33, 2.1, 0.1, 1, 17],
    "leek": [61, 1.5, 0.3, 14, 1.8, 0, 3.9, 20],
    "shallot": [72, 2.5, 0.1, 17, 3.2, 0, 8, 12],
    "scallion": [32, 1.8, 0.2, 7, 2.6, 0, 2.3, 16],
    "chive": [30, 3.3, 0.7, 4.4, 2.5, 0.1, 1.9, 3],
    "mushroom": [22, 3.1, 0.3, 3.3, 1, 0, 2, 5],
    "portobello": [22, 3.1, 0.3, 3.3, 1, 0, 2, 5],
    "shiitake": [34, 2.2, 0.5, 7, 2.5, 0.1, 2.4, 9],
    "enoki": [37, 2.7, 0.3, 8, 3.5, 0, 0.2, 3],
    "oyster_mushroom": [33, 2.8, 0.4, 6, 2.3, 0.1, 1.1, 5],
    "maitake": [31, 1.9, 0.2, 7, 2.7, 0, 2, 1],
    "king_oyster_mushroom": [33, 2.8, 0.4, 6, 2.3, 0, 2, 5],
    "wood_ear": [28, 1.0, 0.2, 7, 5, 0, 1, 15],
    "asparagus": [20, 2.2, 0.1, 3.9, 2.1, 0, 1.9, 2],
    "green_bean": [31, 1.8, 0.1, 7, 2.7, 0, 3.3, 6],
    "snow_pea": [42, 2.8, 0.2, 7.5, 2.6, 0, 4, 5],
    "sugar_snap_pea": [42, 2.8, 0.2, 8, 2.6, 0, 4, 5],
    "pea": [81, 5.4, 0.4, 14, 5.7, 0.1, 5.9, 3],
    "corn": [86, 3.3, 1.4, 19, 2.7, 0.2, 3.2, 15],
    "sweet_corn": [86, 3.3, 1.4, 19, 2.7, 0.2, 3.2, 15],
    "potato": [77, 2, 0.1, 17, 2.2, 0, 0.8, 6],
    "sweet_potato": [86, 1.6, 0.1, 20, 3, 0, 4.2, 55],
    "yam": [118, 1.5, 0.1, 28, 4.1, 0, 0.5, 9],
    "taro": [112, 1.5, 0.1, 26, 4.1, 0, 0.4, 11],
    "cassava": [160, 1.4, 0.3, 38, 1.8, 0.1, 1.7, 14],
    "avocado": [160, 2, 15, 8.5, 6.7, 2.1, 0.7, 7],
    "beet": [43, 1.6, 0.2, 10, 2.8, 0, 6.8, 78],
    "radish": [16, 0.7, 0.1, 3.4, 1.6, 0, 1.9, 39],
    "daikon": [18, 0.6, 0.1, 4.1, 1.6, 0, 2.5, 21],
    "turnip": [28, 0.9, 0.1, 6.4, 1.8, 0, 3.8, 67],
    "rutabaga": [37, 1.1, 0.2, 9, 2.3, 0, 6, 20],
    "kohlrabi": [27, 1.7, 0.1, 6.2, 3.6, 0, 2.6, 20],
    "jicama": [38, 0.7, 0.1, 9, 4.9, 0, 1.8, 4],
    "artichoke": [85, 3.3, 0.6, 18, 9.8, 0.1, 2, 120],
    "fennel": [31, 1.2, 0.2, 7, 3.1, 0, 3.9, 52],
    "pumpkin": [26, 1, 0.1, 7, 0.5, 0.1, 2.8, 1],
    "squash": [34, 1.4, 0.2, 8, 2.5, 0, 3.5, 3],
    "butternut_squash": [45, 1, 0.1, 12, 2, 0, 2.2, 4],
    "acorn_squash": [40, 0.8, 0.1, 10, 1.5, 0, 4, 4],
    "spaghetti_squash": [31, 0.7, 0.6, 7, 1.5, 0.1, 2.8, 17],
    "okra": [33, 2, 0.1, 7, 3.2, 0, 1.5, 7],
    "rhubarb": [21, 0.9, 0.2, 4.5, 1.8, 0, 1.1, 4],
    "horseradish_root": [48, 1.2, 0.7, 11, 3.3, 0.1, 6, 420],
    "water_chestnut": [97, 1.4, 0.1, 23, 3, 0, 4.8, 14],
    "bamboo_shoot": [27, 2.6, 0.3, 5, 2.2, 0.1, 3, 4],
    "heart_of_palm": [115, 2.7, 0.2, 27, 1.6, 0, 17, 200],
    "seaweed": [43, 4.6, 0.7, 9, 1.3, 0.2, 0.5, 230],
    "nori": [35, 5.8, 0.3, 5, 0.3, 0, 0.5, 240],
    "kombu": [60, 5.5, 0.9, 11, 3, 0.1, 1, 180],
    "wakame": [45, 3.0, 0.6, 9, 0.5, 0.1, 1, 870],
    "nopal": [16, 1.3, 0.1, 3.3, 2, 0, 1.1, 15],

    # Fruits
    "apple": [52, 0.3, 0.2, 14, 2.4, 0, 10, 1],
    "pear": [57, 0.4, 0.1, 15, 3.1, 0, 10, 1],
    "quince": [57, 0.4, 0.1, 15, 1.9, 0, 11, 4],
    "banana": [89, 1.1, 0.3, 23, 2.6, 0.1, 12, 1],
    "plantain": [122, 1.3, 0.4, 32, 2.3, 0.1, 15, 4],
    "orange": [47, 0.9, 0.1, 12, 2.4, 0, 9, 0],
    "lemon": [29, 1.1, 0.3, 9, 2.8, 0, 2.5, 2],
    "lime": [30, 0.7, 0.2, 11, 2.8, 0, 1.7, 2],
    "grapefruit": [42, 0.8, 0.1, 11, 1.6, 0, 7, 0],
    "clementine": [47, 0.9, 0.1, 12, 1.7, 0, 9, 1],
    "tangerine": [53, 0.8, 0.3, 13, 1.8, 0, 11, 2],
    "yuzu": [30, 0.8, 0.2, 11, 2.8, 0, 2.5, 2],
    "strawberry": [32, 0.7, 0.3, 8, 2, 0, 4.9, 1],
    "blueberry": [57, 0.7, 0.3, 14, 2.4, 0, 10, 1],
    "raspberry": [52, 1.2, 0.7, 12, 6.5, 0, 4.4, 1],
    "blackberry": [43, 1.4, 0.5, 10, 5.3, 0, 4.9, 1],
    "cranberry": [46, 0.4, 0.1, 12, 4.6, 0, 4, 2],
    "grape": [69, 0.7, 0.2, 18, 0.9, 0.1, 16, 2],
    "raisin": [299, 3.1, 0.5, 79, 3.7, 0.1, 59, 11],
    "cherry": [50, 1, 0.3, 12, 1.6, 0.1, 8, 0],
    "peach": [39, 0.9, 0.3, 10, 1.5, 0, 8, 0],
    "nectarine": [44, 1.1, 0.3, 11, 1.7, 0, 8, 0],
    "plum": [46, 0.7, 0.3, 11, 1.4, 0, 10, 0],
    "apricot": [48, 1.4, 0.4, 11, 2, 0, 9, 1],
    "mango": [60, 0.8, 0.4, 15, 1.6, 0.1, 14, 1],
    "papaya": [43, 0.5, 0.3, 11, 1.7, 0.1, 8, 3],
    "pineapple": [50, 0.5, 0.1, 13, 1.4, 0, 10, 1],
    "kiwi": [61, 1.1, 0.5, 15, 3, 0, 9, 2],
    "watermelon": [30, 0.6, 0.2, 8, 0.4, 0, 6, 1],
    "cantaloupe": [34, 0.8, 0.2, 8, 0.9, 0, 8, 16],
    "honeydew": [36, 0.5, 0.1, 9, 0.8, 0, 8, 18],
    "pomegranate": [83, 1.7, 1.2, 18, 4, 0.1, 14, 3],
    "persimmon": [81, 0.6, 0.2, 22, 3.6, 0, 13, 1],
    "fig": [74, 0.8, 0.3, 19, 2.9, 0, 16, 1],
    "date": [282, 2.5, 0.4, 75, 8, 0, 63, 1],
    "coconut": [354, 3.3, 33, 15, 9, 29, 7, 20],
    "coconut_milk": [230, 2.3, 24, 5.5, 2.2, 21, 3, 15],
    "coconut_cream": [330, 3.5, 34, 7, 3, 30, 3, 12],
    "olive": [115, 0.8, 11, 6, 3.2, 1.4, 0.5, 735],
    "medjool_date": [282, 2.5, 0.4, 75, 8, 0, 63, 1],
    "dried_fig": [250, 3.3, 1, 63, 10, 0.1, 48, 11],
    "dried_apricot": [241, 3.4, 0.5, 63, 7.3, 0, 53, 10],
    "prune": [240, 2.2, 0.4, 63, 7, 0, 38, 3],
    "goji_berry": [349, 14, 0.4, 77, 13, 0, 45, 10],
    "acai": [60, 0.8, 4, 7, 2.5, 1.2, 3, 7],

    # Grains
    "rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "white_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "jasmine_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "basmati_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "arborio_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "sushi_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "brown_rice": [111, 2.6, 0.9, 23, 1.8, 0.2, 0.4, 5],
    "wild_rice": [101, 4, 0.3, 21, 1.8, 0.1, 0.7, 3],
    "red_rice": [110, 2.5, 0.8, 23, 1.8, 0.2, 0.4, 4],
    "risotto_rice": [130, 2.7, 0.3, 28, 0.4, 0.1, 0.1, 1],
    "quinoa": [120, 4.4, 1.9, 21, 2.8, 0.2, 0.9, 7],
    "red_quinoa": [120, 4.4, 1.9, 21, 2.8, 0.2, 0.9, 7],
    "black_quinoa": [120, 4.4, 1.9, 21, 2.8, 0.2, 0.9, 7],
    "couscous": [112, 3.8, 0.2, 23, 1.4, 0, 0, 5],
    "bulgur": [83, 3.1, 0.2, 19, 4.5, 0, 0.2, 6],
    "farro": [150, 5, 1, 30, 5, 0.2, 0.5, 5],
    "spelt": [150, 5.5, 1.2, 30, 4.5, 0.2, 0.5, 5],
    "barley": [123, 2.3, 0.4, 28, 3.8, 0.1, 0.3, 9],
    "oat": [389, 17, 7, 66, 10.6, 1.2, 1, 2],
    "rolled_oat": [389, 17, 7, 66, 10.6, 1.2, 1, 2],
    "steel_cut_oat": [389, 17, 7, 66, 10.6, 1.2, 1, 2],
    "oatmeal": [71, 2.5, 1.5, 12, 1.7, 0.3, 0.5, 2],
    "muesli": [370, 10, 5, 75, 7, 1.0, 15, 20],
    "granola": [471, 10, 20, 64, 6, 3.5, 20, 25],
    "buckwheat": [143, 6, 0.8, 33, 2.7, 0.2, 0.8, 1],
    "amaranth": [371, 14, 7, 65, 7, 1.5, 1.5, 4],
    "millet": [119, 3.5, 1, 23, 1.3, 0.2, 0.1, 2],
    "teff": [101, 3.9, 0.7, 20, 2.8, 0.1, 0.5, 4],
    "sorghum": [339, 11, 3.4, 72, 6, 0.6, 3, 2],
    "pasta": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "spaghetti": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "fettuccine": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "penne": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "lasagna": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "angel_hair_pasta": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "linguine": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "rigatoni": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "macaroni": [131, 5, 1.1, 25, 1.8, 0.2, 0.6, 1],
    "soba": [99, 5, 0.1, 21, 1.5, 0, 0.4, 60],
    "udon": [110, 3.2, 0.4, 23, 1.3, 0.1, 0.5, 180],
    "ramen": [138, 4.5, 1.9, 24, 1.1, 0.7, 0.5, 450],
    "rice_noodle": [105, 0.8, 0.1, 24, 0.5, 0, 0, 5],
    "glass_noodle": [351, 0.1, 0, 86, 0.5, 0, 0, 5],
    "egg_noodle": [138, 4.5, 2.1, 25, 1, 0.5, 0.5, 15],
    "bread": [265, 9, 3.2, 49, 2.7, 0.7, 5, 490],
    "white_bread": [265, 8, 3.2, 49, 2, 0.7, 5, 491],
    "whole_wheat_bread": [247, 13, 3.4, 41, 5, 0.6, 5, 400],
    "rye_bread": [259, 8.5, 3.3, 48, 5.8, 0.5, 4, 600],
    "sourdough_bread": [266, 8, 3.5, 50, 2.5, 0.7, 5, 480],
    "pita_bread": [275, 9, 2.6, 55, 2.2, 0.4, 1, 400],
    "naan": [262, 8, 6, 44, 2, 2.5, 3, 500],
    "tortilla": [300, 7, 7, 51, 4, 2.5, 3, 550],
    "corn_tortilla": [218, 5, 2.5, 44, 4.5, 0.5, 1, 45],
    "flour_tortilla": [300, 7, 7, 51, 2, 2.5, 3, 550],
    "lavash": [270, 8, 3, 53, 2, 0.5, 2, 420],
    "bagel": [250, 10, 1.5, 48, 2, 0.3, 6, 430],
    "croissant": [406, 8, 21, 46, 2, 12, 11, 380],
    "pizza_dough": [260, 8, 4, 48, 2, 0.8, 2, 450],
    "pie_crust": [520, 6, 35, 46, 1, 12, 1, 350],
    "flour": [364, 10, 1, 76, 2.7, 0.2, 0.3, 2],
    "bread_crumb": [395, 13, 5, 73, 4.5, 1.2, 6, 650],
    "panko": [357, 11, 3, 75, 4, 0.8, 5, 580],
    "crouton": [465, 8, 18, 63, 3, 4, 5, 700],
    "cornmeal": [370, 8, 3.7, 79, 3.5, 0.5, 0.5, 35],
    "polenta": [71, 1.6, 0.4, 16, 0.5, 0.1, 0.2, 2],
    "rice_flour": [366, 6, 1.4, 80, 2.4, 0.4, 0.1, 0],
    "coconut_flour": [443, 19, 16, 65, 38, 15, 8, 40],
    "almond_flour": [590, 21, 54, 20, 11, 4.1, 4, 1],

    # Nuts & Seeds
    "almond": [579, 21, 50, 22, 12.5, 3.8, 4.4, 1],
    "almond_milk": [17, 0.6, 1.1, 0.8, 0.3, 0.1, 0.6, 72],
    "almond_butter": [614, 21, 56, 19, 10, 4.3, 4, 7],
    "walnut": [654, 15, 65, 14, 6.7, 6.1, 2.6, 2],
    "pecan": [691, 9, 72, 14, 9.6, 6.2, 4, 0],
    "cashew": [553, 18, 44, 30, 3.3, 7.8, 6, 12],
    "cashew_milk": [20, 0.5, 1.5, 1, 0.2, 0.3, 0.5, 50],
    "pistachio": [560, 20, 45, 27, 10.6, 5.4, 7.7, 1],
    "peanut": [567, 26, 49, 16, 8.5, 6.8, 4.7, 6],
    "peanut_butter": [597, 24, 51, 22, 5.5, 7.2, 10, 459],
    "hazelnut": [628, 15, 61, 17, 9.7, 4.5, 4.3, 0],
    "macadamia": [718, 8, 76, 14, 8.6, 12, 4.6, 5],
    "brazil_nut": [659, 14, 67, 12, 7.5, 16, 2.4, 2],
    "chestnut": [245, 3.2, 2.2, 53, 5.1, 0.4, 11, 2],
    "pine_nut": [673, 14, 68, 13, 3.7, 4.9, 3.6, 2],
    "chia_seed": [486, 17, 31, 42, 34.4, 3.3, 0, 16],
    "flaxseed": [534, 18, 42, 29, 27.3, 3.7, 1.6, 30],
    "hemp_seed": [533, 32, 46, 6, 2, 3.5, 1.5, 5],
    "pumpkin_seed": [559, 30, 49, 11, 6, 8.6, 1.4, 7],
    "sunflower_seed": [584, 21, 51, 20, 8.6, 4.5, 2.6, 9],
    "sesame_seed": [573, 18, 50, 23, 11.8, 7, 0.3, 11],
    "tahini": [595, 17, 54, 21, 9.2, 7.5, 0.5, 60],
    "poppy_seed": [525, 18, 42, 28, 19.5, 4.5, 3, 26],
    "caraway_seed": [333, 20, 15, 50, 38, 1, 0.6, 17],

    # Oils & Fats
    "olive_oil": [884, 0, 100, 0, 0, 14, 0, 2],
    "extra_virgin_olive_oil": [884, 0, 100, 0, 0, 14, 0, 2],
    "coconut_oil": [862, 0, 100, 0, 0, 87, 0, 0],
    "sesame_oil": [884, 0, 100, 0, 0, 14, 0, 0],
    "vegetable_oil": [884, 0, 100, 0, 0, 11, 0, 0],
    "canola_oil": [884, 0, 100, 0, 0, 7, 0, 0],
    "peanut_oil": [884, 0, 100, 0, 0, 17, 0, 0],
    "sunflower_oil": [884, 0, 100, 0, 0, 10, 0, 0],
    "avocado_oil": [884, 0, 100, 0, 0, 12, 0, 0],
    "palm_oil": [884, 0, 100, 0, 0, 49, 0, 0],
    "grape_seed_oil": [884, 0, 100, 0, 0, 10, 0, 0],
    "walnut_oil": [884, 0, 100, 0, 0, 9, 0, 0],
    "truffle_oil": [884, 0, 100, 0, 0, 14, 0, 2],
    "chili_oil": [884, 0, 100, 0, 0, 14, 0, 0],
    "lard": [902, 0, 100, 0, 0, 39, 0, 0],
    "shortening": [880, 0, 100, 0, 0, 25, 0, 0],
    "tallow": [902, 0, 100, 0, 0, 50, 0, 0],
    "duck_fat": [902, 0, 100, 0, 0, 33, 0, 0],
    "chicken_fat": [902, 0, 100, 0, 0, 30, 0, 0],
    "beef_tallow": [902, 0, 100, 0, 0, 50, 0, 0],

    # Herbs & Spices (fresh unless noted)
    "basil": [23, 3.2, 0.6, 2.7, 1.6, 0, 0.3, 4],
    "basil_dried": [233, 24, 4, 48, 38, 0.5, 2, 25],
    "parsley": [36, 3, 0.8, 6, 3.3, 0, 0.9, 56],
    "parsley_dried": [292, 28, 5.5, 57, 31, 0.8, 6, 380],
    "cilantro": [23, 2.1, 0.5, 3.7, 2.8, 0, 0.9, 46],
    "mint": [44, 3.3, 0.7, 8, 6.9, 0.1, 0, 31],
    "spearmint": [44, 3.3, 0.7, 8, 6.9, 0.1, 0, 31],
    "rosemary": [131, 3.3, 5.9, 21, 14, 2.8, 0, 26],
    "thyme": [101, 5.6, 1.7, 24, 14, 0.5, 0, 9],
    "oregano": [265, 9, 5.6, 69, 42.5, 1.2, 4, 25],
    "dill": [43, 3.5, 1.1, 7, 2.1, 0.1, 0, 61],
    "sage": [315, 11, 13, 61, 40, 7, 2, 11],
    "bay_leaf": [313, 7.6, 8.4, 75, 27, 2.3, 0, 23],
    "tarragon": [295, 22, 5, 50, 7.4, 1.2, 0, 62],
    "marjoram": [271, 13, 7, 61, 41, 0.5, 4, 35],
    "savory": [272, 6.7, 5.9, 69, 45, 1.5, 0, 10],
    "lovage": [42, 3.3, 0.6, 8, 4.3, 0, 0, 10],
    "chervil": [237, 23, 3.9, 49, 15, 0.5, 2, 70],
    "black_pepper": [251, 10, 3.3, 64, 25.3, 1.4, 0.6, 20],
    "white_pepper": [296, 10, 2.1, 68, 26.2, 1, 0, 5],
    "green_peppercorn": [251, 10, 3.3, 64, 25, 1.4, 0.6, 20],
    "pink_peppercorn": [251, 10, 3.3, 64, 25, 1.4, 0.6, 20],
    "sichuan_peppercorn": [310, 12, 8, 60, 22, 1.5, 0, 5],
    "cayenne": [318, 12, 17, 57, 27, 3.3, 10, 30],
    "red_pepper_flake": [318, 12, 17, 57, 27, 3.3, 10, 30],
    "chili_powder": [282, 12, 14, 50, 29, 2.5, 10, 60],
    "paprika": [282, 15, 13, 54, 37, 2.1, 10, 68],
    "smoked_paprika": [282, 15, 13, 54, 37, 2.1, 10, 68],
    "cumin": [375, 18, 22, 44, 10.5, 1.5, 2.3, 168],
    "cumin_seed": [375, 18, 22, 44, 10.5, 1.5, 2.3, 168],
    "coriander": [298, 12, 18, 55, 14, 1, 1, 35],
    "coriander_seed": [298, 12, 18, 55, 14, 1, 1, 35],
    "turmeric": [354, 7.8, 9.9, 65, 21, 3.1, 0.5, 38],
    "ginger": [80, 1.8, 0.8, 18, 2, 0.2, 1.7, 13],
    "ginger_dried": [335, 9, 4.2, 72, 14, 2, 3, 30],
    "cinnamon": [247, 4, 1.2, 81, 53, 0.3, 2, 10],
    "cinnamon_stick": [247, 4, 1.2, 81, 53, 0.3, 2, 10],
    "nutmeg": [525, 6, 36, 49, 21, 26, 3, 16],
    "clove": [274, 6, 13, 66, 34, 3.6, 2, 94],
    "allspice": [263, 6, 9, 69, 21, 2.2, 2, 55],
    "cardamom": [311, 11, 6.7, 68, 28, 0.7, 0, 18],
    "star_anise": [337, 18, 16, 50, 14.7, 2, 5, 20],
    "fennel_seed": [345, 16, 15, 52, 40, 0.5, 0, 88],
    "anise_seed": [337, 18, 16, 50, 15, 0.6, 1, 20],
    "mustard_seed": [508, 26, 36, 28, 12, 2, 7, 25],
    "mustard": [66, 3.7, 3.3, 6, 1.5, 0.2, 1, 1100],
    "wasabi": [292, 32, 16, 25, 8, 1.5, 5, 50],
    "horseradish": [48, 1.2, 0.7, 11, 3.3, 0.1, 6, 420],
    "vanilla_extract": [288, 0.1, 0.1, 12, 0, 0, 12, 0],
    "vanilla_bean": [288, 0.1, 0.1, 12, 0, 0, 12, 0],
    "saffron": [310, 11, 6, 65, 4, 1.5, 0, 40],
    "asafoetida": [357, 17, 8, 67, 13, 1, 2, 50],
    "nigella_seed": [345, 17, 15, 52, 40, 1, 1, 50],
    "fenugreek": [323, 23, 6, 58, 25, 1.3, 5, 67],
    "fenugreek_seed": [323, 23, 6, 58, 25, 1.3, 5, 67],
    "curry_leaf": [108, 6, 1, 18, 7, 0.1, 2, 30],
    "lemongrass": [99, 1.8, 0.5, 25, 3.7, 0.1, 0, 6],
    "galangal": [71, 1.5, 0.7, 16, 2, 0.1, 1, 10],
    "kaffir_lime_leaf": [30, 0.8, 0.3, 7, 2, 0, 1, 2],
    "pandan_leaf": [30, 0.8, 0.3, 7, 2, 0, 1, 2],
    "shiso": [30, 2.3, 0.7, 5, 3, 0.1, 0, 5],
    "perilla": [30, 2.3, 0.7, 5, 3, 0.1, 0, 5],

    # Sugars & Sweeteners
    "sugar": [387, 0, 0, 100, 0, 0, 100, 0],
    "brown_sugar": [380, 0, 0, 98, 0, 0, 97, 10],
    "powdered_sugar": [389, 0, 0, 100, 0, 0, 100, 1],
    "cane_sugar": [387, 0, 0, 100, 0, 0, 100, 0],
    "coconut_sugar": [375, 0, 0, 100, 0, 0, 92, 0],
    "date_sugar": [290, 1.5, 0, 75, 7, 0, 65, 2],
    "honey": [304, 0.3, 0, 82, 0.2, 0, 82, 4],
    "maple_syrup": [260, 0, 0.1, 67, 0, 0, 60, 7],
    "agave": [310, 0, 0.1, 76, 0.2, 0, 70, 4],
    "corn_syrup": [290, 0, 0, 77, 0, 0, 77, 50],
    "molasses": [290, 0, 0.1, 75, 0, 0, 75, 37],
    "caramel": [382, 4.6, 8.5, 77, 0, 5.3, 65, 245],
    "chocolate": [546, 4.9, 31, 61, 3.4, 19, 48, 24],
    "dark_chocolate": [546, 4.9, 31, 61, 3.4, 19, 48, 24],
    "milk_chocolate": [535, 7.7, 30, 59, 3.4, 18, 52, 80],
    "white_chocolate": [539, 5.9, 32, 59, 0.2, 19, 59, 75],
    "cocoa_powder": [228, 20, 14, 58, 37, 8, 2, 21],
    "cacao_nib": [480, 14, 40, 40, 20, 24, 0, 10],
    "nutella": [544, 6.6, 31, 58, 3.4, 10, 56, 35],

    # Sauces & Condiments
    "ketchup": [101, 1.1, 0.1, 25, 0.3, 0, 22, 907],
    "mustard": [66, 3.7, 3.3, 6, 1.5, 0.2, 1, 1100],
    "dijon_mustard": [66, 3.7, 3.3, 6, 1.5, 0.2, 1, 1100],
    "whole_grain_mustard": [66, 3.7, 3.3, 6, 1.5, 0.2, 1, 1100],
    "mayonnaise": [680, 0.6, 75, 1.3, 0, 12, 1, 635],
    "japanese_mayonnaise": [680, 0.6, 75, 1.3, 0, 12, 1, 635],
    "vinegar": [18, 0, 0, 0.9, 0, 0, 0.4, 5],
    "rice_vinegar": [18, 0, 0, 0.9, 0, 0, 0.4, 5],
    "balsamic_vinegar": [88, 0.5, 0, 17, 0, 0, 15, 23],
    "apple_cider_vinegar": [21, 0, 0, 0.9, 0, 0, 0.4, 5],
    "red_wine_vinegar": [19, 0.1, 0, 0.9, 0, 0, 0.4, 5],
    "white_wine_vinegar": [18, 0, 0, 0.9, 0, 0, 0.4, 5],
    "worcestershire_sauce": [78, 0, 0, 19, 0, 0, 10, 750],
    "hoisin_sauce": [220, 3.5, 1.5, 50, 1, 0.2, 35, 1200],
    "oyster_sauce": [85, 1.5, 0.5, 17, 0.5, 0.1, 8, 1800],
    "teriyaki_sauce": [89, 2.5, 0, 18, 0, 0, 12, 1400],
    "sriracha": [93, 1.6, 1.2, 19, 1.5, 0.2, 15, 1100],
    "hot_sauce": [32, 1, 0.4, 6, 0.8, 0.1, 2, 950],
    "salsa": [20, 1.1, 0.2, 4.7, 1.7, 0, 2.5, 330],
    "salsa_verde": [20, 1.1, 0.2, 4.7, 1.7, 0, 2.5, 330],
    "pesto": [500, 11, 48, 9, 2.5, 7, 2, 400],
    "tomato_paste": [82, 4.3, 0.5, 19, 4.1, 0.1, 12, 59],
    "tomato_sauce": [24, 1.2, 0.3, 5, 1.5, 0, 3.5, 270],
    "marinara_sauce": [35, 1.3, 0.6, 6, 1.5, 0.1, 4, 300],
    "alfredo_sauce": [300, 5, 30, 4, 0, 18, 2, 400],
    "curry_paste": [150, 3, 12, 8, 3, 2, 3, 500],
    "red_curry_paste": [150, 3, 12, 8, 3, 2, 3, 500],
    "green_curry_paste": [150, 3, 12, 8, 3, 2, 3, 500],
    "gochujang": [190, 4.5, 2, 40, 3, 0.5, 25, 1500],
    "doubanjiang": [200, 5, 3, 35, 4, 0.5, 15, 2000],
    "fermented_black_bean": [200, 12, 1.5, 38, 15, 0.4, 5, 2500],
    "bean_paste": [160, 8, 1.5, 30, 5, 0.3, 10, 1500],
    "soy_bean_paste": [160, 8, 1.5, 30, 5, 0.3, 10, 1500],
    "shrimp_paste": [150, 22, 2, 11, 0, 0.5, 1, 4500],
    "marmite": [565, 43, 0.1, 74, 0.1, 0, 2, 3000],
    "vegemite": [565, 43, 0.1, 74, 0.1, 0, 2, 3000],
    "nutritional_yeast": [376, 50, 5, 36, 15, 1, 2, 60],
    "mushroom_sauce": [35, 1, 0.5, 6, 0.5, 0.1, 3, 350],
    "barbecue_sauce": [135, 0.8, 1.2, 30, 0.5, 0.2, 24, 700],
    "soy_sauce_dark": [53, 8, 0.1, 5, 0.8, 0, 0.8, 5493],

    # Beverages
    "coffee": [1, 0.1, 0, 0, 0, 0, 0, 2],
    "espresso": [9, 0.1, 0.2, 1.7, 0, 0.1, 0, 14],
    "green_tea": [1, 0, 0, 0, 0, 0, 0, 2],
    "black_tea": [1, 0, 0, 0, 0, 0, 0, 2],
    "herbal_tea": [0, 0, 0, 0, 0, 0, 0, 2],
    "white_tea": [1, 0, 0, 0, 0, 0, 0, 2],
    "oolong_tea": [1, 0, 0, 0, 0, 0, 0, 2],
    "matcha": [30, 2.4, 0.6, 5, 0, 0.1, 0.5, 2],
    "wine": [85, 0.1, 0, 2.6, 0, 0, 0.6, 4],
    "red_wine": [85, 0.1, 0, 2.6, 0, 0, 0.6, 4],
    "white_wine": [82, 0.1, 0, 2.6, 0, 0, 0.6, 4],
    "rosé_wine": [83, 0.1, 0, 2.6, 0, 0, 0.6, 4],
    "sparkling_wine": [76, 0.1, 0, 2, 0, 0, 1, 5],
    "sake": [134, 0.5, 0, 5, 0, 0, 1, 2],
    "beer": [42, 0.5, 0, 3.6, 0, 0, 0.3, 4],
    "dark_beer": [50, 0.5, 0, 4, 0, 0, 0.5, 10],
    "stout": [50, 0.6, 0, 5, 0, 0, 0.6, 15],
    "mirin": [241, 0.2, 0, 50, 0, 0, 35, 10],
    "rum": [231, 0, 0, 0, 0, 0, 0, 1],
    "vodka": [231, 0, 0, 0, 0, 0, 0, 1],
    "gin": [263, 0, 0, 0, 0, 0, 0, 1],
    "whiskey": [250, 0, 0, 0.1, 0, 0, 0.1, 1],
    "bourbon": [250, 0, 0, 0.1, 0, 0, 0.1, 1],
    "tequila": [231, 0, 0, 0, 0, 0, 0, 1],
    "brandy": [231, 0, 0, 0, 0, 0, 0.1, 1],
    "vermouth": [140, 0.1, 0, 10, 0, 0, 8, 5],
    "campari": [160, 0, 0, 12, 0, 0, 8, 0],
    "triple_sec": [250, 0, 0, 25, 0, 0, 25, 0],
    "coffee_liqueur": [330, 0, 0.5, 42, 0, 0, 42, 5],
    "amaretto": [280, 0, 0, 35, 0, 0, 35, 0],
    "baileys": [327, 3, 14, 34, 0, 8, 32, 80],

    # Broths & Stocks
    "chicken_broth": [4, 0.6, 0.1, 0.2, 0, 0, 0.1, 350],
    "beef_broth": [4, 0.6, 0.1, 0.2, 0, 0, 0.1, 360],
    "vegetable_broth": [4, 0.4, 0.1, 0.5, 0, 0, 0.2, 310],
    "bone_broth": [20, 2.5, 0.5, 0.5, 0, 0.2, 0.2, 380],
    "dashi": [6, 0.8, 0.1, 0.2, 0, 0, 0, 150],
    "fish_stock": [10, 1.5, 0.2, 0.5, 0, 0, 0.1, 250],
    "miso_soup_base": [20, 1.5, 0.5, 2.5, 0.5, 0.1, 1, 500],

    # Processed & Specialty
    "gelatin": [62, 14, 0, 0, 0, 0, 0, 10],
    "collagen": [350, 85, 0, 0, 0, 0, 0, 10],
    "protein_powder": [400, 80, 5, 10, 0, 1, 2, 100],
    "whey_protein": [420, 80, 6, 10, 0, 2, 3, 150],
    "casein_protein": [380, 75, 4, 8, 0, 1.5, 2, 100],
    "ice_cream": [207, 3.5, 11, 24, 0.5, 7, 21, 60],
    "gelato": [200, 4, 10, 24, 0, 6, 22, 50],
    "sorbet": [165, 0.3, 0.1, 42, 0.5, 0, 35, 10],
    "frozen_yogurt": [159, 3, 5.5, 26, 0, 3.5, 22, 60],
    "pudding": [150, 3, 4, 27, 0, 2.5, 20, 80],
    "custard": [120, 4, 6, 13, 0, 3, 10, 55],

    # Fermented & Pickled
    "kimchi": [24, 1.1, 0.2, 4.5, 2.4, 0, 2, 500],
    "sauerkraut": [15, 0.9, 0.1, 3.3, 2.9, 0, 1.5, 661],
    "pickle": [11, 0.3, 0.2, 2.3, 1, 0, 1.2, 800],
    "cornichon": [11, 0.3, 0.2, 2.3, 1, 0, 1.2, 800],
    "caper": [23, 2.4, 0.9, 5, 3.3, 0.2, 0.4, 2400],
    "kombucha": [5, 0, 0, 1, 0, 0, 0.5, 5],
    "pickled_ginger": [30, 0.3, 0.1, 7, 0.5, 0, 5, 400],
    "pickled_radish": [20, 0.5, 0.1, 4, 1, 0, 3, 350],
    "pickled_onion": [25, 0.5, 0.1, 5, 0.5, 0, 3, 400],
    "pickled_egg": [130, 11, 8, 1, 0, 2.5, 0.5, 700],
    "olive_oil_packed_tuna": [198, 29, 9, 0, 0, 1.5, 0, 300],
    "pickled_jalapeno": [20, 0.5, 0.3, 4, 1.5, 0, 2, 500],
    "pickled_beet": [50, 1, 0.1, 12, 2, 0, 8, 300],
}

# ── FSA traffic light thresholds (per 100g) ──
# Green = low, Orange = medium, Red = high
# Source: UK FSA (Food Standards Agency) guidelines
def fsa_light_fat(val):
    if val <= 3: return "green"
    if val <= 17.5: return "orange"
    return "red"

def fsa_light_saturates(val):
    if val <= 1.5: return "green"
    if val <= 5: return "orange"
    return "red"

def fsa_light_sugars(val):
    if val <= 5: return "green"
    if val <= 22.5: return "orange"
    return "red"

def fsa_light_salt(val):
    if val <= 0.3: return "green"
    if val <= 1.5: return "orange"
    return "red"


# ── Ingredient category heuristics for missing entries ──
# We assign every ingredient to a "food group" based on its name.
# This lets us estimate nutrition for ingredients we don't have exact USDA data for.

def guess_food_group(name):
    """Guess the broad food category from ingredient name."""
    name_lower = name.lower()

    # Check for known suffix/prefix patterns
    meat_keywords = [
        "meat", "beef", "pork", "lamb", "chicken", "turkey", "duck", "goose",
        "bacon", "ham", "sausage", "steak", "rib", "loin", "breast", "thigh",
        "drumstick", "wing", "liver", "kidney", "heart", "tongue", "tripe",
        "salami", "pepperoni", "chorizo", "prosciutto", "pastrami", "corned",
        "pate", "patty", "burger", "meatball", "meatloaf", "hot_dog", "spam",
        "venison", "bison", "goat", "rabbit", "lamb", "mutton", "veal",
        "mortadella", "liverwurst", "pancetta", "guanciale", "soppressata",
    ]
    fish_keywords = [
        "fish", "salmon", "tuna", "cod", "sardine", "anchovy", "mackerel",
        "trout", "halibut", "tilapia", "shrimp", "prawn", "crab", "lobster",
        "octopus", "squid", "clam", "mussel", "oyster", "scallop", "roe",
        "caviar", "surimi", "eel", "sea_bass", "snapper", "catfish",
        "turbot", "monkfish", "swordfish", "yellowtail", "toro", "uni",
        "bass", "flounder", "sole", "pollock", "haddock", "herring",
        "sprat", "whitebait", "crayfish", "langoustine", "abalone",
        "escargot", "frog", "seafood",
    ]
    dairy_keywords = [
        "milk", "cream", "butter", "cheese", "yogurt", "kefir", "lassi",
        "ghee", "buttermilk", "ricotta", "mozzarella", "cheddar", "brie",
        "camembert", "gouda", "feta", "paneer", "curd", "quark",
        "neufchatel", "mascarpone", "fromage", "queso", "formaggio",
    ]
    egg_keywords = ["egg", "egg_white", "egg_yolk", "omelette"]
    legume_keywords = [
        "bean", "lentil", "chickpea", "hummus", "tofu", "tempeh", "edamame",
        "natto", "miso", "soy", "pea", "legume", "dal", "dhal",
    ]
    vegetable_keywords = [
        "cabbage", "lettuce", "spinach", "kale", "broccoli", "cauliflower",
        "carrot", "celery", "tomato", "cucumber", "zucchini", "squash",
        "pepper", "onion", "garlic", "leek", "shallot", "mushroom",
        "asparagus", "green_bean", "corn", "potato", "sweet_potato",
        "avocado", "beet", "radish", "turnip", "eggplant", "okra",
        "artichoke", "pumpkin", "rhubarb", "seaweed", "nori", "kombu",
        "wakame", "nopal", "chard", "endive", "arugula", "watercress",
        "cress", "sprout", "water_chestnut", "bamboo_shoot", "okra",
        "jicama", "daikon", "parsnip", "kohlrabi", "fennel",
    ]
    fruit_keywords = [
        "apple", "pear", "banana", "orange", "lemon", "lime", "grape",
        "berry", "strawberry", "blueberry", "raspberry", "cranberry",
        "cherry", "peach", "plum", "apricot", "mango", "pineapple",
        "kiwi", "melon", "watermelon", "cantaloupe", "honeydew",
        "pomegranate", "fig", "date", "coconut", "olive", "raisin",
        "prune", "currant", "fruit", "papaya", "guava", "lychee",
        "durian", "dragon_fruit", "passion_fruit", "tamarind", "plantain",
        "persimmon", "quince", "rhubarb", "citrus", "clementine",
        "tangerine", "grapefruit", "yuzu", "kumquat", "pomelo",
    ]
    grain_keywords = [
        "rice", "wheat", "bread", "pasta", "noodle", "flour", "oat",
        "quinoa", "couscous", "barley", "bulgur", "farro", "spelt",
        "buckwheat", "amaranth", "millet", "teff", "sorghum", "cornmeal",
        "polenta", "tortilla", "bagel", "croissant", "pita", "naan",
        "lavash", "pizza_dough", "pie_crust", "crouton", "panko",
        "bread_crumb", "muesli", "granola", "cereal", "grain",
    ]
    nut_seed_keywords = [
        "almond", "walnut", "pecan", "cashew", "pistachio", "peanut",
        "hazelnut", "macadamia", "brazil_nut", "chestnut", "pine_nut",
        "seed", "chia", "flax", "hemp", "pumpkin_seed", "sunflower_seed",
        "sesame", "tahini", "poppy_seed", "caraway", "nut",
    ]
    oil_keywords = [
        "oil", "lard", "shortening", "tallow", "fat", "ghee",
    ]
    spice_keywords = [
        "spice", "pepper", "paprika", "cinnamon", "nutmeg", "clove",
        "cardamom", "cumin", "coriander", "turmeric", "ginger", "chili",
        "cayenne", "oregano", "basil", "thyme", "rosemary", "sage",
        "parsley", "dill", "mint", "bay_leaf", "tarragon", "marjoram",
        "savory", "fennel", "anise", "mustard_seed", "wasabi", "saffron",
        "vanilla", "allspice", "star_anise", "galangal", "lemongrass",
        "curry", "fenugreek", "nigella", "asafoetida",
    ]
    sweetener_keywords = [
        "sugar", "honey", "syrup", "molasses", "caramel", "chocolate",
        "cocoa", "cacao", "agave", "sweetener", "nutella", "marshmallow",
        "candy", "toffee", "fudge",
    ]
    sauce_keywords = [
        "sauce", "ketchup", "mustard", "mayonnaise", "vinegar", "pesto",
        "salsa", "paste", "curry_paste", "gochujang", "doubanjiang",
        "marmite", "vegemite",
    ]
    beverage_keywords = [
        "tea", "coffee", "wine", "beer", "sake", "mirin", "liqueur",
        "vermouth", "campari", "triple_sec", "amaretto", "baileys",
        "vodka", "gin", "rum", "whiskey", "bourbon", "tequila", "brandy",
        "juice", "soda", "tonic",
    ]
    broth_keywords = [
        "broth", "stock", "dashi", "soup", "consomme", "bouillon",
    ]
    fermented_keywords = [
        "kimchi", "sauerkraut", "pickle", "kombucha", "fermented",
    ]

    for kw in meat_keywords:
        if kw in name_lower: return "meat"
    for kw in fish_keywords:
        if kw in name_lower: return "fish"
    for kw in dairy_keywords:
        if kw in name_lower: return "dairy"
    for kw in egg_keywords:
        if kw in name_lower: return "egg"
    for kw in legume_keywords:
        if kw in name_lower: return "legume"
    for kw in vegetable_keywords:
        if kw in name_lower: return "vegetable"
    for kw in fruit_keywords:
        if kw in name_lower: return "fruit"
    for kw in grain_keywords:
        if kw in name_lower: return "grain"
    for kw in nut_seed_keywords:
        if kw in name_lower: return "nut_seed"
    for kw in oil_keywords:
        if kw in name_lower: return "oil"
    for kw in spice_keywords:
        if kw in name_lower: return "spice"
    for kw in sweetener_keywords:
        if kw in name_lower: return "sweetener"
    for kw in sauce_keywords:
        if kw in name_lower: return "sauce"
    for kw in beverage_keywords:
        if kw in name_lower: return "beverage"
    for kw in broth_keywords:
        if kw in name_lower: return "broth"
    for kw in fermented_keywords:
        if kw in name_lower: return "fermented"

    return "other"


# ── Default nutrient profiles per food group (per 100g) ──
# [calories, protein_g, fat_g, carbs_g, fiber_g, saturates_g, sugars_g, sodium_mg]
GROUP_NUTRITION = {
    "meat": [220, 22, 14, 0.5, 0, 5.0, 0, 350],
    "fish": [120, 20, 4, 0.5, 0, 1.0, 0, 150],
    "dairy": [250, 12, 18, 6, 0, 11.0, 6, 400],
    "egg": [155, 13, 11, 1.1, 0, 3.3, 1.1, 124],
    "legume": [130, 9, 3, 20, 7, 0.5, 3, 20],
    "vegetable": [30, 1.5, 0.3, 6, 2.5, 0.1, 2.5, 30],
    "fruit": [60, 0.8, 0.3, 15, 2.5, 0.1, 11, 2],
    "grain": [200, 6, 3, 38, 4, 0.8, 5, 120],
    "nut_seed": [580, 18, 50, 22, 10, 6, 5, 10],
    "oil": [880, 0, 100, 0, 0, 25, 0, 0],
    "spice": [250, 10, 8, 50, 20, 1.5, 5, 40],
    "sweetener": [380, 0, 5, 90, 2, 3, 75, 20],
    "sauce": [120, 3, 5, 18, 1, 1, 8, 800],
    "beverage": [60, 0.2, 0.1, 5, 0, 0, 3, 5],
    "broth": [5, 0.5, 0.1, 0.3, 0, 0, 0.1, 300],
    "fermented": [25, 1.5, 0.3, 4, 2, 0.1, 2, 500],
    "other": [100, 3, 4, 14, 3, 1, 5, 100],
}


def get_nutrition(name):
    """Get nutritional data for an ingredient, with defaults and estimation."""
    # Exact match
    if name in NUTRITION_DB:
        return NUTRITION_DB[name]

    # Try synonyms: replace underscores with nothing, try common variants
    synonyms = [
        name.replace("_", ""),  # e.g. "apple_juice" -> "applejuice"
        name.replace("_", " "),  # Try space-separated
    ]
    for s in synonyms:
        if s in NUTRITION_DB:
            return NUTRITION_DB[s]

    # Try removing suffixes like "_dried", "_fresh", "_raw", "_cooked"
    for suffix in ["_dried", "_fresh", "_raw", "_cooked", "_smoked", "_ground", "_roasted", "_toasted", "_candied", "_glazed"]:
        if name.endswith(suffix):
            base = name[:-len(suffix)]
            if base in NUTRITION_DB:
                return NUTRITION_DB[base]

    # Try prefix matching (e.g. "chicken_liver" matches "chicken_breast" group)
    parts = name.split("_")
    for i in range(len(parts), 0, -1):
        prefix = "_".join(parts[:i])
        if prefix in NUTRITION_DB:
            return NUTRITION_DB[prefix]

    # Fall back to group default
    group = guess_food_group(name)
    return GROUP_NUTRITION[group]


def compute_sodium_to_salt(sodium_mg):
    """Convert sodium (mg) to salt (g). FSA: salt = sodium * 2.5 / 1000"""
    return round(sodium_mg * 2.5 / 1000, 4)


def im2recipe_format(name, nutrition):
    """Convert our internal format to im2recipe-Pytorch format."""
    energy_kcal, protein_g, fat_g, carbs_g, fiber_g, saturates_g, sugars_g, sodium_mg = nutrition

    salt_g = compute_sodium_to_salt(sodium_mg)

    return {
        "nutr_values_per100g": {
            "energy": round(energy_kcal, 4),
            "fat": round(fat_g, 4),
            "protein": round(protein_g, 4),
            "salt": round(salt_g, 4),
            "saturates": round(saturates_g, 4),
            "sugars": round(sugars_g, 4),
        },
        "nutr_per_100g_extended": {
            "carbs": round(carbs_g, 4),
            "fiber": round(fiber_g, 4),
            "sodium_mg": round(sodium_mg, 4),
        },
        "fsa_lights_per100g": {
            "fat": fsa_light_fat(fat_g),
            "salt": fsa_light_salt(salt_g),
            "saturates": fsa_light_saturates(saturates_g),
            "sugars": fsa_light_sugars(sugars_g),
        },
    }


# ── Main ──

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Load all Epicure ingredient names
    vocab_path = os.path.join(DATA_DIR, "vocab.csv")
    if not os.path.exists(vocab_path):
        print(f"❌ vocab.csv not found at {vocab_path}")
        sys.exit(1)

    names = []
    with open(vocab_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row["name"])

    print(f"Loaded {len(names)} ingredient names from vocab.csv")

    # Build nutrition data
    nutrition_data = {}
    vocab_map = {}  # im2recipe-style name -> Epicure canonical name
    matched_count = 0
    estimated_count = 0

    for name in names:
        nutrition = get_nutrition(name)
        if name in NUTRITION_DB:
            matched_count += 1
        else:
            estimated_count += 1

        # Record in im2recipe-Pytorch format
        nutrition_data[name] = im2recipe_format(name, nutrition)

        # Build vocabulary mapping
        im2recipe_style = name.replace("_", " ").lower()
        vocab_map[im2recipe_style] = name

        # Also add USDA-style ingredient names (plural forms, variations)
        if not name.endswith("_seed") and not name.endswith("_oil"):
            # Add a version with "s" suffix for common ingredients
            plural = name + "s"
            vocab_map[plural.replace("_", " ").lower()] = name

    # Write epicure_nutrition.json
    output = {
        "version": "1.0",
        "generated": "2026-06-07",
        "format": "im2recipe-Pytorch",
        "n_ingredients": len(names),
        "n_matched_usda": matched_count,
        "n_estimated": estimated_count,
        "data": nutrition_data,
        "_im2recipe_note": "Format matches im2recipe-Pytorch nutr_values_per100g + fsa_lights_per100g. "
                           "Load actual im2recipe 35K dataset via the data access form for enriched per-recipe data.",
    }

    out_path = os.path.join(DATA_DIR, "epicure_nutrition.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    out_size = os.path.getsize(out_path)
    print(f"\n✅ Written {out_path} ({out_size / 1024:.0f} KB)")
    print(f"   {matched_count} ingredients with exact USDA match")
    print(f"   {estimated_count} ingredients estimated (food-group defaults)")
    print(f"   {len(names)} total ingredients covered")

    # Write nutrition_vocab.json
    vocab_path_out = os.path.join(DATA_DIR, "nutrition_vocab.json")
    with open(vocab_path_out, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "note": "Maps im2recipe-Pytorch/USDA ingredient name formats to Epicure canonical names. "
                    "Use this to bridge the im2recipe 35K nutritional dataset when obtained.",
            "mapping": vocab_map,
        }, f, ensure_ascii=False, indent=2)

    vocab_size = os.path.getsize(vocab_path_out)
    print(f"✅ Written {vocab_path_out} ({vocab_size / 1024:.1f} KB)")
    print(f"   {len(vocab_map)} vocabulary entries")


# ── 35K Per-Recipe Importer (im2recipe-Pytorch format) ──
# When you obtain the actual im2recipe 35K per-recipe dataset (via the Recipe1M data access form),
# place the JSON file in data/ and run this function:
#
#   1. Fill the form at https://forms.gle/EzYSu8j3D1LJzVbR8
#     (Access granted for research purposes to universities/research institutions)
#   2. Place the downloaded im2recipe nutritional JSON in data/im2recipe_recipes.json
#   3. Run: python3 build_nutrition.py --import-im2recipe
#
# Expected format (from im2recipe-Pytorch README):
#   Array of dicts like:
#     {
#       "id": "000095fc1d",
#       "title": "Yogurt Parfaits",
#       "ingredients": [{"text": "yogurt, greek, plain, nonfat"}, ...],
#       "instructions": [{"text": "Layer all ingredients..."}],
#       "nutr_values_per100g": {"energy": 81.1, "fat": 2.14, "protein": 6.9, "salt": 0.06, "saturates": 0.37, "sugars": 5.09},
#       "fsa_lights_per100g": {"fat": "green", "salt": "green", "saturates": "green", "sugars": "orange"},
#       "nutr_per_ingredient": [{"nrg": 133.8, "pro": 23.1, "fat": 0.88, "sat": 0.27, "sod": 81.6, "sug": 7.35}, ...],
#       "weight_per_ingr": [226.8, 152.0, 30.5],
#       "partition": "train",
#     }

def import_im2recipe_recipes(input_path="data/im2recipe_recipes.json"):
    """Import the im2recipe-Pytorch 35K per-recipe nutritional dataset and
    merge it with our ingredient-level data for per-recipe FSA scoring.

    Generates:
      data/recipe_nutrition.json — Per-recipe nutrition index keyed by recipe ID.
      data/recipe_ingredient_map.json — Maps Epicure canonical ingredient names
        to im2recipe recipe IDs for cross-referencing.
    """
    import os

    if not os.path.exists(input_path):
        print(f"❌ im2recipe recipes file not found at {input_path}")
        print(f"   Fill the form: https://forms.gle/EzYSu8j3D1LJzVbR8")
        print(f"   Place the downloaded file at {input_path}")
        return

    print(f"Loading im2recipe recipes from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    print(f"Loaded {len(recipes)} recipes")
    partitions = {}
    for r in recipes:
        p = r.get("partition", "unknown")
        partitions.setdefault(p, 0)
        partitions[p] += 1

    for p, count in partitions.items():
        print(f"  {p}: {count}")

    # Build per-recipe nutrition index
    recipe_nutrition = {}
    ingredient_to_recipes = {}  # USDA ingredient name -> [recipe IDs]

    for r in recipes:
        rid = r["id"]
        recipe_nutrition[rid] = {
            "title": r.get("title", ""),
            "partition": r.get("partition", "unknown"),
            "nutr_values_per100g": r.get("nutr_values_per100g", {}),
            "fsa_lights_per100g": r.get("fsa_lights_per100g", {}),
            "nutr_per_ingredient": r.get("nutr_per_ingredient", []),
            "weight_per_ingr": r.get("weight_per_ingr", []),
            "ingredients": [i["text"] for i in r.get("ingredients", [])],
        }

        # Index ingredients -> recipe IDs
        for ingr in r.get("ingredients", []):
            usda_name = ingr["text"].lower().strip()
            if usda_name not in ingredient_to_recipes:
                ingredient_to_recipes[usda_name] = []
            ingredient_to_recipes[usda_name].append(rid)

    # Write recipe_nutrition.json
    out = {
        "version": "2.0",
        "generated": "2026-06-07",
        "n_recipes": len(recipes),
        "partitions": partitions,
        "recipes": recipe_nutrition,
        "_note": "Per-recipe nutrition from im2recipe-Pytorch 35K dataset. "
                 "Each recipe has nutr_values_per100g, fsa_lights_per100g, "
                 "nutr_per_ingredient array (one per ingredient), and weight_per_ingr.",
    }
    out_path = os.path.join(DATA_DIR, "recipe_nutrition.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Written {out_path} ({os.path.getsize(out_path) / 1024:.0f} KB)")
    print(f"   {len(recipe_nutrition)} recipes indexed")

    # Write ingredient -> recipes map
    map_out = {
        "version": "1.0",
        "generated": "2026-06-07",
        "n_ingredients": len(ingredient_to_recipes),
        "_note": "Maps USDA ingredient names (lowercase, matching im2recipe format) "
                 "to im2recipe recipe IDs. Cross-reference with nutrition_vocab.json "
                 "to bridge to Epicure canonical names.",
        "mapping": {k: list(set(v)) for k, v in ingredient_to_recipes.items()},
    }
    map_path = os.path.join(DATA_DIR, "recipe_ingredient_map.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(map_out, f, ensure_ascii=False, indent=2)

    print(f"✅ Written {map_path} ({os.path.getsize(map_path) / 1024:.0f} KB)")
    print(f"   {len(ingredient_to_recipes)} unique USDA ingredients mapped")


if __name__ == "__main__":
    import sys
    if "--import-im2recipe" in sys.argv:
        import_im2recipe_recipes()
    else:
        main()
