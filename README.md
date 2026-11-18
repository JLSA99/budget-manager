# Personal Budget Manager (Release 1)

A command-line tool to record income and expenses, validate them, and see a summary. Data is saved in a local JSON file. No database is needed.

## Setup

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Run all commands from the project root:

```
python -m src.budget_manager.cli --help
python -m src.budget_manager.cli add 2026-09-06 expense leisure 25
python -m src.budget_manager.cli list
python -m src.budget_manager.cli list --kind expense --category food
python -m src.budget_manager.cli summary
python -m src.budget_manager.cli undo
python -m src.budget_manager.cli import data/sample_transactions.csv
```

## Example

```
$ python -m src.budget_manager.cli import data/sample_invalid.csv
Import failed. Nothing was saved:
  Row 3: amount must be > 0.
  Row 4: category 'pets' is unknown. Allowed: food, rent, transport, leisure, health, salary, other.
  Row 5: date must be YYYY-MM-DD, got '2026-13-01'.

$ python -m src.budget_manager.cli import data/sample_transactions.csv
Imported 4 transactions.

$ python -m src.budget_manager.cli summary
Income:   2000.00
Expenses: 780.50
Balance:  1219.50
```

## Rules (acceptance criteria)

| Input | Result |
|---|---|
| amount `-5` or `0` | Rejected: `amount must be > 0.` |
| unknown category (e.g. `pets`) | Rejected, allowed categories are listed |
| date not in `YYYY-MM-DD` | Rejected with the bad value shown |
| `undo` with no transactions | `Error: Nothing to undo.` |
| CSV with any invalid row | Whole import rejected, error per row, nothing saved |

## Test

```
pytest
```

Expected: `8 passed`.

## Project structure

- `models.py`: the Transaction record
- `validation.py`: all input rules and error messages
- `services.py`: business logic (add, filter, summarize, undo, import)
- `storage.py`: reading and writing JSON and CSV files
- `cli.py`: the command line, the only file that prints and reads commands

## Known limitations

- Only EUR is supported.
- Ids are based on the number of transactions, so they are only unique while undo is the only way to remove data.
- No editing or deleting of old transactions, only undo of the last one.
- Data is stored in `data/transactions.json`, which is not included in the repository.