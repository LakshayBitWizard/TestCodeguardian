"""Medical supplier connector and purchase order utilities."""

from typing import Any


def format_currency(amount: float, currency_code: str = "USD") -> str:
    """Format floating point currency figure with ISO symbol."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
    sym = symbols.get(currency_code, "$")
    return f"{sym}{amount:,.2f}"


def calculate_reorder_cost(unit_cost: float, quantity: int) -> float:
    """Compute subtotal cost for replenishment purchase order."""
    if unit_cost < 0 or quantity < 0:
        raise ValueError("Cost and quantity must be non-negative")
    return round(unit_cost * quantity, 2)
