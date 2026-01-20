"""Mock data generator for Nova demo.

Generates realistic financial data including transactions, accounts, and bills.
Uses a singleton pattern so transfers can update balances during the session.
"""

import random
from datetime import datetime, timedelta
from typing import Optional

from nova.models.account import Account, AccountType, RecurringBill
from nova.models.transaction import (
    Transaction,
    MerchantInfo,
    TransactionCategory,
)


class MockDataStore:
    """Singleton store for mock financial data.

    This allows transfers to update balances within a session.
    """

    _instance: Optional["MockDataStore"] = None
    _initialized: bool = False

    def __new__(cls) -> "MockDataStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if MockDataStore._initialized:
            return
        MockDataStore._initialized = True

        # Set random seed for reproducible demo data
        random.seed(42)

        self._accounts = self._generate_accounts()
        self._transactions = self._generate_transactions()
        self._recurring_bills = self._generate_recurring_bills()

    def _generate_accounts(self) -> list[Account]:
        """Generate mock bank accounts."""
        now = datetime.now()
        return [
            Account(
                id="acct_checking_001",
                name="Primary Checking",
                type=AccountType.CHECKING,
                balance=2915.67,  # After recent paycheck, before bills
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

    def _generate_recurring_bills(self) -> list[RecurringBill]:
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

    def _generate_transactions(self) -> list[Transaction]:
        """Generate realistic mock transactions for the past 90 days.

        Patterns are tuned to produce approximately:
        - ~$271 at Starbucks (monthly)
        - ~$312 at Uber Eats (monthly)
        - ~$104 at McDonald's (monthly)
        """
        transactions: list[Transaction] = []
        now = datetime.now()

        # Define spending patterns
        # frequency = expected times per week
        patterns = [
            # Coffee - targeting ~$271/month
            # With ~40 visits at ~$6.75 avg = $270
            {
                "merchant": "Starbucks",
                "category": TransactionCategory.COFFEE,
                "amount_range": (5.50, 8.00),
                "frequency": 10,  # ~10 times per week (includes multiple visits/day)
                "weekday_only": False,  # Some weekend visits too
            },
            # Uber Eats - targeting ~$312/month
            # ~2.5 visits/week * 4.3 weeks * $35 avg = ~$376/month
            {
                "merchant": "Uber Eats",
                "category": TransactionCategory.DELIVERY,
                "amount_range": (28.00, 48.00),
                "frequency": 2.3,
                "weekday_only": False,
            },
            # McDonald's - targeting ~$104/month
            # ~2 visits/week * 4.3 weeks * $12 avg = ~$103/month
            {
                "merchant": "McDonald's",
                "category": TransactionCategory.FAST_FOOD,
                "amount_range": (9.00, 15.00),
                "frequency": 2.0,
                "weekday_only": False,
            },
            # Other fast food
            {
                "merchant": "Chick-fil-A",
                "category": TransactionCategory.FAST_FOOD,
                "amount_range": (11.00, 18.00),
                "frequency": 1.0,
                "weekday_only": False,
            },
            # More delivery
            {
                "merchant": "DoorDash",
                "category": TransactionCategory.DELIVERY,
                "amount_range": (22.00, 42.00),
                "frequency": 1.5,
                "weekday_only": False,
            },
            # Groceries
            {
                "merchant": "Whole Foods",
                "category": TransactionCategory.GROCERIES,
                "amount_range": (55.00, 140.00),
                "frequency": 0.8,
                "weekday_only": False,
            },
            {
                "merchant": "Trader Joe's",
                "category": TransactionCategory.GROCERIES,
                "amount_range": (35.00, 85.00),
                "frequency": 0.7,
                "weekday_only": False,
            },
            # Transportation
            {
                "merchant": "Uber",
                "category": TransactionCategory.TRANSPORTATION,
                "amount_range": (14.00, 32.00),
                "frequency": 1.5,
                "weekday_only": False,
            },
            {
                "merchant": "Shell",
                "category": TransactionCategory.TRANSPORTATION,
                "amount_range": (42.00, 62.00),
                "frequency": 0.4,
                "weekday_only": False,
            },
            # Entertainment
            {
                "merchant": "AMC Theatres",
                "category": TransactionCategory.ENTERTAINMENT,
                "amount_range": (16.00, 28.00),
                "frequency": 0.4,
                "weekday_only": False,
            },
            # Shopping
            {
                "merchant": "Amazon",
                "category": TransactionCategory.SHOPPING,
                "amount_range": (18.00, 95.00),
                "frequency": 1.8,
                "weekday_only": False,
            },
            {
                "merchant": "Target",
                "category": TransactionCategory.SHOPPING,
                "amount_range": (28.00, 75.00),
                "frequency": 0.8,
                "weekday_only": False,
            },
        ]

        # Generate transactions for 90 days
        for day_offset in range(90):
            date = now - timedelta(days=day_offset)
            is_weekday = date.weekday() < 5

            for pattern in patterns:
                if pattern["weekday_only"] and not is_weekday:
                    continue

                # Probability based on frequency per week
                if random.random() < pattern["frequency"] / 7:
                    amount = -round(random.uniform(*pattern["amount_range"]), 2)

                    # Randomly assign to checking or credit card
                    account_id = (
                        "acct_checking_001"
                        if random.random() > 0.4
                        else "acct_credit_001"
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
            # Make payday Friday
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

        # Sort by date descending
        transactions.sort(key=lambda x: x.date, reverse=True)
        return transactions

    @property
    def accounts(self) -> list[Account]:
        """Get all accounts."""
        return self._accounts

    @property
    def transactions(self) -> list[Transaction]:
        """Get all transactions."""
        return self._transactions

    @property
    def recurring_bills(self) -> list[RecurringBill]:
        """Get all recurring bills."""
        return self._recurring_bills

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Get an account by ID."""
        for account in self._accounts:
            if account.id == account_id:
                return account
        return None

    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        """Execute a transfer between accounts.

        Updates balances in-memory for the demo.
        """
        from_account = self.get_account_by_id(from_account_id)
        to_account = self.get_account_by_id(to_account_id)

        if not from_account or not to_account:
            return False

        if from_account.balance < amount:
            return False

        # Update balances
        from_account.balance -= amount
        if from_account.available_balance is not None:
            from_account.available_balance -= amount

        to_account.balance += amount
        if to_account.available_balance is not None:
            to_account.available_balance += amount

        # Add transfer transactions
        now = datetime.now()
        self._transactions.insert(
            0,
            Transaction(
                id=f"txn_transfer_{len(self._transactions):06d}",
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
        self._transactions.insert(
            0,
            Transaction(
                id=f"txn_transfer_{len(self._transactions):06d}",
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


# Convenience functions that use the singleton
def get_mock_accounts() -> list[Account]:
    """Get all mock accounts."""
    return MockDataStore().accounts


def get_mock_transactions() -> list[Transaction]:
    """Get all mock transactions."""
    return MockDataStore().transactions


def get_mock_recurring_bills() -> list[RecurringBill]:
    """Get all mock recurring bills."""
    return MockDataStore().recurring_bills
