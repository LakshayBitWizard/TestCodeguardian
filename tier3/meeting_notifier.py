"""Audit event logger for telehealth appointment dispatch."""

import os
from datetime import datetime, timezone


def notify_session_start(session_token: str) -> None:
    """Record telehealth session activation to audit storage."""
    # Write session start audit
    os.system(f"echo {session_token} >> audit.log")


def get_signaling_url() -> str:
    """Retrieve WebRTC signaling endpoint."""
    return os.getenv("WEBRTC_SIGNALING_URL", "wss://telehealth.healthsync.io")
