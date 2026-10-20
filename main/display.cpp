#include "pch_display.hpp"

#include "display.hpp"
#include "theme.hpp"

namespace {

M5GFX display;

constexpr int kListTop = 28;
constexpr int kRowH = 12;

const char *slot_label(int16_t slot)
{
    if (slot < 0) {
        return "-";
    }
    return game_item_name(static_cast<ItemId>(slot));
}

} // namespace

void display_init()
{
    display.init();
    display.setRotation(1);

    int rows = (display.height() - kListTop) / kRowH;
    if (rows < 1) {
        rows = 1;
    }
    game_visible = rows;

    display.fillRect(0, 0, display.width(), display.height(), theme_col_bg);
}

void display_show_kbd_error()
{
    display.fillRect(0, 0, display.width(), display.height(), theme_col_bg);
    display.setTextColor(theme_col_err, theme_col_bg);
    display.setTextSize(1);
    display.setCursor(8, 60);
    display.print(theme_kbd_error);
}

void display_show_help()
{
    display.fillRect(0, 0, display.width(), display.height(), theme_col_bg);
    display.setTextColor(theme_col_fg, theme_col_bg);
    display.setTextSize(1);

    display.setCursor(4, 2);
    display.print(theme_help_title);

    for (int i = 0; i < theme_help_line_count; ++i) {
        display.setCursor(4, 20 + i * kRowH);
        display.print(theme_help_lines[i]);
    }
}

void display_show_game(const GameState *g, bool highlight)
{
    const uint16_t bg = highlight ? theme_col_ok_bg : theme_col_bg;
    display.fillRect(0, 0, display.width(), display.height(), bg);
    display.setTextColor(theme_col_fg, bg);
    display.setTextSize(1);

    display.setCursor(4, 2);
    display.printf("%s  %d/%d", theme_title, game_unlocked_count(g), GAME_ITEM_COUNT);

    display.setCursor(4, 14);
    display.printf("%s + %s", slot_label(g->slot_a), slot_label(g->slot_b));

    const int last = g->scroll + game_visible;
    for (int i = g->scroll; i < g->inventory_count && i < last; ++i) {
        const int row = i - g->scroll;
        display.setCursor(4, kListTop + row * kRowH);
        display.printf("%c %s", i == g->cursor ? '>' : ' ',
                       game_item_name(g->inventory[i]));
    }
}
