FROM espressif/idf:v5.2.1

LABEL maintainer="Jarvis Swarm <alvroblaw@users.noreply.github.com>"
LABEL description="Entorno ESP32: ESP-IDF + MicroPython + toolchain C/C++"

RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3-pip \
    python3-serial \
    && rm -rf /var/lib/apt/lists/*

# Herramientas MicroPython / ESP32
RUN pip3 install --no-cache-dir \
    esptool \
    mpremote \
    adafruit-ampy

WORKDIR /workspace

CMD ["bash"]
