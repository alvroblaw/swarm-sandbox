# swarm-sandbox

Repositorio sandbox del enjambre Jarvis. Pruebas del ciclo completo: código → test → PR → merge.

## Stack

| Entorno | Tecnología |
|---------|------------|
| Python | Python 3.11, pytest, embit, pillow |
| MicroPython | embit, código para SeedSigner |
| C/C++ | ESP-IDF v5.2, toolchain xtensa |

## Focus

- **Bitcoin** — libraries, utilities, testing
- **SeedSigner** — MicroPython/Python code for the device

## Implemented examples

- `python/bitcoin_address.py` — Bitcoin address validation (P2PKH, P2SH, Bech32)
- `python/bip39_mnemonic.py` — English BIP39 mnemonic generation and checksum validation

## Estructura

```
swarm-sandbox/
├── docker/
│   ├── python/          → Dockerfile entorno Python
│   └── esp32/           → Dockerfile entorno ESP32/MicroPython
├── python/              → código Python + tests
├── micropython/         → código MicroPython para SeedSigner/ESP32
├── c_cpp/               → código C/C++ para ESP32
└── .github/workflows/   → CI/CD
```

## Desarrollo local

```bash
# Entorno Python
cd docker/python && docker compose up -d
docker exec -it swarm-python pytest /workspace/python -v

# Entorno ESP32
cd docker/esp32 && docker build -t swarm-esp32 .
docker run --rm -v $(pwd):/workspace swarm-esp32 bash
```
