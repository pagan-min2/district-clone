from django import forms
from .models import Event,Slot
from django.utils import timezone

class EventForm(forms.ModelForm) :
    class Meta :
        model = Event
        fields = ["title","description","kind","price","venue"]

class SlotForm(forms.ModelForm) :
    class Meta :
        model = Slot
        fields = ["start_time","end_time","capacity"]

        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")
        capacity = cleaned.get("capacity")
        if start and start <= timezone.now():
            self.add_error("start_time", "Start time must be in the future.")
        if start and end and end <= start:
            self.add_error("end_time", "End time must be after start time.")
        if capacity is not None and capacity < 1:
            self.add_error("capacity", "Capacity must be at least 1.")
        return cleaned