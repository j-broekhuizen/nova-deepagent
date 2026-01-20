"""Savings tools."""

from datetime import datetime, timedelta
from typing import Optional

from langchain_core.tools import tool

from nova.data.mock_data import (
    MockDataStore,
    get_mock_accounts,
    get_mock_transactions,
    get_mock_recurring_bills,
)


@tool
def get_savings_recommendation() -> dict:
    """Calculate how much the user can safely save after income and bills.

    This analyzes:
    - Recent income (paychecks in last 7 days)
    - Upcoming recurring bills
    - Current account balances

    Use this when the user asks about saving money or after detecting a recent paycheck.

    Returns:
        Recommendation with suggested savings amount and reasoning.
    """
    accounts = get_mock_accounts()
    transactions = get_mock_transactions()
    bills = get_mock_recurring_bills()

    # Find checking and savings accounts
    checking = next((a for a in accounts if a.type.value == "checking"), None)
    savings = next((a for a in accounts if a.type.value == "savings"), None)

    # Get recent income (last 7 days)
    recent_cutoff = datetime.now() - timedelta(days=7)
    recent_income = [t for t in transactions if t.is_income and t.date >= recent_cutoff]

    # Calculate upcoming bills (monthly total)
    total_upcoming_bills = sum(b.amount for b in bills)

    if checking and recent_income:
        total_recent_income = sum(t.amount for t in recent_income)

        # Calculate available after bills
        available_after_bills = checking.balance - total_upcoming_bills

        # Suggest saving ~30% of what's available after bills
        # This leaves ~70% for discretionary spending
        if available_after_bills > 100:
            suggested = available_after_bills * 0.30
            # Round to nice numbers
            suggested = round(suggested / 25) * 25  # Round to nearest $25
            suggested = max(suggested, 50)  # At least $50 if possible
        else:
            suggested = 0

        return {
            "has_recent_deposit": True,
            "recent_income": round(total_recent_income, 2),
            "checking_balance": round(checking.balance, 2),
            "upcoming_bills": round(total_upcoming_bills, 2),
            "available_after_bills": round(available_after_bills, 2),
            "suggested_savings": round(suggested, 2),
            "remaining_for_spending": round(available_after_bills - suggested, 2),
            "savings_account_balance": round(savings.balance, 2) if savings else 0,
            "recommendation": (
                f"You could save ${suggested:,.2f} and still have "
                f"${available_after_bills - suggested:,.2f} for spending this month."
            ),
        }

    return {
        "has_recent_deposit": False,
        "checking_balance": round(checking.balance, 2) if checking else 0,
        "upcoming_bills": round(total_upcoming_bills, 2),
        "message": "No recent income detected to base savings recommendation on.",
    }


@tool
def calculate_savings_potential(
    category: str,
    alternative_cost_per_instance: float,
    alternative_description: str,
) -> dict:
    """Calculate potential savings from changing a spending habit.

    Use this for "what if" scenarios like:
    - "How much could I save making coffee at home?" (category="coffee", alternative_cost=0.50)
    - "How much would I save cooking instead of ordering delivery?" (category="delivery", alternative_cost=10.00)

    Args:
        category: The spending category to analyze (e.g., "coffee", "delivery", "fast_food").
        alternative_cost_per_instance: The estimated cost of the alternative per instance.
        alternative_description: Description of the change (e.g., "making coffee at home").

    Returns:
        Projected monthly and yearly savings with current habit analysis.
    """
    transactions = get_mock_transactions()
    cutoff = datetime.now() - timedelta(days=30)

    # Get transactions in this category
    category_txns = [
        t
        for t in transactions
        if t.is_expense
        and t.date >= cutoff
        and t.merchant
        and t.merchant.category.value == category
    ]

    if not category_txns:
        return {"error": f"No spending found in category: {category}"}

    current_monthly = sum(abs(t.amount) for t in category_txns)
    visit_count = len(category_txns)
    avg_per_visit = current_monthly / visit_count if visit_count else 0

    # Calculate savings
    new_monthly_cost = visit_count * alternative_cost_per_instance
    monthly_savings = current_monthly - new_monthly_cost
    yearly_savings = monthly_savings * 12

    return {
        "category": category,
        "current_monthly_spending": round(current_monthly, 2),
        "visits_per_month": visit_count,
        "average_per_visit": round(avg_per_visit, 2),
        "alternative": alternative_description,
        "alternative_cost_per_instance": alternative_cost_per_instance,
        "new_monthly_cost": round(new_monthly_cost, 2),
        "monthly_savings": round(monthly_savings, 2),
        "yearly_savings": round(yearly_savings, 2),
        "summary": (
            f"By {alternative_description}, you could save "
            f"${monthly_savings:,.2f}/month or ${yearly_savings:,.2f}/year."
        ),
    }


@tool
def transfer_to_savings(
    amount: float,
    from_account_id: Optional[str] = None,
    to_account_id: Optional[str] = None,
) -> dict:
    """Transfer money to savings account.

    This executes a simulated transfer between accounts, updating the balances.

    Args:
        amount: Amount to transfer.
        from_account_id: Source account ID (defaults to primary checking).
        to_account_id: Destination account ID (defaults to primary savings).

    Returns:
        Transfer result with updated balances.
    """
    store = MockDataStore()
    accounts = store.accounts

    # Find accounts
    if from_account_id:
        from_account = store.get_account_by_id(from_account_id)
    else:
        from_account = next((a for a in accounts if a.type.value == "checking"), None)

    if to_account_id:
        to_account = store.get_account_by_id(to_account_id)
    else:
        to_account = next((a for a in accounts if a.type.value == "savings"), None)

    if not from_account:
        return {"error": "Could not find source account"}

    if not to_account:
        return {"error": "Could not find destination account"}

    if amount <= 0:
        return {"error": "Amount must be positive"}

    if amount > from_account.balance:
        return {
            "error": f"Insufficient funds. {from_account.name} balance: ${from_account.balance:,.2f}"
        }

    # Execute the transfer
    success = store.transfer(from_account.id, to_account.id, amount)

    if success:
        return {
            "status": "completed",
            "amount": amount,
            "from_account": from_account.name,
            "from_new_balance": round(from_account.balance, 2),
            "to_account": to_account.name,
            "to_new_balance": round(to_account.balance, 2),
            "message": (
                f"Transferred ${amount:,.2f} from {from_account.name} to {to_account.name}. "
                f"Your new savings balance is ${to_account.balance:,.2f}."
            ),
        }
    else:
        return {"error": "Transfer failed. Please try again."}
