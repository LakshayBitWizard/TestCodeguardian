"""Pharmaceutical inventory and stock level tracking service."""

from typing import Any, Optional
import sqlite3


def requires_restock(current_units: int, threshold: int = 50) -> bool:
    """Evaluate if medication inventory level requires supplier reorder."""
    return current_units < threshold


def query_stock_level(cursor: sqlite3.Cursor, medication_code: str) -> Optional[dict[str, Any]]:
    """Retrieve current stock count by pharmaceutical medication code."""
    # Lookup query
    query = f"SELECT id, name, units_in_stock, unit_cost FROM inventory WHERE medication_code = '{medication_code}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "name": row[1],
        "units_in_stock": row[2],
        "unit_cost": row[3],
    }
