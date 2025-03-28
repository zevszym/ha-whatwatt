#!/bin/bash
# Installation script for WhatWatt Home Assistant integration

# Default Home Assistant config directory
DEFAULT_HA_CONFIG_DIR="$HOME/.homeassistant"

# Function to display usage information
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -d, --dir DIR    Home Assistant config directory (default: $DEFAULT_HA_CONFIG_DIR)"
    echo "  -h, --help       Display this help message"
    exit 1
}

# Parse command line arguments
HA_CONFIG_DIR="$DEFAULT_HA_CONFIG_DIR"

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -d|--dir)
            HA_CONFIG_DIR="$2"
            shift
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if the Home Assistant config directory exists
if [ ! -d "$HA_CONFIG_DIR" ]; then
    echo "Error: Home Assistant config directory not found at $HA_CONFIG_DIR"
    echo "Please specify the correct directory using the -d or --dir option."
    exit 1
fi

# Create the custom_components directory if it doesn't exist
CUSTOM_COMPONENTS_DIR="$HA_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Create the whatwatt directory if it doesn't exist
WHATWATT_DIR="$CUSTOM_COMPONENTS_DIR/whatwatt"
if [ ! -d "$WHATWATT_DIR" ]; then
    echo "Creating whatwatt directory..."
    mkdir -p "$WHATWATT_DIR"
    mkdir -p "$WHATWATT_DIR/translations"
else
    echo "Removing existing whatwatt directory..."
    rm -rf "$WHATWATT_DIR"
    mkdir -p "$WHATWATT_DIR"
    mkdir -p "$WHATWATT_DIR/translations"
fi

# Copy the integration files
echo "Copying integration files..."
cp -v custom_components/whatwatt/*.py "$WHATWATT_DIR/"
cp -v custom_components/whatwatt/*.json "$WHATWATT_DIR/"
cp -v custom_components/whatwatt/translations/*.json "$WHATWATT_DIR/translations/"

# Set permissions
echo "Setting permissions..."
chmod -R 755 "$WHATWATT_DIR"

echo "Installation complete!"
echo "Please restart Home Assistant to load the integration."
echo "After restarting, you can add the integration from the Home Assistant UI:"
echo "Settings > Devices & Services > Add Integration > WhatWatt"
