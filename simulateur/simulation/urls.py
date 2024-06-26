from django.urls import path, include
from rest_framework.routers import DefaultRouter
from simulation.api.data_modification import CustomStatViewSet, SimulationDataViewSet
from simulation.api.trigger import TriggerViewSet

# Importing HTML views
from simulation.views.dashboard import HomeView, UserDashboardView, AdminDashboardView, TeamDashboardView, MarketOverviewView, BuySellView
from simulation.views.auth import SignupView, LoginView
from simulation.views.simulation import SimulationGraphView
# Importing API views
from simulation.api.company import CompanyViewSet
from simulation.api.scenario import ScenarioViewSet
from simulation.api.event import EventViewSet
from simulation.api.simulation import SimulationSettingsView, StartSimulation, PauseSimulation, StopSimulation, FastForwardSimulation, RewindSimulation
from simulation.api.portfolio import BuyStock, PortfolioView, SellStock

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'scenarios', ScenarioViewSet)
router.register(r'events', EventViewSet)
router.register(r'triggers', TriggerViewSet)
router.register(r'custom_stats', CustomStatViewSet)
router.register(r'simulation_data', SimulationDataViewSet)

html_patterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
        path('team/dashboard/', TeamDashboardView.as_view(), name='team_dashboard'),
    path('market/overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('buy_sell/<int:stock_id>/', BuySellView.as_view(), name='buy_sell'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]

api_patterns = [
    path('simulation/start/', StartSimulation.as_view(), name='start-simulation'),
    path('simulation/pause/', PauseSimulation.as_view(), name='pause-simulation'),
    path('simulation/stop/', StopSimulation.as_view(), name='stop-simulation'),
    path('simulation/fast-forward/', FastForwardSimulation.as_view(), name='fast-forward-simulation'),
    path('simulation/rewind/', RewindSimulation.as_view(), name='rewind-simulation'),
    path('portfolio/<int:user_id>/', PortfolioView.as_view(), name='portfolio-view'),
    path('stock/buy/', BuyStock.as_view(), name='buy-stock'),
    path('stock/sell/', SellStock.as_view(), name='sell-stock'),
    path('graph/', SimulationGraphView.as_view(), name='simulation-graph'),
    path('settings/', SimulationSettingsView.as_view(), name='simulation-settings'),
]

# Combine both HTML and API patterns into a single list
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(api_patterns)),
    path('', include(html_patterns)),
]
