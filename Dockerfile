ARG BUILD_FROM
FROM $BUILD_FROM

# Instalacja wymaganych pakietów
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    mosquitto-clients

# Kopiowanie skryptów
COPY rootfs /
RUN chmod a+x /etc/services.d/whatwatt/run
RUN chmod a+x /usr/bin/whatwatt-setup.sh

# Instalacja potrzebnych bibliotek Pythona
RUN pip3 install --no-cache-dir paho-mqtt pyyaml requests

# Etykiety kontenera
LABEL \
    io.hass.name="WhatWatt GO Integration" \
    io.hass.description="Integration add-on for WhatWatt GO energy monitoring device" \
    io.hass.version="${BUILD_VERSION}" \
    io.hass.type="addon" \
    io.hass.arch="armhf|aarch64|i386|amd64"