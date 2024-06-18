# simulation/api/scenario.py
from rest_framework import viewsets
from simulation.models import Scenario
from simulation.serializers import ScenarioSerializer

class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
