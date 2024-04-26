import pytest

# Import Models
from .models import Spending_Category, Spending, Income, Savings, Debt, Debt_Payment


# Test Models
@pytest.mark.django_db
def test_spending_category():
    spending_category = Spending_Category.objects.create(
        spending_category="Groceries", monthly_budget=200.00, current_spending=150.00
    )
    assert Spending_Category.objects.count() == 1
    assert spending_category.spending_category == "Groceries"
    assert spending_category.monthly_budget == 200.00
    assert spending_category.current_spending == 150.00


def test_spending():
    spending_category = Spending_Category.objects.create(
        spending_category="Groceries", monthly_budget=200.00, current_spending=150.00
    )
    spending = Spending.objects.create(
        spending_category=spending_category, spending_amount=50.00
    )
    assert Spending.objects.count() == 1
    assert spending.spending_category == spending_category
    assert spending.spending_amount == 50.00


def test_income():
    income = Income.objects.create(income_amount=1000.00)
    assert Income.objects.count() == 1
    assert income.income_amount == 1000.00


def test_savings():
    savings = Savings.objects.create(savings_amount=500.00)
    assert Savings.objects.count() == 1
    assert savings.savings_amount == 500.00


def test_debt():
    debt = Debt.objects.create(debt_account="Credit Card", debt_amount=1000.00)
    assert Debt.objects.count() == 1
    assert debt.debt_account == "Credit Card"
    assert debt.debt_amount == 1000.00


def test_debt_payment():
    debt = Debt.objects.create(debt_account="Credit Card", debt_amount=1000.00)
    debt_payment = Debt_Payment.objects.create(debt=debt, debt_payment_amount=100.00)
    assert Debt_Payment.objects.count() == 1
    assert debt_payment.debt == debt
    assert debt_payment.debt_payment_amount == 100.00
