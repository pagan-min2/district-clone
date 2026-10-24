from django.shortcuts import render
from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

@login_required
def event_list (request):
    active_events = Event.objects.filter(is_active=True).order_by("-created_at")
    return render(request,'events/event_list.html',{"events":active_events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    slots = event.slots.order_by("start_time")
    return render(request, "events/event_detail.html", {"event": event, "slots": slots})