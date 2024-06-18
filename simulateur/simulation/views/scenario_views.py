from rest_framework import generics
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from simulation.models import Scenario, Event
from simulation.serializers import ScenarioSerializer, EventSerializer
from simulation.views import admin_required

class ScenarioCreate(generics.CreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class ScenarioList(generics.ListAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

class EventList(View):
    @method_decorator(admin_required)
    def get(self, request):
        events = list(Event.objects.values())
        return JsonResponse(events, safe=False)
