from django.urls import path

from users import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("<user_id>", views.UserIdView.as_view()),
    path("register", views.start_register),
    path("register/<code>", views.verify_register),
    path("login", views.login),
]
