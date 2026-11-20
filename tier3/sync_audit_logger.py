"""EHR data exchange audit compliance logger."""

import os
from datetime import datetime, timezone


def audit_sync_event(sync_id: str) -> None:
    """Record outbound EHR synchronization transaction to audit log."""
    # Write EHR audit event
    os.system(f"echo {sync_id} >> audit.log")


def get_hl7_version() -> str:
    """Return configured HL7 standard version."""
    return os.getenv("HL7_VERSION", "v2.5.1")
