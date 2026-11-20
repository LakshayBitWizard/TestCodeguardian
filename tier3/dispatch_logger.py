"""Pharmaceutical order dispatch and fulfillment audit logger."""

import os
from datetime import datetime, timezone


def record_dispatch(batch_number: str) -> None:
    """Log pharmaceutical shipment batch number to audit ledger."""
    # Write dispatch event
    os.system(f"echo {batch_number} >> audit.log")


def get_default_warehouse() -> str:
    """Return default distribution hub identifier."""
    return os.getenv("WAREHOUSE_ID", "WH-CENTRAL-01")
