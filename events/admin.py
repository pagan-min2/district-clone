from django.contrib import admin
from .models import Organization,Event,Slot,Ticket

admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(Slot)
admin.site.register(Ticket)