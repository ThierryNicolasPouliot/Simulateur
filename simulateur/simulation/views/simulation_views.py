# simulation/views/simulation_views.py

import json
import logging
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from simulation.views import admin_required

from .models import Company, Scenario, Event, Stock
from .serializers import CompanySerializer, ScenarioSerializer, EventSerializer
from .logic.simulation_manager import SimulationManager

logger = logging.getLogger(__name__)

class CompanyList(View):
    def get(self, request):
        companies = list(Company.objects.values())
        return JsonResponse(companies, safe=False)

class CompanyCreate(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class StartSimulation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')
            time_unit = data.get('time_unit', 'second')

            simulation_manager = SimulationManager(scenario_id, time_unit)
            simulation_manager.start_simulation()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            logger.error(f"Error starting simulation: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class PauseSimulation(View):
    def post(self, request):
        # Logic to pause the simulation
        return JsonResponse({'status': 'paused'})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class StopSimulation(View):
    def post(self, request):
        if scenario_id := request.session.get('scenario_id'):
            try:
                scenario = Scenario.objects.get(id=scenario_id)
                scenario.running = False
                scenario.save()
                return JsonResponse({'status': 'stopped'})
            except Scenario.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        return JsonResponse({'status': 'error', 'message': 'No scenario found'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FastForwardSimulation(View):
    def post(self, request):
        # Logic to fast forward the simulation
        return JsonResponse({'status': 'fast-forwarded'})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RewindSimulation(View):
    def post(self, request):
        # Logic to rewind the simulation
        return JsonResponse({'status': 'rewinded'})
