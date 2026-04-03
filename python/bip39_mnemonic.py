"""BIP39 mnemonic generation helpers.

This module generates 12-word and 24-word BIP39 mnemonics using
cryptographically secure entropy from Python's ``secrets`` module.

It relies on ``embit`` for the official English wordlist and checksum-aware
mnemonic handling.
"""

from __future__ import annotations

import hashlib
import secrets
from typing import Final

from embit import bip39

_ALLOWED_WORD_COUNTS: Final[set[int]] = {12, 24}
_ENTROPY_BITS_BY_WORD_COUNT: Final[dict[int, int]] = {
    12: 128,
    24: 256,
}


def _entropy_to_mnemonic(entropy: bytes) -> str:
    """Convert raw entropy to an English BIP39 mnemonic.

    Args:
        entropy: Raw entropy bytes. Supported sizes are 16 bytes (128 bits)
            and 32 bytes (256 bits).

    Returns:
        A space-separated English BIP39 mnemonic.
    """
    if len(entropy) not in (16, 32):
        raise ValueError("entropy must be 16 bytes (12 words) or 32 bytes (24 words)")
    return bip39.mnemonic_from_bytes(entropy)


def generate_mnemonic(word_count: int = 12) -> str:
    """Generate a new English BIP39 mnemonic.

    Args:
        word_count: Number of words to generate. Supported values are 12 and 24.

    Returns:
        A valid English BIP39 mnemonic.
    """
    if word_count not in _ALLOWED_WORD_COUNTS:
        raise ValueError("word_count must be 12 or 24")

    entropy_bits = _ENTROPY_BITS_BY_WORD_COUNT[word_count]
    entropy = secrets.token_bytes(entropy_bits // 8)
    return _entropy_to_mnemonic(entropy)


def validate_mnemonic(mnemonic: str) -> bool:
    """Validate a BIP39 mnemonic and its checksum.

    Args:
        mnemonic: Space-separated mnemonic phrase.

    Returns:
        ``True`` if the mnemonic is a valid English BIP39 phrase with a valid
        checksum, otherwise ``False``.
    """
    if not isinstance(mnemonic, str):
        return False

    phrase = " ".join(mnemonic.strip().split())
    if not phrase:
        return False

    try:
        bip39.mnemonic_to_bytes(phrase, ignore_checksum=False)
        return True
    except Exception:
        return False


def mnemonic_checksum_bits(mnemonic: str) -> str:
    """Return the checksum bits encoded in a valid mnemonic.

    Args:
        mnemonic: Space-separated mnemonic phrase.

    Returns:
        The checksum bits as a binary string.
    """
    phrase = " ".join(mnemonic.strip().split())
    if not validate_mnemonic(phrase):
        raise ValueError("invalid BIP39 mnemonic")

    words = phrase.split()
    entropy = bip39.mnemonic_to_bytes(phrase, ignore_checksum=False)
    checksum_length = len(words) // 3
    digest = hashlib.sha256(entropy).digest()
    checksum_byte = digest[0]
    return format(checksum_byte, "08b")[:checksum_length]
