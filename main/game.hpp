#pragma once

#include <cstdint>

constexpr int GAME_ITEM_COUNT = 10;
constexpr int GAME_VISIBLE = 4;

enum ItemId : uint8_t {
    ITEM_FIRE = 0,
    ITEM_WATER,
    ITEM_EARTH,
    ITEM_AIR,
    ITEM_STEAM,
    ITEM_LAVA,
    ITEM_MUD,
    ITEM_DUST,
    ITEM_ENERGY,
    ITEM_RAIN,
};

struct GameState {
    bool unlocked[GAME_ITEM_COUNT];
    ItemId inventory[GAME_ITEM_COUNT]; // unlocked ids, dense
    int inventory_count;
    int cursor;       // index into inventory[]
    int scroll;       // first visible inventory index
    int8_t slot_a;    // ItemId or -1
    int8_t slot_b;    // ItemId or -1
    const char *status;
};

void game_init(GameState *g);
const char *game_item_name(ItemId id);
int game_unlocked_count(const GameState *g);

// Enter on current cursor item — fill A, then B+combine.
// Returns true if the screen should highlight a discovery.
bool game_pick(GameState *g);
void game_clear_slots(GameState *g);
void game_move(GameState *g, int delta);
