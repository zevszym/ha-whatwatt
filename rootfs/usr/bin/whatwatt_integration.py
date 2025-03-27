#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import time
import requests
import yaml

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
_LOGGER = logging.getLogger("whatwatt-integration")

def parse_args():
    """Parsowanie argumentów wiersza poleceń."""
    parser = argparse.ArgumentParser(description='WhatWatt GO Integration for Home Assistant')
    parser.add_argument('--whatwatt-ip', required=True, help='IP address of WhatWatt GO device')
    parser.add_argument('--mqtt-broker', required=True, help='MQTT broker address')
    parser.add_argument('--mqtt-username', required=False, help='MQTT username')
    parser.add_argument('--mqtt-password', required=False, help='MQTT password')
    parser.add_argument('--mqtt-port', type=int, default=1883, help='MQTT port')
    parser.add_argument('--mqtt-topic', default='energy/whatwatt/go', help='MQTT topic for WhatWatt GO')
    parser.add_argument('--reporting-interval', type=int, default=30, help='Reporting interval in seconds')
    parser.add_argument('--config', required=True, help='Path to configuration file')
    return parser.parse_args()

def configure_whatwatt(args, obis_codes):
    """Konfiguracja urządzenia WhatWatt GO."""
    # Pobranie listy OBIS z konfiguracji
    template = build_template(obis_codes)
    
    # Tworzymy adres URL dla interfejsu WebUI
    base_url = f"http://{args.whatwatt_ip}"
    _LOGGER.info(f"Konfiguracja urządzenia WhatWatt GO na {base_url}")
    
    # Konfiguracja MQTT w WhatWatt GO
    mqtt_url = f"mqtt://{args.mqtt_broker}:{args.mqtt_port}"
    mqtt_config = {
        "active": True,
        "broker_url": mqtt_url,
        "username": args.mqtt_username,
        "password": args.mqtt_password,
        "client_id": "whatwattGO",
        "topic": args.mqtt_topic,
        "template": template
    }
    
    try:
        # Najpierw sprawdzamy, czy urządzenie jest dostępne
        response = requests.get(f"{base_url}/api/status", timeout=10)
        if response.status_code != 200:
            _LOGGER.error(f"Nie można połączyć się z urządzeniem WhatWatt GO: {response.status_code}")
            return False
            
        # Konfiguracja MQTT
        response = requests.post(
            f"{base_url}/api/mqtt/config", 
            json=mqtt_config,
            timeout=10
        )
        if response.status_code != 200:
            _LOGGER.error(f"Nie można skonfigurować MQTT: {response.status_code}")
            return False
            
        # Ustawienie częstotliwości raportowania
        response = requests.post(
            f"{base_url}/api/system/config",
            json={"interval_to_systems": args.reporting_interval},
            timeout=10
        )
        if response.status_code != 200:
            _LOGGER.error(f"Nie można ustawić interwału raportowania: {response.status_code}")
            return False
            
        _LOGGER.info("Konfiguracja WhatWatt GO zakończona pomyślnie")
        return True
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"Błąd podczas konfiguracji WhatWatt GO: {e}")
        return False

def build_template(obis_codes):
    """Budowanie szablonu MQTT na podstawie kodów OBIS."""
    template = {
        "sys_id": "${sys.id}",
        "meter_id": "${meter.id}",
        "time": "${timestamp}"
    }
    
    # Mapowanie kodów OBIS na nazwy w JSON
    obis_mapping = {
        "1_7_0": "power_in",
        "2_7_0": "power_out",
        "1_8_0": "energy_in",
        "2_8_0": "energy_out",
        "32_7_0": "voltage_l1",
        "52_7_0": "voltage_l2",
        "72_7_0": "voltage_l3"
    }
    
    # Dodawanie kodów OBIS do szablonu
    for obis in obis_codes:
        if obis in obis_mapping:
            template[obis_mapping[obis]] = "${" + obis + "}"
    
    return json.dumps(template, indent=2)

def generate_sensor_config(args, obis_codes):
    """Generowanie konfiguracji czujników dla Home Assistant."""
    # Mapowanie kodów OBIS na nazwy, ikony i jednostki
    sensor_config = {
        "1_7_0": {
            "name": "Power In",
            "icon": "mdi:transmission-tower-import",
            "unit": "kW"
        },
        "2_7_0": {
            "name": "Power Out",
            "icon": "mdi:transmission-tower-export",
            "unit": "kW"
        },
        "1_8_0": {
            "name": "Energy In",
            "icon": "mdi:lightning-bolt",
            "unit": "kWh",
            "device_class": "energy",
            "state_class": "total_increasing"
        },
        "2_8_0": {
            "name": "Energy Out",
            "icon": "mdi:lightning-bolt",
            "unit": "kWh",
            "device_class": "energy",
            "state_class": "total_increasing"
        },
        "32_7_0": {
            "name": "Voltage L1",
            "icon": "mdi:sine-wave",
            "unit": "V",
            "device_class": "voltage",
            "state_class": "measurement"
        },
        "52_7_0": {
            "name": "Voltage L2",
            "icon": "mdi:sine-wave",
            "unit": "V",
            "device_class": "voltage",
            "state_class": "measurement"
        },
        "72_7_0": {
            "name": "Voltage L3",
            "icon": "mdi:sine-wave",
            "unit": "V",
            "device_class": "voltage",
            "state_class": "measurement"
        }
    }
    
    # Generowanie konfiguracji MQTT dla Home Assistant
    mqtt_sensors = []
    
    for obis in obis_codes:
        if obis in sensor_config:
            info = sensor_config[obis]
            sensor = {
                "name": info["name"],
                "unique_id": f"whatwatt_{obis.lower().replace('_', '')}",
                "icon": info["icon"],
                "state_topic": args.mqtt_topic,
                "value_template": "{{ value_json." + obis_mapping[obis] + " }}",
                "unit_of_measurement": info["unit"]
            }
            
            # Dodawanie opcjonalnych pól, jeśli są dostępne
            if "device_class" in info:
                sensor["device_class"] = info["device_class"]
            if "state_class" in info:
                sensor["state_class"] = info["state_class"]
                
            mqtt_sensors.append(sensor)
    
    # Tworzenie konfiguracji YAML
    config = {
        "mqtt": {
            "sensor": mqtt_sensors
        }
    }
    
    # Zapis konfiguracji do pliku
    config_path = "/config/whatwatt_sensors.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    _LOGGER.info(f"Konfiguracja czujników zapisana do {config_path}")
    _LOGGER.info("Dodaj następującą linię do pliku configuration.yaml:")
    _LOGGER.info("mqtt: !include whatwatt_sensors.yaml")
    
    return True

def main():
    """Główna funkcja."""
    args = parse_args()
    
    try:
        # Wczytaj konfigurację
        with open(args.config, 'r') as f:
            config = json.load(f)
        
        # Pobierz listę kodów OBIS
        obis_codes = config.get('obis_codes', [])
        
        # Konfiguracja urządzenia WhatWatt GO
        if not configure_whatwatt(args, obis_codes):
            _LOGGER.error("Konfiguracja WhatWatt GO nie powiodła się")
            sys.exit(1)
        
        # Generowanie konfiguracji czujników dla Home Assistant
        if not generate_sensor_config(args, obis_codes):
            _LOGGER.error("Generowanie konfiguracji nie powiodło się")
            sys.exit(1)
        
        # Pętla monitorująca status urządzenia
        _LOGGER.info("Rozpoczęcie monitorowania urządzenia WhatWatt GO")
        while True:
            try:
                response = requests.get(f"http://{args.whatwatt_ip}/api/status", timeout=5)
                if response.status_code == 200:
                    _LOGGER.debug("Urządzenie WhatWatt GO działa poprawnie")
                else:
                    _LOGGER.warning(f"Urządzenie WhatWatt GO nie odpowiada poprawnie: {response.status_code}")
            except requests.exceptions.RequestException as e:
                _LOGGER.warning(f"Nie można połączyć się z urządzeniem WhatWatt GO: {e}")
                
            time.sleep(60)  # Sprawdzanie co minutę
            
    except Exception as e:
        _LOGGER.error(f"Wystąpił błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()