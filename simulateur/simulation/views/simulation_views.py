# simulation/views/simulation_views.py
import json
import logging
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from simulation.models import Scenario
from simulation.logic.simulation_manager import SimulationManagerSingleton
from simulation.decorators import admin_required

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class StartSimulation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')
            time_unit = data.get('time_unit', 'second')

            simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
            simulation_manager.start_simulation(time_unit)

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
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')

            simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
            simulation_manager.pause_simulation()

            return JsonResponse({'status': 'paused'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            logger.error(f"Error pausing simulation: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class StopSimulation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')

            simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
            simulation_manager.stop_simulation()

            SimulationManagerSingleton.remove_instance(scenario_id)
            return JsonResponse({'status': 'stopped'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            logger.error(f"Error stopping simulation: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FastForwardSimulation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')

            simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
            simulation_manager.fast_forward_simulation()

            return JsonResponse({'status': 'fast-forwarded'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            logger.error(f"Error fast-forwarding simulation: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RewindSimulation(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')

            simulation_manager = SimulationManagerSingleton.get_instance(scenario_id)
            simulation_manager.rewind_simulation()

            return JsonResponse({'status': 'rewinded'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)
        except Exception as e:
            logger.error(f"Error rewinding simulation: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
