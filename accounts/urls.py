from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-money/", views.add_money, name="add_money"),
    path("transactions/", views.transactions, name="transactions"),
]