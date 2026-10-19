# cardputer-adv-template

Minimal [ESP-IDF](https://docs.espressif.com/projects/esp-idf/) starter for the **M5Stack Cardputer ADV** only.

Fork this for games/apps. It is not a full demo and not a template for the original Cardputer (GPIO matrix keyboard). ADV uses a **TCA8418** over I2C — if keys do nothing, you are on the wrong board.

Hardware: [Cardputer ADV](https://docs.m5stack.com/en/core/Cardputer-Adv) (Stamp-S3A / ESP32-S3, 8 MB flash, 1.14" LCD).

## Prerequisites (one-time)

Follow Espressif’s [Linux/macOS setup for ESP-IDF v5.4.2](https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/get-started/linux-macos-setup.html). Summary for macOS:

### 0. Homebrew

Install [Homebrew](https://brew.sh) if you do not have it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Also install Xcode CLT if macOS complains about `xcrun`:

```bash
xcode-select --install
```

### 1. Toolchain packages

```bash
brew install cmake ninja dfu-util ccache
```

`ccache` speeds up rebuilds; project scripts set `IDF_CCACHE_ENABLE=1` automatically. `ninja` is required for the fast watch path.

Optional if `python3` is missing: `brew install python3`.

### 2. Get ESP-IDF v5.4.2

```bash
mkdir -p ~/esp
cd ~/esp
git clone -b v5.4.2 --recursive https://github.com/espressif/esp-idf.git
```

### 3. Install IDF tools

```bash
cd ~/esp/esp-idf
./install.sh esp32s3
```

### 4. Export the environment (every new shell)

```bash
. ~/esp/esp-idf/export.sh
```

You need a USB-C cable and the Cardputer ADV connected for flash/monitor.

If the shell already has IDF exported, `scripts/idf.sh` skips re-sourcing `export.sh` (faster `npm run *` loops).

## One-time project deps (then offline)

Pin and vendor [M5GFX](https://github.com/m5stack/M5GFX) locally (needs Cardputer ADV board support — **0.2.29+**):

```bash
git clone --branch 0.2.33 --depth 1 https://github.com/m5stack/M5GFX.git components/M5GFX
```

After this, builds do not need the network.

## Build & flash

With Node/npm (scripts load ESP-IDF for you):

```bash
npm run deps              # clone M5GFX once into components/
npm run setup             # idf.py set-target esp32s3 (once per checkout)
npm run build             # compile only (idf.py)
npm run flash             # full flash (bootloader + partitions + app) — first bring-up / after partition changes
npm run app-flash         # app image only (day-to-day)
npm run monitor           # serial console only
npm run flash:monitor     # full flash once, then open serial (no watch)
npm run dev:build         # watch main/; ninja rebuild only on save
npm run dev               # watch main/; ninja app-flash on save (no monitor)
npm run menuconfig        # ESP-IDF config UI
npm run clean             # fullclean build tree (use only if build is broken)
npm run bin               # write merged flash image to bins/
```

### Fast edit → live loop

1. `npm run setup` + `npm run build` once per checkout (creates `build/`).
2. `npm run dev:build` until the project compiles cleanly.
3. `npm run dev` to push to the device on each save via [`scripts/fast-build.sh`](scripts/fast-build.sh).
4. Optional second terminal: `npm run monitor`. If monitor already holds the port, flash from it with `Ctrl+T` then `Ctrl+F` instead of running `dev`.

**Why this is fast:** a normal `ninja` rebuild after a one-line edit spends ~4–5s regenerating `sections.ld` (ldgen) even though the linker script did not change, plus ~2s if `export.sh` runs again. `fast-build` compiles `main/`, then **reuses the existing `sections.ld`** and links/elf2images directly (~1.4s vs ~6s measured here). `watch.sh` exports IDF **once** and lets `entr` inherit that env (no re-export per save).

Tweak colors/strings in [`main/theme.cpp`](main/theme.cpp) so you do not recompile M5GFX. Display helpers live in [`main/display.cpp`](main/display.cpp) (PCH’d).

```bash
npm run fast-build          # app .bin only (~1–2s after theme edit)
npm run app-flash           # fast-build + flash @ 921600
npm run app-flash:full      # official idf.py app-flash (runs ldgen)
```

Override baud if needed: `ESPBAUD=460800 npm run dev`. On IDF 5.4+, flash baud is **not** an sdkconfig option — scripts set `ESPBAUD`.

There is no live UI reload. Optional but snappier watches: `brew install entr`.

After `menuconfig` / CMake changes, run a normal `npm run build` once so ldgen refreshes; then `fast-build` / `dev` again.

`flash` / `app-flash` / `monitor` / `flash:monitor` / `dev` auto-pick a USB serial port (`/dev/cu.usbmodem*` on macOS, `/dev/ttyACM*` on Linux) via `scripts/port.sh`. Override with `PORT=…` if needed:

```bash
PORT=/dev/cu.usbmodem14201 npm run dev
```

Prebuilt merged image (bootloader + partition table + app, flash at `0x0`):

- [`bins/cardputer_adv_template.bin`](bins/cardputer_adv_template.bin)

Or call `idf.py` directly after `. ~/esp/esp-idf/export.sh`.

Put the device in download mode if flash fails (hold G0 / reset per Stamp-S3 docs).

## What the sample does

Clears the LCD, waits for one TCA8418 key press, then draws the key code. That proves display + ADV keyboard wiring.

## How to: colors & copy

All visuals go through a thin theme layer so you can tweak without pulling in M5GFX.

| File | Role |
|------|------|
| [`main/theme.cpp`](main/theme.cpp) | **Edit here** — RGB565 colors + UI strings |
| [`main/theme.hpp`](main/theme.hpp) | Declarations (no M5GFX) |
| [`main/display.cpp`](main/display.cpp) | Applies theme via M5GFX (`fillScreen`, `setTextColor`, …) |
| [`main/app_main.cpp`](main/app_main.cpp) | Calls `display_show_*` — no color literals |

### Palette

| Variable | Used for |
|----------|----------|
| `theme_col_bg` | Idle screen background |
| `theme_col_fg` | Normal text (on bg / ok bg) |
| `theme_col_err` | Keyboard-init error text |
| `theme_col_ok_bg` | Background after a key press |

Strings: `theme_title`, `theme_prompt`, `theme_kbd_error`.

Example in `theme.cpp`:

```cpp
uint16_t theme_col_bg = 0x001F;     // TFT_BLUE
uint16_t theme_col_fg = 0xFFFF;     // TFT_WHITE
uint16_t theme_col_err = 0xF800;    // TFT_RED
uint16_t theme_col_ok_bg = 0x03E0;  // TFT_DARKGREEN
```

Values are **RGB565** (same as LovyanGFX `TFT_*`). After a theme edit: `npm run dev` (or `npm run app-flash`) — fast path skips regenerating M5GFX / ldgen.

### Common RGB565 colors

Full named list lives in M5GFX after `npm run deps`:  
`components/M5GFX/src/lgfx/v1/misc/enum.hpp` (search `TFT_BLACK`). You can also use any custom color via `display.color565(r, g, b)` inside `display.cpp`.

| | Name | RGB565 | RGB |
|---:|------|--------|-----|
| ![#000000](https://placehold.co/20x20/000000/000000.png) | `TFT_BLACK` | `0x0000` | 0, 0, 0 |
| ![#000080](https://placehold.co/20x20/000080/000080.png) | `TFT_NAVY` | `0x000F` | 0, 0, 128 |
| ![#008000](https://placehold.co/20x20/008000/008000.png) | `TFT_DARKGREEN` | `0x03E0` | 0, 128, 0 |
| ![#008080](https://placehold.co/20x20/008080/008080.png) | `TFT_DARKCYAN` | `0x03EF` | 0, 128, 128 |
| ![#800000](https://placehold.co/20x20/800000/800000.png) | `TFT_MAROON` | `0x7800` | 128, 0, 0 |
| ![#800080](https://placehold.co/20x20/800080/800080.png) | `TFT_PURPLE` | `0x780F` | 128, 0, 128 |
| ![#808000](https://placehold.co/20x20/808000/808000.png) | `TFT_OLIVE` | `0x7BE0` | 128, 128, 0 |
| ![#D3D3D3](https://placehold.co/20x20/D3D3D3/D3D3D3.png) | `TFT_LIGHTGREY` | `0xD69A` | 211, 211, 211 |
| ![#808080](https://placehold.co/20x20/808080/808080.png) | `TFT_DARKGREY` | `0x7BEF` | 128, 128, 128 |
| ![#0000FF](https://placehold.co/20x20/0000FF/0000FF.png) | `TFT_BLUE` | `0x001F` | 0, 0, 255 |
| ![#00FF00](https://placehold.co/20x20/00FF00/00FF00.png) | `TFT_GREEN` | `0x07E0` | 0, 255, 0 |
| ![#00FFFF](https://placehold.co/20x20/00FFFF/00FFFF.png) | `TFT_CYAN` | `0x07FF` | 0, 255, 255 |
| ![#FF0000](https://placehold.co/20x20/FF0000/FF0000.png) | `TFT_RED` | `0xF800` | 255, 0, 0 |
| ![#FF00FF](https://placehold.co/20x20/FF00FF/FF00FF.png) | `TFT_MAGENTA` | `0xF81F` | 255, 0, 255 |
| ![#FFFF00](https://placehold.co/20x20/FFFF00/FFFF00.png) | `TFT_YELLOW` | `0xFFE0` | 255, 255, 0 |
| ![#FFFFFF](https://placehold.co/20x20/FFFFFF/FFFFFF.png) | `TFT_WHITE` | `0xFFFF` | 255, 255, 255 |
| ![#FFB400](https://placehold.co/20x20/FFB400/FFB400.png) | `TFT_ORANGE` | `0xFDA0` | 255, 180, 0 |
| ![#B4FF00](https://placehold.co/20x20/B4FF00/B4FF00.png) | `TFT_GREENYELLOW` | `0xB7E0` | 180, 255, 0 |
| ![#FFC0CB](https://placehold.co/20x20/FFC0CB/FFC0CB.png) | `TFT_PINK` | `0xFE19` | 255, 192, 203 |
| ![#964B00](https://placehold.co/20x20/964B00/964B00.png) | `TFT_BROWN` | `0x9A60` | 150, 75, 0 |
| ![#FFD700](https://placehold.co/20x20/FFD700/FFD700.png) | `TFT_GOLD` | `0xFEA0` | 255, 215, 0 |
| ![#C0C0C0](https://placehold.co/20x20/C0C0C0/C0C0C0.png) | `TFT_SILVER` | `0xC618` | 192, 192, 192 |
| ![#87CEEB](https://placehold.co/20x20/87CEEB/87CEEB.png) | `TFT_SKYBLUE` | `0x867D` | 135, 206, 235 |
| ![#B42EE2](https://placehold.co/20x20/B42EE2/B42EE2.png) | `TFT_VIOLET` | `0x915C` | 180, 46, 226 |

## Layout

```
package.json          # npm run build / flash / dev / …
scripts/idf.sh        # sources ESP-IDF (skips if already exported), runs idf.py @ 921600 baud
scripts/fast-build.sh # incremental build skipping ldgen (used by dev / app-flash)
scripts/port.sh       # auto-detect USB serial port (or $PORT)
scripts/watch.sh      # watch → fast-build for npm run dev / dev:build
bins/                 # merged .bin (flash at 0x0)
CMakeLists.txt
sdkconfig.defaults    # 8 MB flash, USB Serial/JTAG console
main/app_main.cpp     # hello-world + keyboard
main/theme.cpp        # colors/strings (edit here for fast visual tweaks)
main/theme.hpp
main/display.cpp      # M5GFX helpers
main/display.hpp
main/pch_display.hpp  # M5GFX precompiled header for display.cpp
components/M5GFX/     # after clone (gitignored)
```

## Out of scope

Games, audio/IMU, and dropping a merged `.bin` into an installer catalog.

## Credits

- [M5GFX](https://github.com/m5stack/M5GFX)
- [M5Cardputer-UserDemo `CardputerADV`](https://github.com/m5stack/M5Cardputer-UserDemo/tree/CardputerADV) (fetch → `idf.py build` reference)
- TCA8418 keypad controller (I2C)

## License

Released under the [MIT license](LICENSE).

## Colophon

Cardputer ADV firmware toy built from the ADV template. Display + TCA8418 keyboard on Stamp-S3A, with a fast npm/ninja edit→flash loop. Vibe coded with [Cursor](https://cursor.com).

**Stack**

| Piece | Choice |
|---|---|
| Firmware | [ESP-IDF](https://docs.espressif.com/projects/esp-idf/) v5.4.2 (ESP32-S3) |
| Display | [M5GFX](https://github.com/m5stack/M5GFX) |
| Keyboard | TCA8418 over I2C |
| Tooling | npm scripts, ninja, ccache, `scripts/fast-build.sh` |
| Device | [M5Stack Cardputer ADV](https://docs.m5stack.com/en/core/Cardputer-Adv) |

**Tools**

- [ESP-IDF](https://docs.espressif.com/projects/esp-idf/): build / flash / monitor
- [M5GFX](https://github.com/m5stack/M5GFX): LCD
- [Cursor](https://cursor.com): vibe coding

