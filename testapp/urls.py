from django.urls import path

from . import views

app_name = "testapp"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("spending/", views.AnalyticView.as_view(), name="spending"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("ajax/post/url", views.ajax_post, name="ajax_post"),
]
