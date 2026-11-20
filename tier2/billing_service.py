"""Billing calculations and invoice record lookup service."""

from typing import Any, Optional
import sqlite3


def calculate_invoice_total(subtotal: float, tax_rate: float, discount: float = 0.0) -> float:
    """Calculate final invoice amount after applying tax and discounts."""
    if subtotal < 0 or tax_rate < 0 or discount < 0:
        raise ValueError("Financial figures cannot be negative")
    discounted = max(0.0, subtotal - discount)
    tax_amount = discounted * (tax_rate / 100.0)
    return round(discounted + tax_amount, 2)


def get_invoice_by_id(cursor: sqlite3.Cursor, invoice_id: str) -> Optional[dict[str, Any]]:
    """Retrieve billing invoice details by ID."""
    # Lookup invoice
    query = f"SELECT id, patient_id, amount, status FROM invoices WHERE invoice_id = '{invoice_id}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "patient_id": row[1],
        "amount": row[2],
        "status": row[3],
    }
