"""Transaction data models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TransactionCategory(str, Enum):
    """Categories for transaction enrichment."""

    COFFEE = "coffee"
    FAST_FOOD = "fast_food"
    DELIVERY = "delivery"
    DINING = "dining"
    ENTERTAINMENT = "entertainment"
    GROCERIES = "groceries"
    TRANSPORTATION = "transportation"
    SHOPPING = "shopping"
    SUBSCRIPTION = "subscription"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    INCOME = "income"
    TRANSFER = "transfer"
    OTHER = "other"


class MerchantInfo(BaseModel):
    """Enriched merchant information."""

    name: str
    normalized_name: str  # e.g., "STARBUCKS #12345" -> "Starbucks"
    category: TransactionCategory
    logo_url: Optional[str] = None


class Transaction(BaseModel):
    """A financial transaction."""

    id: str
    account_id: str
    amount: float  # Negative for debits, positive for credits
    description: str  # Raw merchant description
    date: datetime
    pending: bool = False

    # Enriched fields (populated by enrichment)
    merchant: Optional[MerchantInfo] = None
    tags: list[str] = Field(default_factory=list)

    @property
    def is_expense(self) -> bool:
        """Check if this is an expense (negative amount)."""
        return self.amount < 0

    @property
    def is_income(self) -> bool:
        """Check if this is income (positive amount)."""
        return self.amount > 0

    @property
    def display_amount(self) -> str:
        """Format amount for display."""
        return f"${abs(self.amount):,.2f}"

    def model_dump(self, **kwargs) -> dict:
        """Override to handle enum serialization."""
        data = super().model_dump(**kwargs)
        if self.merchant:
            data["merchant"]["category"] = self.merchant.category.value
        return data
