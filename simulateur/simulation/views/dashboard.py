from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from simulation.models import SimulationSettings, UserProfile, Stock, Cryptocurrency, Event, Portfolio, TransactionHistory

class HomeView(View):
    def get(self, request):
        return render(request, 'simulation/home.html')

class UserDashboardView(View):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist
            messages.error(request, "User profile does not exist. Please create your profile.")
            return redirect(reverse('create_user_profile'))  # Redirect to a profile creation page or another appropriate view

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

class AdminDashboardView(View):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        settings = SimulationSettings.objects.first()
        context = {
            'portfolios': portfolios,
            'settings': settings
        }
        return render(request, 'simulation/admin_dashboard.html', context)

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

