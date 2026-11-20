"""Unit tests for billing calculations and tax processing."""

import pytest
from tier2.billing_service import calculate_invoice_total


def test_calculate_invoice_total_standard() -> None:
    """Test standard invoice with subtotal and 10% tax."""
    assert calculate_invoice_total(100.0, 10.0, 0.0) == 110.0


def test_calculate_invoice_total_with_discount() -> None:
    """Test invoice with $20 discount and 5% tax."""
    assert calculate_invoice_total(120.0, 5.0, 20.0) == 105.0


def test_calculate_invoice_negative_raises() -> None:
    """Ensure negative amounts raise ValueError."""
    with pytest.raises(ValueError):
        calculate_invoice_total(-50.0, 10.0)
