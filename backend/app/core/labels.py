"""
Class labels for both ML models, plus rich metadata for UI display.
PlantVillage dataset classes (38 disease classes across 14 plant species).
"""

from typing import Dict, Any

# ── Stage 1: Plant Species Labels ────────────────────────────────────────────
# Maps model output index → plant common name
SPECIES_LABELS: Dict[int, str] = {
    0: "Apple",
    1: "Blueberry",
    2: "Cherry",
    3: "Corn (Maize)",
    4: "Grape",
    5: "Orange",
    6: "Peach",
    7: "Bell Pepper",
    8: "Potato",
    9: "Raspberry",
    10: "Soybean",
    11: "Squash",
    12: "Strawberry",
    13: "Tomato",
}

# ── Stage 2: Disease Labels ───────────────────────────────────────────────────
# Maps model output index → (plant, disease, is_healthy)
DISEASE_LABELS: Dict[int, Dict[str, Any]] = {
    0:  {"plant": "Apple",       "disease": "Apple Scab",                "healthy": False},
    1:  {"plant": "Apple",       "disease": "Black Rot",                 "healthy": False},
    2:  {"plant": "Apple",       "disease": "Cedar Apple Rust",          "healthy": False},
    3:  {"plant": "Apple",       "disease": "Healthy",                   "healthy": True},
    4:  {"plant": "Blueberry",   "disease": "Healthy",                   "healthy": True},
    5:  {"plant": "Cherry",      "disease": "Powdery Mildew",            "healthy": False},
    6:  {"plant": "Cherry",      "disease": "Healthy",                   "healthy": True},
    7:  {"plant": "Corn",        "disease": "Cercospora Leaf Spot",      "healthy": False},
    8:  {"plant": "Corn",        "disease": "Common Rust",               "healthy": False},
    9:  {"plant": "Corn",        "disease": "Northern Leaf Blight",      "healthy": False},
    10: {"plant": "Corn",        "disease": "Healthy",                   "healthy": True},
    11: {"plant": "Grape",       "disease": "Black Rot",                 "healthy": False},
    12: {"plant": "Grape",       "disease": "Esca (Black Measles)",      "healthy": False},
    13: {"plant": "Grape",       "disease": "Leaf Blight",               "healthy": False},
    14: {"plant": "Grape",       "disease": "Healthy",                   "healthy": True},
    15: {"plant": "Orange",      "disease": "Haunglongbing (Citrus Greening)", "healthy": False},
    16: {"plant": "Peach",       "disease": "Bacterial Spot",            "healthy": False},
    17: {"plant": "Peach",       "disease": "Healthy",                   "healthy": True},
    18: {"plant": "Bell Pepper", "disease": "Bacterial Spot",            "healthy": False},
    19: {"plant": "Bell Pepper", "disease": "Healthy",                   "healthy": True},
    20: {"plant": "Potato",      "disease": "Early Blight",              "healthy": False},
    21: {"plant": "Potato",      "disease": "Late Blight",               "healthy": False},
    22: {"plant": "Potato",      "disease": "Healthy",                   "healthy": True},
    23: {"plant": "Raspberry",   "disease": "Healthy",                   "healthy": True},
    24: {"plant": "Soybean",     "disease": "Healthy",                   "healthy": True},
    25: {"plant": "Squash",      "disease": "Powdery Mildew",            "healthy": False},
    26: {"plant": "Strawberry",  "disease": "Leaf Scorch",               "healthy": False},
    27: {"plant": "Strawberry",  "disease": "Healthy",                   "healthy": True},
    28: {"plant": "Tomato",      "disease": "Bacterial Spot",            "healthy": False},
    29: {"plant": "Tomato",      "disease": "Early Blight",              "healthy": False},
    30: {"plant": "Tomato",      "disease": "Late Blight",               "healthy": False},
    31: {"plant": "Tomato",      "disease": "Leaf Mold",                 "healthy": False},
    32: {"plant": "Tomato",      "disease": "Septoria Leaf Spot",        "healthy": False},
    33: {"plant": "Tomato",      "disease": "Spider Mites",              "healthy": False},
    34: {"plant": "Tomato",      "disease": "Target Spot",               "healthy": False},
    35: {"plant": "Tomato",      "disease": "Tomato Yellow Leaf Curl Virus", "healthy": False},
    36: {"plant": "Tomato",      "disease": "Tomato Mosaic Virus",       "healthy": False},
    37: {"plant": "Tomato",      "disease": "Healthy",                   "healthy": True},
}

# ── Rich Plant Metadata ───────────────────────────────────────────────────────
PLANT_METADATA: Dict[str, Dict[str, Any]] = {
    "Tomato": {
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "common_names": ["Tomato", "Love Apple", "Garden Tomato"],
        "description": (
            "Tomato is a fruiting plant native to South America, now one of the world's "
            "most widely cultivated crops. Its bright red, juicy fruits are a staple in "
            "cuisines globally, valued for flavor, nutrition, and culinary versatility."
        ),
        "uses": [
            "Culinary — raw in salads, cooked in sauces, soups, and pastes",
            "Medicinal — rich in lycopene, an antioxidant linked to reduced cancer risk",
            "Industrial — used in ketchup, juice, and canned food production",
        ],
        "growing_conditions": (
            "Full sun (6–8 hrs/day), well-drained fertile soil, pH 6.0–6.8. "
            "Warm temperatures 21–27°C. Regular watering; avoid waterlogging. "
            "Stake plants when they exceed 30 cm height."
        ),
        "interesting_facts": [
            "Botanically a fruit, legally classified as a vegetable in the US since 1893",
            "China is the world's largest tomato producer (>60 million tonnes/year)",
            "There are over 10,000 known tomato varieties worldwide",
            "Tomatoes were once believed to be poisonous in Europe",
        ],
        "origin": "South America (Peru, Ecuador)",
        "season": "Summer–Autumn",
    },
    "Potato": {
        "scientific_name": "Solanum tuberosum",
        "family": "Solanaceae",
        "common_names": ["Potato", "White Potato", "Irish Potato"],
        "description": (
            "Potato is a starchy tuberous crop and the world's fourth-largest food crop. "
            "Originating in the Andean highlands, it became a global staple after the "
            "Columbian Exchange and is now grown on every inhabited continent."
        ),
        "uses": [
            "Culinary — boiled, baked, fried, mashed; used in countless dishes worldwide",
            "Industrial — starch production, biofuel, animal feed",
            "Medicinal — high in potassium, Vitamin C, and B6",
        ],
        "growing_conditions": (
            "Cool climate, 15–20°C optimal. Loose, well-drained soil pH 5.0–6.0. "
            "Plant seed tubers 10–15 cm deep. Hill soil as plants grow. "
            "Moderate, consistent watering."
        ),
        "interesting_facts": [
            "Potatoes were the first vegetable grown in space (1995, Space Shuttle Columbia)",
            "The Irish Famine (1845–1852) was caused by potato late blight (P. infestans)",
            "A potato is about 80% water and 20% solid",
            "Over 4,000 potato varieties exist in the Andes alone",
        ],
        "origin": "Andes Mountains, South America",
        "season": "Spring–Summer",
    },
    "Apple": {
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "common_names": ["Apple", "Eating Apple", "Cultivated Apple"],
        "description": (
            "Apple is one of the most widely cultivated tree fruits, with a history spanning "
            "thousands of years. Grown in temperate regions worldwide, apples are prized for "
            "their flavor, nutrition, and long storage life."
        ),
        "uses": [
            "Culinary — fresh eating, pies, juices, ciders, vinegar",
            "Medicinal — rich in fiber, quercetin; linked to heart health",
            "Ornamental — spring blossoms make apple trees popular garden trees",
        ],
        "growing_conditions": (
            "Temperate climate with cold winters for dormancy. Full sun. "
            "Well-drained loamy soil, pH 6.0–7.0. Requires cross-pollination "
            "from another variety. Regular pruning for best yields."
        ),
        "interesting_facts": [
            "There are over 7,500 known apple cultivars worldwide",
            "Apples are a member of the rose family",
            "Apple seeds contain small amounts of cyanide-producing amygdalin",
            "The science of apple growing is called pomology",
        ],
        "origin": "Central Asia (Kazakhstan)",
        "season": "Autumn",
    },
    "Corn (Maize)": {
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "common_names": ["Maize", "Corn", "Indian Corn"],
        "description": (
            "Corn is a cereal grain first domesticated by indigenous peoples in Mexico "
            "around 9,000 years ago. It is now the world's most produced crop by weight, "
            "with applications ranging from food to fuel to industrial materials."
        ),
        "uses": [
            "Culinary — eaten fresh, ground into flour/meal, popped as popcorn",
            "Industrial — ethanol biofuel, corn syrup, starch, plastics",
            "Animal feed — primary feed grain globally",
        ],
        "growing_conditions": (
            "Warm season crop; soil temp >10°C for germination. Full sun. "
            "Rich, well-drained soil with high nitrogen. Plant in blocks "
            "for wind pollination. 65–95 days to maturity."
        ),
        "interesting_facts": [
            "Each ear of corn has an even number of rows, typically 16",
            "Corn is a grass, not a vegetable",
            "The US produces ~35% of the world's corn supply",
            "Corn can be red, blue, pink, and black in addition to yellow and white",
        ],
        "origin": "Mesoamerica (Mexico)",
        "season": "Summer",
    },
    "Grape": {
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "common_names": ["Grape", "Wine Grape", "Table Grape"],
        "description": (
            "Grapes are berry fruits grown on woody vines of the genus Vitis. "
            "Cultivated for thousands of years, they are used for fresh consumption, "
            "dried as raisins, and fermented into wine."
        ),
        "uses": [
            "Culinary — eaten fresh, dried into raisins, pressed for juice",
            "Beverage — winemaking; one of the world's oldest industries",
            "Medicinal — resveratrol in grape skin linked to cardiovascular benefits",
        ],
        "growing_conditions": (
            "Sunny, warm climate with cool nights. Well-drained soil; tolerates poor soils. "
            "pH 5.5–6.5. Requires trellising and annual pruning. "
            "Drought-tolerant once established."
        ),
        "interesting_facts": [
            "Viticulture (grape growing) is over 8,000 years old",
            "A single grape vine can live over 100 years",
            "It takes about 600–800 grapes to make one bottle of wine",
            "Grapes are the most widely grown fruit crop in the world",
        ],
        "origin": "Near East / Caucasus region",
        "season": "Late Summer–Autumn",
    },
    "Strawberry": {
        "scientific_name": "Fragaria × ananassa",
        "family": "Rosaceae",
        "common_names": ["Strawberry", "Garden Strawberry"],
        "description": (
            "The garden strawberry is a widely grown hybrid species of the genus Fragaria. "
            "Prized for its distinctive aroma, bright red color, and sweet flavor, "
            "it is among the most popular fruits worldwide."
        ),
        "uses": [
            "Culinary — eaten fresh, in jams, desserts, salads, smoothies",
            "Medicinal — high in Vitamin C, manganese, and antioxidants",
            "Cosmetic — used in skincare for brightening and exfoliating",
        ],
        "growing_conditions": (
            "Full sun, at least 6 hours/day. Sandy loam, pH 5.5–6.5. "
            "Plant in raised beds for drainage. Mulch to retain moisture and "
            "suppress weeds. Replace plants every 3–4 years."
        ),
        "interesting_facts": [
            "Strawberries are not true berries — they are aggregate accessory fruits",
            "Each strawberry has about 200 tiny seeds on its surface",
            "Belgium has a museum dedicated entirely to strawberries",
            "Ancient Romans used strawberries medicinally for depression and fever",
        ],
        "origin": "Brittany, France (1750s hybrid)",
        "season": "Spring–Early Summer",
    },
    "Bell Pepper": {
        "scientific_name": "Capsicum annuum",
        "family": "Solanaceae",
        "common_names": ["Bell Pepper", "Sweet Pepper", "Capsicum"],
        "description": (
            "Bell peppers are a cultivar group of Capsicum annuum, characterized by their "
            "thick walls, sweet flavor, and zero heat (Scoville 0). Available in green, "
            "red, yellow, and orange, they are globally popular vegetables."
        ),
        "uses": [
            "Culinary — eaten raw, roasted, stuffed, or stir-fried",
            "Medicinal — exceptionally high in Vitamin C (3× more than oranges)",
            "Food industry — used in spice blends, paprika, and sauces",
        ],
        "growing_conditions": (
            "Warm season; soil temp >18°C. Full sun. "
            "Rich, moist, well-drained soil, pH 6.0–6.8. "
            "Start indoors 8–10 weeks before last frost. "
            "Regular watering; sensitive to drought."
        ),
        "interesting_facts": [
            "Green bell peppers are unripe red bell peppers — same plant",
            "Red bell peppers have 11× more beta-carotene than green peppers",
            "Bell peppers are native to Mexico, Central, and South America",
            "They are one of the highest Vitamin C vegetables available",
        ],
        "origin": "Mexico and Central America",
        "season": "Summer–Autumn",
    },
    "Peach": {
        "scientific_name": "Prunus persica",
        "family": "Rosaceae",
        "common_names": ["Peach", "Nectarine (smooth variety)"],
        "description": (
            "Peach is a deciduous tree native to Northwest China, bearing juicy, "
            "fragrant drupes with velvety skin. Widely cultivated in warm temperate "
            "regions, peaches are beloved for their sweet flavor and aroma."
        ),
        "uses": [
            "Culinary — eaten fresh, in pies, jams, cobblers, and beverages",
            "Medicinal — good source of Vitamins A and C, dietary fiber",
            "Industrial — used in flavoring, cosmetics, and essential oils",
        ],
        "growing_conditions": (
            "Full sun, 6–8 hours/day. Well-drained soil, pH 6.0–7.0. "
            "Requires 600–900 chill hours (<7°C) for dormancy break. "
            "Annual pruning improves fruit quality. Thin fruit for larger size."
        ),
        "interesting_facts": [
            "Peaches are closely related to almonds — both are drupes",
            "China produces ~60% of the world's peaches",
            "The peach is the national fruit of Iran",
            "Peach fuzz repels insects and regulates moisture loss",
        ],
        "origin": "Northwest China",
        "season": "Summer",
    },
    "Cherry": {
        "scientific_name": "Prunus avium / Prunus cerasus",
        "family": "Rosaceae",
        "common_names": ["Sweet Cherry", "Sour Cherry", "Wild Cherry"],
        "description": (
            "Cherries are small stone fruits that come in sweet (P. avium) and sour "
            "(P. cerasus) varieties. They are prized for their flavor, vibrant color, "
            "and a short but celebrated growing season."
        ),
        "uses": [
            "Culinary — eaten fresh, in pies, jams, juices, and liqueurs",
            "Medicinal — anti-inflammatory properties; melatonin aids sleep",
            "Ornamental — cherry blossom trees (Sakura) are culturally iconic in Japan",
        ],
        "growing_conditions": (
            "Full sun. Deep, well-drained soil, pH 6.0–7.0. "
            "Requires winter chill hours. Sweet cherries need cross-pollination. "
            "Net trees to protect from birds."
        ),
        "interesting_facts": [
            "Japan's cherry blossom (Sakura) festival attracts millions of visitors annually",
            "The Bing cherry, the most common US variety, was named after a Chinese laborer",
            "A single cherry tree can produce up to 7,000 cherries per year",
            "Cherries are one of the few natural sources of melatonin",
        ],
        "origin": "Europe and Western Asia",
        "season": "Early Summer",
    },
    "Orange": {
        "scientific_name": "Citrus sinensis",
        "family": "Rutaceae",
        "common_names": ["Orange", "Sweet Orange", "Navel Orange"],
        "description": (
            "The orange is a citrus fruit hybrid originating in South Asia. "
            "It is the world's most cultivated citrus fruit, grown for its sweet, "
            "juicy flesh and aromatic peel. Brazil and China are top producers."
        ),
        "uses": [
            "Culinary — eaten fresh, juiced, used in marmalade and zest",
            "Medicinal — excellent Vitamin C source; immune-boosting",
            "Industrial — essential oils used in perfumery and cleaning products",
        ],
        "growing_conditions": (
            "Subtropical to tropical climate. Full sun. "
            "Well-drained sandy loam, pH 6.0–7.5. "
            "Frost-sensitive; protect below 0°C. "
            "Drip irrigation preferred; avoid waterlogging."
        ),
        "interesting_facts": [
            "Oranges are a hybrid of pomelo and mandarin",
            "Brazil is the world's largest orange juice producer",
            "The color 'orange' was named after the fruit, not vice versa",
            "Orange blossom is the state flower of Florida",
        ],
        "origin": "South and Southeast Asia",
        "season": "Winter–Spring",
    },
    "Blueberry": {
        "scientific_name": "Vaccinium corymbosum",
        "family": "Ericaceae",
        "common_names": ["Blueberry", "Highbush Blueberry"],
        "description": (
            "Blueberries are perennial flowering plants producing blue-purple berries. "
            "Native to North America, they are among the most antioxidant-rich foods "
            "available and have grown into a major global commercial crop."
        ),
        "uses": [
            "Culinary — eaten fresh, in muffins, jams, smoothies, sauces",
            "Medicinal — highest antioxidant capacity among common fruits",
            "Health food — linked to improved brain function and heart health",
        ],
        "growing_conditions": (
            "Acidic soil is essential — pH 4.5–5.5. Full sun to partial shade. "
            "Well-drained, moist, organic-rich soil. Plant two varieties for cross-pollination. "
            "Mulch heavily with pine bark or sawdust."
        ),
        "interesting_facts": [
            "Blueberries are one of the few fruits native to North America",
            "They can live for 50+ years and still produce berries",
            "Wild blueberries have twice the antioxidants of cultivated ones",
            "The US produces ~40% of the world's blueberries",
        ],
        "origin": "North America",
        "season": "Summer",
    },
    "Soybean": {
        "scientific_name": "Glycine max",
        "family": "Fabaceae",
        "common_names": ["Soybean", "Soya Bean", "Edamame (immature)"],
        "description": (
            "Soybean is a legume species native to East Asia, widely grown for its edible "
            "bean with numerous uses. It is an extremely versatile crop used for human food, "
            "animal feed, and industrial applications."
        ),
        "uses": [
            "Culinary — tofu, soy milk, miso, tempeh, edamame, soy sauce",
            "Industrial — biodiesel, ink, candles, lubricants",
            "Animal feed — primary global protein source for livestock",
        ],
        "growing_conditions": (
            "Warm season; soil temp >10°C. Full sun. "
            "Well-drained loam, pH 6.0–7.0. "
            "Fixes atmospheric nitrogen (reduces fertilizer need). "
            "100–120 days to maturity."
        ),
        "interesting_facts": [
            "Soy accounts for ~70% of all protein fed to US livestock",
            "Soybeans can be processed into over 200 different products",
            "The US, Brazil, and Argentina produce ~80% of the world's soybeans",
            "Soybeans are the only plant food with all essential amino acids",
        ],
        "origin": "Northeast China",
        "season": "Summer",
    },
    "Squash": {
        "scientific_name": "Cucurbita pepo / maxima / moschata",
        "family": "Cucurbitaceae",
        "common_names": ["Squash", "Pumpkin", "Zucchini", "Marrow"],
        "description": (
            "Squash encompasses several species of Cucurbita, cultivated for their "
            "edible fruits. Divided into summer squash (eaten young) and winter squash "
            "(eaten mature), they are among the oldest cultivated plants."
        ),
        "uses": [
            "Culinary — roasted, puréed, stuffed, in soups and pies",
            "Medicinal — rich in beta-carotene, Vitamins A and C",
            "Seeds — edible and nutritious; pressed for oil",
        ],
        "growing_conditions": (
            "Warm season; frost-sensitive. Full sun. "
            "Rich, well-drained soil, pH 6.0–7.0. "
            "Plant after last frost; needs space to sprawl. "
            "Regular watering at base (avoid wetting leaves)."
        ),
        "interesting_facts": [
            "Squash was one of the 'Three Sisters' crops of Native Americans",
            "Pumpkins are technically a variety of squash",
            "The Atlantic Giant pumpkin holds world records exceeding 1,000 kg",
            "Squash flowers are edible and commonly used in Mexican cuisine",
        ],
        "origin": "Mesoamerica (Mexico)",
        "season": "Summer–Autumn",
    },
    "Raspberry": {
        "scientific_name": "Rubus idaeus",
        "family": "Rosaceae",
        "common_names": ["Raspberry", "Red Raspberry"],
        "description": (
            "Raspberries are aggregate fruits of the genus Rubus, growing on "
            "biennial canes. Prized for their intense flavor, they are popular "
            "fresh and used extensively in preserves, desserts, and beverages."
        ),
        "uses": [
            "Culinary — fresh, in jams, jellies, desserts, sauces, wines",
            "Medicinal — high in antioxidants, fiber, and Vitamin C",
            "Health — raspberry leaf tea traditionally used for women's health",
        ],
        "growing_conditions": (
            "Temperate climate. Full sun to partial shade. "
            "Well-drained, fertile soil, pH 5.5–6.5. "
            "Support canes with trellis. Prune after fruiting. "
            "Mulch to conserve moisture."
        ),
        "interesting_facts": [
            "Each raspberry is made of about 100 individual small fruits (drupelets)",
            "Russia is the world's largest raspberry producer",
            "Black and golden raspberries exist, not just red",
            "Raspberry canes fruit in their second year then die",
        ],
        "origin": "Europe and Northern Asia",
        "season": "Summer",
    },
}

# ── Disease Metadata ──────────────────────────────────────────────────────────
DISEASE_METADATA: Dict[str, Dict[str, Any]] = {
    "Early Blight": {
        "severity": "moderate",
        "description": (
            "Early Blight is a common fungal disease caused by Alternaria solani. "
            "It appears as dark brown to black lesions with concentric rings (target-board pattern) "
            "on older leaves first, gradually spreading upward. Severe infections defoliate plants "
            "and significantly reduce yield."
        ),
        "pathogen": "Alternaria solani (fungus)",
        "causes": [
            "Warm, humid weather (24–29°C with >90% relative humidity)",
            "Infected plant debris left in soil after harvest",
            "Overhead irrigation that keeps foliage wet",
            "Poor air circulation in dense plantings",
            "Nutrient-deficient or stressed plants",
        ],
        "prevention": [
            "Use certified disease-free seeds and transplants",
            "Rotate crops — avoid planting Solanaceae in same location for 3+ years",
            "Remove and destroy infected plant debris after harvest",
            "Space plants adequately to improve air circulation",
            "Water at the base (drip irrigation); avoid wetting leaves",
            "Apply balanced fertilizer to keep plants vigorous",
        ],
        "treatment": [
            "Remove and destroy severely infected leaves immediately",
            "Apply copper-based fungicides (copper oxychloride) at first signs",
            "Use chlorothalonil or mancozeb fungicides on a 7–10 day schedule",
            "Organic option: Neem oil spray every 7 days",
            "Biofungicide: Bacillus subtilis (Serenade) as preventive spray",
            "Ensure potassium-rich feeding to strengthen plant cell walls",
        ],
    },
    "Late Blight": {
        "severity": "severe",
        "description": (
            "Late Blight, caused by the oomycete Phytophthora infestans, is one of the most "
            "devastating plant diseases in history — it caused the Irish Potato Famine. "
            "Water-soaked lesions with white fuzzy growth on leaf undersides spread rapidly "
            "in cool, moist conditions, destroying entire crops within days."
        ),
        "pathogen": "Phytophthora infestans (oomycete/water mold)",
        "causes": [
            "Cool temperatures (10–20°C) combined with high humidity or rain",
            "Infected seed tubers or transplants",
            "Windborne spores from neighboring infected fields",
            "Prolonged leaf wetness (>10 hours)",
        ],
        "prevention": [
            "Plant resistant varieties (e.g., Sarpo Mira, Defender)",
            "Use certified disease-free seed potatoes/transplants",
            "Avoid planting in low-lying, poorly drained areas",
            "Hill up soil around potato stems to prevent spore infiltration",
            "Monitor weather forecasts — apply protectant fungicides before rain",
            "Destroy volunteer plants that harbor disease between seasons",
        ],
        "treatment": [
            "Remove and dispose of (do not compost) all infected plant material",
            "Apply systemic fungicides: metalaxyl/mancozeb combination products",
            "Phosphonate-based fungicides (potassium phosphonate) are effective",
            "Copper fungicides as organic option (preventive only)",
            "In severe cases, remove entire crop to prevent field spread",
            "Do not store visibly infected tubers — they will rot and spread disease",
        ],
    },
    "Bacterial Spot": {
        "severity": "moderate",
        "description": (
            "Bacterial Spot is caused by Xanthomonas species and affects peppers and tomatoes. "
            "Small, water-soaked spots appear on leaves, stems, and fruit, turning dark brown "
            "with yellow halos. Fruit lesions are raised, rough, and scab-like, reducing "
            "market value and plant vigor."
        ),
        "pathogen": "Xanthomonas campestris / X. vesicatoria (bacteria)",
        "causes": [
            "Warm temperatures (25–30°C) and wet, rainy conditions",
            "Infected seeds or transplants",
            "Splashing rain or overhead irrigation spreading bacteria",
            "Insects and tools acting as mechanical vectors",
            "Wounds in plant tissue from pruning or insects",
        ],
        "prevention": [
            "Start with certified pathogen-free seeds — hot water treat at 50°C for 25 min",
            "Purchase disease-free transplants from reputable nurseries",
            "Avoid working in plants when foliage is wet",
            "Disinfect tools with 10% bleach solution between plants",
            "Use drip irrigation to keep foliage dry",
            "Plant resistant varieties where available",
        ],
        "treatment": [
            "Apply copper-based bactericides preventively and at first signs",
            "Combination sprays of copper + mancozeb improve efficacy",
            "Remove severely infected leaves and fruit",
            "Streptomycin sprays (where legally permitted) for severe outbreaks",
            "Biobactericide: Bacillus subtilis products as organic option",
        ],
    },
    "Apple Scab": {
        "severity": "moderate",
        "description": (
            "Apple Scab, caused by Venturia inaequalis, is the most economically important "
            "disease of apple worldwide. Olive-green to black velvety spots appear on leaves "
            "and fruit, causing defoliation, misshapen fruit, and significant crop losses in "
            "wet seasons."
        ),
        "pathogen": "Venturia inaequalis (fungus)",
        "causes": [
            "Cool, wet spring weather (16–24°C with rain or dew)",
            "Overwintering spores in fallen infected leaves",
            "Prolonged leaf wetness enabling spore germination",
            "Poorly pruned, dense canopies with poor air flow",
        ],
        "prevention": [
            "Plant resistant varieties: Liberty, Freedom, Enterprise, Redfree",
            "Collect and destroy fallen leaves in autumn",
            "Prune for open canopy structure to improve airflow and drying",
            "Apply lime sulfur during dormancy to kill overwintering spores",
            "Begin protective fungicide program at green tip growth stage",
        ],
        "treatment": [
            "Apply fungicides (captan, myclobutanil, or trifloxystrobin) at 7–10 day intervals",
            "Sulfur-based fungicides effective as organic option",
            "Apply potassium bicarbonate sprays to reduce existing infections",
            "Remove and dispose of infected fruit and leaves",
            "Kaolin clay creates a physical barrier on fruit surfaces",
        ],
    },
    "Black Rot": {
        "severity": "moderate-severe",
        "description": (
            "Black Rot in grapes and apples is caused by fungi (Guignardia bidwellii in grapes, "
            "Botryosphaeria obtusa in apples). On grapes it causes leaf spots with dark borders "
            "and mummified berries; on apples it causes leaf spots, fruit rot, and cankers that "
            "girdle branches."
        ),
        "pathogen": "Guignardia bidwellii (grapes) / Botryosphaeria obtusa (apples)",
        "causes": [
            "Warm, moist weather during the growing season",
            "Overwintering in mummified fruit and infected wood/cankers",
            "Splashing rain distributing spores to healthy tissue",
            "Pruning wounds as entry points for infection",
        ],
        "prevention": [
            "Remove and destroy all mummified fruit at end of season",
            "Prune out cankered wood, cutting 15 cm below visible infection",
            "Train vines/branches for good air circulation",
            "Avoid wetting foliage; use drip irrigation",
            "Apply dormant copper sprays before bud break",
        ],
        "treatment": [
            "Apply captan, myclobutanil, or mancozeb fungicides from bud break",
            "Critical spray timing: pre-bloom through early fruit development",
            "Remove infected berries/fruit immediately to reduce spore load",
            "For organic control: copper hydroxide + sulfur combination",
        ],
    },
    "Powdery Mildew": {
        "severity": "mild-moderate",
        "description": (
            "Powdery Mildew is a fungal disease affecting many plants, characterized by a "
            "distinctive white or grayish powdery coating on leaf surfaces, stems, and sometimes "
            "fruit. Unlike most fungi, it thrives in warm, dry conditions with high humidity — "
            "not actual rain. It weakens plants by reducing photosynthesis."
        ),
        "pathogen": "Erysiphe / Podosphaera / Sphaerotheca species (obligate fungi)",
        "causes": [
            "Warm days (20–27°C) combined with cool nights creating dew",
            "High humidity without rain (60–90% RH)",
            "Poor air circulation in dense plantings",
            "Excess nitrogen fertilization producing lush, susceptible growth",
            "Crowded, shaded conditions",
        ],
        "prevention": [
            "Choose resistant varieties whenever available",
            "Plant in full sun with adequate spacing for airflow",
            "Avoid excess nitrogen fertilization",
            "Water in the morning so plants dry before nightfall",
            "Prune for open canopy structure",
        ],
        "treatment": [
            "Apply sulfur-based fungicides at first signs (very effective)",
            "Potassium bicarbonate sprays are a highly effective organic option",
            "Neem oil spray every 7 days controls established infections",
            "Milk spray (40% milk : 60% water) — proven effective in studies",
            "Remove the most severely infected growth",
            "Apply synthetic fungicides (myclobutanil, trifloxystrobin) for severe cases",
        ],
    },
    "Leaf Scorch": {
        "severity": "mild",
        "description": (
            "Leaf Scorch in strawberries is caused by Diplocarpon earliana. It appears as "
            "small, irregular purple to reddish-purple spots on leaf surfaces that enlarge "
            "and develop tan or gray centers. Heavy infections cause leaves to appear 'scorched' "
            "and can weaken plants, reducing runner production and fruit yield."
        ),
        "pathogen": "Diplocarpon earliana (fungus)",
        "causes": [
            "Warm, wet conditions during the growing season",
            "Dense planting limiting air circulation",
            "Overhead irrigation keeping foliage wet",
            "Infected plant material introduced at planting",
        ],
        "prevention": [
            "Plant resistant varieties where available",
            "Use certified disease-free transplants",
            "Maintain plant spacing for good air circulation",
            "Use drip or furrow irrigation — avoid wetting leaves",
            "Renovate strawberry beds annually by mowing and thinning",
        ],
        "treatment": [
            "Apply captan or copper fungicide at first signs of disease",
            "Remove and dispose of heavily infected leaves",
            "Improve air circulation by thinning dense plantings",
            "Maintain good fertility to keep plants vigorous",
        ],
    },
    "Cedar Apple Rust": {
        "severity": "moderate",
        "description": (
            "Cedar Apple Rust is caused by Gymnosporangium juniperi-virginianae, a fascinating "
            "fungus that requires two host plants to complete its life cycle: Eastern red cedar "
            "(Juniperus) and apple trees. Bright orange-yellow spots appear on apple leaves in "
            "spring, and infected leaves may drop prematurely."
        ),
        "pathogen": "Gymnosporangium juniperi-virginianae (fungus, requires two hosts)",
        "causes": [
            "Proximity to Eastern red cedar or juniper trees (alternate host)",
            "Wet spring weather when apple buds are opening",
            "Spores released from orange gelatinous galls on cedar trees during rain",
        ],
        "prevention": [
            "Plant cedar rust-resistant apple varieties (Liberty, Enterprise, Redfree)",
            "Remove Eastern red cedar and juniper from within 1–2 km if possible",
            "Inspect and remove orange galls from cedars in late winter",
            "Apply protective fungicides starting at pink bud stage in spring",
        ],
        "treatment": [
            "Apply myclobutanil or propiconazole fungicides preventively in spring",
            "Sulfur-based fungicides offer some protection when applied early",
            "Remove infected leaves from tree and ground to reduce spore load",
            "Once infection is established, fungicides halt spread but don't cure existing lesions",
        ],
    },
    "Haunglongbing (Citrus Greening)": {
        "severity": "severe",
        "description": (
            "Huanglongbing (HLB), also known as Citrus Greening, is the most destructive "
            "citrus disease in the world with no known cure. Caused by bacteria spread by "
            "the Asian citrus psyllid insect, infected trees produce small, bitter, "
            "misshapen fruit with green bottoms, and eventually die within years."
        ),
        "pathogen": "Candidatus Liberibacter asiaticus (bacteria), spread by Diaphorina citri (psyllid insect)",
        "causes": [
            "Asian citrus psyllid (Diaphorina citri) feeding on and infecting trees",
            "Infected budwood or nursery stock introduced to orchards",
            "Rapid psyllid population explosion in warm climates",
        ],
        "prevention": [
            "Control Asian citrus psyllid populations with systemic insecticides",
            "Never move citrus plant material from HLB-affected areas",
            "Inspect trees regularly for psyllid presence and HLB symptoms",
            "Plant certified HLB-free nursery stock only",
            "Remove infected trees promptly to prevent spread",
        ],
        "treatment": [
            "No cure exists currently — this is a terminal disease",
            "Thermotherapy (heat treatment) is experimental and not commercially viable",
            "Nutritional supplementation (micronutrients) extends productive life",
            "Aggressive psyllid control slows disease spread to other trees",
            "Research into resistant varieties and bactericides is ongoing",
        ],
    },
    "Septoria Leaf Spot": {
        "severity": "moderate",
        "description": (
            "Septoria Leaf Spot, caused by Septoria lycopersici, is one of the most common "
            "tomato diseases. It produces small, circular spots (3–5 mm) with dark brown borders "
            "and tan or gray centers, often with tiny black dots (pycnidia) inside. "
            "Lower leaves are infected first, with disease moving upward, causing defoliation."
        ),
        "pathogen": "Septoria lycopersici (fungus)",
        "causes": [
            "Warm (20–25°C), wet weather or high humidity",
            "Infected soil or plant debris from previous season",
            "Splashing water spreading spores from soil to leaves",
            "Overhead irrigation wetting foliage",
        ],
        "prevention": [
            "Rotate crops — avoid planting tomatoes in same area for 2+ years",
            "Mulch soil to prevent spore splash from soil surface",
            "Remove infected leaves at first signs of disease",
            "Use drip irrigation; water in mornings to allow drying",
            "Stake and prune for good air circulation",
        ],
        "treatment": [
            "Remove and destroy infected leaves (do not compost)",
            "Apply copper-based fungicide at first signs",
            "Chlorothalonil or mancozeb fungicides applied every 7–10 days",
            "Organic option: Neem oil or Bacillus subtilis biofungicide",
        ],
    },
    "Tomato Yellow Leaf Curl Virus": {
        "severity": "severe",
        "description": (
            "Tomato Yellow Leaf Curl Virus (TYLCV) is a devastating begomovirus spread "
            "by the silverleaf whitefly (Bemisia tabaci). Infected plants show upward "
            "leaf curling, yellowing (chlorosis), stunting, and drastically reduced fruit "
            "production. There is no cure once a plant is infected."
        ),
        "pathogen": "Tomato yellow leaf curl virus (TYLCV) — transmitted by Bemisia tabaci (whitefly)",
        "causes": [
            "Whitefly feeding and inoculating plants with the virus",
            "Infected transplants introduced from nurseries",
            "Weed reservoirs harboring the virus between seasons",
            "Warm climates that support year-round whitefly populations",
        ],
        "prevention": [
            "Use TYLCV-resistant or tolerant tomato varieties",
            "Install reflective aluminum mulch to repel whiteflies",
            "Use yellow sticky traps to monitor and reduce whitefly populations",
            "Protect seedlings with insect-proof mesh in nursery",
            "Remove and destroy infected plants and weeds promptly",
            "Apply systemic insecticides (imidacloprid) to control whitefly vectors",
        ],
        "treatment": [
            "No cure for infected plants — remove and destroy symptomatic plants",
            "Control whitefly populations with insecticides to prevent spread",
            "Mineral oil sprays reduce whitefly transmission rates",
            "Kaolin clay creates physical barrier deterring whitefly landing",
        ],
    },
    "Tomato Mosaic Virus": {
        "severity": "moderate",
        "description": (
            "Tomato Mosaic Virus (ToMV) causes a distinctive light and dark green mottled "
            "mosaic pattern on leaves, often with leaf distortion, reduced leaf size, and "
            "stunted growth. Fruit may show internal browning. The virus is extremely stable "
            "and spreads easily through mechanical contact."
        ),
        "pathogen": "Tomato mosaic virus (ToMV) — mechanically transmitted",
        "causes": [
            "Handling infected plants then touching healthy plants (hands, tools)",
            "Contaminated seed (virus persists in seed coat)",
            "Grafting with infected rootstock or scion",
            "Tobacco products introducing Tobacco mosaic virus (close relative)",
        ],
        "prevention": [
            "Use certified virus-free seeds and transplants",
            "Wash hands thoroughly before working with plants; after touching tobacco",
            "Disinfect all tools with 10% bleach or 70% alcohol between cuts",
            "Plant resistant varieties (carrying Tm-2 gene)",
            "Do not smoke near tomato plants",
        ],
        "treatment": [
            "No chemical cure for viral infections",
            "Remove and destroy severely infected plants",
            "Wash tools and hands frequently during any work",
            "Maintain plant vigor with balanced nutrition to minimize yield loss",
        ],
    },
    "Spider Mites": {
        "severity": "mild-moderate",
        "description": (
            "Spider mites (Tetranychus urticae) are tiny arachnids, not insects, that "
            "feed on plant cell contents, causing bronze or silver stippling on leaf surfaces, "
            "fine webbing under leaves, and eventual leaf browning and drop. Hot, dry conditions "
            "cause rapid population explosions."
        ),
        "pathogen": "Tetranychus urticae (two-spotted spider mite — arachnid, not fungal/bacterial)",
        "causes": [
            "Hot, dry weather accelerating mite reproduction (a generation in 5 days at 30°C)",
            "Dusty conditions that kill mite predators",
            "Overuse of broad-spectrum insecticides eliminating natural predators",
            "Water-stressed plants more susceptible to mite damage",
        ],
        "prevention": [
            "Maintain plant hydration — mites thrive on drought-stressed plants",
            "Spray foliage with water to knock off mites and increase humidity",
            "Encourage natural predators: predatory mites, ladybugs, lacewings",
            "Avoid broad-spectrum insecticides that kill beneficial insects",
            "Monitor plants regularly, especially undersides of leaves",
        ],
        "treatment": [
            "Strong water sprays dislodge and kill mites (repeat every 2–3 days)",
            "Neem oil or insecticidal soap applied to undersides of leaves",
            "Release predatory mites (Phytoseiulus persimilis) as biological control",
            "Miticide (acaricide) sprays: bifenazate, spiromesifen for severe infestations",
            "Ensure multiple spray applications to catch all life stages",
        ],
    },
    "Target Spot": {
        "severity": "moderate",
        "description": (
            "Target Spot of tomato is caused by Corynespora cassiicola and produces "
            "circular lesions with concentric rings resembling a target or bull's eye. "
            "Spots appear on leaves, stems, and fruit, causing defoliation and yield "
            "reduction in warm, humid conditions."
        ),
        "pathogen": "Corynespora cassiicola (fungus)",
        "causes": [
            "Warm temperatures (25–30°C) with high humidity",
            "Prolonged leaf wetness from rain or overhead irrigation",
            "Dense canopy limiting air circulation",
            "Infected crop debris in soil",
        ],
        "prevention": [
            "Improve canopy airflow through staking and pruning",
            "Use drip irrigation and avoid overhead watering",
            "Rotate crops away from tomatoes/Solanaceae for 2+ years",
            "Apply preventive fungicides in warm, humid conditions",
        ],
        "treatment": [
            "Apply chlorothalonil, mancozeb, or azoxystrobin fungicides",
            "Remove infected leaves to reduce inoculum levels",
            "Copper fungicides as organic option, though less effective",
        ],
    },
    "Leaf Mold": {
        "severity": "moderate",
        "description": (
            "Leaf Mold is caused by Passalora fulva (syn. Fulvia fulva) and is primarily "
            "a problem in greenhouse tomatoes. Pale greenish-yellow spots appear on leaf "
            "upper surfaces, while olive-green to brown velvety mold develops underneath. "
            "Affected leaves curl, wither, and drop, reducing photosynthetic area and yield."
        ),
        "pathogen": "Passalora fulva (fungus)",
        "causes": [
            "High humidity (>85% RH) — primary driver",
            "Poor ventilation in greenhouse or polytunnel conditions",
            "Temperatures between 22–24°C favoring sporulation",
            "Infected plant debris or spores overwintering in structures",
        ],
        "prevention": [
            "Maintain relative humidity below 85% through ventilation",
            "Increase plant spacing and prune lower leaves for airflow",
            "Avoid overhead watering; water early in the day",
            "Use resistant varieties: many modern hybrids carry Cf resistance genes",
            "Disinfect greenhouse structures between crops",
        ],
        "treatment": [
            "Improve ventilation immediately as first response",
            "Remove and destroy infected leaves",
            "Apply chlorothalonil or copper-based fungicides",
            "Mancozeb or iprodione fungicides for more severe cases",
        ],
    },
    "Cercospora Leaf Spot": {
        "severity": "mild-moderate",
        "description": (
            "Cercospora Leaf Spot (also called Gray Leaf Spot) in corn is caused by "
            "Cercospora zeae-maydis. It produces rectangular, tan to gray lesions running "
            "parallel to leaf veins, giving infected leaves a scorched appearance. "
            "Severe infection reduces photosynthesis and can cause significant yield losses."
        ),
        "pathogen": "Cercospora zeae-maydis (fungus)",
        "causes": [
            "High humidity and moderate temperatures (22–30°C)",
            "Minimum tillage leaving infected residue on soil surface",
            "Dense corn canopy limiting air movement",
            "Continuous corn cropping without rotation",
        ],
        "prevention": [
            "Plant resistant hybrid varieties — most important management strategy",
            "Rotate to non-corn crops for at least one year",
            "Till to bury infected residue from previous seasons",
            "Scout fields regularly from early silking stage onward",
        ],
        "treatment": [
            "Apply strobilurin fungicides (azoxystrobin, pyraclostrobin) at early stages",
            "Triazole fungicides (propiconazole) effective against Cercospora",
            "Economic threshold: apply only if disease is significant at or before tasseling",
        ],
    },
    "Common Rust": {
        "severity": "mild-moderate",
        "description": (
            "Common Rust of corn is caused by Puccinia sorghi and recognized by "
            "brick-red to brown oval pustules scattered on both leaf surfaces. "
            "Pustules rupture and release rust-colored spores. Generally manageable "
            "in field corn but can be severe in sweet corn and susceptible hybrids."
        ),
        "pathogen": "Puccinia sorghi (rust fungus)",
        "causes": [
            "Cool nights (16–23°C) with warm days and high relative humidity",
            "Airborne spore dispersal over long distances from southern regions",
            "Susceptible hybrid selection",
        ],
        "prevention": [
            "Plant resistant or tolerant hybrid varieties",
            "Plant early to avoid high-spore-load periods",
            "Monitor crops from knee-high stage onward",
        ],
        "treatment": [
            "Apply triazole or strobilurin fungicides if disease is progressing rapidly",
            "Fungicide application most beneficial in sweet corn or seed corn",
            "In field corn, treat only if upper leaves are infected before tasseling",
        ],
    },
    "Northern Leaf Blight": {
        "severity": "moderate-severe",
        "description": (
            "Northern Leaf Blight (NLB) of corn is caused by Exserohilum turcicum. "
            "Large (2.5–15 cm), cigar-shaped gray-green to tan lesions appear on leaves. "
            "Severe early infections before tasseling significantly reduce yield "
            "by limiting photosynthetic area during grain fill."
        ),
        "pathogen": "Exserohilum turcicum (fungus)",
        "causes": [
            "Moderate temperatures (18–27°C) with extended periods of leaf wetness",
            "High relative humidity and overcast, cloudy weather",
            "Infected residue on soil surface from previous corn crop",
            "Susceptible hybrid varieties planted in continuous corn rotations",
        ],
        "prevention": [
            "Plant resistant hybrid varieties — most effective management tool",
            "Crop rotation away from corn reduces residue inoculum",
            "Tillage to bury infected residue",
            "Scout fields from V6 stage through grain fill",
        ],
        "treatment": [
            "Apply fungicides (triazoles + strobilurins) at or before tasseling if risk is high",
            "Propiconazole, tebuconazole, or azoxystrobin + propiconazole combinations",
            "Economic threshold: significant disease on third leaf below ear at tasseling",
        ],
    },
    "Esca (Black Measles)": {
        "severity": "severe",
        "description": (
            "Esca (Black Measles) is a complex grapevine trunk disease caused by a consortium "
            "of wood-decaying fungi. It produces leaf symptoms of tiger-striping (yellow/red "
            "bands between veins), berry spotting (black measles), and internal wood decay. "
            "Chronic esca slowly debilitates vines over years; apoplectic form kills vines rapidly."
        ),
        "pathogen": "Phaeomoniella chlamydospora, Phaeoacremonium spp., Fomitiporia mediterranea (fungal complex)",
        "causes": [
            "Pruning wounds are primary entry points for fungal infection",
            "Large pruning cuts that are slow to heal",
            "Stressful conditions: drought, waterlogging, nutritional deficiency",
            "Old vines more susceptible due to accumulated wood damage",
        ],
        "prevention": [
            "Prune during dry weather to minimize wound exposure time",
            "Make small cuts — large pruning cuts heal more slowly",
            "Apply wound protectants (Trichoderma-based products) immediately after pruning",
            "Use double-pruning technique: leave a long spur initially, cut back later",
            "Maintain vine vigor through balanced nutrition and irrigation",
        ],
        "treatment": [
            "No systemic fungicide treatment is currently effective once established",
            "Remedial surgery: cut out infected wood until clean white wood is visible",
            "Protect cut surfaces with wound sealants containing fungicide",
            "Replace severely affected vines (pull and replant)",
            "Sodium arsenite (banned in EU) was historically used but is no longer available",
        ],
    },
    "Leaf Blight": {
        "severity": "moderate",
        "description": (
            "Grape Leaf Blight (Isariopsis Leaf Spot) is caused by Pseudocercospora vitis "
            "and causes irregular dark brown lesions on older leaves, leading to premature "
            "defoliation that weakens vines and reduces fruit quality and the following "
            "season's bud hardiness."
        ),
        "pathogen": "Pseudocercospora vitis (fungus)",
        "causes": [
            "Warm, humid weather late in the growing season",
            "Poor canopy management limiting airflow",
            "Infected leaf debris overwintering in vineyard",
        ],
        "prevention": [
            "Shoot positioning and leaf removal for better air circulation",
            "Remove fallen leaves from vineyard floor",
            "Apply fungicides if disease history warrants preventive treatment",
        ],
        "treatment": [
            "Apply copper or mancozeb fungicides when symptoms appear",
            "Remove heavily infected leaves",
            "Improve canopy management for next season",
        ],
    },
    "Healthy": {
        "severity": "none",
        "description": (
            "The plant appears to be in good health with no visible signs of disease, "
            "pest damage, or nutritional deficiency. Continue with regular care practices "
            "to maintain plant vigor."
        ),
        "pathogen": "None detected",
        "causes": [],
        "prevention": [
            "Continue regular watering, fertilization, and monitoring",
            "Inspect plants weekly for early signs of problems",
            "Practice crop rotation to prevent disease buildup in soil",
            "Maintain good garden hygiene — remove dead or diseased material promptly",
        ],
        "treatment": [
            "No treatment needed",
            "Maintain current care practices",
            "Ensure adequate nutrition for continued plant health",
        ],
    },
}
