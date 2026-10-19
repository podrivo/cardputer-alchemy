#pragma once

#include "game.hpp"

// Thin display API — keeps M5GFX out of other translation units.

void display_init();
void display_show_kbd_error();
void display_show_game(const GameState *g, bool highlight);
