#pragma once

#include <cstdint>

// Tweak colors/strings here (or in theme.cpp) — no M5GFX include, fast rebuilds.

extern uint16_t theme_col_bg;
extern uint16_t theme_col_fg;
extern uint16_t theme_col_err;
extern uint16_t theme_col_ok_bg;
extern uint16_t theme_col_dim;

extern const char *theme_title;
extern const char *theme_kbd_error;

extern const char *theme_help_title;
extern const char *theme_help_lines[];
extern const int theme_help_line_count;
