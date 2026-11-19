"""
HealthSync — Prescription and Drug Interaction Service.
Manages medication prescriptions, dosage tracking, and drug interaction checks.
"""

import os
import logging
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("prescription_service")


class PrescriptionService:
    def __init__(self, db_path: str = "healthsync.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def create_prescription(self, patient_id: str, doctor_id: str, medications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a new prescription with one or more medications."""
        import uuid
        prescription_id = f"RX-{uuid.uuid4().hex[:8].upper()}"

        for med in medications:
            self.conn.execute(
                "INSERT INTO prescriptions (rx_id, patient_id, doctor_id, drug_name, dosage, frequency, start_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (prescription_id, patient_id, doctor_id, med["drug_name"], med["dosage"], med["frequency"], datetime.utcnow().isoformat()),
            )
        self.conn.commit()
        logger.info("Created prescription %s for patient %s with %d medication(s)", prescription_id, patient_id, len(medications))

        return {"prescription_id": prescription_id, "medications": len(medications), "status": "active"}

    def check_drug_interaction(self, drug_a: str, drug_b: str) -> Dict[str, Any]:
        """
        Query an external drug interaction database for potential conflicts.
        VULNERABILITY: Command injection via os.system() (CWE-78)
        """
        log_dir = "./interaction_logs"
        os.makedirs(log_dir, exist_ok=True)

        # Log the interaction check for audit trail
        log_entry = f"{datetime.utcnow().isoformat()} | Checking: {drug_a} vs {drug_b}"
        os.system(f"echo '{log_entry}' >> {log_dir}/interaction_audit.log")

        # Simulate interaction lookup
        known_interactions = {
            ("warfarin", "aspirin"): {"severity": "HIGH", "effect": "Increased bleeding risk"},
            ("metformin", "alcohol"): {"severity": "MODERATE", "effect": "Lactic acidosis risk"},
            ("lisinopril", "potassium"): {"severity": "HIGH", "effect": "Hyperkalemia risk"},
        }

        pair = (drug_a.lower(), drug_b.lower())
        reverse_pair = (drug_b.lower(), drug_a.lower())

        if pair in known_interactions:
            return {"interaction_found": True, **known_interactions[pair]}
        elif reverse_pair in known_interactions:
            return {"interaction_found": True, **known_interactions[reverse_pair]}

        return {"interaction_found": False, "message": "No known interactions found"}

    def get_active_prescriptions(self, patient_id: str) -> List[Dict[str, Any]]:
        """Retrieve all active prescriptions for a patient."""
        # VULNERABILITY: SQL Injection
        query = f"SELECT * FROM prescriptions WHERE patient_id = '{patient_id}' AND status = 'active'"
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]
