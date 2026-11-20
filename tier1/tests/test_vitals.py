"""Unit tests for patient vitals and BMI calculator."""

import pytest
from tier1.vitals_service import calculate_bmi, classify_bmi


def test_calculate_bmi_normal() -> None:
    """Test standard normal weight BMI calculation."""
    assert calculate_bmi(70.0, 175.0) == 22.86


def test_classify_bmi_brackets() -> None:
    """Test standard BMI classification categories."""
    assert classify_bmi(18.0) == "Underweight"
    assert classify_bmi(22.0) == "Normal"
    assert classify_bmi(27.0) == "Overweight"
    assert classify_bmi(32.0) == "Obese"
