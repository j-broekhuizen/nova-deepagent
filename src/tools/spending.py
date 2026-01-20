"""Spending analysis tools."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Literal

from langchain_core.tools import tool

from src.data.mock_data import get_mock_transactions


@tool
def get_spending_summary(
    period: Literal["week", "month", "quarter"] = "month",
    group_by: Literal["category", "merchant", "day"] = "category",
    top_n: int = 10,
) -> dict:
    """Get a summary of spending grouped by category, merchant, or day.

    Args:
        period: Time period to analyze - "week", "month", or "quarter".
        group_by: How to group the spending - "category", "merchant", or "day".
        top_n: Number of top items to return.

    Returns:
        Dictionary with grouped spending data and insights.
    """
    # Calculate date range
    now = datetime.now()
    if period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    else:  # quarter
        start = now - timedelta(days=90)

    transactions = get_mock_transactions()
    expenses = [t for t in transactions if t.is_expense and t.date >= start]

    if not expenses:
        return {
            "period": period,
            "group_by": group_by,
            "total_spending": 0,
            "breakdown": [],
            "transaction_count": 0,
        }

    # Group spending
    grouped: dict[str, float] = defaultdict(float)
    for txn in expenses:
        if group_by == "category":
            key = txn.merchant.category.value if txn.merchant else "other"
        elif group_by == "merchant":
            key = txn.merchant.normalized_name if txn.merchant else txn.description
        else:  # day
            key = txn.date.strftime("%Y-%m-%d")
        grouped[key] += abs(txn.amount)

    # Sort and take top N
    sorted_items = sorted(grouped.items(), key=lambda x: x[1], reverse=True)
    top_items = sorted_items[:top_n]

    total_spending = sum(abs(t.amount) for t in expenses)

    return {
        "period": period,
        "group_by": group_by,
        "total_spending": round(total_spending, 2),
        "breakdown": [
            {
                "name": k,
                "amount": round(v, 2),
                "percentage": round(v / total_spending * 100, 1),
            }
            for k, v in top_items
        ],
        "transaction_count": len(expenses),
    }


@tool
def get_category_spending(
    categories: list[str],
    days: int = 30,
) -> dict:
    """Get detailed spending for specific categories.

    Use this to analyze spending in categories like "dining", "entertainment",
    "coffee", "fast_food", "delivery", etc.

    Args:
        categories: List of categories to analyze (e.g., ["dining", "coffee", "fast_food", "delivery"]).
        days: Number of days to look back.

    Returns:
        Dictionary with per-category breakdown including top merchants.
    """
    cutoff = datetime.now() - timedelta(days=days)
    transactions = get_mock_transactions()

    result = {}
    combined_total = 0

    for category in categories:
        category_txns = [
            t
            for t in transactions
            if t.is_expense
            and t.date >= cutoff
            and t.merchant
            and t.merchant.category.value == category
        ]

        # Group by merchant within category
        by_merchant: dict[str, list] = defaultdict(list)
        for txn in category_txns:
            by_merchant[txn.merchant.normalized_name].append(txn)

        merchant_totals = [
            {
                "merchant": name,
                "total": round(sum(abs(t.amount) for t in txns), 2),
                "count": len(txns),
            }
            for name, txns in by_merchant.items()
        ]
        merchant_totals.sort(key=lambda x: x["total"], reverse=True)

        category_total = round(sum(abs(t.amount) for t in category_txns), 2)
        combined_total += category_total

        result[category] = {
            "total": category_total,
            "transaction_count": len(category_txns),
            "top_merchants": merchant_totals[:5],
        }

    return {
        "categories": result,
        "combined_total": round(combined_total, 2),
        "period_days": days,
    }


@tool
def get_merchant_spending_pattern(
    merchant_name: str,
    days: int = 30,
) -> dict:
    """Analyze spending pattern for a specific merchant.

    Use this to understand habits like coffee shop visits, food delivery frequency, etc.
    This is useful for calculating savings potential from changing habits.

    Args:
        merchant_name: Name of the merchant to analyze (e.g., "Starbucks", "Uber Eats").
        days: Number of days to analyze.

    Returns:
        Spending pattern including frequency, average, weekday vs weekend analysis.
    """
    cutoff = datetime.now() - timedelta(days=days)
    transactions = get_mock_transactions()

    merchant_txns = [
        t
        for t in transactions
        if t.is_expense
        and t.date >= cutoff
        and t.merchant
        and merchant_name.lower() in t.merchant.normalized_name.lower()
    ]

    if not merchant_txns:
        return {"error": f"No transactions found for '{merchant_name}' in the last {days} days"}

    # Analyze patterns
    total = sum(abs(t.amount) for t in merchant_txns)
    count = len(merchant_txns)

    # Day of week analysis
    day_counts: dict[str, int] = defaultdict(int)
    day_amounts: dict[str, float] = defaultdict(float)
    for txn in merchant_txns:
        day = txn.date.strftime("%A")
        day_counts[day] += 1
        day_amounts[day] += abs(txn.amount)

    # Weekday vs weekend
    weekday_txns = [t for t in merchant_txns if t.date.weekday() < 5]
    weekend_txns = [t for t in merchant_txns if t.date.weekday() >= 5]

    weekday_total = sum(abs(t.amount) for t in weekday_txns)
    weekend_total = sum(abs(t.amount) for t in weekend_txns)

    weeks = days / 7

    return {
        "merchant": merchant_name,
        "period_days": days,
        "total_spent": round(total, 2),
        "transaction_count": count,
        "average_transaction": round(total / count, 2),
        "visits_per_week": round(count / weeks, 1),
        "weekday_spending": round(weekday_total, 2),
        "weekday_visits": len(weekday_txns),
        "weekend_spending": round(weekend_total, 2),
        "weekend_visits": len(weekend_txns),
        "busiest_day": max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None,
        "by_day_of_week": {k: round(v, 2) for k, v in day_amounts.items()},
    }
