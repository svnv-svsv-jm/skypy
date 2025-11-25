import json
import os
import random
import re
import shutil
import subprocess
import traceback

# ===== Allowed devNo list for encounters/starters =====
ALLOWED_DEVNOS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    13,
    14,
    15,
    16,
    17,
    18,
    23,
    24,
    25,
    26,
    35,
    36,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    79,
    80,
    98,
    93,
    94,
    95,
    115,
    120,
    121,
    123,
    127,
    129,
    130,
    133,
    134,
    135,
    136,
    142,
    147,
    148,
    149,
    150,
    152,
    153,
    154,
    158,
    159,
    160,
    167,
    168,
    172,
    173,
    179,
    180,
    181,
    196,
    197,
    199,
    208,
    212,
    214,
    225,
    227,
    228,
    229,
    246,
    247,
    248,
    280,
    281,
    282,
    302,
    303,
    304,
    305,
    306,
    307,
    308,
    309,
    310,
    315,
    318,
    319,
    322,
    333,
    334,
    353,
    354,
    359,
    361,
    362,
    371,
    372,
    373,
    374,
    375,
    376,
    406,
    407,
    427,
    428,
    443,
    444,
    448,
    449,
    450,
    459,
    460,
    470,
    471,
    475,
    478,
    498,
    499,
    500,
    504,
    505,
    511,
    512,
    513,
    514,
    515,
    516,
    529,
    530,
    531,
    543,
    544,
    545,
    551,
    552,
    553,
    559,
    560,
    568,
    569,
    582,
    583,
    584,
    587,
    602,
    603,
    604,
    607,
    608,
    609,
    618,
    701,
    702,
    703,
    704,
    705,
    706,
    707,
    708,
    709,
    710,
    711,
    712,
    713,
    714,
    715,
    716,
    717,
    718,
    719,
    720,
    721,
    722,
    723,
    724,
    725,
    726,
    727,
    728,
    729,
    730,
    731,
    732,
    733,
    734,
    735,
    736,
    737,
    738,
    739,
    740,
    741,
    742,
    743,
    744,
    745,
    746,
    747,
    748,
    749,
    751,
    752,
    753,
    754,
    755,
    756,
    757,
    758,
    759,
    760,
    761,
    762,
    763,
    764,
    765,
    766,
    767,
    768,
    769,
    770,
    772,
    773,
    774,
    856,
    923,
]

# Starter entries (what you actually receive) — IN pokemon_data_array.json
STARTER_IDS = [
    "test_encount_init_poke_0",
    "test_encount_init_poke_1",
    "test_encount_init_poke_2",
]

# Linked NPC entries whose devNo should match the starter's new devNo — IN pokemon_data_array.json
STARTER_TO_NPC = {
    "test_encount_init_poke_0": "npc_pokemon_152",
    "test_encount_init_poke_1": "npc_pokemon_498",
    "test_encount_init_poke_2": "npc_pokemon_158",
}

# Regex for encounters devNo in encount_data_array.json
DEVNO_REGEX = re.compile(r'("devNo"\s*:\s*)(\d+)')

# ===== Paths =====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "Input")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Output")
BAT_FILE = os.path.join(SCRIPT_DIR, "Convert To Bin.bat")


# ===== Auto-clean output before running =====


def auto_clean():
    print("=== Cleaning old output files ===")

    # Remove Output/randomizer folder if it exists
    mod_root = os.path.join(OUTPUT_DIR, "randomizer")
    if os.path.isdir(mod_root):
        shutil.rmtree(mod_root)
        print(f"[CLEAN] Removed folder: {mod_root}")

    # Remove .bin files in Output/
    if os.path.isdir(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            if file.lower().endswith(".bin"):
                fpath = os.path.join(OUTPUT_DIR, file)
                os.remove(fpath)
                print(f"[CLEAN] Removed file: {fpath}")
    else:
        # Make sure Output exists for later
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Remove Randomizer.zip if it exists
    zip_path = os.path.join(OUTPUT_DIR, "Randomizer.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"[CLEAN] Removed zip: {zip_path}")

    print("[CLEAN] Cleanup complete.\n")


# ===== Utility helpers =====


def yes_input(prompt: str) -> bool:
    """Return True if user types yes/y (case-insensitive), else False."""
    ans = input(prompt).strip().lower()
    return ans in ("y", "yes")


def randomize_number(original, pool):
    """Pick a random devNo from pool, not equal to original."""
    choices = [n for n in pool if n != original]
    if not choices:
        return original
    return random.choice(choices)


# ===== 1. Randomize encounters (encount_data_array.json) =====


def randomize_encounters():
    path = os.path.join(INPUT_DIR, "encount_data_array.json")
    if not os.path.isfile(path):
        print(f"[WARN] {path} not found, skipping encounters.")
        return

    with open(path, encoding="utf-8") as f:
        text = f.read()

    def replacer(m):
        old = int(m.group(2))
        new = randomize_number(old, ALLOWED_DEVNOS)
        return f"{m.group(1)}{new}"

    new_text = DEVNO_REGEX.sub(replacer, text)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

    print("[OK] Randomized encounters in encount_data_array.json")


# ===== 2. Randomize starters (devNo) + NPC overworld (devNo) in pokemon_data_array.json =====


def randomize_starters_and_npc_devno():
    path = os.path.join(INPUT_DIR, "pokemon_data_array.json")
    if not os.path.isfile(path):
        print(f"[WARN] {path} not found, skipping starters & overworld.")
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Flatten entries (values[] -> root[] list of dicts)
    entries = []
    for blk in data.get("values", []):
        root = blk.get("root", [])
        if isinstance(root, list):
            for e in root:
                if isinstance(e, dict):
                    entries.append(e)

    id_to_entry = {e.get("id"): e for e in entries if "id" in e}

    starter_new_devno = {}

    # Step 1: change devNo on the starter entries (test_encount_init_poke_*)
    for sid in STARTER_IDS:
        e = id_to_entry.get(sid)
        if not e or "devNo" not in e:
            print(
                f"[WARN] Starter entry {sid} not found in pokemon_data_array, skipping."
            )
            continue
        old_dev = int(e["devNo"])
        new_dev = randomize_number(old_dev, ALLOWED_DEVNOS)
        e["devNo"] = new_dev
        starter_new_devno[sid] = new_dev
        print(f"[INFO] Starter {sid}: devNo {old_dev} -> {new_dev}")

    # Step 2: change devNo on the linked npc_pokemon_* entries to match
    for sid, npc_id in STARTER_TO_NPC.items():
        if sid not in starter_new_devno:
            continue
        npc = id_to_entry.get(npc_id)
        if not npc:
            print(
                f"[WARN] NPC entry {npc_id} not found in pokemon_data_array, skipping."
            )
            continue

        if "devNo" not in npc:
            print(f"[WARN] NPC {npc_id} has no devNo field, skipping.")
            continue

        old_dev = int(npc["devNo"])
        new_dev = starter_new_devno[sid]
        npc["devNo"] = new_dev
        print(f"[INFO] NPC {npc_id}: devNo {old_dev} -> {new_dev} (matching {sid})")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("[OK] Randomized starters + NPC overworld devNo in pokemon_data_array.json")


# ===== 3. Randomize trainers by devId only (trdata_array.json) =====


def randomize_trainers():
    """Randomizes trainer Pokémon species by shuffling devId among existing trainer mons.
    Moves stay as-is.
    """
    path = os.path.join(INPUT_DIR, "trdata_array.json")
    if not os.path.isfile(path):
        print(f"[WARN] {path} not found, skipping trainer randomization.")
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    rows = data.get("values", [])
    if not isinstance(rows, list):
        print("[WARN] trdata_array.json has unexpected structure.")
        return

    dev_ids = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        for i in range(1, 7):
            poke = row.get(f"poke{i}")
            if isinstance(poke, dict):
                dev = poke.get("devId")
                lvl = poke.get("level", 0)
                if (
                    isinstance(dev, str)
                    and dev not in ("DEV_NULL", "DEV_NONE")
                    and isinstance(lvl, int)
                    and lvl > 0
                ):
                    dev_ids.add(dev)

    dev_ids = sorted(dev_ids)
    if not dev_ids:
        print("[WARN] No trainer devIds found to randomize.")
        return

    print(f"[INFO] Trainer devId pool size: {len(dev_ids)}")

    changed_count = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        for i in range(1, 7):
            poke = row.get(f"poke{i}")
            if not isinstance(poke, dict):
                continue
            dev = poke.get("devId")
            lvl = poke.get("level", 0)

            if (
                not isinstance(dev, str)
                or dev in ("DEV_NULL", "DEV_NONE")
                or not isinstance(lvl, int)
                or lvl <= 0
            ):
                continue

            new_dev = random.choice(dev_ids)
            poke["devId"] = new_dev
            changed_count += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Randomized {changed_count} trainer Pokémon entries.")


# ===== 4. Run converter and build mod structure =====


def run_convert():
    if not os.path.isfile(BAT_FILE):
        print(
            f"[ERROR] '{BAT_FILE}' not found. Make sure the .bat is next to this script."
        )
        return
    print("[INFO] Running Convert To Bin.bat...")
    subprocess.run(["cmd", "/c", BAT_FILE], cwd=SCRIPT_DIR)
    print("[OK] Converter finished.")


def move_bins_and_zip():
    # Ensure Output exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clean old randomizer folder (just in case)
    mod_root = os.path.join(OUTPUT_DIR, "randomizer")
    if os.path.isdir(mod_root):
        shutil.rmtree(mod_root)

    world_root = os.path.join(mod_root, "world", "ik_data")

    # Pokémon field data
    enc_path = os.path.join(
        world_root, "field", "pokemon", "encount_data", "encount_data"
    )
    poke_path = os.path.join(
        world_root, "field", "pokemon", "pokemon_data", "pokemon_data"
    )

    # Trainer data (if present)
    tr_path = os.path.join(world_root, "trainer", "trdata")

    os.makedirs(enc_path, exist_ok=True)
    os.makedirs(poke_path, exist_ok=True)
    os.makedirs(tr_path, exist_ok=True)

    found_any = False
    for file in os.listdir(OUTPUT_DIR):
        if not file.lower().endswith(".bin"):
            continue
        src = os.path.join(OUTPUT_DIR, file)
        lower = file.lower()

        if "encount_data_array" in lower:
            dst = os.path.join(enc_path, "encount_data_array.bin")
            shutil.copy(src, dst)
            found_any = True
            print(f"[OK] Copied {file} -> {dst}")
        elif "pokemon_data_array" in lower:
            dst = os.path.join(poke_path, "pokemon_data_array.bin")
            shutil.copy(src, dst)
            found_any = True
            print(f"[OK] Copied {file} -> {dst}")
        elif "trdata_array" in lower:
            dst = os.path.join(tr_path, "trdata_array.bin")
            shutil.copy(src, dst)
            found_any = True
            print(f"[OK] Copied {file} -> {dst}")

    if not found_any:
        print(
            "[WARN] No .bin files were found in Output/. "
            "Check that Convert To Bin.bat ran correctly."
        )

    if found_any:
        zip_base = os.path.join(OUTPUT_DIR, "Randomizer")
        if os.path.exists(zip_base + ".zip"):
            os.remove(zip_base + ".zip")
        shutil.make_archive(zip_base, "zip", mod_root)
        print(f"[OK] Created {zip_base}.zip")
    else:
        print("[WARN] Skipping zip creation because no .bin files were copied.")


def main():
    random.seed()

    # CLEAN FIRST
    auto_clean()

    # === Menu ===
    do_encounters = yes_input("Randomize encounters? (yes/no): ")
    do_starters = yes_input("Randomize starters & overworld? (yes/no): ")
    do_trainers = yes_input("Randomize trainers? (yes/no): ")

    print("\n=== Starting randomizer with options ===")
    print(f"  Encounters: {'ON' if do_encounters else 'OFF'}")
    print(f"  Starters & overworld: {'ON' if do_starters else 'OFF'}")
    print(f"  Trainers: {'ON' if do_trainers else 'OFF'}\n")

    if do_encounters:
        print("=== Randomizing encounters (encount_data_array.json) ===")
        randomize_encounters()
    else:
        print("Skipping encounters.")

    if do_starters:
        print("\n=== Randomizing starters + overworld (pokemon_data_array.json) ===")
        randomize_starters_and_npc_devno()
    else:
        print("Skipping starters & overworld.")

    if do_trainers:
        print("\n=== Randomizing trainers (trdata_array.json) ===")
        randomize_trainers()
    else:
        print("Skipping trainers.")

    print("\n=== Converting JSON -> BIN ===")
    run_convert()

    print("\n=== Moving .bin files and creating zip ===")
    move_bins_and_zip()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n[ERROR] An exception occurred:")
        print(e)
        print("\nTraceback:")
        traceback.print_exc()
    finally:
        input("\nDone. Press ENTER to close this window...")
