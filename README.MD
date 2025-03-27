# WhatWatt GO Integration for Home Assistant

Ten add-on umożliwia łatwą integrację urządzenia WhatWatt GO z systemem Home Assistant, automatyzując proces konfiguracji MQTT oraz dodawania sensorów do monitorowania energii.

## Funkcje

- Automatyczna konfiguracja urządzenia WhatWatt GO do komunikacji przez MQTT
- Automatyczne tworzenie sensorów w Home Assistant dla monitorowanych parametrów
- Wsparcie dla różnych kodów OBIS umożliwiających monitorowanie:
  - Mocy pobieranej i oddawanej
  - Energii pobranej i oddanej
  - Napięcia na poszczególnych fazach (L1, L2, L3)
- Automatyczne wykrywanie i konfiguracja z oficjalnym add-onem Mosquitto

## Wymagania

- Home Assistant w wersji 14 lub nowszej
- Urządzenie WhatWatt GO podłączone do sieci lokalnej
- Broker MQTT (zalecany oficjalny add-on Mosquitto)
- Licencja na usługi REST API i MQTT dla urządzenia WhatWatt GO

## Instalacja

1. Dodaj to repozytorium do swojego Home Assistant
2. Zainstaluj add-on "WhatWatt GO Integration"
3. Skonfiguruj add-on podając adres IP urządzenia WhatWatt GO oraz dane MQTT
4. Uruchom add-on
5. Po uruchomieniu add-on automatycznie skonfiguruje urządzenie WhatWatt GO oraz utworzy sensory w Home Assistant

## Konfiguracja

### Opcje add-onu

| Opcja | Opis |
|-------|------|
| `whatwatt_ip` | Adres IP urządzenia WhatWatt GO |
| `mqtt_broker` | Adres brokera MQTT (domyślnie: core-mosquitto) |
| `mqtt_username` | Nazwa użytkownika MQTT |
| `mqtt_password` | Hasło użytkownika MQTT |
| `mqtt_port` | Port MQTT (domyślnie: 1883) |
| `mqtt_topic` | Temat MQTT dla danych (domyślnie: energy/whatwatt/go) |
| `reporting_interval` | Interwał raportowania w sekundach (10-300, domyślnie: 30) |
| `obis_codes` | Lista kodów OBIS do monitorowania |

### Konfiguracja Home Assistant

Add-on automatycznie tworzy plik konfiguracyjny `whatwatt_sensors.yaml` w katalogu konfiguracyjnym Home Assistant. Aby aktywować sensory, dodaj następującą linię do pliku `configuration.yaml`:

```yaml
mqtt: !include whatwatt_sensors.yaml
```

Po zapisaniu zmian i ponownym uruchomieniu Home Assistant, sensory będą dostępne w systemie.

## Wizualizacja danych

Po skonfigurowaniu sensorów możesz dodać je do dashboardu Home Assistant:

1. Przejdź do Overview w Home Assistant
2. Kliknij "Edit Dashboard"
3. Dodaj kartę Entity Card dla wybranych sensorów
4. Zapisz zmiany, aby zobaczyć dane na dashboardzie

## Rozwiązywanie problemów

- Jeśli sensory nie pokazują danych, sprawdź w "Developer Tools > States" czy sensory (np. sensor.power_in) istnieją i otrzymują wartości
- Sprawdź logi Home Assistant pod kątem ostrzeżeń dotyczących połączenia z brokerem MQTT
- Upewnij się, że urządzenie WhatWatt GO publikuje dane (możesz to sprawdzić używając klienta MQTT do subskrypcji tematu)

## Wskazówki

- Dla optymalnego działania, ustaw interwał raportowania na 30 sekund
- Dalsza personalizacja sensorów możliwa jest bezpośrednio w pliku `whatwatt_sensors.yaml`
- Aby wykorzystać sensory energii w Energy Dashboard Home Assistant, ustaw odpowiednie atrybuty `device_class` i `state_class` w konfiguracji sensorów

## Uwagi

Usługi takie jak REST API i MQTT wymagają licencji. Sprawdź [www.whatwatt.ch/pricing](https://www.whatwatt.ch/pricing) aby uzyskać więcej informacji.