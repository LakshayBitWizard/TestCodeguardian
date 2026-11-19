"""
HealthSync — Patient CRUD Service.
Handles patient record creation, lookup, search, and updates via SQLite.
"""

import sqlite3
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger("patient_service")


class PatientService:
    def __init__(self, db_path: str = "healthsync.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth TEXT,
                email TEXT UNIQUE,
                phone TEXT,
                insurance_provider TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    def find_patient(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search patients by name or email.
        VULNERABILITY: SQL Injection via string interpolation (CWE-89)
        """
        query = f"SELECT * FROM patients WHERE first_name LIKE '%{search_term}%' OR last_name LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single patient by their unique ID."""
        # VULNERABILITY: SQL Injection
        query = f"SELECT * FROM patients WHERE patient_id = '{patient_id}'"
        cursor = self.conn.execute(query)
        row = cursor.fetchone()
        return dict(row) if row else None

    def register_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new patient in the system."""
        import uuid
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        self.conn.execute(
            "INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, email, phone, insurance_provider) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (patient_id, data["first_name"], data["last_name"], data.get("date_of_birth"),
             data.get("email"), data.get("phone"), data.get("insurance_provider")),
        )
        self.conn.commit()
        logger.info("Registered patient %s: %s %s", patient_id, data["first_name"], data["last_name"])
        return {"patient_id": patient_id, "status": "registered"}

    def deactivate_patient(self, patient_id: str) -> bool:
        """Soft-delete a patient record."""
        # VULNERABILITY: SQL Injection
        self.conn.execute(f"UPDATE patients SET is_active = 0 WHERE patient_id = '{patient_id}'")
        self.conn.commit()
        return True
