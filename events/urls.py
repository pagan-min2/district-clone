from django.urls import path
from . import views

urlpatterns = [
    path("",views.event_list,name = "event_list"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("slot/<int:pk>/book/", views.book_slot, name="book_slot"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("org/", views.org_dashboard, name="org_dashboard"),
]