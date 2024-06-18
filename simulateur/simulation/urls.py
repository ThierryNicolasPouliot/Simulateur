# simulation/urls.py
from django.urls import path
from .views import (
    HomeView,
    DashboardView,
    MarketOverviewView,
    TeamDashboardView,
    BuySellView,
    CompanyList,
    CompanyCreate,
    ScenarioCreate,
    ScenarioList,
    EventList,
    StartSimulation,
    PauseSimulation,
    StopSimulation,
    FastForwardSimulation,
    RewindSimulation,
    PortfolioView,
    BuyStock,
    SellStock,
    Signup,
    Login,
    SimulationGraphView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('market_overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('team_dashboard/', TeamDashboardView.as_view(), name='team_dashboard'),
    path('buy_sell/<int:stock_id>/', BuySellView.as_view(), name='buy_sell'),
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('companies/create/', CompanyCreate.as_view(), name='company-create'),
    path('scenarios/', ScenarioList.as_view(), name='scenario-list'),
    path('scenarios/create/', ScenarioCreate.as_view(), name='scenario-create'),
    path('events/', EventList.as_view(), name='event-list'),
    path('simulation/start/', StartSimulation.as_view(), name='start-simulation'),
    path('simulation/pause/', PauseSimulation.as_view(), name='pause-simulation'),
    path('simulation/stop/', StopSimulation.as_view(), name='stop-simulation'),
    path('simulation/fast-forward/', FastForwardSimulation.as_view(), name='fast-forward-simulation'),
    path('simulation/rewind/', RewindSimulation.as_view(), name='rewind-simulation'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio-view'),
    path('stock/buy/', BuyStock.as_view(), name='buy-stock'),
    path('stock/sell/', SellStock.as_view(), name='sell-stock'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('graph/', SimulationGraphView.as_view(), name='simulation-graph'),
]
