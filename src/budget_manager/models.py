from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    id: str
    date: str
    kind: str       # "expense" or "income"
    category: str
    amount: float
    currency: str

    def to_dict(self):
        return asdict(self)
#Creation of the class and data for the dict. 