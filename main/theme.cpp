#include "theme.hpp"

// RGB565 purple family (anchored to the dark bg). Edit for quick visual iteration.
uint16_t theme_col_bg = 0x180C;     // deep purple
uint16_t theme_col_fg = 0xEF7F;     // pale lavender
uint16_t theme_col_err = 0xF81F;    // magenta
uint16_t theme_col_ok_bg = 0x5014;  // mid purple (discovery flash)
uint16_t theme_col_dim = 0x7C1A;    // muted purple

const char *theme_title = "Alchemy";
const char *theme_kbd_error = "No TCA8418";

const char *theme_help_title = "Shortcuts";
const char *theme_help_lines[] = {
    "^v  move",
    "ent pick",
    "del clear",
    "+-  volume",
    "esc close",
};
const int theme_help_line_count =
    static_cast<int>(sizeof(theme_help_lines) / sizeof(theme_help_lines[0]));
