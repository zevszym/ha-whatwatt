# WhatWatt Home Assistant Integration

Custom Home Assistant integration for WhatWatt Go devices that read data from electricity meters.

## Features

- Connects to WhatWatt Go devices via MQTT
- Displays real-time power consumption and generation data
- Shows voltage levels for all three phases
- Tracks total energy consumption and generation
- Provides easy access to the device's configuration page

## Installation

### HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL `https://github.com/vestiacom/whatwatt-home-asistance-integration` with category "Integration"
5. Click "Add"
6. Search for "WhatWatt" in the integrations tab
7. Click "Download"
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/vestiacom/whatwatt-home-asistance-integration)
2. Extract the `custom_components/whatwatt` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Make sure your WhatWatt Go device is configured to send data to your MQTT broker
2. In Home Assistant, go to Settings > Devices & Services
3. Click "Add Integration" and search for "WhatWatt"
4. Enter the MQTT topic that your WhatWatt Go device is publishing to
5. Enter the IP address of your WhatWatt Go device (for accessing the configuration page)
6. Optionally, provide a custom name for the device

## Available Entities

For each WhatWatt Go device, the following entities will be created:

### Sensors

- **Power In**: Current power being drawn from the grid (W)
- **Power Out**: Current power being exported to the grid (W)
- **Energy In**: Total energy consumed from the grid (kWh)
- **Energy Out**: Total energy exported to the grid (kWh)
- **Voltage L1**: Voltage level on phase L1 (V)
- **Voltage L2**: Voltage level on phase L2 (V)
- **Voltage L3**: Voltage level on phase L3 (V)

### Buttons

- **Configuration**: Opens the device's configuration page in your web browser

## MQTT Payload Format

The WhatWatt Go device sends data in the following JSON format:

```json
{
  "sys_id": "device-id",
  "meter_id": "meter-id",
  "time": "timestamp",
  "power_in": 1234.5,
  "power_out": 0.0,
  "energy_in": 12345.6,
  "energy_out": 123.4,
  "voltage_l1": 230.1,
  "voltage_l2": 231.2,
  "voltage_l3": 229.8
}
```

## Troubleshooting

### MQTT Connection Issues

- Ensure that the MQTT integration is properly set up in Home Assistant
- Verify that the WhatWatt Go device is correctly configured to publish to the MQTT broker
- Check that the MQTT topic in the integration configuration matches the one configured on the device

### Missing Sensors

- The sensors will appear only after the first MQTT message is received
- Check the Home Assistant logs for any errors related to the WhatWatt integration

### Configuration Button Not Working

- The configuration button opens the device's web interface in your browser
- Ensure that the IP address entered during setup is correct and accessible from your network
- The button may not work if Home Assistant is running in a container or on a system without a GUI

## Support

For issues, feature requests, or questions, please open an issue on the [GitHub repository](https://github.com/vestiacom/whatwatt-home-asistance-integration/issues).
