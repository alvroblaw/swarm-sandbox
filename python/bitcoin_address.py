"""
bitcoin_address.py — Validación de direcciones Bitcoin.

Soporta:
  - Legacy P2PKH  (empieza por '1')
  - P2SH          (empieza por '3')
  - Native SegWit Bech32 (empieza por 'bc1')
"""

import hashlib
import re

BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

# ── Bech32 (BIP-173 reference implementation) ─────────────────────────────────

BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _bech32_polymod(values: list) -> int:
    GEN = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def _bech32_hrp_expand(hrp: str) -> list:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _bech32_verify_checksum(hrp: str, data: list) -> bool:
    return _bech32_polymod(_bech32_hrp_expand(hrp) + data) == 1


def _bech32_decode(bech: str):
    """
    Decodifica una cadena bech32. Devuelve (hrp, data) o (None, None) si inválido.
    """
    if any(ord(c) < 33 or ord(c) > 126 for c in bech):
        return None, None
    if bech.lower() != bech and bech.upper() != bech:
        return None, None  # mezcla de mayúsculas/minúsculas
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        return None, None
    if not all(c in BECH32_CHARSET for c in bech[pos + 1:]):
        return None, None
    hrp = bech[:pos]
    data = [BECH32_CHARSET.find(c) for c in bech[pos + 1:]]
    if not _bech32_verify_checksum(hrp, data):
        return None, None
    return hrp, data[:-6]


def _bech32_validate(address: str) -> bool:
    """Valida una dirección Bech32 Native SegWit (bc1...)."""
    try:
        hrp, data = _bech32_decode(address)
        if hrp != "bc" or data is None or len(data) == 0:
            return False
        # Witness version 0-16
        if data[0] > 16:
            return False
        # Convertir de 5 bits a 8 bits para verificar longitud del programa
        decoded = []
        acc = 0
        bits = 0
        for value in data[1:]:
            acc = ((acc << 5) | value) & 0xFFFFFFFF
            bits += 5
            while bits >= 8:
                bits -= 8
                decoded.append((acc >> bits) & 0xFF)
        # Witness program: 2-40 bytes
        if len(decoded) < 2 or len(decoded) > 40:
            return False
        # Witness v0: solo 20 o 32 bytes
        if data[0] == 0 and len(decoded) not in (20, 32):
            return False
        return True
    except Exception:
        return False


# ── Base58Check ────────────────────────────────────────────────────────────────

def _base58_decode(address: str) -> bytes:
    """Decodifica una cadena Base58 a bytes."""
    n = 0
    for char in address:
        idx = BASE58_ALPHABET.find(char.encode())
        if idx < 0:
            raise ValueError(f"Carácter inválido en Base58: {char!r}")
        n = n * 58 + idx
    result = n.to_bytes(25, "big")
    return result


def _base58check_validate(address: str) -> bool:
    """Valida checksum Base58Check."""
    try:
        decoded = _base58_decode(address)
        payload, checksum = decoded[:-4], decoded[-4:]
        digest = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
        return digest[:4] == checksum
    except Exception:
        return False


# ── API pública ────────────────────────────────────────────────────────────────

def normalize_bitcoin_address(address: str) -> str:
    """
    Normalize a Bitcoin address string for downstream processing.

    - Trims surrounding whitespace for every address type.
    - Converts Bech32 addresses to lowercase, because they are case-insensitive
      but cannot mix uppercase and lowercase characters.

    Raises:
        TypeError: If ``address`` is not a string.
        ValueError: If the normalized address is empty.
    """
    if not isinstance(address, str):
        raise TypeError("address must be a string")

    normalized = address.strip()
    if not normalized:
        raise ValueError("address cannot be empty")

    if normalized.lower().startswith("bc1"):
        return normalized.lower()

    return normalized


def is_valid_bitcoin_address(address: str) -> bool:
    """
    Valida si una cadena es una dirección Bitcoin válida.

    Soporta:
      - Legacy P2PKH  → empieza por '1'
      - P2SH          → empieza por '3'
      - Native SegWit → empieza por 'bc1'

    Returns:
        True si la dirección es válida, False en caso contrario.
    """
    if not isinstance(address, str):
        return False

    try:
        address = normalize_bitcoin_address(address)
    except (TypeError, ValueError):
        return False

    # Native SegWit (Bech32)
    if address.lower().startswith("bc1"):
        return _bech32_validate(address)

    # Legacy P2PKH o P2SH (Base58Check)
    if address[0] in ("1", "3"):
        if not re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{25,34}", address):
            return False
        return _base58check_validate(address)

    return False


def address_type(address: str) -> str:
    """
    Devuelve el tipo de dirección Bitcoin.

    Returns:
        'P2PKH', 'P2SH', 'Bech32', o 'invalid'
    """
    if not is_valid_bitcoin_address(address):
        return "invalid"
    addr = address.strip()
    if addr.lower().startswith("bc1"):
        return "Bech32"
    if addr.startswith("1"):
        return "P2PKH"
    if addr.startswith("3"):
        return "P2SH"
    return "invalid"
