# simulation/api/company.py
from rest_framework import viewsets
from simulation.models import Company
from simulation.serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
