from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Spending_Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    spending_category = models.CharField(max_length=200)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2)
    current_spending = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.spending_category


class Spending(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    spending_category = models.ForeignKey(Spending_Category, on_delete=models.CASCADE)
    spending_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.spending_description


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.income_amount


class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    savings_account = models.CharField(max_length=200, default="Savings")
    savings_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.savings_amount)


class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    debt_account = models.CharField(max_length=200)
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.debt_amount


class Debt_Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    debt_payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.debt_payment_amount


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    message = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=200, default="user")

    def __str__(self):
        return self.message
