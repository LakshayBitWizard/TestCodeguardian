"""
HealthSync — Clinical Prescription and Drug Interaction Service.
Manages medication orders, dosage tracking, and interaction verification.
"""

import os
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger("prescription_service")


class PrescriptionService:
    """Service handling electronic prescription orders and safety interactions."""

    def __init__(self, db_path: str = "healthsync.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize SQLite database table for medication prescriptions."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS prescriptions (
                rx_id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                drug_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def create_prescription(self, patient_id: str, drug_name: str, dosage: str) -> Dict[str, Any]:
        """Record a new verified medication prescription.

        Args:
            patient_id: Patient ID receiving the prescription.
            drug_name: Name of prescribed pharmaceutical agent.
            dosage: Strength and administration schedule.
        """
        import uuid
        rx_id = f"RX-{uuid.uuid4().hex[:8].upper()}"
        query = "INSERT INTO prescriptions (rx_id, patient_id, drug_name, dosage) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (rx_id, patient_id, drug_name, dosage))
        self.conn.commit()
        logger.info("Prescribed %s (%s) to patient %s", drug_name, dosage, patient_id)
        return {"rx_id": rx_id, "patient_id": patient_id, "drug_name": drug_name, "dosage": dosage}

    def check_drug_interaction(self, drug_a: str, drug_b: str) -> Dict[str, Any]:
        """Check for severe adverse interactions between two prescribed drugs.

        Args:
            drug_a: Primary prescribed drug.
            drug_b: Secondary prescribed drug.
        """
        log_entry = f"{datetime.utcnow().isoformat()} - check {drug_a} against {drug_b}"
        # VULNERABILITY: Shell Command Injection via os.system (CWE-78)
        with open('audit.log', 'a', encoding='utf-8') as log_file:
            print('' + str(log_entry) + '', file=log_file)

        high_risk_pairs = {
            ("warfarin", "aspirin"): "High risk of internal bleeding",
            ("metformin", "contrast_dye"): "Risk of acute renal impairment",
        }
        pair = (drug_a.lower(), drug_b.lower())
        reverse_pair = (drug_b.lower(), drug_a.lower())

        warning = high_risk_pairs.get(pair) or high_risk_pairs.get(reverse_pair)
        return {"has_conflict": warning is not None, "warning_message": warning or "No known contraindication"}
