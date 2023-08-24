from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Spending_Category, Spending, Income, Savings, Debt, Debt_Payment


class IndexView(generic.ListView):
    template_name = "testapp/index.html"
    context_object_name = "spending_categories_list"

    def get_queryset(self):
        return Spending_Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["spending"] = Spending.objects.all()
        context["income"] = Income.objects.all()
        context["savings"] = Savings.objects.all()
        context["debt"] = Debt.objects.all()
        context["debt_payment"] = Debt_Payment.objects.all()
        return context
