import json
from pathlib import Path

# Load both files
raw_path = Path("assets/za/Raw/trdata_array.json")
assets_path = Path("src/skypy/assets/za/trdata_array.json")

with open(raw_path) as f:
    raw_data = json.load(f)["Table"]

with open(assets_path) as f:
    assets_data = json.load(f)["values"]

# Build index by trainer ID for quick lookup
raw_by_id = {entry["TrId"]: entry for entry in raw_data}

# Mappings for different categorical fields
mappings = {
    "devId": {},  # Pokemon species
    "ballId": {},  # Ball types
    "wazaId": {},  # Moves
    "seikaku": {},  # Natures
    "item": {},  # Items
    "tokusei": {},  # Abilities
    "rareType": {},  # Rarity
    "rank": {},  # Rank
}

# Field name conversions (camelCase -> PascalCase)
field_map = {
    "devId": "DevId",
    "ballId": "BallId",
    "wazaId": "WazaId",
    "seikaku": "Seikaku",
    "item": "Item",
    "tokusei": "Tokusei",
    "rareType": "RareType",
    "rank": "Rank",
}

for asset_entry in assets_data:
    trid = asset_entry["trid"]
    raw_entry = raw_by_id.get(trid)
    if not raw_entry:
        continue

    # Process each pokemon slot (poke1-poke6)
    for i in range(1, 7):
        poke_key = f"poke{i}"
        Poke_key = f"Poke{i}"

        asset_poke = asset_entry.get(poke_key, {})
        raw_poke = raw_entry.get(Poke_key, {})

        # Map direct fields
        for camel, pascal in field_map.items():
            if camel in asset_poke and pascal in raw_poke:
                str_val = asset_poke[camel]
                int_val = raw_poke[pascal]
                if str_val and isinstance(str_val, str):
                    mappings[camel][str_val] = int_val

        # Map waza fields (nested)
        for w in range(1, 5):
            waza_key = f"waza{w}"
            Waza_key = f"Waza{w}"
            asset_waza = asset_poke.get(waza_key, {})
            raw_waza = raw_poke.get(Waza_key, {})
            if "wazaId" in asset_waza and "WazaId" in raw_waza:
                str_val = asset_waza["wazaId"]
                int_val = raw_waza["WazaId"]
                if str_val and isinstance(str_val, str):
                    mappings["wazaId"][str_val] = int_val

# Write each mapping to a file
output_dir = Path("src/skypy/assets/za/mappings")
output_dir.mkdir(exist_ok=True)

for name, mapping in mappings.items():
    if mapping:  # Only write non-empty mappings
        sorted_mapping = dict(sorted(mapping.items(), key=lambda x: x[1]))
        with open(output_dir / f"{name}.json", "w") as f:
            json.dump(sorted_mapping, f, indent=2)
        print(f"Wrote {len(mapping)} entries to {name}.json")
