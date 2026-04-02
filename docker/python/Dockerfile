FROM python:3.11-slim

LABEL maintainer="Jarvis Swarm <alvroblaw@users.noreply.github.com>"
LABEL description="Entorno Python para proyectos Bitcoin/SeedSigner"

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Herramientas de desarrollo
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    embit \
    pillow \
    qrcode

COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["bash"]
