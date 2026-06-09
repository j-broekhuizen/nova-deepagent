"""Tests for the spending-alert and auto-pay tools."""

from src.data.mock_data import (
    get_mock_recurring_bills,
    get_spending_alerts,
)
from src.tools.accounts import (
    create_spending_alert,
    enable_auto_pay,
    get_recurring_bills,
)


def test_create_spending_alert_registers_alert():
    result = create_spending_alert.invoke(
        {"category": "delivery", "threshold": 300.0, "period": "month"}
    )

    assert result["status"] == "created"
    assert result["category"] == "delivery"
    assert result["threshold"] == 300.0
    assert result["period"] == "month"
    assert result["alert_id"].startswith("alert_")
    assert "$300" in result["message"]

    assert any(a.id == result["alert_id"] for a in get_spending_alerts())


def test_create_spending_alert_rejects_non_positive_threshold():
    result = create_spending_alert.invoke(
        {"category": "coffee", "threshold": 0, "period": "week"}
    )
    assert "error" in result


def test_get_recurring_bills_exposes_autopay_flag():
    result = get_recurring_bills.invoke({})
    assert result["bills"], "expected at least one bill"
    for bill in result["bills"]:
        assert "autopay_enabled" in bill


def test_enable_auto_pay_flips_flag():
    bill = next(b for b in get_mock_recurring_bills() if b.name == "Electric")
    bill.autopay_enabled = False

    result = enable_auto_pay.invoke({"bill_id": bill.id})

    assert result["status"] == "enabled"
    assert result["autopay_enabled"] is True
    assert result["bill_id"] == bill.id
    assert bill.autopay_enabled is True


def test_enable_auto_pay_idempotent():
    bill = next(b for b in get_mock_recurring_bills() if b.name == "Internet")
    bill.autopay_enabled = True

    result = enable_auto_pay.invoke({"bill_id": bill.id})

    assert result["status"] == "already_enabled"
    assert result["autopay_enabled"] is True


def test_enable_auto_pay_unknown_bill():
    result = enable_auto_pay.invoke({"bill_id": "bill_does_not_exist"})
    assert "error" in result
