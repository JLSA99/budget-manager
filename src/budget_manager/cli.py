import argparse
from pathlib import Path

from . import services, storage

# Always points to <project>/data/transactions.json, wherever you run it from.
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "transactions.json"


def build_parser():
    parser = argparse.ArgumentParser(description="Personal Budget Manager")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="add a transaction")
    add.add_argument("date", help="YYYY-MM-DD")
    add.add_argument("kind", help="expense or income")
    add.add_argument("category")
    add.add_argument("amount")
    add.add_argument("--currency", default="EUR")

    ls = commands.add_parser("list", help="list transactions")
    ls.add_argument("--kind")
    ls.add_argument("--category")

    commands.add_parser("summary", help="show totals")
    commands.add_parser("undo", help="remove the last transaction")

    imp = commands.add_parser("import", help="import transactions from a CSV")
    imp.add_argument("csv_file")
    return parser


def run_command(args, transactions):
    """Returns True if the data changed and must be saved."""
    if args.command == "add":
        t = services.add_transaction(
            transactions, args.date, args.kind, args.category, args.amount, args.currency
        )
        print(f"Added {t.id}: {t.kind} {t.amount:.2f} {t.currency} ({t.category})")
        return True

    if args.command == "list":
        for t in services.filter_transactions(transactions, args.kind, args.category):
            print(f"{t.id}  {t.date}  {t.kind:<8} {t.category:<10} {t.amount:>9.2f} {t.currency}")
        return False

    if args.command == "summary":
        s = services.summarize(transactions)
        print(f"Income:   {s['income']:.2f}")
        print(f"Expenses: {s['expenses']:.2f}")
        print(f"Balance:  {s['balance']:.2f}")
        for category, total in s["by_category"].items():
            print(f"  {category}: {total:.2f}")
        return False

    if args.command == "undo":
        removed = services.undo_last(transactions)
        print(f"Removed {removed.id}")
        return True

    if args.command == "import":
        rows = storage.read_csv_rows(args.csv_file)
        errors = services.import_rows(transactions, rows)
        if errors:
            print("Import failed. Nothing was saved:")
            for message in errors:
                print("  " + message)
            return False
        print(f"Imported {len(rows)} transactions.")
        return True


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        transactions = storage.load_transactions(DATA_FILE)
        if run_command(args, transactions):
            storage.save_transactions(DATA_FILE, transactions)  # save right after every change
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#build_parser defines the commands you type: add, list, summary, undo and import with the arguments currency, kind, category
#run_command reads the command chosen and calls function from services printing the result, returns true if data changed and false if not. 
#main parses command line args, loads data, runs command, saves only if run-command true, and catches errors otherwise returns 0