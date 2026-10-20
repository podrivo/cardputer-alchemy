#pragma once

#include "driver/i2c_master.h"

// Cardputer ADV speaker (ES8311 → NS4150B). Failures are non-fatal.

bool sound_init(i2c_master_bus_handle_t i2c_bus);
void sound_play_discover();
void sound_volume_up();
void sound_volume_down();
