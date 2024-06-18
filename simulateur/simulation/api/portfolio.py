import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from simulation.models import Portfolio, Stock
from simulation.logic.queue import buy_sell_queue
from simulation.serializers import PortfolioSerializer

class PortfolioView(View):
    def get(self, request, user_id):
        try:
            portfolio = Portfolio.objects.get(owner__user_id=user_id)
            serializer = PortfolioSerializer(portfolio)
            return JsonResponse(serializer.data, safe=False)
        except Portfolio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Portfolio not found'}, status=404)

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
