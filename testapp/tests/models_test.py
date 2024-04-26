import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_finance.settings")
django.setup()

import pytest
from django.contrib.auth.models import User
from ..models import Spending_Category, Spending, Income, Savings, Debt, Debt_Payment


# Create Dummy Model Instances
@pytest.fixture
def user():
    user = User.objects.get_or_create(
        username="testuser", email="test@test.com", password="testpassword"
    )

    return user[0]


@pytest.fixture()
def spending_category(user):
    spending_category = Spending_Category.objects.get_or_create(
        user=user,
        spending_category="Groceries",
        monthly_budget=200.00,
        current_spending=150.00,
    )

    return spending_category[0]


@pytest.fixture()
def spending(user, spending_category):
    spending = Spending.objects.get_or_create(
        user=user, spending_category=spending_category, spending_amount=50.00
    )

    return spending[0]


@pytest.fixture()
def income(user):
    income = Income.objects.get_or_create(user=user, income_amount=1000.00)

    return income[0]


@pytest.fixture()
def savings(user):
    savings = Savings.objects.get_or_create(user=user, savings_amount=500.00)

    return savings[0]


@pytest.fixture()
def debt(user):
    debt = Debt.objects.get_or_create(
        user=user, debt_account="Credit Card", debt_amount=1000.00
    )

    return debt[0]


@pytest.fixture()
def debt_payment(user, debt):
    debt_payment = Debt_Payment.objects.get_or_create(
        user=user, debt=debt, debt_payment_amount=100.00
    )

    return debt_payment[0]


# Test Models
@pytest.mark.django_db
def test_user(user):

    assert User.objects.count() == 1
    assert user.username == "testuser"
    assert user.email == "test@test.com"
    assert user.password == "testpassword"


@pytest.mark.django_db
def test_spending_category(spending_category):
    assert Spending_Category.objects.count() == 1
    assert spending_category.spending_category == "Groceries"
    assert spending_category.monthly_budget == 200.00
    assert spending_category.current_spending == 150.00


@pytest.mark.django_db
def test_spending(spending, spending_category):
    assert Spending.objects.count() == 1
    assert spending.spending_category == spending_category
    assert spending.spending_amount == 50.00


@pytest.mark.django_db
def test_income(income):
    assert Income.objects.count() == 1
    assert income.income_amount == 1000.00


@pytest.mark.django_db
def test_savings(savings):
    assert Savings.objects.count() == 1
    assert savings.savings_amount == 500.00


@pytest.mark.django_db
def test_debt(debt):
    assert Debt.objects.count() == 1
    assert debt.debt_account == "Credit Card"
    assert debt.debt_amount == 1000.00


@pytest.mark.django_db
def test_debt_payment(debt_payment, debt):
    assert Debt_Payment.objects.count() == 1
    assert debt_payment.debt == debt
    assert debt_payment.debt_payment_amount == 100.00
