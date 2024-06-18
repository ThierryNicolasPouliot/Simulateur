# simulation/api/data_modification.py
from rest_framework import viewsets
from simulation.models import CustomStat, SimulationData
from simulation.serializers import CustomStatSerializer, SimulationDataSerializer

class CustomStatViewSet(viewsets.ModelViewSet):
    queryset = CustomStat.objects.all()
    serializer_class = CustomStatSerializer

class SimulationDataViewSet(viewsets.ModelViewSet):
    queryset = SimulationData.objects.all()
    serializer_class = SimulationDataSerializer
