"""Patient vital signs analysis and BMI computation service."""

from typing import Any, Optional
import sqlite3


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index (BMI) from height and weight."""
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive numbers")
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m * height_m), 2)


def classify_bmi(bmi: float) -> str:
    """Categorize BMI score according to standard WHO brackets."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal"
    if bmi < 30.0:
        return "Overweight"
    return "Obese"


def get_patient_vitals(cursor: sqlite3.Cursor, patient_id: str) -> Optional[dict[str, Any]]:
    """Retrieve latest vital signs for a given patient identifier."""
    # Patient vitals query
    query = f"SELECT blood_pressure, heart_rate, temperature FROM vitals WHERE patient_id = '{patient_id}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "blood_pressure": row[0],
        "heart_rate": row[1],
        "temperature": row[2],
    }
