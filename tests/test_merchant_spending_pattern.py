"""Tests for `get_merchant_spending_pattern` exact-merchant matching."""

from datetime import datetime, timedelta

import pytest

from src.models.transaction import (
    MerchantInfo,
    Transaction,
    TransactionCategory,
)
from src.tools import spending as spending_module
from src.tools.spending import get_merchant_spending_pattern


@pytest.fixture
def uber_and_uber_eats(monkeypatch):
    """Two distinct merchants sharing a name prefix but different categories."""
    now = datetime.now()
    txns = [
        Transaction(
            id="txn_uber_001",
            account_id="acct_checking_001",
            amount=-20.00,
            description="UBER TRIP",
            date=now - timedelta(days=1),
            merchant=MerchantInfo(
                name="UBER TRIP",
                normalized_name="Uber",
                category=TransactionCategory.TRANSPORTATION,
            ),
        ),
        Transaction(
            id="txn_uber_eats_001",
            account_id="acct_checking_001",
            amount=-35.00,
            description="UBER EATS",
            date=now - timedelta(days=2),
            merchant=MerchantInfo(
                name="UBER EATS",
                normalized_name="Uber Eats",
                category=TransactionCategory.DELIVERY,
            ),
        ),
    ]
    monkeypatch.setattr(spending_module, "get_mock_transactions", lambda: txns)
    return txns


def test_uber_does_not_match_uber_eats(uber_and_uber_eats):
    result = get_merchant_spending_pattern.invoke({"merchant_name": "Uber", "days": 30})
    assert result["transaction_count"] == 1
    assert result["total_spent"] == 20.00


def test_uber_query_only_returns_transportation_category(uber_and_uber_eats):
    txns = uber_and_uber_eats
    matched = [
        t
        for t in txns
        if t.merchant and t.merchant.normalized_name.lower() == "uber"
    ]
    assert len(matched) == 1
    assert matched[0].merchant.category is TransactionCategory.TRANSPORTATION


def test_uber_eats_query_only_returns_uber_eats(uber_and_uber_eats):
    result = get_merchant_spending_pattern.invoke(
        {"merchant_name": "Uber Eats", "days": 30}
    )
    assert result["transaction_count"] == 1
    assert result["total_spent"] == 35.00
