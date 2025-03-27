#!/usr/bin/with-contenv bashio
# ==============================================================================
# Skrypt konfiguracyjny dla WhatWatt GO Integration
# ==============================================================================

bashio::log.info "Uruchamianie konfiguracji WhatWatt GO Integration..."

# Sprawdzenie dostępności Mosquitto
if bashio::addon.available "core_mosquitto"; then
    bashio::log.info "Wykryto oficjalny add-on Mosquitto. Ustawiam konfigurację MQTT..."
    
    # Pobieranie danych z Mosquitto
    if [ -z "$(bashio::config 'mqtt_username')" ]; then
        MQTT_USERNAME=$(bashio::addon.config 'core_mosquitto' 'logins[0].username')
        MQTT_PASSWORD=$(bashio::addon.config 'core_mosquitto' 'logins[0].password')
        
        # Aktualizacja konfiguracji
        if [ ! -z "$MQTT_USERNAME" ] && [ ! -z "$MQTT_PASSWORD" ]; then
            bashio::log.info "Zaktualizowano dane uwierzytelniające MQTT"
            bashio::addon.option 'mqtt_username' "$MQTT_USERNAME"
            bashio::addon.option 'mqtt_password' "$MQTT_PASSWORD"
        else
            bashio::log.warning "Nie można pobrać danych uwierzytelniających z Mosquitto"
        fi
    fi
else
    bashio::log.warning "Nie wykryto oficjalnego add-onu Mosquitto. Upewnij się, że masz działający broker MQTT."
fi

# Sprawdzenie IP urządzenia WhatWatt GO
if [ -z "$(bashio::config 'whatwatt_ip')" ]; then
    bashio::log.warning "Adres IP urządzenia WhatWatt GO nie jest skonfigurowany. Proszę ustawić go w konfiguracji."
fi

bashio::log.info "Konfiguracja WhatWatt GO Integration zakończona."