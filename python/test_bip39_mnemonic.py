"""Tests for BIP39 mnemonic generation."""

from __future__ import annotations

from bip39_mnemonic import generate_mnemonic, mnemonic_checksum_bits, validate_mnemonic


def test_generate_12_word_mnemonic() -> None:
    mnemonic = generate_mnemonic(12)
    words = mnemonic.split()

    assert len(words) == 12
    assert validate_mnemonic(mnemonic) is True


def test_generate_24_word_mnemonic() -> None:
    mnemonic = generate_mnemonic(24)
    words = mnemonic.split()

    assert len(words) == 24
    assert validate_mnemonic(mnemonic) is True


def test_generated_mnemonics_are_not_identical_across_small_sample() -> None:
    mnemonics = {generate_mnemonic(12) for _ in range(5)}

    assert len(mnemonics) == 5


def test_invalid_word_count_raises() -> None:
    try:
        generate_mnemonic(18)
    except ValueError as exc:
        assert "12 or 24" in str(exc)
    else:
        raise AssertionError("generate_mnemonic(18) should raise ValueError")


def test_checksum_validation_detects_tampering() -> None:
    mnemonic = generate_mnemonic(12)
    words = mnemonic.split()
    tampered = " ".join(words[:-1] + ["zoo"])

    assert validate_mnemonic(mnemonic) is True
    assert validate_mnemonic(tampered) is False


def test_checksum_bits_length_matches_bip39_rule() -> None:
    mnemonic_12 = generate_mnemonic(12)
    mnemonic_24 = generate_mnemonic(24)

    assert len(mnemonic_checksum_bits(mnemonic_12)) == 4
    assert len(mnemonic_checksum_bits(mnemonic_24)) == 8
