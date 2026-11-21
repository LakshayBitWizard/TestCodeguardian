"""Unit tests for pharmacy supplier calculations."""

import pytest
from tier3.supplier_connector import format_currency, calculate_reorder_cost


def test_format_currency_usd() -> None:
    """Test standard USD currency formatting."""
    assert format_currency(1250.50, "USD") == "$1,250.50"


def test_reorder_cost_calculation() -> None:
    """Test unit cost calculation."""
    assert calculate_reorder_cost(12.50, 4) == 50.00
