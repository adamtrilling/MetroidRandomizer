import Ophis.Main
import os
import random
import re
import shutil


def generate(seed):
    # assemble non-randomized files if necessary
    if (os.path.isfile("work/Defines.asm") is not True):
        shutil.copy("src/asm/code/Defines.asm", "work")
    if (os.path.isfile("work/3.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/3.bin", "src/asm/PRG/3.asm"])
    if (os.path.isfile("work/6.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/6.bin", "src/asm/PRG/6.asm"])
    if (os.path.isfile("work/7.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/7.bin", "src/asm/PRG/7.asm"])

    randomize(seed)

    # assemble PRGs
    prg = open("work/0-{0}.asm".format(seed), 'w')
    prg.write(".require \"Title-{0}.asm\"  ; Title, pg 0\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/0-{0}.bin".format(seed),
                          "work/0-{0}.asm".format(seed)])

    prg = open("work/1-{0}.asm".format(seed), 'w')
    prg.write(".require \"Brinstar-{0}.asm\"  ; Brinstar, pg 1\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/1-{0}.bin".format(seed),
                          "work/1-{0}.asm".format(seed)])

    prg = open("work/2-{0}.asm".format(seed), 'w')
    prg.write(".require \"Norfair-{0}.asm\" ; pg 2\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/2-{0}.bin".format(seed),
                          "work/2-{0}.asm".format(seed)])

    prg = open("work/4-{0}.asm".format(seed), 'w')
    prg.write(".require \"Kraid-{0}.asm\" ; pg 4\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/4-{0}.bin".format(seed),
                          "work/4-{0}.asm".format(seed)])

    prg = open("work/5-{0}.asm".format(seed), 'w')
    prg.write(".require \"Ridley-{0}.asm\" ; pg 5\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/5-{0}.bin".format(seed),
                          "work/5-{0}.asm".format(seed)])

    # generate and execute makefile
    output_file = "work/metroid-{0}.nes".format(seed)
    makefile = open("work/make-{0}.asm".format(seed), 'w')
    makefile.write(".outfile \"{0}\"\n".format(output_file))
    makefile.write(".include \"../src/asm/code/header.asm\"\n")
    makefile.write(".incbin \"0-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"1-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"2-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"3.bin\"\n")
    makefile.write(".incbin \"4-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"5-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"6.bin\"\n")
    makefile.write(".incbin \"7.bin\"\n")
    makefile.close()

    Ophis.Main.run_ophis(["work/make-{0}.asm".format(seed)])

    return output_file


# randomizer constants
ITEMS = [0, 1, 2, 3, 5, 6] + [7] * 2 + [8] * 8 + [9] * 21

ITEM_LOCATIONS = {
    1: {"zone": "Brinstar", "zone_line": "LA41F", "pass_line": "L902B"},  # 1
    2: {"zone": "Brinstar", "zone_line": "LA409", "pass_line": "L9031"},  # 4
    3: {"zone": "Brinstar", "zone_line": "LA3FC", "pass_line": "L9035"},  # 6
    4: {"zone": "Brinstar", "zone_line": "LA3E7", "pass_line": "L9039"},  # 8
    5: {"zone": "Brinstar", "zone_line": "LA3ED", "pass_line": "L903B"},  # 9
    6: {"zone": "Brinstar", "zone_line": "LA3DE", "pass_line": "L903F"},  # 11
    7: {"zone": "Brinstar", "zone_line": "LA433", "pass_line": "L9041"},  # 12
    8: {"zone": "Norfair",  "zone_line": "LA316", "pass_line": "L9043"},  # 13
    9: {"zone": "Norfair",  "zone_line": "LA31F", "pass_line": "L9045"},  # 14
    10: {"zone": "Norfair",  "zone_line": "LA2DC", "pass_line": "L9049"},  # 16
    11: {"zone": "Norfair",  "zone_line": "LA2E2", "pass_line": "L904B"},  # 17
    12: {"zone": "Norfair",  "zone_line": "LA2FC", "pass_line": "L904D"},  # 18
    13: {"zone": "Norfair",  "zone_line": "LA2F6", "pass_line": "L904F"},  # 19
    14: {"zone": "Norfair",  "zone_line": "LA2F0", "pass_line": "L9051"},  # 20
    15: {"zone": "Norfair",  "zone_line": "LA32C", "pass_line": "L9053"},  # 21
    16: {"zone": "Norfair",  "zone_line": "LA326", "pass_line": "L9055"},  # 22
    17: {"zone": "Norfair",  "zone_line": "LA35D", "pass_line": "L9059"},  # 24
    18: {"zone": "Norfair",  "zone_line": "LA33E", "pass_line": "L905D"},  # 26
    19: {"zone": "Norfair",  "zone_line": "LA39A", "pass_line": "L905F"},  # 27
    20: {"zone": "Norfair",  "zone_line": "LA3A0", "pass_line": "L9061"},  # 28
    21: {"zone": "Norfair",  "zone_line": "LA370", "pass_line": "L9065"},  # 30
    22: {"zone": "Norfair",  "zone_line": "LA383", "pass_line": "L9067"},  # 31
    23: {"zone": "Kraid",    "zone_line": "LA286", "pass_line": "L906B"},  # 33
    24: {"zone": "Kraid",    "zone_line": "LA27F", "pass_line": "L906D"},  # 34
    25: {"zone": "Kraid",    "zone_line": "LA28F", "pass_line": "L9071"},  # 36
    26: {"zone": "Kraid",    "zone_line": "LA2A1", "pass_line": "L9077"},  # 39
    27: {"zone": "Kraid",    "zone_line": "LA298", "pass_line": "L9079"},  # 40
    28: {"zone": "Kraid",    "zone_line": "LA2B1", "pass_line": "L907D"},  # 42
    29: {"zone": "Ridley",   "zone_line": "LA210", "pass_line": "L907F"},  # 43
    30: {"zone": "Ridley",   "zone_line": "LA21E", "pass_line": "L9083"},  # 45
    31: {"zone": "Ridley",   "zone_line": "LA239", "pass_line": "L9085"},  # 46
    32: {"zone": "Ridley",   "zone_line": "LA230", "pass_line": "L9089"},  # 48
    33: {"zone": "Ridley",   "zone_line": "LA227", "pass_line": "L908B"},  # 49
    34: {"zone": "Brinstar", "zone_line": "LA3F6"},
    35: {"zone": "Brinstar", "zone_line": "LA412"},
    36: {"zone": "Norfair",  "zone_line": "LA305"},
    37: {"zone": "Norfair",  "zone_line": "LA38C"}
}

ITEM_NAMES = {
    0: "bombs", 1: "high jump", 2: "long beam", 3: "screw attack",
    4: "morph ball", 5: "varia", 6: "wave beam", 7: "ice beam",
    8: "energy tank", 9: "missiles"
}

FIRST_MISSILE_LOCATIONS = {1, 2, 5, 12, 13, 14}
BOMB_LOCATIONS = FIRST_MISSILE_LOCATIONS | {3}
ANYWHERE_ITEMS = [1, 2, 3, 5, 6] + [7] * 2 + [8] * 8 + [9] * 20


FILENAMES = ['Title', 'Brinstar', 'Norfair', 'Kraid', 'Ridley']

# number of missiles for boss defeat - LDD75


def randomize(seed):
    # open asm files
    filedata = {}
    for filename in FILENAMES:
        input_path = "src/asm/code/{0}.asm".format(filename)

        with open(input_path, 'r') as file:
            filedata[filename] = file.read()

    # shuffle items
    random.seed(int(seed, 16))
    random_locations = {}
    item_locations = set(ITEM_LOCATIONS.keys())

    # place an easily-accessible missile tank
    location = random.choice(
        tuple(FIRST_MISSILE_LOCATIONS & item_locations)
    )
    print("first missiles: location {0}".format(location))
    random_locations[location] = 9

    # make sure boms aren't bomb-blocked
    location = random.choice(
        tuple((BOMB_LOCATIONS & item_locations) - random_locations.viewkeys())
    )
    print("bombs: location {0}".format(location))
    random_locations[location] = 0

    # place other items
    for item in ANYWHERE_ITEMS:
        location = random.choice(
            tuple(item_locations - random_locations.viewkeys())
        )
        print("{0}: location {1}".format(ITEM_NAMES[item], location))
        random_locations[location] = item

    for loc, item in random_locations.iteritems():
        location = ITEM_LOCATIONS[loc]
        filename = location["zone"]

        print("putting {0} in {1}:{2}".format(
            ITEM_NAMES[item], location["zone"], location["zone_line"])
        )

        # place item on map
        exp = r"({0}:\s+\.byte\ \$\w\w,\ \$\w\w,\ \$\w\w, \$)\w\w".format(
            location["zone_line"]
        )
        regex = re.compile(exp, re.MULTILINE)
        results = regex.search(filedata[filename])
        filedata[filename] = regex.sub("{0}{1:=02X}".format(results.group(1),
                                                            item),
                                       filedata[filename])

        # point item to the correct password bit
        if ("pass_line" in location):
            exp = r"({0}:\s+\.word\ \$(\w\w))".format(location["pass_line"])
            regex = re.compile(exp, re.MULTILINE)
            matches = regex.search(filedata['Title'])

            # some weird bit munging going on here. The first six bits are the
            # item code, and the last two are part of the x coordinate. See
            # the ItemData commentary in Title.asm for details
            x_coord_bits = int(matches.groups()[1], 16) % 4
            item_bits = item * 4 + x_coord_bits

            sub_regex = r"{0}:\t.word ${1:=02X}".format(
                location["pass_line"], item_bits)
            filedata["Title"] = regex.sub(sub_regex, filedata["Title"])

    # write shuffled asm files
    for filename in FILENAMES:
        output_path = "work/{0}-{1}.asm".format(filename, seed)
        with open(output_path, 'w') as file:
            file.write(filedata[filename])
