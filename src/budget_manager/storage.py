import csv
import json
from pathlib import Path

from .models import Transaction
from .validation import ValidationError


def load_transactions(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValidationError(f"{path} is not valid JSON: {error}")
    if not isinstance(raw, list):
        raise ValidationError(f"{path} must contain a JSON list.")
    try:
        return [Transaction(**item) for item in raw]
    except TypeError:
        raise ValidationError(f"{path} has records with missing or extra fields.")


def save_transactions(path, transactions):
    """Write to a temporary file first, then swap it in, so a crash
    never leaves a half-written file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps([t.to_dict() for t in transactions], indent=2), encoding="utf-8"
    )
    temp.replace(path)


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))