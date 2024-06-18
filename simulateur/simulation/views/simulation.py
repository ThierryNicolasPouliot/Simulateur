from django.shortcuts import render
from django.views import View

class SimulationGraphView(View):
    def get(self, request):
        # Logic to generate the simulation graph
        return render(request, 'simulation/graph.html')