from django.urls import path

from . import views

app_name = "testapp"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("spending/", views.plot_view, name="spending"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
]
