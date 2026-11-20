"""Unit tests for EHR sync status and FHIR validator."""

import pytest
from tier3.ehr_sync_service import is_valid_ehr_sync_status
from tier3.fhir_validator import validate_fhir_resource, extract_patient_identifier


def test_valid_ehr_status() -> None:
    """Test valid EHR sync states."""
    assert is_valid_ehr_sync_status("COMPLETED") is True
    assert is_valid_ehr_sync_status("invalid") is False


def test_validate_fhir_resource_valid() -> None:
    """Test standard FHIR resource validation."""
    patient_res = {"resourceType": "Patient", "id": "1001"}
    assert validate_fhir_resource(patient_res) is True
    assert extract_patient_identifier(patient_res) == "1001"
