from rest_framework import generics
from django.http import JsonResponse
from django.views import View
from simulation.models import Company
from simulation.serializers import CompanySerializer

class CompanyList(View):
    def get(self, request):
        companies = list(Company.objects.values())
        return JsonResponse(companies, safe=False)

class CompanyCreate(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
