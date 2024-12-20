from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "username"
        self.fields["username"].widget.attrs["placeholder"] = "username"
        self.fields["username"].label = ""
        self.fields["username"].help_text = ""

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "email address"
        self.fields["email"].label = ""
        self.fields["email"].help_text = ""

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "password"
        self.fields["password1"].widget.attrs["placeholder"] = "password"
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = ""

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "confirm password"
        self.fields["password2"].widget.attrs["placeholder"] = "confirm password"
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = ""


class Log_Payment(forms.ModelForm):
    spending_category = forms.CharField(max_length=200)
    monthly_budget = forms.DecimalField(max_digits=10, decimal_places=2)
    current_spending = forms.DecimalField(max_digits=10, decimal_places=2)
