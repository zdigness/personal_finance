from django.contrib import admin
from .models import Spending_Category, Spending, Income, Savings, Debt, Debt_Payment

# Register your models here.
admin.site.register(Spending_Category)
admin.site.register(Spending)
admin.site.register(Income)
admin.site.register(Savings)
admin.site.register(Debt)
admin.site.register(Debt_Payment)
