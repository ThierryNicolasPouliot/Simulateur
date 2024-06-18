import time
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from simulation.models import (
    Company, Scenario, Event, Portfolio, Stock, Cryptocurrency,
    UserProfile, SimulationSettings
)
from simulation.logic.simulation_manager import SimulationManagerSingleton
from channels.testing import WebsocketCommunicator
from simulateur.routing import application


class SimulationTests(TestCase):
    def setUp(self):
        # Set up initial data for tests
        self.admin_user = User.objects.create_user(username='admin', password='password123', is_staff=True, is_superuser=True)
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
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestCompany')

    def test_event_list_view(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EventA')

    def test_buy_stock(self):
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('buy-stock'), {
            'stock_id': self.stock.id,
            'amount': 5,
            'price': 10.0
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_sell_stock(self):
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('sell-stock'), {
            'stock_id': self.stock.id,
            'amount': 5,
            'price': 10.0
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_start_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('start-simulation'), {
            'scenario_id': self.scenario.id,
            'time_unit': 'second'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_pause_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('pause-simulation'), {
            'scenario_id': self.scenario.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'paused')

    def test_stop_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('stop-simulation'), {
            'scenario_id': self.scenario.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'stopped')

    def test_fast_forward_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('fast-forward-simulation'), {
            'scenario_id': self.scenario.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'fast-forwarded')

    def test_rewind_simulation(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('rewind-simulation'), {
            'scenario_id': self.scenario.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'rewinded')

    def test_simulation_websocket(self):
        communicator = WebsocketCommunicator(application, f"/ws/simulation/{self.scenario.id}/")
        connected, subprotocol = communicator.connect()
        self.assertTrue(connected)

        # Test sending and receiving messages
        communicator.send_json_to({'message': 'Hello'})
        response = communicator.receive_json_from()
        self.assertEqual(response['message'], 'Hello')

        communicator.disconnect()
