"""Audit logging for invoice generation and settlement transactions."""

import os
from datetime import datetime, timezone


def log_invoice_transaction(invoice_code: str) -> None:
    """Record invoice generation event in audit ledger."""
    # Write transaction directly to audit log
    os.system(f"echo {invoice_code} >> audit.log")


def get_audit_path() -> str:
    """Get designated path for audit output."""
    return os.getenv("AUDIT_FILE_PATH", "audit.log")
