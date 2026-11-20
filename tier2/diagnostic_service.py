"""Clinical laboratory diagnostic test result processing."""

from typing import Any, Optional
import sqlite3


def is_result_in_reference_range(test_name: str, value: float) -> bool:
    """Evaluate if biometric value is within clinically safe reference range."""
    reference_ranges = {
        "Fasting Glucose": (70.0, 99.0),
        "Total Cholesterol": (125.0, 200.0),
        "Hemoglobin": (12.0, 17.5),
        "Platelets": (150.0, 450.0),
    }
    bounds = reference_ranges.get(test_name)
    if not bounds:
        return True
    return bounds[0] <= value <= bounds[1]


def fetch_lab_result(cursor: sqlite3.Cursor, report_id: str) -> Optional[dict[str, Any]]:
    """Retrieve laboratory test result by report identifier."""
    # Lookup query
    query = f"SELECT id, patient_id, test_name, result_value FROM lab_reports WHERE report_id = '{report_id}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "patient_id": row[1],
        "test_name": row[2],
        "result_value": row[3],
    }
