# simulation/views/event_views.py
from rest_framework import generics
from simulation.models import Event
from simulation.serializers import EventSerializer

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
