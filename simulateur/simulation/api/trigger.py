# simulation/api/trigger.py
from rest_framework import viewsets
from simulation.models import Trigger
from simulation.serializers import TriggerSerializer

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer
