# simulation/views/scenario_views.py
from django.utils.decorators import method_decorator
from rest_framework import generics
from django.http import JsonResponse
from simulation.serializers import ScenarioSerializer
from simulation.decorators import admin_required
from simulation.models import Scenario, Event

class ScenarioCreate(generics.CreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class ScenarioList(generics.ListAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer