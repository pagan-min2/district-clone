from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile, Transaction
from .models import Event, Slot, Ticket

@login_required
def event_list (request):
    active_events = Event.objects.filter(is_active=True).order_by("-created_at")
    return render(request,'events/event_list.html',{"events":active_events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    slots = event.slots.order_by("start_time")
    return render(request, "events/event_detail.html", {"event": event, "slots": slots})

@login_required
def book_slot(request, pk):
    if request.method != "POST":
        return redirect("event_list")
    with transaction.atomic():
        slot = Slot.objects.select_for_update().get(pk=pk)
        profile = Profile.objects.select_for_update().get(user=request.user)
        price = slot.event.price
        if slot.booked_count >= slot.capacity:
            return HttpResponse("Slot is full")
        if profile.balance < price:
            return HttpResponse("Not enough balance")
        slot.booked_count += 1
        slot.save()
        profile.balance -= price
        profile.save()
        Transaction.objects.create(
            user=request.user,
            amount=price,
            kind=Transaction.Kind.DEBIT,
            description="Booked " + slot.event.title,
        )
        Ticket.objects.create(user=request.user, slot=slot, amount_paid=price)
    return redirect("my_tickets")


@login_required
def my_tickets(request):
    tickets = request.user.tickets.filter(is_consumed=False)
    return render(request, "events/my_tickets.html", {"tickets": tickets})