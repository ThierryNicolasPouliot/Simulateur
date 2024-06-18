# simulation/views/dashboard_views.py

from django.shortcuts import render
from django.views import View

from .models import UserProfile, Stock, Cryptocurrency, Event, Portfolio, TransactionHistory


class HomeView(View):
    def get(self, request):
        return render(request, 'simulation/home.html')

class DashboardView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        transactions = TransactionHistory.objects.filter(portfolio=user_profile.portfolio)
        stocks = Stock.objects.all()
        cryptos = Cryptocurrency.objects.all()
        context = {
            'portfolio': user_profile.portfolio,
            'transactions': transactions,
            'stocks': stocks,
            'cryptos': cryptos
        }
        return render(request, 'simulation/user_dashboard.html', context)

class TeamDashboardView(View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        team = user_profile.team
        portfolios = Portfolio.objects.filter(team=team)
        context = {
            'team': team,
            'portfolios': portfolios
        }
        return render(request, 'simulation/team_dashboard.html', context)

class MarketOverviewView(View):
    def get(self, request):
        stocks = Stock.objects.all()
        cryptos = Cryptocurrency.objects.all()
        events = Event.objects.all()
        context = {
            'stocks': stocks,
            'cryptos': cryptos,
            'events': events
        }
        return render(request, 'simulation/market_overview.html', context)

class BuySellView(View):
    def get(self, request, stock_id):
        stock = Stock.objects.get(id=stock_id)
        context = {
            'stock': stock
        }
        return render(request, 'simulation/buy_sell.html', context)
