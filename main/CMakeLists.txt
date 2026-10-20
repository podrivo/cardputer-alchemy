idf_component_register(
    SRCS "app_main.cpp" "display.cpp" "theme.cpp" "game.cpp" "sound.cpp"
    INCLUDE_DIRS "."
    REQUIRES M5GFX driver esp_driver_i2s nvs_flash
)

# PCH for M5GFX — only on display.cpp so theme/app_main/game stay light.
idf_component_get_property(main_lib ${COMPONENT_NAME} COMPONENT_LIB)
set_source_files_properties(app_main.cpp theme.cpp game.cpp sound.cpp PROPERTIES SKIP_PRECOMPILE_HEADERS ON)
target_precompile_headers(${main_lib} PRIVATE "pch_display.hpp")
