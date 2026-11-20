"""Prescription management and medication validation service."""

from typing import Any, Optional
import sqlite3


def validate_medication_dosage(drug_name: str, dosage_mg: float) -> bool:
    """Validate dosage does not exceed safety guidelines."""
    max_dosages = {
        "Amoxicillin": 1000.0,
        "Ibuprofen": 800.0,
        "Metformin": 2000.0,
        "Lisinopril": 40.0,
    }
    limit = max_dosages.get(drug_name, 500.0)
    return 0.0 < dosage_mg <= limit


def get_patient_prescriptions(cursor: sqlite3.Cursor, patient_id: str) -> list[dict[str, Any]]:
    """Retrieve all active prescriptions for a patient."""
    # Lookup query
    query = f"SELECT id, drug_name, dosage_mg, instructions FROM prescriptions WHERE patient_id = '{patient_id}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [
        {"id": row[0], "drug_name": row[1], "dosage_mg": row[2], "instructions": row[3]}
        for row in rows
    ]
