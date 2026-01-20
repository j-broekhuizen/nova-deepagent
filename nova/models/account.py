"""Account data models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AccountType(str, Enum):
    """Types of financial accounts."""

    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"


class Account(BaseModel):
    """A user's financial account."""

    id: str
    name: str
    type: AccountType
    balance: float
    available_balance: Optional[float] = None  # For credit cards: limit - balance
    institution: str
    last_updated: datetime

    # For savings accounts
    apy: Optional[float] = None  # Annual percentage yield

    @property
    def display_balance(self) -> str:
        """Format balance for display."""
        return f"${self.balance:,.2f}"

    def model_dump(self, **kwargs) -> dict:
        """Override to handle enum serialization."""
        data = super().model_dump(**kwargs)
        data["type"] = self.type.value
        if self.last_updated:
            data["last_updated"] = self.last_updated.isoformat()
        return data


class RecurringBill(BaseModel):
    """A detected recurring bill/expense."""

    id: str
    name: str
    amount: float
    frequency: str  # "monthly", "weekly", "biweekly"
    next_due: datetime
    account_id: str
    category: str

    def model_dump(self, **kwargs) -> dict:
        """Override to handle datetime serialization."""
        data = super().model_dump(**kwargs)
        if self.next_due:
            data["next_due"] = self.next_due.isoformat()
        return data
