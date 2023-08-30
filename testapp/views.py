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


def spend(request, spending_category_id):
    spending_category = get_object_or_404(Spending_Category, pk=spending_category_id)
    try:
        selected_spending = spending_category.spending_set.get(
            pk=request.POST["spending"]
        )
    except (KeyError, Spending.DoesNotExist):
        return render(
            request,
            "testapp/index.html",
            {
                "spending_categories_list": Spending_Category.objects.all(),
                "error_message": "You didn't select a spending.",
            },
        )
    else:
        selected_spending.spending_amount += 1
        selected_spending.save()
        return HttpResponseRedirect(reverse("testapp:index"))
