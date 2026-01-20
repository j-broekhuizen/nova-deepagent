"""Account tools."""

from langchain_core.tools import tool

from src.data.mock_data import get_mock_accounts, get_mock_recurring_bills


@tool
def get_accounts() -> dict:
    """Get all linked financial accounts with current balances.

    Returns:
        List of accounts with balances, types, and a summary.
    """
    accounts = get_mock_accounts()

    total_assets = sum(
        a.balance for a in accounts if a.type.value in ["checking", "savings", "investment"]
    )
    total_liabilities = sum(
        abs(a.balance) for a in accounts if a.type.value == "credit_card" and a.balance < 0
    )

    return {
        "accounts": [a.model_dump() for a in accounts],
        "summary": {
            "total_accounts": len(accounts),
            "total_assets": round(total_assets, 2),
            "total_liabilities": round(total_liabilities, 2),
            "net_worth": round(total_assets - total_liabilities, 2),
        },
    }


@tool
def get_recurring_bills() -> dict:
    """Get detected recurring bills and subscriptions.

    Use this to understand the user's fixed monthly expenses.

    Returns:
        List of recurring expenses with due dates, amounts, and monthly total.
    """
    bills = get_mock_recurring_bills()

    monthly_total = sum(b.amount for b in bills if b.frequency == "monthly")

    # Group by category
    by_category: dict[str, float] = {}
    for bill in bills:
        by_category[bill.category] = by_category.get(bill.category, 0) + bill.amount

    return {
        "bills": [b.model_dump() for b in bills],
        "monthly_total": round(monthly_total, 2),
        "count": len(bills),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
    }
