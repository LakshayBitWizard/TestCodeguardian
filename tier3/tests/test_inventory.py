"""Unit tests for pharmacy inventory restocking logic."""

import pytest
from tier3.inventory_service import requires_restock
from tier3.supplier_connector import format_currency, calculate_reorder_cost


def test_requires_restock_below_threshold() -> None:
    """Test stock below 50 triggers restock."""
    assert requires_restock(30) is True


def test_requires_restock_above_threshold() -> None:
    """Test stock at or above 50 does not restock."""
    assert requires_restock(100) is False


def test_reorder_cost_calculation() -> None:
    """Test unit cost calculation."""
    assert calculate_reorder_cost(12.50, 4) == 50.00
