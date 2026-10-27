from django.db import models
from django.contrib.auth.models import User
import uuid

class Organization(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='organization')
    name = models.CharField(max_length=100)
    description = models.TextField(default="")

    def __str__(self):
        return self.name
    
class Event(models.Model):
    
    class Kind(models.TextChoices):
        slot_based = "SLOT-BASED","Slot-Based"
        ticket_based = "TICKET-BASED","Ticket-Based"

    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name='events')
    title = models.CharField(max_length=150)
    description = models.TextField()
    kind = models.CharField( max_length=12, choices=Kind.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    venue = models.CharField( max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Slot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    booked_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.event} at {self.start_time}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'tickets')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name = 'tickets')
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ticket_id)
