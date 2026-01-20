"""Transaction query tools."""

from datetime import datetime, timedelta
from typing import Optional

from langchain_core.tools import tool

from nova.data.mock_data import get_mock_transactions


@tool
def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    account_id: Optional[str] = None,
    category: Optional[str] = None,
    merchant_name: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    limit: int = 50,
) -> dict:
    """Get transactions with optional filters.

    Args:
        start_date: Start date in ISO format (YYYY-MM-DD). Defaults to 30 days ago.
        end_date: End date in ISO format (YYYY-MM-DD). Defaults to today.
        account_id: Filter by specific account ID.
        category: Filter by category (e.g., "coffee", "dining", "fast_food", "delivery").
        merchant_name: Filter by merchant name (partial match, case-insensitive).
        min_amount: Minimum transaction amount (absolute value).
        max_amount: Maximum transaction amount (absolute value).
        limit: Maximum number of transactions to return (default 50).

    Returns:
        Dictionary with transactions list and metadata.
    """
    # Parse dates
    if start_date:
        start = datetime.fromisoformat(start_date)
    else:
        start = datetime.now() - timedelta(days=30)

    if end_date:
        end = datetime.fromisoformat(end_date)
    else:
        end = datetime.now()

    # Get all transactions and apply filters
    transactions = get_mock_transactions()

    filtered = []
    for txn in transactions:
        # Date filter
        if txn.date.date() < start.date() or txn.date.date() > end.date():
            continue

        # Account filter
        if account_id and txn.account_id != account_id:
            continue

        # Category filter
        if category and txn.merchant:
            if txn.merchant.category.value != category:
                continue
        elif category and not txn.merchant:
            continue

        # Merchant name filter
        if merchant_name and txn.merchant:
            if merchant_name.lower() not in txn.merchant.normalized_name.lower():
                continue
        elif merchant_name and not txn.merchant:
            continue

        # Amount filters (use absolute value)
        if min_amount is not None and abs(txn.amount) < min_amount:
            continue
        if max_amount is not None and abs(txn.amount) > max_amount:
            continue

        filtered.append(txn)

    # Sort by date descending and limit
    filtered.sort(key=lambda x: x.date, reverse=True)
    filtered = filtered[:limit]

    return {
        "transactions": [t.model_dump() for t in filtered],
        "count": len(filtered),
        "total_amount": round(sum(t.amount for t in filtered), 2),
        "date_range": {"start": start.isoformat(), "end": end.isoformat()},
    }


@tool
def get_recent_income(days: int = 14) -> dict:
    """Get recent income deposits (paychecks, transfers in, etc.).

    Use this to find recent paychecks and determine if the user just got paid.

    Args:
        days: Number of days to look back. Defaults to 14 (to catch bi-weekly pay).

    Returns:
        Dictionary with income transactions and total.
    """
    transactions = get_mock_transactions()
    cutoff = datetime.now() - timedelta(days=days)

    income = [t for t in transactions if t.is_income and t.date >= cutoff]

    # Sort by date descending (most recent first)
    income.sort(key=lambda x: x.date, reverse=True)

    return {
        "income_transactions": [t.model_dump() for t in income],
        "total_income": round(sum(t.amount for t in income), 2),
        "count": len(income),
        "most_recent": income[0].model_dump() if income else None,
    }
