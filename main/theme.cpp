#include "theme.hpp"

// RGB565 (same values as LovyanGFX TFT_*). Edit these for quick visual iteration.
uint16_t theme_col_bg = 0x000F;     // near-black blue
uint16_t theme_col_fg = 0xFFFF;     // white
uint16_t theme_col_err = 0xF800;    // red
uint16_t theme_col_ok_bg = 0x03E0;  // dark green
uint16_t theme_col_dim = 0x7BEF;    // dark grey

const char *theme_title = "Alchemy";
const char *theme_kbd_error = "No TCA8418";

const char *theme_help_title = "Shortcuts";
const char *theme_help_lines[] = {
    "^v  move",
    "ent pick",
    "del clear",
    "esc close",
};
const int theme_help_line_count =
    static_cast<int>(sizeof(theme_help_lines) / sizeof(theme_help_lines[0]));
