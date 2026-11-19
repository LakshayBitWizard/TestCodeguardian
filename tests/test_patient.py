"""
Unit tests for HealthSync Patient Service.
Validates patient registration, record retrieval, and risk scoring.
"""

import pytest
from services.patient_service import PatientService


@pytest.fixture
def patient_service():
    """Create an isolated in-memory PatientService instance for testing."""
    service = PatientService(db_path=":memory:")
    return service


def test_register_and_get_patient(patient_service):
    """Test safe patient registration and lookup using the fixture."""
    reg = patient_service.register_patient("Alice", "Smith", "alice@example.com", "555-0100")
    assert "patient_id" in reg

    fetched = patient_service.get_patient_by_id(reg["patient_id"])
    assert fetched is not None
    assert fetched["first_name"] == "Alice"
    assert fetched["last_name"] == "Smith"


def test_calculate_risk_score(patient_service):
    """Test clinical risk scoring boundaries using the fixture."""
    elderly_risk = patient_service.calculate_patient_risk_score(age=70, has_chronic_condition=True, prior_admissions=2)
    assert elderly_risk >= 65

    young_healthy = patient_service.calculate_patient_risk_score(age=25, has_chronic_condition=False, prior_admissions=0)
    assert young_healthy == 10
