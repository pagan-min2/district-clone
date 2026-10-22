from django.shortcuts import render
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required
def event_list (request):
    active_events = Event.objects.filter(is_active=True).order_by("-created_at")
    return render(request,'events/event_list.html',{"events":active_events})