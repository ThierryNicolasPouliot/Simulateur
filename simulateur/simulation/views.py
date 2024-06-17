from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from rest_framework import generics
from .models import Company, Scenario, Event, Portfolio, Stock, Cryptocurrency, TransactionHistory, SimulationSettings, UserProfile
from .serializers import CompanySerializer, ScenarioSerializer, EventSerializer, PortfolioSerializer, StockSerializer, CryptocurrencySerializer
from .queue import buy_sell_queue
from django.shortcuts import render
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda user: user.is_staff)(view_func)
    return decorated_view_func

class CompanyList(View):
    @method_decorator(admin_required)
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
            time_unit = data.get('time_unit', 'second')  # Default to 'second' if not provided

            # Instantiate the simulation manager with the provided scenario_id and time_unit
            from .simulation_manager import SimulationManager
            simulation_manager = SimulationManager(scenario_id, time_unit)
            simulation_manager.start_simulation()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Scenario.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Scenario not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class PauseSimulation(View):
    def post(self, request):
        # Logic to pause the simulation
        # This will depend on how your simulation manager handles pausing
        return JsonResponse({'status': 'paused'})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FastForwardSimulation(View):
    def post(self, request):
        # Logic to fast forward the simulation
        # This will depend on how your simulation manager handles fast forwarding
        return JsonResponse({'status': 'fast-forwarded'})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class RewindSimulation(View):
    def post(self, request):
        # Logic to rewind the simulation
        # This will depend on how your simulation manager handles rewinding
        return JsonResponse({'status': 'rewinded'})

class PortfolioView(View):
    def get(self, request, user_id):
        portfolio = Portfolio.objects.get(owner__user_id=user_id)
        serializer = PortfolioSerializer(portfolio)
        return JsonResponse(serializer.data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class BuyStock(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user.userprofile  # Assuming you have user profile linked to user
            stock = Stock.objects.get(id=data['stock_id'])
            amount = data['amount']
            price = data['price']
            buy_sell_queue.add_to_buy_queue(user, stock, amount, price)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class SellStock(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user.userprofile  # Assuming you have user profile linked to user
            stock = Stock.objects.get(id=data['stock_id'])
            amount = data['amount']
            price = data['price']
            buy_sell_queue.add_to_sell_queue(user, stock, amount, price)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class Signup(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user)
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)


class SimulationGraphView(View):
    def get(self, request):
        return render(request, 'simulation/graph.html')

class SimulationGraphImageView(View):
    def get(self, request):
        fig, ax = plt.subplots()
        canvas = FigureCanvas(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        return response