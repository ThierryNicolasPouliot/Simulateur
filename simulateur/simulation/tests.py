import time
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Company, Scenario, Event, Portfolio, Stock, Cryptocurrency, UserProfile, SimulationSettings
from simulateur.simulation.logic.simulation_manager import SimulationManager

class SimulationTests(TestCase):
    def setUp(self):
        # Set up initial data for tests
        self.admin_user = User.objects.create_user(username='admin', password='password123', is_staff=True)
        self.regular_user = User.objects.create_user(username='user', password='password123')
        self.client = Client()

        # Create SimulationSettings
        self.sim_settings = SimulationSettings.objects.create(
            max_users=100, max_companies=50, timer_step=1, interval=60,
            max_interval=300, fluctuation_rate=0.1, close_stock_market_at_night=True
        )

        # Create a Scenario
        self.scenario = Scenario.objects.create(
            name='ScenarioA', description='Description for ScenarioA',
            backstory='Backstory for ScenarioA', difficulty_level='Easy', 
            duration=3600, simulation_settings=self.sim_settings
        )

        # Create Company, Stock, and Cryptocurrency
        self.company = Company.objects.create(name='TestCompany')
        self.stock = Stock.objects.create(company=self.company, price=10.0)
        self.crypto = Cryptocurrency.objects.create(name='TestCrypto', price=100.0)

        # Create Event with timezone-aware datetime
        self.event = Event.objects.create(
            name='EventA', description='Description for Event A', impact=5.0,
            event_type='TypeA', trigger_date=make_aware(datetime.strptime('2024-06-17 12:00:00', '%Y-%m-%d %H:%M:%S'))
        )

        # Create UserProfile and Portfolio
        self.user_profile = UserProfile.objects.create(user=self.regular_user)
        self.portfolio = Portfolio.objects.create(owner=self.user_profile)
        self.portfolio.stocks.add(self.stock)
        self.portfolio.cryptocurrencies.add(self.crypto)

    def test_company_list_view(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestCompany')

    def test_event_list_view(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EventA')

    def test_buy_stock(self):
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('buy_stock'), {
            'stock_id': self.stock.id,
            'amount': 5,
            'price': 10.0
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_sell_stock(self):
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('sell_stock'), {
            'stock_id': self.stock.id,
            'amount': 5,
            'price': 10.0
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_start_simulation(self):
        self.client.login(username='admin', password='password123')
        simulation_manager = SimulationManager(scenario_id=self.scenario.id, time_unit='second', run_duration=5)
        simulation_manager.start_simulation()
        time.sleep(5)
        simulation_manager.stop_simulation()
        self.assertFalse(simulation_manager.running)

    def test_pause_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('pause_simulation'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'paused')

    def test_fast_forward_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('fast_forward_simulation'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'fast-forwarded')

    def test_rewind_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('rewind_simulation'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'rewinded')
