import csv
import random

# --- Helper: round to nearest 0.05 ---
def round_to_005(x):
    return round(round(x / 0.05) * 0.05, 2)

# --- Step 1: Card type effects ---
card_type_effects = {
    "Speed":   {"Speed": 1.0, "Power": 0.3},
    "Power":   {"Power": 1.0, "Stamina": 0.3},
    "Stamina": {"Stamina": 1.0, "Guts": 0.3},
    "Guts":    {"Guts": 1.0, "Speed": 0.2, "Power": 0.2},
    "Wit":     {"Wit": 1.0, "Speed": 0.3},
}

# --- Step 2: Options ---
distance_options = ["sprint", "mile", "medium", "long"]
strategy_options = ["front", "pace", "late", "end"]
location_options = ["Tokyo", "Kyoto", "Sapporo", "Hakodate", "Nakayama"]
terrain_options = ["turf", "dirt"]
season_options = ["spring", "summer", "fall", "winter"]
weather_options = ["sunny", "rainy", "cloudy"]
ground_options = ["firm", "soft", "heavy"]

# --- Step 3: Generate cards ---
num_cards = 150
cards = []

for i in range(num_cards):
    card = {
        "card_name": f"Card_{i}",
        "card_type": random.choice(list(card_type_effects.keys())),

        # probability-based skill assignment
        "distance_skills": [d for d in distance_options if random.random() < 0.15],
        "strategy_skills": [s for s in strategy_options if random.random() < 0.15],
        "location_skills": [l for l in location_options if random.random() < 0.15],
        "terrain_skills": [t for t in terrain_options if random.random() < 0.15],
        "season_skills": [s for s in season_options if random.random() < 0.15],
        "weather_skills": [w for w in weather_options if random.random() < 0.15],

        # firm-only skill
        "ground_skills": ["firm"] if random.random() < 0.15 else [],

        "general_skill": 1 if random.random() < 0.25 else 0,
        "training_effectiveness": round_to_005(random.uniform(0.05, 0.2)),
        "specialty_priority": round_to_005(random.uniform(0.1, 1.0)),
        "friendship_bonus": round_to_005(random.uniform(0.1, 0.4)),
        "mood_effect": round_to_005(random.uniform(0.0, 0.5)),
    }
    cards.append(card)

# --- Step 4: Generate races ---
num_races = 65
races = []

for _ in range(num_races):
    race = {
        "location": random.choice(location_options),
        "terrain": random.choice(terrain_options),
        "distance": random.choice(distance_options),
        "season": random.choice(season_options),
        "weather": random.choice(weather_options),
        "ground": random.choice(ground_options),
    }
    races.append(race)

# --- Step 5: Compute performance ---
def compute_performance(card, race):
    effects = card_type_effects[card["card_type"]]

    base = 100

    modifier = (
        1
        + card["training_effectiveness"]
        + card["specialty_priority"]
        + card["friendship_bonus"]
    )

    mood_multiplier = 1 + (0.2 * (1 + card["mood_effect"]))

    speed = base * effects.get("Speed", 0) * modifier * mood_multiplier
    wit = base * effects.get("Wit", 0) * modifier * mood_multiplier
    stamina = base * effects.get("Stamina", 0) * modifier * mood_multiplier
    power = base * effects.get("Power", 0) * modifier * mood_multiplier

    stat_score = (
        speed * 4 +
        wit * 3 +
        stamina * 3 +
        power * 2
    )

    match_score = 0

    if race["distance"] in card["distance_skills"]:
        match_score += 2

    if race["location"] in card["location_skills"]:
        match_score += 1

    if race["terrain"] in card["terrain_skills"]:
        match_score += 1

    if race["season"] in card["season_skills"]:
        match_score += 1

    if race["weather"] in card["weather_skills"]:
        match_score += 1

    if race["ground"] in card["ground_skills"]:
        match_score += 1

    if card["general_skill"]:
        match_score += 1

    perf_score = stat_score + (match_score * 50)

    return round(perf_score, 2)

# --- Step 6: Write CSV ---
csv_columns = [
    "card_name", "card_type", "distance_skills", "strategy_skills",
    "location_skills", "terrain_skills", "season_skills",
    "weather_skills", "ground_skills",
    "general_skill", "training_effectiveness", "specialty_priority",
    "friendship_bonus", "mood_effect",
    "location", "terrain", "distance", "season", "weather", "ground",
    "performance_score"
]

with open("uma_synthetic.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for card in cards:
        for race in races:
            row = {**card, **race}

            row["performance_score"] = compute_performance(card, race)

            # Convert lists to strings
            row["distance_skills"] = ";".join(card["distance_skills"])
            row["strategy_skills"] = ";".join(card["strategy_skills"])
            row["location_skills"] = ";".join(card["location_skills"])
            row["terrain_skills"] = ";".join(card["terrain_skills"])
            row["season_skills"] = ";".join(card["season_skills"])
            row["weather_skills"] = ";".join(card["weather_skills"])
            row["ground_skills"] = ";".join(card["ground_skills"])

            writer.writerow(row)

print("CSV generation complete!")
