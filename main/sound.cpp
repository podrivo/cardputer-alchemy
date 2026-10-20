#include "sound.hpp"

#include "driver/gpio.h"
#include "driver/i2s_std.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

namespace {

constexpr char TAG[] = "sound";

constexpr uint8_t ES8311_ADDR = 0x18;
constexpr gpio_num_t I2S_BCLK = GPIO_NUM_41;
constexpr gpio_num_t I2S_WS = GPIO_NUM_43;
constexpr gpio_num_t I2S_DOUT = GPIO_NUM_42;
constexpr int SAMPLE_RATE = 16000;

i2c_master_dev_handle_t es8311;
i2s_chan_handle_t tx;
bool ready = false;

esp_err_t es_write(uint8_t reg, uint8_t val)
{
    uint8_t buf[2] = {reg, val};
    return i2c_master_transmit(es8311, buf, sizeof(buf), 100);
}

bool es8311_init()
{
    // Minimal DAC bring-up clocked from BCLK (no MCLK on ADV).
    // Sequence from M5Unified / espp Cardputer ADV speaker init.
    const uint8_t regs[][2] = {
        {0x00, 0x80}, // RESET: power on
        {0x01, 0xBF}, // CLOCK: MCLK from BCLK, clocks on
        {0x02, 0x18}, // CLOCK: MULT_PRE = 3
        {0x0D, 0x01}, // SYSTEM: analog power up
        {0x09, 0x0C}, // SDP IN: 16-bit I2S
        {0x12, 0x00}, // SYSTEM: DAC power up
        {0x13, 0x10}, // SYSTEM: enable HP drive
        {0x32, 0xBF}, // DAC: volume 0 dB
        {0x37, 0x08}, // DAC: bypass equalizer
    };
    for (const auto &r : regs) {
        if (es_write(r[0], r[1]) != ESP_OK) {
            return false;
        }
    }
    return true;
}

bool i2s_init()
{
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    chan_cfg.auto_clear = true;
    if (i2s_new_channel(&chan_cfg, &tx, nullptr) != ESP_OK) {
        return false;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg =
            {
                .mclk = GPIO_NUM_NC,
                .bclk = I2S_BCLK,
                .ws = I2S_WS,
                .dout = I2S_DOUT,
                .din = GPIO_NUM_NC,
                .invert_flags = {.mclk_inv = false, .bclk_inv = false, .ws_inv = false},
            },
    };
    if (i2s_channel_init_std_mode(tx, &std_cfg) != ESP_OK) {
        return false;
    }
    return i2s_channel_enable(tx) == ESP_OK;
}

void write_tone(int freq_hz, int ms)
{
    const int n = SAMPLE_RATE * ms / 1000;
    const int period = freq_hz > 0 ? SAMPLE_RATE / freq_hz : 1;
    int16_t buf[128];
    int written = 0;
    while (written < n) {
        const int chunk = (n - written) > 128 ? 128 : (n - written);
        for (int i = 0; i < chunk; ++i) {
            const int t = written + i;
            buf[i] = (period > 1 && (t % period) < (period / 2)) ? 9000 : -9000;
        }
        size_t bytes = 0;
        i2s_channel_write(tx, buf, chunk * sizeof(int16_t), &bytes, portMAX_DELAY);
        written += chunk;
    }
}

} // namespace

bool sound_init(i2c_master_bus_handle_t i2c_bus)
{
    i2c_device_config_t dev_cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = ES8311_ADDR,
        .scl_speed_hz = 400000,
    };
    if (i2c_master_bus_add_device(i2c_bus, &dev_cfg, &es8311) != ESP_OK) {
        ESP_LOGE(TAG, "ES8311 I2C add failed");
        return false;
    }
    if (!i2s_init()) {
        ESP_LOGE(TAG, "I2S init failed");
        return false;
    }
    // Codec clocks from BCLK — enable I2S first.
    if (!es8311_init()) {
        ESP_LOGE(TAG, "ES8311 init failed");
        return false;
    }
    ready = true;
    ESP_LOGI(TAG, "Speaker ready");
    return true;
}

void sound_play_discover()
{
    if (!ready) {
        return;
    }
    // Short ascending discovery jingle (C5–E5–G5–C6).
    write_tone(523, 70);
    write_tone(659, 70);
    write_tone(784, 80);
    write_tone(1047, 120);
    write_tone(0, 20);
}
