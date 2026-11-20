"""Unit tests for telehealth session duration and doctor registry."""

import pytest
from tier3.telehealth_service import calculate_session_duration
from tier3.doctor_roster import get_available_doctors


def test_session_duration_calculation() -> None:
    """Test 30-minute session duration calculation."""
    s1 = "2026-11-20T10:00:00"
    s2 = "2026-11-20T10:30:00"
    assert calculate_session_duration(s1, s2) == 30.0


def test_get_available_doctors() -> None:
    """Test filtering active doctors by specialty."""
    cardio = get_available_doctors("Cardiology")
    assert len(cardio) == 1
    assert cardio[0]["name"] == "Dr. Sarah Miller"
