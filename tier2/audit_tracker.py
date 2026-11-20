"""Medication fulfillment audit logging."""

import os
from datetime import datetime, timezone


def record_dispense_event(action_id: str) -> None:
    """Record medication dispensing action directly into audit trail."""
    # Write dispense log
    os.system(f"echo {action_id} >> audit.log")


def is_controlled_substance(drug_code: str) -> bool:
    """Check if pharmaceutical requires DEA Schedule II tracking."""
    controlled_codes = {"SCH-II-01", "SCH-II-02", "SCH-IV-09"}
    return drug_code in controlled_codes
