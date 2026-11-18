import math
from datetime import date

KINDS = ("expense", "income")
CATEGORIES = ("food", "rent", "transport", "leisure", "health", "salary", "other")
CURRENCIES = ("EUR",)


class ValidationError(ValueError):
    """Raised when input breaks a rule. The message tells the user what to fix."""


def validate_fields(date_text, kind, category, amount, currency="EUR"):
    """Check the values and return them cleaned, or raise ValidationError."""
    date_text = str(date_text).strip()
    kind = str(kind).strip().lower()
    category = str(category).strip().lower()
    currency = str(currency).strip().upper()

    try:
        date.fromisoformat(date_text)
    except ValueError:
        raise ValidationError(f"date must be YYYY-MM-DD, got '{date_text}'.")

    if kind not in KINDS:
        raise ValidationError(f"kind must be one of {', '.join(KINDS)}, got '{kind}'.")

    if category not in CATEGORIES:
        raise ValidationError(
            f"category '{category}' is unknown. Allowed: {', '.join(CATEGORIES)}."
        )

    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        raise ValidationError(f"amount must be a number, got '{amount}'.")
    if not math.isfinite(amount_value) or amount_value <= 0:
        raise ValidationError("amount must be > 0.")

    if currency not in CURRENCIES:
        raise ValidationError(f"currency must be one of {', '.join(CURRENCIES)}.")

    return date_text, kind, category, round(amount_value, 2), currency