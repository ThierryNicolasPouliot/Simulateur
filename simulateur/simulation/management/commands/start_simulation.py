from django.core.management.base import BaseCommand
from simulation.simulation_manager import SimulationManager

class Command(BaseCommand):
    help = 'Start the simulation based on a scenario'

    def add_arguments(self, parser):
        parser.add_argument('scenario_id', type=int, help='The ID of the scenario to simulate')

    def handle(self, *args, **kwargs):
        scenario_id = kwargs['scenario_id']
        simulation_manager = SimulationManager(scenario_id)
        simulation_manager.start_simulation()
