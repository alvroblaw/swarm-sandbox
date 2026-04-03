"""
test_bitcoin_address.py — Tests de validación de direcciones Bitcoin.
"""

import pytest
from bitcoin_address import normalize_bitcoin_address, is_valid_bitcoin_address, address_type


# ── Direcciones válidas conocidas ──────────────────────────────────────────────

VALID_P2PKH = [
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7Divf Na",  # génesis — se limpia con strip()
    "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
]

VALID_P2PKH_CLEAN = [
    "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
    "1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
    "1CounterpartyXXXXXXXXXXXXXXXUWLpVr",
]

VALID_P2SH = [
    "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
    "3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC",
]

VALID_BECH32 = [
    # Direcciones Bech32 con checksum verificado (BIP-173)
    "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4",  # vector BIP-173
    "bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3",  # P2WSH
]

# ── Direcciones inválidas ──────────────────────────────────────────────────────

INVALID_ADDRESSES = [
    "",                          # vacía
    "   ",                       # solo espacios
    None,                        # None
    123,                         # tipo incorrecto
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",  # Ethereum
    "1InvalidAddress!!!",        # caracteres inválidos
    "bc1wrongchecksum",          # bech32 inválido
    "2BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",  # prefijo inválido
    "LKdYMeAkJsez62bMTwb3BbSB9cCVkNjuZt",  # Litecoin
    "abcdefghijklmnopqrstuvwxyz123456",  # sin prefijo válido
]


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestNormalizeBitcoinAddress:

    def test_strips_whitespace_for_base58_addresses(self):
        assert normalize_bitcoin_address(" 1BoatSLRHtKNngkdXEeobR76b53LETtpyT ") == "1BoatSLRHtKNngkdXEeobR76b53LETtpyT"

    def test_lowercases_bech32_addresses(self):
        assert normalize_bitcoin_address(" BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4 ") == "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"

    def test_rejects_non_string_values(self):
        with pytest.raises(TypeError):
            normalize_bitcoin_address(None)

    def test_rejects_empty_strings(self):
        with pytest.raises(ValueError):
            normalize_bitcoin_address("   ")


class TestValidAddresses:

    def test_p2pkh_valid(self):
        for addr in VALID_P2PKH_CLEAN:
            assert is_valid_bitcoin_address(addr), f"Debería ser válida: {addr}"

    def test_p2sh_valid(self):
        for addr in VALID_P2SH:
            assert is_valid_bitcoin_address(addr), f"Debería ser válida: {addr}"

    def test_bech32_valid(self):
        for addr in VALID_BECH32:
            assert is_valid_bitcoin_address(addr), f"Debería ser válida: {addr}"


class TestInvalidAddresses:

    def test_invalid_addresses(self):
        for addr in INVALID_ADDRESSES:
            assert not is_valid_bitcoin_address(addr), f"Debería ser inválida: {addr}"


class TestAddressType:

    def test_p2pkh_type(self):
        assert address_type("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2") == "P2PKH"

    def test_p2sh_type(self):
        assert address_type("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") == "P2SH"

    def test_bech32_type(self):
        assert address_type("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == "Bech32"

    def test_invalid_type(self):
        assert address_type("notanaddress") == "invalid"
        assert address_type("") == "invalid"
