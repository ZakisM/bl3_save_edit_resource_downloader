import csv
from pathlib import Path

import gspread
import requests


def format_info(info):
    info = info.replace("Dmg", "Damage")
    info = info.replace("dmg", "damage")
    info = info.replace("Acc. Bloom", "Acc Bloom")
    info = info.replace("Recoil W:", "Recoil Width:")
    info = info.replace("Recoil H:", "Recoil Height:")

    # Fix incorrect spelling
    info = info.replace("Amarea", "Amara")
    info = info.replace("enemry", "enemy")
    info = info.replace("Mazimum", "Maximum")
    info = info.replace("receieve", "receive")
    info = info.replace("additonal", "additional")
    info = info.replace("Unlease", "Unleash")
    info = info.replace("borken", "broken")
    info = info.replace("dmage", "damage")
    info = info.replace("Forify", "Fortify")
    info = info.replace("dropa ", "drop a")
    info = info.replace("Critcal", "Critical")
    info = info.replace("Maxium", "Maximum")
    info = info.replace("dealth", "dealt")
    info = info.replace("increasted", "increased")

    words = info.split(',')
    res = []

    for w in words:
        res.append(w.removeprefix(',').removesuffix(',').strip())

    res_joined = ', '.join(res)

    return res_joined.strip().removesuffix(',')


def download_inventory_parts():
    # Make output dir
    Path("./output/INV_PARTS").mkdir(parents=True, exist_ok=True)

    # Borderlands 3 Weapon/Item Parts + Weights
    print("Downloading Weapon Parts")
    weapons_csv_data = requests.get(
        "https://raw.githubusercontent.com/BLCM/bl3mods/master/Apocalyptech/dataprocessing/gun_balances.csv").content

    print("Downloading Shield Parts")
    shields_csv_data = requests.get(
        "https://raw.githubusercontent.com/BLCM/bl3mods/master/Apocalyptech/dataprocessing/shield_balances.csv").content

    print("Downloading Grenade Mod Parts")
    grenade_mods_csv_data = requests.get(
        "https://raw.githubusercontent.com/BLCM/bl3mods/master/Apocalyptech/dataprocessing/grenade_balances.csv").content

    print("Downloading Class Mod Parts")
    class_mods_csv_data = requests.get(
        "https://raw.githubusercontent.com/BLCM/bl3mods/master/Apocalyptech/dataprocessing/com_balances.csv").content

    print("Downloading Artifacts Parts")
    artifacts_csv_data = requests.get(
        "https://raw.githubusercontent.com/BLCM/bl3mods/master/Apocalyptech/dataprocessing/artifact_balances.csv").content

    items = [{"WEAPONS": weapons_csv_data}, {"SHIELDS": shields_csv_data}, {"GRENADE_MODS": grenade_mods_csv_data},
             {"CLASS_MODS": class_mods_csv_data}, {"ARTIFACTS": artifacts_csv_data}]

    parts_filenames = []

    for item in items:
        for name in item:
            data = item[name]

            filename = "output/INV_PARTS/INVENTORY_PARTS_{}.csv".format(name)
            parts_filenames.append(filename)
            print("Saving: {}".format(filename))

            with open(filename, "wb") as f:
                f.write(data)

    all_keys = ["Name", "Weapon Type", "Rarity", "Balance", "Category", "Min Parts", "Max Parts", "Weight", "Part",
                "Dependencies", "Excluders"]

    all_keys_len = len(all_keys)

    with open("output/INV_PARTS/INVENTORY_PARTS_ALL.csv", "w", newline="") as inv_parts_all:
        headers = ",".join(all_keys)
        inv_parts_all.write(headers + "\n")

        for filename in parts_filenames:
            with open(filename, "r") as f:
                csv_reader = csv.reader(f, delimiter=',')
                for idx, row in enumerate(csv_reader):
                    if idx == 0:
                        continue

                    if len(row) != all_keys_len:
                        row.insert(1, '')

                    for idx_item, item in enumerate(row):
                        if "," in item:
                            row[idx_item] = "\"{}\"".format(item)

                    inv_parts_all.write(",".join(row) + "\n")


def download_old_inventory_parts_info():
    # Make output dir
    Path("./output/INV_PARTS_INFO").mkdir(parents=True, exist_ok=True)

    # Borderlands 3 - Item parts/stats
    sh = gc.open_by_key("16b7bGPFKIrNg_cJm_WCMO6cKahexBs7BiJ6ja0RlD04")

    print("Downloading Artifacts, Shields and Grenades")
    artifact = sh.worksheet("Artifact")
    shield = sh.worksheet("Shield")
    grenade = sh.worksheet("Grenade")

    # Class mods
    print("Downloading Class Mods")
    fl4k_com = sh.worksheet("Fl4k COM")
    zane_com = sh.worksheet("Zane COM")
    amara_com = sh.worksheet("Amara COM")
    moze_com = sh.worksheet("Moze COM")

    # Pistols
    print("Downloading Pistols")
    ps_atl = sh.worksheet("PS_ATL")
    ps_cov = sh.worksheet("PS_COV")
    ps_dal = sh.worksheet("PS_DAL")
    ps_jak = sh.worksheet("PS_JAK")
    ps_mal = sh.worksheet("PS_MAL")
    ps_ted = sh.worksheet("PS_TED")
    ps_tor = sh.worksheet("PS_TOR")
    ps_vla = sh.worksheet("PS_VLA")

    pistols = [ps_atl, ps_cov, ps_dal, ps_jak, ps_mal, ps_ted, ps_tor, ps_vla]

    # Shotguns
    print("Downloading Shotguns")
    sg_hyp = sh.worksheet("SG_HYP")
    sg_jak = sh.worksheet("SG_JAK")
    sg_mal = sh.worksheet("SG_MAL")
    sg_ted = sh.worksheet("SG_TED")
    sg_tor = sh.worksheet("SG_TOR")

    shotguns = [sg_hyp, sg_jak, sg_mal, sg_ted, sg_tor]

    # Assault Rifles
    print("Downloading Assault Rifles")
    ar_atl = sh.worksheet("AR_ATL")
    ar_cov = sh.worksheet("AR_COV")
    ar_dal = sh.worksheet("AR_DAL")
    ar_jak = sh.worksheet("AR_JAK")
    ar_tor = sh.worksheet("AR_TOR")
    ar_vla = sh.worksheet("AR_VLA")

    assault_rifles = [ar_atl, ar_cov, ar_dal, ar_jak, ar_tor, ar_vla]

    # SMG's
    print("Downloading SMG's")
    sm_dal = sh.worksheet("SM_DAL")
    sm_hyp = sh.worksheet("SM_HYP")
    sm_mal = sh.worksheet("SM_MAL")
    sm_ted = sh.worksheet("SM_TED")

    smgs = [sm_dal, sm_hyp, sm_mal, sm_ted]

    # Sniper Rifles
    print("Downloading Sniper Rifles")
    sr_dal = sh.worksheet("SR_DAL")
    sr_hyp = sh.worksheet("SR_HYP")
    sr_jak = sh.worksheet("SR_JAK")
    sr_mal = sh.worksheet("SR_MAL")
    sr_vla = sh.worksheet("SR_VLA")

    sniper_rifles = [sr_dal, sr_hyp, sr_jak, sr_mal, sr_vla]

    # Heavy Weapons
    print("Downloading Heavy Weapons")
    hw_atl = sh.worksheet("HW_ATL")
    hw_cov = sh.worksheet("HW_COV")
    hw_tor = sh.worksheet("HW_TOR")
    hw_vla = sh.worksheet("HW_VLA")

    heavy_weapons = [hw_atl, hw_cov, hw_tor, hw_vla]

    print("Downloading Anointment's")
    anointment = sh.worksheet("Anointment")

    # Download Sheets that only have the part and effect (i.e key/val)
    effects_sheets = [artifact, shield, grenade, fl4k_com, zane_com, amara_com, moze_com, anointment]

    # Download Weapon Sheets that have the part and positives/negatives
    weapon_sheets_unflattened = [pistols, shotguns, assault_rifles, smgs, sniper_rifles, heavy_weapons]
    weapon_sheets = [item for sublist in weapon_sheets_unflattened for item in sublist]

    with open("output/INV_PARTS_INFO/INVENTORY_PARTS_INFO_ALL_OLD.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Part", "Positives", "Negatives", "Effects"])

        for sheet in effects_sheets:
            print("Saving: {}".format(sheet.title))
            for val in sheet.get_all_values():
                if len(val) >= 2:
                    part_name_split = val[0].split('.')
                    if len(part_name_split) == 2 and part_name_split[0] == part_name_split[1]:
                        if val[1].strip() != "" and val[1].strip() != "* Unknown":
                            part_name_s = part_name_split[0].strip()
                            effects_s = format_info(val[1].strip())

                            csv_row = [part_name_s, "", "", effects_s]
                            w.writerow(csv_row)

        for sheet in weapon_sheets:
            print("Saving: {}".format(sheet.title))
            for val in sheet.get_all_values():
                if len(val) >= 3:
                    part_name_split = val[0].split('.')
                    if len(part_name_split) == 2 and part_name_split[0] == part_name_split[1]:
                        if val[1].strip() == "-":
                            val[1] = ""

                        if val[2].strip() == "-":
                            val[2] = ""

                        if val[1].strip() == "" and val[2].strip() == "":
                            continue

                        part_name_s = part_name_split[0].strip()
                        positives_s = format_info(val[1])
                        negatives_s = format_info(val[2])

                        csv_row = [part_name_s, positives_s, negatives_s, ""]
                        w.writerow(csv_row)


def download_all_global_customizations():
    # Make output dir
    Path("./output/SKINS").mkdir(parents=True, exist_ok=True)

    # Borderlands 3 - All Global Customizations
    sh = gc.open_by_key("1v-F_3C2ceaFKJae1b6wmbelw_jLjmPPriBLzGTZMqRc")

    print("Downloading Beastmaster Heads, Skins and Emotes")
    beastmaster_heads = sh.worksheet("Beastmaster Heads")
    beastmaster_skins = sh.worksheet("Beastmaster Skins")
    beastmaster_emotes = sh.worksheet("Beastmaster Emotes")

    print("Downloading Gunner Heads, Skins and Emotes")
    gunner_heads = sh.worksheet("Gunner Heads")
    gunner_skins = sh.worksheet("Gunner Skins")
    gunner_emotes = sh.worksheet("Gunner Emotes")

    print("Downloading Operative Heads, Skins and Emotes")
    operative_heads = sh.worksheet("Operative Heads")
    operative_skins = sh.worksheet("Operative Skins")
    operative_emotes = sh.worksheet("Operative Emotes")

    print("Downloading Siren Heads, Skins and Emotes")
    siren_heads = sh.worksheet("Siren Heads")
    siren_skins = sh.worksheet("Siren Skins")
    siren_emotes = sh.worksheet("Siren Emotes")

    print("Downloading Weapon Skins and Trinkets")
    weapon_skins = sh.worksheet("Weapon Skins")
    weapon_trinkets = sh.worksheet("Weapon Trinkets")

    print("Downloading ECHO Themes")
    echo_themes = sh.worksheet("ECHO Themes")

    print("Downloading Room Decorations")
    room_decorations = sh.worksheet("Room Decorations")

    profile_heads = [beastmaster_heads, gunner_heads, operative_heads, siren_heads]
    profile_skins = [beastmaster_skins, gunner_skins, operative_skins, siren_skins]
    profile_emotes = [beastmaster_emotes, gunner_emotes, operative_emotes, siren_emotes]

    weapon_skins = [weapon_skins]
    weapon_trinkets = [weapon_trinkets]

    echo_themes = [echo_themes]

    room_decorations = [room_decorations]

    all_items = [("PROFILE_HEADS", profile_heads), ("PROFILE_SKINS", profile_skins), ("PROFILE_EMOTES", profile_emotes),
                 ("PROFILE_WEAPON_SKINS", weapon_skins), ("PROFILE_WEAPON_TRINKETS", weapon_trinkets),
                 ("PROFILE_ECHO_THEMES", echo_themes), ("PROFILE_ROOM_DECORATIONS", room_decorations)]

    # Write Profile Heads
    for (name, values) in all_items:
        print("Saving {}...".format(name))

        with open("output/SKINS/{}.csv".format(name), "w", newline="") as f:
            w = csv.writer(f)

            for sheet in values:
                print("Saving: {}".format(sheet.title))

                for (i, val) in enumerate(sheet.get_all_values()):
                    not_allowed = ["director", "deluxe", "designer", "neon", "retro", "gearbox", "gold", "toy box"]
                    unlock_requirements = val[1].lower()

                    if any(n in unlock_requirements for n in not_allowed):
                        continue

                    if i != 0:
                        if len(val) >= 4:
                            if val[3] != "Always Available":
                                fixed_bal_name = val[2].replace("InvBal_", "")

                                csv_row = [fixed_bal_name, val[0]]
                                w.writerow(csv_row)


def download_new_inventory_parts_info():
    # Make output dir
    Path("./output/INV_PARTS_INFO").mkdir(parents=True, exist_ok=True)

    # Borderlands 3 - Item parts/stats
    sh = gc.open_by_key("1urwGdlmpzw7wbQcA_7zHqFlfM6QAm9SHG0CX4dxfRuQ")

    # Pistols
    print("Downloading Pistols")
    pistols = sh.worksheet("Pistols")

    # SMG's
    print("Downloading SMG's")
    smgs = sh.worksheet("SMGs")

    # Assault Rifles
    print("Downloading Assault Rifles")
    assault_rifles = sh.worksheet("Assault Rifles")

    # Shotguns
    print("Downloading Shotguns")
    shotguns = sh.worksheet("Shotguns")

    # Rocket Launchers/Heavy's
    print("Downloading Rocket Launchers")
    rocket_launchers = sh.worksheet("Rocket Launchers")

    # Sniper Rifles
    print("Downloading Sniper Rifles")
    sniper_rifles = sh.worksheet("Sniper Rifles")

    # Download Weapon Sheets that have the part and positives/negatives
    all_weapon_sheets = [pistols, smgs, assault_rifles, shotguns, rocket_launchers, sniper_rifles]

    with open("output/INV_PARTS_INFO/INVENTORY_PARTS_INFO_ALL_NEW.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Part", "Positives", "Negatives", "Effects"])

        for sheet in all_weapon_sheets:
            print("Saving: {}".format(sheet.title))

            for val in sheet.get_all_values():
                if len(val) >= 3:
                    part_name = val[3]

                    val[1] = val[1].replace(" ♦ ", ", ")
                    val[2] = val[2].replace(" ♦ ", ", ")

                    if val[1].strip() == "" and val[2].strip() == "":
                        continue

                    part_name_s = part_name.strip()
                    positives_s = format_info(val[1])
                    positives_s = positives_s.replace(":", " ")
                    negatives_s = format_info(val[2])
                    negatives_s = negatives_s.replace(":", " ")

                    csv_row = [part_name_s, positives_s, negatives_s, ""]
                    w.writerow(csv_row)


def combine_inventory_parts_new_and_old():
    all_rows = dict()

    with open("output/INV_PARTS_INFO/INVENTORY_PARTS_INFO_ALL_OLD.csv", "r") as old_info:
        old_reader = csv.reader(old_info)

        for (i, row) in enumerate(old_reader):
            if i == 0:
                continue

            all_rows[row[0]] = row

    with open("output/INV_PARTS_INFO/INVENTORY_PARTS_INFO_ALL_NEW.csv", "r") as new_info:
        new_reader = csv.reader(new_info)

        for (i, new_row) in enumerate(new_reader):
            if i == 0:
                continue

            all_rows[new_row[0]] = new_row

    with open("output/INV_PARTS_INFO/INVENTORY_PARTS_INFO_ALL.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Part", "Positives", "Negatives", "Effects"])

        for row in all_rows.values():
            w.writerow(row)


if __name__ == "__main__":
    gc = gspread.service_account()

    # download_inventory_parts()
    # download_old_inventory_parts_info()
    # download_new_inventory_parts_info()
    # download_all_global_customizations()
    combine_inventory_parts_new_and_old()
