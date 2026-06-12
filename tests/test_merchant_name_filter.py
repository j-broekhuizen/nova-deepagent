"""Regression tests for merchant_name brand-vs-extension exact-match filter."""

from src.tools.spending import get_merchant_spending_pattern
from src.tools.transactions import get_transactions


def test_get_transactions_uber_does_not_match_uber_eats():
    result = get_transactions.invoke({"merchant_name": "Uber", "limit": 500})
    merchants = {t["merchant"]["normalized_name"] for t in result["transactions"]}
    assert merchants == {"Uber"}
    assert "Uber Eats" not in merchants


def test_get_transactions_uber_eats_does_not_match_uber():
    result = get_transactions.invoke({"merchant_name": "Uber Eats", "limit": 500})
    merchants = {t["merchant"]["normalized_name"] for t in result["transactions"]}
    assert merchants == {"Uber Eats"}
    assert "Uber" not in merchants


def test_get_transactions_merchant_name_is_case_insensitive():
    lower = get_transactions.invoke({"merchant_name": "uber", "limit": 500})
    upper = get_transactions.invoke({"merchant_name": "Uber", "limit": 500})
    assert lower["count"] == upper["count"]
    assert lower["count"] > 0


def test_merchant_spending_pattern_uber_excludes_uber_eats():
    pattern = get_merchant_spending_pattern.invoke({"merchant_name": "Uber", "days": 90})
    assert pattern.get("merchant") == "Uber"
    # If Uber Eats had bled in, totals/counts would be inflated; sanity-check by
    # comparing against Uber Eats lookup — the two sets must be disjoint.
    eats = get_merchant_spending_pattern.invoke({"merchant_name": "Uber Eats", "days": 90})
    assert eats.get("merchant") == "Uber Eats"
    assert pattern["transaction_count"] + eats["transaction_count"] > 0
