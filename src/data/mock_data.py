"""Mock data generator for Nova demo.

Generates realistic financial data including transactions, accounts, and bills.
Data is generated once per module load and cached.
"""

import random
from datetime import datetime, timedelta

from src.models.account import Account, AccountType, RecurringBill
from src.models.transaction import (
    Transaction,
    MerchantInfo,
    TransactionCategory,
)


def _generate_accounts() -> list[Account]:
    """Generate mock bank accounts."""
    now = datetime.now()
    return [
        Account(
            id="acct_checking_001",
            name="Primary Checking",
            type=AccountType.CHECKING,
            balance=2915.67,
            available_balance=2915.67,
            institution="Chase",
            last_updated=now,
        ),
        Account(
            id="acct_savings_001",
            name="Emergency Savings",
            type=AccountType.SAVINGS,
            balance=8500.00,
            institution="Chase",
            last_updated=now,
            apy=0.045,
        ),
        Account(
            id="acct_credit_001",
            name="Chase Sapphire",
            type=AccountType.CREDIT_CARD,
            balance=-1234.56,
            available_balance=8765.44,
            institution="Chase",
            last_updated=now,
        ),
    ]


def _generate_recurring_bills() -> list[RecurringBill]:
    """Generate mock recurring bills."""
    now = datetime.now()
    return [
        RecurringBill(
            id="bill_001",
            name="Rent",
            amount=1850.00,
            frequency="monthly",
            next_due=now + timedelta(days=5),
            account_id="acct_checking_001",
            category="housing",
        ),
        RecurringBill(
            id="bill_002",
            name="Electric",
            amount=125.00,
            frequency="monthly",
            next_due=now + timedelta(days=12),
            account_id="acct_checking_001",
            category="utilities",
        ),
        RecurringBill(
            id="bill_003",
            name="Internet",
            amount=79.99,
            frequency="monthly",
            next_due=now + timedelta(days=8),
            account_id="acct_checking_001",
            category="utilities",
        ),
        RecurringBill(
            id="bill_004",
            name="Car Insurance",
            amount=156.00,
            frequency="monthly",
            next_due=now + timedelta(days=15),
            account_id="acct_checking_001",
            category="insurance",
        ),
        RecurringBill(
            id="bill_005",
            name="Netflix",
            amount=15.49,
            frequency="monthly",
            next_due=now + timedelta(days=20),
            account_id="acct_credit_001",
            category="subscription",
        ),
        RecurringBill(
            id="bill_006",
            name="Spotify",
            amount=10.99,
            frequency="monthly",
            next_due=now + timedelta(days=18),
            account_id="acct_credit_001",
            category="subscription",
        ),
    ]


def _generate_transactions() -> list[Transaction]:
    """Generate realistic mock transactions for the past 90 days."""
    random.seed(42)  # Reproducible data
    transactions: list[Transaction] = []
    now = datetime.now()

    patterns = [
        {
            "merchant": "Starbucks",
            "category": TransactionCategory.COFFEE,
            "amount_range": (5.50, 8.00),
            "frequency": 10,
        },
        {
            "merchant": "Uber Eats",
            "category": TransactionCategory.DELIVERY,
            "amount_range": (28.00, 48.00),
            "frequency": 2.3,
        },
        {
            "merchant": "McDonald's",
            "category": TransactionCategory.FAST_FOOD,
            "amount_range": (9.00, 15.00),
            "frequency": 2.0,
        },
        {
            "merchant": "Chick-fil-A",
            "category": TransactionCategory.FAST_FOOD,
            "amount_range": (11.00, 18.00),
            "frequency": 1.0,
        },
        {
            "merchant": "DoorDash",
            "category": TransactionCategory.DELIVERY,
            "amount_range": (22.00, 42.00),
            "frequency": 1.5,
        },
        {
            "merchant": "Whole Foods",
            "category": TransactionCategory.GROCERIES,
            "amount_range": (55.00, 140.00),
            "frequency": 0.8,
        },
        {
            "merchant": "Trader Joe's",
            "category": TransactionCategory.GROCERIES,
            "amount_range": (35.00, 85.00),
            "frequency": 0.7,
        },
        {
            "merchant": "Uber",
            "category": TransactionCategory.TRANSPORTATION,
            "amount_range": (14.00, 32.00),
            "frequency": 1.5,
        },
        {
            "merchant": "Shell",
            "category": TransactionCategory.TRANSPORTATION,
            "amount_range": (42.00, 62.00),
            "frequency": 0.4,
        },
        {
            "merchant": "AMC Theatres",
            "category": TransactionCategory.ENTERTAINMENT,
            "amount_range": (16.00, 28.00),
            "frequency": 0.4,
        },
        {
            "merchant": "Amazon",
            "category": TransactionCategory.SHOPPING,
            "amount_range": (18.00, 95.00),
            "frequency": 1.8,
        },
        {
            "merchant": "Target",
            "category": TransactionCategory.SHOPPING,
            "amount_range": (28.00, 75.00),
            "frequency": 0.8,
        },
    ]

    for day_offset in range(90):
        date = now - timedelta(days=day_offset)

        for pattern in patterns:
            if random.random() < pattern["frequency"] / 7:
                amount = -round(random.uniform(*pattern["amount_range"]), 2)
                account_id = (
                    "acct_checking_001" if random.random() > 0.4 else "acct_credit_001"
                )

                transactions.append(
                    Transaction(
                        id=f"txn_{len(transactions):06d}",
                        account_id=account_id,
                        amount=amount,
                        description=f"{pattern['merchant']} #{random.randint(1000, 9999)}",
                        date=date.replace(
                            hour=random.randint(7, 21),
                            minute=random.randint(0, 59),
                        ),
                        merchant=MerchantInfo(
                            name=pattern["merchant"],
                            normalized_name=pattern["merchant"],
                            category=pattern["category"],
                        ),
                    )
                )

    # Add income (bi-weekly paychecks)
    for week in range(0, 90, 14):
        paycheck_date = now - timedelta(days=week)
        days_since_friday = (paycheck_date.weekday() - 4) % 7
        paycheck_date = paycheck_date - timedelta(days=days_since_friday)

        transactions.append(
            Transaction(
                id=f"txn_income_{week:03d}",
                account_id="acct_checking_001",
                amount=3250.00,
                description="DIRECT DEPOSIT - ACME CORP PAYROLL",
                date=paycheck_date.replace(hour=6, minute=0),
                merchant=MerchantInfo(
                    name="ACME Corp",
                    normalized_name="Paycheck",
                    category=TransactionCategory.INCOME,
                ),
            )
        )

    transactions.sort(key=lambda x: x.date, reverse=True)
    return transactions


# Module-level cache - generated once on import
_accounts: list[Account] | None = None
_transactions: list[Transaction] | None = None
_recurring_bills: list[RecurringBill] | None = None


def get_mock_accounts() -> list[Account]:
    """Get all mock accounts."""
    global _accounts
    if _accounts is None:
        _accounts = _generate_accounts()
    return _accounts


def get_mock_transactions() -> list[Transaction]:
    """Get all mock transactions."""
    global _transactions
    if _transactions is None:
        _transactions = _generate_transactions()
    return _transactions


def get_mock_recurring_bills() -> list[RecurringBill]:
    """Get all mock recurring bills."""
    global _recurring_bills
    if _recurring_bills is None:
        _recurring_bills = _generate_recurring_bills()
    return _recurring_bills


def get_account_by_id(account_id: str) -> Account | None:
    """Get an account by ID."""
    for account in get_mock_accounts():
        if account.id == account_id:
            return account
    return None


def transfer(from_account_id: str, to_account_id: str, amount: float) -> bool:
    """Execute a transfer between accounts."""
    from_account = get_account_by_id(from_account_id)
    to_account = get_account_by_id(to_account_id)

    if not from_account or not to_account:
        return False

    if from_account.balance < amount:
        return False

    from_account.balance -= amount
    if from_account.available_balance is not None:
        from_account.available_balance -= amount

    to_account.balance += amount
    if to_account.available_balance is not None:
        to_account.available_balance += amount

    now = datetime.now()
    transactions = get_mock_transactions()
    transactions.insert(
        0,
        Transaction(
            id=f"txn_transfer_{len(transactions):06d}",
            account_id=from_account_id,
            amount=-amount,
            description=f"Transfer to {to_account.name}",
            date=now,
            merchant=MerchantInfo(
                name="Internal Transfer",
                normalized_name="Transfer",
                category=TransactionCategory.TRANSFER,
            ),
        ),
    )
    transactions.insert(
        0,
        Transaction(
            id=f"txn_transfer_{len(transactions):06d}",
            account_id=to_account_id,
            amount=amount,
            description=f"Transfer from {from_account.name}",
            date=now,
            merchant=MerchantInfo(
                name="Internal Transfer",
                normalized_name="Transfer",
                category=TransactionCategory.TRANSFER,
            ),
        ),
    )

    return True
