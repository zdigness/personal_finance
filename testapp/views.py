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

# plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns


from io import BytesIO
import base64

from openai import OpenAI

from decouple import config

from datetime import datetime, timedelta

client = OpenAI(api_key=config("OPENAI_API_KEY"))
bot_messages = []


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
                    Spending.objects.create(
                        user_id=request.user.id,
                        spending_category_id=spending_category.id,
                        spending_amount=amount,
                    )
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
                if request.POST["action"] == "create_debt":
                    amount = request.POST["amount"]
                    account = request.POST["account"]
                    Debt.objects.create(
                        debt_account=account,
                        debt_amount=amount,
                    )
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "log_debt":
                    amount = request.POST["amount"]
                    account = request.POST["account"]
                    debt_account = Debt.objects.get(debt_account=account)
                    debt_account.debt_amount = float(amount)
                    debt_account.save()
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "create_savings":
                    amount = request.POST["amount"]
                    account = request.POST["account"]
                    Savings.objects.create(
                        savings_account=account,
                        savings_amount=amount,
                    )
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "log_savings":
                    amount = request.POST["amount"]
                    account = request.POST["account"]
                    savings_account = Savings.objects.get(savings_account=account)
                    savings_account.savings_amount = float(
                        savings_account.savings_amount
                    ) + float(amount)
                    savings_account.save()
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "edit-category":
                    category = request.POST["category"]
                    name = request.POST["category-name"]
                    budget = request.POST["monthly-budget"]
                    current = request.POST["current-spending"]
                    if budget == "" and current == "" and name == "":
                        return redirect(reverse("testapp:index"))
                    elif budget == "" and current == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(spending_category=name)
                    elif budget == "" and name == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(current_spending=current)
                    elif current == "" and name == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(monthly_budget=budget)
                    elif budget == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(spending_category=name, current_spending=current)
                    elif current == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(spending_category=name, monthly_budget=budget)
                    elif name == "":
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(current_spending=current, monthly_budget=budget)
                    else:
                        Spending_Category.objects.filter(
                            spending_category=category
                        ).update(
                            spending_category=name,
                            monthly_budget=budget,
                            current_spending=current,
                        )
                    return redirect(reverse("testapp:index"))
                if request.POST["action"] == "delete-category":
                    category = request.POST["category"]
                    Spending_Category.objects.filter(
                        spending_category=category
                    ).delete()
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


class AnalyticView(generic.ListView):
    template_name = "testapp/spending.html"
    context_object_name = "spending"

    def get_queryset(self):
        return Spending_Category.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(AnalyticView, self).get_context_data(**kwargs)
        context["piechart"] = get_chart(self.request.user.id)
        context["barchart"] = get_bar_chart(self.request.user.id)
        return context

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                user_input = request.POST["user_input"]
                bot_response = get_response(str(user_input))
                bot_messages.append(bot_response)
                return render(
                    request,
                    "testapp/spending.html",
                    {
                        "user_input": user_input,
                        "bot_messages": bot_messages,
                        "piechart": get_chart(self.request.user.id),
                        "barchart": get_bar_chart(self.request.user.id),
                    },
                )
            else:
                return render(request, "testapp/spending.html")
        else:
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


def get_response(usrText):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": usrText}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()


def get_chart(user_id: int):
    labels = []
    data = []
    queryset = Spending_Category.objects.filter(user_id=user_id)
    for spending_category in queryset:
        labels.append(spending_category.spending_category)
        data.append(spending_category.current_spending)
    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.gcf().set_facecolor("#17141d")
    plt.tight_layout()

    for text in plt.gca().texts:
        text.set_color("white")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode("utf-8")
    buffer.close()
    return graphic


def get_bar_chart(user_id: int):
    # current date and date from 7 days ago
    current_date_time = datetime.now()
    start_date = current_date_time - timedelta(days=6)

    # get all spending objects from the user for past 7 days
    queryset = Spending.objects.filter(user_id=user_id, pub_date__gte=start_date)

    # set labels as the past 7 days
    labels = []
    while start_date <= current_date_time:
        labels.append(start_date.strftime("%m-%d"))
        start_date += timedelta(days=1)

    # set data as the spending amount for each day
    data = [0] * 7
    for spending in queryset:
        index = labels.index(spending.pub_date.strftime("%m-%d"))
        data[index] += spending.spending_amount

    # plot the bar chart
    plt.clf()
    plt.figure(figsize=(6, 6))
    plt.bar(labels, data)
    plt.gcf().set_facecolor("#17141d")
    plt.xlabel("Date", color="white")
    plt.ylabel("Amount Spent", color="white")
    plt.tick_params(axis="x", colors="white")
    plt.tick_params(axis="y", colors="white")

    # save the plot as a png
    bff = BytesIO()
    plt.savefig(bff, format="png")
    bff.seek(0)
    image_png = bff.getvalue()
    barchart = base64.b64encode(image_png)
    barchart = barchart.decode("utf-8")
    bff.close()
    return barchart
