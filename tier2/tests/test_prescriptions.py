"""Unit tests for medication dosage validation."""

import pytest
from tier2.prescription_service import validate_medication_dosage


def test_validate_dosage_within_limit() -> None:
    """Test valid dosage within drug limit."""
    assert validate_medication_dosage("Amoxicillin", 500.0) is True


def test_validate_dosage_exceeded() -> None:
    """Test dosage exceeding maximum safety threshold."""
    assert validate_medication_dosage("Amoxicillin", 1500.0) is False


def test_validate_dosage_zero_invalid() -> None:
    """Test zero dosage is rejected."""
    assert validate_medication_dosage("Ibuprofen", 0.0) is False
