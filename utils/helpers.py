"""
============================================================================
General Helpers & Formatters
============================================================================
Utility functions used across the application.
============================================================================
"""

from __future__ import annotations

import locale


def format_number(value: int | float, decimals: int = 0) -> str:
    """Format a number with thousands separators. E.g. 1234567 → '1,234,567'."""
    if decimals > 0:
        return f"{value:,.{decimals}f}"
    return f"{value:,.0f}"


def format_currency(value: float, symbol: str = "$", decimals: int = 2) -> str:
    """Format a number as currency. E.g. 1234.5 → '$1,234.50'."""
    return f"{symbol}{value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a decimal as percentage. E.g. 0.123 → '12.3%'."""
    return f"{value * 100:,.{decimals}f}%"


def truncate_text(text: str, max_length: int = 100, suffix: str = "…") -> str:
    """Truncate text to max_length characters, appending suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division that returns default instead of raising ZeroDivisionError."""
    if denominator == 0:
        return default
    return numerator / denominator
