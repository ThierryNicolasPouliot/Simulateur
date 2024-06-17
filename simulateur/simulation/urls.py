from django.urls import path
from .views import (
    CompanyList, CompanyCreate, ScenarioCreate, ScenarioList, EventList,
    StartSimulation, PauseSimulation, FastForwardSimulation, RewindSimulation,
    PortfolioView, BuyStock, SellStock, Signup, Login, SimulationGraphView, SimulationGraphImageView
)

urlpatterns = [
    path('companies/', CompanyList.as_view(), name='company_list'),
    path('companies/create/', CompanyCreate.as_view(), name='company_create'),
    path('scenarios/create/', ScenarioCreate.as_view(), name='scenario_create'),
    path('scenarios/', ScenarioList.as_view(), name='scenario_list'),
    path('events/', EventList.as_view(), name='event_list'),
    path('simulation/start/', StartSimulation.as_view(), name='start_simulation'),
    path('simulation/pause/', PauseSimulation.as_view(), name='pause_simulation'),
    path('simulation/fast-forward/', FastForwardSimulation.as_view(), name='fast_forward_simulation'),
    path('simulation/rewind/', RewindSimulation.as_view(), name='rewind_simulation'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio_view'),
    path('stock/buy/', BuyStock.as_view(), name='buy_stock'),
    path('stock/sell/', SellStock.as_view(), name='sell_stock'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('graph/', SimulationGraphView.as_view(), name='simulation_graph'),
    path('graph/image/', SimulationGraphImageView.as_view(), name='simulation_graph_image'),
]
