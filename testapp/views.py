from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .models import Spending_Category, Spending, Income, Savings, Debt, Debt_Payment

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import SignUpForm


class IndexView(generic.ListView):
    template_name = "testapp/index.html"
    context_object_name = "spending_categories_list"

    def get_queryset(self):
        return Spending_Category.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["spending"] = Spending.objects.all()
        context["income"] = Income.objects.all()
        context["savings"] = Savings.objects.all()
        context["debt"] = Debt.objects.all()
        context["debt_payment"] = Debt_Payment.objects.all()
        return context

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                if request.POST["action"] == "log_spending":
                    amount = request.POST["amount"]
                    category = request.POST["category"]
                    spending_category = Spending_Category.objects.get(
                        spending_category=category
                    )
                    spending_category.current_spending = float(
                        spending_category.current_spending
                    ) + float(amount)
                    spending_category.save()
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "create_spending":
                    category = request.POST["category-name"]
                    budget = request.POST["monthly-budget"]
                    current = request.POST["current-spending"]
                    Spending_Category.objects.create(
                        user_id=request.user.id,
                        spending_category=category,
                        monthly_budget=budget,
                        current_spending=current,
                    )
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "Submit Debt":
                    amount = request.POST["debt-amount"]
                    account = request.POST["debt-account"]
                    Debt.objects.create(
                        debt_account=account,
                        debt_amount=amount,
                    )
                    return redirect(reverse("testapp:index"))
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect(reverse("testapp:index"))
            else:
                messages.error(request, "Invalid username or password")
                return redirect(reverse("testapp:index"))


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(reverse("testapp:index"))


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registered successfully")
            return redirect(reverse("testapp:index"))
        else:
            return render(request, "testapp/register.html", {"form": form})
    else:
        form = SignUpForm()
        return render(request, "testapp/register.html", {"form": form})
