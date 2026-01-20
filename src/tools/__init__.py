"""Nova financial tools."""

from src.tools.transactions import get_transactions, get_recent_income
from src.tools.spending import (
    get_spending_summary,
    get_category_spending,
    get_merchant_spending_pattern,
)
from src.tools.savings import (
    get_savings_recommendation,
    calculate_savings_potential,
    transfer_to_savings,
)
from src.tools.accounts import get_accounts, get_recurring_bills
from src.tools.enrichment import enrich_transaction

__all__ = [
    # Transactions
    "get_transactions",
    "get_recent_income",
    # Spending
    "get_spending_summary",
    "get_category_spending",
    "get_merchant_spending_pattern",
    # Savings
    "get_savings_recommendation",
    "calculate_savings_potential",
    "transfer_to_savings",
    # Accounts
    "get_accounts",
    "get_recurring_bills",
    # Enrichment
    "enrich_transaction",
]
