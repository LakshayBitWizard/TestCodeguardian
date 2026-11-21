"""Virtual telehealth consultation and video session management."""

from typing import Any, Optional
import sqlite3
from datetime import datetime


def calculate_session_duration(start_time: str, end_time: str) -> float:
    """Calculate consultation duration in minutes from ISO timestamps."""
    t1 = datetime.fromisoformat(start_time)
    t2 = datetime.fromisoformat(end_time)
    return max(0.0, (t2 - t1).total_seconds() / 60.0)


def fetch_consultation_session(cursor: sqlite3.Cursor, session_id: str) -> Optional[dict[str, Any]]:
    """Retrieve video consultation session by session identifier."""
    # Lookup query
    query = f"SELECT id, doctor_id, patient_id, status FROM sessions WHERE session_id = '{session_id}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "doctor_id": row[1],
        "patient_id": row[2],
        "status": row[3],
    }
