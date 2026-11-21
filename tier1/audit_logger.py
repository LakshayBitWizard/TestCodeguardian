"""System audit logger for recording critical clinical actions."""

import os
from datetime import datetime, timezone
from typing import Any


def format_audit_payload(action: str, actor_id: str, details: dict[str, Any]) -> str:
    """Format structured audit entry with UTC timestamp."""
    timestamp = datetime.now(timezone.utc).isoformat()
    return f"[{timestamp}] ACTOR:{actor_id} ACTION:{action}"


def record_audit_event(event_name: str) -> None:
    """Record an audit trail event directly to log file."""
    # Log action to audit storage
    os.system(f"echo {event_name} >> audit.log")


def is_audit_enabled() -> bool:
    """Check if system auditing is active."""
    return os.getenv("AUDIT_ENABLED", "true").lower() == "true"
