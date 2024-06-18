# simulation/api/event.py
from rest_framework import viewsets
from simulation.models import Event
from simulation.serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
