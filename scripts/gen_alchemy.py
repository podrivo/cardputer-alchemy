#!/usr/bin/env python3
"""Generate game.hpp / game.cpp / COMBINATIONS.md from the alchemy catalog."""

from __future__ import annotations

from collections import defaultdict

# Starters unlock at init.
STARTERS = ("Fire", "Water", "Earth", "Air")

# Display names in enum order. Keep short (Cardputer LCD).
ITEMS: list[str] = [
    "Fire",
    "Water",
    "Earth",
    "Air",
    "Steam",
    "Lava",
    "Mud",
    "Dust",
    "Energy",
    "Rain",
    "Pressure",
    "Sea",
    "Ocean",
    "Land",
    "Stone",
    "Sand",
    "Glass",
    "Metal",
    "Clay",
    "Brick",
    "Wall",
    "House",
    "Cloud",
    "Sky",
    "Storm",
    "Lightning",
    "Wind",
    "Fog",
    "Smoke",
    "Ash",
    "Plant",
    "Grass",
    "Tree",
    "Forest",
    "Seed",
    "Flower",
    "Fruit",
    "Reed",
    "Swamp",
    "Microbe",
    "Life",
    "Egg",
    "Beast",
    "Bird",
    "Fish",
    "Worm",
    "Snake",
    "Turtle",
    "Beetle",
    "Scorpion",
    "Bee",
    "Butterfly",
    "Frog",
    "Chicken",
    "Duck",
    "Whale",
    "Shark",
    "Horse",
    "Cow",
    "Pig",
    "Sheep",
    "Dog",
    "Cat",
    "Wolf",
    "Mouse",
    "Monkey",
    "Bear",
    "Penguin",
    "Dinosaur",
    "Dragon",
    "Human",
    "Farmer",
    "Hunter",
    "Lumberjack",
    "Sailor",
    "Pirate",
    "Soldier",
    "Knight",
    "Doctor",
    "Wizard",
    "Coder",
    "Hero",
    "Archer",
    "Astronaut",
    "Pharaoh",
    "Vampire",
    "Werewolf",
    "Zombie",
    "Franken",
    "Ghost",
    "Skeleton",
    "Mummy",
    "Golem",
    "Robot",
    "Cyborg",
    "Alien",
    "Tool",
    "Axe",
    "Weapon",
    "Armor",
    "Bow",
    "Arrow",
    "Gun",
    "Powder",
    "Wood",
    "Wheel",
    "Cart",
    "Chariot",
    "Car",
    "Bicycle",
    "Engine",
    "Train",
    "Boat",
    "Sailboat",
    "Ship",
    "Steamer",
    "Submarine",
    "Airplane",
    "Rocket",
    "Drone",
    "UFO",
    "Parachute",
    "Windmill",
    "Pottery",
    "Lens",
    "Glasses",
    "Mirror",
    "Bulb",
    "Lighthouse",
    "Panel",
    "Volt",
    "Wire",
    "Battery",
    "PC",
    "Web",
    "Cardputer",
    "Coal",
    "Oil",
    "Fossil",
    "Diamond",
    "Gold",
    "Salt",
    "Cement",
    "Concrete",
    "Fabric",
    "Wool",
    "Rope",
    "Clothes",
    "Paper",
    "Book",
    "Map",
    "Ink",
    "Pen",
    "Feather",
    "Scroll",
    "Hourglass",
    "Time",
    "Clock",
    "SunDial",
    "Campfire",
    "Tent",
    "Field",
    "Wheat",
    "Flour",
    "Dough",
    "Bread",
    "Milk",
    "Cheese",
    "Bacon",
    "Meat",
    "Blood",
    "Bone",
    "Corpse",
    "Juice",
    "Alcohol",
    "Beer",
    "Wine",
    "Omelette",
    "IceCream",
    "Soap",
    "Poison",
    "Medicine",
    "Hospital",
    "Sound",
    "Music",
    "Guitar",
    "Wand",
    "Magic",
    "Shell",
    "Pearl",
    "Aquarium",
    "Wave",
    "Tsunami",
    "Ice",
    "Snow",
    "Snowman",
    "Igloo",
    "Desert",
    "Cactus",
    "Camel",
    "Beach",
    "Island",
    "Palm",
    "Mountain",
    "Volcano",
    "Sun",
    "Moon",
    "Night",
    "Day",
    "Rainbow",
    "Eclipse",
    "Star",
    "Space",
    "Planet",
    "Telescope",
    "BlackHole",
    "Smog",
    "City",
    "Treasure",
    "Phoenix",
]

# Exactly one result per unordered input pair. Inspired by Little Alchemy 1/2.
# https://hints.littlealchemy2.com/  https://littlealchemy2cheats.com/combinations
RECIPES: list[tuple[str, str, str]] = [
    # —— elements ——
    ("Fire", "Water", "Steam"),
    ("Fire", "Earth", "Lava"),
    ("Water", "Earth", "Mud"),
    ("Air", "Earth", "Dust"),
    ("Fire", "Air", "Energy"),
    ("Water", "Air", "Rain"),
    ("Air", "Air", "Pressure"),
    ("Earth", "Earth", "Land"),
    ("Water", "Water", "Sea"),
    ("Sea", "Water", "Ocean"),
    ("Air", "Lava", "Stone"),
    ("Earth", "Pressure", "Stone"),
    ("Air", "Stone", "Sand"),
    ("Wind", "Stone", "Sand"),
    ("Fire", "Sand", "Glass"),
    ("Lightning", "Sand", "Glass"),
    ("Fire", "Stone", "Metal"),
    ("Mud", "Sand", "Clay"),
    ("Mud", "Stone", "Clay"),
    ("Fire", "Mud", "Brick"),
    ("Clay", "Sun", "Brick"),
    ("Brick", "Brick", "Wall"),
    ("Wall", "Wall", "House"),
    ("Human", "Brick", "House"),
    ("Steam", "Air", "Cloud"),
    ("Rain", "Air", "Cloud"),
    ("Cloud", "Air", "Sky"),
    ("Cloud", "Energy", "Storm"),
    ("Storm", "Energy", "Lightning"),
    ("Cloud", "Lightning", "Lightning"),
    ("Air", "Pressure", "Wind"),
    ("Cloud", "Earth", "Fog"),
    ("Fire", "Dust", "Smoke"),
    ("Campfire", "Air", "Smoke"),
    ("Fire", "Plant", "Ash"),
    ("Fire", "Tree", "Ash"),
    ("Rain", "Earth", "Plant"),
    ("Seed", "Earth", "Plant"),
    ("Seed", "Water", "Plant"),
    ("Plant", "Earth", "Grass"),
    ("Plant", "Plant", "Tree"),
    ("Plant", "Time", "Tree"),
    ("Tree", "Tree", "Forest"),
    ("Plant", "Grass", "Seed"),
    ("Flower", "Time", "Seed"),
    ("Grass", "Seed", "Flower"),
    ("Plant", "Rainbow", "Flower"),
    ("Flower", "Water", "Fruit"),
    ("Tree", "Farmer", "Fruit"),
    ("Grass", "Mud", "Reed"),
    ("Swamp", "Grass", "Reed"),
    ("Mud", "Plant", "Swamp"),
    ("Mud", "Tree", "Swamp"),
    ("Swamp", "Energy", "Life"),
    ("Swamp", "Lightning", "Life"),
    ("Ocean", "Lightning", "Life"),
    ("Life", "Water", "Microbe"),
    ("Life", "Mud", "Microbe"),
    ("Life", "Stone", "Egg"),
    ("Bird", "Bird", "Egg"),
    ("Fish", "Fish", "Egg"),
    ("Life", "Land", "Beast"),
    ("Life", "Forest", "Beast"),
    ("Air", "Beast", "Bird"),
    ("Air", "Egg", "Bird"),
    ("Sky", "Egg", "Bird"),
    ("Water", "Beast", "Fish"),
    ("Sea", "Egg", "Fish"),
    ("Ocean", "Egg", "Fish"),
    ("Earth", "Beast", "Worm"),
    ("Worm", "Sand", "Snake"),
    ("Worm", "Swamp", "Snake"),
    ("Egg", "Sand", "Turtle"),
    ("Egg", "Beach", "Turtle"),
    ("Earth", "Worm", "Beetle"),
    ("Sand", "Beetle", "Scorpion"),
    ("Desert", "Beetle", "Scorpion"),
    ("Flower", "Beetle", "Bee"),
    ("Air", "Worm", "Butterfly"),
    ("Flower", "Worm", "Butterfly"),
    ("Swamp", "Egg", "Frog"),
    ("Swamp", "Life", "Frog"),
    ("Egg", "Life", "Chicken"),
    ("Egg", "Bird", "Chicken"),
    ("Bird", "Water", "Duck"),
    ("Fish", "Ocean", "Whale"),
    ("Beast", "Ocean", "Whale"),
    ("Ocean", "Blood", "Shark"),
    ("Fish", "Wolf", "Shark"),
    ("Beast", "Grass", "Horse"),
    ("Beast", "Field", "Horse"),
    ("Beast", "Farmer", "Cow"),
    ("Grass", "Farmer", "Cow"),
    ("Beast", "Mud", "Pig"),
    ("Beast", "Cloud", "Sheep"),
    ("Land", "Beast", "Sheep"),
    ("Wolf", "Human", "Dog"),
    ("Beast", "House", "Dog"),
    ("Milk", "Beast", "Cat"),
    ("Mouse", "Beast", "Cat"),
    ("Moon", "Beast", "Wolf"),
    ("Dog", "Forest", "Wolf"),
    ("Dust", "Beast", "Mouse"),
    ("Cheese", "Beast", "Mouse"),
    ("Beast", "Tree", "Monkey"),
    ("Human", "Tree", "Monkey"),
    ("Beast", "Forest", "Bear"),
    ("Bird", "Ice", "Penguin"),
    ("Egg", "Ice", "Penguin"),
    ("Egg", "Earth", "Dinosaur"),
    ("Beast", "Earth", "Dinosaur"),
    ("Dinosaur", "Fire", "Dragon"),
    ("Dinosaur", "Air", "Dragon"),
    ("Clay", "Life", "Human"),
    ("Beast", "Tool", "Human"),
    ("Monkey", "Tool", "Human"),
    ("Human", "Plant", "Farmer"),
    ("Human", "Field", "Farmer"),
    ("Human", "Bow", "Hunter"),
    ("Human", "Axe", "Lumberjack"),
    ("Human", "Forest", "Lumberjack"),
    ("Human", "Boat", "Sailor"),
    ("Human", "Ocean", "Sailor"),
    ("Sailor", "Weapon", "Pirate"),
    ("Boat", "Weapon", "Pirate"),
    ("Human", "Gun", "Soldier"),
    ("Human", "Armor", "Knight"),
    ("Human", "Medicine", "Doctor"),
    ("Human", "Energy", "Wizard"),
    ("Human", "Wand", "Wizard"),
    ("Human", "PC", "Coder"),
    ("Knight", "Dragon", "Hero"),
    ("Human", "Dragon", "Hero"),
    ("Hunter", "Bow", "Archer"),
    ("Soldier", "Bow", "Archer"),
    ("Human", "Rocket", "Astronaut"),
    ("Human", "Space", "Astronaut"),
    ("Human", "Mummy", "Pharaoh"),
    ("Desert", "Human", "Pharaoh"),
    ("Human", "Blood", "Vampire"),
    ("Human", "Night", "Vampire"),
    ("Human", "Wolf", "Werewolf"),
    ("Human", "Moon", "Werewolf"),
    ("Corpse", "Life", "Zombie"),
    ("Corpse", "Lightning", "Franken"),
    ("Corpse", "Night", "Ghost"),
    ("Bone", "Bone", "Skeleton"),
    ("Corpse", "Time", "Skeleton"),
    ("Corpse", "Fabric", "Mummy"),
    ("Corpse", "Desert", "Mummy"),
    ("Stone", "Life", "Golem"),
    ("Clay", "Energy", "Golem"),
    ("Golem", "Metal", "Robot"),
    ("Metal", "Life", "Robot"),
    ("Armor", "Golem", "Robot"),
    ("Human", "Robot", "Cyborg"),
    ("Life", "Space", "Alien"),
    ("Life", "Planet", "Alien"),
    ("Human", "Stone", "Tool"),
    ("Human", "Wood", "Tool"),
    ("Metal", "Wood", "Tool"),
    ("Tool", "Forest", "Axe"),
    ("Blade", "Wood", "Axe"),
    ("Metal", "Stone", "Weapon"),
    ("Tool", "Metal", "Weapon"),
    ("Metal", "Fabric", "Armor"),
    ("Tool", "Fabric", "Armor"),
    ("Wood", "Rope", "Bow"),
    ("Wood", "String", "Bow"),
    ("Wood", "Metal", "Arrow"),
    ("Bow", "Wood", "Arrow"),
    ("Powder", "Metal", "Gun"),
    ("Weapon", "Powder", "Gun"),
    ("Dust", "Fire", "Powder"),
    ("Dust", "Energy", "Powder"),
    ("Tree", "Tool", "Wood"),
    ("Forest", "Tool", "Wood"),
    ("Axe", "Tree", "Wood"),
    ("Tool", "Water", "Wheel"),
    ("Stone", "Tool", "Wheel"),
    ("Wheel", "Wood", "Cart"),
    ("Wheel", "Horse", "Cart"),
    ("Cart", "Horse", "Chariot"),
    ("Wheel", "Engine", "Car"),
    ("Cart", "Engine", "Car"),
    ("Wheel", "Wheel", "Bicycle"),
    ("Steam", "Metal", "Engine"),
    ("Steam", "Tool", "Engine"),
    ("Coal", "Steam", "Engine"),
    ("Engine", "Metal", "Train"),
    ("Engine", "Cart", "Train"),
    ("Water", "Wood", "Boat"),
    ("Ocean", "Wood", "Boat"),
    ("Boat", "Fabric", "Sailboat"),
    ("Boat", "Wind", "Sailboat"),
    ("Boat", "Boat", "Ship"),
    ("Boat", "Wood", "Ship"),
    ("Boat", "Steam", "Steamer"),
    ("Boat", "Engine", "Steamer"),
    ("Boat", "Fish", "Submarine"),
    ("Ship", "Fish", "Submarine"),
    ("Metal", "Ocean", "Submarine"),
    ("Bird", "Metal", "Airplane"),
    ("Bird", "Engine", "Airplane"),
    ("Airplane", "Space", "Rocket"),
    ("Metal", "Fire", "Rocket"),
    ("Airplane", "Robot", "Drone"),
    ("Airplane", "PC", "Drone"),
    ("Alien", "Airplane", "UFO"),
    ("Alien", "Metal", "UFO"),
    ("Rocket", "Alien", "UFO"),
    ("Fabric", "Air", "Parachute"),
    ("Clothes", "Air", "Parachute"),
    ("Air", "Wheel", "Windmill"),
    ("Wind", "Wheel", "Windmill"),
    ("Wind", "House", "Windmill"),
    ("Clay", "Wheel", "Pottery"),
    ("Clay", "Tool", "Pottery"),
    ("Glass", "Glass", "Lens"),
    ("Glass", "Tool", "Lens"),
    ("Lens", "Lens", "Glasses"),
    ("Glass", "Metal", "Mirror"),
    ("Glass", "Wire", "Bulb"),
    ("Glass", "Energy", "Bulb"),
    ("Bulb", "House", "Lighthouse"),
    ("Sun", "Tool", "Panel"),
    ("Sun", "Glass", "Panel"),
    ("Energy", "Metal", "Volt"),
    ("Lightning", "Metal", "Volt"),
    ("Volt", "Tool", "Wire"),
    ("Metal", "Rope", "Wire"),
    ("Volt", "Pottery", "Battery"),
    ("Volt", "Glass", "Battery"),
    ("Energy", "Pottery", "Battery"),
    ("Wire", "Bulb", "PC"),
    ("Wire", "Book", "PC"),
    ("Tool", "Wire", "PC"),
    ("PC", "Wire", "Web"),
    ("PC", "Book", "Web"),
    ("PC", "Metal", "Cardputer"),
    ("Coder", "Tool", "Cardputer"),
    ("Plant", "Pressure", "Coal"),
    ("Tree", "Earth", "Coal"),
    ("Time", "Dinosaur", "Fossil"),
    ("Earth", "Dinosaur", "Fossil"),
    ("Bone", "Earth", "Fossil"),
    ("Fossil", "Pressure", "Oil"),
    ("Fossil", "Time", "Oil"),
    ("Pressure", "Coal", "Diamond"),
    ("Coal", "Time", "Diamond"),
    ("Metal", "Sun", "Gold"),
    ("Metal", "Rainbow", "Gold"),
    ("Ocean", "Sun", "Salt"),
    ("Sea", "Fire", "Salt"),
    ("Clay", "Stone", "Cement"),
    ("Clay", "Fire", "Cement"),
    ("Cement", "Water", "Concrete"),
    ("Cement", "Brick", "Concrete"),
    ("Tool", "Sheep", "Wool"),
    ("Tool", "Wool", "Fabric"),
    ("Wool", "Wool", "Fabric"),
    ("Fabric", "Fabric", "Rope"),
    ("Fabric", "Human", "Clothes"),
    ("Fabric", "Tool", "Clothes"),
    ("Wood", "Pressure", "Paper"),
    ("Reed", "Tool", "Paper"),
    ("Paper", "Paper", "Book"),
    ("Paper", "Feather", "Book"),
    ("Paper", "Land", "Map"),
    ("Paper", "Ocean", "Map"),
    ("Ash", "Water", "Ink"),
    ("Coal", "Water", "Ink"),
    ("Feather", "Metal", "Pen"),
    ("Tool", "Feather", "Pen"),
    ("Bird", "Air", "Feather"),
    ("Bird", "Tool", "Feather"),
    ("Paper", "Ink", "Scroll"),
    ("Paper", "Pen", "Scroll"),
    ("Glass", "Sand", "Hourglass"),
    ("Glass", "Time", "Hourglass"),
    ("Hourglass", "Sand", "Time"),
    ("Hourglass", "Life", "Time"),
    ("Time", "Wheel", "Clock"),
    ("Hourglass", "Energy", "Clock"),
    ("Time", "Tool", "Clock"),
    ("Sun", "Wheel", "SunDial"),
    ("Sun", "Clock", "SunDial"),
    ("Fire", "Grass", "Campfire"),
    ("Fire", "Wood", "Campfire"),
    ("Fabric", "Wood", "Tent"),
    ("Fabric", "House", "Tent"),
    ("Farmer", "Earth", "Field"),
    ("Tool", "Earth", "Field"),
    ("Farmer", "Grass", "Wheat"),
    ("Field", "Grass", "Wheat"),
    ("Wheat", "Stone", "Flour"),
    ("Wheat", "Wheel", "Flour"),
    ("Flour", "Water", "Dough"),
    ("Dough", "Fire", "Bread"),
    ("Dough", "Campfire", "Bread"),
    ("Cow", "Farmer", "Milk"),
    ("Cow", "Human", "Milk"),
    ("Milk", "Time", "Cheese"),
    ("Milk", "Tool", "Cheese"),
    ("Pig", "Fire", "Bacon"),
    ("Pig", "Campfire", "Bacon"),
    ("Beast", "Tool", "Meat"),
    ("Cow", "Tool", "Meat"),
    ("Pig", "Tool", "Meat"),
    ("Human", "Weapon", "Blood"),
    ("Meat", "Time", "Bone"),
    ("Corpse", "Tool", "Bone"),
    ("Human", "Time", "Corpse"),
    ("Human", "Poison", "Corpse"),
    ("Fruit", "Water", "Juice"),
    ("Fruit", "Pressure", "Juice"),
    ("Fruit", "Time", "Alcohol"),
    ("Juice", "Time", "Alcohol"),
    ("Wheat", "Fruit", "Alcohol"),
    ("Alcohol", "Wheat", "Beer"),
    ("Alcohol", "Fruit", "Wine"),
    ("Egg", "Fire", "Omelette"),
    ("Egg", "Campfire", "Omelette"),
    ("Milk", "Ice", "IceCream"),
    ("Milk", "Snow", "IceCream"),
    ("Oil", "Ash", "Soap"),
    ("Oil", "Salt", "Soap"),
    ("Snake", "Tool", "Poison"),
    ("Scorpion", "Human", "Poison"),
    ("Plant", "Poison", "Medicine"),
    ("Microbe", "Tool", "Medicine"),
    ("House", "Medicine", "Hospital"),
    ("House", "Doctor", "Hospital"),
    ("Air", "Wave", "Sound"),
    ("Human", "Wave", "Sound"),
    ("Sound", "Human", "Music"),
    ("Sound", "Paper", "Music"),
    ("Music", "Wood", "Guitar"),
    ("Music", "Tool", "Guitar"),
    ("Wood", "Wizard", "Wand"),
    ("Tool", "Wizard", "Wand"),
    ("Energy", "Life", "Magic"),
    ("Wand", "Energy", "Magic"),
    ("Beach", "Life", "Shell"),
    ("Sand", "Ocean", "Shell"),
    ("Shell", "Sand", "Pearl"),
    ("Shell", "Stone", "Pearl"),
    ("Glass", "Fish", "Aquarium"),
    ("Glass", "Water", "Aquarium"),
    ("Ocean", "Wind", "Wave"),
    ("Sea", "Wind", "Wave"),
    ("Ocean", "Air", "Wave"),
    ("Wave", "Wave", "Tsunami"),
    ("Ocean", "Storm", "Tsunami"),
    ("Water", "Mountain", "Ice"),
    ("Cloud", "Mountain", "Snow"),
    ("Rain", "Mountain", "Snow"),
    ("Ice", "Rain", "Snow"),
    ("Snow", "Human", "Snowman"),
    ("Ice", "House", "Igloo"),
    ("Snow", "House", "Igloo"),
    ("Sand", "Sand", "Desert"),
    ("Sand", "Land", "Desert"),
    ("Desert", "Plant", "Cactus"),
    ("Desert", "Tree", "Cactus"),
    ("Desert", "Horse", "Camel"),
    ("Desert", "Beast", "Camel"),
    ("Ocean", "Sand", "Beach"),
    ("Sea", "Sand", "Beach"),
    ("Ocean", "Volcano", "Island"),
    ("Volcano", "Sea", "Island"),
    ("Island", "Tree", "Palm"),
    ("Beach", "Tree", "Palm"),
    ("Earth", "Energy", "Mountain"),
    ("Lava", "Mountain", "Volcano"),
    ("Lava", "Earth", "Volcano"),
    ("Fire", "Mountain", "Volcano"),
    ("Fire", "Sky", "Sun"),
    ("Fire", "Planet", "Sun"),
    ("Sky", "Stone", "Moon"),
    ("Moon", "Time", "Night"),
    ("Sky", "Moon", "Night"),
    ("Sun", "Sky", "Day"),
    ("Sun", "Time", "Day"),
    ("Rain", "Sun", "Rainbow"),
    ("Water", "Sun", "Rainbow"),
    ("Sun", "Moon", "Eclipse"),
    ("Night", "Sun", "Star"),
    ("Sky", "Night", "Star"),
    ("Star", "Star", "Space"),
    ("Sky", "Star", "Space"),
    ("Earth", "Space", "Planet"),
    ("Earth", "Sky", "Planet"),
    ("Glass", "Sky", "Telescope"),
    ("Lens", "Sky", "Telescope"),
    ("Lens", "Space", "Telescope"),
    ("Star", "Pressure", "BlackHole"),
    ("Sun", "Pressure", "BlackHole"),
    ("City", "Smoke", "Smog"),
    ("Fog", "Smoke", "Smog"),
    ("House", "House", "City"),
    ("Pirate", "Map", "Treasure"),
    ("Island", "Gold", "Treasure"),
    ("Bird", "Fire", "Phoenix"),
    ("Chicken", "Fire", "Phoenix"),
    ("Ash", "Life", "Phoenix"),
]


def enum_name(name: str) -> str:
    return "ITEM_" + "".join(ch if ch.isalnum() else "_" for ch in name.upper())


def clean_recipes(
    items: list[str], recipes: list[tuple[str, str, str]]
) -> list[tuple[str, str, str]]:
    item_set = set(items)
    by_pair: dict[tuple[str, str], str] = {}
    order: list[tuple[str, str, str]] = []
    skipped_unknown = 0
    skipped_conflict = 0
    for a, b, out in recipes:
        if a not in item_set or b not in item_set or out not in item_set:
            skipped_unknown += 1
            continue
        key = tuple(sorted((a, b)))
        if key in by_pair:
            if by_pair[key] != out:
                skipped_conflict += 1
            continue
        by_pair[key] = out
        order.append((a, b, out))
    print(f"skipped unknown={skipped_unknown} conflict={skipped_conflict}")
    return order


def check_graph(items: list[str], recipes: list[tuple[str, str, str]]) -> None:
    unlocked = set(STARTERS)
    changed = True
    while changed:
        changed = False
        for a, b, out in recipes:
            if a in unlocked and b in unlocked and out not in unlocked:
                unlocked.add(out)
                changed = True
    unreachable = [i for i in items if i not in unlocked]
    no_recipe = [
        i for i in items if i not in STARTERS and not any(r[2] == i for r in recipes)
    ]
    print(f"items={len(items)} recipes={len(recipes)} reachable={len(unlocked)}")
    if unreachable:
        print("unreachable:", unreachable)
    if no_recipe:
        print("no_recipe:", no_recipe)
    if unreachable or no_recipe:
        # hint: which deps block
        have = set(STARTERS)
        for _ in range(20):
            progressed = False
            for a, b, out in recipes:
                if out in have:
                    continue
                if a in have and b in have:
                    have.add(out)
                    progressed = True
            if not progressed:
                break
        still = [i for i in items if i not in have]
        needed: dict[str, list[str]] = defaultdict(list)
        for a, b, out in recipes:
            if out in still:
                miss = [x for x in (a, b) if x not in have]
                needed[out].append(f"{a}+{b} missing={miss}")
        for out in still[:30]:
            print(f"  {out}: {needed[out][:3]}")
        raise SystemExit("Graph incomplete")


def write_hpp(items: list[str]) -> None:
    lines = [
        "#pragma once",
        "",
        "#include <cstdint>",
        "",
        f"constexpr int GAME_ITEM_COUNT = {len(items)};",
        "extern int game_visible; // visible inventory rows (set from display height)",
        "",
        "enum ItemId : uint8_t {",
    ]
    for i, name in enumerate(items):
        comma = "," if i + 1 < len(items) else ""
        lines.append(f"    {enum_name(name)} = {i}{comma}")
    lines += [
        "};",
        "",
        "struct GameState {",
        "    bool unlocked[GAME_ITEM_COUNT];",
        "    ItemId inventory[GAME_ITEM_COUNT]; // unlocked ids, dense",
        "    int inventory_count;",
        "    int cursor;       // index into inventory[]",
        "    int scroll;       // first visible inventory index",
        "    int16_t slot_a;   // ItemId or -1",
        "    int16_t slot_b;   // ItemId or -1",
        "};",
        "",
        "void game_init(GameState *g);",
        "const char *game_item_name(ItemId id);",
        "int game_unlocked_count(const GameState *g);",
        "",
        "// Enter on current cursor item — fill A, then B+combine.",
        "// Returns newly unlocked ItemId, or 0xFF if nothing new.",
        "ItemId game_pick(GameState *g);",
        "void game_clear_slots(GameState *g);",
        "void game_move(GameState *g, int delta);",
        "",
    ]
    open("main/game.hpp", "w").write("\n".join(lines))


def write_cpp(items: list[str], recipes: list[tuple[str, str, str]]) -> None:
    name_lines = []
    for i in range(0, len(items), 4):
        chunk = ", ".join(f'"{n}"' for n in items[i : i + 4])
        if i + 4 < len(items):
            chunk += ","
        name_lines.append(f"    {chunk}")

    recipe_lines = [
        f"    {{{enum_name(a)}, {enum_name(b)}, {enum_name(out)}}},"
        for a, b, out in recipes
    ]

    body = f"""#include "game.hpp"

#include <cstring>

#include "esp_log.h"
#include "nvs.h"
#include "nvs_flash.h"

int game_visible = 4;

namespace {{

constexpr char TAG[] = "game";
constexpr char kNvsNs[] = "alchemy";
constexpr char kNvsKey[] = "unlock";
constexpr uint8_t kSaveVer = 1;
constexpr size_t kBitBytes = (GAME_ITEM_COUNT + 7) / 8;
constexpr size_t kBlobSize = 1 + kBitBytes;

const char *const kNames[GAME_ITEM_COUNT] = {{
{chr(10).join(name_lines)}
}};

struct Recipe {{
    ItemId a;
    ItemId b;
    ItemId out;
}};

constexpr Recipe kRecipes[] = {{
{chr(10).join(recipe_lines)}
}};

void rebuild_inventory(GameState *g)
{{
    g->inventory_count = 0;
    for (int i = 0; i < GAME_ITEM_COUNT; ++i) {{
        if (g->unlocked[i]) {{
            g->inventory[g->inventory_count++] = static_cast<ItemId>(i);
        }}
    }}
    if (g->cursor >= g->inventory_count) {{
        g->cursor = g->inventory_count > 0 ? g->inventory_count - 1 : 0;
    }}
    if (g->scroll > g->cursor) {{
        g->scroll = g->cursor;
    }}
    if (g->cursor >= g->scroll + game_visible) {{
        g->scroll = g->cursor - game_visible + 1;
    }}
    if (g->scroll < 0) {{
        g->scroll = 0;
    }}
}}

bool nvs_ensure()
{{
    static bool ready = false;
    if (ready) {{
        return true;
    }}
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {{
        nvs_flash_erase();
        err = nvs_flash_init();
    }}
    ready = (err == ESP_OK);
    if (!ready) {{
        ESP_LOGE(TAG, "NVS init failed: %s", esp_err_to_name(err));
    }}
    return ready;
}}

bool load_unlocked(GameState *g)
{{
    if (!nvs_ensure()) {{
        return false;
    }}
    nvs_handle_t h;
    if (nvs_open(kNvsNs, NVS_READONLY, &h) != ESP_OK) {{
        return false;
    }}
    uint8_t blob[kBlobSize];
    size_t len = sizeof(blob);
    esp_err_t err = nvs_get_blob(h, kNvsKey, blob, &len);
    nvs_close(h);
    if (err != ESP_OK || len < 2 || blob[0] != kSaveVer) {{
        return false;
    }}
    const int bits = static_cast<int>((len - 1) * 8);
    int count = 0;
    for (int i = 0; i < GAME_ITEM_COUNT && i < bits; ++i) {{
        const bool on = (blob[1 + i / 8] >> (i % 8)) & 1;
        g->unlocked[i] = on;
        count += on ? 1 : 0;
    }}
    return count > 0;
}}

void save_unlocked(const GameState *g)
{{
    if (!nvs_ensure()) {{
        return;
    }}
    uint8_t blob[kBlobSize] = {{}};
    blob[0] = kSaveVer;
    for (int i = 0; i < GAME_ITEM_COUNT; ++i) {{
        if (g->unlocked[i]) {{
            blob[1 + i / 8] |= static_cast<uint8_t>(1u << (i % 8));
        }}
    }}
    nvs_handle_t h;
    if (nvs_open(kNvsNs, NVS_READWRITE, &h) != ESP_OK) {{
        return;
    }}
    if (nvs_set_blob(h, kNvsKey, blob, sizeof(blob)) == ESP_OK) {{
        nvs_commit(h);
    }}
    nvs_close(h);
}}

bool unlock(GameState *g, ItemId id)
{{
    if (g->unlocked[id]) {{
        return false;
    }}
    g->unlocked[id] = true;
    rebuild_inventory(g);
    save_unlocked(g);
    return true;
}}

ItemId combine(ItemId a, ItemId b)
{{
    for (const Recipe &r : kRecipes) {{
        if ((r.a == a && r.b == b) || (r.a == b && r.b == a)) {{
            return r.out;
        }}
    }}
    return static_cast<ItemId>(0xFF);
}}

}} // namespace

void game_init(GameState *g)
{{
    std::memset(g, 0, sizeof(*g));
    g->slot_a = -1;
    g->slot_b = -1;
    if (!load_unlocked(g)) {{
        g->unlocked[{enum_name("Fire")}] = true;
        g->unlocked[{enum_name("Water")}] = true;
        g->unlocked[{enum_name("Earth")}] = true;
        g->unlocked[{enum_name("Air")}] = true;
        save_unlocked(g);
    }}
    rebuild_inventory(g);
}}

const char *game_item_name(ItemId id)
{{
    if (id >= GAME_ITEM_COUNT) {{
        return "?";
    }}
    return kNames[id];
}}

int game_unlocked_count(const GameState *g)
{{
    return g->inventory_count;
}}

void game_move(GameState *g, int delta)
{{
    if (g->inventory_count <= 0) {{
        return;
    }}
    g->cursor += delta;
    if (g->cursor < 0) {{
        g->cursor = g->inventory_count - 1;
    }} else if (g->cursor >= g->inventory_count) {{
        g->cursor = 0;
    }}
    if (g->cursor < g->scroll) {{
        g->scroll = g->cursor;
    }} else if (g->cursor >= g->scroll + game_visible) {{
        g->scroll = g->cursor - game_visible + 1;
    }}
}}

void game_clear_slots(GameState *g)
{{
    g->slot_a = -1;
    g->slot_b = -1;
}}

ItemId game_pick(GameState *g)
{{
    if (g->inventory_count <= 0) {{
        return static_cast<ItemId>(0xFF);
    }}
    const ItemId id = g->inventory[g->cursor];

    if (g->slot_a < 0) {{
        g->slot_a = static_cast<int16_t>(id);
        g->slot_b = -1;
        return static_cast<ItemId>(0xFF);
    }}

    g->slot_b = static_cast<int16_t>(id);
    const ItemId result = combine(static_cast<ItemId>(g->slot_a), id);
    g->slot_a = -1;
    g->slot_b = -1;
    if (result == static_cast<ItemId>(0xFF) || !unlock(g, result)) {{
        return static_cast<ItemId>(0xFF);
    }}
    return result;
}}
"""
    open("main/game.cpp", "w").write(body)


def write_md(
    items: list[str], recipes: list[tuple[str, str, str]], starters: tuple[str, ...]
) -> None:
    by_out: dict[str, list[tuple[str, str]]] = {i: [] for i in items}
    for a, b, out in recipes:
        by_out[out].append((a, b))

    lines = [
        "# Alchemy catalog",
        "",
        f"**{len(items)} items**, **{len(recipes)} combinations**.",
        "",
        "Recipes lean on [Little Alchemy](https://littlealchemy.com/) /",
        "[Little Alchemy 2](https://littlealchemy2.com/) style mixes",
        "([official hints](https://hints.littlealchemy2.com/),",
        "[combination list](https://littlealchemy2cheats.com/combinations)),",
        "plus a few Cardputer easter eggs.",
        "",
        "Starters (unlocked at boot): " + ", ".join(starters) + ".",
        "",
        "## Items",
        "",
        "| # | Item | How to unlock |",
        "|--:|------|---------------|",
    ]
    for i, name in enumerate(items):
        if name in starters:
            how = "_starter_"
        else:
            how = "; ".join(f"{a} + {b}" for a, b in by_out[name]) or "_missing_"
        lines.append(f"| {i} | {name} | {how} |")

    lines += [
        "",
        "## Combinations",
        "",
        "| A | B | Result |",
        "|---|---|--------|",
    ]
    for a, b, out in recipes:
        lines.append(f"| {a} | {b} | {out} |")
    lines.append("")
    open("COMBINATIONS.md", "w").write("\n".join(lines))


def main() -> None:
    assert len(ITEMS) == len(set(ITEMS)), "duplicate item names"
    assert len(ITEMS) <= 255, "ItemId is uint8_t"
    recipes = clean_recipes(ITEMS, RECIPES)
    check_graph(ITEMS, recipes)
    write_hpp(ITEMS)
    write_cpp(ITEMS, recipes)
    write_md(ITEMS, recipes, STARTERS)
    print("Wrote main/game.hpp main/game.cpp COMBINATIONS.md")


if __name__ == "__main__":
    main()
