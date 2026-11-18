from .models import Transaction
from .validation import ValidationError, validate_fields


def next_id(transactions):
    return f"T{len(transactions) + 1:03d}"


def add_transaction(transactions, date_text, kind, category, amount, currency="EUR"):
    """Validate, create and append a transaction. Returns the new one."""
    fields = validate_fields(date_text, kind, category, amount, currency)
    transaction = Transaction(next_id(transactions), *fields)
    transactions.append(transaction)
    return transaction


def filter_transactions(transactions, kind=None, category=None):
    result = transactions
    if kind:
        result = [t for t in result if t.kind == kind]
    if category:
        result = [t for t in result if t.category == category]
    return result


def summarize(transactions):
    income = sum(t.amount for t in transactions if t.kind == "income")
    expenses = sum(t.amount for t in transactions if t.kind == "expense")
    by_category = {}
    for t in transactions:
        if t.kind == "expense":
            by_category[t.category] = by_category.get(t.category, 0) + t.amount
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "by_category": {c: round(v, 2) for c, v in by_category.items()},
    }


def undo_last(transactions):
    if not transactions:
        raise ValueError("Nothing to undo.")
    return transactions.pop()


def import_rows(transactions, rows):
    """All-or-nothing import. Returns a list of error messages.
    If there is any error, `transactions` is left untouched."""
    candidate = list(transactions)
    errors = []
    for row_number, row in enumerate(rows, start=2):  # row 1 is the CSV header
        try:
            add_transaction(
                candidate,
                row.get("date"), row.get("kind"), row.get("category"),
                row.get("amount"), row.get("currency") or "EUR",
            )
        except ValidationError as error:
            errors.append(f"Row {row_number}: {error}")
    if not errors:
        transactions.extend(candidate[len(transactions):])
    return errors