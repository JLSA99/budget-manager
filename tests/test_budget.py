import pytest

from budget_manager import services, storage
from budget_manager.validation import ValidationError


def test_add_valid_expense():
    transactions = []
    t = services.add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    assert t.id == "T001"
    assert t.amount == 18.5
    assert len(transactions) == 1


def test_negative_amount_is_rejected():
    with pytest.raises(ValidationError, match="amount must be > 0"):
        services.add_transaction([], "2026-09-04", "expense", "food", "-5")


def test_zero_amount_is_rejected():
    with pytest.raises(ValidationError, match="amount must be > 0"):
        services.add_transaction([], "2026-09-04", "expense", "food", "0")


def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError, match="category 'pets' is unknown"):
        services.add_transaction([], "2026-09-04", "expense", "pets", "10")


def test_summary_balance():
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", "100")
    services.add_transaction(transactions, "2026-09-02", "expense", "food", "30.25")
    assert services.summarize(transactions)["balance"] == 69.75


def test_undo_removes_last_and_fails_when_empty():
    transactions = []
    services.add_transaction(transactions, "2026-09-04", "expense", "food", "10")
    removed = services.undo_last(transactions)
    assert removed.id == "T001"
    assert transactions == []
    with pytest.raises(ValueError, match="Nothing to undo"):
        services.undo_last(transactions)


def test_save_and_load_round_trip(tmp_path):
    file = tmp_path / "t.json"
    transactions = []
    services.add_transaction(transactions, "2026-09-04", "expense", "food", "18.50")
    storage.save_transactions(file, transactions)
    assert storage.load_transactions(file) == transactions


def test_import_reports_row_numbers_and_saves_nothing():
    rows = [
        {"date": "2026-09-01", "kind": "income", "category": "salary", "amount": "10"},
        {"date": "2026-09-02", "kind": "expense", "category": "food", "amount": "-5"},
    ]
    transactions = []
    errors = services.import_rows(transactions, rows)
    assert errors == ["Row 3: amount must be > 0."]
    assert transactions == []
#test_add_valid_expense : a valid transaction gets id T001 the amount 18.50 and gets added to the list 
#test_negative_amount_is_rejected : -5 raises that the amount must be >0
#test_zero_amount_is_rejected : 0 raises same error 
#test_unknown_category_is_rejected : category pets raises cat. pets is unkown 
#test_summary_balance : 100 income - 30.25 expense gives the value 69.75
#test_undo_removes_last_and_fails_when_empty : Undo removes T001 then raises the Nothing to undo on an empty list 
#test_save_and_load_round_trip : Saving and loading gives back identical data and uses a temporary folder "tmp_path"
#test_import_reports_row_numbers_and_saves_nothing : With a bad row 3, the error says Row 3 and transactions won't be added even the valid row 2.