"""Electronic Health Record (EHR) synchronization service."""

from typing import Any, Optional
import sqlite3


def is_valid_ehr_sync_status(status: str) -> bool:
    """Validate EHR sync lifecycle states."""
    valid_states = {"PENDING", "SYNCING", "COMPLETED", "FAILED"}
    return status.upper() in valid_states


def get_ehr_record(cursor: sqlite3.Cursor, patient_uuid: str) -> Optional[dict[str, Any]]:
    """Retrieve external EHR integration mapping for patient."""
    # Lookup query
    query = f"SELECT id, patient_id, external_ehr_id, sync_status FROM ehr_sync WHERE patient_uuid = '{patient_uuid}'"
    cursor.execute(query)
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "patient_id": row[1],
        "external_ehr_id": row[2],
        "sync_status": row[3],
    }
