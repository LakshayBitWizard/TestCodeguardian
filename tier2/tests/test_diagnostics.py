"""Unit tests for laboratory diagnostic reference ranges."""

import pytest
from tier2.diagnostic_service import is_result_in_reference_range


def test_glucose_normal() -> None:
    """Test normal fasting glucose reference range."""
    assert is_result_in_reference_range("Fasting Glucose", 85.0) is True


def test_glucose_elevated() -> None:
    """Test elevated fasting glucose out of range."""
    assert is_result_in_reference_range("Fasting Glucose", 130.0) is False


def test_unknown_test_defaults_true() -> None:
    """Test unspecified test defaults to safe pass."""
    assert is_result_in_reference_range("Unknown Panel", 50.0) is True
