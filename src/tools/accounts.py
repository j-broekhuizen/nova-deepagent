"""Account tools."""

from datetime import datetime
from typing import Literal
from uuid import uuid4

from langchain_core.tools import tool

from src.data.mock_data import (
    add_spending_alert,
    get_mock_accounts,
    get_mock_recurring_bills,
    get_recurring_bill_by_id,
)
from src.models.account import SpendingAlert


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


@tool
def create_spending_alert(
    category: str,
    threshold: float,
    period: Literal["week", "month"],
) -> dict:
    """Register a spending alert that fires when category spending crosses a threshold.

    Use this when the user asks to be notified when spending in a category
    exceeds an amount over a given period (e.g. "alert me when delivery hits
    $300/month").

    Args:
        category: Spending category to monitor (e.g. "delivery", "coffee").
        threshold: Dollar amount that triggers the alert when crossed.
        period: Window the threshold applies to — "week" or "month".

    Returns:
        Confirmation with the new alert_id, category, threshold, and period.
    """
    if threshold <= 0:
        return {"error": "Threshold must be positive"}

    alert = SpendingAlert(
        id=f"alert_{uuid4().hex[:8]}",
        category=category,
        threshold=round(threshold, 2),
        period=period,
        created_at=datetime.now(),
    )
    add_spending_alert(alert)

    return {
        "status": "created",
        "alert_id": alert.id,
        "category": alert.category,
        "threshold": alert.threshold,
        "period": alert.period,
        "message": (
            f"Alert set: I'll notify you when {category} spending crosses "
            f"${threshold:,.2f} per {period}."
        ),
    }


@tool
def enable_auto_pay(bill_id: str) -> dict:
    """Enable automatic payments on a recurring bill.

    Use this when the user asks to turn on auto-pay for one of their bills.
    Look up the bill ID first with `get_recurring_bills`.

    Args:
        bill_id: ID of the recurring bill (e.g. "bill_002").

    Returns:
        Confirmation with the bill's new autopay state.
    """
    bill = get_recurring_bill_by_id(bill_id)
    if bill is None:
        return {"error": f"No recurring bill found with id: {bill_id}"}

    already_on = bill.autopay_enabled
    bill.autopay_enabled = True

    return {
        "status": "already_enabled" if already_on else "enabled",
        "bill_id": bill.id,
        "bill_name": bill.name,
        "amount": bill.amount,
        "autopay_enabled": True,
        "message": (
            f"Auto-pay is already on for {bill.name}."
            if already_on
            else f"Auto-pay enabled for {bill.name} (${bill.amount:,.2f})."
        ),
    }
