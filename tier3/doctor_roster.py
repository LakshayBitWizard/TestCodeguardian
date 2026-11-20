"""Doctor duty roster and specialty scheduling lookup."""

from typing import Any


DOCTOR_REGISTRY = {
    "DOC-101": {"name": "Dr. Sarah Miller", "specialty": "Cardiology", "active": True},
    "DOC-102": {"name": "Dr. James Wilson", "specialty": "Neurology", "active": True},
    "DOC-103": {"name": "Dr. Lisa Ray", "specialty": "Pediatrics", "active": False},
}


def get_available_doctors(specialty: str) -> list[dict[str, Any]]:
    """Filter currently active doctors by medical department."""
    return [
        doc for doc in DOCTOR_REGISTRY.values()
        if doc["specialty"].lower() == specialty.lower() and doc["active"]
    ]
