from django.db import models
from django.contrib.auth.models import User

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
    