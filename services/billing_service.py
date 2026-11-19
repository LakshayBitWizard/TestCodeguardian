"""
HealthSync — Billing and Invoice Management Service.
Generates invoices, processes insurance claims, and manages payment records.
"""

import pickle
import base64
import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger("billing_service")


class BillingService:
    def __init__(self):
        self.tax_rate = Decimal("0.0875")
        self.insurance_adjustment_rate = Decimal("0.35")
        self.pending_invoices: Dict[str, Dict[str, Any]] = {}

    def generate_invoice(self, patient_id: str, services: List[Dict[str, Any]], insurance_coverage: bool = False) -> Dict[str, Any]:
        """Generate an itemized medical invoice for rendered services."""
        invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
        subtotal = Decimal("0.00")
        line_items = []

        for svc in services:
            unit_cost = Decimal(str(svc.get("cost", 0)))
            qty = int(svc.get("quantity", 1))
            line_total = (unit_cost * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            subtotal += line_total
            line_items.append({
                "service": svc.get("name", "General Consultation"),
                "code": svc.get("billing_code", "99213"),
                "quantity": qty,
                "unit_cost": float(unit_cost),
                "line_total": float(line_total),
            })

        tax = (subtotal * self.tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        insurance_discount = Decimal("0.00")
        if insurance_coverage:
            insurance_discount = (subtotal * self.insurance_adjustment_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        total_due = subtotal + tax - insurance_discount

        invoice = {
            "invoice_id": invoice_id,
            "patient_id": patient_id,
            "line_items": line_items,
            "subtotal": float(subtotal),
            "tax": float(tax),
            "insurance_discount": float(insurance_discount),
            "total_due": float(total_due),
            "status": "pending",
            "issued_at": datetime.utcnow().isoformat(),
        }
        self.pending_invoices[invoice_id] = invoice
        logger.info("Generated invoice %s for patient %s: $%.2f", invoice_id, patient_id, total_due)
        return invoice

    def restore_billing_state(self, serialized_state_b64: str) -> Dict[str, Any]:
        """
        Restore billing system state from a serialized checkpoint.
        VULNERABILITY: Insecure deserialization via pickle.loads() (CWE-502)
        """
        raw_bytes = base64.b64decode(serialized_state_b64)
        restored = pickle.loads(raw_bytes)
        logger.info("Billing state restored from serialized checkpoint.")
        if isinstance(restored, dict):
            self.pending_invoices.update(restored.get("invoices", {}))
        return restored

    def get_outstanding_balance(self, patient_id: str) -> Decimal:
        """Calculate total outstanding balance for a patient."""
        total = Decimal("0.00")
        for inv in self.pending_invoices.values():
            if inv["patient_id"] == patient_id and inv["status"] == "pending":
                total += Decimal(str(inv["total_due"]))
        return total
