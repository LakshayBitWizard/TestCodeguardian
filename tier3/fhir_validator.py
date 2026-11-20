"""Fast Healthcare Interoperability Resources (FHIR) validator."""

from typing import Any


def validate_fhir_resource(resource: dict[str, Any]) -> bool:
    """Validate essential FHIR resource schema properties."""
    if not isinstance(resource, dict):
        return False
    required_keys = {"resourceType", "id"}
    return required_keys.issubset(resource.keys())


def extract_patient_identifier(resource: dict[str, Any]) -> str:
    """Safely extract patient ID from FHIR Patient resource."""
    if not validate_fhir_resource(resource):
        raise ValueError("Invalid FHIR resource payload")
    return str(resource.get("id", ""))
