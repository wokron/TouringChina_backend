from django.urls import path

from users import views

urlpatterns = [
    path("hello/", views.hello),
    path("register", views.start_register),
    path("register/<code>", views.verify_register),
    path("login", views.login),
]
