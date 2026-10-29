from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse,HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EventForm,SlotForm
from django.db.models import Count, Sum

from accounts.models import Profile, Transaction
from .models import Event, Slot, Ticket, Organization

def get_organization(user):
    if not user.groups.filter(name="Organizations").exists():
        return None
    return Organization.objects.filter(user=user).first()

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

@login_required
def org_dashboard(request):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organizations only")
    events = org.events.order_by("-created_at")
    return render(request, "events/org_dashboard.html", {"org": org, "events": events})

@login_required
def event_create(request):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organisation Only")
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = org
            event.save()
            return redirect("org_dashboard")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})

@login_required
def slot_create(request, pk):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organizations only")
    event = get_object_or_404(Event, pk=pk, organization=org)
    if request.method == "POST":
        form = SlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.event = event
            slot.save()
            return redirect("org_dashboard")
    else:
        form = SlotForm()
    return render(request, "events/slot_form.html", {"form": form, "event": event})

@login_required
def event_tickets(request, pk):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organizations only")
    event = get_object_or_404(Event, pk=pk, organization=org)
    tickets = (
        Ticket.objects.filter(slot__event=event)
        .select_related("user", "slot")
        .order_by("-created_at")
    )
    return render(request, "events/event_tickets.html", {"event": event, "tickets": tickets})

@login_required
def ticket_consume(request, pk):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organizations only")
    if request.method != "POST":
        return redirect("org_dashboard")
    with transaction.atomic():
        ticket = get_object_or_404(
            Ticket.objects.select_for_update().select_related("slot__event"),
            pk=pk,
            slot__event__organization=org,
        )
        if not ticket.is_consumed:
            ticket.is_consumed = True
            ticket.save()
    return redirect("event_tickets", ticket.slot.event.pk)

@login_required
def org_analytics(request):
    org = get_organization(request.user)
    if org is None:
        return HttpResponseForbidden("Organization Only")
    events = org.events.annotate(
        tickets_sold=Count("slots__tickets"),
        revenue=Sum("slots__tickets__amount_paid"),
    )
    return render(request, "events/org_analytics.html", {"events": events})