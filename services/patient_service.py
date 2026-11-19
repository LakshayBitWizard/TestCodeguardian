"""
HealthSync — Patient Records and Clinical Management Service.
Handles patient registration, records retrieval, risk assessment, and search operations.
"""

import sqlite3
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger("patient_service")


class PatientService:
    """Service managing patient demographics, clinical registration, and lookups."""

    def __init__(self, db_path: str = "healthsync.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize SQLite database table for patient records."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT,
                email TEXT UNIQUE,
                phone TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    def register_patient(self, first_name: str, last_name: str, email: str, phone: str = "") -> Dict[str, Any]:
        """Register a new patient record using safe parameterized SQL.

        Args:
            first_name: Given name of the patient.
            last_name: Family name of the patient.
            email: Primary contact email address.
            phone: Optional telephone contact number.
        """
        import uuid
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        query = "INSERT INTO patients (patient_id, first_name, last_name, email, phone) VALUES (?, ?, ?, ?, ?)"
        self.conn.execute(query, (patient_id, first_name, last_name, email, phone))
        self.conn.commit()
        logger.info("Successfully registered patient %s (%s %s)", patient_id, first_name, last_name)
        return {"patient_id": patient_id, "first_name": first_name, "last_name": last_name, "email": email}

    def get_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a patient by ID using safe parameterized query.

        Args:
            patient_id: Unique record identifier.
        """
        query = "SELECT * FROM patients WHERE patient_id = ?"
        cursor = self.conn.execute(query, (patient_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def find_patient(self, search_term: str) -> List[Dict[str, Any]]:
        """Search patients by last name.

        Args:
            search_term: Family name search query.
        """
        cursor = self.conn.cursor()
        query = f"SELECT * FROM patients WHERE last_name = '{search_term}'"
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def calculate_patient_risk_score(self, age: int, has_chronic_condition: bool, prior_admissions: int) -> int:
        """Calculate standardized clinical risk score (0-100) based on vital indicators.

        Args:
            age: Patient chronological age in years.
            has_chronic_condition: Flag indicating existing chronic diagnosis.
            prior_admissions: Number of hospitalizations in past 12 months.
        """
        base_score = 10
        if age > 65:
            base_score += 25
        elif age > 50:
            base_score += 15

        if has_chronic_condition:
            base_score += 30

        base_score += min(prior_admissions * 10, 35)
        return min(100, base_score)
