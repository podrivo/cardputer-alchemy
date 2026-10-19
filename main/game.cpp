#include "game.hpp"

#include <cstdio>
#include <cstring>

namespace {

char status_buf[28];


const char *const kNames[GAME_ITEM_COUNT] = {
    "Fire", "Water", "Earth", "Air", "Steam",
    "Lava", "Mud", "Dust", "Energy", "Rain",
};

struct Recipe {
    ItemId a;
    ItemId b;
    ItemId out;
};

constexpr Recipe kRecipes[] = {
    {ITEM_FIRE, ITEM_WATER, ITEM_STEAM},
    {ITEM_FIRE, ITEM_EARTH, ITEM_LAVA},
    {ITEM_WATER, ITEM_EARTH, ITEM_MUD},
    {ITEM_AIR, ITEM_EARTH, ITEM_DUST},
    {ITEM_FIRE, ITEM_AIR, ITEM_ENERGY},
    {ITEM_WATER, ITEM_AIR, ITEM_RAIN},
};

void rebuild_inventory(GameState *g)
{
    g->inventory_count = 0;
    for (int i = 0; i < GAME_ITEM_COUNT; ++i) {
        if (g->unlocked[i]) {
            g->inventory[g->inventory_count++] = static_cast<ItemId>(i);
        }
    }
    if (g->cursor >= g->inventory_count) {
        g->cursor = g->inventory_count > 0 ? g->inventory_count - 1 : 0;
    }
    if (g->scroll > g->cursor) {
        g->scroll = g->cursor;
    }
    if (g->cursor >= g->scroll + GAME_VISIBLE) {
        g->scroll = g->cursor - GAME_VISIBLE + 1;
    }
    if (g->scroll < 0) {
        g->scroll = 0;
    }
}

bool unlock(GameState *g, ItemId id)
{
    if (g->unlocked[id]) {
        return false;
    }
    g->unlocked[id] = true;
    rebuild_inventory(g);
    return true;
}

ItemId combine(ItemId a, ItemId b)
{
    for (const Recipe &r : kRecipes) {
        if ((r.a == a && r.b == b) || (r.a == b && r.b == a)) {
            return r.out;
        }
    }
    return static_cast<ItemId>(0xFF);
}

} // namespace

void game_init(GameState *g)
{
    std::memset(g, 0, sizeof(*g));
    g->slot_a = -1;
    g->slot_b = -1;
    g->unlocked[ITEM_FIRE] = true;
    g->unlocked[ITEM_WATER] = true;
    g->unlocked[ITEM_EARTH] = true;
    g->unlocked[ITEM_AIR] = true;
    g->status = "Pick two to combine";
    rebuild_inventory(g);
}

const char *game_item_name(ItemId id)
{
    if (id >= GAME_ITEM_COUNT) {
        return "?";
    }
    return kNames[id];
}

int game_unlocked_count(const GameState *g)
{
    return g->inventory_count;
}

void game_move(GameState *g, int delta)
{
    if (g->inventory_count <= 0) {
        return;
    }
    g->cursor += delta;
    if (g->cursor < 0) {
        g->cursor = g->inventory_count - 1;
    } else if (g->cursor >= g->inventory_count) {
        g->cursor = 0;
    }
    if (g->cursor < g->scroll) {
        g->scroll = g->cursor;
    } else if (g->cursor >= g->scroll + GAME_VISIBLE) {
        g->scroll = g->cursor - GAME_VISIBLE + 1;
    }
}

void game_clear_slots(GameState *g)
{
    g->slot_a = -1;
    g->slot_b = -1;
    g->status = "Pick two to combine";
}

bool game_pick(GameState *g)
{
    if (g->inventory_count <= 0) {
        return false;
    }
    const ItemId id = g->inventory[g->cursor];

    if (g->slot_a < 0) {
        g->slot_a = static_cast<int8_t>(id);
        g->slot_b = -1;
        g->status = "Pick second item";
        return false;
    }

    g->slot_b = static_cast<int8_t>(id);
    const ItemId result = combine(static_cast<ItemId>(g->slot_a), id);
    g->slot_a = -1;
    g->slot_b = -1;
    if (result == static_cast<ItemId>(0xFF)) {
        g->status = "Nothing happened";
        return false;
    }

    const bool is_new = unlock(g, result);
    std::snprintf(status_buf, sizeof(status_buf), is_new ? "New: %s" : "Got: %s",
                  game_item_name(result));
    g->status = status_buf;
    return is_new;
}
