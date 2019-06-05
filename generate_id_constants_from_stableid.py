import json
import os
import platform
from pathlib import Path

HEADER = f'# DO NOT EDIT!\n# This file was automatically generated by "{os.path.basename(__file__)}"\n'

PF = platform.system()

HOME_DIR = str(Path.home())
DATA_JSON = {
    "Darwin": HOME_DIR + "/Library/Application Support/Blizzard/StarCraft II/stableid.json",
    "Windows": HOME_DIR + "/Documents/StarCraft II/stableid.json",
}

ENUM_TRANSLATE = {
    "Units": "UnitTypeId",
    "Abilities": "AbilityId",
    "Upgrades": "UpgradeId",
    "Buffs": "BuffId",
    "Effects": "EffectId",
}

FILE_TRANSLATE = {
    "Units": "unit_typeid",
    "Abilities": "ability_id",
    "Upgrades": "upgrade_id",
    "Buffs": "buff_id",
    "Effects": "effect_id",
}


def make_key(key):
    if key[0].isdigit():
        key = "_" + key
    return key.upper().replace(" ", "_")


def parse_data(data):
    # for d in data:  # Units, Abilities, Upgrades, Buffs, Effects

    units = parse_simple("Units", data)
    upgrades = parse_simple("Upgrades", data)
    effects = parse_simple("Effects", data)
    buffs = parse_simple("Buffs", data)

    abilities = {}
    for v in data["Abilities"]:
        key = v["buttonname"]
        remapid = v.get("remapid")

        if (not key) and (remapid is None):
            assert v["buttonname"] == ""
            continue

        if not key:
            if v["friendlyname"] != "":
                key = v["friendlyname"]
            else:
                exit(f"Not mapped: {v !r}")

        key = key.upper().replace(" ", "_")

        if "name" in v:
            key = f'{v["name"].upper().replace(" ", "_")}_{key}'

        if "friendlyname" in v:
            key = v["friendlyname"].upper().replace(" ", "_")

        if key[0].isdigit():
            key = "_" + key

        if key in abilities and v["index"] == 0:
            print(f"{key} has value 0")
            # raise ValueError
        else:
            abilities[key] = v["id"]

    abilities["SMART"] = 1

    enums = {}
    enums["Units"] = units
    enums["Abilities"] = abilities
    enums["Upgrades"] = upgrades
    enums["Buffs"] = buffs
    enums["Effects"] = effects

    return enums


def parse_simple(d, data):
    units = {}
    for v in data[d]:
        key = v["name"]

        if not key:
            continue
        key_to_insert = make_key(key)
        if key_to_insert in units:
            index = 2
            tmp = f"{key_to_insert}_{index}"
            while tmp in units:
                index += 1
                tmp = f"{key_to_insert}_{index}"
            key_to_insert = tmp
        units[key_to_insert] = v["id"]

    return units


def generate_python_code(enums):
    assert {"Units", "Abilities", "Upgrades", "Buffs", "Effects"} <= enums.keys()

    sc2dir = Path("sc2/")
    idsdir = sc2dir / "ids"
    idsdir.mkdir(exist_ok=True)

    with (idsdir / "__init__.py").open("w") as f:
        initstring = f"__all__ = {[n.lower() for n in FILE_TRANSLATE.values()] !r}\n".replace("'", '"')
        f.write("\n".join([HEADER, initstring]))

    for name, body in enums.items():
        class_name = ENUM_TRANSLATE[name]

        code = [HEADER, "import enum", "\n", f"class {class_name}(enum.Enum):"]

        for key, value in sorted(body.items(), key=lambda p: p[1]):
            code.append(f"    {key} = {value}")

        code += [
            "\n",
            f"for item in {class_name}:",
            f"    assert not item.name in globals()",
            f"    globals()[item.name] = item",
            "",
        ]

        with (idsdir / FILE_TRANSLATE[name]).with_suffix(".py").open("w") as f:
            f.write("\n".join(code))


if __name__ == "__main__":
    stableid_json = os.getenv("DATA_JSON") or DATA_JSON[PF]
    with open(stableid_json, encoding="utf-8") as data_file:
        data = json.loads(data_file.read())
        generate_python_code(parse_data(data))
