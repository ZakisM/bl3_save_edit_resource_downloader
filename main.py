import csv

import gspread

if __name__ == "__main__":
    gc = gspread.service_account()

    # Borderlands 3 Weapon/Item Parts + Weights
    sh = gc.open_by_key("1XYG30B6CulmcmmVDuq-PkLEJVtjAFacx7cuSkqbv5N4")

    weapons = sh.worksheet("Weapons")
    shields = sh.worksheet("Shields")
    grenade_mods = sh.worksheet("Grenade Mods")
    class_mods = sh.worksheet("Class Mods")
    artifacts = sh.worksheet("Artifacts")

    items = [weapons, shields, grenade_mods, class_mods, artifacts]

    all_records = []

    for i in items:
        filename = "output/INVENTORY_PARTS_{}.csv".format(i.title.upper().replace(" ", "_"))
        print(filename)

        keys = i.row_values(1)
        records = i.get_all_records()

        all_records.append(records)

        with open(filename, "w") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(records)

    all_keys = ["Name", "Weapon Type", "Rarity", "Balance", "Category", "Min Parts", "Max Parts", "Weight", "Part",
                "Dependencies", "Excluders"]

    all_keys_len = len(all_keys)

    with open("output/INVENTORY_PARTS_ALL.csv", "w") as inv_parts_all:
        headers = ",".join(all_keys)
        inv_parts_all.write(headers + "\n")

        for i in ["WEAPONS", "SHIELDS", "GRENADE_MODS", "CLASS_MODS", "ARTIFACTS"]:
            filename = "output/INVENTORY_PARTS_{}.csv".format(i)

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
