from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.db import transaction
from .forms import AddMoneyForm
from .models import Profile, Transaction


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            customers, _ = Group.objects.get_or_create(name="Customers")
            user.groups.add(customers)
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

@login_required
def add_money(request):
    if request.method == "POST":
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            with transaction.atomic():
                profile = Profile.objects.select_for_update().get(user=request.user)
                profile.balance += amount
                profile.save(update_fields=["balance"])
                Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    kind=Transaction.Kind.CREDIT,
                    description="Wallet top-up",
                )
            return redirect("transactions")
    else:
        form = AddMoneyForm()
    return render(request, "accounts/add_money.html", {"form": form})


@login_required
def transactions(request):
    history = request.user.transactions.all()
    return render(request, "accounts/transactions.html", {"history": history})