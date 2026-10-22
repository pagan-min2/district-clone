from django.contrib import admin
from .models import Organization,Event,Slot

admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(Slot)