from django.urls import path
from .views import CompanyList, EventList, StartSimulation, PauseSimulation, FastForwardSimulation, RewindSimulation, CompanyCreate, ScenarioCreate, ScenarioList, PortfolioView, BuyStock, SellStock, Signup, Login

urlpatterns = [
    path('companies/', CompanyList.as_view(), name='company-list'),
    path('companies/create/', CompanyCreate.as_view(), name='company-create'),
    path('events/', EventList.as_view(), name='event-list'),
    path('start_simulation/', StartSimulation.as_view(), name='start-simulation'),
    path('pause_simulation/', PauseSimulation.as_view(), name='pause-simulation'),
    path('fast_forward_simulation/', FastForwardSimulation.as_view(), name='fast-forward-simulation'),
    path('rewind_simulation/', RewindSimulation.as_view(), name='rewind-simulation'),
    path('scenarios/create/', ScenarioCreate.as_view(), name='scenario-create'),
    path('scenarios/', ScenarioList.as_view(), name='scenario-list'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio-view'),
    path('buy_stock/', BuyStock.as_view(), name='buy-stock'),
    path('sell_stock/', SellStock.as_view(), name='sell-stock'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
]
